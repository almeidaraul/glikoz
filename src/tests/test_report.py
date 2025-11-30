import pytest

from glikoz.report import LaTeXReport
from glikoz.summary import Summary


class TestLaTeXReportOnShortDataFrameSpanning2Days:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_2_days):
        self.df = dataframe_spanning_2_days
        self.summary = Summary(self.df)
        self.report = LaTeXReport(self.summary)

    def test_write_to_file_has_expected_content(self, tmp_path):
        output_file = tmp_path / "output.tex"
        self.report.write_to_file(output_file)

        expected_content = r"""\documentclass[a4paper]{article}
\usepackage{graphicx}
\usepackage{pgfplots}
\usepackage{pgf-pie}
\pgfplotsset{compat=1.18}
\begin{document}
\title{Glikoz Report}
\date{\today}
\maketitle
\textbf{HbA1c:} 6.51

\textbf{Entry Count:} 5

\textbf{Glucose Entry Count:} 3

\textbf{Mean Daily Glucose Entry Rate:} 1.50

\textbf{Total Low Count:} 0.00

\textbf{Total Very Low Count:} 0.00

\textbf{Mean Daily Fast Insulin Intake:} 5.00

\subsection*{Time in Range}
\begin{center}
\begin{tikzpicture}
\pie[color={green,red}]{66.7/In Range,33.3/Above Range}
\end{tikzpicture}
\end{center}

\subsection*{Time in Range by Hour}
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    ybar stacked,
    width=1.2\textwidth,
    height=8cm,
    xlabel={Hour},
    ylabel={Percentage},
    ymin=0,
    ymax=1,
    ytick={0.25,0.5,0.75},
    enlarge x limits=false,
    xtick=data,
    xticklabels={00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23},
    x tick label style={font=\small},
    legend style={at={(0.5,-0.2)}, anchor=north, legend columns=3},
]
\addplot[fill=green] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,1.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,0.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{In Range}
\addplot[fill=blue] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,0.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,0.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{Below Range}
\addplot[fill=red] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,0.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,1.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{Above Range}
\end{axis}
\end{tikzpicture}
\end{center}

\subsection*{Mean Glucose by Hour}
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    width=1.2\textwidth,
    height=8cm,
    xlabel={Hour},
    ylabel={Glucose (mg/dL)},
    xmin=0, xmax=23,
    xtick={0,1,...,23},
    xticklabels={00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23},
    x tick label style={font=\small},
    grid=major,
    legend style={at={(0.5,-0.15)}, anchor=north},
]
\addplot[mark=*, blue, thick] coordinates {
    (8,110.0)
    (18,200.0)
};
\addlegendentry{Mean Glucose}
\end{axis}
\end{tikzpicture}
\end{center}


\end{document}
"""

        actual_content = output_file.read_text()
        assert actual_content == expected_content


class TestLaTeXReportOnShortDataFrameSpanning6Months:
    @pytest.fixture(autouse=True)
    def setup(self, dataframe_spanning_6_months):
        self.df = dataframe_spanning_6_months
        self.summary = Summary(self.df)
        self.report = LaTeXReport(self.summary)

    def test_write_to_file_has_expected_content(self, tmp_path):
        output_file = tmp_path / "output.tex"
        self.report.write_to_file(output_file)

        expected_content = r"""\documentclass[a4paper]{article}
\usepackage{graphicx}
\usepackage{pgfplots}
\usepackage{pgf-pie}
\pgfplotsset{compat=1.18}
\begin{document}
\title{Glikoz Report}
\date{\today}
\maketitle
\textbf{HbA1c:} 7.20

\textbf{Entry Count:} 3

\textbf{Glucose Entry Count:} 2

\textbf{Mean Daily Glucose Entry Rate:} 1.00

\textbf{Total Low Count:} 0.00

\textbf{Total Very Low Count:} 0.00

\textbf{Mean Daily Fast Insulin Intake:} 2.50

\subsection*{Time in Range}
\begin{center}
\begin{tikzpicture}
\pie[color={green,red}]{50.0/In Range,50.0/Above Range}
\end{tikzpicture}
\end{center}

\subsection*{Time in Range by Hour}
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    ybar stacked,
    width=1.2\textwidth,
    height=8cm,
    xlabel={Hour},
    ylabel={Percentage},
    ymin=0,
    ymax=1,
    ytick={0.25,0.5,0.75},
    enlarge x limits=false,
    xtick=data,
    xticklabels={00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23},
    x tick label style={font=\small},
    legend style={at={(0.5,-0.2)}, anchor=north, legend columns=3},
]
\addplot[fill=green] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,1.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,0.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{In Range}
\addplot[fill=blue] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,0.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,0.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{Below Range}
\addplot[fill=red] coordinates {
    (0,0.0)
    (1,0.0)
    (2,0.0)
    (3,0.0)
    (4,0.0)
    (5,0.0)
    (6,0.0)
    (7,0.0)
    (8,0.0)
    (9,0.0)
    (10,0.0)
    (11,0.0)
    (12,0.0)
    (13,0.0)
    (14,0.0)
    (15,0.0)
    (16,0.0)
    (17,0.0)
    (18,1.0)
    (19,0.0)
    (20,0.0)
    (21,0.0)
    (22,0.0)
    (23,0.0)
};
\addlegendentry{Above Range}
\end{axis}
\end{tikzpicture}
\end{center}

\subsection*{Mean Glucose by Hour}
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    width=1.2\textwidth,
    height=8cm,
    xlabel={Hour},
    ylabel={Glucose (mg/dL)},
    xmin=0, xmax=23,
    xtick={0,1,...,23},
    xticklabels={00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23},
    x tick label style={font=\small},
    grid=major,
    legend style={at={(0.5,-0.15)}, anchor=north},
]
\addplot[mark=*, blue, thick] coordinates {
    (8,120.0)
    (18,200.0)
};
\addlegendentry{Mean Glucose}
\end{axis}
\end{tikzpicture}
\end{center}


\end{document}
"""

        actual_content = output_file.read_text()
        assert actual_content == expected_content
