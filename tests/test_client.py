import io
import os
from xml.etree import ElementTree

import pytest

from jeng.client import WitsmlClient

# Loads test variables
QUERY_PATH = "tests/query"
CONNECTION_URL = os.environ.get("JENG_CONN_URL")
CONNECTION_USERNAME = os.environ.get("JENG_CONN_USERNAME")
CONNECTION_PASSWORD = os.environ.get("JENG_CONN_PASSWORD")

# Link: https://stackoverflow.com/a/33997423
def __parse_and_remove_ns(xml: str):
    it = ElementTree.iterparse(io.StringIO(xml))
    for _, el in it:
        # strip all namespaces
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
        # strip namespaces of attributes too
        for at in list(el.attrib.keys()):
            if "}" in at:
                newat = at.split("}", 1)[1]
                el.attrib[newat] = el.attrib[at]
                del el.attrib[at]
    return it.root


def __connect() -> WitsmlClient:
    client = WitsmlClient()
    assert client.connect(
        url=CONNECTION_URL,
        username=CONNECTION_USERNAME,
        password=CONNECTION_PASSWORD,
    )
    return client


def test_incorrect_credentials():
    client = WitsmlClient()
    assert (
        client.connect(
            url=CONNECTION_URL,
            username=f"{CONNECTION_USERNAME}$",
            password=f"{CONNECTION_PASSWORD}$",
        )
        == False
    )


def test_incorrect_credentials_username():
    client = WitsmlClient()
    assert (
        client.connect(
            url=CONNECTION_URL,
            username=f"{CONNECTION_USERNAME}$",
            password=CONNECTION_PASSWORD,
        )
        == False
    )


def test_incorrect_credentials_password():
    client = WitsmlClient()
    assert (
        client.connect(
            url=CONNECTION_URL,
            username=CONNECTION_USERNAME,
            password=f"{CONNECTION_PASSWORD}$",
        )
        == False
    )


@pytest.mark.dependency()
def test_add_to_store():
    client = __connect()
    with open(f"{QUERY_PATH}/well_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELL_001"


@pytest.mark.dependency(depends=["test_add_to_store"])
def test_update_in_store():
    client = __connect()
    with open(f"{QUERY_PATH}/well_update.xml", "r") as query:
        reply = client.update_in_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1


@pytest.mark.dependency(depends=["test_update_in_store"])
def test_get_from_store():
    client = __connect()
    with open(f"{QUERY_PATH}/well_read.xml", "r") as query:
        reply = client.get_from_store(
            wml_type_in="well",
            xml_in=query.read(),
            return_element="all",
        )
        assert reply is not None

        root = __parse_and_remove_ns(reply.XMLout)
        well_name = root.find("well/name").text
        assert reply.Result == 1 and well_name == "WELL 002"


@pytest.mark.dependency(depends=["test_get_from_store"])
def test_delete_from_store():
    client = __connect()
    with open(f"{QUERY_PATH}/well_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1


def test_direct_call():
    client = __connect()
    reply = client.service().WMLS_GetVersion()
    assert reply == "1.3.1.1,1.4.1.1"


def test_api_call_before_connect():
    client = WitsmlClient()
    with open(f"{QUERY_PATH}/well_create.xml", "r") as query:
        with pytest.raises(Exception):
            client.add_to_store(
                wml_type_in="well",
                xml_in=query.read(),
            )

    with open(f"{QUERY_PATH}/well_update.xml", "r") as query:
        with pytest.raises(Exception):
            client.update_in_store(
                wml_type_in="well",
                xml_in=query.read(),
            )

    with open(f"{QUERY_PATH}/well_read.xml", "r") as query:
        with pytest.raises(Exception):
            client.get_from_store(
                wml_type_in="well",
                xml_in=query.read(),
                return_element="all",
            )

    with open(f"{QUERY_PATH}/well_delete.xml", "r") as query:
        with pytest.raises(Exception):
            client.delete_from_store(
                wml_type_in="well",
                xml_in=query.read(),
            )
