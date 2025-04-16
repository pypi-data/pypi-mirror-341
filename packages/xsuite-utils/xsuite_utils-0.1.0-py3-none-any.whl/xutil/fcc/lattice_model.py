#!/usr/bin/env python3
"""
FCC-ee Lattice Model

This script constructs an FCC-ee lattice using MAD-X and Xsuite, configures various beam parameters,
and sets up the environment for particle tracking studies.

Key features:
- Loads lattice definition from MAD-X sequence files
- Configures reference particle parameters
- Sets up beam-beam interactions if enabled
- Configures injection parameters and bump
- Handles synchrotron radiation and emittance matching
- Saves final lattice configuration for tracking studies
"""

import sys
from pathlib import Path
import re
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from cpymad.madx import Madx
import xtrack as xt
import xobjects as xo
import xpart as xp
import xutil
import xutil.fcc.utils as fcc_utils

import logging
logger = logging.getLogger("xutil")
logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class TrackingDict(dict):
    """A dictionary subclass that triggers callbacks for all modifications, including nested dicts.
    
    Features:
    - Tracks all changes including nested dictionary updates
    - Automatically wraps nested dicts in TrackingDict
    - Handles update() and direct assignments
    - Preserves callback chain through nested structures
    """

    def __init__(self, name, *args, callback=None, **kwargs):
        """Initialize the TrackingDict with optional callback.
        
        Args:
            name: Identifier for this dictionary
            *args: Positional arguments passed to dict constructor
            callback: Function called when items are set (name, key, value) -> None
            **kwargs: Keyword arguments passed to dict constructor
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self._callback = callback
        
        # Convert any existing nested dicts to TrackingDicts
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, TrackingDict):
                super().__setitem__(key, TrackingDict(
                    name=key,
                    *args,
                    callback=self._callback,
                    **kwargs
                ))


    def __setitem__(self, key, value):
        """Set item, wrap nested dicts, and trigger callback.
        
        If value is a dict, triggers callbacks for each key-value pair separately.
        """
        # If assigning a dictionary, process each item individually
        if isinstance(value, dict) and not isinstance(value, TrackingDict):
            new_dict = TrackingDict(
                name=key,
                callback=self._callback
            )
            
            # Set each item individually to trigger callbacks
            for k, v in value.items():
                new_dict[k] = v
                
            super().__setitem__(key, new_dict)
        else:
            # Normal assignment for non-dict values
            super().__setitem__(key, value)
            
        # Trigger callback for the top-level assignment
        if self._callback:
            self._callback(self.name, key, value)


    def update(self, *args, **kwargs):
        """Override update to ensure all new values are properly tracked."""
        for k, v in dict(*args, **kwargs).items():
            self[k] = v  # Uses the __setitem__ definded above


    def __reduce__(self):
        """Support for proper pickling."""
        return (self.__class__, (self.name, dict(self), {'callback': self._callback}))


    def set_callback(self, callback):
        """Update the callback for this dictionary and all nested TrackingDicts."""
        self._callback = callback
        for value in self.values():
            if isinstance(value, TrackingDict):
                value.set_callback(callback)


class LatticeConfig():
    """
    Container for lattice configuration parameters.
    The parameters are intended to be saved as a yaml file.
    Everything here is basically dictionnaries of dictionnaries.
    """

    def __init__(
        self,
        optics_repository_path,
        operation_mode,
        particle,
        sequence_file,
        ref_params_name,
    ):
        # Basic lattice parameters
        aperture_dir = str(Path(optics_repository_path) / "aperture")
        reference_parameters_file = str(Path(optics_repository_path) / ref_params_name)

        # Initialize parameter dictionaries with TrackingDict, wrapping around a basic dict
        # Each will call self._parameter_updated when modified
        self._parameters = TrackingDict(name="parameters", callback=self._parameter_updated)
        self._parameters.update({
            category: TrackingDict(name=category, callback=self._parameter_updated)
                for category in [
                    "reference_parameters",
                    "beam_beam_parameters",
                    "injection_parameters",
                    "field_error_parameters",
                    "collimation_parameters",
                    "study_parameters",
                    "jobsubmission",
                ]
        })

        # Load reference parameters from file
        self._parameters["reference_parameters"] = fcc_utils.read_reference_parameters(
            reference_parameters_file, operation_mode
        )

        # Set particle properties
        pdg_id = xp.get_pdg_id_from_name(particle)
        pdg_atrr = xp.reference_from_pdg_id(pdg_id)
        particle_mass = pdg_atrr.mass0 
        particle_charge = pdg_atrr.charge[0]
        particle_classical_radius0 = pdg_atrr.get_classical_particle_radius0()
        gamma_relativistic = self._parameters['reference_parameters']['energy'] / particle_mass
        beta_relativistic = np.sqrt(1 - 1 / gamma_relativistic**2)
        emittance_x = self._parameters['reference_parameters']['emittance_x']
        emittance_y = self._parameters['reference_parameters']['emittance_y']

        # Update reference parameters
        self._parameters["reference_parameters"].update({
            "gamma_relativistic": gamma_relativistic,
            "beta_relativistic": beta_relativistic,
            "normalized_emittance_x": emittance_x * gamma_relativistic * beta_relativistic,
            "normalized_emittance_y": emittance_y * gamma_relativistic * beta_relativistic,
            "aperture_dir": aperture_dir,
            "optics_repository_path": optics_repository_path,
            "sequence_file_name": sequence_file,
            "particle": particle,
            "particle_charge": particle_charge,
            "particle_mass": particle_mass,
            "particle_classical_radius0": particle_classical_radius0,
            "crab_waist_sext_weight": None,
        })

    def _parameter_updated(self, category, key, new_val):
        """Internal handler for parameter updates.
        Used to check if parameters conflict upon update.

        Args:
            category: Which parameter category was modified
                     (e.g., "reference_parameters")
            key: key in the dictionnary that was changed
            new_val: new value of category[key]
        """
        logger.info(f"Parameter {key} in {category} updated: {new_val}")

        # If collisions is True, correctly set the energy_spread and bunch_length
        if category == "beam_beam_parameters" and key == "collisions" and new_val is True:
            energy_spread_bs = self.parameters["reference_parameters"]["energy_spread_BS"]
            self.parameters["reference_parameters"]["energy_spread"] = energy_spread_bs

            bunch_length_bs = self.parameters["reference_parameters"]["bunch_length_BS"]
            self.parameters["reference_parameters"]["bunch_length"] = bunch_length_bs

            logger.warning(
                "Collisions are set to True, the energy_spread and bunch_length have been updated"
            )

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        """Prevent direct replacement of the parameters dictionary.
        
        Raises:
            AttributeError: Always raised to enforce using individual parameter updates
        """
        raise AttributeError(
            "Direct assignment to parameters is not allowed.\n"
            "Modify individual parameter dictionaries instead.\n"
            "Example: config.parameters['reference_parameters'] = {'energy': 7000}"
        )

    def initialize_madx_with_beam_parameters(self) -> Madx:
        """
        Initialize MAD-X instance and configure basic beam parameters.

        Loads the specified lattice sequence and sets up the beam properties (particle type, energy,
        bunch characteristics) in MAD-X.

        Args:
            config (LatticeConfig): Lattice configuration object
        Returns:
            madx: cpymad.madx.Madx
                - Initialized MAD-X instance with beam parameters configured

        Note:
            Modifies the input config object by setting the sequence_name attribute.
        """
        madx = Madx()

        # Get some parameters from the reference
        params = self.parameters["reference_parameters"]
        operation_mode = params["operation_mode"]
        sequence_file = params["sequence_file_name"]
        optics_repository = params["optics_repository_path"]
        particle = params["particle"]

        # Load sequence file
        seq_path = f"{optics_repository}/lattices/{operation_mode}/{sequence_file}"
        madx.call(seq_path)

        # Get sequence name (first key in sequence dictionary)
        sequence_name = list(madx.sequence.keys())[0]

        madx.input(
            f"""
            beam, particle={particle}, 
            sequence={sequence_name},  
            energy:={params['energy'] / 1e9}, 
            NPART:={params['bunch_population']},  
            ex:={params['emittance_x']}, 
            ey:={params['emittance_y']},  
            sige:={params['energy_spread']}, 
            sigt:={params['bunch_length']}
        """
        )

        # Use the sequence and add its name to the configuration
        madx.use(sequence=sequence_name)
        params["sequence_name"] = sequence_name

        return madx

    def load_madx_to_xsuite(self, madx: Madx) -> xt.Line:
        """
        Convert a MAD-X sequence to an XSuite line with proper reference particle configuration.

        Args:
            madx (cpymad.madx.Madx): Initialized MAD-X instance containing the sequence
            config (LatticeConfig): Lattice configuration object

        Returns:
            xt.Line: Configured XSuite line
        """
        # Convert MAD-X sequence to XSuite line
        line = xt.Line.from_madx_sequence(
            sequence=madx.sequence[
                self.parameters["reference_parameters"]["sequence_name"]
            ],
            allow_thick=True,
            enable_align_errors=True,
            deferred_expressions=True,
            install_apertures=self.parameters["collimation_parameters"][
                "collimators_on"
            ],
        )
        line.config.XTRACK_USE_EXACT_DRIFTS = True

        # Configure reference particle
        beam_params = self.parameters["reference_parameters"]
        line.particle_ref = xt.Particles(
            mass0=beam_params["particle_mass"],
            q0=beam_params["particle_charge"],
            gamma0=beam_params["gamma_relativistic"],
        )

        return line

    def save_configuration_and_line(self, line, line_name=None, param_name=None):
        """
        Save the lattice configuration and line to files

        Args:
            config (LatticeConfig): Configuration objecS
            line (xt.Line): Constructed lattice line
        """
        # Generate file names
        name_parts = [
            self.parameters["reference_parameters"]["sequence_name"],
            self.parameters["reference_parameters"]["operation_mode"],
            self.parameters["study_parameters"]["study_name"],
        ]

        # Save line to JSON
        if line_name is None:
            line_name = f"line_{'_'.join(str(p) for p in name_parts[:-1] if p)}.json"
        line.to_json(line_name)

        # Save configuration to YAML
        if param_name is None:
            param_name = (
                f"configuration_{'_'.join(str(p) for p in name_parts if p)}.yaml"
            )

        self.parameters["reference_parameters"]["line_name"] = line_name
        self.parameters["reference_parameters"]["configuration_name"] = param_name
        xutil.save_config_file(file_name=param_name, dict_to_save=self.parameters)
