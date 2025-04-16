#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""FastGB

fast waveform generator for galactic binaries, as seen by the LISA
instrument. Galactic binaries are described by the following 8
parameters: frequency (f0), frequency evolution (fdot), amplitude
(ampl), sky location (beta, lambda), polarisation (psi), inclination
(incl) and initial phas (phi0).

"""
import numpy as np
import lisaconstants as constants
from lisaorbits import ResampledOrbits

try:
    import jax.numpy as jnp
except ImportError:
    jnp = np

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes

YEAR = constants.SIDEREALYEAR_J2000DAY * 24 * 60 * 60
CLIGHT = constants.SPEED_OF_LIGHT


class orbitsFromL0L1:
    """Orbits wrapper."""

    def __init__(self, orbits):
        """Load orbits."""

        if isinstance(orbits, str):
            self.orbits = ResampledOrbits(orbits)
        else:
            self.orbits = orbits

    def compute_position(self, sc, t):
        """Compute the position of sc (sc needs to be 1, 2 or 3) at time t
        return an numpy array of dim 3 x ntimes (similar to LDC Orbits)
        """
        x = self.orbits.compute_position(t, [sc])  # dimension ntimes x 1 x 3
        return np.reshape(x, (len(x[:, 0, 0]), 3)).T

    @property
    def arm_length(self):
        """Read armlength from given orbits."""
        if hasattr(self, "ltt"):
            return np.mean(self.ltt) * constants.C
        if hasattr(self.orbits, "original_attrs"):
            return self.orbits.original_attrs["L"]
        return self.orbits.L


def computeXYZ(T, Gs, f0, fdot, fstar, ampl, q, tm, jax=False):
    """Compute TDI X, Y, Z from y_sr"""
    _jnp = jnp if jax else np
    f = f0[:, None] + fdot[:, None] * tm[None, :]
    omL = f / fstar
    SomL = _jnp.sin(omL)
    fctr = _jnp.exp(-1.0j * omL)
    fctr2 = 4.0 * omL * SomL * fctr / ampl[:, None]

    # I have factored out 1 - exp(1j*omL) and transformed to
    # fractional frequency: those are in fctr2
    # I have removed Ampl to reduce dynamical range, will restore it later

    # Gs convention: 12, 23, 31, 21, 32, 13
    Xsl = Gs[:, 3] - Gs[:, 2] + (Gs[:, 0] - Gs[:, 5]) * fctr
    Ysl = Gs[:, 4] - Gs[:, 0] + (Gs[:, 1] - Gs[:, 3]) * fctr
    Zsl = Gs[:, 5] - Gs[:, 1] + (Gs[:, 2] - Gs[:, 4]) * fctr

    XYZsl = fctr2[:, None, :] * _jnp.concatenate(
        [Xsl[:, None, :], Ysl[:, None, :], Zsl[:, None, :]], axis=1
    )
    XYZf_slow = ampl[:, None, None] * _jnp.fft.fft(XYZsl, axis=2)
    M = XYZf_slow.shape[2]
    XYZf = _jnp.fft.fftshift(XYZf_slow, axes=2)
    f0 = (q - M / 2) / T  # freq = (q + np.arange(M) - M/2)/T
    return XYZf, f0


def construct_slow_part(
    T, arm_length, Ps, tm, f0, fdot, fstar, phi0, k, DP, DC, eplus, ecross, jax=False
):
    """
    Build linearly interpolated unit vectors of constellation arms.
    Matrix shape:
    - 3 satellites (vector start)
    - 3 satellites (vector end)
    - 3 coordinates
    - N points (linear interpolation of orbits)
    We only need to compute three vectors, since the matrix is skew-symmetric.
    TODO: Can we (or should we) even reduce it to a single vector ?
    """
    _jnp = jnp if jax else np
    P = _jnp.array(Ps)
    Nt = Ps[0].shape[1]
    nsrc = len(f0) if isinstance(f0, np.ndarray) else 1

    r = _jnp.zeros((4, 3, Nt))  # r convention: 12,13,23,31
    if jax:
        r = r.at[0].set(P[1] - P[0])  ## [3xNt]
        r = r.at[1].set(P[2] - P[0])  ## [3xNt]
        r = r.at[2].set(P[2] - P[1])  ## [3xNt]
        r = r.at[3].set(-r[1])  ## [3xNt]
    else:
        r[0] = P[1] - P[0]  ## [3xNt]
        r[1] = P[2] - P[0]
        r[2] = P[2] - P[1]
        r[3] = -r[1]
    r /= arm_length

    # kdotr convention: 12, 21, 13, 31, 23, 32
    kdotr = _jnp.zeros((nsrc, 6, Nt))
    if jax:
        kdotr = kdotr.at[:, ::2].set(_jnp.dot(k.T, r[:3]))
        kdotr = kdotr.at[:, 1::2].set(-kdotr[:, ::2])
    else:
        kdotr[:, ::2] = _jnp.dot(k.T, r[:3])
        kdotr[:, 1::2] = -kdotr[:, ::2]

    kdotP = _jnp.dot(k.T, Ps)
    kdotP /= CLIGHT

    Nt = len(tm)
    xi = tm - kdotP
    fi = f0[:, None, None] + fdot[:, None, None] * xi
    fonfs = fi / fstar  # Ratio of true frequency to transfer frequency

    ### compute transfer f-n
    q = _jnp.rint(f0 * T)  # index of nearest Fourier bin
    df = 2.0 * np.pi * (q / T)
    om = 2.0 * np.pi * f0

    # Reduce to (3, 3, N).
    # A = (eplus @ r * r * DP + ecross @ r * r * DC).sum(axis=2)
    idx = _jnp.array([0, 2, 3])
    aij = (
        _jnp.swapaxes(_jnp.dot(eplus, r[idx]), 1, 2) * r[idx] * DP[:, None, None, None]
        + _jnp.swapaxes(_jnp.dot(ecross, r[idx]), 1, 2)
        * r[idx]
        * DC[:, None, None, None]
    )
    A = aij.sum(axis=2)  # A convention: 12, 23, 31
    argS = (phi0[:, None] + (om - df)[:, None] * tm[None, :])[:, None, :] + (
        np.pi * fdot[:, None, None] * (xi**2)
    )
    kdotP = om[:, None, None] * kdotP - argS

    # Gs convention: 12, 23, 31, 21, 32, 13
    idx = _jnp.array([0, 4, 3, 1, 5, 2])
    arg_ij = 0.5 * fonfs[:, [0, 1, 2, 1, 2, 0]] * (1 + kdotr[:, idx])
    G = (
        0.25
        * _jnp.sinc(arg_ij / np.pi)
        * _jnp.exp(-1j * (arg_ij + kdotP[:, [0, 1, 2, 1, 2, 0]]))
        * A[:, [0, 1, 2, 0, 1, 2]]
    )

    return G, q


class FastGB:
    """Galactic binary waveform fast generation."""

    def __init__(self, orbits=None, T=6.2914560e7, delta_t=15, t0=0, tinit=0, N=None):
        """Init orbits and spacecraft positions."""

        self.N = N
        if "ldc" in str(orbits.__class__):
            self.orbits = orbits
        else:
            self.orbits = orbitsFromL0L1(orbits)

        self.T, self.delta_t, self.t0, self.tinit = T, delta_t, t0, tinit
        self.tm = np.linspace(0, self.T, num=N, endpoint=False)

        self.arm_length = self.orbits.arm_length
        self.position = [
            self.orbits.compute_position(1, self.t0 + self.tm),
            self.orbits.compute_position(2, self.t0 + self.tm),
            self.orbits.compute_position(3, self.t0 + self.tm),
        ]
        # Pi = [3 x Nt] - coordinates vs time

    def get_fd_tdixyz(self, params, tdi2=False):
        """Return TDI X,Y,Z in freq. domain.

        params is an [n,8] array of source parameters,
        [f0, fdot, ampl, beta, lambda, psi, incl, phi0]

        f0 in Hz, fdot in Hz/s, ampl in strain,
        theta, phi, psi, incl, phi0 in rad.
        """
        params = params.copy()
        jax = not (isinstance(params, np.ndarray))
        _jnp = jnp if jax else np

        if jax:
            _shift = np.pi * (
                2 * params[:, 0] * (self.tinit - self.t0)
                - params[:, 1] * (self.tinit - self.t0) ** 2
            )
            params = params.at[:, 7].set(params[:, 7] + _shift)
            params = params.at[:, 7].set(params[:, 7] * -1)
            params = params.at[:, 0].set(
                params[:, 0] - (params[:, 1] * (self.tinit - self.t0))
            )
            params = params.at[:, 3].set(np.pi / 2 - params[:, 3])  # ecl lat to theta
        else:
            params[:, 7] += np.pi * (
                2 * params[:, 0] * (self.tinit - self.t0)
                - params[:, 1] * (self.tinit - self.t0) ** 2
            )
            params[:, 7] *= -1
            params[:, 0] -= params[:, 1] * (self.tinit - self.t0)
            params[:, 3] = np.pi / 2 - params[:, 3]  # ecl lat to theta

        cosiota = _jnp.cos(params[:, 6])
        fstar = CLIGHT / (self.arm_length * 2 * np.pi)
        cosps = _jnp.cos(2 * params[:, 5])
        sinps = _jnp.sin(2 * params[:, 5])
        Aplus = params[:, 2] * (1.0 + cosiota * cosiota)
        Across = -2.0 * params[:, 2] * cosiota
        DP = Aplus * cosps - 1.0j * Across * sinps
        DC = -Aplus * sinps - 1.0j * Across * cosps

        sinth = _jnp.sin(params[:, 3])
        costh = _jnp.cos(params[:, 3])
        sinph = _jnp.sin(params[:, 4])
        cosph = _jnp.cos(params[:, 4])

        u = _jnp.array([costh * cosph, costh * sinph, -sinth], ndmin=2)
        v = _jnp.array([sinph, -cosph, _jnp.zeros_like(sinph)], ndmin=2)
        k = _jnp.array([-sinth * cosph, -sinth * sinph, -costh], ndmin=2)

        eplus = (v[None, :, :] * v[:, None, :] - u[None, :, :] * u[:, None, :]).T
        ecross = (u[None, :, :] * v[:, None, :] + v[None, :, :] * u[:, None, :]).T

        Gs, q = construct_slow_part(
            self.T,
            self.arm_length,
            _jnp.array(self.position),
            self.tm,
            params[:, 0],
            params[:, 1],
            fstar,
            params[:, 7],
            k,
            DP,
            DC,
            eplus,
            ecross,
            jax=jax,
        )
        Xf, f0 = computeXYZ(
            self.T,
            Gs,
            params[:, 0],
            params[:, 1],
            fstar,
            params[:, 2],
            q,
            self.tm,
            jax=jax,
        )
        df = 1 / self.T
        kmin = np.round(f0 / df).astype(np.int32)
        fctr = 0.5 * self.T / self.N
        f_min = df * kmin
        f_max = df * (kmin + self.N)
        if tdi2:
            tdi2_factor = self.get_tdi2_factor(
                _jnp.linspace(f_min, f_max, num=self.N, axis=-1, endpoint=False),
                jax=jax,
            )
            fctr *= tdi2_factor
            Xf *= fctr[:, None, :]
        else:
            Xf *= fctr

        X = Xf[:, 0, :]
        Y = Xf[:, 1, :]
        Z = Xf[:, 2, :]
        return X, Y, Z, kmin

    def get_tdi2_factor(self, f, jax=False):
        """tdi1.5 to tdi2 factor."""
        _jnp = jnp if jax else np
        omegaL = 2 * np.pi * f * (self.arm_length / CLIGHT)
        return 2.0j * _jnp.sin(2 * omegaL) * _jnp.exp(-2j * omegaL)
