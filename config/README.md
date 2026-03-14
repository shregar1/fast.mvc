# Config override (main repo)

Config is loaded from this directory so you can **override package defaults** without changing package code.

## How it works

1. **`FASTMVC_CONFIG_BASE`** is set at startup (in `start_utils`) to this directory (`config/`).
2. Each package (e.g. `fastmvc_core`, `fastmvc_kafka`, `fastmvc_webrtc`, `fastmvc_channels`) resolves config paths in this order:
   - **`FASTMVC_<NAME>_CONFIG_PATH`** – explicit path (e.g. `FASTMVC_DB_CONFIG_PATH=/etc/myapp/db.json`)
   - **`{FASTMVC_CONFIG_BASE}/{name}/config.json`** – this repo’s override (e.g. `config/db/config.json`)
   - **`config/{name}/config.json`** – cwd-relative default

So any JSON file you add or edit under `config/<name>/config.json` in the main repo **overrides** the package default for that feature.

## Layout

```
config/
├── README.md           ← this file
├── db/
│   └── config.json     ← DB (fastmvc_core)
├── cache/
│   └── config.json     ← Redis cache (fastmvc_core)
├── dynamo/
│   └── config.json     ← DynamoDB (fastmvc_core)
├── kafka/
│   └── config.json     ← Kafka (fastmvc_kafka)
├── webrtc/
│   └── config.json     ← WebRTC (fastmvc_webrtc)
├── channels/
│   └── config.json     ← Channels (fastmvc_channels)
└── ...                 ← other configs (configurations/* in main)
```

## Overriding a single config via env

To point one config to a different file (e.g. for tests or multiple envs):

```bash
export FASTMVC_DB_CONFIG_PATH=/etc/myapp/db.json
export FASTMVC_KAFKA_CONFIG_PATH=./config/kafka/prod.json
```

## Moving more config into packages

Configurations that still live in `fast_mvc_main/configurations/` can be moved to their respective packages (e.g. `fastmvc_core`) using the same pattern: loader in the package, path from `FASTMVC_<X>_CONFIG_PATH` or `FASTMVC_CONFIG_BASE/<name>/config.json`. This directory remains the place to override in the main repo.
