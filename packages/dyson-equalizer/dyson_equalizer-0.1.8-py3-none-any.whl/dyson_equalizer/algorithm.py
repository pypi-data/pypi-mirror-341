"""
    The ``dyson_equalizer.algorithm`` module provides functions implementing the algorithms needed
    to compute the Dyson Equalizer and related auxiliary functions.

    The functions may be used to build specialized implementation of the Dyson Equalizer.

"""
import numpy as np

from dyson_equalizer.validation import validate_svd


def compute_scaling_factors(
        svd,
        normalize_factors: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the scaling factors for the Dyson equalizer

    Parameters
    ----------
    svd:
        The svd of the data matrix, computed e.g. using ``numpy.linalg.svd(Y, full_matrices=False)``
    normalize_factors : bool, optional
        if ``True``, normalize the factors so that the mean of x and y are close to 1. This option is
        useful when iteration

    Returns
    -------
    x_hat: (m) numpy.array
        Normalizing factors for the rows
    y_hat: (n) numpy.array
        Normalizing factors for the columns

    See Also
    --------
    numpy.linalg.svd

    Notes
    -----
    This function computes the normalizing factors for the Dyson equalizer.
    Details, derivation and convergence analysis are provided in [1]_, in particular Algorithm 1.

    First, it computes the solutions to the Dyson equation as

    .. math:: \\hat{g}_{i}^{(1)} = \\sum_{k=1}^{m} \\frac{\\eta^2}{\\sigma^2_k + \\eta^2} U^2_{ik}

    .. math:: \\hat{g}_{j}^{(2)} = \\frac{1}{\\eta} \\sum_{k=1}^{m} \\left( \\frac{\\eta^2}{\\sigma^2_k + \\eta^2} \
              - \\frac{1}{\\eta} \\right) V^2_{jk}

    Then, assuming :math:`m \\le n`, the normalizing factors are computed as:

    .. math:: \\hat{x}_i = \\frac{1}{\\sqrt{m - \\eta \\Vert \\hat{g}_{i}^{(1)} \\Vert_{1}}} \\left( \\frac{1}{\\hat{g}_{i}^{(1)}} - \\eta \\right)

    .. math:: \\hat{y}_i = \\frac{1}{\\sqrt{n - \\eta \\Vert \\hat{g}_{i}^{(2)} \\Vert_{1}}} \\left( \\frac{1}{\\hat{g}_{i}^{(2)}} - \\eta \\right)

    where:
      * :math:`m` is the number of rows
      * :math:`m` is the number of columns
      * :math:`\\eta` is the median principal value
      * :math:`\\sigma_k` is the :math:`k`-th principal value
      * :math:`\\hat{g}_{i}^{(1)}` is the solution to the Dyson equation for the smallest dimension
      * :math:`\\hat{g}_{j}^{(2)}` is the solution to the Dyson equation for the largest dimension

    References
    ----------

    .. [1] Landa B., Kluger Y., "The Dyson Equalizer: Adaptive Noise Stabilization for Low-Rank Signal
       Detection and Recovery," arXiv, https://arxiv.org/abs/2306.11263

    """
    m, n = validate_svd(svd)
    U, S, Vh = svd

    # Transpose if the matrix has more rows than columns
    if m > n:
        y_hat, x_hat = compute_scaling_factors((Vh.T, S, U.T))
        return x_hat, y_hat

    eta = np.median(S)

    ees = eta / (eta ** 2 + S ** 2)
    g1 = (U ** 2 * ees).sum(axis=1)
    g2 = 1 / eta + (Vh.T ** 2 * (ees - 1 / eta)).sum(axis=1)

    x_hat = 1 / np.sqrt(m - eta * np.linalg.norm(g1, 1)) * (1 / g1 - eta)
    y_hat = 1 / np.sqrt(n - eta * np.linalg.norm(g2, 1)) * (1 / g2 - eta)

    if normalize_factors:
        kx = x_hat.mean()
        ky = y_hat.mean()
        kr = np.sqrt(kx / ky)
        x_hat /= kr
        y_hat *= kr

    return x_hat, y_hat


def compute_low_rank_approximation_mp(
        svd
) -> tuple[np.ndarray, int]:
    """Computes the low rank approximation by keeping all eigeinvalues above the maximum
    of the Marchenko-Pastur distribution.
    Details, derivation and convergence analysis are provided in [1]_, in particular Algorithms 2 and 3.

    Parameters
    ----------
    svd:
       The svd of the data matrix, computed e.g. using ``numpy.linalg.svd(Y, full_matrices=False)``

    Returns
    -------
    Y_tr: (m, n) numpy.array
        The low-rank approximation of the data matrix truncated to `r_hat`
    r_hat: int
        The rank of the truncated matrix

    See Also
    --------
    marchenko_pastur
    numpy.linalg.svd

    Notes
    -----
    The threshold for significance is based on the Marchenko-Pastur distribution
    and is estimated as :math:`\\sqrt{m} + \\sqrt{m}`,  where :math:`m \\le n` are the matrix's dimensions.

    References
    ----------

    .. [1] Landa B., Kluger Y., "The Dyson Equalizer: Adaptive Noise Stabilization for Low-Rank Signal
       Detection and Recovery," arXiv, https://arxiv.org/abs/2306.11263

    """
    m, n = validate_svd(svd)
    U, S, Vh = svd

    yhat_sv_threshold = np.sum(np.sqrt([n, m]))
    r_hat = S[S > yhat_sv_threshold].size
    Y_tr = U[:, :r_hat] * S[:r_hat] @ Vh[:r_hat, :]
    return Y_tr, r_hat


def scale_matrix(
        Y: np.ndarray,
        x: np.ndarray,
        y: np.ndarray
) -> np.ndarray:
    """Scales a matrix by the given normalization factors for rows and columns

    .. math:: \\hat{Y} = D\\{x\\} Y D\\{y\\}

    Parameters
    ----------
    Y: (m, n) numpy.ndarray
        a matrix
    x: (m) numpy.ndarray
        the row weights
    x: (n) numpy.ndarray
        the column weights

    Returns
    -------
    Y_hat: (m, n) numpy.ndarray
        The normalized matrix

    """
    m, n = Y.shape[-2:]
    if x.shape != (m, ):
        raise ValueError(f"The row weights vector have the wrong shape {x.shape}, expected {(m,)}")
    if y.shape != (n, ):
        raise ValueError(f"The columns weights vector have the wrong shape {y.shape}, expected {(n,)}")

    return x[:, None] * Y * y


def marchenko_pastur(
        x: np.ndarray,
        gamma: float,
        sigma: float = 1
) -> np.ndarray:
    """Computes the density of the Marchenko-Pastur distribution for the given values

    Parameters
    ----------
    x: (n) numpy.array or float
        a vector or a value for the xs to be computed
    gamma: float
        the ratio between the number of rows and the number of columns (between 0 and 1)
    sigma: float, optional
        the variance of the entries of the random matrix (defaults to 1)

    Returns
    -------
    y: (n) numpy.ndarray
        The values of the Marchenko-Pastur distribution

    Notes
    -----
    The density of the Marchenko-Pastur distribution can be defined as


    .. math:: dF_{\\gamma, \\sigma}(x) = \\frac{\\sqrt{(\\beta_+ - x)(x - \\beta_-)}}{2 \\pi \\sigma^2 \\gamma x} \\mathbb{1}(\\beta_- \\le x \\le \\beta_+)

    where:
      * :math:`m` is the number of rows
      * :math:`n` is the number of columns
      * :math:`\\gamma` is the ratio :math:`\\frac{m}{n}` (assuming :math:`m \\le n`)
      * :math:`\\beta_\\pm = \\sigma^2(1\\pm\\sqrt{\\gamma})^2`

    """
    if gamma < 0 or gamma > 1:
        raise ValueError(f"The gamma must be between 0 and 1, got {gamma}")

    x = np.asarray(x)
    s2 = sigma ** 2

    beta_m, beta_p = np.array([(1 - gamma ** 0.5) ** 2, (1 + gamma ** 0.5) ** 2]) * sigma**2

    r = np.zeros_like(x)
    i = (x > beta_m) & (x < beta_p)
    xi = x[i]
    r[i] = 1 / (2 * np.pi * s2) * np.sqrt((beta_p - xi) * (xi - beta_m)) / (gamma * xi)
    return r


def marchenko_pastur_cdf(
        x,
        gamma: float,
        sigma: float = 1,
):
    """Computes the cumulative density function of the Marchenko-Pastur distribution for the given values

    Parameters
    ----------
    x: (n) numpy.array or float
        a vector or a value for the xs to be computed
    gamma: float
        the ratio between the number of rows and the number of columns (between 0 and 1)
    sigma: float, optional
        the variance of the entries of the random matrix (defaults to 1)

    Returns
    -------
    y: (n) numpy.ndarray
        The values of the cdf of the Marchenko-Pastur distribution

    """
    if gamma < 0 or gamma > 1:
        raise ValueError(f"The gamma must be between 0 and 1, got {gamma}")

    a, b = np.array([(1 - gamma ** 0.5) ** 2, (1 + gamma ** 0.5) ** 2]) * sigma ** 2

    r = np.zeros_like(x)
    r[x >= b] = 1
    i = (x > a) & (x < b)
    xi = x[i]

    r[i] = (np.sqrt((xi - a) * (b - xi)) + (a + b) / 2 * np.arcsin((2 * xi - a - b) / (b - a)) -
            (np.sqrt(a * b)) * np.arcsin(((a + b) * xi - 2 * a * b) / (xi * (b - a)))) / (
                       2 * np.pi * gamma * sigma ** 2) + .5

    return r
