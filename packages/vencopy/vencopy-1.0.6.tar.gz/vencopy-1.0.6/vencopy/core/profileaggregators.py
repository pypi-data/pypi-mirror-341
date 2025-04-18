__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import logging
import time
from pathlib import Path

import pandas as pd

from ..core.diarybuilders import DiaryBuilder
from ..utils.metadata import read_metadata_config, write_out_metadata
from ..utils.utils import create_file_name, write_out


class ProfileAggregator:
    def __init__(self, configs: dict, data: dict, profiles: DiaryBuilder):
        """
        In the ProfileAggregator, single vehicle profiles are aggregated across all vehicles to gain fleet level
        profiles. Depending on the profile type, different aggregation approaches are used.
        The design pattern is similar as in the diarybuilders. There is one wrapper class, ProfileAggregator, that has
        an instance of the class Aggregator as attribute. This attribute's method perform_aggregation() is then called
        for each profile relevant for the analysis, specifying the profile type as a parameter ('flow' or 'state'). The
        profiles for drain, availability and uncontrolled charging are all flow profiles, whereas the battery level
        profiles are state profiles and thus, are aggregated differently.
        Two options can be given in the user_config for refining profile aggregation: The timespan and the aggregation
        weights. The timespan can be given in the option 'aggregation_timespan', specifying if the resulting profile is
        a daily profile or a weekly profile.
        The flow profiles are aggregated using means or weighted means which can be specified in the profileaggregators
        section of the user_config under the option 'weight_flow_profiles'. The aggregation does not change the temporal
        resolution, it is only related to aggregate the charging profiles from around 100,000 single-vehicle profiles to
        fleet profiles. Thus, after aggregation, there are 5 profiles with the temporal timespan (daily or weekly) and
        the temporal resolution selected in the diary builder before (e.g. 24 values for daily profiles with hourly
        resolution).

        Args:
            configs (dict): A dictionary containing a user_config dictionary and a dev_config dictionary
            activities (pd.DataFrame): A dataframe containing all trip and parking activities
            profiles (DiaryBuilder): An instance of type DiaryBuilder
        """
        self.user_config = configs["user_config"]
        self.dev_config = configs["dev_config"]
        self.dataset = self.user_config["global"]["dataset"]
        self.weighted = self.user_config["profileaggregators"]["weight_flow_profiles"]
        self.data = data
        self.activities = data["activities"]
        self.profiles = profiles
        self.drain = profiles.drain
        self.charging_power = profiles.charging_power
        self.uncontrolled_charging = profiles.uncontrolled_charging
        self.max_battery_level = profiles.max_battery_level
        self.min_battery_level = profiles.min_battery_level
        self.drain_weekly = pd.DataFrame()
        self.charging_power_weekly = pd.DataFrame()
        self.uncontrolled_charging_weekly = pd.DataFrame()
        self.max_battery_level_weekly = pd.DataFrame()
        self.min_battery_level_weekly = pd.DataFrame()
        self.aggregator = Aggregator(
            activities=self.activities,
            dataset=self.dataset,
            user_config=self.user_config,
            dev_config=self.dev_config,
            weighted=self.weighted,
        )

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
            "Discetised timeseries with venco.py output profiles at fleet level"
        )
        metadata_config["description"] = "Time discrete profile at fleet level."
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
                "profileaggregators"
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

    def aggregate_profiles(self):
        """
        Wrapper method for the ProfileAggregator class. This method is supposed to be called in the overarching venco.py
        workflow.
        """
        if (
            self.user_config["global"]["consider_temperature_cycle_dependency"][
                "season"
            ]
            == "all"
        ):
            seasons = ["spring", "summer", "winter", "fall"]
            for season in seasons:
                logging.info(f"Aggreagting a weekly profile for season: {season}")
                ids_season = self.activities[self.activities.season == season][
                    "unique_id"
                ].unique()
                self.drain_weekly[season] = self.aggregator.perform_aggregation(
                    profile=self.drain.loc[ids_season],
                    profile_name=f"drain_{season}",
                    method="flow",
                )
                self.charging_power_weekly[season] = (
                    self.aggregator.perform_aggregation(
                        profile=self.charging_power.loc[ids_season],
                        profile_name=f"charging_power_{season}",
                        method="flow",
                    )
                )
                self.uncontrolled_charging_weekly[season] = (
                    self.aggregator.perform_aggregation(
                        profile=self.uncontrolled_charging.loc[ids_season],
                        profile_name=f"uncontrolled_charging_{season}",
                        method="flow",
                    )
                )
                self.max_battery_level_weekly[season] = (
                    self.aggregator.perform_aggregation(
                        profile=self.max_battery_level.loc[ids_season],
                        profile_name=f"max_battery_level_{season}",
                        method="state",
                    )
                )
                self.min_battery_level_weekly[season] = (
                    self.aggregator.perform_aggregation(
                        profile=self.min_battery_level.loc[ids_season],
                        profile_name=f"min_battery_level_{season}",
                        method="state",
                    )
                )
        else:
            self.drain_weekly = self.aggregator.perform_aggregation(
                profile=self.drain, profile_name="drain", method="flow"
            )
            self.charging_power_weekly = self.aggregator.perform_aggregation(
                profile=self.charging_power,
                profile_name="charging_power",
                method="flow",
            )
            self.uncontrolled_charging_weekly = self.aggregator.perform_aggregation(
                profile=self.uncontrolled_charging,
                profile_name="uncontrolled_charging",
                method="flow",
            )
            self.max_battery_level_weekly = self.aggregator.perform_aggregation(
                profile=self.max_battery_level,
                profile_name="max_battery_level",
                method="state",
            )
            self.min_battery_level_weekly = self.aggregator.perform_aggregation(
                profile=self.min_battery_level,
                profile_name="min_battery_level",
                method="state",
            )
        if self.user_config["global"]["write_output_to_disk"]["aggregator_output"]:
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["aggregator_output"]
            file_name = create_file_name(
                dev_config=self.dev_config,
                user_config=self.user_config,
                file_name_id="output_profileaggregator",
                dataset=self.dataset
            )
            if self.user_config["global"]["write_output_to_disk"]["metadata"]:
                self._write_metadata(file_name=root / folder / file_name)
            logging.info("Aggregation finished for all profiles.")


