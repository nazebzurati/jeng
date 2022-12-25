import common
import pandas
import pytest

from jeng import exception, generate, parse

EXPECTED_ROW_COUNT = 10
EXPECTED_COLUMN_COUNT = 3


@pytest.mark.integration
def test_parse_actual_reply():

    # load data and prepare
    dataframe = pandas.read_csv(
        filepath_or_buffer=f"{common.SAMPLE_PATH}/NOPIMS_LAV02ST2_LWD_8.5_Time.csv",
        nrows=EXPECTED_ROW_COUNT,
    )[["TIME", "DEPTH", "HKLA"]]
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # create log with data
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
        dataframe=dataframe,
    )
    client = common.__connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # get log data
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_INFO_CURVE_LIST,
        dataframe=None,
    )
    reply = client.get_from_store(
        wml_type_in="log",
        xml_in=log_query,
        return_element="data-only",
    )
    assert reply is not None and reply.Result == 1

    # parse reply
    dataframe = parse.parse_log_into_dataframe(
        xml_out=reply["XMLout"],
    )
    assert dataframe is not None and dataframe.shape == (EXPECTED_ROW_COUNT, EXPECTED_COLUMN_COUNT)
    assert dataframe.columns.values.tolist() == ["TIME", "DEPTH", "HKLA"]

    common.__delete_and_clean_witsml(client)


@pytest.mark.unit
def test_parse_reply_data():
    with open(f"{common.QUERY_PATH}/log_reply_data.xml", "r") as reply:
        dataframe = parse.parse_log_into_dataframe(xml_out=reply.read())
        assert dataframe is not None and dataframe.shape == (EXPECTED_ROW_COUNT, EXPECTED_COLUMN_COUNT)
        assert dataframe.columns.values.tolist() == ["TIME", "DEPTH", "HKLA"]


@pytest.mark.unit
def test_parse_reply_no_data():
    with open(f"{common.QUERY_PATH}/log_reply_no_data.xml", "r") as reply:
        with pytest.raises(exception.JengReplyContainsNoDataAndMnemonicException):
            parse.parse_log_into_dataframe(xml_out=reply.read())


@pytest.mark.unit
def test_parse_reply_insufficient_column():
    with open(f"{common.QUERY_PATH}/log_reply_insufficient_column.xml", "r") as reply:
        with pytest.raises(exception.JengReplyRowWithMismatchedColumnsException):
            parse.parse_log_into_dataframe(xml_out=reply.read())


@pytest.mark.unit
def test_parse_reply_empty_column_name():
    with open(f"{common.QUERY_PATH}/log_reply_empty_column.xml", "r") as reply:
        dataframe = parse.parse_log_into_dataframe(xml_out=reply.read())
        assert dataframe is not None and dataframe.shape == (EXPECTED_ROW_COUNT, EXPECTED_COLUMN_COUNT)
        assert dataframe.columns.values.tolist() == ["TIME", "DEPTH", ""]


@pytest.mark.unit
def test_parse_reply_no_column():
    with open(f"{common.QUERY_PATH}/log_reply_no_column.xml", "r") as reply:
        with pytest.raises(exception.JengReplyContainsNoDataAndMnemonicException):
            parse.parse_log_into_dataframe(xml_out=reply.read())


@pytest.mark.unit
def test_parse_reply_no_data_value():
    with open(f"{common.QUERY_PATH}/log_reply_no_data_value.xml", "r") as reply:
        with pytest.raises(exception.JengReplyContainsNoDataAndMnemonicException):
            parse.parse_log_into_dataframe(xml_out=reply.read())


@pytest.mark.unit
def test_parse_reply_insufficient_data():
    with open(f"{common.QUERY_PATH}/log_reply_insufficient_data.xml", "r") as reply:
        with pytest.raises(exception.JengReplyRowWithMismatchedColumnsException):
            parse.parse_log_into_dataframe(xml_out=reply.read())
