"""Base Generator"""

from abc import ABC, abstractmethod

import torch
from pydantic import BaseModel, ConfigDict

from fed_rag.base.tokenizer import BaseTokenizer


class BaseGenerator(BaseModel, ABC):
    """Base Generator Class."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def generate(self, query: str, context: str, **kwargs: dict) -> str:
        """Generate an output from a given query and context."""

    @property
    @abstractmethod
    def model(self) -> torch.nn.Module:
        """Model associated with this generator."""

    @property
    @abstractmethod
    def tokenizer(self) -> BaseTokenizer:
        """Tokenizer associated with this generator."""
