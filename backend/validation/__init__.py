import datetime
import re
from time import strptime

from controller import CoreController
from structs import Batch, BatchEntry
from enums import ValidationStatus


class StaticValidation:
    """Performs validation of the input data."""

    EXPECTED_HEADERS = [
        'batch_id', 'timestamp',
        'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6', 'reading7', 'reading8', 'reading9',
        'reading10'
    ]

    REGEXP_VALUE = re.compile("^([0-8].[0-9]{3})|(9.[0-8][0-9]{2})|(9.900)$")

    @staticmethod
    def validate_headers(controller: CoreController, batch: Batch, filename: str, headers) -> bool:
        # If there is no headers, return an error.
        if len(headers) != len(StaticValidation.EXPECTED_HEADERS):
            controller.app.logger.error("Skipping file: {}; missing columns", filename)
            return False

        # TODO: validate headers.
        for i in range(0, len(StaticValidation.EXPECTED_HEADERS)):
            # If the header is missing, we'll assume it's what we think it's meant to be.
            # (The data will validate it later).
            if not headers[i].strip():
                batch.set_validation_status(ValidationStatus.FIXED_HEADERS)
                controller.app.logger.warning("Fixing file: {}; adding missing header at position {}, (should be {})",
                                              filename, i, StaticValidation.EXPECTED_HEADERS[i])

            # Otherwise, if the headers do not match, we'll fix them assuming the new value
            # doesn't already exist.
            # (If it does, it implies the columns are in the wrong order which cannot be processed)
            elif headers[i] != StaticValidation.EXPECTED_HEADERS[i]:
                if not headers[i] in StaticValidation.EXPECTED_HEADERS:
                    batch.set_validation_status(ValidationStatus.FIXED_HEADERS)
                    controller.app.logger.warning(
                        "Fixing file: {}; changing mis-spelled header at position {} (= '{}') (should be {})",
                        filename, i, headers[i], StaticValidation.EXPECTED_HEADERS[i])
                else:
                    batch.set_validation_status(ValidationStatus.INVALID_HEADERS)
                    controller.app.logger.error(
                        "Skipping file: {}; duplicate header or bad header ordering at position {} (= '{}') (should "
                        "be {}) - cannot be fixed due to ambiguity",
                        filename, i, headers[i], StaticValidation.EXPECTED_HEADERS[i])
                    return False

        return True

    @staticmethod
    def validate_row(controller: CoreController, batch: Batch, filename: str, row, row_index: int) -> bool:
        # If we don't have a sufficient number of values, error immediately.
        if len(row) != len(StaticValidation.EXPECTED_HEADERS):
            controller.app.logger.error("Skipping file: {}; missing columns at row index {}", filename, row_index)
            batch.set_validation_status(ValidationStatus.MISSING_DATA)
            return False

        # Validate batch_id
        try:
            row[0] = int(row[0])
        except ValueError:
            controller.app.logger.error("Skipping file: {}; invalid batch id {} at row index {}", filename, row[0],
                                        row_index)
            batch.set_validation_status(ValidationStatus.BAD_BATCH_IDS)
            return False

        # Validate timestamp
        try:
            time_struct = strptime(row[1], '%H:%M:%S')
            row[1] = datetime.time(
                hour=time_struct.tm_hour,
                minute=time_struct.tm_min,
                second=time_struct.tm_sec
            )
        except ValueError:
            controller.app.logger.error("Skipping file: {}; invalid timestamp {} at row index {}", filename, row[1],
                                        row_index)
            batch.set_validation_status(ValidationStatus.BAD_VALUES)
            return False

        # Validate other values
        for N in range(1, 11):
            # Identify reading N.
            reading = row[N + 1]

            # Pad with zeroes (because the example data was not 3dp).
            # (but only do this if there was a decimal place, so we're padding to 3dp).
            if len(reading.split('.')) == 2:
                to_pad = 3 - len(reading.split('.')[1])
                reading += ('0' * to_pad)

            # Match regex for 3dp with 1 leading value.
            if not StaticValidation.REGEXP_VALUE.match(reading):
                controller.app.logger.error("Skipping file: {}; invalid value for reading{} (= '{}') at row index {}",
                                            filename, N, reading, row_index)
                batch.set_validation_status(ValidationStatus.BAD_VALUES)
                return False

        # Create a BatchEntry from the row.
        batch_entry = BatchEntry(
            *row
        )

        # Insert the BatchEntry into batch to check for contextual errors.
        # If there is one, a message will be returned and a status set internally.
        # So we just log that error and return false.
        error = batch.add_entry(batch_entry)
        if error:
            controller.app.logger.error("Skipping file: {}; {}", filename, error)
        return error is None
