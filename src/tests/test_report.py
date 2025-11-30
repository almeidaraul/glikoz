import pytest

from glikoz.report import LateXReport
from glikoz.summary import Summary


class TestLaTeXReportOnShortDataFrameSpanning2Days:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_2_days):
        self.df = dataframe_spanning_2_days
        self.summary = Summary(self.df)
        self.report = LateXReport(self.summary)

    def test_write_to_file_has_expected_content(self):
        pass


class TestLaTeXReportOnShortDataFrameSpanning6Months:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_6_months):
        self.df = dataframe_spanning_6_months
        self.summary = Summary(self.df)
        self.report = LateXReport(self.summary)

    def test_write_to_file_has_expected_content(self):
        pass
