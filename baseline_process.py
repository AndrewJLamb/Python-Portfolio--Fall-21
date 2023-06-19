#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 17:18:26 2023

@author: andrew7
"""

# Standard libraries;
import itertools
import warnings
from pathlib import Path
from os import getcwd, cpu_count
from collections import defaultdict
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from sklearn.metrics import (
    mean_absolute_percentage_error,
    mean_squared_error
)


# Statistical software libraries;
from statsmodels.tsa.stattools import adfuller, kpss
from statsforecast import StatsForecast
from statsforecast.models import (
    HistoricAverage,
    Naive,
    RandomWalkWithDrift,
    AutoARIMA,
    AutoETS,
    AutoCES,
    AutoTheta
)

# Filter warnings;
warnings.filterwarnings("ignore")

# Log file formatting;
LOG_FMT = """
        %(levelname)s: %(funcName)s: %(name)s: %(asctime)s:
        %(message)s (Line: %(lineno)s [%(filename)s])
        """
YMD_FMT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "model_process.log"

# logging protocol configuration;
# logging.basicConfig(
# format=log_fmt,
# filename=log_file,
# datefmt=ymd_fmt,
# level=# logging.INFO)


class QuickProcess():
    """
     -----------------------------------------
    ===========================================

     Quick Process (nixtla StatsForecast):

    Models:

    * Main:
        -HistoricAverage()
        -Naive()
        -RandomWalkWithDrift()
    * Additional:
        -SeasonalNaive()

    ===========================================
     -----------------------------------------
    """

    def __init__(self, directory: str, y_name="Streams", window=45, full=False):
        """
         -----------------------------------------
        ===========================================

         Initializes SimpleProcess class instance;

          params:
          * directory: (str), Directory to iterate over ;
          * y_name: (str), Variable to generate forecasts of;
          * window: (int), Length of forecasting horizon;

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Directory;
        self.directory = directory

        # Forecasting window;
        self.window = window

        # Endog. Variable of Interest:
        self.y_name = y_name

        print(directory)

        # Full date range;
        if not full:
            self.full = False
        else:
            self.full = True

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        # logging;
        # logging.info("Directory: %s ;", directory)
        # logging.info("Forecasting window: %s Days", window)
        # logging.info("Predict: Daily %s", y_name)
        # logging.info("Runtime: %s ;", runtime)

    def locate_file(self, directory: str):
        """
         -----------------------------------------
        ===========================================

         Iterates over 'directory' to locate modeling dataset;

          params:
          * directory: (str), Directory to iterate over ;
          * y_name: (str), Variable to generate forecasts of;

        ===========================================
         -----------------------------------------
        """

        # pathlib.Path(), iter directory;
        paths = Path(directory).iterdir()

        # Start timing;
        # start = time.perf_counter()

        for path in paths:
            # Looking for files, ending with '.csv';
            if path.is_file() and path.suffix == ".csv":
                check_model = str(path.name).startswith("EST_")
                # Modeling files all start with 'EST'
                if check_model:
                    # logging.info("Modeling dataset found: %s ;", p.name)
                    filename = str(path.name)

                    # File location object; Modeling Data;
                    file_location = "/".join([directory, filename])
                    # logging.info("File location: %s ;", self.file_location)
                else:
                    # logging.info("No modeling dataset found ; ", p.name)
                    print("Dataset not found; Consult documentation")
                    return None

        return file_location

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        # # logging;
        # logging.info("Runtime: %s s", runtime)

    def read_file(self, file_location: str, y_name="Streams"):
        """
         -----------------------------------------
        ===========================================

         Processes modeling dataset;

          params:
          * file_location: (str), Directort location of modeling dataset;;
          * y_name: (str), Variable to generate forecasts of;

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Read in file from location in Multivariate.path_iterate();
        read_file = pd.read_csv(
            str(file_location), sep=",", parse_dates=[0], index_col=[0]
        )

        # Instantiating file object;
        file = read_file.filter(like=y_name)

        # File headers;
        header = list(file.columns)

        # File index;
        index = file.index

        # Data type == 'float64' Ex. 1.0, 2.0 ...;
        dtypes_dict = {s: "float64" for s in header}

        # Setting data type;
        for key, value in dtypes_dict.items():
            file[key] = file[key].astype(value)

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        return (file, index)

        # logging;
        # logging.info("Runtime: %s s", runtime)

    def generate_y_data(self, file) -> dict:
        """
         -----------------------------------------
        ===========================================

        Isolates initial modeling series data by 'Source':
         ie., Apple Music, SoundCloud, Spotify;

        params:
         * file: (DataFrane) DataFrame containing historical daily level of
          streams data, isolated by Digital Streaming Platform;

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Sources of streams;
        sources = list(file.columns)

        # Isolated data series for each source of streams;
        y_dict = {source: file[source] for source in sources}

        y_data = defaultdict(pd.Series, y_dict)

        # For each source of streams;
        for source in sources:
            assert np.isfinite(y_data[source]).all()

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        # logging;
        # logging.info("Runtime: %s s", runtime)

        return y_data

    def stationarity(self, data) -> dict:
        """name, series
         -----------------------------------------
        ===========================================

         Returns DataFrame containing test statistics and
          p-values for Augmented Dickey-Fuller, Kwiatkowski–
          Phillips–Schmidt–Shin tests for stationarity;

          params:
          * data: (dict) Dictionary of isolated series of
          historical daily level of streams data;
          * data should == self.variables

          returns:
          * self.[t]rain_[t]est_[s]plits

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Alpha levels for significance;
        alpha_p = 0.05
        alpha_t = 1.96

        # Augmented Dickey_Fuller(ADF) Test Statistic and P-Value;
        a_t, a_p = adfuller(data)[:2]

        # Kwiatkowski-Philips-Schmidt-Shin(KPSS) Test Statistic and P-Value;
        k_t, k_p = kpss(data)[:2]

        # T-Value, P-Value checks;
        t_check = (a_t >= abs(alpha_t)) | (k_t >= abs(alpha_t))
        p_check = (a_p >= alpha_p) | (k_p >= alpha_p)

        # Stationarity criteria;
        stationarity_check = t_check | p_check

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        # logging;
        # logging.info("Runtime: %s s", runtime)

        return {
            "Stationarity likely:": stationarity_check,
            "Augmented Dickey-Fuller": {
                "t_stat": round(a_t, 5),
                "p_value": round(a_p, 5)},
            "Kwiatkowksi-Phillips-Schmidt-Shin": {
                "t_stat": round(k_t, 5),
                "p_value": round(k_p, 5)}
        }

    def set_baseline_approaches(
            self,
            models=None,
            scalers=None,
            alphas=None,
            seasonality_period=None):
        """
         -----------------------------------------
        ===========================================

         Sets iteration lists of model iteration regression
         parameters;

          params:

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Model parameters;
        if models is None:
            models = {"HistoricAverage", "Naive", "RWD",
                      "AutoARIMA", "AutoETS", "CES", "AutoTheta"}

        if scalers is None:
            scalers = {"minmax", "power", "standard", "robust"}

        if seasonality_period is None:
            seasonality_period = 7
        else:
            pass

        # Model iterations;
        param_groups = {
            scaler: {
                "".join([model, "_iter_", str(i)]):
                dict(zip([str("model"), str("season_length")],
                         [model, seasonality_period]))
                    for i, model in enumerate(models)
            } for scaler in scalers
        }

        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start-finish), 3)

        # logging;
        # logging.info("Runtime: %s ;", runtime)

        return (models, param_groups)

    def apply_splits(self,
                     data,
                     freq="d") -> tuple:
        """
         -----------------------------------------
        ===========================================

         Performs train-test splitting;

          params:
          * window: (int), Length of forecasting horizon;
          * data: (dict), Dictionary of isolated modeling data series;
          * freq: (int), Data frequency;

          returns:
          * Dictionary of train/test split indices/data;

        ===========================================
         -----------------------------------------
        """

        # Start timing;
        # start = time.perf_counter()

        # Performing Train/Test splits on series indices and values;
        data_iv = {
            "train": {
                "index": data[:-self.window].index,
                "values": data[:-self.window].values.reshape(-1, 1)},
            "test": {
                "index": data[-self.window:].index,
                "values": data[-self.window:].values.reshape(-1, 1)}
        }
        # Finish timing;
        # finish = time.perf_counter()

        # Runtime;
        # runtime = round(abs(start - finish), 3)

        # logging;
        # logging.info("Runtime: %s ;", runtime)

        return data_iv
