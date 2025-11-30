from abc import ABC
from pathlib import Path

from glikoz.summary import Summary


class Report(ABC):
    def __init__(self, summary: Summary):
        pass

    def write_to_file(self, file_path: Path):
        pass


class TypstReport(Report):
    def __init__(self, summary: Summary):
        self.summary = summary

    def write_to_file(self, file_path: Path):
        self.write_file_header()

        self.write_number("HbA1c", self.summary.hba1c)

        self.write_number("Entry Count", self.summary.total_entry_count)

        self.write_number("Glucose Entry Count", self.summary.total_glucose_entry_count)
        self.write_number(
            "Mean Daily Glucose Entry Rate", self.summary.mean_daily_glucose_entry_rate
        )

        self.write_number("Total Low Count", self.summary.total_low_count)
        self.write_number("Total Very Low Count", self.summary.total_very_low_count)

        self.write_number("Mean Daily Fast Insulin Intake", self.summary.mean_fast_insulin_per_day)

        self.write_pie_chart(
            "Time in Range",
            self.summary.time_in_range,
            self.summary.time_below_range,
            self.summary.time_above_range,
        )
        self.write_stacked_bar_chart(
            "Time in Range by Hour",
            self.summary.time_in_range_by_hour,
            self.summary.time_below_range_by_hour,
            self.summary.time_above_range_by_hour,
        )

        self.write_line_graph("Mean Glucose by Hour", self.summary.mean_glucose_by_hour)

        self.write_file_footer()

    def write_file_header(self):
        raise NotImplementedError

    def write_file_footer(self):
        raise NotImplementedError

    def write_number(self, label: str, value: float | int):
        raise NotImplementedError

    def write_pie_chart(
        self,
        title: str,
        in_range: float,
        below_range: float,
        above_range: float,
    ):
        raise NotImplementedError

    def write_stacked_bar_chart(
        self,
        title: str,
        in_range: list[float],
        below_range: list[float],
        above_range: list[float],
    ):
        raise NotImplementedError

    def write_line_graph(self, title: str, values: list[float]):
        raise NotImplementedError
