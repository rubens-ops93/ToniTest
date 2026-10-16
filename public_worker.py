"""Generic bounded polling worker. Private files and subprocess output stay private."""
import base64
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

def cadence(poll,cycles,interval=480,clock=time.monotonic,sleep=time.sleep):
    start=clock();results=[]
    for index in range(cycles):
        target=start+index*interval
        while clock()<target:sleep(min(60,target-clock()))
        results.append(poll(index))
    return results

def run(args,cwd=None,check=True,env=None):
    return subprocess.run(args,cwd=cwd,check=check,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def main():
    root=None;stage='configuration'
    try:
        for key in ('PRIVATE_REPOSITORY','PRIVATE_REPO_TOKEN','TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID'):
            if not os.environ.get(key):raise RuntimeError('Missing configuration')
        repo=os.environ['PRIVATE_REPOSITORY']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise RuntimeError('Invalid configuration')
        auth=base64.b64encode(('x-access-token:'+os.environ['PRIVATE_REPO_TOKEN']).encode()).decode()
        git=['git','-c','http.https://github.com/.extraheader=AUTHORIZATION: basic '+auth]
        root=tempfile.mkdtemp(prefix='private-worker-');app=Path(root)/'app'
        stage='private access'
        run(git+['clone','--quiet','--depth','1','--branch','main','https://github.com/'+repo+'.git',str(app)])
        stage='dependencies'
        run([sys.executable,'-m','venv',str(Path(root)/'venv')])
        python=str(Path(root)/'venv/bin/python')
        run([python,'-m','pip','install','--quiet','youtube-transcript-api==1.2.4'])
        run(['git','config','user.name','github-actions[bot]'],app)
        run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'],app)
        def poll(index):
            nonlocal stage
            stage='private update';run(git+['pull','--quiet','--rebase','origin','main'],app)
            stage='validation';run([python,'-m','unittest','discover','-s','tests'],app)
            stage='application'
            code=run([python,'run_cycle.py'],app,check=False).returncode
            stage='private state persistence'
            paths=[p for p in ('data/state.json','data/health.json','data/transcripts','data/summary_budget.json') if (app/p).exists()]
            if paths:run(['git','add',*paths],app)
            changed=run(['git','diff','--cached','--quiet'],app,check=False).returncode
            if changed not in (0,1):raise RuntimeError('State check failed')
            if changed:
                run(['git','commit','--quiet','-m','Update private monitor state'],app)
                for attempt in range(3):
                    try:
                        run(git+['pull','--quiet','--rebase','origin','main'],app)
                        run(git+['push','--quiet','origin','main'],app);break
                    except subprocess.CalledProcessError:
                        if attempt==2:raise
                        time.sleep((attempt+1)*5)
            print('Cycle '+str(index+1)+(' completed.' if code==0 else ' recorded with application error.'),flush=True)
            return code
        cycles=max(1,min(int(os.getenv('WORKER_CYCLES','4')),4))
        results=cadence(poll,cycles)
        print('Worker block completed.',flush=True)
        return 1 if any(results) else 0
    except Exception:
        print('Worker failed during '+stage+'; private diagnostic output is suppressed.',flush=True)
        return 1
    finally:
        if root:shutil.rmtree(root,ignore_errors=True)

if __name__=='__main__':raise SystemExit(main())
