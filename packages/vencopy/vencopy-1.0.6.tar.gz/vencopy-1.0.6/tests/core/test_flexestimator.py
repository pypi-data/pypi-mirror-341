__maintainer__ = "Fabia Miorelli"
__license__ = "BSD-3-Clause"


import pandas as pd
import pytest
from dateutil import parser

from ...vencopy.core.flexestimators import FlexEstimator
from ...vencopy.utils.utils import calculate_daily_seasonal_factor


@pytest.fixture
def sample_data():
    data = {
        "unique_id": [1, 1, 2, 2, 3],
        "timestamp_start": [
            "2023-09-01 08:00",
            "2023-09-01 08:45",
            "2023-09-01 10:00",
            "2023-09-01 10:30",
            "2023-09-01 11:00",
        ],
        "timestamp_end": [
            "2023-09-01 09:00",
            "2023-09-01 09:30",
            "2023-09-01 10:15",
            "2023-09-01 11:15",
            "2023-09-01 11:30",
        ],
        "trip_distance": [60.0, 15.0, 10.0, 10.0, 10.0],
        "travel_time": [60, 45, 90, 90, 90],
        "season": ["summer", "winter", "spring", "summer", "summer"],
        "trip_start_hour": [8, 8, 10, 10, 11],  # Example trip start hours
    }
    data["timestamp_start"] = [parser.parse(x) for x in data["timestamp_start"]]
    data["timestamp_end"] = [parser.parse(x) for x in data["timestamp_end"]]

    return pd.DataFrame(data)


@pytest.fixture
def sample_configs():
    configs = {
        "user_config": {
            "global": {
                "consider_temperature_cycle_dependency": {
                    "annual": True,
                    "daily": True,
                    "season": "summer",
                    "day_night_factors": {
                        "winter": {
                            "temperature_range": 6.52,
                            "highest_temperature_hour": 14,
                            "consumption_at_highest_hour": min,
                            "lowest_temperature_hour": 1,
                            "consumption_at_lowest_hour": max,
                        },
                        "spring": {
                            "temperature_range": 10.58,
                            "highest_temperature_hour": 14,
                            "consumption_at_highest_hour": min,
                            "lowest_temperature_hour": 3,
                            "consumption_at_lowest_hour": max,
                        },
                        "summer": {
                            "temperature_range": 11.37,
                            "highest_temperature_hour": 14,
                            "consumption_at_highest_hour": max,
                            "lowest_temperature_hour": 3,
                            "consumption_at_lowest_hour": min,
                        },
                        "fall": {
                            "temperature_range": 6.53,
                            "highest_temperature_hour": 13,
                            "consumption_at_highest_hour": min,
                            "lowest_temperature_hour": 1,
                            "consumption_at_lowest_hour": max,
                        },
                    },
                },
                "flexestimators": {
                    "electric_consumption": {
                        "general": 18,
                        "winter_factor": 0.3,
                        "spring_factor": 0,
                        "summer_factor": 0.03,
                        "fall_factor": 0,
                    }
                },
            }
        }
    }

    return configs


# def test_drain(sample_data, sample_configs):
#     seasons = ["winter", "spring", "summer", "fall"]

#     result = FlexEstimator._drain(
#         activities=sample_data,
#         user_config=sample_configs["user_config"],
#         seasons=seasons,
#         calculate_daily_seasonal_factor=calculate_daily_seasonal_factor,
#     )

#     assert (
#         "electric_consumption" in result.columns
#     ), "The 'electric_consumption' column is missing in the result."
#     assert "drain" in result.columns, "The 'drain' column is missing in the result."

#     assert (
#         result.loc[0, "electric_consumption"] > 0
#     ), "Electric consumption should be positive."
#     assert (
#         result.loc[1, "electric_consumption"] > 0
#     ), "Electric consumption should be positive."
#     assert result.loc[0, "drain"] == pytest.approx(
#         result.loc[0, "trip_distance"] * result.loc[0, "electric_consumption"] / 100
#     ), "Drain calculation mismatch."
#     assert result.loc[1, "drain"] == pytest.approx(
#         result.loc[1, "trip_distance"] * result.loc[1, "electric_consumption"] / 100
#     ), "Drain calculation mismatch."

#     expected_electric_consumption = [
#         18 * (1 + 0.03 * 0.1),  # Summer with daily factor applied
#         18 * (1 + 0.3 * 0.1),  # Winter with daily factor applied
#         18,  # Spring, factor is 0
#         18 * (1 + 0.03 * 0.1),  # Summer with daily factor applied
#         18 * (1 + 0.03 * 0.1),  # Summer with daily factor applied
#     ]
#     expected_drain = [
#         60.0 * expected_electric_consumption[0] / 100,
#         15.0 * expected_electric_consumption[1] / 100,
#         10.0 * expected_electric_consumption[2] / 100,
#         10.0 * expected_electric_consumption[3] / 100,
#         10.0 * expected_electric_consumption[4] / 100,
#     ]

#     pd.testing.assert_series_equal(
#         result["electric_consumption"],
#         pd.Series(expected_electric_consumption, name="electric_consumption"),
#         check_dtype=False,
#     )

#     pd.testing.assert_series_equal(
#         result["drain"],
#         pd.Series(expected_drain, name="drain"),
#         check_dtype=False,
#     )
