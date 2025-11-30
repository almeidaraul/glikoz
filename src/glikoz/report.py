from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO

from glikoz.summary import Summary


class Report(ABC):
    def __init__(self, summary: Summary):
        self.summary = summary

    @abstractmethod
    def write_to_file(self, file_path: Path) -> None:
        pass


class LaTeXReport(Report):
    def __init__(self, summary: Summary):
        super().__init__(summary)

    def write_to_file(self, file_path: Path) -> None:
        with open(file_path, "w+") as f:
            self.write_file_header(f)

            self.write_number(f, "HbA1c", self.summary.hba1c)

            self.write_number(f, "Entry Count", self.summary.total_entry_count)

            self.write_number(f, "Glucose Entry Count", self.summary.total_glucose_entry_count)
            self.write_number(
                f, "Mean Daily Glucose Entry Rate", self.summary.mean_daily_glucose_entry_rate
            )

            self.write_number(f, "Total Low Count", self.summary.total_low_count)
            self.write_number(f, "Total Very Low Count", self.summary.total_very_low_count)

            self.write_number(
                f, "Mean Daily Fast Insulin Intake", self.summary.mean_fast_insulin_per_day
            )

            self.write_pie_chart(
                f,
                "Time in Range",
                self.summary.time_in_range,
                self.summary.time_below_range,
                self.summary.time_above_range,
            )

            hours_as_strings = list(map(lambda x: f"{x:02}", range(24)))

            self.write_stacked_bar_chart(
                f,
                "Time in Range by Hour",
                hours_as_strings,
                self.summary.time_in_range_by_hour,
                self.summary.time_below_range_by_hour,
                self.summary.time_above_range_by_hour,
            )

            self.write_line_graph(
                f, "Mean Glucose by Hour", hours_as_strings, self.summary.mean_glucose_by_hour
            )

            self.write_file_footer(f)

    def write_file_header(self, file_buffer: TextIO) -> None:
        header_lines = [
            r"\documentclass[a4paper]{article}",
            r"\usepackage{graphicx}",
            r"\usepackage{pgfplots}",
            r"\usepackage{pgf-pie}",
            r"\pgfplotsset{compat=1.18}",
            r"\begin{document}",
            r"\title{Glikoz Report}",
            r"\date{\today}",
            r"\maketitle",
            "",
        ]
        file_buffer.write("\n".join(header_lines))

    def write_file_footer(self, file_buffer: TextIO) -> None:
        file_buffer.write("\n\\end{document}\n")

    def write_number(self, file_buffer: TextIO, label: str, value: float | int) -> None:
        value_str = str(value) if isinstance(value, int) else f"{value:.2f}"
        file_buffer.write(f"\\textbf{{{label}:}} {value_str}\n\n")

    def write_pie_chart(self, file_buffer: TextIO, title: str, *values: float) -> None:
        file_buffer.write(f"\\subsection*{{{title}}}\n")
        file_buffer.write("\\begin{center}\n")
        file_buffer.write("\\begin{tikzpicture}\n")

        all_labels = ["In Range", "Below Range", "Above Range"]
        all_colors = ["green", "blue", "red"]

        # Filter out zero values
        pie_parts = []
        colors = []
        for v, label, color in zip(values, all_labels, all_colors, strict=True):
            if v > 0.0:
                percentage = f"{v * 100:.1f}"
                pie_parts.append(f"{percentage}/{label}")
                colors.append(color)

        pie_data = ",".join(pie_parts)

        file_buffer.write(f"\\pie[color={{{','.join(colors)}}}]{{{pie_data}}}\n")
        file_buffer.write("\\end{tikzpicture}\n")
        file_buffer.write("\\end{center}\n\n")

    def write_stacked_bar_chart(
        self,
        file_buffer: TextIO,
        title: str,
        horizontal_axis: list[str] | list[int],
        *bars: list[float],
    ) -> None:
        file_buffer.write(f"\\subsection*{{{title}}}\n")
        file_buffer.write("\\begin{center}\n")
        file_buffer.write("\\begin{tikzpicture}\n")
        file_buffer.write("\\begin{axis}[\n")
        file_buffer.write("    ybar stacked,\n")
        file_buffer.write("    width=1.2\\textwidth,\n")
        file_buffer.write("    height=8cm,\n")
        file_buffer.write("    xlabel={Hour},\n")
        file_buffer.write("    ylabel={Percentage},\n")
        file_buffer.write("    ymin=0,\n")
        file_buffer.write("    ymax=1,\n")
        file_buffer.write("    ytick={0.25,0.5,0.75},\n")
        file_buffer.write("    enlarge x limits=false,\n")
        file_buffer.write("    xtick=data,\n")
        file_buffer.write(f"    xticklabels={{{','.join(map(str, horizontal_axis))}}},\n")
        file_buffer.write("    x tick label style={font=\\small},\n")
        file_buffer.write("    legend style={at={(0.5,-0.2)}, anchor=north, legend columns=3},\n")
        file_buffer.write("]\n")

        legend_labels = ["In Range", "Below Range", "Above Range"]
        colors = ["green", "blue", "red"]

        # Write each bar dataset
        for i, bar_data in enumerate(bars):
            color = colors[i] if i < len(colors) else "gray"
            file_buffer.write(f"\\addplot[fill={color}] coordinates {{\n")
            for j, value in enumerate(bar_data):
                file_buffer.write(f"    ({j},{value})\n")
            file_buffer.write("};\n")
            if i < len(legend_labels):
                file_buffer.write(f"\\addlegendentry{{{legend_labels[i]}}}\n")

        file_buffer.write("\\end{axis}\n")
        file_buffer.write("\\end{tikzpicture}\n")
        file_buffer.write("\\end{center}\n\n")

    def write_line_graph(
        self, file_buffer: TextIO, title: str, x_axis: list[str] | list[int], y_axis: list[float]
    ) -> None:
        file_buffer.write(f"\\subsection*{{{title}}}\n")
        file_buffer.write("\\begin{center}\n")
        file_buffer.write("\\begin{tikzpicture}\n")
        file_buffer.write("\\begin{axis}[\n")
        file_buffer.write("    width=1.2\\textwidth,\n")
        file_buffer.write("    height=8cm,\n")
        file_buffer.write("    xlabel={Hour},\n")
        file_buffer.write("    ylabel={Glucose (mg/dL)},\n")
        file_buffer.write(f"    xmin=0, xmax={len(x_axis) - 1},\n")
        file_buffer.write(f"    xtick={{0,1,...,{len(x_axis) - 1}}},\n")
        file_buffer.write(f"    xticklabels={{{','.join(map(str, x_axis))}}},\n")
        file_buffer.write("    x tick label style={font=\\small},\n")
        file_buffer.write("    grid=major,\n")
        file_buffer.write("    legend style={at={(0.5,-0.15)}, anchor=north},\n")
        file_buffer.write("]\n")
        file_buffer.write("\\addplot[mark=*, blue, thick] coordinates {\n")
        for i, y_value in enumerate(y_axis):
            if y_value > 0.0:
                file_buffer.write(f"    ({i},{y_value})\n")
        file_buffer.write("};\n")
        file_buffer.write("\\addlegendentry{Mean Glucose}\n")
        file_buffer.write("\\end{axis}\n")
        file_buffer.write("\\end{tikzpicture}\n")
        file_buffer.write("\\end{center}\n\n")
