import time
import jax
import numpy as np
import jax.numpy as jnp

from lisaorbits import EqualArmlengthOrbits
from fastgb import fastgb

jax.config.update("jax_enable_x64", True)

pGB = np.array(
    [
        0.00135962,  # f0 Hz
        8.94581279e-19,  # fdot "Hz^2
        1.07345e-22,  # ampl strain
        0.312414,  # eclipticlatitude radian
        -2.75291,  # eclipticLongitude radian
        3.5621656,  # polarization radian
        0.523599,  # inclination radian
        3.0581565,  # initial phase radian
    ]
)

size = 512
fgb = fastgb.FastGB(
    delta_t=15, T=365 * 24 * 3600, N=size, orbits=EqualArmlengthOrbits()
)


def test_nojax():
    X, Y, Z, kmin = fgb.get_fd_tdixyz(pGB.reshape(1, -1))
    assert X.shape == (1, size)


def test_jax():
    X, Y, Z, kmin = fgb.get_fd_tdixyz(jnp.array(pGB).reshape(1, -1))
    assert X.shape == (1, size)
    _X, _Y, _Z, _kmin = fgb.get_fd_tdixyz(np.array(pGB).reshape(1, -1))
    np.testing.assert_allclose(X, _X, rtol=1e-10)
    np.testing.assert_allclose(Y, _Y, rtol=1e-10)
    np.testing.assert_allclose(Z, _Z, rtol=1e-10)
    assert kmin == _kmin


single = lambda: fgb.get_fd_tdixyz(pGB.reshape(1, -1))
single_jax = lambda: fgb.get_fd_tdixyz(jnp.array(pGB.reshape(1, -1)))
single_jit = lambda: jitted(
    pGB.reshape(1, -1)
)  # jax.jit(fgb.get_fd_tdixyz)(jnp.array(pGB.reshape(1, -1)))


@jax.jit
def jitted(p):
    return fgb.get_fd_tdixyz(jnp.array(p))


single_jax()
single_jit()

# vectorized

vpGB = np.tile(pGB, 50).reshape(50, -1)
vpGB_v = jnp.array(vpGB).reshape(50, 1, 8)

vectorized = lambda: fgb.get_fd_tdixyz(vpGB)
vectorized_jax = lambda: jax.vmap(fgb.get_fd_tdixyz, in_axes=0)(vpGB_v)
vectorized_jit = lambda: jax.vmap(jitted, in_axes=0)(vpGB_v)

vectorized_jax()
vectorized_jit()

__benchmarks__ = [
    (single, single_jax, f"single source: with jax"),
    (single, single_jit, f"single source: with jit"),
    (vectorized, vectorized_jax, f"multi source: using jax.vmap"),
    (vectorized, vectorized_jit, f"multi source: using jit and vmap"),
]
