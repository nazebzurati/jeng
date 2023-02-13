import typing

import pandas
import xmltodict

from jeng import exception, model


def parse_log_into_dataframe(xml_out: str) -> pandas.DataFrame:
    """
    Parse 'log' XMLout reply data into pandas.DataFrame.

    Parameters
    ----------
    xml_out : str
        WITSML XMLout reply string.

    Returns
    -------
    pandas.DataFrame
        DataFrame with mnemonic as column name.
    """
    parsed_xml_dict = xmltodict.parse(xml_out)

    # create column name and append with data
    try:
        column_name_list = str(parsed_xml_dict["logs"]["log"]["logData"]["mnemonicList"]).split(",")
        dataframe = pandas.DataFrame(columns=column_name_list)
        try:
            # fix data list becomes an object if only 1 data row present.
            data_list = parsed_xml_dict["logs"]["log"]["logData"]["data"]
            if not isinstance(data_list, typing.List):
                data_list = [parsed_xml_dict["logs"]["log"]["logData"]["data"]]

            for data in data_list:
                dataframe.loc[len(dataframe.index)] = str(data).split(",")
        except ValueError:
            raise exception.JengReplyRowWithMismatchedColumnsException
    except KeyError:
        raise exception.JengReplyContainsNoDataAndMnemonicException

    return dataframe


def parse_log_into_curve_info(xml_out: str) -> typing.List[model.LogCurveInfoModel]:
    """
    Parse 'log' XMLout reply into model.LogCurveInfoModel.

    Parameters
    ----------
    xml_out : str
        WITSML XMLout reply string.

    Returns
    -------
    model.LogCurveInfoModel
        List of log curve info model.
    """
    parsed_xml_dict = xmltodict.parse(xml_out)
    parsed_log_dict = parsed_xml_dict["logs"]["log"]

    # parse log curve info
    curve_info_list = []
    if "logCurveInfo" in parsed_log_dict.keys():
        # for a single curve info, it parsed as an object and not list.
        # this line convert single object as list.
        parsed_log_curve_info_list = parsed_log_dict["logCurveInfo"]
        if not isinstance(parsed_log_dict["logCurveInfo"], typing.List):
            parsed_log_curve_info_list = [parsed_log_dict["logCurveInfo"]]

        for parsed_log_curve_info in parsed_log_curve_info_list:
            curve_info = model.LogCurveInfoModel(
                uid=parsed_log_curve_info["@uid"],
                mnemonic=parsed_log_curve_info["mnemonic"],
                unit=parsed_log_curve_info["unit"],
                curve_description=parsed_log_curve_info["curveDescription"],
                type_log_data=parsed_log_curve_info["typeLogData"],
            )

            # set index, if applicable
            if (
                all(x in parsed_log_dict.keys() for x in ["indexCurve", "indexType"])
                and parsed_log_dict["indexCurve"] == curve_info.mnemonic
            ):
                curve_info.is_index_curve = True
                curve_info.index_type = parsed_log_dict["indexType"]
            curve_info_list.append(curve_info)

    return curve_info_list
