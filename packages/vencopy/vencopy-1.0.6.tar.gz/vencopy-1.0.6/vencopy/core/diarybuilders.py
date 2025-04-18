__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import datetime as dt
import logging
import time
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from ..utils.metadata import read_metadata_config, write_out_metadata
from ..utils.utils import create_file_name, write_out


class DiaryBuilder:
    def __init__(self, configs: dict, data: dict, is_week_diary: bool = False):
        """
        Wrapper function to build daily or weekly travel diaries from single vehicle trips.
        The class also discretises the profiles from a table format into a timeseries format.

        Args:
            configs (dict): A dictionary containing a user_config dictionary and a dev_config dictionary.
            activities (pd.DataFrame): A dataframe containing all trip and parking activities.
            is_week_diary (bool, optional): Boolean identifing whether a weekly diary should be created.
                Defaults to False.
        """
        self.dev_config = configs["dev_config"]
        self.user_config = configs["user_config"]
        self.dataset = configs["user_config"]["global"]["dataset"]
        self.data = data
        self.activities = data["activities"]
        self.time_resolution = configs["user_config"]["diarybuilders"][
            "time_resolution"
        ]
        self.consider_plugging_behaviour = self.user_config["flexestimators"][
            "plugging_behaviour"
        ]["consider_plugging_behaviour"]
        self.is_week_diary = is_week_diary
        self.drain = None
        self.charging_power = None
        self.uncontrolled_charging = None
        self.max_battery_level = None
        self.min_battery_level = None
        self.distributor = TimeDiscretiser(
            dataset=self.dataset,
            dev_config=self.dev_config,
            user_config=self.user_config,
            time_resolution=self.time_resolution,
            is_week=is_week_diary,
        )

    def __update_activities(self):
        """
        Updates timestamps and removes activities whose length equals zero to avoid inconsistencies in profiles
        which are separately discretised (interdependence at single vehicle level of drain, charging power etc i.e.
        no charging available when driving).
        """
        self.activities = self._correct_timestamps(
            activities=self.activities, time_resolution=self.time_resolution
        )
        self.activities = self._removes_zero_length_activities(
            activities=self.activities
        )

    @staticmethod
    def _correct_timestamps(activities, time_resolution) -> pd.DataFrame:
        """
        Rounds timestamps to predefined resolution. Edge case of immobile vehicle
        timestamps being set to 1 day.

        Args:
            activities (pd.DataFrame): A dataframe containing all trip and parking activities.
            time_resolution (int): Time resolution as specified in the user_config.

        Returns:
            pd.DataFrame: A dataframe containing all trip and parking activities.
        """
        activities["timestamp_start_corrected"] = activities[
            "timestamp_start"
        ].dt.round(f"{time_resolution}min")
        activities["timestamp_end_corrected"] = activities["timestamp_end"].dt.round(
            f"{time_resolution}min"
        )

        # Calculate activity duration based on new timestamps
        activities["activity_duration"] = (
            activities["timestamp_end_corrected"]
            - activities["timestamp_start_corrected"]
        )

        # Account for immobile vehicle that otherwise get deleted because activity duration is 0
        activities.loc[
            (activities["is_first_activity"] == True)  # noqa: E712
            & (activities["is_last_activity"] == True),  # noqa: E712
            "activity_duration",
        ] = dt.timedelta(days=1)
        return activities

    @staticmethod
    def _removes_zero_length_activities(activities):
        """
        Drops line when activity duration is zero, which causes inconsistencies in diaryBuilder
        (e.g. division by zero in number_bins calculation).

        Args:
            activities (pd.DataFrame): A dataframe containing all trip and parking activities.

        Returns:
            pd.DataFrame: A dataframe containing all trip and parking activities.
        """
        start_length = len(activities)
        activities = activities.drop(
            activities[activities.activity_duration == pd.Timedelta(0)].index.to_list()
        )
        end_length = len(activities)
        logging.info(
            f"{start_length - end_length} activities dropped from {start_length} total activities because activity "
            "start and end time are the same."
        )
        return activities

    def generate_metadata(self, metadata_config, file_name):
        """
        _summary_

        Args:
            metadata_config (_type_): _description_
            file_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        metadata_config["name"] = file_name
        metadata_config["title"] = (
            "Discetised timeseries with venco.py output profiles at single vehicle level"
        )
        metadata_config["description"] = (
            "Time discrete profile at single vehicle level."
        )
        metadata_config["sources"] = [
            f for f in metadata_config["sources"] if f["title"] in self.dataset
        ]
        reference_resource = metadata_config["resources"][0]
        this_resource = reference_resource.copy()
        this_resource["name"] = file_name.rstrip(".csv")
        this_resource["path"] = file_name
        these_fields = [
            f
            for f in reference_resource["schema"][self.dataset]["fields"][
                "diarybuilders"
            ]
        ]
        this_resource["schema"] = {"fields": these_fields}
        metadata_config["resources"].pop()
        metadata_config["resources"].append(this_resource)
        return metadata_config

    def _write_metadata(self, file_name):
        metadata_config = read_metadata_config()
        class_metadata = self.generate_metadata(
            metadata_config=metadata_config, file_name=file_name.name
        )
        write_out_metadata(
            metadata_yaml=class_metadata,
            file_name=file_name.as_posix().replace(".csv", ".metadata.yaml"),
        )

    def create_diaries(self):
        """
        Wrapper function to discretise the profiles.
        """
        start_time = time.time()
        self.__update_activities()
        self.drain = self.distributor.discretise(
            activities=self.activities, profile_name="drain", method="distribute"
        )
        if self.consider_plugging_behaviour:
            self.charging_power = self.distributor.discretise(
                activities=self.activities,
                profile_name="connection_power",
                method="select",
            )
        else:
            self.charging_power = self.distributor.discretise(
                activities=self.activities,
                profile_name="available_power",
                method="select",
            )
        self.uncontrolled_charging = self.distributor.discretise(
            activities=self.activities,
            profile_name="uncontrolled_charging",
            method="dynamic",
        )
        self.max_battery_level = self.distributor.discretise(
            activities=self.activities,
            profile_name="max_battery_level_start",  # was max_battery_level_start
            method="dynamic",
        )
        self.min_battery_level = self.distributor.discretise(
            activities=self.activities,
            profile_name="min_battery_level_start",  # was min_battery_level_end
            method="dynamic",
        )
        if self.user_config["global"]["write_output_to_disk"]["diary_output"]:
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["diary_output"]
            self.dev_config["global"]["additional_label"] = ""
            file_name = create_file_name(
                dev_config=self.dev_config,
                user_config=self.user_config,
                file_name_id="output_diarybuilder",
                dataset=self.dataset,
            )
            if self.user_config["global"]["write_output_to_disk"]["metadata"]:
                self._write_metadata(file_name=root / folder / file_name)
        needed_time = time.time() - start_time
        self.data["activities"] = self.activities
        logging.info(f"Needed time to discretise all columns: {needed_time} seconds.")


class TimeDiscretiser:
    def __init__(
        self,
        time_resolution: int,
        dataset: str,
        user_config: dict,
        dev_config: dict,
        is_week: bool = False,
    ):
        """
        Class for discretisation of activities to fixed temporal resolution.

        Args:
            time_resolution (int): Integer specifying the fixed resolution that the discretisation should use.
            dataset (str):
            user_config (dict): _description_
            dev_config (dict): _description_
            is_week (bool, optional): _description_. Defaults to False.
        """
        self.activities = None
        self.dataset = dataset
        self.data_to_discretise = None
        self.user_config = user_config
        self.dev_config = dev_config
        self.quantum = pd.Timedelta(value=1, unit="min")
        self.time_resolution = time_resolution  # e.g. 15 min
        self.is_week = is_week
        self.number_time_slots = int(
            self.__number_slots_per_interval(
                interval=pd.Timedelta(value=self.time_resolution, unit="min")
            )
        )
        if is_week:
            self.time_delta = pd.timedelta_range(
                start="00:00:00", end="168:00:00", freq=f"{self.time_resolution}T"
            )
            self.weekdays = self.activities["trip_start_weekday"].unique()
        else:  # is Day
            self.time_delta = pd.timedelta_range(
                start="00:00:00", end="24:00:00", freq=f"{self.time_resolution}T"
            )
        self.time_index = list(self.time_delta)
        self.discrete_data = None

    def __number_slots_per_interval(self, interval: pd.Timedelta) -> int:
        """
        Check if interval is an integer multiple of quantum.
        The minimum resolution is 1 min, case for resolution below 1 min.
        Then check if an integer number of intervals fits into one day (15 min equals 96 intervals)

        Args:
            interval (pd.Timedelta): _description_

        Returns:
            int: _description_
        """
        if interval.seconds / 60 < self.quantum.seconds / 60:
            raise (
                ValueError(
                    f"The specified resolution is not a multiple of {self.quantum} minute, "
                    f"which is the minmum possible resolution"
                )
            )
        quot = interval.seconds / 3600 / 24
        quot_day = pd.Timedelta(value=24, unit="h") / interval
        if (1 / quot) % int(1 / quot) == 0:  # or (quot % int(1) == 0):
            return quot_day
        else:
            raise (
                ValueError(
                    f"The specified resolution does not fit into a day."
                    f"There cannot be {quot_day} finite intervals in a day"
                )
            )

    def __dataset_cleanup(self):
        """
        Cleans up the activities dataset by removing the columns not used.
        """
        self.__remove_columns()
        self.__correct_values()
        self.__correct_timestamps()

    def __remove_columns(self):
        """
        Removes additional columns not used in the TimeDiscretiser class.
        Only keeps timestamp start and end, unique ID, and the column to discretise.
        """
        necessary_columns = [
            "trip_id",
            "timestamp_start",
            "timestamp_end",
            "unique_id",
            "park_id",
            "is_first_activity",
            "is_last_activity",
            "time_delta",
            "activity_id",
            "next_activity_id",
            "previous_activity_id",
        ] + [self.column_to_discretise]
        if self.is_week:
            necessary_columns = necessary_columns + ["trip_start_weekday"]
        if self.column_to_discretise == "uncontrolled_charging":
            necessary_columns = necessary_columns + [
                "available_power",
                "timestamp_end_uncontrolled_charging",
            ]
        self.data_to_discretise = self.activities[necessary_columns].copy()

    def __correct_values(self):
        """
        Depending on the columns to discretise correct some values.
        - drain profile: pads NaN with 0s
        - uncontrolled_charging profile: instead of removing rows with trip_id, assign 0 to rows with trip_id
        - residual_need profile: pads NaN with 0s
        """
        if self.column_to_discretise == "drain":
            self.data_to_discretise["drain"] = self.data_to_discretise["drain"].fillna(
                0
            )
        elif self.column_to_discretise == "uncontrolled_charging":
            self.data_to_discretise["uncontrolled_charging"] = self.data_to_discretise[
                "uncontrolled_charging"
            ].fillna(0)
            # start_number_vehicles = len(self.data_to_discretise)
            # remove immobile vehicles which do not contribute to UC profile levels (only account in
            # #normalisation for them)
            # self.data_to_discretise = self.data_to_discretise.drop((self.data_to_discretise[(
            # self.data_to_discretise['is_first_activity'] == True)
            # & (self.data_to_discretise['is_last_activity'] == True)]).index.to_list())
            # end_number_vehicles = len(self.data_to_discretise)
            # logging.info(f"Removed {start_number_vehicles - end_number_vehicles} immobile vehicles from
            # uncontrolled charging profile discretisation.")
        elif self.column_to_discretise == "residual_need":
            self.data_to_discretise["residual_need"] = self.data_to_discretise[
                "residual_need"
            ].fillna(0)

    def __correct_timestamps(self):
        """
        Rounds timestamps to predifined resolution for all activities and
        specific uncontrolled charging end timestamp.
        """
        self.data_to_discretise["timestamp_start_corrected"] = self.data_to_discretise[
            "timestamp_start"
        ].dt.round(f"{self.time_resolution}min")
        self.data_to_discretise["timestamp_end_corrected"] = self.data_to_discretise[
            "timestamp_end"
        ].dt.round(f"{self.time_resolution}min")

    def __identify_bin_shares(self):
        """
        Calculates value share to be assigned to bins and identifies the bins.
        Includes a wrapper for the 'distribute', 'select' and 'dynamic' method.
        """
        self.__calculate_number_bins()
        self.__identify_bins()
        if self.method == "distribute":
            self.__value_distribute()
        elif self.method == "select":
            self.__value_select()
        elif self.method == "dynamic":
            if self.column_to_discretise in (
                "max_battery_level_start",
                "min_battery_level_start",
                "min_battery_level_end",
                "max_battery_level_end",
            ):
                self.__value_non_linear_level()  # TODO: change with max and min vol charged
            elif self.column_to_discretise == "uncontrolled_charging":
                self.__value_non_linear_charge()
        else:
            raise (
                ValueError(
                    f'Specified method {self.method} is not implemented please specify "distribute" or "select".'
                )
            )

    def __calculate_number_bins(self):
        """
        Updates the activity duration based on the rounded timstamps.
        Calculates the multiple of time_resolution of the activity duration and stores it to column number_bins
        (e.g. a 2h-activity) with a time_resolution of 15 mins would have a 8 in the column.
        """
        self.data_to_discretise["activity_duration"] = (
            self.data_to_discretise["timestamp_end_corrected"]
            - self.data_to_discretise["timestamp_start_corrected"]
        )
        # reset the immobile vehicle activity duration so that these are not removed
        self.data_to_discretise.loc[
            (self.data_to_discretise["is_first_activity"] == True)  # noqa: E712
            & (self.data_to_discretise["is_last_activity"] == True),  # noqa: E712
            "activity_duration",
        ] = dt.timedelta(days=1)
        self.__removes_zero_length_activities()
        self.data_to_discretise["number_bins"] = self.data_to_discretise[
            "activity_duration"
        ] / (pd.Timedelta(value=self.time_resolution, unit="min"))
        if not self.data_to_discretise["number_bins"].apply(float.is_integer).all():
            raise ValueError("Not all bin counts are integers.")
        self.__drop_if_number_bins_length_is_zero()
        self.data_to_discretise["number_bins"] = self.data_to_discretise[
            "number_bins"
        ].astype(int)

    def __drop_if_number_bins_length_is_zero(self):
        """
        Drops line when number_bins is zero, which cause division by zero in number_bins calculation.
        """
        start_length = len(self.data_to_discretise)
        self.data_to_discretise.drop(
            self.data_to_discretise[self.data_to_discretise.number_bins == 0].index
        )
        end_length = len(self.data_to_discretise)
        dropped_profiles = start_length - end_length
        if dropped_profiles != 0:
            raise ValueError(
                f"{dropped_profiles} activities dropped because bin lenght equals zero."
            )

    def __value_distribute(self):
        """
        Calculates the profile value for each bin for the 'distribute' method.
        """
        if self.data_to_discretise["number_bins"].any() == 0:
            raise ArithmeticError(
                "The total number of bins is zero for one activity, which caused a division by zero."
                "This should not happen because events with length zero should have been dropped."
            )
        self.data_to_discretise["value_per_bin"] = (
            self.data_to_discretise[self.column_to_discretise]
            / self.data_to_discretise["number_bins"]
        )

    def __value_select(self):
        """
        Calculates the profile value for each bin for the 'select' method.
        """
        self.data_to_discretise["value_per_bin"] = self.data_to_discretise[
            self.column_to_discretise
        ]

    def __value_non_linear_level(self):
        """
        Calculates the bin values dynamically (e.g. for the battery level). It returns a
        non-linearly increasing list of values capped to upper and lower battery
        capacity limitations. The list of values is allocated to bins in the
        function __allocate() in the same way as for value-per-bins.
        """
        self.__delta_battery_level_driving(
            data=self.data_to_discretise, column=self.column_to_discretise
        )  # linear
        self.__delta_battery_level_charging(
            data=self.data_to_discretise, column=self.column_to_discretise
        )  # not linear

    def __delta_battery_level_driving(self, data: pd.DataFrame, column: str):
        """
        Calculates decreasing battery level values for driving activities for
        both cases, minimum and maximum battery level.
        The function __increase_level_per_bin() is applied to the whole data
        set with the respective start battery levels (soc_start), battery
        level increases(added_energy_per_bin) and number_bins for each
        activity respectively in a vectorized manner.
        The function adds a column 'value_per_bin' to data directly,
        thus it doesn'treturn anything.

        Args:
            data (pd.DataFrame): Activity data with activities in rows and at
            least
            the columns column, 'drain_per_bin', 'value_per_bin', 'park_id' and
            'number_bins'.
            column (str): The column to descritize. Currently only
            max_battery_level_start and min_battery_level_start are
            implemented.
        """
        if (column == "max_battery_level_end") or (column == "min_battery_level_end"):
            raise NotImplementedError("The method has not been implemented yet.")

        elif (column == "max_battery_level_start") or (
            column == "min_battery_level_start"
        ):
            data["drain_per_bin"] = (self.activities.drain / data.number_bins) * -1

        data["value_per_bin"] = data.loc[data["park_id"].isna(), :].apply(
            lambda x: self.__increase_level_per_bin(
                soc_start=x[column],
                added_energy_per_bin=x["drain_per_bin"],
                number_bins=x["number_bins"],
            ),
            axis=1,
        )
        data.loc[data["park_id"].isna(), "value_per_bin"] = data.loc[
            data["park_id"].isna(), "value_per_bin"
        ].apply(
            self._enforce_battery_limit,
            how="lower",
            lim=self.user_config["flexestimators"]["battery"]["battery_capacity"]
            * self.user_config["flexestimators"]["battery"]["minimum_soc"],
        )

        # (overnightsplitting)
        data.loc[
            data["park_id"].isna() & data["is_first_activity"], "maximum_morning_value"
        ] = data.loc[
            data["park_id"].isna() & data["is_first_activity"], "value_per_bin"
        ].apply(
            lambda x: max(x) if isinstance(x, list) else np.nan
        )

        unique_id_to_maximum_value = (
            data.loc[data["park_id"].isna() & data["is_first_activity"]]
            .set_index("unique_id")["maximum_morning_value"]
            .to_dict()
        )

        data.loc[
            data["park_id"].isna() & data["is_last_activity"], "maximum_morning_value"
        ] = data.loc[
            data["park_id"].isna() & data["is_last_activity"], "unique_id"
        ].map(
            unique_id_to_maximum_value
        )

        data.loc[
            data["park_id"].isna() & data["is_last_activity"], "value_per_bin"
        ] = data.loc[data["park_id"].isna() & data["is_last_activity"]].apply(
            lambda row: self._enforce_battery_limit(
                delta_battery=row["value_per_bin"],
                how="upper",
                lim=row["maximum_morning_value"],
            ),
            axis=1,
        )

    def __delta_battery_level_charging(self, data: pd.DataFrame, column: str):
        """
        Calculates increasing battery level values for park / charging
        activities for both cases, minimum and maximum battery level. The cases
        have to be differentiated because the max case runs chronologically
        from morning to evening. Charging volumes per bin are
        calculated from the 'max/min_charge_volume' column in data.
        The function __increase_level_per_bin() is applied to the whole data
        set with the respective start battery levels (soc_start), battery
        level increases (added_energy_per_bin) and number_bins for each
        activity respectively in a vectorized manner.
        Then, battery capacity limitations are enforced applying the
        function _enforce_battery_limit().
        The function adds a column 'value_per_bin' to data directly,
        thus it doesn'treturn anything.
        After that the first activity minimum value is calculated and stored
        in another column called "minimum morning value" to then apply this
        value as a limit to the last activity of the day (also done with
        _enforce_battery_limit)

        Args:
            data (pd.DataFrame): DataFrame with activities in rows and at least
            the columns column, 'max/min_charge_volume', 'trip_id' and
            'number_bins'.
            column (str): The column to descritize. Currently only
            max_battery_level_start and min_battery_level_start are
            implemented.
        """
        if (column == "min_battery_level_end") or (column == "max_battery_level_end"):
            raise NotImplementedError("The method has not been implemented yet.")
        if self.user_config["flexestimators"]["cccv_charging"]["consider_cccv"]:
            if column == "max_battery_level_start":
                data["charge_per_bin"] = self.activities.max_charge_volume / (
                    self.activities.activity_duration / pd.Timedelta("1 hour")
                )
            elif column == "min_battery_level_start":
                data["charge_per_bin"] = self.activities.min_charge_volume / (
                    self.activities.activity_duration / pd.Timedelta("1 hour")
                )
            data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[
                data["trip_id"].isna(), :
            ].apply(
                lambda x: self.__increase_level_per_bin(
                    soc_start=x[column],
                    added_energy_per_bin=x["charge_per_bin"],
                    number_bins=x["number_bins"],
                ),
                axis=1,
            )
            data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[
                data["trip_id"].isna(), "value_per_bin"
            ].apply(
                self._enforce_battery_limit,
                how="upper",
                lim=self.user_config["flexestimators"]["battery"]["battery_capacity"]
                * self.user_config["flexestimators"]["battery"]["maximum_soc"],
            )

            data.loc[
                data["trip_id"].isna() & data["is_first_activity"], "minimum_morning_value"
            ] = data.loc[
                data["trip_id"].isna() & data["is_first_activity"], "value_per_bin"
            ].apply(
                lambda x: min(x) if isinstance(x, list) else np.nan
            )

            # Create a dictionary to map unique_id to minimum_morning_value
            unique_id_to_minimum_value = (
                data.loc[data["trip_id"].isna() & data["is_first_activity"]]
                .set_index("unique_id")["minimum_morning_value"]
                .to_dict()
            )

            # Update minimum_morning_value for rows where is_last_activity is
            # True and unique_id matches
            data.loc[
                data["trip_id"].isna() & data["is_last_activity"], "minimum_morning_value"
            ] = data.loc[
                data["trip_id"].isna() & data["is_last_activity"], "unique_id"
            ].map(
                unique_id_to_minimum_value
            )

            data.loc[
                data["trip_id"].isna() & data["is_last_activity"], "value_per_bin"
            ] = data.loc[data["trip_id"].isna() & data["is_last_activity"]].apply(
                lambda row: self._enforce_battery_limit(
                    delta_battery=row["value_per_bin"],
                    how="upper",
                    lim=row["minimum_morning_value"],
                ),
                axis=1,
            )
        else:  # no cccv
            if column == "max_battery_level_start":
                data["charge_per_bin"] = self.activities.available_power * self.time_resolution / 60
                data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[data["trip_id"].isna(), :].apply(
                    lambda x: self.__increase_level_per_bin(
                        soc_start=x[column], added_energy_per_bin=x["charge_per_bin"], number_bins=x["number_bins"]
                    ),
                    axis=1,
                )
                data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[
                    data["trip_id"].isna(), "value_per_bin"
                ].apply(
                    self._enforce_battery_limit,
                    how="upper",
                    lim=self.user_config["flexestimators"]["battery"][
                        "battery_capacity"
                    ]
                    * self.user_config["flexestimators"]["battery"]["maximum_soc"],
                )
            elif column == "min_battery_level_start":
                data["charge_per_bin"] = self.activities.available_power * self.time_resolution / 60 * -1
                data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[data["trip_id"].isna(), :].apply(
                    lambda x: self.__increase_level_per_bin(
                        soc_start=x[column], added_energy_per_bin=x["charge_per_bin"], number_bins=x["number_bins"]
                    ),
                    axis=1,
                )
                data.loc[data["trip_id"].isna(), "value_per_bin"] = data.loc[
                    data["trip_id"].isna(), "value_per_bin"
                ].apply(
                    self._enforce_battery_limit,
                    how="lower",
                    lim=self.user_config["flexestimators"]["battery"][
                        "battery_capacity"
                    ]
                    * self.user_config["flexestimators"]["battery"]["minimum_soc"],
                )

    def __increase_level_per_bin(
        self, soc_start: float, added_energy_per_bin: float, number_bins: int
    ) -> list:
        """
        Returns a list of battery level values with length number_bins starting
        with soc_start with added value of added_energy_per_bin.

        Args:
            soc_start (float): Starting battery SoC
            added_energy_per_bin (float): Consecutive (constant) additions to
            the start battery energy level
            number_bins (int): Number of discretised bins (one per timeslot)

        Returns:
            list: List of number_bins increasing battery level values
        """
        tmp = soc_start
        lst = [tmp]
        for _ in range(number_bins - 1):
            tmp += added_energy_per_bin
            lst.append(tmp)
        return lst

    def _enforce_battery_limit(self, delta_battery: list, how: str, lim: float) -> list:
        """
        Lower-level function that caps a list of values at lower or upper
        (determined by how) limits given by limit. Thus [0, 40, 60] with
        how=upper and lim=50 would return [0, 40, 50].

        Args:
            delta_battery (list): List of float values of arbitrary length.
            how (str): Must be either 'upper' or 'lower'.
            lim (float): Number of threshold to which to limit the values in
            the list.

        Returns:
            list: Returns a list of same length with values limited to lim.
        """
        if how == "lower":
            return [max(i, lim) for i in delta_battery]
        elif how == "upper":
            return [min(i, lim) for i in delta_battery]

    def __value_non_linear_charge(self):
        """
        Wrapper to calculate the value of charging when this is not linear.
        """
        self.__uncontrolled_charging_parking()
        self.__uncontrolled_charging_driving()

    def __uncontrolled_charging_parking(self):
        """
        Discretises the uncontrolled charging profile during a parking activity.
        """
        timestamp_end_uncontrolled_charging = self.data_to_discretise.apply(
            lambda row: (
                row["timestamp_end"]
                if row["timestamp_end_uncontrolled_charging"] is None
                else row["timestamp_end_uncontrolled_charging"]
            ),
            axis=1,
        )
        timestamp_end_uncontrolled_charging_corrected = (
            timestamp_end_uncontrolled_charging.dt.round(f"{self.time_resolution}min")
        )
        self.data_to_discretise["timestamp_end_uncontrolled_charging_corrected"] = (
            timestamp_end_uncontrolled_charging_corrected
        )
        self.data_to_discretise["time_delta_uncontrolled_charging"] = (
            self.data_to_discretise["timestamp_end_uncontrolled_charging_corrected"]
            - self.data_to_discretise["timestamp_start"]
        )
        self.data_to_discretise["number_full_bins_uncontrolled_charging"] = (
            self.data_to_discretise.loc[
                self.data_to_discretise["trip_id"].isna(),
                "time_delta_uncontrolled_charging",
            ].dt.total_seconds()
            / 60
            / self.time_resolution
        ).astype(int)
        self.data_to_discretise["value_per_bin"] = self.data_to_discretise.loc[
            self.data_to_discretise["trip_id"].isna(), :
        ].apply(
            lambda x: self.__charge_rate_per_bin(
                charging_rate=x["available_power"],
                charged_volume=x["uncontrolled_charging"],
                number_bins=x["number_bins"],
            ),
            axis=1,
        )

    def __uncontrolled_charging_driving(self):
        """
        Assign 0 to uncontrolled charging while driving.
        """
        self.data_to_discretise.loc[
            self.data_to_discretise["park_id"].isna(), "value_per_bin"
        ] = 0

    def __charge_rate_per_bin(
        self, charging_rate: float, charged_volume: float, number_bins: int
    ) -> list:
        # TODO: update to max_charge/min_charge_volume from cccv
        """
        Calculate the charging rate for each bin.

        Args:
            charging_rate (float): _description_
            charged_volume (float): _description_
            number_bins (int): _description_

        Returns:
            list: _description_
        """
        if charging_rate == 0:
            return [0] * number_bins
        charging_rates_per_bin = [charging_rate] * number_bins
        volumes_per_bin = [
            r * self.time_resolution / 60 for r in charging_rates_per_bin
        ]
        charged_energy = np.cumsum(volumes_per_bin)
        indeces_overshoot = [
            idx for idx, en in enumerate(charged_energy) if en > charged_volume
        ]

        # Incomplete bin treatment
        if indeces_overshoot:
            bin_overshoot = indeces_overshoot.pop(0)
        # uncontrolled charging never completed during activity. This occurs when discretised activity is shorter than
        # original due to discr. e.g. unique_id == 10040082, park_id==5 starts at 16:10 and ends at 17:00, with
        # time_resolution=15 min it has 3 bins reducing the discretised duration to 45 minutes instead of 50 minutes.
        elif charged_energy[0] < charged_volume:
            return volumes_per_bin
        else:  # uncontrolled charging completed in first bin
            return [round(charged_volume, 3)]

        if bin_overshoot == 0:
            value_last_charged_bin = round(charged_volume, 3)
        else:
            value_last_charged_bin = round(
                (charged_volume - charged_energy[bin_overshoot - 1]), 3
            )

        return (
            volumes_per_bin[:bin_overshoot]
            + [value_last_charged_bin]
            + [0] * (len(indeces_overshoot))
        )

    def __identify_bins(self):
        """
        Wrapper which identifies the first and the last bin.
        """
        self.__identify_first_bin()
        self.__identify_last_bin()

    def __identify_first_bin(self):
        """
        Identifies every first bin for each activity (trip or parking).
        """
        self.data_to_discretise["timestamp_start_corrected"] = self.data_to_discretise[
            "timestamp_start_corrected"
        ].apply(lambda x: pd.to_datetime(str(x)))
        day_start = self.data_to_discretise["timestamp_start_corrected"].apply(
            lambda x: pd.Timestamp(year=x.year, month=x.month, day=x.day)
        )
        self.data_to_discretise["daily_time_delta_start"] = (
            self.data_to_discretise["timestamp_start_corrected"] - day_start
        )
        self.data_to_discretise["start_time_from_midnight_seconds"] = (
            self.data_to_discretise["daily_time_delta_start"].apply(lambda x: x.seconds)
        )
        bins = pd.DataFrame({"bin_timestamp": self.time_delta})
        bins.drop(
            bins.tail(1).index, inplace=True
        )  # remove last element, which is zero
        self.bin_from_midnight_seconds = bins["bin_timestamp"].apply(
            lambda x: x.seconds
        )
        self.bin_from_midnight_seconds = self.bin_from_midnight_seconds + (
            self.time_resolution * 60
        )
        self.data_to_discretise["first_bin"] = (
            self.data_to_discretise["start_time_from_midnight_seconds"].apply(
                lambda x: np.argmax(x < self.bin_from_midnight_seconds)
            )
        ).astype(int)
        if self.data_to_discretise["first_bin"].any() > self.number_time_slots:
            raise ArithmeticError(
                "One of first bin values is bigger than total number of bins."
            )
        if self.data_to_discretise["first_bin"].unique().any() < 0:
            raise ArithmeticError("One of first bin values is smaller than 0.")
        if self.data_to_discretise["first_bin"].isna().any():
            raise ArithmeticError("One of first bin values is NaN.")

    def __identify_last_bin(self):
        """
        Identifies every last bin for each activity (trip or parking).
        """
        day_end = self.data_to_discretise["timestamp_end_corrected"].apply(
            lambda x: pd.Timestamp(year=x.year, month=x.month, day=x.day)
        )
        self.data_to_discretise["daily_time_delta_end"] = (
            self.data_to_discretise["timestamp_end_corrected"] - day_end
        )
        self.data_to_discretise["last_bin"] = (
            self.data_to_discretise["first_bin"]
            + self.data_to_discretise["number_bins"]
            - 1
        ).astype(int)
        if self.data_to_discretise["last_bin"].any() > self.number_time_slots:
            raise ArithmeticError(
                "One of first bin values is bigger than total number of bins."
            )
        if self.data_to_discretise["last_bin"].unique().any() < 0:
            raise ArithmeticError("One of first bin values is smaller than 0.")
        if self.data_to_discretise["last_bin"].isna().any():
            raise ArithmeticError("One of first bin values is NaN.")

    def __allocate_bin_shares(self):
        """
        Wrapper which identifies shared bins and allocates them to a discrestised structure.
        """
        self.discrete_data = (
            self.__allocate_week() if self.is_week else self.__allocate()
        )
        self.__check_bin_values()

    def __check_bin_values(self):
        """
        Verifies that all bins get a value assigned, otherwise raise an error.
        """
        if self.discrete_data.isna().any().any():
            raise ValueError("There are NaN in the dataset.")

    def __removes_zero_length_activities(self):
        """
        Implements a strategy for overlapping bins if time resolution high enough so that the event becomes negligible,
        i.e. drops events with no length (timestamp_start_corrected = timestamp_end_corrected or activity_duration = 0),
        which cause division by zero in number_bins calculation.
        """
        start_length = len(self.data_to_discretise)
        indeces_no_length_activities = self.data_to_discretise[
            self.data_to_discretise.activity_duration == pd.Timedelta(0)
        ].index.to_list()
        self.ids_with_no_length_activities = self.data_to_discretise.loc[
            indeces_no_length_activities
        ]["unique_id"].unique()
        self.data_to_discretise = self.data_to_discretise.drop(
            indeces_no_length_activities
        )
        end_length = len(self.data_to_discretise)
        dropped_activities = start_length - end_length
        if dropped_activities != 0:
            raise ValueError(
                f"{dropped_activities} zero-length activities dropped from {len(self.ids_with_no_length_activities)} "
                "IDs."
            )
        self.__remove_activities_with_zero_value()

    def __remove_activities_with_zero_value(self):
        """
        Removes activities which end up having zero value in the bin.

        Raises:
            ValueError: Error raised when the activities dropped are more than the ones initially dropped when
                rounding the timestamps.
        """
        start_length = len(self.data_to_discretise)
        subset_no_length_activities_ids = self.data_to_discretise.loc[
            self.data_to_discretise.unique_id.isin(self.ids_with_no_length_activities)
        ]
        subset_no_length_activities_ids = subset_no_length_activities_ids.set_index(
            "unique_id", drop=False
        )
        subset_no_length_activities_ids.index.names = ["unique_id_index"]
        ids_with_sum_zero = subset_no_length_activities_ids.groupby(["unique_id"])[
            self.column_to_discretise
        ].sum()
        ids_to_drop = ids_with_sum_zero[ids_with_sum_zero == 0].index
        self.data_to_discretise = self.data_to_discretise.loc[
            ~self.data_to_discretise.unique_id.isin(ids_to_drop)
        ]
        end_length = len(self.data_to_discretise)
        dropped_activities = start_length - end_length
        if dropped_activities != 0:
            raise ValueError(
                f"Additional {dropped_activities} activities dropped as the sum of all {self.column_to_discretise} "
                "activities for the specific ID was zero."
            )

    def __allocate_week(self):
        """
        Wrapper method for allocating respective values per bin to days within a week. Expects that the activities
        are formatted in a way that unique_id represents a unique week ID. The function then loops over the 7 weekdays
        and calls __allocate for each day a total of 7 times.

        Raises:
            NotImplementedError: The error is raised if the selected discretisation method does not exist.
        """
        raise NotImplementedError("The method has not been implemneted yet.")

    def __allocate(self) -> pd.DataFrame:
        """
        Loops over every activity (row) and allocates the respective value per bin (value_per_bin) to each column
        specified in the columns first_bin and last_bin.

        Returns:
            pd.DataFrame: Discretised data set with temporal discretisations in the columns.
        """
        trips = self.data_to_discretise.copy()
        trips = trips[["unique_id", "first_bin", "last_bin", "value_per_bin"]]
        trips["unique_id"] = trips["unique_id"].astype(int)
        return trips.groupby(by="unique_id").apply(self.assign_bins)

    def assign_bins(self, activities: pd.DataFrame) -> pd.Series:
        """
        Assigns values for every unique_id based on first and last bin.

        Args:
            activities (pd.DataFrame): A dataframe containing all trip and parking activities.

        Returns:
            pd.Series: Series containing the value depending on the profile to discretise and the time resolution.
        """
        s = pd.Series(index=range(self.number_time_slots), dtype=float)
        for _, itrip in activities.iterrows():
            start = itrip["first_bin"]
            end = itrip["last_bin"]
            value = itrip["value_per_bin"]
            if self.column_to_discretise == "min_battery_level_end":
                s.loc[start:end] = value[::-1]
            else:
                s.loc[start:end] = value
        return s

    def __write_output(self):
        """
        Function to write output to disk.
        """
        if self.user_config["global"]["write_output_to_disk"]["diary_output"]:
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["diary_output"]
            self.dev_config["global"]["additional_label"] = self.column_to_discretise
            file_name = create_file_name(
                dev_config=self.dev_config,
                user_config=self.user_config,
                file_name_id="output_diarybuilder",
                dataset=self.dataset,
            )
            write_out(data=self.discrete_data, path=root / folder / file_name)

    def discretise(self, activities, profile_name: str, method: str) -> pd.DataFrame:
        """
        Wrapper function to discretise the venco.py output profiles from a table format to a timeseries format.

        Args:
            activities (pd.DataFrame): A dataframe containing all trip and parking activities.
            profile_name (str): Name fo the profile to be discretised
            method (str): method specifies how the discretisation should be carried out. 'Distribute' assumes
                          act provides a divisible variable (energy, distance etc.) and distributes this
                          depending on the time share of the activity within the respective time interval.
                          'Select' assumes an undivisible variable such as power is given and selects
                          the values for the given timestamps. For now: If start or end timestamp of an
                          activity exactly hits the middle of a time interval (time_resolution/2), the value is
                          allocated if its ending but not if its starting (value set to 0). For time_resolution=30 min,
                          a parking activity ending at 9:15 with a charging availability of 11 kW, 11 kW will be
                          assigned to the last slot (9:00-9:30) whereas if it had started at 7:45, the slot (7:30-8:00)
                          is set to 0 kW.

        Returns:
            pd.DataFrame: Timeseries for each vehicle containing the value of the specified profile.
                The headers of the dataframe reflect the temporal resolution specified in the user_config.
        """
        self.column_to_discretise: Optional[str] = profile_name
        self.activities = activities
        self.method = method
        logging.info(f"Starting to discretise {self.column_to_discretise}.")
        start_time_diary_builder = time.time()
        self.__dataset_cleanup()
        self.__identify_bin_shares()
        self.__allocate_bin_shares()
        if self.user_config["global"]["write_output_to_disk"]["diary_output"]:
            self.__write_output()
        logging.info(f"Discretisation finished for {self.column_to_discretise}.")
        elapsed_time_diary_builder = time.time() - start_time_diary_builder
        logging.info(
            f"Needed time to discretise {self.column_to_discretise}: {elapsed_time_diary_builder} seconds."
        )
        self.column_to_discretise = None
        return self.discrete_data
