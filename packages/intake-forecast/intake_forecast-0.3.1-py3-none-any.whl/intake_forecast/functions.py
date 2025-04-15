import numpy as np


def amplitude(dcomplex):
    """Amplitude from complex-valued array."""
    return np.absolute(dcomplex)


def phase(dcomplex):
    """Phase from complex-valued array."""
    return np.rad2deg(np.arctan2(-dcomplex.imag, dcomplex.real)) % 360


def speed(u, v):
    return np.sqrt(u**2 + v**2)


def wspd_at_height(wspd, input_height, output_height=10.0):
    return wspd * (output_height / input_height) ** 0.11