class Aggregator:
    def __init__(
        self,
        activities: pd.DataFrame,
        dataset: str,
        user_config: dict,
        dev_config: dict,
        weighted: bool,
    ):
        """
        Class to perform aggregation of state and flow profiles either on daily or weekly scope.

        Args:
            activities (pd.DataFrame): A dataframe containing all trip and parking activities
            dataset (str): Name of initial mobility data set used for resulting file name annotation
            user_config (dict): A dictionary specifying user-specific options
            dev_config (dict): A dictionary specifying options that are only needed if own development is going on.
            weighted (bool): Shall the aggregation take into account weights from the initial mobility data sets?
        """
        self.dataset = dataset
        self.activities = activities
        self.weighted = weighted
        self.user_config = user_config
        self.dev_config = dev_config
        self.alpha = self.user_config["profileaggregators"]["alpha"]
        self.aggregation_scope = user_config["profileaggregators"][
            "aggregation_timespan"
        ]
        self.weekday_profiles = None

    def _extract_weights(self):
        """
        Get weights from the initial mobility data set stored in the column trip_weight and store it in self.weights.
        """
        self.weights = (
            self.activities.loc[:, ["unique_id", "trip_weight"]]
            .drop_duplicates(subset=["unique_id"])
            .reset_index(drop=True)
            .set_index("unique_id")
        )

    def __basic_aggregation(self):
        """
        Decider function differentiating between daily and weekly scope for the aggregation.
        """
        if self.aggregation_scope == "daily":
            self._aggregate_daily()
        elif self.aggregation_scope == "weekly":
            self._aggregate_weekly()
            self.__compose_week_profile()
        else:
            NotImplementedError(
                "The aggregation timespan can either be daily or weekly."
            )

    def _aggregate_daily(self):
        """
        Function to aggregate all profiles across all days, independently of the day of the week for both, state and
        flow profiles. The result is stored under self.profile_agg.

        Raises:
            NotImplementedError: Raised if this function is called for a state profile and the profile is neither of
            max_battery_level and min_battery_level
        """
        self.daily_profile = pd.DataFrame(
            columns=self.profile.columns, index=range(1, 2)
        )
        cols = ["unique_id", "trip_weight"]
        self.activities_subset = (
            self.activities[cols]
            .copy()
            .drop_duplicates(subset=["unique_id"])
            .reset_index(drop=True)
        )
        self.activities_weekday = pd.merge(
            self.profile, self.activities_subset, on="unique_id", how="inner"
        )
        self.activities_weekday = self.activities_weekday.set_index("unique_id")
        if self.method == "flow":
            if self.weighted:
                # weekday_subset = weekday_subset.drop("trip_start_weekday", axis=1)
                # aggregate activities_weekday to one profile by multiplying by weights
                weight_sum = sum(self.activities_weekday.trip_weight)
                daily_subset_weight = self.activities_weekday.apply(
                    lambda x: x * self.activities_weekday.trip_weight.values
                )
                daily_subset_weight = daily_subset_weight.drop("trip_weight", axis=1)
                daily_subset_weight_agg = daily_subset_weight.sum() / weight_sum
                self.weekday_profiles = daily_subset_weight_agg
            else:
                daily_subset = self.activities_weekday.drop(
                    columns=["trip_weight"], axis=1
                ).reset_index(drop=True)
                self.weekday_profiles = daily_subset.mean(axis=0)
        elif self.method == "state":
            daily_subset = self.activities_weekday.drop(
                columns=["trip_weight"]
            ).reset_index(drop=True)
            daily_subset = daily_subset.convert_dtypes()
            if self.profile_name == "max_battery_level":
                self.weekday_profiles = daily_subset.quantile(1 - (self.alpha / 100))
            elif self.profile_name == "min_battery_level":
                self.weekday_profiles = daily_subset.quantile(self.alpha / 100)
            else:
                raise NotImplementedError(
                    f"An unknown profile {self.profile_name} was selected."
                )

    def _aggregate_weekly(self, by_column: str = "trip_start_weekday"):
        """
        Function to aggregate all profiles depending on the day of the week to be able to create a weekly profile from
        individual daily aggregates. Two differentiations are made. Firstly, the function differentiates between flow
        and state profiles (stored in self.method), secondly if weights should be applied to the daily aggregations
        stored in self.weighted.

        Args:
            by_column (str, optional): Column to be used to perform the aggregation. Defaults to "trip_start_weekday".
        """

        self.weekday_profiles = pd.DataFrame(
            columns=self.profile.columns, index=range(1, 8)
        )
        cols = ["unique_id", "trip_weight"] + [by_column]
        self.activities_subset = (
            self.activities[cols]
            .copy()
            .drop_duplicates(subset=["unique_id"])
            .reset_index(drop=True)
        )
        self.activities_weekday = pd.merge(
            self.profile, self.activities_subset, on="unique_id", how="inner"
        )
        # self.profile.drop('unique_id', axis=1, inplace=True)
        self.activities_weekday = self.activities_weekday.set_index("unique_id")
        # Compose weekly profile from 7 separate profiles
        if self.method == "flow":
            if self.weighted:
                self.__calculate_weighted_mean_flow_profiles(
                    by_column="trip_start_weekday"
                )
            else:
                self.__calculate_average_flow_profiles(by_column="trip_start_weekday")
        elif self.method == "state":
            self.__aggregate_state_profiles(
                by_column="trip_start_weekday", alpha=self.alpha
            )

    def __calculate_average_flow_profiles(self, by_column: str):
        """
        Iterates through all unique elements given in by_column and aggregates flow profiles for the set of unique_ids
        that are associated with each element of the currently iterated instance. The resulting profile is stored in
        self.pofile_agg.

        Args:
            by_column (str): The column to split the profile unique_ids by, defaulting to trip_start_weekday
        """
        for idate in self.activities_weekday[by_column].unique():
            weekday_subset = self.activities_weekday[
                self.activities_weekday[by_column] == idate
            ].reset_index(drop=True)
            weekday_subset = weekday_subset.drop(
                columns=["trip_start_weekday", "trip_weight"], axis=1
            )
            weekday_subset_agg = weekday_subset.sum(axis=0)
            self.weekday_profiles.iloc[idate - 1] = weekday_subset_agg

    def __calculate_weighted_mean_flow_profiles(self, by_column: str):
        """
        The same as self.__calculate_average_flow_profiles(), but applying weighted means using weights from the initial
        mobility data set.

        Args:
            by_column (str): The column to split the profile unique_ids by, defaulting to trip_start_weekday
        """
        for idate in self.activities_weekday[by_column].unique():
            weekday_subset = self.activities_weekday[
                self.activities_weekday[by_column] == idate
            ].reset_index(drop=True)
            weekday_subset = weekday_subset.drop("trip_start_weekday", axis=1)
            # aggregate activities_weekday to one profile by multiplying by weights

            # DEPRECATED
            # weight_sum = sum(weekday_subset.trip_weight)

            weekday_subset_weight = weekday_subset.apply(
                lambda x: x * weekday_subset.trip_weight.values
            )
            weekday_subset_weight = weekday_subset_weight.drop("trip_weight", axis=1)
            weekday_subset_weight_agg = (
                weekday_subset_weight.sum()
            )  # / weight_sum DEPRECATED
            self.weekday_profiles.iloc[idate - 1] = weekday_subset_weight_agg

    def __aggregate_state_profiles(self, by_column: str, alpha: int = 10):
        """
        Selects the alpha (100 - alpha) percentile from maximum battery level (minimum batttery level) profile for each
        hour. If alpha = 10, the 10%-biggest (10%-smallest) value is selected, all values beyond are disregarded as
        outliers.

        Args:
            by_column (str): The column to split the profile unique_ids by, defaulting to trip_start_weekday
            alpha (int, optional): Percentage, giving the amount of profiles whose mobility demand can not be fulfilled
                after selection. Defaults to 10.

        Raises:
            NotImplementedError: This error is raised if self.profile_name is not one of max_battery_level and
            min_battery_level
        """
        for idate in self.activities_weekday[by_column].unique():
            levels = self.activities_weekday.copy()
            weekday_subset = levels[levels[by_column] == idate].reset_index(drop=True)
            weekday_subset = weekday_subset.drop(
                columns=["trip_start_weekday", "trip_weight"]
            )
            weekday_subset = weekday_subset.convert_dtypes()
            # TODO: not sure is correct
            if self.profile_name.startswith("max_battery_level"):
                self.weekday_profiles.iloc[idate - 1] = weekday_subset.quantile(
                    alpha / 100
                )
            elif self.profile_name.startswith("min_battery_level"):
                self.weekday_profiles.iloc[idate - 1] = weekday_subset.quantile(
                    1 - (alpha / 100)
                )
            else:
                raise NotImplementedError(
                    f"An unknown profile {self.profile_name} was selected."
                )

    def __compose_week_profile(self):
        """
        Input is self.weekday_profiles. Method only works if aggregation is weekly. Check if any day of the week is not
        filled, copy line above in that case
        """
        if self.weekday_profiles.isna().any(axis=1).any():
            index_empty_rows = (
                self.weekday_profiles[self.weekday_profiles.isna().any(axis=1)].index
                - 1
            )
            for empty_row in index_empty_rows:
                if empty_row == 5 or empty_row == 7:
                    self.weekday_profiles.iloc[empty_row] = self.weekday_profiles.iloc[
                        empty_row - 1
                    ]
                else:
                    self.weekday_profiles.iloc[empty_row] = self.weekday_profiles.iloc[
                        empty_row + 1
                    ]

        self.weekday_profiles.index.name = "weekday"
        self.weekday_profiles = self.weekday_profiles.stack().unstack(0)
        if self.weekday_profiles.empty:
            raise ValueError(
                r"The 'weekday_profiles' DataFrame seems to be empty for one or more seasons. "
                r"Please add more columns to debug mode."
            )
        self.weekday_profiles = pd.concat(
            [
                self.weekday_profiles[1],
                self.weekday_profiles[2],
                self.weekday_profiles[3],
                self.weekday_profiles[4],
                self.weekday_profiles[5],
                self.weekday_profiles[6],
                self.weekday_profiles[7],
            ],
            ignore_index=True,
        )
        self.weekday_profiles = pd.DataFrame(
            self.weekday_profiles, columns=[self.profile_name]
        )
        logging.info(f"Finished generating a weekly profile with {self.profile_name}.")

    def __write_output(self):
        """
        Write out the profile given in profile adding the self.profile_name and the string "output_profileaggregator"
        (overarching file label) to the written filename.
        """
        if self.user_config["global"]["write_output_to_disk"]["aggregator_output"]:
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["aggregator_output"]
            self.dev_config["global"]["additional_label"] = (
                "_" + self.profile_name + "_"
            )
            file_name = create_file_name(
                dev_config=self.dev_config,
                user_config=self.user_config,
                file_name_id="output_profileaggregator",
                dataset=self.dataset,
            )
            write_out(data=self.weekday_profiles, path=root / folder / file_name)

    def perform_aggregation(
        self, profile: pd.DataFrame, profile_name: str, method: str
    ) -> pd.DataFrame:
        """
        Inner wrapper function (of sub-class) that extracts weights, performs the aggregation and writes the output to
        disk. Internal class attributes are reset to None after write-out.

        Args:
            profile (pd.DataFrame): Profiles to be aggregated
            profile_name (str): Descriptor used for filename annotation
            method (str): Can be one of "state" or "flow"

        Returns:
            pd.DataFrame: Returns the aggregated profile
        """
        self.profile = profile
        self.profile_name = profile_name
        self.method = method
        logging.info(
            f"Starting to aggregate {self.profile_name} to fleet level based on day of the week."
        )
        start_time_agg = time.time()
        if self.weighted:
            self._extract_weights()
        self.__basic_aggregation()
        if self.user_config["global"]["write_output_to_disk"]["aggregator_output"]:
            self.__write_output()
        logging.info(f"Aggregation finished for {self.profile_name}.")
        elapsed_time_agg = time.time() - start_time_agg
        logging.info(
            f"Needed time to aggregate {self.profile_name}: {elapsed_time_agg} seconds."
        )
        self.profile = None
        self.profile_name = None
        self.method = None
        return self.weekday_profiles
