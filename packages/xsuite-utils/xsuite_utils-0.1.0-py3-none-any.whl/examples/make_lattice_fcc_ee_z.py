from xutil.fcc.lattice_model import (
    LatticeConfig,
)
import xutil
import xutil.fcc as fcc_utils  # FCC specific functions
import numpy as np
import xobjects as xo


def define_user_parameters() -> LatticeConfig:
    """
    User defined parameters to build the lattice.

    Returns
        config (LatticeConfig): Configuration of the lattice with user-defined parameters relevant
                                to beambeam, injection, collimation, study, etc.
    """
    # Initialize LatticeConfig with the reference parameters
    optics_repository_path = "fcc-ee-lattice-V25_GHC"
    operation_mode = "z"
    particle = "positron"
    sequence_file = "FCCee_z_624_nosol_9.seq"
    ref_params_name = "reference_parameters_oide_feb_12.json"
    config = LatticeConfig(
        optics_repository_path, operation_mode, particle, sequence_file, ref_params_name
    )

    # Lattice type, unused at the moment
    if "GHC" in optics_repository_path:
        optics_type = "GHC"
    elif "LCC" in optics_repository_path:
        optics_type = "LCC"

    # Retrieve them for later
    reference_parameters = config.parameters["reference_parameters"]

    # Sextupoles crabing, max is 1
    config.parameters["reference_parameters"]["crab_waist_sext_weight"] = None

    # Beam-beam parameters
    # Conflicts are automatically checked to update bunch spread
    config.parameters["beam_beam_parameters"] = {
        "collisions": True,
        "half_xing_angle": 15 * 1e-3,  # half-crossing angle in radians
        "xing_plane": 0,  # 0: horizontal plane
        "num_slices": 200,
        "beamstrahlung_on": True,
        "binning_mode": "unicharge",
    }

    # Injection parameters
    config.parameters["injection_parameters"] = {
        "injection_marker_name": "finj.4",
        "energy_offset": 0.95e-2,  # 0.85E-2  #0.95E-2
        "x_offset": 0,  # 1.5E-3 # 0 # meters
        "energy_spread": 0.38e-3,
        "bunch_length": 4.43e-3,
        "emittance_x": 0.12e-9,  # meters
        "emittance_y": 10e-12,  # meters
        "septum_thickness": 2.8e-3,
        "bump_risefall_time": 600 * 1e-9,  # seconds
        "bump_flattop_time": 301.2
        * 1e-6,  # seconds, not the desighn value but slightly lower so to keep the bump on for only one turn
        "rms_orbit_bump_height": 10,
        "orbit_bump_phase_advance": 0.5,  # in [2π] units
    }

    # Calculate normalized emittances
    gamma = reference_parameters["gamma_relativistic"]
    beta = reference_parameters["beta_relativistic"]
    injection_parameters = config.parameters["injection_parameters"]
    config.parameters["injection_parameters"].update(
        {
            "normalized_emittance_x": injection_parameters["emittance_x"]
            * gamma
            * beta,
            "normalized_emittance_y": injection_parameters["emittance_y"]
            * gamma
            * beta,
        }
    )

    # Field error parameters
    config.parameters["field_error_parameters"] = {
        "include_field_error": False,
        "error_element_familys": [
            "b1.*"
        ],  # ['Bend', 'Quadrupole', 'sy.*', 'b1.*','qd1.*','qf2.*','qd3.*','qf4.*']
        "error_class": "random",  # 'random' or 'systematic'
        "error_type": "b3",
        "error_category": "relative",
        "error_seed": [1, 2],  # or the values in rad1 can be used
        "error_strengths": np.array([0.05, 0.1])
        * 1e-4,  # or the values in rad2 can be used
        "error_reference_radius": 1e-2,
    }

    # Collimation parameters
    config.parameters["collimation_parameters"] = {
        "collimators_on": False,
        "collimator_file": "CollDB_FCCee_z_V25.1_GHC_TCT_at_TCS_settings_SEPTUM.json",
        "bdsim_config": "settings.gmad",
        "weights": "energy",
        "inv2": 1993,
        "aperture_interp": 0.03,
        "aperture_binwidth": 10,
    }

    # Study parameters
    config.parameters["study_parameters"] = {
        "study_name": "test_study",
        "ini_cond_type": "distribution_matched",  # grid_DA, grid_MA, distribution_matched, distribution_injected
        "output_dir": "out",
        "number_of_turns": 100,
        "number_particles": 500,
        "inv1": config.parameters["field_error_parameters"][
            "error_seed"
        ],  # np.arange(2)+1,
        "inv2": config.parameters["field_error_parameters"][
            "error_strengths"
        ],  # np.arange(2,2+3)+1,
        "start_element": injection_parameters["injection_marker_name"],  # ca1.1
        "ini_cond_nemittance_x": injection_parameters["normalized_emittance_x"],
        "ini_cond_nemittance_y": injection_parameters["normalized_emittance_y"],
        "ini_cond_bunch_length": injection_parameters["bunch_length"],
        "ini_cond_energy_spread": injection_parameters["energy_spread"],
        "ini_cond_energy_offset": injection_parameters["energy_offset"],
    }

    # Job submission parameters
    num_inv1 = np.size(config.parameters["study_parameters"]["inv1"])
    num_inv2 = np.size(config.parameters["study_parameters"]["inv2"])
    config.parameters["jobsubmission"] = {
        "working_directory": "b1_ferror_injection_beambeam",
        "run_local": False,
        "dryrun": False,
        "jobflavour": "workday",  # 'tomorrow'
        "htc_arguments": {
            "accounting_group": "group_u_BE.ABP.normal",
            "notification": "never",
        },
        "mask": "mask_jobsubmission.sh",
        "num_jobs": num_inv1 * num_inv2,
        "job_output_dir": config.parameters["study_parameters"]["output_dir"],
    }
    # Create the bash script
    xutil.generate_bash_script(input_file="examples/run_tracking.py")

    return config


