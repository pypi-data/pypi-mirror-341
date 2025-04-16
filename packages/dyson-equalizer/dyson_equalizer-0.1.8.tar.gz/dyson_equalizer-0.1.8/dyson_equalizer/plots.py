""" The ``dyson_equalizer.plots`` module provides functions to create useful plots
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import ks_1samp

from dyson_equalizer.algorithm import marchenko_pastur, marchenko_pastur_cdf


def plot_mp_eigenvalues(
        eigs: np.ndarray, gamma: float,
        eigenvalues_to_show: int = 100,
        log_y: bool = True,
        matrix_label: str = 'X',
        ax: plt.Axes | None = None,
) -> None:
    """Plots the eigenvalues of the covariance matrix and compares to the Marchenko-Pastur threshold

    This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
    whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

    Parameters
    ----------
    eigs: (n) numpy.array
        The array of eigenvalues (e.g. of a covariance matrix) to plot
    gamma: float
        The ratio between the dimensions of the matrix (between 0 and 1)
    eigenvalues_to_show: int, optional
        The number of eigenvalues to show in the plot (defaults to 100)
    log_y: bool, optional
        Whether the y-axis should be logarithmic (defaults to True)
    matrix_label: str, optional
        The name of the matrix that will be used as label (defaults to ``X``)
    ax: plt.Axes, optional
        A matplotlib Axes object. If none is provided, a new figure is created.

    See Also
    --------

    dyson_equalizer.algorithm.marchenko_pastur

    Examples
    --------

    We generate a random matrix X of size (100, 1000) and show that the eigenvalues of
    the covariance matrix Y = ¹⁄ₙXXᵀ follow a Marchenko-Pastur distribution.


    .. plot::
        :context: close-figs
        :caption: Eigenvalues plot of a random matrix

        import numpy as np
        from dyson_equalizer.plots import plot_mp_eigenvalues

        m, n = 100, 1000
        X = np.random.normal(size=(m, n))
        Y = X @ X.T / n
        eigs = sorted(np.linalg.eigvals(Y), reverse=True)

        plot_mp_eigenvalues(eigs, gamma=m/n)
    """
    if ax is None:
        _, ax = plt.subplots()

    beta_p = (1 + gamma ** 0.5) ** 2
    nx = min(eigenvalues_to_show, len(eigs))
    ax.bar(x=range(nx), height=eigs[:nx], label=f'Eigenvalues of {matrix_label}')
    ax.axhline(y=beta_p, linestyle='--', color='green', label='MP upper edge β₊')
    if log_y:
        ax.set_yscale('log')
    ax.legend()


from matplotlib import pyplot as plt
import numpy as np
from typing import Sequence


def plot_mp_density(
        eigs: np.ndarray,
        gamma: float,
        show_only_significant: int = None,
        show_only_significant_right_margin: float = 0.3,
        matrix_label: str = 'X',
        bins: int | str | Sequence = 'sqrt',
        ax: plt.Axes | None = None,
) -> None:
    """Plots the density of eigenvalues of the covariance matrix and compares to the Marchenko-Pastur distribution

    This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
    whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

    Parameters
    ----------
    eigs: (n) numpy.array
        The array of eigenvalues (e.g. of a covariance matrix) to plot
    gamma: float
        The ratio between the dimensions of the matrix (between 0 and 1)
    show_only_significant: int, optional
        Set this value to show only a small number of significant eigenvalues (defaults to None)
        This option is useful is some of the signal eigenvalues are much bigger than the noise.
        Set to zero to show only significant eigenvalues within the margin indicated by
        `show_only_significant_right_margin`
    show_only_significant_right_margin: float, optional
        Specifies the size of the right margin (defaults to 0.3) from the largest eigenvalue
        selected by the show_only_significant option
    matrix_label: str, optional
        The name of the matrix that will be used as label (defaults to ``X``)
    bins: int or sequence or str, default: 'sqrt'
        The bins parameter used to build the histogram.
    ax: plt.Axes, optional
        A matplotlib Axes object. If none is provided, a new figure is created.

    See Also
    --------

    dyson_equalizer.algorithm.marchenko_pastur
    matplotlib.pyplot.Axes.hist

    Examples
    --------

    We generate a random matrix X of size (100, 1000) and show that the eigenvalues of
    the covariance matrix Y = ¹⁄ₙXXᵀ follow a Marchenko-Pastur distribution.


    .. plot::
        :context: close-figs
        :caption: Eigenvalues plot of a random matrix

        import numpy as np
        from dyson_equalizer.plots import plot_mp_density

        m, n = 100, 1000
        X = np.random.normal(size=(m, n))
        Y = X @ X.T / n
        eigs = sorted(np.linalg.eigvals(Y), reverse=True)

        plot_mp_density(eigs, gamma=m/n)

    """
    if show_only_significant_right_margin is not None:
        if show_only_significant_right_margin < 0 or show_only_significant_right_margin > 1:
            raise ValueError('show_only_significant_right_margin should be between 0 and 1')

    if ax is None:
        _, ax = plt.subplots()

    ksr = ks_1samp(eigs, cdf=marchenko_pastur_cdf, args=[gamma])

    eigs = np.asarray(eigs)
    beta_p = (1 + gamma ** 0.5) ** 2
    rank = np.sum(eigs > beta_p)

    eig_max_idx = max(0, rank - show_only_significant) if show_only_significant is not None else 0
    xmax = None
    if eig_max_idx > 0 and (xclip := eigs[eig_max_idx] * (1+ show_only_significant_right_margin)) < eigs[0] * 1.05:
        xmax = xclip

    ax.hist(eigs, bins=bins, density=True, range=(0, xmax) if xmax else None, label=f'Eigenvalues of {matrix_label}')
    x = np.linspace(start=0, stop=xmax or eigs[0], num=1000)
    mp = marchenko_pastur(x, gamma)
    ax.plot(x, mp, color='red', label='MP density')

    ax.set_xlim(0, xmax)
    ax.axvline(beta_p, linestyle='--', color='green', label='MP upper edge β₊')

    ax.text(0.60, 0.89, f'Rank = {rank}\nKS p-val = {ksr.pvalue:.5f}', transform=ax.transAxes)

    ax.legend(bbox_to_anchor=(0.98, 0.87), loc='upper right', borderaxespad=0.)
