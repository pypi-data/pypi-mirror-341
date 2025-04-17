"""Tools for automated validation of the periodical pattern of scATAC Fragment Length Distributions."""
# Author: Jan Detleffsen (jan.detleffsen@mpi-bn.mpg.de)

import numpy as np
from numpy.random import default_rng
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import matplotlib

from tqdm import tqdm
import multiprocessing as mp
import concurrent.futures

from scipy.signal import find_peaks
from scipy.signal import fftconvolve

from beartype.typing import Optional, Literal, SupportsFloat, Tuple, Union, Dict
from beartype import beartype
import numpy.typing as npt

import peakqc.insertsizes as insertsizes


@beartype
def moving_average(series: npt.ArrayLike,
                   n: int = 10) -> npt.ArrayLike:
    """
    Move average filter to smooth out data.

    This implementation ensures that the smoothed data has no shift and
    local maxima remain at the same position.

    Parameters
    ----------
    series : npt.ArrayLike
        Array of data to be smoothed.
    n : int, default 10
        Number of steps to the left and right of the current step to be averaged.

    Returns
    -------
    npt.ArrayLike
        Smoothed array
    """

    list(series)
    smoothed = []
    for i in range(len(series)):  # loop over all steps
        sumPerStep = 0
        if i > n and i <= (len(series) - n):  # main phase
            for j in range(-n, n):
                sumPerStep += series[i + j]
            smoothed.append(sumPerStep / (n * 2))
        elif i > (len(series) - n):  # end phase
            smoothed.append(series[i])
        elif i <= n:  # init phase
            smoothed.append(series[i])

    smoothed = np.array(smoothed)

    return smoothed


@beartype
def multi_ma(series: npt.ArrayLike,
             n: int = 2,
             window_size: int = 10,
             n_threads: int = 8) -> npt.ArrayLike:
    """
    Multiprocessing wrapper for moving average filter.

    Parameters
    ----------
    series : npt.ArrayLike
        Array of data to be smoothed.
    n : int, default 2
        Number of times to apply the filter
    window_size : int, default 10
        Number of steps to the left and right of the current step to be averaged.
    n_threads : int, default 8
        Number of threads to be used for multiprocessing.

    Returns
    -------
    npt.ArrayLike
        array of smoothed array
    """

    # smooth
    for i in range(n):

        smooth_series = []
        # init pool
        pool = mp.Pool(n_threads)
        jobs = []
        # loop over chunks

        for dist in series:
            job = pool.apply_async(moving_average, args=(dist, window_size))
            jobs.append(job)
        pool.close()

        # collect results
        for job in jobs:
            smooth_series.append(job.get())

        series = np.array(smooth_series)

    return series


@beartype
def scale(series_arr: npt.ArrayLike) -> npt.ArrayLike:
    """
    Scale a series array to a range of 0 to 1.

    Parameters
    ----------
    series_arr : npt.ArrayLike
        Array of data to be scaled 1D or 2D

    Notes
    -----
    If the array is 2D, the scaling is done on axis=1.

    Returns
    -------
    npt.ArrayLike
        Scaled array
    """

    if len(series_arr.shape) == 1:
        max_v = np.max(series_arr)
        scaled_arr = series_arr / max_v

        return scaled_arr

    elif len(series_arr.shape) == 2:
        # Scale as sum off all features within cell match one
        maxis = np.max(series_arr, axis=1)  # total features per cell
        scaled_arr = np.divide(series_arr.T, maxis).T

        return scaled_arr


# ////////////////////////////////// Peak calling \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


@beartype
def call_peaks(data: npt.ArrayLike,
               n_threads: int = 4,
               distance: int = 50,
               width: int = 10) -> npt.ArrayLike:
    """
    Find peaks for multiple arrays at once.

    Parameters
    ----------
    data : np.ndarray
        Array of arrays to find peaks in (2D).
    n_threads : int, default 4
        Number of threads to be used for multiprocessing.
    distance : int, default 50
        Minimum distance between peaks.
    width : int, default 10
        Minimum width of peaks.

    Notes
    -----
    Multiprocessing wrapper for scipy.signal.find_peaks.

    Returns
    -------
    npt.ArrayLike
        Array of peaks (index of data)
    """

    peaks = []

    pool = mp.Pool(n_threads)
    jobs = []

    for array in data:
        job = pool.apply_async(call_peaks_worker, args=(array, distance, width))
        jobs.append(job)
    pool.close()

    # collect results
    for job in jobs:
        peak_list = job.get()
        peaks.append(peak_list)

    return peaks


@beartype
def call_peaks_worker(array: npt.ArrayLike,
                      distance: int = 50,
                      width: int = 10) -> npt.ArrayLike:
    """
    Worker function for multiprocessing of scipy.signal.find_peaks.

    Parameters
    ----------
    array : npt.ArrayLike
        Array of data to find peaks in.
    distance : int, default 50
        Minimum distance between peaks.
    width : int, default 10
        Minimum width of peaks.

    Returns
    -------
    npt.ArrayLike
        Array of peaks (index of data)
    """

    peaks, _ = find_peaks(array, distance=distance, width=width)

    return peaks


