import copy

import common
import pandas
import pytest
import xmltodict

from jeng import exception, generate, jeng, model, parse


@pytest.mark.unit
def test_generate_log_missing_unit():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    with pytest.raises(exception.JengColumnCountNotMatchException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST[:2],
            dataframe=dataframe,
        )


@pytest.mark.unit
def test_generate_log_missing_curve_index_in_dataframe():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )[["DEPTH", "HKLA"]]

    # generate log
    with pytest.raises(exception.JengIndexCurveNotExistInDataFrameException):
        generate.generate_log_query(
            log_basic_info=common.LOG_INFO_WELL_WELLBORE,
            log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
            dataframe=dataframe,
        )


@pytest.mark.unit
def test_generate_no_index_curve_info():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    common.log_info_curve_list_copy = copy.deepcopy(common.LOG_CURVE_INFO_TIME_LIST)
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
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    common.log_info_curve_list_copy = copy.deepcopy(common.LOG_CURVE_INFO_TIME_LIST)
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
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = common.__connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    common.__delete_and_clean_witsml(client)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_full_no_index"])
def test_generate_log_full():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = common.__connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    common.__delete_and_clean_witsml(client)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_full"])
def test_generate_log_header_only():
    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )

    # test with WITSML Server
    client = common.__connect_and_prepare()
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_header_only"])
def test_generate_log_data_only():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)
    dataframe = dataframe.set_index("TIME")

    # generate log
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
        is_include_log_curve_info=False,
        dataframe=dataframe,
    )

    # test with WITSML Server
    client = common.__connect()
    reply = client.update_in_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # clean up WITMSL data on server
    common.__delete_and_clean_witsml(client)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_header_only"])
def test_generate_log_data_with_time_index():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(
        dataframe["TIME"],
        format=common.SAMPLE_TIME_FORMAT,
    ).dt.tz_localize("Asia/Kuala_Lumpur")

    # add data
    client: jeng.WitsmlClient = common.__connect_and_prepare()
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
        dataframe=dataframe,
    )
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # get some data
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
        is_include_log_curve_info=False,
        log_index=model.LogIndexModel(
            start="2020-06-30T17:44:33.000+08:00",
            end="2020-06-30T17:45:13.000+08:00",
        ),
    )
    reply = client.get_from_store(
        wml_type_in="log",
        xml_in=log_query,
        return_element="data-only",
    )
    assert reply is not None and reply.Result == 1

    # validate
    dataframe = parse.parse_log_into_dataframe(
        xml_out=reply["XMLout"],
    )
    assert dataframe.shape[0] == 5

    # clean up WITMSL data on server
    common.__delete_and_clean_witsml(client)


@pytest.mark.integration
@pytest.mark.dependency(depends=["test_generate_log_data_with_time_index"])
def test_generate_log_data_with_depth_index():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.DEPTH_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_DEPTH_LIST,
    )

    # add data
    client: jeng.WitsmlClient = common.__connect_and_prepare()
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_DEPTH_LIST,
        dataframe=dataframe,
    )
    reply = client.add_to_store(
        wml_type_in="log",
        xml_in=log_query,
    )
    assert reply is not None and reply.Result == 1

    # get some data
    log_query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        log_curve_info_list=common.LOG_CURVE_INFO_DEPTH_LIST,
        is_include_log_curve_info=False,
        log_index=model.LogIndexModel(
            start="2575.2552",
            end="2575.56",
            type=model.LogIndexTypeEnum.NON_TIME,
        ),
    )
    reply = client.get_from_store(
        wml_type_in="log",
        xml_in=log_query,
        return_element="data-only",
    )
    assert reply is not None and reply.Result == 1

    # validate
    dataframe = parse.parse_log_into_dataframe(
        xml_out=reply["XMLout"],
    )
    assert dataframe.shape[0] == 3

    # clean up WITMSL data on server
    common.__delete_and_clean_witsml(client)


@pytest.mark.unit
def test_generate_log_without_log_curve_info():
    # generate log
    query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
    )
    query_parsed = xmltodict.parse(query)
    assert not [
        item for item in ["indexCurve", "indexType", "logCurveInfo"] if item in query_parsed["logs"]["log"].keys()
    ]


@pytest.mark.unit
def test_generate_log_without_log_curve_info_with_dataframe():
    # load data and prepare
    dataframe = common.__prepare_sample_dataset(
        filename=common.TIME_BASED_SAMPLE_FILENAME,
        log_curve_info_list=common.LOG_CURVE_INFO_TIME_LIST,
    )
    dataframe["TIME"] = pandas.to_datetime(dataframe["TIME"], format=common.SAMPLE_TIME_FORMAT)

    # generate log
    query = generate.generate_log_query(
        log_basic_info=common.LOG_INFO_WELL_WELLBORE,
        dataframe=dataframe,
    )
    query_parsed = xmltodict.parse(query)
    assert not [
        item
        for item in ["indexCurve", "indexType", "logCurveInfo", "logData"]
        if item in query_parsed["logs"]["log"].keys()
    ]
