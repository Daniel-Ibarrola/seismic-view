import numpy as np
import pytest

from seismicview.test.wave_generator import WaveGenerator


def test_wave_generation():
    """Test the basic wave generation without changing period."""
    wg = WaveGenerator(size=100, n_samples=5, change_period=False)
    wave = next(wg)
    assert len(wave) == 5
    assert isinstance(wave[0], float)


def test_period_change():
    """Test that the period changes correctly if enabled."""
    wg = WaveGenerator(size=10, n_samples=1, change_period=True)
    initial_period = wg.period
    # Generate waves to trigger a period change
    for _ in range(11):  # Ensure we go beyond the initial data size to trigger the period change
        next(wg)
    assert wg.period == initial_period + 0.5


def test_stop_generation():
    """Test the stop method actually stops the generation."""
    wg = WaveGenerator(size=10, n_samples=2)
    wg.stop()
    with pytest.raises(StopIteration):
        next(wg)


def test_wave_values():
    """Test the actual values of the generated sine wave against expected numpy results."""
    wg = WaveGenerator(size=4, n_samples=4, change_period=False)
    wg.period = 2  # Set a specific period for predictable output
    expected_values = np.sin(2 * np.linspace(0, 2 * np.pi, 4)) * 100
    generated_values = next(wg)
    assert np.allclose(generated_values, expected_values,
                       atol=1e-6), "Generated values do not match expected sine values."


def test_cycle_restart_and_period_increase():
    """Test that the generator correctly restarts its cycle and increases the period if enabled."""
    size = 10
    n_samples = 5
    wg = WaveGenerator(size=size, n_samples=n_samples, change_period=True)
    # Complete one full cycle
    n_iters = size // n_samples
    for _ in range(n_iters):
        next(wg)
    # Test if it restarts correctly
    assert wg.index == 0, "Index did not reset after completing a cycle."
    # Test if period increases
    next(wg)  # Trigger the increase
    assert wg.period == 4.5, "Period did not increase after completing a cycle."


def test_get_wave_stats():
    """ Test the statistics from the values of a wave"""
    values = [1., 2., 3., 4.,]
    channel_data = WaveGenerator.get_wave_stats("S160", "HLZ", values)
    expected_data = {
        "station": "S160",
        "channel": "HLZ",
        "min": 1.,
        "max": 4.,
        "avg": 2.5,
        "trace": [1., 2., 3., 4]
    }
    assert channel_data == expected_data


if __name__ == "__main__":
    pytest.main()
