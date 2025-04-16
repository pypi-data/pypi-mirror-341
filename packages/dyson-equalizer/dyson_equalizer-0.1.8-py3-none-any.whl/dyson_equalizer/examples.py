import numpy as np


def generate_X(
        m: int = 1000,
        n: int = 2000,
        seed: int = 123
) -> np.ndarray:
    """ Generates a signal matrix with 10 strong principal values and 10 weak principal values.

    Parameters
    ----------
    m: int, optional
        The number of rows (default=1000)
    n: int, optional
        The number of rows (default=2000)
    seed: int, optional
        The random seed (default=123)

    Returns
    -------
    numpy.ndarray
        The data matrix

    """
    np.random.seed(seed)
    assert m <= n

    # Make a random matrix
    Xr = np.random.normal(loc=0, scale=1, size=(m, n))
    Xr_svd = np.linalg.svd(Xr, full_matrices=False)

    # Set pv
    s_20 = [np.sqrt(1000 * n)] * 10 + [np.sqrt(3 * n)] * 10

    # Y of rank 20
    X_20 = Xr_svd.U[:, :20] @ np.diag(s_20) @ Xr_svd.Vh[:20, :]

    return X_20


def generate_Y_with_almost_homoskedastic_noise(
        m: int = 1000,
        n: int = 2000,

        seed: int = 123,
) -> np.ndarray:
    """ Generates a test matrix with 10 strong principal values and 10 weak principal values.

    The noise is homoskedastic except for the last 5 rows and columns where it is abnormally strong

    Parameters
    ----------
    m: int, optional
        The number of rows (default=1000)
    n: int, optional
        The number of rows (default=2000)
    seed: int, optional
        The random seed (default=123)

    Returns
    -------
    numpy.ndarray
        The data matrix

    See Also
    --------
    generate_X

    """
    np.random.seed(seed)

    X = generate_X(m=m, n=n)

    x = np.ones(m)
    y = np.ones(n)
    x[-5:] = 10
    y[-5:] = 100
    S = x[:, None] * y
    E = np.random.normal(scale=np.sqrt(S))

    return X + E


def generate_Y_with_heteroskedastic_noise(
        m: int = 1000,
        n: int = 2000,
        noise_dimensions: int = 10,
        seed: int = 123,
) -> np.ndarray:
    """ Generates a test matrix with 10 strong principal values and 10 weak principal values.

    Parameters
    ----------
    m: int, optional
        The number of rows (default=1000)
    n: int, optional
        The number of rows (default=2000)
    noise_dimensions: int, optional
        The number of noise dimensions (default=10)
    seed: int, optional
        The random seed (default=123)

    Returns
    -------
    numpy.ndarray
        The data matrix

    See Also
    --------
    generate_X

    """
    np.random.seed(seed)

    X = generate_X(m=m, n=n)

    A = np.exp(np.random.normal(0, np.sqrt(2), size=(m, noise_dimensions)))
    B = np.exp(np.random.normal(0, np.sqrt(2), size=(noise_dimensions, n)))
    S = A @ B
    S /= S.mean()
    E = np.random.normal(scale=np.sqrt(S))

    return X + E
