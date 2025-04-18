.. venco.py getting started documentation file, created on February 27, 2025
    Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/deed.en

.. _adaptability:

Adaptability for New Databases
===================================

Integrating new databases into venco.py is essential for expanding its
capabilities to handle diverse data sources, such as mobility data, transport
research model outputs, and national travel surveys (NTS). The software is
designed to be flexible, allowing seamless integration of datasets from various
domains, provided that specific criteria are met. The integration process
requires careful attention to dataset structure and adherence to the software's
expectations for data formatting. This section provides step-by-step
instructions on how to integrate new databases and configure the software to
process them effectively.

Instructions to integrate new databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Ensure the minimum requirements for the databases are met**: The new dataset
   must contain the following variables for successful integration:

   - Unique ID: A unique identifier for each individual, vehicle, or household.
   - Trip ID: A distinct identifier for each trip.
   - Timestamps: Start and end times for each trip, plus either date or weekday.
   - Trip purpose: The underlying reason for each journey (e.g., home, work,
     leisure).
   - Distance: The total distance traveled (in kilometers) during the trip. 


2. **Write a new parsing class for the new dataset**: To adapt the software to
   the new dataset, you must create a new parsing class. This class should implement a `process()` method, similar to the one used in the MiD (German NTS)
   case (see: `ParseMiD <https://gitlab.com/dlr-ve/esy/vencopy/vencopy/-/blob/main/vencopy/core/dataparsers/parseMiD.py?ref_type=heads>`_).
   The class should inherit from the existing `DataParser` and `IntermediateParsing` classes, which will allow for reusability of existing methods.
   This minimizes the need for redundant code and ensures consistency across different datasets. The parsing class is usually called ParseDataset where Dataset is
   the abbreviation for the dataset name.

3. **Add the new dataset variables to the `dev_config.yaml` file**: The new
   dataset variables should be incorporated into the `dev_config.yaml` file to facilitate the correct parsing of data. By defining these variables, the parsing class will 
   know how to map the data appropriately. Once the dataset is formatted correctly (i.e., following the structure of the `DataParser` class, with data stored in 
   `data.data["activities"]`), the rest of the workflow should function seamlessly.

4. **Update the `user_config.yaml` for follow up classes**: Minor adjustments 
   will be required in the `user_config.yaml` file for subsequent classes. These changes 
   typically involve adding the missing keys, which will raise `KeyError` 
   exceptions if not defined. The `user_config.yaml` is designed to make it easy 
   for users to retrieve and update necessary configurations when these errors occur.

5. **Ensure the minimum database structure is correct**: After applying the necessary parsing logic,
   ensure that the dataset follows the minimum database structure outlined below:

   - unique_id: Unique identifier for each vehicle (or person or household).
   - park_id: Counter for the park activities of the same unique_id.
   - trip_id: Counter for each trip of the same unique_id.
   - trip_distance: Distance covered during the trip (in kilometers).
   - travel_time: Time spent traveling during the trip.
   - trip_start_weekday: Weekday of the trip start.
   - trip_start_hour: Hour the trip began.
   - purpose_string: Purpose of the trip (e.g., leisure, work) needed to model
     the charging infrastructure availability.
   - trip_start_day: Day the trip started.
   - timestamp_start: Start timestamp of the trip.
   - timestamp_end: End timestamp of the trip.
   - is_first_activity: Boolean indicating if it's the first activity in the
     sequence.
   - is_last_activity: Boolean indicating if it's the last activity in the
     sequence.
   - activity_id: Identifier for the activity within the trip.
   - next_activity_id: Identifier for the next activity (if applicable).
   - previous_activity_id: Identifier for the previous activity (if applicable).
   - is_first_park_activity: Boolean indicating if it is the first park
     activity.
   - time_delta: Time difference of the trip or park activity.

To process the new data in the follow up classes, you want to ensure that the
dataset adheres to the following guidelines:

1. Counters of trip_id and park_id: 

 - trip_id starts with 1 (real number from original dataset): Ensure that the
   trip_id in the dataset begins at 1, and it should correspond to the real
   numbers from the original dataset. Example: If trip_id in the original
   dataset starts from 100, you can map it to start from 1 in your new
   dataset. Ensure that all trip_id remain unique and sequential after this
   transformation.
 - park_id starts with 0 (creation in the code): The park_id should be
   initialized to 0 in the code. You can generate it dynamically. Ensure that
   the park_id is assigned to all parking activities and increments
   sequentially for each new parking event.

