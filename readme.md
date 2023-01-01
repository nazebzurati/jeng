# Jeng

A simple WITSML client with utilities.

[![Unit test](https://github.com/nazebzurati/jeng/actions/workflows/unit-test.yml/badge.svg)](https://github.com/nazebzurati/jeng/actions/workflows/unit-test.yml)

## Installation

```
pip install jeng
```

## Getting started

- Jeng should be compatible with Python 3.8 and higher.
- Jeng should work with WITSML data schema v1.3.1.1 and v1.4.1.1.
- Incompatible package version update:
  - `0.0.6` → `0.0.7`: Change from `jeng.client.WitsmlClient` package to `jeng.jeng.WitsmlClient`

### Client

1. To create and connect to WITSML Server:
    ```python
    from jeng import jeng

    client = jeng.WitsmlClient()

    # return True if success, else False
    status = client.connect(
        url=CONNECTION_URL,
        username=CONNECTION_USERNAME,
        password=CONNECTION_PASSWORD,
    )
    ```

2. To call wrapper API (make sure to connect to WTISML Server first):
    ```python
    # send query to WMLS_AddToStore API
    with open(f"{QUERY_PATH}/query.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="well",
            xml_in=query.read(),
        )

    # send query to WMLS_UpdateInStore API
    with open(f"{QUERY_PATH}/query.xml", "r") as query:
        reply = client.update_in_store(
            wml_type_in="well",
            xml_in=query.read(),
        )

    # send query to WMLS_GetFromStore API
    with open(f"{QUERY_PATH}/query.xml", "r") as query:
        reply = client.get_from_store(
            wml_type_in="well",
            xml_in=query.read(),
            return_element="all",
        )

    # send query to WMLS_DeleteFromStore API
    with open(f"{QUERY_PATH}/query.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="well",
            xml_in=query.read(),
        )

    # string is expected for xml_in and you can
    # pass string query to all the wrapper API
    client.add_to_store(
        wml_type_in="well",
        xml_in=query_xml_str,
    )
    ```

3. To call other WITSML APIs than provided wrapper APIs (make sure to connect to WTISML Server first):
    ```python
    # send WMLS_GetVersion directly from Jeng client service
    reply = client.service().WMLS_GetVersion()
    ```

### Log Query Generator

```python
from jeng import model, generate

# set log basic info
log_basic_info = model.LogBasicInfoModel(
    well_uid="WELL_001",
    well_name="WELL 001",
    wellbore_uid="WELLBORE_001",
    wellbore_name="WELLBORE 001",
    log_uid="LOG_001",
    log_name="LOG 001",
)

# set time log curve info
log_curve_info_list = [
    model.LogCurveInfoModel(
        uid="TIME",
        mnemonic="TIME",
        unit="s",
        curve_description="Time",
        type_log_data="date time",
        index_type="date time",
        is_index_curve=True,
    ),
    model.LogCurveInfoModel(
        uid="HKLA",
        mnemonic="HKLA",
        unit="klbf",
        curve_description="Average Hookload",
        type_log_data="double",
    ),
    ...
]

# set depth log curve info
log_curve_info_list = [
    model.LogCurveInfoModel(
        uid="DEPTH",
        mnemonic="DEPTH",
        unit="m",
        curve_description="Depth Index",
        type_log_data="double",
        index_type="measured depth",
        is_index_curve=True,
    ),
    model.LogCurveInfoModel(
        uid="HKLA",
        mnemonic="HKLA",
        unit="klbf",
        curve_description="Average Hookload",
        type_log_data="double",
    ),
    ...
]

...

# generate query (make sure to use mnemonic as column name)
query_xml = generate.generate_log_query(
    log_basic_info=log_basic_info,
    log_curve_info_list=log_curve_info_time_list,
    dataframe=dataframe,
)

# it's possible to generate WMLS_GetFromStore compatible
# query with specific time interval
query_xml = generate.generate_log_query(
    log_basic_info=log_basic_info,
    log_curve_info_list=log_curve_info_time_list,
    log_index=model.LogIndexModel(
        start="2020-06-30T17:44:00.000+08:00",
        end="2020-06-30T17:45:00.000+08:00",
    ),
)

# it's possible to generate WMLS_GetFromStore compatible
# query with specific non-time interval
query_xml = generate.generate_log_query(
    log_basic_info=log_basic_info,
    log_curve_info_list=log_curve_info_depth_list,
    log_index=model.LogIndexModel(
        start="2575.2",
        end="2575.5",
        type=model.LogIndexTypeEnum.NON_TIME,
    ),
)
```

### Log Reply Parser

```python
from jeng import parse

...

# parse WITSML XMLout reply data into dataframe
dataframe = parse.parse_log_into_dataframe(
    xml_out=reply["XMLout"],
)
```

## Test

Make sure to have a WITSML server running for the test.

1. Clone the project:
    ```bash
    git clone https://github.com/nazebzurati/jeng.git
    ```

2. Prepare environment:
    ```bash
    # create environment and activate
    virtualenv env
    .\env\Scripts\activate

    # install development dependencies
    pip install -e .[dev]
    ```

3. Change the source code and test.
    ```bash
    # run code formatter
    isort . --skip env
    black --line-length 120 .

    # run coverage and pytest
    coverage run -m pytest -v
    coverage run -m pytest -m integration -v    # test with WITSML server integration
    coverage run -m pytest -m unit -v           # test without WITSML server integration

    # run static code test
    coverage xml && sonar-scanner.bat -D"sonar.projectKey=<project-key>" -D"sonar.sources=." -D"sonar.host.url=<host-url>" -D"sonar.login=<project-token>"
    ```