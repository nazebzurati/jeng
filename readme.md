# Jeng

A simple WITSML client with utilities.

Testing is done locally for now. So, no CI test badge status at the moment.

## Installation

```
pip install jeng
```

## Getting started

### Client

1. To create and connect to WITSML Server:
    ```python
    from jeng.client import WitsmlClient

    client = WitsmlClient()

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

# set log curve info
log_curve_info_list = [
    model.LogCurveInfoModel(
        uid="TIME",
        mnemonic="TIME",
        unit="s",
        curve_description="Time",
        type_log_data="date time",
        is_index_curve=True,
    ),
    ...
]

...

# generate query (make sure to use mnemonic as column name)
query_xml = generate.generate_log_query(
    log_basic_info=log_basic_info,
    log_curve_info_list=log_curve_info_list,
    dataframe=dataframe,
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
    # Update environment variable using pytest.ini
    coverage run -m pytest && coverage xml
    sonar-scanner.bat -D"sonar.projectKey=<project-key>" -D"sonar.sources=." -D"sonar.host.url=<host-url>" -D"sonar.login=<project-token>"
    ```