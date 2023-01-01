class LogIndexTypeEnum:
    """
    Specifying type of log index: time or non-time. To be used by
    `jeng.model.LogIndexModel`.
    """

    TIME = 0
    NON_TIME = 1


class LogCurveInfoModel:
    """
    Data structure for specifying log curve info.

    Parameters
    ----------
    uid: str
        Unique ID.

    mnemonic: str
        Parameter mnemonic or abbreviation.

    unit: str
        Unit of measure.

    curve_description: str
        Parameter description or additional information.

    type_log_data: str
        Log data type.

    index_type: str, default None
        Required when is_index_curve is True. Usually 'date time'
        for time based log data and 'measured depth' for depth based
        log data.

    is_index_curve: bool, default False
        Determine whether the parameter is the index.
    """

    def __init__(
        self,
        uid: str,
        mnemonic: str,
        unit: str,
        curve_description: str,
        type_log_data: str,
        index_type: str = None,
        is_index_curve: bool = False,
    ) -> None:
        self.uid = uid
        self.mnemonic = mnemonic
        self.unit = unit
        self.curve_description = curve_description
        self.type_log_data = type_log_data
        self.index_type = index_type
        self.is_index_curve = is_index_curve


class LogBasicInfoModel:
    """
    Data structure for specifying log info.

    Parameters
    ----------
    well_uid: str
        Well unique ID.

    well_name: str
        Well name.

    wellbore_uid: str
        Wellbore unique ID.

    wellbore_name: str
        Wellbore name.

    log_uid: str
        Log unique ID.

    log_name: str, default None
        Log name.
    """

    def __init__(
        self,
        well_uid: str,
        well_name: str,
        wellbore_uid: str,
        wellbore_name: str,
        log_uid: str,
        log_name: str,
    ) -> None:
        self.well_uid = well_uid
        self.well_name = well_name
        self.wellbore_uid = wellbore_uid
        self.wellbore_name = wellbore_name
        self.log_uid = log_uid
        self.log_name = log_name


class LogIndexModel:
    """
    Data structure for specifying an interval of data to retrieve.

    Parameters
    ----------
    start: str
        Start of the interval.

    end: str
        End of the interval.

    type: jeng.model.LogIndexTypeEnum, default jeng.model.LogIndexTypeEnum.TIME
        Type of log index: time or non-time index.
    """

    def __init__(
        self,
        start: str,
        end: str,
        type: LogIndexTypeEnum = LogIndexTypeEnum.TIME,
    ) -> None:
        self.start = start
        self.end = end
        self.type = type