2. Trips and park activities should be alternating and not consecutive: Ensure
   that the sequence of activities alternates between trips and parks. There
   should be no consecutive trip or park activities for the same vehicle or
   unique_id. For instance, you could have: park_id=0, trip_id=1, park_id=1,
   trip_id=2, etc. If two trips or two parks are consecutive, you should merge
   the consecutive entries into a single event.

3. Merging consecutive trips or park activities: If two consecutive trips or
   park activities are detected, merge them into a single event. For instance,
   if two consecutive trip_id entries happen one after another, merge them into
   a single entry (or vice versa for park activities). Ensure that merging
   preserves the correct time intervals and vehicle information.

4. The unique_id should be unique for each vehicle and day of the week: The
   unique_id should be constructed in such a way that each vehicle gets a unique
   identifier per day of the week. Example: unique_id = vehicle_id +
   day_of_week. This guarantees that each vehicle on a specific day has a unique
   identifier. Ensure that the new unique_id does not overlap with other
   vehicles on the same day or across different days.

5. Ordered consecutive timestamps: For each trip or park event, the
   timestamp_start should be the same as the timestamp_end of the previous
   event. This ensures continuity in the events for each vehicle, with no time
   gaps between the end of one event and the start of the next.

6. First and last timestamp of the day should be 00:00:00 for each unique_id:
   The timestamp_start for the first event of each unique_id should be set to
   00:00:00 (midnight) to indicate the start of the day. Similarly, the
   timestamp_end for the last event of each unique_id should also be set to
   00:00:00 of the next day to mark the end of the day.


Below is a sample of how the dataset should be formatted and structured once parsed:

.. list-table:: Example dataset structure after the DataParser class
   :widths: 10, 15, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 10, 10, 10, 10, 10
   :header-rows: 1

   * - unique_id
     - park_id
     - trip_id
     - trip_distance
     - travel_time
     - trip_start_weekday
     - trip_start_hour
     - purpose_string
     - trip_start_day
     - timestamp_start
     - timestamp_end
     - is_first_activity
     - is_last_activity
     - activity_id
     - next_activity_id
     - previous_activity_id
     - is_first_park_activity
     - time_delta
   * - 10001952
     - 0.0
     - 
     - 
     - 
     - 2
     - 11.0
     - HOME
     - 18.0
     - 2017-04-18 00:00:00
     - 2017-04-18 11:10:00
     - True
     - False
     - 0.0
     - 1.0
     - 
     - True
     - 0 days 11:10:00
   * - 10001952
     - 
     - 1.0
     - 9.5
     - 25.0
     - 2
     - 11.0
     - LEISURE
     - 18.0
     - 2017-04-18 11:10:00
     - 2017-04-18 11:35:00
     - False
     - False
     - 1.0
     - 1.0
     - 0.0
     - False
     - 0 days 00:25:00
   * - 10001952
     - 1.0
     - 
     - 
     - 
     - 2
     - 11.0
     - LEISURE
     - 18.0
     - 2017-04-18 11:35:00
     - 2017-04-18 18:00:00
     - False
     - False
     - 1.0
     - 2.0
     - 1.0
     - False
     - 0 days 06:25:00
   * - 10001952
     - 
     - 2.0
     - 9.5
     - 25.0
     - 2
     - 18.0
     - HOME
     - 18.0
     - 2017-04-18 18:00:00
     - 2017-04-18 18:45:00
     - False
     - False
     - 2.0
     - 2.0
     - 1.0
     - False
     - 0 days 00:45:00
   * - 10001952
     - 2.0
     - 
     - 
     - 
     - 2
     - 18.0
     - HOME
     - 18.0
     - 2017-04-18 18:45:00
     - 2017-04-19 00:00:00
     - False
     - True
     - 2.0
     - 
     - 2.0
     - False
     - 0 days 05:15:00



Once the dataset is structured correctly and the configuration files are
updated, the software will be able to process the new data with minimal
adjustments in the following classes.


