"""Define an object to store SPARK3D simulation results."""

from pathlib import Path

import numpy as np

from simultipac.plotter.plotter import Plotter
from simultipac.simulation_results.simulation_results import (
    SimulationResults,
    SimulationResultsFactory,
)


class Spark3DResults(SimulationResults):
    """Store a single SPARK3D simulation results."""


class Spark3DResultsFactory(SimulationResultsFactory):
    """Define an object to easily instantiate :class:`.Spark3DResults`."""

    def __init__(
        self,
        plotter: Plotter | None = None,
        freq_ghz: float | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(plotter=plotter, freq_ghz=freq_ghz, *args, **kwargs)

    def from_file(
        self, filepath: Path, e_acc: np.ndarray, delimiter: str = " ", **kwargs
    ) -> list[Spark3DResults]:
        """Load a ``TXT`` or ``CSV`` file and create associated objects."""
        filetype = filepath.suffix
        if filetype == ".txt":
            return self._from_txt(
                filepath=filepath, e_acc=e_acc, delimiter=delimiter, **kwargs
            )
        if filetype == ".csv":
            return self._from_csv(
                filepath=filepath, e_acc=e_acc, delimiter=delimiter, **kwargs
            )
        raise OSError(f"SPARK3D files must be CSV or TXT. I got {filetype = }")

    def _from_txt(
        self, filepath: Path, e_acc: np.ndarray, delimiter: str = " ", **kwargs
    ) -> list[Spark3DResults]:
        """
        Create several :class:`.Spark3DResults` from :file:`time_results.txt`.

        These file are generally produced with SPARK3D CLI. ``TXT`` files look
        like this::

            #Sim num	Power(W)	Time(s)	Num.elec.
            1           100         0       1000
            1           100         1       1010
            1           100         2       1020
            ...         ...         ...     ...
            2           50          0       1000
            2           50          1       900
            2           50          2       500
            ...         ...         ...     ...

        .. todo::
            Handle malformed files. In particular what happens if simulation
            numbers are mixed?

        Parameters
        ----------
        filepath : Path
            Path to the file to load.
        e_acc : np.ndarray
            Accelerating field values in :unit:`V/m`.
        delimiter : str, optional
            Delimiter between columns. The default is a space.

        """
        raw_data = np.loadtxt(filepath, delimiter=delimiter)
        raw_data[:, 2] *= 1e9

        results: list[Spark3DResults] = []

        for i, this_e_acc in enumerate(e_acc, start=1):
            idx_lines = np.where(raw_data[:, 0] == float(i))[0]
            power = raw_data[idx_lines, 1][0]
            time = raw_data[idx_lines, 2]
            num_elec = raw_data[idx_lines, 3]

            results.append(
                Spark3DResults(
                    id=i,
                    e_acc=this_e_acc,
                    time=time,
                    population=num_elec,
                    p_rms=power,
                    plotter=self._plotter,
                    period=self._period,
                )
            )

        return results

    def _from_csv(
        self, filepath: Path, e_acc: np.ndarray, delimiter: str = " ", **kwargs
    ) -> list[Spark3DResults]:
        """
        Create several :class:`.Spark3DResults` from :file:`time_results.csv`.

        Right-click on ``Multipactor results``, ``Export to CSV``.
        These file are manually produed by the user. ``CSV`` files look like
        this::

            0      1000    1000    1000    1000
            1e-9   1010    900     999     1001
            2e-9   1020    500     998     1002
            3e-9   1040    100     990     1003
            4e-9   1050    0       950     1004
            ...

        There are no headers. The first column holds the time in seconds.
        Following columns hold the number of electrons for every simulation
        (one simulation on one column).

        .. note::
            In order to be consistent with CST import, we remove the end of the
            simulations, when the population is 0.

        Parameters
        ----------
        filepath : Path
            Path to the file to load.
        e_acc : np.ndarray
            Accelerating field values in :unit:`V/m`.
        delimiter : str, optional
            Delimiter between columns. The default is a space.

        """
        raw_data = np.loadtxt(filepath, delimiter=delimiter)
        time = raw_data[:, 0] * 1e9
        p_rms = None

        results: list[Spark3DResults] = []

        for idx_col, this_e_acc in enumerate(e_acc, start=1):
            population = raw_data[:, idx_col]
            results.append(
                Spark3DResults(
                    id=idx_col,
                    e_acc=this_e_acc,
                    time=time,
                    population=population,
                    p_rms=p_rms,
                    plotter=self._plotter,
                    trim_trailing=True,
                    period=self._period,
                )
            )

        return results
