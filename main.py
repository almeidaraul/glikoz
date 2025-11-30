import argparse
from pathlib import Path

import pandas as pd

from glikoz.report import LaTeXReport
from glikoz.summary import Summary


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Glikoz report from a CSV file with glucose and insulin data. "
        "CSV file should contain columns: date, glucose, fast_insulin, basal_insulin, carbs"
    )
    parser.add_argument(
        "--csv_file",
        type=Path,
        help="Path to input CSV file",
        required=True,
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        help="Path to the output LaTeX file",
        default=Path("./glikoz_report.tex"),
    )

    args = parser.parse_args()

    # Read CSV file
    df = pd.read_csv(args.csv_file)
    df["date"] = pd.to_datetime(df["date"])

    # Create summary from DataFrame
    summary = Summary(df)

    # Create LaTeX report
    report = LaTeXReport(summary)

    # Generate report file
    report.write_to_file(args.output_file)

    print(f"Report generated successfully: {args.output_file}")


if __name__ == "__main__":
    main()
