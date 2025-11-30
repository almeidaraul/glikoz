import pandas as pd
import pytest


@pytest.fixture
def dataframe_spanning_2_days() -> pd.DataFrame:
    """Returns a DataFrame with entries spanning 2 days."""
    return pd.DataFrame(
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


@pytest.fixture
def dataframe_spanning_6_months() -> pd.DataFrame:
    """Returns a DataFrame with entries spanning 6 months."""
    return pd.DataFrame(
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
