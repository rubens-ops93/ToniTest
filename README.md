# Scheduled worker

A generic eight-minute scheduler for a separately maintained private application.

Only this launcher is public. Application code, configuration, portfolio data, transcripts and state are stored in a private repository. No private output, artifacts or caches are published by this workflow. Public observers can see this repository, its owner and workflow timing/status.

The workflow is disabled until the repository variable `ENABLED` is set to `true`. It requires the Actions secrets `PRIVATE_REPOSITORY`, `PRIVATE_REPO_TOKEN`, `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. The private-repository credential should be a fine-grained token restricted to that one repository, with Contents read/write permission and an expiration date.

There are no pull-request triggers. Contributors must not be granted write access unless trusted with the private application and its credentials. Never enable Actions debug logging or add public logs, caches or artifacts containing private application output.

Migration requires stopping the old scheduler before enabling this worker, manually testing one run, and verifying successful private state persistence before relying on the schedule. GitHub scheduled starts can be delayed. Eight-minute polling does not imply a notification every eight minutes.
