# FastGB

## Description

This package provides a fast waveform generator for galactic binaries,
as seen by the LISA instrument. Galactic binaries are described by the
following 8 parameters: frequency (f0), frequency evolution (fdot),
amplitude (ampl), sky location (beta, lambda), polarisation (psi),
inclination (incl) and initial phas (phi0).

The main functionality of this package is to compute time delay
interferometry (TDI) observables from those parameters, with the
following options:

- TDI 1.5 or 2nd generation
- multiple sources generation at a time
- analytic or interpolated orbits from file
- numpy arrays or jax arrays for auto differentiation

It is based on 10.1103/physrevd.76.083006 and follows LISA Data
Challenge ([LDC](https://lisa-ldc.lal.in2p3.fr/)) conventions.

## Installation

```
pip install fastgb
```

or

```
pip install fastgb[jax]
```

## Usage

```
import numpy as np
from lisaorbits import EqualArmlengthOrbits
from fastgb import fastgb

pGB = np.array([0.00135962, # f0 Hz
                8.94581279e-19, # fdot "Hz^2
		1.07345e-22, # ampl strain
		0.312414,  # eclipticlatitude radian
               -2.75291,   # eclipticLongitude radian
	        3.5621656, # polarization radian
                0.523599,  # inclination radian
		3.0581565, # initial phase radian
      	       ])

fgb = fastgb.FastGB(delta_t=5, T=365*24*3600, N=128, orbits=EqualArmlengthOrbits())
X, Y, Z, kmin = fgb.get_fd_tdixyz(pGB.reshape(1,-1))
```

## Contributors

Based on work from:

- Stas Babak
- Jean-Baptiste Bayle
- Téo Bouvard
- Christian Chapman-Bird
- Maude Le Jeune
