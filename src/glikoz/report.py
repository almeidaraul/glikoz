from abc import ABC
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, TextIO

from glikoz.summary import Summary


def require_file_buffer(func: Callable) -> Callable:
    """Decorator to ensure file_buffer is not None before executing write methods."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.file_buffer is None:
            raise RuntimeError(f"Cannot call {func.__name__}: file_buffer is None")
        return func(self, *args, **kwargs)

    return wrapper


class Report(ABC):
    def __init__(self, summary: Summary):
        pass

    def write_to_file(self, file_path: Path):
        pass


class LaTeXReport(Report):
    def __init__(self, summary: Summary):
        self.summary = summary
        self.file_buffer: TextIO | None = None

    def write_to_file(self, file_path: Path):
        with open(file_path, "w+") as f:
            self.file_buffer = f
            self.write_file_header()

            self.write_number("HbA1c", self.summary.hba1c)

            self.write_number("Entry Count", self.summary.total_entry_count)

            self.write_number("Glucose Entry Count", self.summary.total_glucose_entry_count)
            self.write_number(
                "Mean Daily Glucose Entry Rate", self.summary.mean_daily_glucose_entry_rate
            )

            self.write_number("Total Low Count", self.summary.total_low_count)
            self.write_number("Total Very Low Count", self.summary.total_very_low_count)

            self.write_number(
                "Mean Daily Fast Insulin Intake", self.summary.mean_fast_insulin_per_day
            )
            
            self.write_pie_chart(
                "Time in Range",
                self.summary.time_in_range,
                self.summary.time_below_range,
                self.summary.time_above_range,
            )

            hours_as_strings = list(map(lambda x: f"{x:02}", range(24)))

            self.write_stacked_bar_chart(
                "Time in Range by Hour",
                hours_as_strings,
                self.summary.time_in_range_by_hour,
                self.summary.time_below_range_by_hour,
                self.summary.time_above_range_by_hour,
            )

            self.write_line_graph("Mean Glucose by Hour", hours_as_strings, self.summary.mean_glucose_by_hour)
            
            self.write_file_footer()
        self.file_buffer = None

    @require_file_buffer
    def write_file_header(self):
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
            ""
        ]
        self.file_buffer.write("\n".join(header_lines))

    @require_file_buffer
    def write_file_footer(self):
        self.file_buffer.write("\n\\end{document}\n")

    @require_file_buffer
    def write_number(self, label: str, value: float | int):
        value_str = str(value) if isinstance(value, int) else f'{value:.2f}'
        self.file_buffer.write(f"\\textbf{{{label}:}} {value_str}\n\n")

    @require_file_buffer
    def write_pie_chart(self, title: str, *values: float):
        self.file_buffer.write(f"\\subsection*{{{title}}}\n")
        self.file_buffer.write("\\begin{center}\n")
        self.file_buffer.write("\\begin{tikzpicture}\n")
        
        all_labels = ["In Range", "Below Range", "Above Range"]
        all_colors = ["green", "blue", "red"]
        
        # Filter out zero values
        pie_parts = []
        colors = []
        for v, label, color in zip(values, all_labels, all_colors):
            if v > 0.0:
                percentage = f"{v * 100:.1f}"
                pie_parts.append(f"{percentage}/{label}")
                colors.append(color)
        
        pie_data = ",".join(pie_parts)
        
        self.file_buffer.write(f"\\pie[color={{{','.join(colors)}}}]{{{pie_data}}}\n")
        self.file_buffer.write("\\end{tikzpicture}\n")
        self.file_buffer.write("\\end{center}\n\n")

    @require_file_buffer
    def write_stacked_bar_chart(
        self,
        title: str,
        horizontal_axis: list[str | int],
        *bars: list[float],
    ):
        self.file_buffer.write(f"\\subsection*{{{title}}}\n")
        self.file_buffer.write("\\begin{center}\n")
        self.file_buffer.write("\\begin{tikzpicture}\n")
        self.file_buffer.write("\\begin{axis}[\n")
        self.file_buffer.write("    ybar stacked,\n")
        self.file_buffer.write("    width=1.2\\textwidth,\n")
        self.file_buffer.write("    height=8cm,\n")
        self.file_buffer.write("    xlabel={Hour},\n")
        self.file_buffer.write("    ylabel={Percentage},\n")
        self.file_buffer.write("    ymin=0,\n")
        self.file_buffer.write("    ymax=1,\n")
        self.file_buffer.write("    ytick={0.25,0.5,0.75},\n")
        self.file_buffer.write("    enlarge x limits=false,\n")
        self.file_buffer.write("    xtick=data,\n")
        self.file_buffer.write(f"    xticklabels={{{','.join(map(str, horizontal_axis))}}},\n")
        self.file_buffer.write("    x tick label style={font=\\small},\n")
        self.file_buffer.write("    legend style={at={(0.5,-0.2)}, anchor=north, legend columns=3},\n")
        self.file_buffer.write("]\n")

        legend_labels = ["In Range", "Below Range", "Above Range"]
        colors = ["green", "blue", "red"]

        # Write each bar dataset
        for i, bar_data in enumerate(bars):
            color = colors[i] if i < len(colors) else "gray"
            self.file_buffer.write(f"\\addplot[fill={color}] coordinates {{\n")
            for j, value in enumerate(bar_data):
                self.file_buffer.write(f"    ({j},{value})\n")
            self.file_buffer.write("};\n")
            if i < len(legend_labels):
                self.file_buffer.write(f"\\addlegendentry{{{legend_labels[i]}}}\n")

        self.file_buffer.write("\\end{axis}\n")
        self.file_buffer.write("\\end{tikzpicture}\n")
        self.file_buffer.write("\\end{center}\n\n")

    @require_file_buffer
    def write_line_graph(self, title: str, x_axis: list[str | int], y_axis: list[float]):
        self.file_buffer.write(f"\\subsection*{{{title}}}\n")
        self.file_buffer.write("\\begin{center}\n")
        self.file_buffer.write("\\begin{tikzpicture}\n")
        self.file_buffer.write("\\begin{axis}[\n")
        self.file_buffer.write("    width=1.2\\textwidth,\n")
        self.file_buffer.write("    height=8cm,\n")
        self.file_buffer.write("    xlabel={Hour},\n")
        self.file_buffer.write("    ylabel={Glucose (mg/dL)},\n")
        self.file_buffer.write(f"    xmin=0, xmax={len(x_axis)-1},\n")
        self.file_buffer.write(f"    xtick={{0,1,...,{len(x_axis)-1}}},\n")
        self.file_buffer.write(f"    xticklabels={{{','.join(map(str, x_axis))}}},\n")
        self.file_buffer.write("    x tick label style={font=\\small},\n")
        self.file_buffer.write("    grid=major,\n")
        self.file_buffer.write("    legend style={at={(0.5,-0.15)}, anchor=north},\n")
        self.file_buffer.write("]\n")
        self.file_buffer.write("\\addplot[mark=*, blue, thick] coordinates {\n")
        for i, y_value in enumerate(y_axis):
            if y_value > 0.0:
                self.file_buffer.write(f"    ({i},{y_value})\n")
        self.file_buffer.write("};\n")
        self.file_buffer.write("\\addlegendentry{Mean Glucose}\n")
        self.file_buffer.write("\\end{axis}\n")
        self.file_buffer.write("\\end{tikzpicture}\n")
        self.file_buffer.write("\\end{center}\n\n")
