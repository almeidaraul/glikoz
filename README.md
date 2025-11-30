<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="img/glikoz_logo.png" alt="Glikoz logo"></a>
</p>

<h1 align="center">Glikoz</h1>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![GitHub Issues](https://img.shields.io/github/issues/almeidaraul/glikoz)](https://github.com/almeidaraul/glikoz/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/almeidaraul/glikoz)](https://github.com/almeidaraul/glikoz/pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Glucose and insulin use data analysis for diabetes therapy
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## 🧐 About <a name = "about"></a>
**Glikoz** · _γλικοζ_ (/ɣli'koz/): a glucose and insulin use data analysis tool to assist the treatment of diabetes. Currently it is built around information exported from the [Diaguard](https://github.com/Faltenreich/Diaguard) app as backup CSVs.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
**Glikoz** is built using Python 3.13+ and uses [uv](https://docs.astral.sh/uv/) for dependency management.

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the project dependencies:
```bash
uv sync
```

## 🔧 Running the tests <a name = "tests"></a>
Automated tests are implemented with PyTest. Run tests with:

```bash
uv run pytest
```

## 🎈 Usage <a name="usage"></a>
Generate a LaTeX report from a CSV file containing glucose and insulin data:

```bash
uv run python main.py input.csv output.tex
```

The CSV file should have the following columns:
- `date`: timestamp in format "YYYY-MM-DD HH:MM"
- `glucose`: glucose reading in mg/dL
- `fast_insulin`: fast-acting insulin dose
- `basal_insulin`: basal insulin dose
- `carbs`: carbohydrate intake in grams

In each row, all columns except for `date` are optional.

After generating the LaTeX file, compile it to PDF:

```bash
pdflatex output.tex
```