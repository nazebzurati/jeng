import os
import copy
import pandas
import pytest

from jeng import generate, model, exception
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


def test_generate_log_missing_unit():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)

    # generate log
    with pytest.raises(exception.JengColumnCountNotMatchException):
        generate.generate_log_query(
            log_basic_info=LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=LOG_INFO_CURVE_LIST[:2],
            dataframe=dataframe,
        )


def test_generate_log_missing_curve_index_in_dataframe():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["DEPTH", "HKLA"]]

    # generate log
    with pytest.raises(exception.JengIndexCurveNotExistInDataFrameException):
        generate.generate_log_query(
            log_basic_info=LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=LOG_INFO_CURVE_LIST,
            dataframe=dataframe,
        )


def test_generate_no_index_curve_info():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)

    # generate log
    log_info_curve_list_copy = copy.deepcopy(LOG_INFO_CURVE_LIST)
    log_info_curve_list_copy[0].is_index_curve = False
    with pytest.raises(exception.JengIndexCurveNotDefinedException):
        generate.generate_log_query(
            log_basic_info=LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=log_info_curve_list_copy,
            dataframe=dataframe,
        )


def test_generate_multiple_index_curve_info():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)

    # generate log
    log_info_curve_list_copy = copy.deepcopy(LOG_INFO_CURVE_LIST)
    log_info_curve_list_copy[1].is_index_curve = True
    with pytest.raises(exception.JengMultipleIndexCurveDefinedException):
        generate.generate_log_query(
            log_basic_info=LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=log_info_curve_list_copy,
            dataframe=dataframe,
        )


@pytest.mark.dependency()
def test_generate_log_full_no_index():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=LOG_INFO_CURVE_LIST,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = __connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    __delete_and_clean_witsml(client)


@pytest.mark.dependency(depends=["test_generate_log_full_no_index"])
def test_generate_log_full():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=LOG_INFO_CURVE_LIST,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = __connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    __delete_and_clean_witsml(client)


@pytest.mark.dependency(depends=["test_generate_log_full"])
def test_generate_log_header_only():

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=LOG_INFO_CURVE_LIST,
    )

    # test with WITSML Server
    client = __connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1


@pytest.mark.dependency(depends=["test_generate_log_header_only"])
def test_generate_log_data_only():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=LOG_INFO_CURVE_LIST,
        is_include_log_curve_info=False,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = __connect()
    reply = client.update_in_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    __delete_and_clean_witsml(client)
