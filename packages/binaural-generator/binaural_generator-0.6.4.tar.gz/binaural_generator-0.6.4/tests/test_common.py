"""Common utilities for tests."""

import numpy as np


def check_generate_output(noise_generator) -> None:
    "Check common outputs of the noise generator."
    # Test with zero samples
    zero_sample = noise_generator.generate(0)
    assert isinstance(zero_sample, np.ndarray)
    assert len(zero_sample) == 0

    # Test with negative samples (should return empty array)
    negative_sample = noise_generator.generate(-10)
    assert len(negative_sample) == 0

    # Test with very small sample count (should still work)
    small_sample = noise_generator.generate(10)
    assert len(small_sample) == 10
    assert np.all(np.abs(small_sample) <= 1.01)  # Allow slight tolerance

    # Test with odd sample counts
    odd_sample = noise_generator.generate(99)
    assert len(odd_sample) == 99
    assert np.all(np.abs(odd_sample) <= 1.01)


def check_basic_noise_properties(noise: np.ndarray, num_samples: int) -> None:
    """Check basic properties that all noise types should satisfy.

    Args:
        noise: The generated noise samples
        num_samples: Expected number of samples
    """
    # Check basic properties
    assert len(noise) == num_samples
    assert -1.0 <= np.min(noise) <= 0
    assert 0 <= np.max(noise) <= 1.0


def estimate_spectral_slope(noise_samples: np.ndarray, freqs: np.ndarray) -> float:
    """
    Estimates the spectral slope of noise from its power spectral density.
    Returns the slope of a linear fit to the log-log PSD.

    Args:
        noise_samples: Noise samples array
        freqs: Frequency array corresponding to the PSD bins

    Returns:
        Estimated spectral slope
    """
    # Compute power spectral density
    freqs = freqs[1:]  # Remove DC component
    psd = np.abs(np.fft.rfft(noise_samples))[1:]  # Remove DC component

    # Compute log-log values for linear fit
    log_freqs = np.log10(freqs)
    log_psd = np.log10(psd)

    # Use polynomial fit to estimate slope
    # First degree polynomial: y = mx + b
    coefficients = np.polyfit(log_freqs, log_psd, 1)
    return coefficients[0]  # Return the slope
