"""
    The ``dyson_equalizer`` package provides a class functions implementing the algorithms needed
    to compute the Dyson Equalizer [1]_ and related auxiliary functions.

    The functions may be used to build specialized implementation of the Dyson Equalizer.

    Examples
    --------

    See :ref:`examples`

    References
    ----------

    .. [1] Landa B., Kluger Y., "The Dyson Equalizer: Adaptive Noise Stabilization for Low-Rank Signal
       Detection and Recovery," arXiv, https://arxiv.org/abs/2306.11263

"""

# Get the version from _version.py (added when building using scm)
try:
    from .version import __version__ # noqa
except ModuleNotFoundError as e:
    __version__ = '0.0.0-dev'
