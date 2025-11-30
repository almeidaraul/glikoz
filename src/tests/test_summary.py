import pandas as pd
import pytest

from glikoz.summary import Summary


class TestSummaryOnEmptyDataFrame:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.DataFrame(
            columns=["date", "glucose", "fast_insulin", "basal_insulin", "carbs"]
        )
        self.summary = Summary(self.df)

    def test_hba1c(self):
        assert self.summary.hba1c is None

    def test_total_entry_count(self):
        assert self.summary.total_entry_count == 0

    def test_total_glucose_entry_count(self):
        assert self.summary.total_glucose_entry_count == 0

    def test_mean_daily_glucose_entry_rate(self):
        assert self.summary.mean_daily_glucose_entry_rate == 0.0

    def test_total_low_count(self):
        assert self.summary.total_low_count == 0

    def test_total_very_low_count(self):
        assert self.summary.total_very_low_count == 0

    def test_mean_fast_insulin_per_day(self):
        assert self.summary.mean_fast_insulin_per_day == 0.0

    def test_time_in_range(self):
        assert self.summary.time_in_range == 0.0

    def test_time_below_range(self):
        assert self.summary.time_below_range == 0.0

    def test_time_above_range(self):
        assert self.summary.time_above_range == 0.0

    def test_time_in_range_by_hour(self):
        assert self.summary.time_in_range_by_hour == [0.0] * 24

    def test_time_below_range_by_hour(self):
        assert self.summary.time_below_range_by_hour == [0.0] * 24

    def test_time_above_range_by_hour(self):
        assert self.summary.time_above_range_by_hour == [0.0] * 24

    def test_mean_glucose_by_hour(self):
        assert self.summary.mean_glucose_by_hour is None


class TestSummaryOnShortDataFrameSpanning2Days:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    [
                        "2024-01-01 08:00",
                        "2024-01-01 12:00",
                        "2024-01-01 18:00",
                        "2024-01-02 08:00",
                        "2024-01-02 12:00",
                    ]
                ),
                "glucose": [100, None, 200, 120, None],
                "fast_insulin": [2, 3, None, 2, 3],
                "basal_insulin": [10, None, 10, None, 10],
                "carbs": [30, 60, None, 30, 60],
            }
        )
        self.summary = Summary(self.df)

    def test_hba1c(self):
        pass

    def test_total_entry_count(self):
        pass

    def test_total_glucose_entry_count(self):
        pass

    def test_mean_daily_glucose_entry_rate(self):
        pass

    def test_total_low_count(self):
        pass

    def test_total_very_low_count(self):
        pass

    def test_mean_fast_insulin_per_day(self):
        pass

    def test_time_in_range(self):
        pass

    def test_time_below_range(self):
        pass

    def test_time_above_range(self):
        pass

    def test_time_in_range_by_hour(self):
        pass

    def test_time_below_range_by_hour(self):
        pass

    def test_time_above_range_by_hour(self):
        pass

    def test_mean_glucose_by_hour(self):
        pass


class TestSummaryOnShortDataFrameSpanning6Months:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    [
                        "2024-01-01 08:00",
                        "2024-01-01 12:00",
                        "2024-07-01 18:00",
                        "2024-07-02 08:00",
                        "2024-07-02 12:00",
                    ]
                ),
                "glucose": [100, None, 200, 120, None],
                "fast_insulin": [2, 3, None, 2, 3],
                "basal_insulin": [10, None, 10, None, 10],
                "carbs": [30, 60, None, 30, 60],
            }
        )
        self.summary = Summary(self.df)

    def test_hba1c(self):
        pass

    def test_total_entry_count(self):
        pass

    def test_total_glucose_entry_count(self):
        pass

    def test_mean_daily_glucose_entry_rate(self):
        pass

    def test_total_low_count(self):
        pass

    def test_total_very_low_count(self):
        pass

    def test_mean_fast_insulin_per_day(self):
        pass

    def test_time_in_range(self):
        pass

    def test_time_below_range(self):
        pass

    def test_time_above_range(self):
        pass

    def test_time_in_range_by_hour(self):
        pass

    def test_time_below_range_by_hour(self):
        pass

    def test_time_above_range_by_hour(self):
        pass

    def test_mean_glucose_by_hour(self):
        pass
