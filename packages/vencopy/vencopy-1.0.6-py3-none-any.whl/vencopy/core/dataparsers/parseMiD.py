__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import logging

import pandas as pd

from ...core.dataparsers.dataparsers import IntermediateParsing
from ...core.dataparsers.parkinference import ParkInference


class ParseMiD(IntermediateParsing):
    def __init__(self, configs: dict, dataset: str):
        """
        Inherited data class to differentiate between abstract interfaces such
        as vencopy internal variable namings and data set specific functions
        such as filters. Specific class for the German MiD B2 dataset.

        Args:
            configs (dict): A dictionary containing a user_config dictionary and a dev_config dictionary.
            dataset (str): Abbreviation of the National Travel Survey to be parsed.
        """
        super().__init__(configs=configs, dataset=dataset)
        self.park_inference = ParkInference(configs=configs)

    def _harmonise_variables(self):
        """
        Harmonizes the input data variables to match internal venco.py names
        given as specified in the mapping in parseConfig['data_variables']. So
        far mappings for MiD08 and MiD17 are given. Since the MiD08 does not
        provide a combined household and person unique identifier, it is
        synthesized of the both IDs.
        """
        replacement_dict = self._create_replacement_dict(
            self.dataset, self.dev_config["dataparsers"]["data_variables"]
        )
        activities_renamed = self.trips.rename(columns=replacement_dict)
        if self.dataset == "MiD08":
            activities_renamed["household_person_id"] = (
                activities_renamed["household_id"].astype("string")
                + activities_renamed["person_id"].astype("string")
            ).astype("int")
        self.trips = activities_renamed
        logging.info("Finished harmonisation of variables.")

    def __add_string_columns(self, weekday=True, purpose=True):
        """
        Adds string columns for either weekday or purpose.

        Args:
            weekday (bool, optional): Boolean identifier if weekday should be
            added in a separate column as string. Defaults to True. purpose
            (bool, optional): Boolean identifier if purpose should be added in a
            separate column as string. Defaults to True.
        """
        if weekday:
            self._add_string_column_from_variable(
                col_name="weekday_string", var_name="trip_start_weekday"
            )
        if purpose:
            self._add_string_column_from_variable(
                col_name="purpose_string", var_name="trip_purpose"
            )

    @staticmethod
    def _compose_start_and_end_timestamps(trips):
        trips["trip_start_day"] = (
            pd.to_datetime(trips["trip_start_year"], format="%Y")
            + pd.to_timedelta((trips["trip_start_week"] - 1) * 7, unit="days")
            + pd.to_timedelta(trips["trip_start_weekday"], unit="days")
        ).dt.day

        trips["timestamp_start"] = (
            pd.to_datetime(trips["trip_start_year"], format="%Y")
            + pd.to_timedelta((trips["trip_start_week"] - 1) * 7, unit="days")
            + pd.to_timedelta(trips["trip_start_weekday"], unit="days")
            + pd.to_timedelta(trips["trip_start_hour"], unit="hours")
            + pd.to_timedelta(trips["trip_start_minute"], unit="minutes")
        )

        trips["timestamp_end"] = (
            pd.to_datetime(trips["trip_start_year"], format="%Y")
            + pd.to_timedelta((trips["trip_start_week"] - 1) * 7, unit="days")
            + pd.to_timedelta(trips["trip_start_weekday"], unit="days")
            + pd.to_timedelta(trips["trip_end_hour"], unit="hours")
            + pd.to_timedelta(trips["trip_end_minute"], unit="minutes")
        )
        return trips

    @staticmethod
    def _cleanup_dataset(activities):
        activities.drop(
            columns=['is_driver',
                     # 'person_id',  # remove for tutorials
                     'household_person_id',
                     'trip_scale_factor',
                     'trip_end_next_day',
                     'trip_is_intermodal',
                     'trip_purpose',
                     'weekday_string',
                     'is_first_trip'], inplace=True)
        return activities

    def process(self) -> pd.DataFrame:
        """
        Wrapper function for harmonising and filtering the trips dataset as well
        as adding parking rows.
        """
        self._load_data()
        self._select_columns()
        self._harmonise_variables()
        self._harmonise_variables_unique_id_names()
        self._convert_types()
        self.__add_string_columns()
        self.trips = self._compose_start_and_end_timestamps(trips=self.trips)
        self.trips = self._update_end_timestamp_if_next_day(trips=self.trips)
        self._assign_season(self.trips)
        if self.user_config["dataparsers"]["seasons"]["filter_season_post_assignment"]:
            self.trips = self.filter_for_season(
                user_config=self.user_config, trips=self.trips
            )
        self._check_filter_dict(dictionary=self.filters)
        self._filter(filters=self.filters)
        self._extract_df_debug_mode()
        self._subset_area_type()
        self.data = self.park_inference.add_parking_rows(trips=self.trips)
        self.data["activities"] = self._cleanup_dataset(
            activities=self.data["activities"]
        )
        self.write_output(data=self.data["activities"])
        logging.info("Parsing MiD dataset completed.")
        return self.data
