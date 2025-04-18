__maintainer__ = "Fabia Miorelli"
__license__ = "BSD-3-Clause"

import pytest

import pandas as pd

from ...vencopy.core.diarybuilders import DiaryBuilder

# NOT TESTED: create_diaries(), __update_activities()

@pytest.fixture
def sample_configs():
    configs = {
        'user_config': {
            'global': {
                'dataset': "dataset1",
                'debug': False,
                'absolute_path': {
                    'dataset1': '/path/to/dataset1',
                    'dataset2': '/path/to/dataset2'
                    }
                },
            'diarybuilders': {
                'time_resolution': 15
            },
            'flexestimators': {
                'plugging_behaviour': {
                    "consider_plugging_behaviour": False
                }
            }
            },
        'dev_config': {
            'dataparsers': {
                'data_variables': False
                }
            }
        }
    return configs


@pytest.fixture
def sample_activities():
    data = {}
    activities = pd.DataFrame({
        "activity_id": [1, 2, 3, 4, 5],
        "activity_duration": [pd.Timedelta(minutes=76), pd.Timedelta(minutes=80), pd.Timedelta(0), pd.Timedelta(minutes=45), pd.Timedelta(minutes=1440)],
        "timestamp_start": pd.DatetimeIndex(["2023-09-12 08:00:00", "2023-09-12 10:30:00", "2023-09-12 10:30:00", "2023-09-12 10:00:00", "2023-09-12 00:00:00"]),
        "timestamp_end": pd.DatetimeIndex(["2023-09-12 09:16:00", "2023-09-12 11:50:00", "2023-09-12 10:30:00", "2023-09-12 10:45:00", "2023-09-13 00:00:00"]),
        "is_first_activity": (True, False, True, False, True),
        "is_last_activity": (False, False, False, False, True)
        })
    data['activities'] = activities
    return data


def test_diarybuilder_init(sample_configs):
    sample_activities = {}
    activities = pd.DataFrame({
        "activity_id": [1, 2, 3, 4],
        "activity_duration": [pd.Timedelta(minutes=76), pd.Timedelta(minutes=80), pd.Timedelta(0), pd.Timedelta(minutes=45)],
        "timestamp_start": pd.DatetimeIndex(["2023-09-12 08:00:00", "2023-09-12 10:30:00", "2023-09-12 10:30:00", "2023-09-12 10:00:00"]),
        "timestamp_end": pd.DatetimeIndex(["2023-09-12 09:16:00", "2023-09-12 11:50:00", "2023-09-12 10:30:00", "2023-09-12 10:45:00"])
        })
    sample_activities['activities'] = activities
    builder = DiaryBuilder(configs=sample_configs, data=sample_activities)

    assert builder.dev_config == sample_configs["dev_config"]
    assert builder.user_config == sample_configs["user_config"]
    assert builder.dataset == "dataset1"
    assert builder.data['activities'].equals(sample_activities['activities'])
    assert builder.time_resolution == 15
    assert builder.is_week_diary == False


def test_correct_timestamps(sample_configs, sample_activities):
    builder = DiaryBuilder(configs=sample_configs, data=sample_activities)
    time_resolution = 15
    result = builder._correct_timestamps(activities=sample_activities['activities'], time_resolution=time_resolution)
    expected_result = pd.DataFrame({
        "activity_duration": [pd.Timedelta(minutes=75), pd.Timedelta(minutes=75), pd.Timedelta(0), pd.Timedelta(minutes=45), pd.Timedelta(days=1)],
        "timestamp_start_corrected": pd.DatetimeIndex(["2023-09-12 08:00:00", "2023-09-12 10:30:00", "2023-09-12 10:30:00", "2023-09-12 10:00:00", "2023-09-12 00:00:00"]),
        "timestamp_end_corrected": pd.DatetimeIndex(["2023-09-12 09:15:00", "2023-09-12 11:45:00", "2023-09-12 10:30:00", "2023-09-12 10:45:00", "2023-09-13 00:00:00"]),
    })

    pd.testing.assert_series_equal(result["timestamp_start_corrected"], expected_result["timestamp_start_corrected"])
    pd.testing.assert_series_equal(result["timestamp_end_corrected"], expected_result["timestamp_end_corrected"])
    pd.testing.assert_series_equal(result["activity_duration"], expected_result["activity_duration"])


def test_removes_zero_length_activities(sample_activities):
    result = DiaryBuilder._removes_zero_length_activities(activities=sample_activities['activities'])

    assert len(result) == 4