@beartype
def filter_peaks(peaks: npt.ArrayLike,
                 reference: npt.ArrayLike,
                 peaks_thr: SupportsFloat,
                 operator: Literal['bigger', 'smaller'] = 'bigger') -> npt.ArrayLike:
    """
    Filter peaks based on a reference array and a threshold.

    Parameters
    ----------
    peaks : npt.ArrayLike
        Array of peaks to be filtered.
    reference : npt.ArrayLike
        Array of reference values (e.g. data were peaks were found).
    peaks_thr : float
        Threshold for filtering.
    operator : str, default 'bigger'
        Operator for filtering. Options ['bigger', 'smaller'].

    Returns
    -------
    npt.ArrayLike
        Filtered array of peaks
    """

    filtered_peaks = []

    if operator == "bigger":
        if len(reference.shape) == 1:
            filtered_peaks = peaks[np.where(reference[peaks] >= peaks_thr)]
        if len(reference.shape) == 2:
            for i, index in enumerate(peaks):
                filtered_peaks.append(index[np.where(reference[i, index] >= peaks_thr)])

    if operator == "smaller":
        if len(reference.shape) == 1:
            filtered_peaks = peaks[np.where(reference[peaks] <= peaks_thr)]
        if len(reference.shape) == 2:
            for i, index in enumerate(peaks):
                filtered_peaks.append(index[np.where(reference[i, index] <= peaks_thr)])

    return filtered_peaks

# //////////////////////////////////////// Scoring \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


@beartype
def distances_score(peaks: npt.ArrayLike,
                    momentum: npt.ArrayLike,
                    period: int,
                    penalty_scale: int) -> npt.ArrayLike:
    """
    Calculate a score based on the distances between peaks.

    Parameters
    ----------
    peaks : npt.ArrayLike
        Array of peaks.
    momentum : npt.ArrayLike
        Array of momentum values.
    period : int
        expected distances
    penalty_scale : int
        scale parameter for the penalty

    Returns
    -------
    npt.ArrayLike
        Array of scores
    """

    scores = []
    # loop over all cells
    for i in range(len(peaks)):
        # get peaks and momentum for single cell
        peak_list = peaks[i]
        single_momentum = momentum[i]

        # calculate score
        if len(peak_list) == 0:
            score = 0
        elif len(peak_list) == 1:  # if only one peak, score is the momentum at that peak divided by 100
            score = single_momentum[peak_list[0]] / 100
        elif len(peak_list) > 1:  # if more than one peak
            corrected_scores = []
            for j in range(1, len(peak_list)):  # loop over all peaks
                amplitude = single_momentum[peak_list[j - 1]] * 2  # amplitude is the momentum at the previous peak

                diff = peak_list[j] - peak_list[j - 1]  # difference between the current and previous peak
                corrected_score = amplitude - (abs(diff - period) / penalty_scale)  # corrected score
                if corrected_score < 0:
                    corrected_score = 0

                corrected_scores.append(corrected_score)  # append corrected score to list

            score = float(np.sum(np.array(corrected_scores))) + 0  # sum all corrected scores

        scores.append(score)  # append score to list

    return scores


@beartype
def score_mask(peaks: npt.ArrayLike,
               convolved_data: npt.ArrayLike,
               plot: bool = False,
               save: Optional[str] = None) -> npt.ArrayLike:
    """
    Compute a score for each sample based on the convolved data and the peaks multiplied by a score mask.

    Parameters
    ----------
    peaks : npt.ArrayLike
        Array of arrays of the peaks.
    convolved_data : npt.ArrayLike
        Array of arrays of the convolved data.
    plot : bool, default False
        If true, the score mask is plotted.
    save : bool, default False
        If true, the score mask is saved as a .png file.

    Returns
    -------
    npt.ArrayLike
        Array of scores for each sample
    """

    # build score mask
    if plot:
        score_mask, _ = build_score_mask(plot=plot, save=save)
    else:
        score_mask = build_score_mask(plot=plot, save=save)

    scores = []
    # loop over all cells
    for i, peak_list in enumerate(peaks):
        conv = convolved_data[i]

        # calculate score
        # if no peaks, score is 0
        if len(peak_list) == 0:
            score = 0
        # if only one peak, score is the convolved data at that peak multiplied by the score mask
        elif len(peak_list) == 1:
            score = conv[peak_list[0]] * score_mask[0][peak_list[0]]

        # if more than one peak, score is the sum of the convolved data at each peak multiplied by the score mask
        elif len(peak_list) > 1:
            score = 0
            for j in range(1, len(peak_list)):
                if j <= 3:
                    score += conv[peak_list[j]] * score_mask[j][peak_list[j]]
                else:
                    score += conv[peak_list[j]] * score_mask[3][peak_list[j]]

        scores.append(score)

    return np.array(scores)


