# -*- coding: utf-8 -*-
"""Model definition for experiments."""

from typing import Union, Type, Dict, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


import keras
import numpy
import pandas
import sklearn


@dataclass
class Metrics:
    """Metrics definition.

    Args:
        train (dict): Dictionary with the training metrics, e.g., {'mse': [0.3, 1.1, ...], 'rmse': [...]}
        test (dict): Dictionary with the test metrics, e.g., {'mse': [1, 1.3, ...], 'rmse': [1, ...]}
    """

    train: Dict[str, Union[List[float], numpy.ndarray]]
    test: Dict[str, Union[List[float], numpy.ndarray]]


class Model(ABC):
    """Abstract class for models.

    Attributes:
        model (sklearn.base, keras.Model): model object
        metrics (Metrics): metrics per iteration during training
    """

    name: str = ""

    def __init__(self, model: Union[Type[sklearn.base], Type[keras.Model]]):
        """Initialize the model.

        Args:
            model (sklearn.base, keras.Model): model object or class to use for training
        """
        self.model = model
        self.metrics = Metrics(train=dict(), test=dict())
        self.param_range: list | numpy.ndarray = []
        self.eval_metrics = []
        self.param = ""

    @abstractmethod
    def fit(
        self,
        x: numpy.ndarray | pandas.DataFrame | pandas.Series,
        y: numpy.ndarray | pandas.DataFrame | pandas.Series,
        param_range: list | numpy.ndarray,
        param: str,
        eval_metrics: str | list[str],
        test_size: float = 0.3,
    ) -> None:
        """Train the model.

        Args:
            x (numpy.ndarray | pandas.DataFrame | pandas.Series): input features
            y (numpy.ndarray | pandas.DataFrame | pandas.Series): target variable
            param_range (list | numpy.ndarray): parameter range to experiment with the same model
            eval_metrics (str | list[str]): metrics to calculate the performance of the model
            param (str): parameter to vary in the range `param_range`
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.
        """
