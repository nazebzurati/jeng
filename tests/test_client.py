import common
import pytest

from jeng import jeng


@pytest.mark.integration
def test_incorrect_credentials():
    client = jeng.WitsmlClient()
    status = client.connect(
        url=common.CONNECTION_URL,
        username=f"{common.CONNECTION_USERNAME}$",
        password=f"{common.CONNECTION_PASSWORD}$",
    )
    assert status == False


@pytest.mark.integration
def test_incorrect_credentials_username():
    client = jeng.WitsmlClient()
    status = client.connect(
        url=common.CONNECTION_URL,
        username=f"{common.CONNECTION_USERNAME}$",
        password=common.CONNECTION_PASSWORD,
    )
    assert status == False


@pytest.mark.integration
def test_incorrect_credentials_password():
    client = jeng.WitsmlClient()
    status = client.connect(
        url=common.CONNECTION_URL,
        username=common.CONNECTION_USERNAME,
        password=f"{common.CONNECTION_PASSWORD}$",
    )
    assert status == False


@pytest.mark.integration
@pytest.mark.dependency()
def test_add_to_store():
    client = common.__connect()
    with open(f"{common.QUERY_PATH}/well_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELL_001"


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_add_to_store"])
def test_update_in_store():
    client = common.__connect()
    with open(f"{common.QUERY_PATH}/well_update.xml", "r") as query:
        reply = client.update_in_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_update_in_store"])
def test_get_from_store():
    client = common.__connect()
    with open(f"{common.QUERY_PATH}/well_read.xml", "r") as query:
        reply = client.get_from_store(
            wml_type_in="well",
            xml_in=query.read(),
            return_element="all",
        )
        assert reply is not None

        root = common.__parse_and_remove_ns(reply.XMLout)
        well_name = root.find("well/name").text
        assert reply.Result == 1 and well_name == "WELL 002"


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_get_from_store"])
def test_delete_from_store():
    client = common.__connect()
    with open(f"{common.QUERY_PATH}/well_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1


@pytest.mark.integration
def test_direct_call():
    client = common.__connect()
    reply = client.service().WMLS_GetVersion()
    assert reply == "1.3.1.1,1.4.1.1"


@pytest.mark.integration
def test_api_call_before_connect():
    client = jeng.WitsmlClient()
    with open(f"{common.QUERY_PATH}/well_create.xml", "r") as query:
        with pytest.raises(Exception):
            client.add_to_store(
                wml_type_in="well",
                xml_in=query.read(),
            )

    with open(f"{common.QUERY_PATH}/well_update.xml", "r") as query:
        with pytest.raises(Exception):
            client.update_in_store(
                wml_type_in="well",
                xml_in=query.read(),
            )

    with open(f"{common.QUERY_PATH}/well_read.xml", "r") as query:
        with pytest.raises(Exception):
            client.get_from_store(
                wml_type_in="well",
                xml_in=query.read(),
                return_element="all",
            )

    with open(f"{common.QUERY_PATH}/well_delete.xml", "r") as query:
        with pytest.raises(Exception):
            client.delete_from_store(
                wml_type_in="well",
                xml_in=query.read(),
            )