@beartype
def build_score_mask(plot: bool = False,
                     save: Optional[str] = None,
                     mu_list: list[int] = [42, 200, 360, 550],
                     sigma_list: list[int] = [25, 35, 45, 25]) -> npt.ArrayLike | tuple[npt.ArrayLike, tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]:
    """
    Build a score mask for the score by custom continuous wavelet transformation.

    Mask is a sum of 4 Gaussian curves with mu and sigma specified
    for the expected peak positions and deviations.

    Parameters
    ----------
    plot : bool, default True
        If true, the score mask is plotted.
    save : bool, default False
        If true, the score mask is saved as png
    mu_list : list[int], default [42, 200, 360, 550]
        List of mu values for the Gaussian curves.
    sigma_list : list[int], default [25, 35, 45, 25]
        List of sigma values for the Gaussian curves.

    Returns
    -------
    npt.ArrayLike | tuple[npt.ArrayLike, tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
        Array of the score mask or tuple of the array and the plot.
    """

    # Create an array of x values
    x = np.linspace(0, 1000, 1000)
    gaussians = []
    for mu, sigma in zip(mu_list, sigma_list):
        gaussians.append(scale((1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)))

    gaussians = np.array(gaussians)

    if plot:
        fig, ax = plt.subplots()

        ax.plot(gaussians[0])
        ax.plot(gaussians[1])
        ax.plot(gaussians[2])
        ax.plot(gaussians[3])
        ax.set_title('Score-Mask')
        ax.set_xlabel('Position')
        ax.set_ylabel('Scoring')

        if save:
            plt.savefig(save)

        return gaussians, (fig, ax)

    return gaussians


@beartype
def gauss(x: npt.ArrayLike,
          mu: int | float,
          sigma: int | float) -> npt.ArrayLike:
    """
    Calculate the values of the Gaussian function for a given x, mu and sigma.

    Parameters
    ----------
    x : npt.ArrayLike
        x values
    mu : float | int
        mu value
    sigma : float | int
        sigma value

    Returns
    -------
    npt.ArrayLike
        Array of Gaussian values
    """

    gaussian = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    # scale max to 1
    gaussian = scale(gaussian)

    return gaussian

# //////////////////////////// wavelet transformation \\\\\\\\\\\\\\\\\\\\\\\\\\\\\


@beartype
def cos_wavelet(wavelength: int = 100,
                amplitude: float | int = 1.0,
                phase_shift: float | int = 0,
                mu: float | int = 0.0,
                sigma: float | int = 0.4,
                plot: bool = False,
                save: Optional[str] = None) -> npt.ArrayLike | tuple[npt.ArrayLike, tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]:
    """
    Build a cosine wavelet. The wavelet is a cosine curve multiplied by a Gaussian curve.

    Parameters
    ----------
    wavelength : int, default 100
        Wavelength of the cosine curve.
    amplitude : float | int, default 1.0
        Amplitude of the cosine curve.
    phase_shift : float | int, default 0
        Phase shift of the cosine curve.
    mu : float | int, default 0.0
        Mean of the Gaussian curve.
    sigma : float | int, default 0.4
        Standard deviation of the Gaussian curve.
    plot : bool, default False
        Plot the wavelet.
    save : Optional[str], default None
        If true, the figure is saved as a .png file.
        Name of the figure to save.

    Returns
    -------
    npt.ArrayLike | tuple[npt.ArrayLike, tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
        Array of the wavelet or tuple of the array and the plot.
    """

    # Scale the wavelength and sigma with the scale
    wavl_scale = int(wavelength * 1.5)
    sigma = sigma * wavl_scale  # This ensures sigma is scaled with scale
    frequency = 1.5 / wavl_scale  # This ensures the frequency is scaled with scale

    # Create an array of x values
    x = np.linspace(-wavl_scale, wavl_scale, wavl_scale * 2)

    # Compute the centered sine curve values for each x
    cosine_curve = amplitude * np.cos(2 * np.pi * frequency * x + phase_shift)

    # Compute the Gaussian values for each x
    gaussian = gauss(x, mu, sigma)

    # Multiply the cosine curve with the Gaussian
    wavelet = cosine_curve * gaussian

    if plot:
        fig, ax = plt.subplots()
        ax.plot(wavelet)
        ax.set_title('Wavelet')
        ax.set_xlabel('Interval')
        ax.set_ylabel('Amplitude')

        if save:
            plt.savefig(save)

        # Optionally, to show the figure
        plt.show()

        return wavelet, (fig, ax)

    return wavelet


@beartype
def get_wavelets(wavelengths: list[int],
                 sigma: float = 0.4) -> list[npt.ArrayLike]:
    """
    Get a list of wavelets.

    Parameters
    ----------
    wavelengths : list[int]
        List of wavelengths for the wavelets.
    sigma : float, default 0.4
        Standard deviation of the Gaussian curve.

    Returns
    -------
    list[npt.ArrayLike]
        List of wavelets.
    """
    wavelets = []
    for wavelength in wavelengths:
        wavelet = cos_wavelet(wavelength=wavelength,
                              amplitude=1.0,
                              phase_shift=0,
                              mu=0.0,
                              sigma=sigma,
                              plot=False)
        wavelets.append(wavelet)

    return wavelets


