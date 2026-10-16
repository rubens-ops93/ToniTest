# Generic private-application worker

This public repository contains only a generic launcher and its cadence tests. Application code, configuration, portfolio data, transcripts, health and notification delivery checkpoints remain in a separately maintained private repository. No private subprocess output, artifacts or caches are published. Public observers can see this repository, its owner and workflow timing/status.

The scheduler requests a block twice an hour, at minute 03 and 33 UTC. Each started scheduled/manual block performs four private application checks, eight minutes apart, and persists state after each check even if the application reports an error. Publication checks perform one cycle. A block is bounded to 40 minutes. GitHub may delay block starts and transitions; this is not a guaranteed always-on service. Standard ubuntu-latest runners are used.

Required Actions secrets: PRIVATE_REPOSITORY, PRIVATE_REPO_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. The private token should be fine-grained, Contents read/write on only the private application repository, with an expiration date. Keep the former private automatic scheduler disabled. The private application entry point is run_cycle.py, and its tests run before each check.

Optional paid source-content analysis stays off unless an API key, an explicit model and ALLOW_PAID_SUMMARIES=true are all configured. A daily request cap is separate from any monetary budget. Never set that flag without the owner's cost approval.

No pull-request triggers. Never grant write access to untrusted contributors, enable debug logging for private processes, or publish private artifacts/caches. The temporary checkout is removed when the block exits. Private output remains suppressed; only generic cycle status is printed.
