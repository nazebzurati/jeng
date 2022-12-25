import pandas
import xmltodict

from jeng import exception


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
            for data in parsed_xml_dict["logs"]["log"]["logData"]["data"]:
                dataframe.loc[len(dataframe.index)] = str(data).split(",")
        except ValueError:
            raise exception.JengReplyRowWithMismatchedColumnsException
    except KeyError:
        raise exception.JengReplyContainsNoDataAndMnemonicException

    return dataframe
