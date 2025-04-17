"""Module for the kernel entropy estimator."""

from numpy import column_stack

from ... import Config
from ...utils.types import LogBaseType
from ..base import EntropyEstimator, WorkersMixin
from ..utils.array import assure_2d_data
from ..utils.kde import kde_probability_density_function


class KernelEntropyEstimator(WorkersMixin, EntropyEstimator):
    """Estimator for entropy (Shannon) using Kernel Density Estimation (KDE).

    Attributes
    ----------
    data : array-like
        The data used to estimate the entropy.
    bandwidth : float | int
        The bandwidth for the kernel.
    kernel : str
        Type of kernel to use, compatible with the KDE
        implementation :func:`kde_probability_density_function() <infomeasure.estimators.utils.kde.kde_probability_density_function>`.
    workers : int, optional
       Number of workers to use for parallel processing.
       Default is 1, meaning no parallel processing.
       If set to -1, all available CPU cores will be used.

    Notes
    -----
    A small ``bandwidth`` can lead to under-sampling,
    while a large ``bandwidth`` may over-smooth the data, obscuring details.
    """

    def __init__(
        self,
        data,
        *,  # all following parameters are keyword-only
        bandwidth: float | int,
        kernel: str,
        workers: int = 1,
        base: LogBaseType = Config.get("base"),
    ):
        """Initialize the KernelEntropyEstimator.

        Parameters
        ----------
        bandwidth : float | int
            The bandwidth for the kernel.
        kernel : str
            Type of kernel to use, compatible with the KDE
            implementation :func:`kde_probability_density_function() <infomeasure.estimators.utils.kde.kde_probability_density_function>`.
        workers : int, optional
           Number of workers to use for parallel processing.
           Default is 1, meaning no parallel processing.
           If set to -1, all available CPU cores will be used.
        """
        super().__init__(data, workers=workers, base=base)
        self.data = assure_2d_data(data)
        self.bandwidth = bandwidth
        self.kernel = kernel

    def _simple_entropy(self):
        """Calculate the entropy of the data.

        Returns
        -------
        array-like
            The local form of the entropy.
        """
        # Compute the KDE densities
        densities = kde_probability_density_function(
            self.data, self.bandwidth, kernel=self.kernel, workers=self.n_workers
        )

        # Compute the log of the densities
        return -self._log_base(densities)

    def _joint_entropy(self):
        """Calculate the joint entropy of the data.

        This is done by joining the variables into one space
        and calculating the entropy.

        Returns
        -------
        array-like
            The local form of the joint entropy.
        """
        self.data = column_stack(self.data)
        return self._simple_entropy()
