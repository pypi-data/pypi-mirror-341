# Dyson Equalizer #

This package is a Python implementation of the Dyson Equalizer. 
The method is described in detail in the article [The Dyson Equalizer: Adaptive Noise Stabilization for Low-Rank Signal Detection and Recovery
](https://doi.org/10.48550/arXiv.2306.11263)

The documentation is available at [https://klugerlab.github.io/DysonEqualizer](https://klugerlab.github.io/DysonEqualizer).

## Installation ##
The main version of the package can be installed as 
```
pip install dyson-equalizer
```

The development version of the package can be installed as 
```
pip install git+https://github.com/Klugerlab/DysonEqualizer.git
```

## Getting started ##

To import the package and apply the Dyson Equalizer to a test matrix

```python
from dyson_equalizer.examples import generate_Y_with_heteroskedastic_noise
from dyson_equalizer.dyson_equalizer import DysonEqualizer

Y = generate_Y_with_heteroskedastic_noise()
de = DysonEqualizer(Y).compute()

```

The `DysonEqualizer` result class will contain the following attributes
- `Y`: The original data matrix
- `x_hat`: The normalizing factors for the rows
- `y_hat`: The normalizing factors for the columns
- `Y_hat`: The normalized data matrix so that the variance of the error is 1
- `X_bar`: The estimated signal matrix. It has rank `r_hat`
- `r_hat`:  The estimated rank of the signal matrix
- `S`: The principal values of the data matrix `Y`
- `S_hat`:  The principal values of the data matrix `Y_hat`

Detailed examples are available on the [Examples](https://klugerlab.github.io/DysonEqualizer/examples.html) 
page.
