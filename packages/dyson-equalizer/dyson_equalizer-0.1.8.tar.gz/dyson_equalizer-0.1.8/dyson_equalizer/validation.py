""" The ``dyson_equalizer.validation`` module provides functions to check matrixes used as input
"""


import numpy as np


def validate_matrix(
        Y
) -> np.ndarray:
    """Compute the scaling factors for the Dyson equalizer

    Parameters
    ----------
    Y: (m, n) array_like
        The svd of the data matrix, computed e.g. using ``numpy.linalg.svd(Y, full_matrices=False)``

    Returns
    -------
    Y: (m, n) numpy.ndarray
        The input matrix as numpy array

    Raises
    ------
    ValueError
        If the input is not a matrix or if the matrix contains a row or a column with only zeros.

    """
    Y = np.asarray(Y)
    if Y.ndim != 2:
        raise ValueError(f"The input is not a matrix. Shape: {Y.shape}")
    if (~Y.any(axis=0)).any():
        raise ValueError(f"The input contains a zero column")
    if (~Y.any(axis=1)).any():
        raise ValueError(f"The input contains a zero row")
    return Y


def validate_svd(
        svd
) -> tuple[int, int]:
    """Compute the scaling factors for the Dyson equalizer

    Parameters
    ----------
    svd:
        The svd of the data matrix, computed e.g. using ``numpy.linalg.svd(Y, full_matrices=False)``

    Returns
    -------
    m: int
        The number of rows
    n: int
        The number of columns

    See Also
    --------
    numpy.linalg.svd

    Raises
    ------
    ValueError
        If the input is not a valid svd or if the dimensions of the svd are not compatible

    """
    U, S, Vh = svd
    if S.shape[0] != U.shape[1] or Vh.shape[0] != S.shape[0]:
        raise ValueError("Incompatible dimensions in the SVD decomposition. "
                         "The input should be a svd decomposition generated using "
                         "e.g. `np.linalg.svd(Y, full_matrices=False)`")
    m, n = U.shape[0], Vh.shape[1]
    return m, n
