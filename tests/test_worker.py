import unittest
from public_worker import cadence

class CadenceTests(unittest.TestCase):
    def test_four_polls_keep_eight_minute_spacing(self):
        clock=[0];starts=[]
        def sleep(seconds):clock[0]+=seconds
        def poll(index):starts.append(clock[0]);clock[0]+=20;return 0
        self.assertEqual(cadence(poll,4,clock=lambda:clock[0],sleep=sleep),[0,0,0,0])
        self.assertEqual(starts,[0,480,960,1440])

    def test_failed_cycle_does_not_prevent_later_checks(self):
        clock=[0]
        def sleep(seconds):clock[0]+=seconds
        self.assertEqual(cadence(lambda i:1 if i==0 else 0,2,clock=lambda:clock[0],sleep=sleep),[1,0])

if __name__=='__main__':unittest.main()
