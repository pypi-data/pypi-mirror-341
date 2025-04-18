"""
Parse Wannier90 output files.

This module implements several parsing functions for reading Wannier90 output files.
The :py:func:`~pengwann.io.read` function is a convenient wrapper for automatically
parsing all the data required to construct an instance of the
:py:class:`~pengwann.descriptors.DescriptorCalculator` class.
"""

# Copyright (C) 2024-2025 Patrick J. Taylor

# This file is part of pengWann.
#
# pengWann is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pengWann is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with pengWann.
# If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import os

import numpy as np
from numpy.typing import NDArray


def read(
    seedname: str, path: str = "."
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.complex128],
    dict[tuple[int, int, int], NDArray[np.complex128]],
]:
    """
    Wrapper function for parsing various Wannier90 output files.

    In total, this function will parse:

    - seedname.eig
    - seedname_u.mat
    - seedname_u_dis.mat (if disentanglement was used)
    - seedname_hr.dat

    Parameters
    ----------
    seedname : str
        The seedname (prefix for all output files) chosen in the prior Wannier90
        calculation.
    path : str, optional
        Filepath to the Wannier90 output files. Defaults to '.' i.e. the current
        working directory.

    Returns
    -------
    kpoints : ndarray of float
        The k-point mesh used in the ab-initio calculation.
    eigenvalues : ndarray of float
        The Kohn-Sham eigenvalues.
    u : ndarray of complex
        The unitary matrices U^k that define the Wannier functions in terms of the
        canonical Bloch states.
    h : dict of {3-length tuple of int : ndarray of complex} pairs.
        The Hamiltonian in the Wannier basis.

    See Also
    --------
    read_eigenvalues
    read_u
    read_hamiltonian
    """
    u, kpoints = read_u(f"{path}/{seedname}_u.mat")
    if os.path.isfile(f"{path}/{seedname}_u_dis.mat"):
        u_dis, _ = read_u(f"{path}/{seedname}_u_dis.mat")
        u = u_dis @ u

    h = read_hamiltonian(f"{path}/{seedname}_hr.dat")
    eigenvalues = read_eigenvalues(f"{path}/{seedname}.eig", u.shape[1], u.shape[0])

    return kpoints, eigenvalues, u, h


def read_eigenvalues(
    path: str,
    num_bands: int,
    num_kpoints: int,
) -> NDArray[np.float64]:
    """
    Parse the Kohn-Sham eigenvalues from a Wannier90 .eig file.

    Parameters
    ----------
    path : str
        The filepath to seedname.eig.
    num_bands : int
        The number of bands used in the prior Wannier90 calculation.
    num_kpoints : int
        The number of k-points used in the prior Wanner90 calculation.

    Returns
    -------
    eigenvalues : ndarray of float
        The Kohn-Sham eigenvalues.
    """
    with open(path, "r") as stream:
        lines = stream.readlines()

    eigenvalues = np.zeros((num_bands, num_kpoints))

    n_lines = range(num_bands)
    k_lines = [idx * num_bands for idx in range(num_kpoints)]

    for n, n_line in enumerate(n_lines):
        for k, k_line in enumerate(k_lines):
            eigenvalue = float(lines[n_line + k_line].split()[-1])

            eigenvalues[n, k] = eigenvalue

    return eigenvalues


def read_u(path: str) -> tuple[NDArray[np.complex128], NDArray[np.float64]]:
    """
    Parse the unitary matrices U^k from a Wannier90 _u.mat file.

    Parameters
    ----------
    path : str
        The filepath to seedname_u.mat or seedname_u_dis.mat.

    Returns
    -------
    u : ndarray of complex
        The unitary matrices U^k.
    kpoints : ndarray of float
        The k-point mesh used in the prior Wannier90 calculation.
    """
    with open(path, "r") as stream:
        lines = stream.readlines()

    num_kpoints, num_wann, num_bands = [int(string) for string in lines[1].split()]

    u = np.zeros((num_kpoints, num_bands, num_wann), dtype=np.complex128)
    kpoints = np.zeros((num_kpoints, 3))

    k_lines = (idx * (num_wann * num_bands + 2) + 4 for idx in range(num_kpoints))
    n_lines = [idx for idx in range(num_bands)]
    w_lines = [idx * num_bands for idx in range(num_wann)]

    for k, k_line in enumerate(k_lines):
        kpoints[k] = [float(string) for string in lines[k_line - 1].split()]

        for n, n_line in enumerate(n_lines):
            for w, w_line in enumerate(w_lines):
                real, imaginary = [
                    float(string) for string in lines[k_line + n_line + w_line].split()
                ]

                u[k, n, w] = complex(real, imaginary)

    return u, kpoints


def read_hamiltonian(path: str) -> dict[tuple[int, int, int], NDArray[np.complex128]]:
    """
    Parse the Wannier Hamiltonian from a Wannier90 seedname_hr.dat file.

    Parameters
    ----------
    path : str
        The filepath to seedname_hr.dat.

    Returns
    -------
    h : dict of {3-length tuple of int : ndarray of complex} pairs.
        The Wannier Hamiltonian.
    """
    with open(path, "r") as stream:
        lines = stream.readlines()

    num_wann = int(lines[1])
    num_rpoints = int(lines[2])

    start_idx = int(np.ceil(num_rpoints / 15)) + 3

    h: dict[tuple[int, int, int], NDArray[np.complex128]] = {}

    for line in lines[start_idx:]:
        data = line.split()
        bl = tuple([int(string) for string in data[:3]])

        assert len(bl) == 3

        if bl not in h.keys():
            h[bl] = np.zeros((num_wann, num_wann), dtype=np.complex128)

        m, n = [int(string) - 1 for string in data[3:5]]
        real, imaginary = [float(string) for string in data[5:]]

        h[bl][m, n] = complex(real, imaginary)

    return h


def read_xyz(path: str) -> tuple[list[str], NDArray[np.float64]]:
    """
    Parse the symbols and coordinates from a Wannier90 seedname_centres.xyz file.

    Parameters
    ----------
    path : str
        The filepath to seedname_centres.xyz

    Returns
    -------
    symbols : list of str
        The elemental symbol for each Wannier centre or atom in the xyz file.

    coords : list of tuple of float
        The cartesian coordinates for each Wannier centre or atom in the xyz file.
    """
    with open(path, "r") as stream:
        lines = stream.readlines()

    start_idx = 2

    symbols: list[str] = []
    coords_list: list[tuple[float, float, float]] = []
    for line in lines[start_idx:]:
        data = line.split()

        symbol = str(data[0]).capitalize()
        coords = tuple(float(coord) for coord in data[1:])

        assert len(coords) == 3

        symbols.append(symbol)
        coords_list.append(coords)

    coords = np.array(coords_list, dtype=np.float64).T

    return symbols, coords


def read_cell(path: str) -> NDArray[np.float64]:
    """
    Parse a Wannier90 seedname.wout file to extract the cell vectors.

    Parameters
    ----------
    path : str
        The filepath to seedname.wout.

    Returns
    -------
    cell : ndarray of float
        The cell vectors.
    """
    with open(path, "r") as stream:
        lines = stream.readlines()

    cell_list: list[list[float]] = []
    for idx, line in enumerate(lines):
        if "Lattice Vectors (Ang)" in line:
            for cell_line in lines[idx + 1 : idx + 4]:
                cell_vector = [float(component) for component in cell_line.split()[1:]]

                cell_list.append(cell_vector)

            break

    cell = np.array(cell_list, dtype=np.float64)

    return cell
