__maintainer__ = "Fabia Miorelli"
__license__ = "BSD-3-Clause"

import pytest
import yaml
import os

from unittest.mock import mock_open, patch
import pandas as pd
from pathlib import Path

from ...vencopy.utils.utils import load_configs, return_lowest_level_dict_keys, return_lowest_level_dict_values, replace_vec, create_output_folders, create_file_name, write_out


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path / "temp_dir"


def test_load_configs(temp_dir):
    temp_dir.mkdir(parents=True)
    (temp_dir / "config").mkdir()
    user_config_name = "user_config.yaml"
    dev_config_name = "dev_config.yaml"

    user_config_data = {"user_key": "user_value"}
    dev_config_data = {"dev_key": "dev_value"}

    with open((temp_dir / "config" / user_config_name), "w") as user_file:
        yaml.dump(user_config_data, user_file, default_flow_style=False)
    with open((temp_dir / "config" / dev_config_name), "w") as dev_file:
        yaml.dump(dev_config_data, dev_file, default_flow_style=False)

    configs = load_configs(temp_dir)

    assert "user_config" in configs
    assert "dev_config" in configs
    assert configs["user_config"] == user_config_data
    assert configs["dev_config"] == dev_config_data

    user_config_data = {}
    dev_config_data = {}
    with open((temp_dir / "config" / user_config_name), "w") as user_file:
        yaml.dump(user_config_data, user_file, default_flow_style=False)
    with open((temp_dir / "config" / dev_config_name), "w") as dev_file:
        yaml.dump(dev_config_data, dev_file, default_flow_style=False)

    configs = load_configs(temp_dir)
    assert configs == {"dev_config": {}, "user_config": {}}


def test_return_lowest_level_dict_keys():
    # Test when the input dictionary has nested dictionaries
    dictionary = {
        "key1": {
            "subkey1": "value1",
            "subkey2": {
                "subsubkey1": "value2"
            }
        },
        "key2": "value3"
    }
    expected_result = ["subsubkey1", "subkey1", "key2"]

    result = return_lowest_level_dict_keys(dictionary)
    assert set(result) == set(expected_result)

    # Test when the input dictionary has no nested dictionaries
    dictionary = {
        "key1": "value1",
        "key2": "value2",
        "key3": None
    }
    expected_result = ["key1", "key2"]

    result = return_lowest_level_dict_keys(dictionary)
    assert result == expected_result

    # Test when the input dictionary is empty
    dictionary = {}
    expected_result = []

    result = return_lowest_level_dict_keys(dictionary)
    assert result == expected_result


def test_return_lowest_level_dict_values():
    # Test when the input dictionary has nested dictionaries
    dictionary = {
        "key1": {
            "subkey1": "value1",
            "subkey2": {
                "subsubkey1": "value2"
            }
        },
        "key2": "value3"
    }
    expected_result = ["value1", "value2", "value3"]

    result = return_lowest_level_dict_values(dictionary)
    assert set(result) == set(expected_result)

    # Test when the input dictionary has no nested dictionaries
    dictionary = {
        "key1": "value1",
        "key2": "value2",
        "key3": None
    }
    expected_result = ["value1", "value2"]

    result = return_lowest_level_dict_values(dictionary)
    assert set(result) == set(expected_result)

    # Test when the input dictionary is empty
    dictionary = {}
    expected_result = []

    result = return_lowest_level_dict_values(dictionary)
    assert result == expected_result