@beartype
def wavelet_transformation(data: npt.ArrayLike,
                           wavelets: list[npt.ArrayLike]) -> npt.ArrayLike:
    """
    Get wavelet transformations of the fragment length distributions.

    Parameters
    ----------
    data : npt.ArrayLike
        Array of the fragment length distributions.
    wavelets : list[npt.ArrayLike]
        List of wavelets.

    Returns
    -------
    npt.ArrayLike
        Array of the wavelet transformations.
    """

    convolved_data = []
    for wavelet in wavelets:
        convolved_data.append(np.convolve(data, wavelet, mode='same'))

    convolved_data = np.array(convolved_data)

    return convolved_data


@beartype
def wavelet_transform_fld(dists_arr: npt.ArrayLike,
                          wavelengths: Optional[list[int]] = None,
                          sigma: float = 0.4) -> npt.ArrayLike:
    """
    Get wavelet transformations of the fragment length distributions.

    Parameters
    ----------
    dists_arr : npt.ArrayLike
        Array of arrays of the fragment length distributions.
    wavelengths : list[int], default None
        List of wavelengths for the wavelets.
    sigma : float, default 0.4
        Standard deviation of the Gaussian curve.

    Returns
    -------
    npt.ArrayLike
        Array of arrays of the wavelet transformations.
    """

    # Set default wavelengths
    if wavelengths is None:
        wavelengths = np.arange(5, 250, 5).astype(int)

    # Get wavelets
    wavelets = get_wavelets(wavelengths, sigma=sigma)

    dataset_convolution = []
    # Process each cell with the wavelet transformation
    for cell in tqdm(dists_arr, desc="Processing cells"):
        dataset_convolution.append(wavelet_transformation(cell, wavelets))

    dataset_convolution = np.array(dataset_convolution)

    return dataset_convolution


@beartype
def custom_conv(data: npt.ArrayLike,
                wavelength: int = 150,
                sigma: float = 0.4,
                mode: str = 'convolve',
                plot_wavl: bool = False) -> npt.ArrayLike:
    """
    Get custom implementation of a wavelet transformation based convolution.

    Parameters
    ----------
    data : npt.ArrayLike
        Array of arrays of the fragment length distributions.
    wavelength : int, default 150
        Wavelength of the wavelet.
    sigma : float, default 0.4
        Standard deviation of the Gaussian curve.
    mode : str, default 'concolve'
        Mode of the convolution. Either 'convolve' or 'fftconvolve'.
    plot_wavl : bool, default False
        If true, the wavelet is plotted.

    Returns
    -------
    npt.ArrayLike
        Array of convolved data.
    """

    # Get the wavelet
    if plot_wavl:
        wavelet, _ = cos_wavelet(wavelength=wavelength,
                                 amplitude=1.0,
                                 phase_shift=0,
                                 mu=0.0,
                                 sigma=sigma,
                                 plot=plot_wavl)
    else:
        wavelet = cos_wavelet(wavelength=wavelength,
                              amplitude=1.0,
                              phase_shift=0,
                              mu=0.0,
                              sigma=sigma,
                              plot=plot_wavl)

    # convolve with the data
    convolved_data = []
    for cell in data:
        if mode == 'convolve':
            convolved_data.append(np.convolve(cell, wavelet, mode='same'))
        elif mode == 'fftconvolve':
            convolved_data.append(fftconvolve(data, wavelet, mode='same'))

    return np.array(convolved_data)


@beartype
def score_by_conv(data: npt.ArrayLike,
                  wavelength: int = 150,
                  sigma: float = 0.4,
                  plot_wavl: bool = False,
                  n_threads: int = 12,
                  peaks_thr: SupportsFloat = 0.01,
                  operator: str = 'bigger',
                  plot_mask: bool = False,
                  plot_ov: bool = True,
                  save: Optional[str] = None,
                  sample: int = 0) -> npt.ArrayLike:
    """
    Get a score by a continues wavelet transformation based convolution of the distribution with a single wavelet and score mask.

    Parameters
    ----------
    data : npt.ArrayLike
        Array of arrays of the fragment length distributions.
    wavelength : int, default 150
        Wavelength of the wavelet.
    sigma : float, default 0.4
        Standard deviation of the Gaussian curve.
    plot_wavl : bool, default False
        If true, the wavelet is plotted.
    n_threads : int, default 12
        Number of threads to use for the peak calling.
    peaks_thr : float, default 0.01
        Threshold for the peak calling.
    operator : str, default 'bigger'
        Operator to use for the peak calling. Either 'bigger' or 'smaller'.
    plot_mask : bool, default False
        If true, the score mask is plotted.
    plot_ov : bool, default True
        If true, the overlay of the score mask and the convolved data is plotted.
    save : bool, default False
        If true, the figure is saved.
    sample : int, default 0
        Index of the sample to plot.

    Returns
    -------
    npt.ArrayLike
        Array of scores for each sample
    """

    convolved_data = custom_conv(data, wavelength=wavelength, sigma=sigma, plot_wavl=plot_wavl)

    peaks = call_peaks(convolved_data, n_threads=n_threads)

    filtered_peaks = filter_peaks(peaks, reference=convolved_data, peaks_thr=peaks_thr, operator=operator)

    scores = score_mask(peaks, convolved_data, plot=plot_mask)

    if plot_ov:
        plot_custom_conv(convolved_data, data, filtered_peaks, scores=scores, sample_n=sample, save=save)

    return scores


