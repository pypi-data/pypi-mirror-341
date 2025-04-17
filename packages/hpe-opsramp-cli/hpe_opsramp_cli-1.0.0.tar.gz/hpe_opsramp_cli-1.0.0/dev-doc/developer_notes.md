## Dependency tree
hpe-opsramp-cli v1.0.0

├── pipreqs v0.5.0

│   ├── docopt v0.6.2

│   ├── ipython v8.12.3

│   │   ├── backcall v0.2.0

│   │   ├── colorama v0.4.6

│   │   ├── decorator v5.2.1

│   │   ├── jedi v0.19.2

│   │   │   └── parso v0.8.4

│   │   ├── matplotlib-inline v0.1.7

│   │   │   └── traitlets v5.14.3

│   │   ├── pickleshare v0.7.5

│   │   ├── prompt-toolkit v3.0.50

│   │   │   └── wcwidth v0.2.13

│   │   ├── pygments v2.19.1

│   │   ├── stack-data v0.6.3

│   │   │   ├── asttokens v3.0.0

│   │   │   ├── executing v2.2.0

│   │   │   └── pure-eval v0.2.3

│   │   └── traitlets v5.14.3

│   ├── nbconvert v7.16.6

│   │   ├── beautifulsoup4 v4.13.3

│   │   │   ├── soupsieve v2.6

│   │   │   └── typing-extensions v4.12.2

│   │   ├── bleach\[css\] v6.2.0

│   │   │   ├── webencodings v0.5.1

│   │   │   └── tinycss2 v1.4.0 (extra: css)

│   │   │       └── webencodings v0.5.1

│   │   ├── defusedxml v0.7.1

│   │   ├── jinja2 v3.1.6

│   │   │   └── markupsafe v3.0.2

│   │   ├── jupyter-core v5.7.2

│   │   │   ├── platformdirs v4.3.6

│   │   │   ├── pywin32 v308

│   │   │   └── traitlets v5.14.3

│   │   ├── jupyterlab-pygments v0.3.0

│   │   ├── markupsafe v3.0.2

│   │   ├── mistune v3.1.2

│   │   ├── nbclient v0.10.2

│   │   │   ├── jupyter-client v8.6.3

│   │   │   │   ├── jupyter-core v5.7.2 (\*)

│   │   │   │   ├── python-dateutil v2.9.0.post0

│   │   │   │   │   └── six v1.17.0

│   │   │   │   ├── pyzmq v26.2.1

│   │   │   │   ├── tornado v6.4.2

│   │   │   │   └── traitlets v5.14.3

│   │   │   ├── jupyter-core v5.7.2 (\*)

│   │   │   ├── nbformat v5.10.4

│   │   │   │   ├── fastjsonschema v2.21.1

│   │   │   │   ├── jsonschema v4.23.0

│   │   │   │   │   ├── attrs v25.1.0

│   │   │   │   │   ├── jsonschema-specifications v2024.10.1

│   │   │   │   │   │   └── referencing v0.36.2

│   │   │   │   │   │       ├── attrs v25.1.0

│   │   │   │   │   │       ├── rpds-py v0.23.1

│   │   │   │   │   │       └── typing-extensions v4.12.2

│   │   │   │   │   ├── referencing v0.36.2 (\*)

│   │   │   │   │   └── rpds-py v0.23.1

│   │   │   │   ├── jupyter-core v5.7.2 (\*)

│   │   │   │   └── traitlets v5.14.3

│   │   │   └── traitlets v5.14.3

│   │   ├── nbformat v5.10.4 (\*)

│   │   ├── packaging v24.2

│   │   ├── pandocfilters v1.5.1

│   │   ├── pygments v2.19.1

│   │   └── traitlets v5.14.3

│   └── yarg v0.1.9

│       └── requests v2.32.3

│           ├── certifi v2025.1.31

│           ├── charset-normalizer v3.4.1

│           ├── idna v3.10

│           └── urllib3 v2.3.0

├── pytest v8.3.5

│   ├── colorama v0.4.6

│   ├── iniconfig v2.0.0

│   ├── packaging v24.2

│   └── pluggy v1.5.0

├── pywin32 v308

├── pyyaml v6.0.2

