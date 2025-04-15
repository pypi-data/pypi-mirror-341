#!/usr/bin/env python3
"""
TWSCA Demo Script

This script demonstrates the basic functionality of the Time-Warped Spectral
Correlation Analysis (TWSCA) package using synthetic sine wave data.
"""

import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# Add parent directory to path for local development
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import TWSCA
from analysis import compute_twsca


def generate_sine_waves(n_points=100, phase_shift=0, time_warp=False):
    """
    Generate synthetic sine wave data, optionally with time warping

    Parameters:
    -----------
    n_points : int
        Number of points in the time series
    phase_shift : float
        Phase shift between the two sine waves (in radians)
    time_warp : bool
        Whether to apply non-linear time warping to the second signal

    Returns:
    --------
    tuple
        (t, signal1, signal2) - time points and two signals
    """
    # Generate time points
    t = np.linspace(0, 10, n_points)

    # Generate first signal
    signal1 = np.sin(t)

    # Generate second signal (phase-shifted)
    if time_warp:
        # Apply non-linear time warping
        warp_factor = 1.5
        warped_t = t + 0.5 * np.sin(t * warp_factor)
        signal2 = np.sin(warped_t + phase_shift)
    else:
        signal2 = np.sin(t + phase_shift)

    return t, signal1, signal2


def plot_signals_and_analysis(
    t, signal1, signal2, twsca_result, title=None, output_file=None
):
    """
    Plot signals and TWSCA analysis results

    Parameters:
    -----------
    t : array-like
        Time points
    signal1 : array-like
        First signal
    signal2 : array-like
        Second signal
    twsca_result : dict
        Result from compute_twsca function
    title : str, optional
        Plot title
    output_file : str, optional
        File path to save the plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Plot original signals
    axes[0, 0].plot(t, signal1, label="Signal 1")
    axes[0, 0].plot(t, signal2, label="Signal 2")
    axes[0, 0].set_title("Original Signals")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Plot aligned signals
    aligned_t = np.arange(len(twsca_result["aligned_series1"]))
    axes[0, 1].plot(
        aligned_t, twsca_result["aligned_series1"], label="Signal 1 (aligned)"
    )
    axes[0, 1].plot(
        aligned_t, twsca_result["aligned_series2"], label="Signal 2 (aligned)"
    )
    axes[0, 1].set_title(
        f'Time-Warped Aligned Signals (Corr: {twsca_result["time_domain_correlation"]:.4f})'
    )
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Plot warping path
    if "warping_path" in twsca_result:
        warping_path = np.array(twsca_result["warping_path"])
        axes[1, 0].plot(warping_path[:, 0], warping_path[:, 1], "k-")
        axes[1, 0].set_title("DTW Warping Path")
        axes[1, 0].set_xlabel("Signal 1 Index")
        axes[1, 0].set_ylabel("Signal 2 Index")
        axes[1, 0].grid(True)

        # Add diagonal line for reference
        path_max = max(warping_path[:, 0].max(), warping_path[:, 1].max())
        axes[1, 0].plot(
            [0, path_max], [0, path_max], "r--", alpha=0.5, label="No warping"
        )
        axes[1, 0].legend()

    # Plot correlation scatter
    axes[1, 1].scatter(signal1, signal2, alpha=0.7, label="Original")
    axes[1, 1].scatter(
        twsca_result["aligned_series1"],
        twsca_result["aligned_series2"],
        alpha=0.7,
        label="After Time-Warping",
    )
    axes[1, 1].set_title(
        f'Correlation Scatter (Spectral: {twsca_result["spectral_correlation"]:.4f})'
    )
    axes[1, 1].grid(True)
    axes[1, 1].legend()

    # Set main title
    if title:
        plt.suptitle(title, fontsize=16)

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"Saved plot to {output_file}")

    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrate TWSCA with synthetic data"
    )
    parser.add_argument(
        "--points", type=int, default=100, help="Number of points in the time series"
    )
    parser.add_argument(
        "--phase",
        type=float,
        default=1.0,
        help="Phase shift between the two signals (in radians)",
    )
    parser.add_argument(
        "--warp",
        action="store_true",
        help="Apply non-linear time warping to the second signal",
    )
    parser.add_argument("--output", default=None, help="Output file to save the plot")

    args = parser.parse_args()

    print("Generating synthetic signals...")
    t, signal1, signal2 = generate_sine_waves(
        n_points=args.points, phase_shift=args.phase, time_warp=args.warp
    )

    print("Computing TWSCA...")
    twsca_result = compute_twsca(signal1, signal2)

    # Print results
    print("\nTWSCA Results:")
    print(
        f"Time-domain correlation (DTW): {twsca_result['time_domain_correlation']:.4f}"
    )
    print(f"Spectral correlation: {twsca_result['spectral_correlation']:.4f}")
    print(f"DTW distance: {twsca_result['dtw_distance']:.4f}")

    # Plot results
    title_suffix = "with Time Warping" if args.warp else "with Phase Shift"
    plot_signals_and_analysis(
        t,
        signal1,
        signal2,
        twsca_result,
        title=f"TWSCA Demo {title_suffix}",
        output_file=args.output,
    )

    print("\nInterpretation:")
    if twsca_result["spectral_correlation"] > 0.7:
        print("The signals show strong correlation after time-warping alignment!")
    else:
        print("The signals show limited correlation even after time-warping alignment.")


if __name__ == "__main__":
    main()
