import copy

import common
import pandas
import pytest

from jeng import exception, generate
from jeng.client import WitsmlClient


def __connect() -> WitsmlClient:
    client = WitsmlClient()
    assert client.connect(
        url=common.CONNECTION_URL,
        username=common.CONNECTION_USERNAME,
        password=common.CONNECTION_PASSWORD,
    )
    return client


def __connect_and_prepare() -> WitsmlClient:

    client = __connect()

    # create well
    with open(f"{common.QUERY_PATH}/well_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELL_001"

    # create wellbore
    with open(f"{common.QUERY_PATH}/wellbore_create.xml", "r") as query:
        reply = client.add_to_store(
            wml_type_in="wellbore",
            xml_in=query.read(),
        )
        assert reply is not None and reply.SuppMsgOut == "WELLBORE_001"

    return client


def __delete_and_clean_witsml(client: WitsmlClient):

    # delete log
    with open(f"{common.QUERY_PATH}/log_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="log",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1

    # delete wellbore
    with open(f"{common.QUERY_PATH}/wellbore_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="wellbore",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1

    # delete well
    with open(f"{common.QUERY_PATH}/well_delete.xml", "r") as query:
        reply = client.delete_from_store(
            wml_type_in="well",
            xml_in=query.read(),
        )
        assert reply is not None and reply.Result == 1


@pytest.mark.unit
def test_generate_log_missing_unit():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    with pytest.raises(exception.JengColumnCountNotMatchException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.LOG_INFO_CURVE_LIST[:2],
            dataframe=dataframe,
        )


@pytest.mark.unit
def test_generate_log_missing_curve_index_in_dataframe():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["DEPTH", "HKLA"]]

    # generate log
    with pytest.raises(exception.JengIndexCurveNotExistInDataFrameException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.LOG_INFO_CURVE_LIST,
            dataframe=dataframe,
        )


@pytest.mark.unit
def test_generate_no_index_curve_info():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    common.log_info_curve_list_copy = copy.deepcopy(common.LOG_INFO_CURVE_LIST)
    common.log_info_curve_list_copy[0].is_index_curve = False
    with pytest.raises(exception.JengIndexCurveNotDefinedException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.log_info_curve_list_copy,
            dataframe=dataframe,
        )


@pytest.mark.unit
def test_generate_multiple_index_curve_info():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    common.log_info_curve_list_copy = copy.deepcopy(common.LOG_INFO_CURVE_LIST)
    common.log_info_curve_list_copy[1].is_index_curve = True
    with pytest.raises(exception.JengMultipleIndexCurveDefinedException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.log_info_curve_list_copy,
            dataframe=dataframe,
        )


@pytest.mark.integration
@pytest.mark.dependency()
def test_generate_log_full_no_index():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
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


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_full_no_index"])
def test_generate_log_full():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
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


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_full"])
def test_generate_log_header_only():

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
    )

    # test with WITSML Server
    client = __connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_header_only"])
def test_generate_log_data_only():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=10,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
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
