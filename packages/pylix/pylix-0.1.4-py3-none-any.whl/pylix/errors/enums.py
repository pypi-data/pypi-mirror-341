import numpy as np

from enum import Enum

class TypesTuple(Enum):
    INT: tuple = (int, np.integer)
    FLOAT: tuple = (float, np.floating)
    NUMBER: tuple = (*INT, *FLOAT)
    LIST: tuple = (list,)
    TUPLE: tuple = (tuple,)
    ND_ARRAY: tuple = (np.ndarray,)
    LISTS: tuple = (*LIST, *ND_ARRAY)

class BaseCodes(Enum):
    NONE: int = 0
    TODO: int = 1

class ArgumentCodes(Enum):
    NONE: int = 0
    ZERO: int = 1
    LIST_LAYER_NOT_NUMBER: int = 2
    OUT_OF_RANGE: int = 3
    NOT_NUMBER: int = 4
    NOT_INT: int = 5
    NOT_LISTS: int = 6
    NOT_POSITIV: int = 7
    LIST_LAYER_NOT_NUMBER_LISTS: int = 8
    NOT_MATRIX_NP_ARRAY: int = 9
    NOT_EQUAL: int = 10
    MISMATCH_DIMENSION: int = 11
    NOT_TUPLE_LIST_ND_ARRAY: int = 12
    NOT_FLOAT: int = 13
    UNEXPECTED_TYPE: int = 14
    NOT_AXIS: int = 15
    NOT_VECTOR3D: int = 16
    NOT_VECTOR: int = 17
    NOT_MATRIX: int = 18
    NOT_LISTS_TUPLE: int = 19
    NOT_BOOl: int = 20
    NOT_POLYNOMIAL: int = 21
    NOT_INT_BOOl: int = 22
    TOO_BIG: int = 23
    TOO_SMALL: int = 24
    NOT_ITERABLE: int = 25

class MathCodes(Enum):
    NONE: int = 0
    UNFIT_DIMENSIONS: int = 1
    NOT_MATRIX: int = 2
    NOT_MATRIX_NUMBER: int = 3
    NOT_NUMBER: int = 4
    NOT_FALSE: int = 5
    NOT_POSITIV: int = 6
    NOT_INT: int = 7
    NOT_VECTOR: int = 8
    NOT_DEFINED: int = 9
    ZERO: int = 10
    NOT_VECTOR_NUMBER: int = 11
    VECTOR: int = 12
