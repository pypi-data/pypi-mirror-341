# stpp_tplot

Simple time series plotting library based on pyspedas and matplotlib.

## Overview

`stpp_tplot` is a Python library that provides convenient functions for plotting time series data, especially for space physics data processed by `pyspedas`. It simplifies the creation of publication-quality plots with features like:

* Multiple panel plots with shared x-axis
* Spectrogram plots with colorbar
* Orbit parameter labels panel
* Customizable plot options

## Installation

```bash
pip install stpp_tplot==0.1.5
```
## Usage
```python
from stpp_tplot import mp, sd, op
from pyspedas.erg import pwe_ofa, mgf, orb

# Load data
trange = ['2017-03-27', '2017-03-28']
pwe_ofa(trange=trange)
mgf(trange=trange)
orb(trange=trange)

# Plot data
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label='erg_orb_l2_pos_rmlatmlt')