"""
Smart Time - Uma biblioteca avançada para manipulação de datas e tempos em Python
"""

from .core.converter import (
    string_to_datetime,
    datetime_to_string,
    validate_date_string,
    convert_to_format,
    convert_with_timezone
)

from .core.time_operations import (
    add_time,
    subtract_time,
    calculate_difference
)

from .core.validation import (
    is_valid_date,
    auto_validate_date
)

from .holidays import (
    is_holiday,
    get_holidays,
    add_holiday,
    remove_holiday
)

from .periods import (
    TimePeriod,
    DateRange,
    get_overlapping_periods
)

from .formatters import (
    format_relative,
    format_custom
)

from .timezone import (
    get_timezone_info,
    convert_timezone,
    get_timezone_abbreviation
)

__version__ = "1.0.0"
__author__ = "Roberto Lima"
__license__ = "MIT"
