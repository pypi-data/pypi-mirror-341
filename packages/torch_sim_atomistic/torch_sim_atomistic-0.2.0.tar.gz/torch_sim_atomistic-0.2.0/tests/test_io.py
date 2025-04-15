import itertools
from typing import Any

import pytest
import torch
from ase import Atoms
from phonopy.structure.atoms import PhonopyAtoms
from pymatgen.core import Structure

from torch_sim.io import (
    atoms_to_state,
    phonopy_to_state,
    state_to_atoms,
    state_to_phonopy,
    state_to_structures,
    structures_to_state,
)
from torch_sim.state import SimState


def test_single_structure_to_state(si_structure: Structure, device: torch.device) -> None:
    """Test conversion from pymatgen Structure to state tensors."""
    state = structures_to_state(si_structure, device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert all(
        t.device.type == device.type for t in [state.positions, state.masses, state.cell]
    )
    assert all(
        t.dtype == torch.float64 for t in [state.positions, state.masses, state.cell]
    )
    assert state.atomic_numbers.dtype == torch.int

    # Check shapes and values
    assert state.positions.shape == (8, 3)
    assert torch.allclose(state.masses, torch.full_like(state.masses, 28.0855))  # Si
    assert torch.all(state.atomic_numbers == 14)  # Si atomic number
    assert torch.allclose(
        state.cell,
        torch.diag(torch.full((3,), 5.43, device=device, dtype=torch.float64)),
    )


def test_multiple_structures_to_state(
    si_structure: Structure, device: torch.device
) -> None:
    """Test conversion from list of pymatgen Structure to state tensors."""
    state = structures_to_state([si_structure, si_structure], device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert state.positions.shape == (16, 3)
    assert state.masses.shape == (16,)
    assert state.cell.shape == (2, 3, 3)
    assert state.pbc
    assert state.atomic_numbers.shape == (16,)
    assert state.batch.shape == (16,)
    assert torch.all(
        state.batch == torch.repeat_interleave(torch.tensor([0, 1], device=device), 8)
    )


def test_single_atoms_to_state(si_atoms: Atoms, device: torch.device) -> None:
    """Test conversion from ASE Atoms to state tensors."""
    state = atoms_to_state(si_atoms, device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert state.positions.shape == (8, 3)
    assert state.masses.shape == (8,)
    assert state.cell.shape == (1, 3, 3)
    assert state.pbc
    assert state.atomic_numbers.shape == (8,)
    assert state.batch.shape == (8,)
    assert torch.all(state.batch == 0)


def test_multiple_atoms_to_state(si_atoms: Atoms, device: torch.device) -> None:
    """Test conversion from ASE Atoms to state tensors."""
    state = atoms_to_state([si_atoms, si_atoms], device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert state.positions.shape == (16, 3)
    assert state.masses.shape == (16,)
    assert state.cell.shape == (2, 3, 3)
    assert state.pbc
    assert state.atomic_numbers.shape == (16,)
    assert state.batch.shape == (16,)
    assert torch.all(
        state.batch == torch.repeat_interleave(torch.tensor([0, 1], device=device), 8),
    )


def test_state_to_structure(ar_supercell_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of pymatgen Structure."""
    structures = state_to_structures(ar_supercell_sim_state)
    assert len(structures) == 1
    assert isinstance(structures[0], Structure)
    assert len(structures[0]) == 32


def test_state_to_multiple_structures(ar_double_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of pymatgen Structure."""
    structures = state_to_structures(ar_double_sim_state)
    assert len(structures) == 2
    assert isinstance(structures[0], Structure)
    assert isinstance(structures[1], Structure)
    assert len(structures[0]) == 32
    assert len(structures[1]) == 32


def test_state_to_atoms(ar_supercell_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of ASE Atoms."""
    atoms = state_to_atoms(ar_supercell_sim_state)
    assert len(atoms) == 1
    assert isinstance(atoms[0], Atoms)
    assert len(atoms[0]) == 32


def test_state_to_multiple_atoms(ar_double_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of ASE Atoms."""
    atoms = state_to_atoms(ar_double_sim_state)
    assert len(atoms) == 2
    assert isinstance(atoms[0], Atoms)
    assert isinstance(atoms[1], Atoms)
    assert len(atoms[0]) == 32
    assert len(atoms[1]) == 32


def test_to_atoms(ar_supercell_sim_state: SimState) -> None:
    """Test conversion from SimState to list of ASE Atoms."""
    atoms = state_to_atoms(ar_supercell_sim_state)
    assert isinstance(atoms[0], Atoms)


def test_to_structures(ar_supercell_sim_state: SimState) -> None:
    """Test conversion from SimState to list of Pymatgen Structure."""
    structures = state_to_structures(ar_supercell_sim_state)
    assert isinstance(structures[0], Structure)


def test_single_phonopy_to_state(si_phonopy_atoms: Any, device: torch.device) -> None:
    """Test conversion from PhonopyAtoms to state tensors."""
    state = phonopy_to_state(si_phonopy_atoms, device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert all(
        t.device.type == device.type for t in [state.positions, state.masses, state.cell]
    )
    assert all(
        t.dtype == torch.float64 for t in [state.positions, state.masses, state.cell]
    )
    assert state.atomic_numbers.dtype == torch.int

    # Check shapes and values
    assert state.positions.shape == (8, 3)
    assert torch.allclose(state.masses, torch.full_like(state.masses, 28.0855))  # Si
    assert torch.all(state.atomic_numbers == 14)  # Si atomic number
    assert torch.allclose(
        state.cell,
        torch.diag(torch.full((3,), 5.43, device=device, dtype=torch.float64)),
    )


def test_multiple_phonopy_to_state(si_phonopy_atoms: Any, device: torch.device) -> None:
    """Test conversion from multiple PhonopyAtoms to state tensors."""
    state = phonopy_to_state([si_phonopy_atoms, si_phonopy_atoms], device, torch.float64)

    # Check basic properties
    assert isinstance(state, SimState)
    assert state.positions.shape == (16, 3)
    assert state.masses.shape == (16,)
    assert state.cell.shape == (2, 3, 3)
    assert state.pbc
    assert state.atomic_numbers.shape == (16,)
    assert state.batch.shape == (16,)
    assert torch.all(
        state.batch == torch.repeat_interleave(torch.tensor([0, 1], device=device), 8),
    )


def test_state_to_phonopy(ar_supercell_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of PhonopyAtoms."""
    phonopy_atoms = state_to_phonopy(ar_supercell_sim_state)
    assert len(phonopy_atoms) == 1
    assert isinstance(phonopy_atoms[0], PhonopyAtoms)
    assert len(phonopy_atoms[0]) == 32


def test_state_to_multiple_phonopy(ar_double_sim_state: SimState) -> None:
    """Test conversion from state tensors to list of PhonopyAtoms."""
    phonopy_atoms = state_to_phonopy(ar_double_sim_state)
    assert len(phonopy_atoms) == 2
    assert isinstance(phonopy_atoms[0], PhonopyAtoms)
    assert isinstance(phonopy_atoms[1], PhonopyAtoms)
    assert len(phonopy_atoms[0]) == 32
    assert len(phonopy_atoms[1]) == 32


@pytest.mark.parametrize(
    ("sim_state_name", "conversion_functions"),
    list(
        itertools.product(
            [
                "ar_supercell_sim_state",
                "si_sim_state",
                "ti_sim_state",
                "sio2_sim_state",
                "fe_supercell_sim_state",
                "cu_sim_state",
                "ar_double_sim_state",
                "mixed_double_sim_state",
                # TODO: round trip benzene/non-pbc systems
            ],
            [
                (state_to_atoms, atoms_to_state),
                (state_to_structures, structures_to_state),
                (state_to_phonopy, phonopy_to_state),
            ],
        )
    ),
)
def test_state_round_trip(
    sim_state_name: str,
    conversion_functions: tuple,
    request: pytest.FixtureRequest,
    device: torch.device,
    dtype: torch.dtype,
) -> None:
    """Test round-trip conversion from SimState through various formats and back.

    Args:
        sim_state_name: Name of the sim_state fixture to test
        conversion_functions: Tuple of (to_format, from_format) conversion functions
        request: Pytest fixture request object to get dynamic fixtures
        device: Device to run tests on
        dtype: Data type to use
    """
    # Get the sim_state fixture dynamically using the name
    sim_state: SimState = request.getfixturevalue(sim_state_name)
    to_format_fn, from_format_fn = conversion_functions
    unique_batches = torch.unique(sim_state.batch)

    # Convert to intermediate format
    intermediate_format = to_format_fn(sim_state)
    assert len(intermediate_format) == len(unique_batches)

    # Convert back to state
    round_trip_state: SimState = from_format_fn(intermediate_format, device, dtype)

    # Check that all properties match
    assert torch.allclose(sim_state.positions, round_trip_state.positions)
    assert torch.allclose(sim_state.cell, round_trip_state.cell)
    assert torch.all(sim_state.atomic_numbers == round_trip_state.atomic_numbers)
    assert torch.all(sim_state.batch == round_trip_state.batch)
    assert sim_state.pbc == round_trip_state.pbc

    if isinstance(intermediate_format[0], Atoms):
        # TODO: the round trip for pmg and phonopy masses is not exact.
        assert torch.allclose(sim_state.masses, round_trip_state.masses)
