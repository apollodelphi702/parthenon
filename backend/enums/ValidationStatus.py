from enum import IntEnum


class ValidationStatus(IntEnum):
    """
    The validation status of a batch.
    Each value is more severe than the last, and if the validation
    status >=_CRITICAL the file cannot be processed and will be skipped.
    """

    VALID = 0
    """All data is valid"""

    FIXED_HEADERS = 1
    """Had to fix missing or mis-spelled column headers"""

    # Critical Errors.
    critical = 2
    """Sentinel value. DO NOT USE AS A STANDALONE STATUS. This is to identify the lowest critical error."""

    INVALID_HEADERS = 2
    """Headers were invalid and could not be fixed because of ambiguity"""

    BATCH_ID_DUPLICATES = 3
    """Duplicated batch IDs"""

    BAD_BATCH_IDS = 4
    """Batch entries have invalid IDs"""

    BAD_VALUES = 5
    """Values in batch entries with invalid values"""

    MISSING_DATA = 6
    """Data within the entries missing"""

