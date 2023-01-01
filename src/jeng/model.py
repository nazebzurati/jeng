class LogIndexTypeEnum:
    TIME = 0
    NON_TIME = 1


class LogCurveInfoModel:
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
    def __init__(
        self,
        start: str,
        end: str,
        type: LogIndexTypeEnum = LogIndexTypeEnum.TIME,
    ) -> None:
        self.start = start
        self.end = end
        self.type = type
