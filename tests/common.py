import io
import os
import typing
from xml.etree import ElementTree

import pandas

from jeng import jeng, model

QUERY_PATH = "tests/xml"
SAMPLE_PATH = "tests/sample"
SAMPLE_TIME_FORMAT = "%H:%M:%S/%d-%b-%Y"
TIME_BASED_SAMPLE_FILENAME = "NOPIMS_LAV02ST2_LWD_8.5_Time"
DEPTH_BASED_SAMPLE_FILENAME = "NOPIMS_LAV02ST2_LWD_8.5_Depth"
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
LOG_CURVE_INFO_TIME_LIST = [
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
LOG_CURVE_INFO_DEPTH_LIST = [
    model.LogCurveInfoModel(
        uid="DEPT",
        mnemonic="DEPT",
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


def __connect() -> jeng.WitsmlClient:
    client = jeng.WitsmlClient()
    assert client.connect(
        url=CONNECTION_URL,
        username=CONNECTION_USERNAME,
        password=CONNECTION_PASSWORD,
    )
    return client


def __connect_and_prepare() -> jeng.WitsmlClient:
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


def __delete_and_clean_witsml(client: jeng.WitsmlClient):
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


def __prepare_sample_dataset(
    filename: str,
    log_curve_info_list: typing.List[model.LogCurveInfoModel],
):
    registered_mnemonic = [log_curve_info.mnemonic for log_curve_info in log_curve_info_list]
    return pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/{filename}.csv",
        nrows=10,
    )[registered_mnemonic]


def __compare_curve_info(
    curve_info1: model.LogCurveInfoModel,
    curve_info2: model.LogCurveInfoModel,
    include_index_check: bool = True,
):
    if include_index_check:
        return (
            curve_info1.uid == curve_info2.uid
            and curve_info1.mnemonic == curve_info2.mnemonic
            and curve_info1.curve_description == curve_info2.curve_description
            and curve_info1.type_log_data == curve_info2.type_log_data
            and curve_info1.is_index_curve == curve_info2.is_index_curve
            and curve_info1.index_type == curve_info2.index_type
        )

    # without index check
    return (
        curve_info1.uid == curve_info2.uid
        and curve_info1.mnemonic == curve_info2.mnemonic
        and curve_info1.curve_description == curve_info2.curve_description
        and curve_info1.type_log_data == curve_info2.type_log_data
    )
