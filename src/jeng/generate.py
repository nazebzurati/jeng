from typing import List

import pandas
import xmltodict

from jeng import exception, model

WITSML_NAMESPACE = "http://www.witsml.org/schemas/1series"  # NOSONAR: It's a XML namespace
WITSML_VERSION = "1.4.1.1"  # NOSONAR: It's a version, not a hardcoded IP address


def __prepare_log_curve_info(log_curve_info_list: List[model.LogCurveInfoModel]):
    index_curve_index = -1
    index_curve_count = 0
    log_curve_info_dict = []
    for index, log_curve_info in enumerate(log_curve_info_list):
        log_curve_info_dict.append(
            {
                "@uid": log_curve_info.uid,
                "mnemonic": log_curve_info.mnemonic,
                "unit": log_curve_info.unit,
                "curveDescription": log_curve_info.curve_description,
                "typeLogData": log_curve_info.type_log_data,
            },
        )
        if log_curve_info.is_index_curve:
            index_curve_index = index
            index_curve_count += 1
    if index_curve_index == -1 or index_curve_count == 0:
        raise exception.JengIndexCurveNotDefinedException
    if index_curve_count > 1:
        raise exception.JengMultipleIndexCurveDefinedException
    return log_curve_info_dict, index_curve_index


def __prepare_dataframe_index(
    log_curve_info_list: List[model.LogCurveInfoModel],
    dataframe: pandas.DataFrame,
    log_curve_index: int,
) -> pandas.DataFrame:
    dataframe = dataframe[:].astype(str)
    if dataframe.index.name != log_curve_info_list[log_curve_index].uid:
        if log_curve_info_list[log_curve_index].uid not in dataframe.columns.values.tolist():
            raise exception.JengIndexCurveNotExistInDataFrameException
        dataframe.set_index(log_curve_info_list[log_curve_index].uid, inplace=True)
    return dataframe


def __prepare_log_data_list(
    log_curve_info_list: List[model.LogCurveInfoModel],
    dataframe: pandas.DataFrame,
    log_curve_index: int,
):
    # generate mnemonic list
    mnemonic_list = [log_curve_info_list[log_curve_index].mnemonic] + dataframe.columns.values.tolist()

    # generate unit list
    unit_list = [log_curve_info_list[log_curve_index].unit]
    for column in dataframe.columns.values.tolist():
        for curve_info in log_curve_info_list:
            if curve_info.mnemonic == column:
                unit_list.append(curve_info.unit)
    if len(unit_list) != dataframe.shape[1] + 1:
        raise exception.JengColumnCountNotMatchException

    # generate data list
    data_list = []
    for index, row in dataframe.iterrows():
        data_list.append(",".join([str(index)] + row.tolist()))

    return mnemonic_list, unit_list, data_list


def generate_log_query(
    log_basic_info: model.LogBasicInfoModel,
    log_curve_info_list: List[model.LogCurveInfoModel],
    dataframe: pandas.DataFrame = None,
    is_include_log_curve_info: bool = True,
) -> str:
    """
    Generate 'log' query using pandas.DataFrame(). Not recommended for generating log
    deletion query.

    Parameters
    ----------
    log_basic_info : jeng.model.LogBasicInfoModel
        Well, wellbore and log information for query generation.
    log_curve_info_list : List[jeng.model.LogCurveInfoModel]
        A list of curve info which contains uid, mnemonic, unit, description and data type.
    dataframe: pandas.DataFrame, default None
        pandas.DataFrame that contains data which mnemonic as column name. It is best if
        the dataframe index name was set similar to index curve uid. If the index name was
        not set or match, the function will attempt to find the index curve uid among the
        column names.
    is_include_log_curve_info: bool, default True
        WITSML query have maximum character limitation and varies between WITSML server. It
        is recommended to include log curve info for creating log for the first time and
        not to include for adding and updating data.

    Returns
    -------
    str
        Log query ready to be executed.
    """
    # prepare log curve info data
    log_curve_info_dict, log_curve_index = __prepare_log_curve_info(log_curve_info_list)
    all_dict = {
        "logs": {
            "@xmlns": WITSML_NAMESPACE,
            "@version": WITSML_VERSION,
            "log": {
                "@uidWell": log_basic_info.well_uid,
                "@uidWellbore": log_basic_info.wellbore_uid,
                "@uid": log_basic_info.log_uid,
                "nameWell": log_basic_info.well_name,
                "nameWellbore": log_basic_info.wellbore_name,
                "name": log_basic_info.log_name,
                "indexCurve": log_curve_info_list[log_curve_index].uid,
                "indexType": log_curve_info_list[log_curve_index].type_log_data,
            },
        },
    }
    if is_include_log_curve_info:
        all_dict["logs"]["log"]["logCurveInfo"] = log_curve_info_dict

    # prepare dataframe
    if dataframe is not None and not dataframe.empty:
        dataframe = __prepare_dataframe_index(
            log_curve_info_list=log_curve_info_list,
            log_curve_index=log_curve_index,
            dataframe=dataframe,
        )

        # generate log data list
        mnemonic_list, unit_list, data_list = __prepare_log_data_list(
            log_curve_info_list=log_curve_info_list,
            log_curve_index=log_curve_index,
            dataframe=dataframe,
        )

        all_dict["logs"]["log"]["logData"] = (
            {
                "mnemonicList": ",".join(mnemonic_list),
                "unitList": ",".join(unit_list),
                "data": data_list,
            },
        )

    # generate log data
    return xmltodict.unparse(all_dict, full_document=False)
