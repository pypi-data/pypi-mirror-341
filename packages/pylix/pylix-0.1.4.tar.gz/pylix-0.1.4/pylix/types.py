from typing import Union
import numpy as np

Int: type = Union[int, np.integer]
Float: type = Union[float, np.floating]
Number: type = Union[int, np.integer, float, np.floating]
List: type = Union[list]
Tuple: type = Union[tuple]
NdArray: type = Union[np.ndarray]
Lists: type = Union[list, np.ndarray]
AllLists: type = Union[list, tuple, np.ndarray]
