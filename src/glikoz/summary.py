import pandas as pd


class Summary:
    """Summary of the provided DataFrame.

    All values are computed based on the entire dataframe, except for the HbA1c, which uses the
    last 3 months.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.low_threshold = 70
        self.high_threshold = 180
        self.very_low_threshold = 54

    @property
    def hba1c(self) -> float:
        raise NotImplementedError

    @property
    def total_entry_count(self) -> int:
        """Return the total number of entries in the dataframe."""
        return len(self.df)

    @property
    def total_glucose_entry_count(self) -> int:
        raise NotImplementedError

    @property
    def mean_daily_glucose_entry_rate(self) -> float:
        raise NotImplementedError

    @property
    def total_low_count(self) -> int:
        raise NotImplementedError

    @property
    def total_very_low_count(self) -> int:
        raise NotImplementedError

    @property
    def mean_fast_insulin_per_day(self) -> float:
        raise NotImplementedError

    @property
    def time_in_range(self) -> float:
        raise NotImplementedError

    @property
    def time_below_range(self) -> float:
        raise NotImplementedError

    @property
    def time_above_range(self) -> float:
        raise NotImplementedError

    @property
    def time_in_range_by_hour(self) -> list[float]:
        raise NotImplementedError

    @property
    def time_below_range_by_hour(self) -> list[float]:
        raise NotImplementedError

    @property
    def time_above_range_by_hour(self) -> list[float]:
        raise NotImplementedError

    @property
    def mean_glucose_by_hour(self) -> list[float]:
        raise NotImplementedError
