import pandas as pd


class Summary:
    """Summary of the provided DataFrame.

    All values are computed based on the entire dataframe, except for the HbA1c, which uses the
    last 3 months.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        if self.total_entry_count == 0:
            raise ValueError("Summary DataFrame is empty")
        self.low_threshold = 70
        self.high_threshold = 180
        self.very_low_threshold = 54

    @property
    def hba1c(self) -> float:
        """
        HbA1c estimate from last 3 months of data (or less if data doesn't span 3 months)

        The HbA1c estimative depends on the estimated average glucose (mg/dL) from the last three
        months, as described in the paper "Translating the A1C assay into estimated average glucose
        values" by Nathan DM, Kuenen J, Borg R, Zheng H, Schoenfeld D, and Heine RJ (2008) (Diabetes
        Care. 31 (8): 1473-78).
        """
        most_recent_entry = self.df["date"].max()
        delta_90_days = pd.Timedelta(days=90)
        mean_glucose = self.df[self.df["date"] >= most_recent_entry - delta_90_days][
            "glucose"
        ].mean()
        mean_glucose = float(mean_glucose)
        return (mean_glucose + 46.7) / 28.7

    @property
    def total_entry_count(self) -> int:
        """Return the total number of entries in the dataframe."""
        return len(self.df)

    @property
    def total_glucose_entry_count(self) -> int:
        return len(self.df["glucose"].dropna())

    @property
    def _number_of_distinct_days_with_entries(self) -> int:
        return int(self.df["date"].dt.date.nunique())

    @property
    def mean_daily_glucose_entry_rate(self) -> float:
        return self.total_glucose_entry_count / self._number_of_distinct_days_with_entries

    @property
    def total_low_count(self) -> int:
        return (self.df["glucose"].dropna() < self.low_threshold).sum()

    @property
    def total_very_low_count(self) -> int:
        return (self.df["glucose"].dropna() < self.very_low_threshold).sum()

    @property
    def mean_fast_insulin_per_day(self) -> float:
        fast_insulin_total = int(self.df["fast_insulin"].sum())
        return fast_insulin_total / self._number_of_distinct_days_with_entries

    @property
    def time_in_range(self) -> float:
        entries_in_range = (
            self.df["glucose"]
            .between(self.low_threshold, self.high_threshold, inclusive="left")
            .sum()
        )
        return entries_in_range / self.total_glucose_entry_count

    @property
    def time_below_range(self) -> float:
        entries_below_range = self.df["glucose"].lt(self.low_threshold).sum()
        return entries_below_range / self.total_glucose_entry_count

    @property
    def time_above_range(self) -> float:
        entries_below_range = self.df["glucose"].ge(self.high_threshold).sum()
        return entries_below_range / self.total_glucose_entry_count

    @property
    def hourly_groups(self) -> pd.core.groupby.DataFrameGroupBy:
        return self.df.groupby(self.df["date"].dt.hour)

    def time_in_range_by_hour_from_filter(self, filter_fn) -> list[float]:
        hourly_glucose = self.hourly_groups["glucose"]
        time_in_range_rates = [0.0] * 24
        for hour in range(24):
            if hour in hourly_glucose.groups:
                glucose_values = hourly_glucose.get_group(hour).dropna()
                if len(glucose_values) > 0:
                    in_range = filter_fn(glucose_values).sum()
                    time_in_range_rates[hour] = in_range / len(glucose_values)
        return time_in_range_rates

    @property
    def time_in_range_by_hour(self) -> list[float]:
        return self.time_in_range_by_hour_from_filter(
            lambda glucose_values: glucose_values.between(
                self.low_threshold, self.high_threshold, inclusive="left"
            )
        )

    @property
    def time_below_range_by_hour(self) -> list[float]:
        return self.time_in_range_by_hour_from_filter(
            lambda glucose_values: glucose_values.lt(self.low_threshold)
        )

    @property
    def time_above_range_by_hour(self) -> list[float]:
        return self.time_in_range_by_hour_from_filter(
            lambda glucose_values: glucose_values.ge(self.high_threshold)
        )

    @property
    def mean_glucose_by_hour(self) -> list[float]:
        hourly_glucose = self.hourly_groups["glucose"]
        mean_glucose = [0.0] * 24
        for hour in range(24):
            if hour in hourly_glucose.groups:
                glucose_values = hourly_glucose.get_group(hour).dropna()
                if len(glucose_values) > 0:
                    mean_glucose[hour] = glucose_values.mean()
        return mean_glucose
