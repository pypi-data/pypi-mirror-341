__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"


import logging
import time
import warnings
from pathlib import Path

from vencopy.core.dataparsers import parse_data
from vencopy.core.diarybuilders import DiaryBuilder
from vencopy.core.flexestimators import FlexEstimator
from vencopy.core.gridmodellers import GridModeller
from vencopy.core.postprocessors import PostProcessor
from vencopy.core.profileaggregators import ProfileAggregator
from vencopy.utils.utils import (
    create_output_folders,
    load_configs,
    load_scenarios,
    overwrite_configs,
)

warnings.simplefilter(action="ignore", category=FutureWarning)
logging.basicConfig(
    level=logging.INFO,
    filename="vencopy.log",
    filemode="w",
    format="{%(filename)s: %(lineno)d} %(message)s",
)

if __name__ == "__main__":

    start_time = time.time()

    base_path = Path(__file__).parent / "vencopy"
    configs = load_configs(base_path=base_path)
    run_multiple_scenario = configs["user_config"]["global"]["multiple_scenarios"][
        "run_multiple_scenarios"
    ]

    if run_multiple_scenario:
        scenarios = load_scenarios(base_path=base_path, configs=configs)
    else:
        scenarios = ["NA"]

    for scenario in range(len(scenarios)):
        if isinstance(scenarios, list):
            logging.info("Running one scenario only.")
        else:
            logging.info(f"Running scenario {scenario} of {len(scenarios)}.")

        start_time_scenario = time.time()
        if run_multiple_scenario:
            configs = overwrite_configs(
                scenario=scenarios.iloc[[scenario]], configs=configs
            )
        create_output_folders(configs=configs)

        data = parse_data(configs=configs)
        data.process()

        grid = GridModeller(configs=configs, data=data.data)
        grid.assign_grid()

        flex = FlexEstimator(configs=configs, data=grid.data)
        flex.estimate_technical_flexibility()

        diary = DiaryBuilder(configs=configs, data=flex.data)
        diary.create_diaries()

        profiles = ProfileAggregator(configs=configs, data=diary.data, profiles=diary)
        profiles.aggregate_profiles()

        post = PostProcessor(configs=configs, profiles=profiles, data=diary.data)
        post.scale_profiles()

        elapsed_time_scenario = time.time() - start_time_scenario
        logging.info(f"Elapsed time: {elapsed_time_scenario / 60} minutes.")

    elapsed_time = time.time() - start_time
    logging.info(f"Elapsed time: {elapsed_time / 60} minutes.")