├── requests v2.32.3 (\*)

├── rich v13.9.4

│   ├── markdown-it-py v3.0.0

│   │   └── mdurl v0.1.2

│   └── pygments v2.19.1

├── ruff v0.9.10

├── typer v0.15.1

│   ├── click v8.1.8

│   │   └── colorama v0.4.6

│   ├── rich v13.9.4 (\*)

│   ├── shellingham v1.5.4

│   └── typing-extensions v4.12.2

└── typing-extensions v4.12.2

(\*) Package tree already displayed

## Testing using pytest 
uv run -m pytest

## docker jaeger command
docker run --hostname=493b047f6c2a --user=10001 --mac-address=02:42:ac:11:00:02 --env=COLLECTOR_OTLP_ENABLED=true --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=SAMPLING_STRATEGIES_FILE=/etc/jaeger/sampling_strategies.json --volume=/tmp --network=bridge --workdir=/ -p 14268:14268 -p 16686:16686 -p 4317:4317 -p 4318:4318 --restart=no --runtime=runc -d jaegertracing/all-in-one

docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.29


  
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest

  ## How to run CLI command during developemnt
  uv run -m  pytest  --disable-warnings -s -k "test_unmanage_alert_resources_help"

  ## test report as on 22-03-2025 06:12
 ============================================================ short test summary info ============================================================= 
FAILED tests/hpe_opsramp_cli_test/test_main.py::test_log_level - assert 2 == 0
FAILED tests/hpe_opsramp_cli_test/test_opsramp_environment.py::test_get_env_aboslute_path - SystemExit: 1
FAILED tests/hpe_opsramp_cli_test/test_opsramp_environment.py::test_do_post - TypeError: can only concatenate str (not "NoneType") to str
FAILED tests/hpe_opsramp_cli_test/test_unmanage_alert_resources.py::test_unmanage_alert_resources_absolute_path - assert 1 == 0
============================================== 4 failed, 14 passed, 2 warnings in 72.46s (0:01:12) =============================================== 

