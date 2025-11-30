import pytest

from glikoz.report import TypstReport
from glikoz.summary import Summary


class TestTypstReportOnShortDataFrameSpanning2Days:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_2_days):
        self.df = dataframe_spanning_2_days
        self.summary = Summary(self.df)
        self.report = TypstReport(self.summary)

    def test_write_to_file_has_expected_content(self):
        pass


class TestTypstReportOnShortDataFrameSpanning6Months:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_6_months):
        self.df = dataframe_spanning_6_months
        self.summary = Summary(self.df)
        self.report = TypstReport(self.summary)

    def test_write_to_file_has_expected_content(self):
        pass