def build_user_lattice(config):
    """
    User-defined construction of the lattice.

    Args:
        config (LatticeConfig): Configuration object containing all parameters

    Returns:
        tuple: (xt.Line, dict) The constructed lattice line and twiss parameters
    """
    # Create the MAD-X instance with our parameters
    madx = config.initialize_madx_with_beam_parameters()

    # Get some parameters
    beam_params = config.parameters["reference_parameters"]
    sequence_name = beam_params["sequence_name"]
    aperture_dir = beam_params["aperture_dir"]

    # Set brho
    config.parameters["reference_parameters"]["brho"] = madx.sequence[
        sequence_name
    ].beam.brho

    # Install wigglers
    fcc_utils.madx_add_fccee_wigglers(madx, sequence_name=sequence_name)

    if config.parameters["collimation_parameters"]["collimators_on"]:
        xutil.madx_add_collimators(madx, aperture_dir, sequence_name=sequence_name)
        fcc_utils.madx_add_apertures(madx, aperture_dir, sequence_name=sequence_name)

    # Load the line via MAD-X an convert it to XSuite
    line = config.load_madx_to_xsuite(madx)

    # Create the context
    context = xo.ContextCpu()
    line.build_tracker(_context=context)

    # Get initial table and twiss
    tt0 = line.get_table(attr=True)
    tw4d = line.twiss4d()

    # Scale crab waist/chroma sextupoles
    # No rematch is performed because will be done in the following make thin
    if config.parameters["reference_parameters"]["crab_waist_sext_weight"] is not None:
        line.vars["cw.sext.weight"] = config.parameters["reference_parameters"][
            "crab_waist_sext_weight"
        ]
        line.vars["k2sy2l"] = line.vars["cw.sext.weight"] * line.vv["k2sy1l"]
        line.vars["k2sy2r"] = line.vars["cw.sext.weight"] * line.vv["k2sy1r"]

    # Set wigglers
    wigs = tt0.rows[tt0.rows.mask["mwi.*"] & (tt0.element_type == "Bend")].name
    for nn in wigs:
        line.element_refs[nn].rot_s_rad = np.pi / 2

    # Add linear chroma knob at every arc focusing and defocusing sext
    line.vars["sf.k2n.chroma.knob"] = 1
    for ii in tt0.rows["sf.*"].name:
        if "_aper" not in ii:
            line.element_refs[ii].k2 = (
                line.vars["sf.k2n.chroma.knob"] * line.element_refs[ii].k2._expr
            )

    line.vars["sd.k2n.chroma.knob"] = 1
    for ii in tt0.rows["sd.*"].name:
        if "_aper" not in ii:
            line.element_refs[ii].k2 = (
                line.vars["sd.k2n.chroma.knob"] * line.element_refs[ii].k2._expr
            )

    # Add Beam Beam elements at the IPs if collisions id True
    if config.parameters["beam_beam_parameters"]["collisions"]:
        bb_elem_name = xutil.install_beam_beam_elements(
            line,
            config.parameters["reference_parameters"]["normalized_emittance_x"],
            config.parameters["reference_parameters"]["normalized_emittance_y"],
            config.parameters["reference_parameters"]["bunch_length"],
            config.parameters["reference_parameters"]["bunch_population"],
            config.parameters["beam_beam_parameters"]["half_xing_angle"],
            config.parameters["beam_beam_parameters"]["xing_plane"],
            config.parameters["beam_beam_parameters"]["beamstrahlung_on"],
            config.parameters["beam_beam_parameters"]["num_slices"],
            config.parameters["beam_beam_parameters"]["binning_mode"],
        )

    # Add kikers for injection bump
    injection_bump_height = -(
        config.parameters["injection_parameters"]["rms_orbit_bump_height"]
        * np.sqrt(
            config.parameters["injection_parameters"]["emittance_x"]
            * tw4d.rows[
                config.parameters["injection_parameters"]["injection_marker_name"]
            ].betx
        )
        + config.parameters["injection_parameters"]["septum_thickness"]
        + tw4d.rows[
            config.parameters["injection_parameters"]["injection_marker_name"]
        ].x[0]
    )[0]

    xutil.install_two_kick_injection_bump(
        line,
        config.parameters["injection_parameters"]["injection_marker_name"],
        injection_bump_height,
    )

    # Set integrator
    if config.parameters["collimation_parameters"]["collimators_on"]:
        line_thin = line.copy(shallow=True)
        xutil.make_thin_and_rematch(line_thin, tw4d)
        # Perform aperture check in thin lattice to be sure all elements have their aperture
        # Not using thick lattice because it looks for upstream and downstream apertures but we install only one
        # If aperture are missing their are assigned using an intepolation of the known once
        xutil.check_and_insert_aperture(line, line_thin)
        line = line_thin
        line.build_tracker(_context=context)
    else:
        xutil.set_integrator(line)

    # Enable synchrotron radiation
    line.configure_radiation(model="mean")
    line.compensate_radiation_energy_loss()

    # Rematch the working point and chroma after the SR compensation and teapering
    fcc_utils.match_wiggler_for_eq_emitt(
        line, target_eq_em_y=config.parameters["reference_parameters"]["emittance_y"]
    )
    xutil.match_tune_chroma(line, tw4d)

    # Compensate synchrotron radiation after matching
    # Tapering is not needed again
    line.compensate_radiation_energy_loss()

    # Compute lattice functions with rf and synchrotron radiation
    tw = line.twiss(eneloss_and_damping=True)

    return line, tw


# Update the config with the user-defined parameters
config = define_user_parameters()

# Build lattice
line, twiss = build_user_lattice(config)

# Save configuration and line
config.save_configuration_and_line(line)

print("Lattice construction completed successfully.")