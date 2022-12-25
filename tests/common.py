import io
import os
from xml.etree import ElementTree

from jeng import model
from jeng.client import WitsmlClient

QUERY_PATH = "tests/query"
SAMPLE_PATH = "tests/sample"
SAMPLE_TIME_FORMAT = "%H:%M:%S/%d-%b-%Y"
CONNECTION_URL = os.environ.get("JENG_CONN_URL")
CONNECTION_USERNAME = os.environ.get("JENG_CONN_USERNAME")
CONNECTION_PASSWORD = os.environ.get("JENG_CONN_PASSWORD")
LOG_INFO_WELL_WELLBORE = model.LogBasicInfoModel(
    well_uid="WELL_001",
    well_name="WELL 001",
    wellbore_uid="WELLBORE_001",
    wellbore_name="WELLBORE 001",
    log_uid="LOG_001",
    log_name="LOG 001",
)
LOG_INFO_CURVE_LIST = [
    model.LogCurveInfoModel(
        uid="TIME",
        mnemonic="TIME",
        unit="s",
        curve_description="Time",
        type_log_data="date time",
        is_index_curve=True,
    ),
    model.LogCurveInfoModel(
        uid="DEPTH",
        mnemonic="DEPTH",
        unit="m",
        curve_description="Depth Index",
        type_log_data="double",
    ),
    model.LogCurveInfoModel(
        uid="HKLA",
        mnemonic="HKLA",
        unit="klbf",
        curve_description="Average Hookload",
        type_log_data="double",
    ),
]


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
                new_at = at.split("}", 1)[1]
                el.attrib[new_at] = el.attrib[at]
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


def __connect_and_prepare() -> WitsmlClient:

    client = __connect()

    # create well
    with open(f"{QUERY_PATH}/well_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELL_001"

    # create wellbore
    with open(f"{QUERY_PATH}/wellbore_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="wellbore",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELLBORE_001"

    return client


def __delete_and_clean_witsml(client: WitsmlClient):

    # delete log
    with open(f"{QUERY_PATH}/log_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="log",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1

    # delete wellbore
    with open(f"{QUERY_PATH}/wellbore_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="wellbore",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1

    # delete well
    with open(f"{QUERY_PATH}/well_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1