# //////////////////////////////// plotting \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

@beartype
def density_plot(count_table: npt.ArrayLike,
                 max_abundance: int = 600,
                 target_height: int = 1000,
                 save: Optional[str] = None,
                 colormap: str = 'jet',
                 ax: Optional[matplotlib.axes.Axes] = None,
                 fig: Optional[matplotlib.figure.Figure] = None) -> npt.ArrayLike:
    """
    Plot the density of the fragment length distribution over all cells.

    The density is calculated by binning the abundances of the fragment lengths.

    Parameters
    ----------
    count_table : npt.ArrayLike
        Array of arrays of the fragment length distributions
    max_abundance : int, default 600
        Maximal abundance of a fragment length of a cell (for better visability)
    target_height : int, default 1000
        Target height of the plot
    save : Optional[str], default None
        If true, the figure is saved under the given name.
    colormap : str, default 'jet'
        Color map of the plot.
    ax : matplotlib.axes.Axes, default None
        Axes to plot on.
    fig : matplotlib.figure.Figure, default None
        Figure to plot on.

    Returns
    -------
    npt.ArrayLike
        Axes and figure of the plot.
    """
    count_table = count_table
    # handle 0,1 min/max scaled count_table
    if count_table.dtype != 'int64':
        if np.max(count_table) > 1:
            rounded = (np.round(count_table)).astype('int64')
            count_table = rounded
        else:
            count_table = (count_table * 1000).astype('int64')
    # get the maximal abundance of a fragment length over all cells
    max_value = np.max(np.around(count_table).astype(int))
    # Init empty densities list
    densities = []
    # loop over all fragment lengths from 0 to 1000
    for i in range(0, len(count_table[0])):
        column = count_table[:, i]
        # round abundances to be integers, that they are countable
        rounded = np.around(column).astype(int)
        # count the abundance of the abundances with boundaries 0 to maximal abundance
        gradient = np.bincount(rounded, minlength=max_value + 1)
        densities.append(gradient)
    densities = np.array(densities)

    # Log normalization + 1 to avoid log(0)
    densities_log = np.log1p(densities)

    # Transpose the matrix
    densities = densities_log.T

    # get the section of interest
    densities = densities[:max_abundance]

    # calculate the mean of the FLD
    mean = count_table.sum(axis=0) / len(count_table)

    # Stretch or compress densities' y-axis to the target height
    num_rows = densities.shape[0]
    old_y = np.linspace(0, num_rows - 1, num_rows)
    new_y = np.linspace(0, num_rows - 1, 1000)

    # Interpolate the densities along the y-axis
    densities_interpolated = np.array([np.interp(new_y, old_y, densities[:, i]) for i in range(densities.shape[1])]).T

    # scaling factor for mean
    scaling_factor = len(new_y) / len(old_y)

    # Apply the scaling factor to the mean values
    mean_interpolated = mean * scaling_factor

    # Initialize subplots
    if ax is None:
        main_plot = True
        fig, ax = plt.subplots()
    else:
        main_plot = False

    # Display the image
    im = ax.imshow(densities_interpolated, aspect='auto', origin="lower", cmap=colormap)

    # Plot additional data
    ax.plot(mean_interpolated, color="red", markersize=1)

    # Set labels and title
    ax.set_title('Fragment Length Density Plot')
    ax.set_xlabel('Fragment Length', color='blue')
    ax.set_ylabel('Number of Fragments', color='blue')

    # Adjust y-ticks to show original scale
    ax.set_yticks(np.linspace(0, target_height - 1, 6))
    ax.set_yticklabels(np.linspace(0, num_rows - 1, 6).astype(int))

    # Add colorbar to the plot
    if fig is not None:
        fig.colorbar(im, ax=ax, label='Density (log scale)')

    if main_plot:
        if save:
            plt.savefig(save)

        plt.show()

    figure = np.array([ax, fig])

    return figure


@beartype
def plot_wavelet_transformation(convolution: npt.ArrayLike,
                                wavelengths: npt.ArrayLike,
                                fld: Optional[npt.ArrayLike] = None,
                                save: Optional[str] = None) -> npt.ArrayLike:
    """
    Plot the wavelet transformation of the fragment length distribution.

    If fld is not None, the fragment length distribution is plotted as well.

    Parameters
    ----------
    convolution : npt.ArrayLike
        Wavelet transformation of the fragment length distribution
    wavelengths : npt.ArrayLike
        Wavelengths of the wavelet transformation
    fld : npt.ArrayLike, default None
        Fragment length distribution
    save : Optional[str], default None
        If true, the figure is saved under the given name.

    Returns
    -------
    npt.ArrayLike
        Axes of the plot
    """

    xmin = 0
    xmax = convolution.shape[1]
    ymin, ymax = wavelengths[0], wavelengths[-1]

    if fld is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.set_title('Fragment Length Distribution')
        ax1.set_xlabel('Fragment Length (bp)')
        ax1.set_ylabel('Number of Fragments')
        ax1.plot(fld)

        img = ax2.imshow(convolution, aspect='auto', cmap='jet', extent=[xmin, xmax, ymax, ymin])
        # Adding a colorbar to ax2
        cbar = fig.colorbar(img, ax=ax2)
        cbar.set_label('Fit')

        ax2.set_title('Wavelet Transformation')
        ax2.set_xlabel('Fragment Length (bp)')
        ax2.set_ylabel('Wavelength (bp)')
        ax2.grid(color='white', linestyle='--', linewidth=0.5)

        plt.tight_layout()

    else:
        # Create a figure and set the size
        plt.imshow(convolution, aspect='auto', cmap='jet', extent=[xmin, xmax, ymax, ymin])
        plt.colorbar(label='Fit')
        plt.xlabel('Fragment Length (bp)')
        plt.ylabel('Wavelength (bp)')
        plt.title('Wavelet Transformation')

        plt.grid(color='white', linestyle='--', linewidth=0.5)

    # Save the figure
    if save:
        plt.savefig(save)

    plt.show()

    axes = np.array([ax1, ax2])

    return axes