## otel spam is printed in test 
F
tests\hpe_opsramp_cli_test\test_opsramp_environment.py .{
    "name": "example-span",
    "context": {
        "trace_id": "0xebffc87aa401de20e3b7e1194f5e5bfa",
        "span_id": "0xee3faf6f723952da",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2025-03-22T00:51:38.987785Z",
    "end_time": "2025-03-22T00:51:38.988419Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "example-attribute": "value"
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.31.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}

## test module locally
Navigate to your project root and install your package locally:
uv pip install --editable .
opsramp-cli.exe --log-level DEBUG 
Usage: opsramp-cli [OPTIONS] COMMAND [ARGS]...
Try 'opsramp-cli --help' for help.
╭─ Error ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮│ Missing command.                                                                                                                                                │╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯(hpe-opsramp-cli) PS C:\Users\vetrivel\src\GitHub-HPE-OpsRamp-CLI\hpe-opsramp-cli> 

## Opsramp-cli commands
opsramp-cli.exe --log-level DEBUG unmanage_alert_resources --env UAT_National_INC --opsql-file .\dev-doc\uat-partner-opsql.json
uv run -m  pytest  --disable-warnings -s -k "test_singleton_debug_log1"

## debug
2025-03-25 20:38:30,633 - hpe_opsramp_cli.singleton_logger - DEBUG - cli_utils - unmanage_resources_progress_bar_partner - 162 - For loop on per_client_alert_only_resoures: 

{
    "b1838501-9d66-4c09-99e0-7db0b8812a7e": [
        "f9427f70-d76e-4c1d-b585-5068c3306093",
        "f53e6c1f-df66-4be0-9462-1fdf0d59b795",
        "ed1ad8d5-6c7f-4f61-b3de-f257847eaa64",
        "6777387a-df21-4523-b294-fcb134897731",
        "9814b490-8e61-4cfc-8919-8b24c4339088",
    ],
    "649c8df6-569e-4aab-8b1d-c132290b602c": [
        "65443f03-6c07-4be9-a69f-6a898c1dcd90",
        "7eb11544-b924-458d-8101-9bcb9b3da324",
    ],
    "cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd": [
        "5d4cac04-a8b0-4a73-bfb4-d1db9e8a7867",
        "93a90c21-bd56-4674-9790-801b38c51e95",
        "d47807a1-71da-4c79-b8ef-643cc581501c",
        "d92c999d-eace-4502-884f-4ac8799dfc08",
    ],
}


Key: b1838501-9d66-4c09-99e0-7db0b8812a7e 
Value: 
[
    "f9427f70-d76e-4c1d-b585-5068c3306093",
    "f53e6c1f-df66-4be0-9462-1fdf0d59b795",
    "ed1ad8d5-6c7f-4f61-b3de-f257847eaa64",
    "6777387a-df21-4523-b294-fcb134897731",
    "9814b490-8e61-4cfc-8919-8b24c4339088",
]

## debugging for keys, value loop
2025-03-25 20:38:30,633 - hpe_opsramp_cli.singleton_logger - DEBUG - cli_utils - unmanage_resources_progress_bar_partner - 162 - For loop on per_client_alert_only_resoures: 
{'b1838501-9d66-4c09-99e0-7db0b8812a7e': ['f9427f70-d76e-4c1d-b585-5068c3306093', 'f53e6c1f-df66-4be0-9462-1fdf0d59b795', 'ed1ad8d5-6c7f-4f61-b3de-f257847eaa64', '6777387a-df21-4523-b294-fcb134897731', '9814b490-8e61-4cfc-8919-8b24c4339088'], '649c8df6-569e-4aab-8b1d-c132290b602c': ['65443f03-6c07-4be9-a69f-6a898c1dcd90', '7eb11544-b924-458d-8101-9bcb9b3da324'], 'cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd': ['5d4cac04-a8b0-4a73-bfb4-d1db9e8a7867', '93a90c21-bd56-4674-9790-801b38c51e95', 'd47807a1-71da-4c79-b8ef-643cc581501c', 'd92c999d-eace-4502-884f-4ac8799dfc08']} Key: b1838501-9d66-4c09-99e0-7db0b8812a7e Value: ['f9427f70-d76e-4c1d-b585-5068c3306093', 'f53e6c1f-df66-4be0-9462-1fdf0d59b795', 'ed1ad8d5-6c7f-4f61-b3de-f257847eaa64', '6777387a-df21-4523-b294-fcb134897731', '9814b490-8e61-4cfc-8919-8b24c4339088'] 

Key: b1838501-9d66-4c09-99e0-7db0b8812a7e
Value: [
    'f9427f70-d76e-4c1d-b585-5068c3306093',
    'f53e6c1f-df66-4be0-9462-1fdf0d59b795',
    'ed1ad8d5-6c7f-4f61-b3de-f257847eaa64',
    '6777387a-df21-4523-b294-fcb134897731',
    '9814b490-8e61-4cfc-8919-8b24c4339088'
]

Key: 649c8df6-569e-4aab-8b1d-c132290b602c
Value: [
    '65443f03-6c07-4be9-a69f-6a898c1dcd90',
    '7eb11544-b924-458d-8101-9bcb9b3da324'
]

Key: cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd
Value: [
    '5d4cac04-a8b0-4a73-bfb4-d1db9e8a7867',
    '93a90c21-bd56-4674-9790-801b38c51e95',
    'd47807a1-71da-4c79-b8ef-643cc581501c',
    'd92c999d-eace-4502-884f-4ac8799dfc08'
]

## Stauts by date
### 05-Apr-2025 20:04 IST
All tests passed except
tests\hpe_opsramp_cli_test\test_unmanage_alert_resources.py:52: AssertionError
==================================================================== short test summary info ===================================================================== 
FAILED tests/hpe_opsramp_cli_test/test_main.py::test_log_level - assert 2 == 0
FAILED tests/hpe_opsramp_cli_test/test_opsramp_environment.py::test_get_env_aboslute_path - SystemExit: 1
FAILED tests/hpe_opsramp_cli_test/test_opsramp_environment.py::test_do_post1 - IndexError: list index out of range
FAILED tests/hpe_opsramp_cli_test/test_unmanage_alert_resources.py::test_unmanage_alert_resources_log_level - assert 2 == 0
=========================================================== 4 failed, 25 passed, 2 warnings in 49.04s ============================================================ 