def test_replace_vec():
    data = pd.DataFrame({
        "timestamp": [pd.to_datetime("2021-01-01 12:30:45"), pd.to_datetime("2022-02-02 13:45:00")]
    })

    # Test replacing only the year
    result = replace_vec(data["timestamp"], year=2023)
    expected_result = pd.to_datetime(["2023-01-01 12:30:45", "2023-02-02 13:45:00"])
    assert all(result == expected_result)

    # Test replacing only the month
    result = replace_vec(data["timestamp"], month=5)
    expected_result = pd.to_datetime(["2021-05-01 12:30:45", "2022-05-02 13:45:00"])
    assert all(result == expected_result)

    # Test replacing only the day
    result = replace_vec(data["timestamp"], day=15)
    expected_result = pd.to_datetime(["2021-01-15 12:30:45", "2022-02-15 13:45:00"])
    assert all(result == expected_result)

    # Test replacing only the hour
    result = replace_vec(data["timestamp"], hour=7)
    expected_result = pd.to_datetime(["2021-01-01 07:30:45", "2022-02-02 07:45:00"])
    assert all(result == expected_result)

    # Test replacing only the minute
    result = replace_vec(data["timestamp"], minute=15)
    expected_result = pd.to_datetime(["2021-01-01 12:15:45", "2022-02-02 13:15:00"])
    assert all(result == expected_result)

    # Test replacing multiple components
    result = replace_vec(data["timestamp"], year=2023, month=5, day=15, hour=7, minute=15, second=30)
    expected_result = pd.to_datetime(["2023-05-15 07:15:30", "2023-05-15 07:15:30"])
    assert all(result == expected_result)

    # Test not replacing any component
    result = replace_vec(data["timestamp"])
    expected_result = pd.to_datetime(["2021-01-01 12:30:45", "2022-02-02 13:45:00"])
    assert all(result == expected_result)


@pytest.fixture
def sample_configs(tmp_path):
    root_path = tmp_path / "sample_root"
    root_path.mkdir(parents=True)

    configs = {
        "user_config": {
            "global": {
                "absolute_path": {
                    "vencopy_root": str(root_path)
                }
            }
        }
    }

    return configs


def test_create_output_folders(sample_configs):
    root_path = Path(sample_configs["user_config"]["global"]["absolute_path"]["vencopy_root"])
    main_dir = "output"
    create_output_folders(sample_configs)

    assert os.path.exists(Path(root_path))
    assert os.path.exists(Path(root_path / main_dir))

    sub_dirs = (
        "dataparser",
        "diarybuilder",
        "gridmodeller",
        "flexestimator",
        "profileaggregator",
        "postprocessor"
    )
    for sub_dir in sub_dirs:
        assert os.path.exists(Path(root_path / main_dir / sub_dir))


def test_create_file_name():
    dev_config = {
        "global": {
            "disk_file_names": {
                "file1": "file1_dev"
            },
            "additional_label": ""
        }
    }
    user_config = {
        "global": {
            "run_label": "run123"
        }
    }

    # Test when dataset is None, manual_label is empty, and suffix is 'csv'
    result = create_file_name(dev_config=dev_config, user_config=user_config, file_name_id="file1", dataset=None, suffix="csv")
    assert result == "file1_dev__run123.csv"

    # Test when dataset is provided, manual_label is empty, and suffix is 'txt'
    result = create_file_name(dev_config=dev_config, user_config=user_config, file_name_id="file1", dataset="dataset1", suffix="txt")
    assert result == "file1_dev_dataset1_run123.txt"

    # Test when manual_label is provided, and dataset and suffix are None
    result = create_file_name(dev_config=dev_config, user_config=user_config, file_name_id="file1", dataset=None)
    assert result == "file1_dev__run123.csv"

    # Test when all parameters are provided
    result = create_file_name(dev_config=dev_config, user_config=user_config, file_name_id="file1", dataset="dataset1", suffix="txt")
    assert result == "file1_dev_dataset1_run123.txt"


def test_write_out(tmp_path):
    data = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6]
    })
    output_path = Path(tmp_path) / "output.csv"

    write_out(data, output_path)

    assert os.path.isfile(output_path)
    assert output_path.exists()

    loaded_data = pd.read_csv(output_path, index_col=0)
    assert data.equals(loaded_data)

    #captured = capsys.readouterr()
    #assert f"Dataset written to {output_path}." in captured.out
