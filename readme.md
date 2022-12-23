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
    ```

3. To call other WITSML APIs than provided wrapper APIs (make sure to connect to WTISML Server first):
    ```python
    # send WMLS_GetVersion directly from Jeng client service
    reply = client.service().WMLS_GetVersion()
    ```

## Contribute

Contribution is welcome.

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

3. Change the source code and test:
    ```bash
    # Update environment variable using pytest.ini 
    coverage run -m pytest && coverage xml
    sonar-scanner.bat -D"sonar.projectKey=<project-key>" -D"sonar.sources=." -D"sonar.host.url=<host-url>" -D"sonar.login=<project-token>"
    ```