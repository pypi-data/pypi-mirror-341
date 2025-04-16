"""
Class designed to facilitate computing the Jacobian
using numerical differentiation
"""

__author__ = ["Karl Naumann-Woleske"]
__credits__ = ["Karl Naumann-Woleske"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = ["Karl Naumann-Woleske"]

# Default libraries
import copy
import inspect
import logging
import multiprocessing as mp
import os
import pickle
from pathlib import Path

# Third-party libraries
import numpy as np
import pandas as pd

from macrostat.core.model import Model
from macrostat.diff.jacobian import Jacobian
from macrostat.sample.sampler import Sampler

logger = logging.getLogger(__name__)


class JacobianNumeric(Jacobian, Sampler):
    def __init__(
        self,
        model: Model,
        output_folder: Path = Path.cwd() / "jacobian_numeric",
        skipparams: list = None,
        paramlist: list = None,
        log_step: bool = False,
        epsilon: float = 1e-6,
        method: str = "central",
        cpu_count: int = 1,
        batchsize: int = None,
    ):
        """Generalized class to compute the Jacobian for a Model using numeric
        differentiation. It inherits from the Sampler class to facilitate easy
        parallel processing in the central, forward or backward differences.

        Parameters
        ----------
        model : Model
            The model to compute the Jacobian for
        output_folder : Path, optional
            Folder to save outputs, by default Path.cwd() / "jacobian_numeric"
        skipparams : list, optional
            List of parameters to skip, by default None
        paramlist : list, optional
            List of parameters to include, by default None
        log_step : bool, optional
            Whether to take steps in log-space, by default False
        epsilon : float, optional
            Step size for finite differences, by default 1e-6
        method : str, optional
            Finite difference method: 'forward', 'backward', or 'central', by default 'central'
        cpu_count : int, optional
            Number of CPUs to use for parallel processing, by default 1
        batchsize : int, optional
            Batch size for parallel processing, by default None
        """
        # Initialize both parent classes
        Jacobian.__init__(
            self,
            model=model,
            output_folder=output_folder,
            skipparams=skipparams,
            paramlist=paramlist,
            log_step=log_step,
        )
        Sampler.__init__(
            self,
            model=model,
            output_folder=output_folder,
            cpu_count=cpu_count,
            batchsize=batchsize,
        )

        self.epsilon = epsilon
        self.method = method

    def generate_tasks(self):
        """
        Generate tasks for computing the Jacobian using numeric differentiation.

        This method creates a list of tasks, where each task is a tuple containing
        a string identifier and a model instance. The tasks include:

        1. A base model with unperturbed parameters.
        2. For each parameter to be differentiated:
           - If using central difference method: two models with the parameter perturbed forward and backward.
           - If using forward or backward difference method: one model with the parameter perturbed in the appropriate direction.

        The perturbation size is determined by the `_compute_step` method, which
        takes into account whether log-space stepping is being used.

        Returns
        -------
        list of tuple
            A list of tasks, where each task is a tuple (str, Model).
            The string is an identifier for the task, and the Model is an
            instance of the model with specific parameter values.

        Notes
        -----
        - The base model is always the first task in the list.
        - The method of perturbation (central, forward, or backward) is
          determined by the `self.method` attribute.
        - The step size for perturbation is influenced by `self.epsilon` and
          `self.log_step` attributes.
        - Only parameters listed in `self.parameters_to_diff` are perturbed.
        """
        tasks = []

        # Generate the baseline model
        base_model = self.modelclass(
            **self.model_kwargs, parameters=self.base_parameters
        )
        tasks.append(("base", base_model))

        for param in self.parameters_to_diff:
            if self.method == "central":
                forward_params = self.base_parameters.copy()
                backward_params = self.base_parameters.copy()

                if np.isscalar(forward_params[param]):
                    h = self._compute_step(forward_params[param])
                    forward_params[param] = self._apply_step(
                        forward_params[param], h, 1
                    )
                    backward_params[param] = self._apply_step(
                        backward_params[param], h, -1
                    )
                else:
                    h = self._compute_step(forward_params[param])
                    forward_params[param] = self._apply_step(
                        forward_params[param], h, 1
                    )
                    backward_params[param] = self._apply_step(
                        backward_params[param], h, -1
                    )

                forward_model = self.modelclass(
                    **self.model_kwargs, parameters=forward_params
                )
                backward_model = self.modelclass(
                    **self.model_kwargs, parameters=backward_params
                )

                tasks.append((f"{param}_forward", forward_model))
                tasks.append((f"{param}_backward", backward_model))
            else:  # forward or backward
                perturbed_params = self.base_parameters.copy()

                if np.isscalar(perturbed_params[param]):
                    h = self._compute_step(perturbed_params[param])
                    perturbed_params[param] = self._apply_step(
                        perturbed_params[param],
                        h,
                        1 if self.method == "forward" else -1,
                    )
                else:
                    h = self._compute_step(perturbed_params[param])
                    perturbed_params[param] = self._apply_step(
                        perturbed_params[param],
                        h,
                        1 if self.method == "forward" else -1,
                    )

                perturbed_model = self.modelclass(
                    **self.model_kwargs, parameters=perturbed_params
                )
                tasks.append((f"{param}_perturbed", perturbed_model))

        return tasks

    def _compute_step(self, param_value):
        if self.log_step:
            return self.epsilon * np.maximum(np.abs(np.log(param_value)), 1.0)
        else:
            return self.epsilon * np.maximum(np.abs(param_value), 1.0)

    def _apply_step(self, param_value, step, direction):
        if self.log_step:
            return np.exp(np.log(param_value) + direction * step)
        else:
            return param_value + direction * step

    def compute_jacobian(self):
        """Compute the Jacobian using numeric differentiation"""
        self.sample()
        outputs = self.extract()

        base_output = outputs.loc["base"]
        jacobian = {}

        for param in self.parameters_to_diff:
            if self.method == "central":
                forward_output = outputs.loc[f"{param}_forward"]
                backward_output = outputs.loc[f"{param}_backward"]

                h = self._compute_step(self.base_parameters[param])
                if np.isscalar(self.base_parameters[param]):
                    diff = (forward_output - backward_output) / (2 * h)
                else:
                    diff = (forward_output - backward_output) / (2 * h[:, np.newaxis])
            else:  # forward or backward
                perturbed_output = outputs.loc[f"{param}_perturbed"]

                h = self._compute_step(self.base_parameters[param])
                if np.isscalar(self.base_parameters[param]):
                    if self.method == "forward":
                        diff = (perturbed_output - base_output) / h
                    else:  # backward
                        diff = (base_output - perturbed_output) / h
                else:
                    if self.method == "forward":
                        diff = (perturbed_output - base_output) / h[:, np.newaxis]
                    else:  # backward
                        diff = (base_output - perturbed_output) / h[:, np.newaxis]

            # Apply log transformation if log_step is True
            if self.log_step:
                if np.isscalar(self.base_parameters[param]):
                    diff *= self.base_parameters[param]
                else:
                    diff *= self.base_parameters[param][:, np.newaxis]

            jacobian[param] = diff

        self.jacobian = pd.DataFrame(jacobian)
        return self.jacobian

    def save(self, folder=None):
        """Save the JacobianNumeric object as a PKL for later use"""
        folder = folder if folder is not None else f"{self.output_folder}"
        filename = f"{folder}/jac_numeric.pkl"
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename):
        """Class method to load an instance of JacobianNumeric"""
        with open(filename, "rb") as f:
            new = pickle.load(f)
        return new

    def transform_variables(self, transformer: callable = lambda x: x):
        """Apply a transformation to the Jacobian

        Parameters
        ----------
        transformer : callable, optional
            Function to transform the Jacobian, by default lambda x: x

        Returns
        -------
        pd.DataFrame
            Transformed Jacobian
        """
        return transformer(self.jacobian)