@beartype
def plot_custom_conv(convolved_data: npt.ArrayLike,
                     data: npt.ArrayLike,
                     peaks: npt.ArrayLike,
                     scores: npt.ArrayLike,
                     sample_n: int = 0,
                     save: Optional[str] = None) -> npt.ArrayLike:
    """
    Plot the overlay of the convolved data, the peaks and the score mask.

    Parameters
    ----------
    convolved_data : npt.ArrayLike
        Array of the convolved data.
    data : npt.ArrayLike
        Array of the original data.
    peaks : npt.ArrayLike
        Array of the peaks.
    scores : npt.ArrayLike
        Array of the scores.
    sample_n : int, default 0
        Index of the sample to plot.
    save : Optional[str], default None
        If true, the figure is saved under the given name.

    Returns
    -------
    npt.ArrayLike
        Axes of the plot
    """

    single_m = convolved_data[sample_n]
    single_d = data[sample_n]
    sample_peaks = peaks[sample_n]

    points_x = sample_peaks
    points_y = single_m[sample_peaks]

    points_y_data = single_d[sample_peaks]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

    ax1.set_title("Convolution: ")
    ax1.set_ylabel('Convolution Fit')
    ax1.set_xlabel('Fragment Length', color='blue')
    ax1.plot(single_m)
    ax1.scatter(points_x, points_y, color='red', zorder=2)

    ax2.set_title('Fragment Length Distribution')
    ax2.set_ylabel('Number of Fragments')
    ax2.set_xlabel('Fragment Length', color='blue')
    ax2.plot(single_d)
    ax2.scatter(points_x, points_y_data, color='red', zorder=2)

    ax3.set_title('Scores')
    ax3.set_ylabel('Number of Cells')
    ax3.set_xlabel('Score', color='blue')
    ax3.hist(scores, bins=100, log=True)

    plt.tight_layout()

    if save:
        plt.savefig(save)

    plt.show()

    axes = np.array([ax1, ax2, ax3])

    return axes


