import os

from jeng import model

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
