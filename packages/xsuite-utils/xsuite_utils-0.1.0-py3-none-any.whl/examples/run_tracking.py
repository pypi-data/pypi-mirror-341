import os
import time
import argparse
import numpy as np
import xpart as xp
import xtrack as xt
import xcoll as xc
import xobjects as xo
import xutil
import xutil.fcc as fcc_utils


def main(
    config_file="configuration_l000017_z_distribution_matched.yaml",
    submit="False",
    merge="False",
):
    start_time = time.time()
    ####### call/set config parameters #######
    parameters = xutil.load_config_file(config_file)

    ref_param = parameters["reference_parameters"]
    beambeam_param = parameters["beam_beam_parameters"]
    study_param = parameters["study_parameters"]
    inject_param = parameters["injection_parameters"]
    field_err_param = parameters["field_error_parameters"]

    output_dir = study_param["output_dir"]
    if submit:
        # submit to htcondor
        xutil.submit_jobs(parameters, config_file)
    elif merge:
        working_directory = parameters["jobsubmission"]["working_directory"]
        job_output_dir = parameters["jobsubmission"]["job_output_dir"]
        match_pattern = "*part.hdf*"
        output_file = os.path.join(working_directory, "part_merged.hdf")
        xutil.load_output(
            working_directory,
            job_output_dir,
            output_file,
            match_pattern=match_pattern,
            load_particles=True,
        )
    else:
        os.makedirs(output_dir, exist_ok=True)

        ######################
        ####### xsuite #######
        ######################

        ## Load line from json
        line = xt.Line.from_json(ref_param["line_name"])
        line.config.XTRACK_USE_EXACT_DRIFTS = True

        ## Choose a context
        context = xo.ContextCpu()  # For CPU
        context_tracking = xo.ContextCpu(
            omp_num_threads="auto"
        )  # For CPU with activate multi-core CPU parallelization

        ## Transfer lattice on context and compile tracking code
        line.build_tracker(_context=context)

        # Cycle the line now to have the correct initialitation of the beam
        line.cycle(name_first_element=study_param["start_element"], inplace=True)

        ## Input lattice, table and survey
        tab = line.get_table(attr=True)

        # turn off beam-beam
        if beambeam_param["collisions"]:
            bb_elem_name = tab.rows[tab.element_type == "BeamBeamBiGaussian3D"].name
            for jj in bb_elem_name:
                line[jj].scale_strength = 0
                # line.get(jj).iscollective = True

        ## Enable synchrotron radiation
        # we choose the `mean` mode in which the mean power loss is applied without
        # stochastic fluctuations (quantum excitation).
        line.configure_radiation(model="mean")

        ## Add field errors
        tw = line.twiss(eneloss_and_damping=True)
        if field_err_param["include_field_error"]:
            xutil.add_field_error(
                line,
                field_err_param["error_element_familys"],
                error_class=field_err_param["error_class"],
                seed=study_param["inv1"],
                error_type=field_err_param["error_type"],
                error_category=field_err_param["error_category"],
                error_strength=study_param["inv1"],
                reference_radius=field_err_param["error_reference_radius"],
                B_ref=None,
            )

            # ## rematch the working point and chroma after error
            xutil.match_tune_chroma(line, tw)

        ## Full twiss
        tw = line.twiss(eneloss_and_damping=True)

        ## Initial conditions
        line.vars["injection_bump.knob"] = 1
        particles = xutil.generate_particle_distribution(line, study_param)

        ## Tracking studies
        line.configure_radiation(model="quantum")

        # turn on/off beam-beam and track
        if beambeam_param["collisions"]:
            line.configure_radiation(
                model="quantum", model_beamstrahlung="quantum"
            )  # , model_bhabha="quantum" )
            for jj in bb_elem_name:
                line[jj].scale_strength = 1
                # line.get(jj).iscollective = True

        # xutil.activate_dynamic_injection_bump(line, inject_param, tw, peak_turn=0)
        # line.enable_time_dependent_vars = True

        ## Change context for multy CPU for tracking
        line.discard_tracker()
        line.build_tracker(_context=context_tracking)

        # Use tracking
        line.track(
            particles,
            num_turns=study_param["number_of_turns"],
            turn_by_turn_monitor=True,
            time=True,
            with_progress=10,
        )  # , freeze_longitudinal=True
        # particles.remove_unused_space()
        particles.sort(interleave_lost_particles=True)

        dic_particles_all = xutil.tracking_data_process(
            tracking_data=line.record_last_track,
            monitor_twiss=tw.rows[0],
            norm_emit_x=ref_param["normalized_emittance_x"],
            norm_emit_y=ref_param["normalized_emittance_y"],
            sigma_z=ref_param["bunch_length"],
            sigma_delta=ref_param["energy_spread"],
            particle_id_to_use="all",
        )
        xutil.save_dict_to_h5(f"{output_dir}/dic_particles_all.h5", dic_particles_all)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Simulation time: {elapsed_time:.4f} seconds")
        print("Done!")


if __name__ == "__main__":
    # Setup command-line argument parser
    parser = argparse.ArgumentParser(description="Track particles.")
    parser.add_argument(
        "--config_file",
        type=str,
        required=True,
        help="Path to the YAML configuration file.",
    )
    parser.add_argument(
        "--submit", action="store_true", help="Select True to submit to htcondor"
    )
    parser.add_argument(
        "--merge", action="store_true", help="Select True to merge output files"
    )
    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.config_file, args.submit, args.merge)
