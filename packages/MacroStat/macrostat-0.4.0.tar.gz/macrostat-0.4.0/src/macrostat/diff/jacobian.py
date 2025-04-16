"""
Class that forms the basis for computing the Jacobian
of a model with respect to its parameters.
"""

__author__ = ["Karl Naumann-Woleske"]
__credits__ = ["Karl Naumann-Woleske"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = ["Karl Naumann-Woleske"]

# Default libraries
import copy
import logging
from pathlib import Path
import pickle

from macrostat.core.model import Model

logger = logging.getLogger(__name__)


class Jacobian:
    def __init__(
        self,
        model: Model,
        output_folder: Path = Path.cwd() / "jacobian",
        skipparams: list = None,
        paramlist: list = None,
        log_step: bool = False,
    ):
        """Initialize a Jacobian object for computing derivatives of a model.

        This class provides a framework for computing the Jacobian matrix of a model
        with respect to its parameters. It supports selective differentiation of
        parameters and can handle both linear and logarithmic step sizes.

        Parameters
        ----------
        model : object
            The model object for which to compute the Jacobian. Must have a
            'parameters' attribute.
        output_folder : Path, optional
            Directory to save output files. Defaults to current working directory
            with a 'jacobian' subfolder.
        skipparams : list, optional
            List of parameter names to exclude from differentiation. If None,
            all parameters are included.
        paramlist : list, optional
            List of parameter names to include in differentiation. If provided,
            overrides skipparams.
        log_step : bool, optional
            If True, use logarithmic steps for differentiation. Defaults to False.

        Attributes
        ----------
        model : object
            The model object provided at initialization.
        output_folder : Path
            Directory for saving output files.
        base_parameters : dict
            Copy of the model's initial parameters.
        parameters_to_diff : list
            List of parameters to differentiate.
        jacobian : None or array-like
            Stores the computed Jacobian matrix once calculate method is called.

        Notes
        -----
        - The class creates the output folder if it doesn't exist.
        - Either skipparams or paramlist should be provided, not both.
        - The compute method must be implemented in subclasses.
        """

        self.model = model
        self.base_parameters = copy.deepcopy(model.parameters)

        # Generate the list of parameters to differentiate
        if paramlist is not None:
            self.parameters_to_diff = paramlist
        elif skipparams is not None:
            allparams = set(self.base_parameters.keys())
            self.parameters_to_diff = list(allparams.difference(skipparams))
        else:
            self.parameters_to_diff = list(self.base_parameters.keys())

        # Set the output folder
        self.output_folder = output_folder
        if not self.output_folder.is_dir():
            self.output_folder.mkdir(parents=True, exist_ok=True)

        self.jacobian = None

    def compute(self, loss_function: callable = lambda x: x, loss_kwargs: dict = None):
        raise NotImplementedError("This method should be implemented in a subclass")

    def save(self, folder=None):
        """Save the Jacobian object as a PKL for later use"""
        folder = folder if folder is not None else self.output_folder
        filename = folder / f"{self.__class__.__name__}.pkl"
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename):
        """Class method to load an instance of Jacobian"""
        with open(filename, "rb") as f:
            new = pickle.load(f)
        return new
