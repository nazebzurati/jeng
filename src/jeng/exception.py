class JengClientNoneException(AttributeError):
    def __init__(self):
        super().__init__("Client is None. Probably client not yet connected / disconnected.")


class JengIndexCurveNotDefinedException(Exception):
    def __init__(self):
        super().__init__("Index curve not defined.")


class JengMultipleIndexCurveDefinedException(Exception):
    def __init__(self):
        super().__init__("Multiple index curve defined.")


class JengIndexCurveNotExistInDataFrameException(Exception):
    def __init__(self):
        super().__init__("Index curve not exist in dataframe.")


class JengColumnCountNotMatchException(Exception):
    def __init__(self):
        super().__init__("Missing unit from log curve info.")


class JengReplyContainsNoDataAndMnemonicException(KeyError):
    def __init__(self):
        super().__init__("Reply query doesn't contains data or mnemonic list (column name).")


class JengReplyRowWithMismatchedColumnsException(ValueError):
    def __init__(self):
        super().__init__("Row with mismatched columns")
