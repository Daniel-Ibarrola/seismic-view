import numpy as np

from seismicview.models import Wave


class WaveGenerator:
    """A generator of sine waves.

    This class generates sine waves with a configurable number of samples, period change behavior, and size. It can be used iteratively to produce sequences of sine wave values.

    Attributes:
        data (list[float]): The linearly spaced data points between 0 and 2π.
        index (int): The current position in the data array for generating sine values.
        period (float): The current period of the sine wave. Affects the frequency of the wave.
        change_period (bool): Flag to determine if the period should change after each full iteration over `data`.
        n_samples (int): The number of sine wave samples to generate in each iteration.
        _stop (bool): Internal flag to stop the generation of sine waves.

    Parameters:
        size (int): The number of points to generate between 0 and 2π for the sine wave. Defaults to 100.
        n_samples (int): The number of samples to return with each iteration. Defaults to 10.
        change_period (bool): Whether to change the sine wave period after completing a pass through all points. Defaults to True.
    """

    def __init__(self, size: int = 100, n_samples: int = 10, change_period: bool = True):
        """Initializes the WaveGenerator with specified configuration."""
        self.data = np.linspace(0, 2*np.pi, size).tolist()
        self.index = 0
        self.period = 4
        self.change_period = change_period
        self.n_samples = n_samples

        self._stop = False

    def stop(self) -> None:
        """Stops the generation of further sine wave values."""
        self._stop = True

    @staticmethod
    def get_wave_stats(station: str, channel, values: list[float]) -> Wave:
        return Wave(
            station=station,
            channel=channel,
            min=min(values),
            max=max(values),
            avg=sum(values) / len(values),
            trace=values
        )

    def _reset_index(self) -> None:
        if self.index > (len(self.data) - 1):
            self.index = 0

    def _increase_period(self) -> None:
        if self.change_period and self.index > (len(self.data) - 1):
            self.period += 0.5

    def __iter__(self):
        """Returns the iterator object itself."""
        return self

    def __next__(self) -> list[float]:
        """Generates the next set of sine wave samples.

        Returns:
            list[int]: A list of sine wave values scaled by 100.

        Raises:
            StopIteration: If the generator is stopped or completes its current cycle.
        """
        if self.change_period and self.period > 5:
            self.period = 1

        self._increase_period()
        self._reset_index()

        if not self._stop:
            values = []
            for _ in range(self.n_samples):
                sine = np.sin(self.period * self.data[self.index]) * 100
                values.append(sine)
                self.index += 1

            self._increase_period()
            self._reset_index()

            return values

        raise StopIteration
