# TODO understand how to use for labels processing
from kornia.augmentation import AugmentationSequential
import albumentations
from regex import E
import torch
from kornia import augmentation as kornia_aug
from torch import nn
from abc import ABC, abstractmethod
import pytest  # For unit tests
from dataclasses import dataclass
# , cupy # cupy for general GPU acceleration use (without torch) to test
import numpy as np
from enum import Enum

# TODO 
class AugsBaseClass(nn.Module, ABC):
    """Base class for specification of dataset aumentations.

    Args:
        nn (_type_): _description_
    """

    def __init__(self):
        super(AugsBaseClass, self).__init__()

    @abstractmethod
    def forward(self, imageAsDN: torch.Tensor) -> torch.Tensor:
        pass

    # PLACEHOLDER method
    def process_labels(self, labels: torch.Tensor | tuple[torch.Tensor]) -> torch.Tensor | tuple[torch.Tensor]:
        pass


# %% Base error models classes
# Currently supported: torch only
# Reference: Gow, 2007, "A Comprehensive tools for modeling CMOS image sensor-noise performance", IEEE Transactions on Electron Devices, Vol. 54, No. 6

class EnumComputeBackend(Enum):
    NUMPY = 1
    TORCH = 2
    CUPY = 3


class EnumModelFidelity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class BaseErrorModel(nn.Module, ABC):
    """Base abstract class for error models

    Args:
        nn (_type_): _description_
        ABC (_type_): _description_
    """

    def __init__(self, inputShape: list, device: str = 'cpu', enumModelFidelity: EnumModelFidelity = EnumModelFidelity.LOW) -> None:
        super(BaseErrorModel, self).__init__()
        # Default fidelity level for all models
        self.enumModelFidelity = enumModelFidelity
        self.inputShape = inputShape  # Must be [B, C, H, W] for images
        self.device = device

        # Internal state
        self.errorRealization = None

        # Assert input shape validity
        assert len(
            self.inputShape) >= 2, "Input shape must be a list of at least 2 dimensions specifying the shape of the input tensor"

    @abstractmethod
    def forward(self, imageAsDN: torch.Tensor) -> torch.Tensor:
        """
        Abstract method to apply error model to input tensor.
        Args:
            imageAsDN (torch.Tensor): Input tensor to which the error model will be applied.

        Returns:
            torch.Tensor: Tensor with error model applied.
        """
        raise NotImplementedError(
            "This is an abstract method and must be implemented by the derived class")

    @abstractmethod
    def realizeError(self, X: torch.Tensor) -> None:
        """
        Abstract method to compute error realization for the specific error model.
        """
        raise NotImplementedError(
            "This is an abstract method and must be implemented by the derived class")


class BaseGainErrorModel(BaseErrorModel):
    """Base for gain error models

    Args:
        BaseErrorModel (_type_): _description_
    """

    def __init__(self, inputShape) -> None:
        super(BaseGainErrorModel, self).__init__(inputShape)

    def forward(self, X: torch.Tensor) -> torch.Tensor:

        # Sample error realization
        self.realizeError()
        assert self.errorRealization is not None, "Error realization must not be None!"

        # Apply gain error to input tensor
        if self.enumComputeBackend == EnumComputeBackend.TORCH:
            # Matrix multiplication along batch dimension
            return torch.bmm(self.errorRealization, X)

        elif self.enumComputeBackend == EnumComputeBackend.NUMPY:
            raise NotImplementedError("Compute operation not implemented")
        else:
            raise NotImplementedError("Compute operation not implemented")


class BaseAddErrorModel(BaseErrorModel):
    """Base for additive error models

    Args:
        BaseErrorModel (_type_): _description_
    """

    def __init__(self, inputShape) -> None:
        super(BaseAddErrorModel, self).__init__(inputShape)

    def forward(self, imageAsDN: torch.Tensor) -> torch.Tensor:
        # Sample error realization
        self.realizeError()
        assert self.errorRealization is not None, "Error realization must not be None!"

        # Apply additive error to input tensor
        return imageAsDN + self.errorRealization








