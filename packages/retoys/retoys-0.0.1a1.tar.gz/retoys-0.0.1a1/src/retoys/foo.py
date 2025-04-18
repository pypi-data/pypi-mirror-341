import time
from typing import Any

import numpy as np
from rich import pretty
from tqdm import tqdm


class ExampleTools:
    def __init__(self, num_samples: int) -> None:
        """A dummy class that makes use of the imported packages.

        Args:
            num_samples: number of total iterations for progress bar.
        """
        self.num_samples = num_samples

    def pbar(self) -> None:
        """Shows a progress bar"""
        for _ in tqdm(range(self.num_samples), desc="Dummy Task"):
            time.sleep(0.5)

    def pprint(self, obj: Any, **kwargs) -> None:
        """uses ``rich`` package to pretty print the input.

        Args:
            obj: object to print.
            **kwargs: passed to ``rich.pretty.pprint()``
        """
        pretty.pprint(obj, **kwargs)

    def matmul(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Multiplies the two given numpy arrays.

        Args:
            a: first array.
            b: second array.

        Returns:
            Result of matmul operation.
        """
        return np.matmul(a, b)
