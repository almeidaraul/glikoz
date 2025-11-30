import pytest

from glikoz.summary import Summary


class TestSummaryOnShortDataFrameSpanning2Days:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_2_days):
        self.df = dataframe_spanning_2_days
        self.summary = Summary(self.df)

    def test_hba1c(self):
        # No 3-month data, only last two days (2024-01-01, 2024-01-02)
        # Mean glucose is 140, HbA1c = (140 + 46.7) / 28.7
        assert self.summary.hba1c == (140 + 46.7) / 28.7

    def test_total_entry_count(self):
        assert self.summary.total_entry_count == 5

    def test_total_glucose_entry_count(self):
        assert self.summary.total_glucose_entry_count == 3

    def test_mean_daily_glucose_entry_rate(self):
        # 3 glucose entries across 2 distinct days (Jan 1, Jan 2)
        assert self.summary.mean_daily_glucose_entry_rate == 1.5

    def test_total_low_count(self):
        assert self.summary.total_low_count == 0

    def test_total_very_low_count(self):
        assert self.summary.total_very_low_count == 0

    def test_mean_fast_insulin_per_day(self):
        # fast_insulin sum = 10, across 2 days = 5 per day
        assert self.summary.mean_fast_insulin_per_day == 5.0

    def test_time_in_range(self):
        assert self.summary.time_in_range == 2 / 3

    def test_time_below_range(self):
        assert self.summary.time_below_range == 0.0

    def test_time_above_range(self):
        assert self.summary.time_above_range == 1 / 3

    def test_time_in_range_by_hour(self):
        expected = [0.0] * 24
        expected[8] = 1.0
        assert self.summary.time_in_range_by_hour == expected

    def test_time_below_range_by_hour(self):
        expected = [0.0] * 24
        assert self.summary.time_below_range_by_hour == expected

    def test_time_above_range_by_hour(self):
        expected = [0.0] * 24
        expected[18] = 1.0
        assert self.summary.time_above_range_by_hour == expected

    def test_mean_glucose_by_hour(self):
        expected = [0.0] * 24
        expected[8] = 110.0
        expected[18] = 200.0
        assert self.summary.mean_glucose_by_hour == expected


class TestSummaryOnShortDataFrameSpanning6Months:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_6_months):
        self.df = dataframe_spanning_6_months
        self.summary = Summary(self.df)

    def test_hba1c(self):
        # Last 3 months (90 days) from 2024-07-02: only July entries (200, 120)
        # Mean glucose = 160, HbA1c = (160 + 46.7) / 28.7
        assert self.summary.hba1c == (160 + 46.7) / 28.7

    def test_total_entry_count(self):
        assert self.summary.total_entry_count == 3

    def test_total_glucose_entry_count(self):
        assert self.summary.total_glucose_entry_count == 2

    def test_mean_daily_glucose_entry_rate(self):
        assert self.summary.mean_daily_glucose_entry_rate == 1.0

    def test_total_low_count(self):
        assert self.summary.total_low_count == 0

    def test_total_very_low_count(self):
        assert self.summary.total_very_low_count == 0

    def test_mean_fast_insulin_per_day(self):
        assert self.summary.mean_fast_insulin_per_day == 5 / 2

    def test_time_in_range(self):
        assert self.summary.time_in_range == 1 / 2

    def test_time_below_range(self):
        assert self.summary.time_below_range == 0.0

    def test_time_above_range(self):
        assert self.summary.time_above_range == 1 / 2

    def test_time_in_range_by_hour(self):
        expected = [0.0] * 24
        expected[8] = 1.0
        assert self.summary.time_in_range_by_hour == expected

    def test_time_below_range_by_hour(self):
        expected = [0.0] * 24
        assert self.summary.time_below_range_by_hour == expected

    def test_time_above_range_by_hour(self):
        expected = [0.0] * 24
        expected[18] = 1.0
        assert self.summary.time_above_range_by_hour == expected

    def test_mean_glucose_by_hour(self):
        expected = [0.0] * 24
        expected[8] = 120.0
        expected[18] = 200.0
        assert self.summary.mean_glucose_by_hour == expected