# https://numpy.org/doc/2.2/reference/random/multithreading.html
@beartype
class MultithreadedMultinomialSampler:
    """Multithreaded multinomial sampler."""

    def __init__(self,
                 dists_arr: npt.ArrayLike,
                 insert_counts: Union[npt.ArrayLike, pd.Series],
                 sample_size: int = 10000,
                 n_simulations: int = 100,
                 size: int = 1,
                 seed: int = 42,
                 n_threads: Optional[int] = None,
                 sample_all: bool = False):
        """
        Initialize the multithreaded multinomial sampler.

        Parameters
        ----------
        dists_arr : npt.ArrayLike
            A 2D array where each row represents the count distribution of fragment lengths.
        insert_counts : Union[npt.ArrayLike, pd.Series]
            A 1D array indicating the number of elements per distribution.
        sample_size : int, optional
            The number of samples to draw per multinomial sampling, by default 10000.
        n_simulations : int, optional
            The number of independent simulations to run, by default 100
        size : int, optional
            Number of multinomial experiments to perform. Default is 1.
        seed : int, optional
            Random seed for reproducibility, by default 42
        n_threads : Optional[int], optional
            The number of parallel threads to use. If None, will determine automatically.
        sample_all : bool, optional
            If True, sample all distributions either based on insert_counts or sample_size, by default False.
            If False, sample where insert_counts > sample_size.
        """
        # Determine thread count if not specified
        if n_threads is None:
            cpu_count = mp.cpu_count()
            if cpu_count >= 4:
                n_threads = 4
            elif cpu_count >= 2:
                print("Less than the optimal four threads available. Falling back to: 2 threads.")
                n_threads = 2
            else:
                n_threads = 1
                print("Only one thread available. MC downsampling will take some time.")

        self.n_threads = n_threads

        # Convert to numpy array if pandas Series
        if isinstance(insert_counts, pd.Series):
            insert_counts = insert_counts.values

        self.dists_arr = dists_arr
        self.insert_counts = insert_counts
        self.sample_size = sample_size
        self.n_simulations = n_simulations
        self.size = size
        self.seed = seed

        # Create seeds sequence
        # https://numpy.org/doc/2.2/reference/random/parallel.html#seedsequence-spawn
        seed_seq = np.random.SeedSequence(self.seed)
        # Spawn child seeds for the random generators
        self.child_seeds = seed_seq.spawn(n_simulations)

        # Sample all flag
        self.sample_all = sample_all

        # Create mask for samples needing subsampling
        if sample_all:
            # If sample_all is True, sample everything
            self.subsample_mask = insert_counts > 0
        else:
            if sample_size is None:
                # If true and not sample_all = True
                # Will return in sampler due to all False
                self.subsample_mask = np.zeros_like(insert_counts, dtype=bool)
            else:
                # Otherwise, sample where insert_counts > sample_size
                self.subsample_mask = insert_counts > sample_size

        # Initialize executor
        self.executor = concurrent.futures.ThreadPoolExecutor(n_threads)

        # Std collector
        self.std_dev = np.zeros_like(self.dists_arr, dtype=np.float64)

    @beartype
    def process_batch(self, batch_indices: npt.ArrayLike) -> Dict[np.int64, Tuple[npt.ArrayLike, npt.ArrayLike]]:
        """Process a batch of distribution indices."""

        results = {}

        for idx in batch_indices:
            dist = self.dists_arr[idx]
            total = dist.sum()
            if total <= 0:
                self.pbar.update(1)
                continue

            pvals = dist / total

            # Using Welford's online update for M1 (mean) and M2 (variance)
            # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
            num_bp = len(dist)

            M1s = np.zeros(num_bp, dtype=np.float64)
            M2s = np.zeros(num_bp, dtype=np.float64)
            N = 0

            # Create random generators for each simulation
            _random_generators = [default_rng(s) for s in self.child_seeds]

            # If sample_size is None use insert_size as sample size
            if self.sample_size is None:
                _sample_size = self.insert_counts[idx]
            else:
                # If sample size provided, use sample size
                _sample_size = self.sample_size

            # Iter over n = n_simulations random generator with n different seeds
            for rng in _random_generators:
                sample = rng.multinomial(_sample_size, pvals, self.size)

                # Iter over
                for smpl in sample:
                    N += 1
                    delta = smpl - M1s
                    M1s += delta / N
                    delta2 = smpl - M1s
                    M2s += delta * delta2

            M1s = np.round(M1s).astype(np.int64)

            if N > 1:
                M2s = M2s / (N - 1)
                std_devs = np.sqrt(M2s)
            else:
                # No variance, thus
                std_devs = np.zeros_like(M1s)

            # Store results
            results[idx] = (M1s, std_devs)

            self.pbar.update(1)

        return results

    @beartype
    def sample(self) -> Tuple[npt.ArrayLike, npt.ArrayLike]:
        """Perform multithreaded multinomial sampling."""

        # Early return if no subsampling needed
        if not np.any(self.subsample_mask):
            # Return zeros for std_dev since no sampling was done
            return self.dists_arr, self.std_dev

        # Get indices that need processing
        indices = np.where(self.subsample_mask)[0]

        # Process distributions in batches
        batch_size = max(1, len(indices) // self.n_threads)
        batches = [indices[i:i + batch_size] for i in range(0, len(indices), batch_size)]
        self.num_batches = len(batches)

        # Set up progress bar
        self.pbar = tqdm(
            total=len(indices),
            desc="Processing Samples"
        )

        futures = [self.executor.submit(self.process_batch, batch) for batch in batches]

        for future in concurrent.futures.as_completed(futures):
            # Collect results
            batch_results = future.result()

            # Fill dists_arr and std_dev array with samples mean and std
            for idx, (result, std) in batch_results.items():
                self.dists_arr[idx] = result
                self.std_dev[idx] = std

        self.pbar.close()

        return self.dists_arr, self.std_dev

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


# ///////////////////////////////////////// final wrapper \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

@beartype
def add_fld_metrics(adata: sc.AnnData,
                    fragments: Optional[str] = None,
                    barcode_col: Optional[str] = None,
                    barcode_tag: str = "CB",
                    chunk_size_bam: int = 1000000,
                    chunk_size_fragments: int = 5000000,
                    regions: Optional[str] = None,
                    peaks_thr: SupportsFloat = 0.5,
                    wavelength: int = 150,
                    sigma: float = 0.4,
                    plot: bool = True,
                    save_density: Optional[str] = None,
                    save_overview: Optional[str] = None,
                    sample: int = 0,
                    n_threads: int = 8,
                    colormap_density: str = 'jet',
                    sample_size: Optional[int] = 10000,
                    mc_seed: int = 42,
                    mc_samples: int = 1000,
                    return_distributions: bool = False) -> Optional[Tuple[pd.DataFrame, npt.ArrayLike]]:
    """
    Add insert size metrics to an AnnData object.

    This function can either take a bam file or a fragments file as input.
    If both are provided, an error is raised. If none are provided, an error is raised.
    Nucleosomal signal can either calculated using the momentum method (differential quotient) or
    the wavelet transformation based convolution method.

    Parameters
    ----------
    adata : sc.AnnData
        AnnData object to add the insert size metrics to.
    fragments : str, default None
        Path to fragments file.
    barcode_col : str, default None
        Name of the column in the adata.obs dataframe that contains the barcodes.
    barcode_tag : str, default 'CB'
        Name of the tag in the bam file that contains the barcodes.
    chunk_size_bam : int, default 1000000
        Chunksize for the bam file.
    chunk_size_fragments : int, default 5000000
        Chunksize for the fragments file.
    regions : str, default None
        Path to bed file containing regions to calculate insert size metrics for.
    peaks_thr : float, default 0.5
        Threshold for the convolution method.
    wavelength : int, default 150
        Wavelength for the convolution method.
    sigma : float, default 0.4
        Sigma for the convolution method.
    plot : bool, default True
        If true, plots are generated.
    save_density : str, default None
        If not None, the density plot is saved as a .png file.
    save_overview : str, default None
        If not None, the overview plot is saved as a .png file.
    sample : int, default 0
        Index of the sample to plot.
    n_threads : int, default 12
        Number of threads.
    colormap_density : str, default 'jet'
        Colormap for the density plot.
    sample_size : Optional[int], default=100,000
        Number of fragments to subsample for multinomial sampling. If None, all fragments are used.
    mc_seed : int, default=42
        Random seed for Monte Carlo sampling to ensure reproducibility.
    mc_samples : int, default=100
        Number of Monte Carlo simulations for subsampling.
    return_distributions : bool, default False
        If true, the fragment length distributions are returned.

    Returns
    -------
    Optional[Tuple[pd.DataFrame, npt.ArrayLike]]
        Dataframe with the insert size metrics and the fragment length distributions.

    Raises
    ------
    ValueError
        If bam and fragment parameter is not None.
    """
    if barcode_col:
        adata_barcodes = adata.obs[barcode_col].tolist()
    else:
        adata_barcodes = adata.obs.index.tolist()

    if fragments is None:
        raise ValueError("Please provide either a bam file or a fragments file.")

    # check if the input is a bam file or a fragments file
    bam = False
    bed = False

    if fragments.endswith("bam"):
        print("Using bam file...")
        bam = True
    else:
        print('Using fragments file...')
        bed = True

    # raise an error if the file ending is not correct
    if bam is False and bed is False:
        raise ValueError("Please provide either a bam file or a fragments file with the correct file ending.")

    if bam:
        count_table = insertsizes.insertsize_from_bam(bamfile=fragments,
                                                      barcodes=adata_barcodes,
                                                      barcode_tag=barcode_tag,
                                                      chunk_size=chunk_size_bam,
                                                      regions=regions)

    elif bed:
        count_table = insertsizes.insertsize_from_fragments(fragments=fragments,
                                                            barcodes=adata_barcodes,
                                                            chunk_size=chunk_size_fragments,
                                                            n_threads=8)

    # get the mean insert size and the insert size counts separately
    means = count_table.pop('mean_insertsize')
    insert_counts = count_table.pop('insertsize_count')

    # get the barcodes from the count_table, which are the index and will be used to match the barcodes of the adata
    barcodes = count_table.index
    # convert the count_table to an array with the dtype int64
    dists_arr = np.array(count_table['dist'].tolist(), dtype=np.int64)

    # Monte Carlo Multinomial Sampling (Optional)
    if sample_size is not None:
        sampler = MultithreadedMultinomialSampler(
            dists_arr,
            insert_counts,
            sample_size=sample_size,
            n_simulations=mc_samples,
            seed=mc_seed,
            n_threads=n_threads
        )
        dists_arr_subsampled, _ = sampler.sample()
    else:
        dists_arr_subsampled = dists_arr

    # plot the densityplot of the fragment length distribution
    if plot:
        print("plotting density...")
        density_plot(dists_arr_subsampled, max_abundance=600, save=save_density, colormap=colormap_density)

    # calculate scores using the convolution method
    print("calculating scores using the custom continues wavelet transformation...")
    conv_scores = score_by_conv(data=dists_arr_subsampled,
                                wavelength=wavelength,
                                sigma=sigma,
                                plot_wavl=plot,
                                n_threads=n_threads,
                                peaks_thr=peaks_thr,
                                operator='bigger',
                                plot_mask=plot,
                                plot_ov=plot,
                                save=save_overview,
                                sample=sample)

    # create a dataframe with the scores and match the barcodes
    inserts_df = pd.DataFrame(data={'fld_score': conv_scores,
                                    'mean_fragment_size': means,
                                    'n_fragments': insert_counts},
                              index=barcodes)

    # delete old columns to overwrite them
    columns_to_add = ['fld_score', 'mean_fragment_size', 'n_fragments']

    for column in columns_to_add:
        if column in adata.obs.columns:
            adata.obs.pop(column)
            print(f'overwriting: {column}')
        else:
            print(f'add new column: {column}')

    # join the dataframe with the adata
    adata.obs = adata.obs.join(inserts_df)

    # fill NaN values with 0 --> no peaks found
    adata.obs['fld_score'] = adata.obs['fld_score'].fillna(0)
    adata.obs['mean_fragment_size'] = adata.obs['mean_fragment_size'].fillna(0)
    adata.obs['n_fragments'] = adata.obs['n_fragments'].fillna(0)

    # return distributions if specified
    if return_distributions:
        inserts_df
        return inserts_df, dists_arr_subsampled
