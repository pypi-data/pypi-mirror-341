# EXAMPLE of collimation studies: top-up injection for FCC-ee
# The circulating beam in the collider is bumped for 1 turn 
# the halo is generated and then is biìumped and so scraped at a collimator introduced during the run 
# lossmpas are produced
# NOTE: BDSIM AS WELL AS COLLIMASIM HAS TO BE INSTALLED IN THE ENVIRONMENT USED FOR RUNNING THIS SCRIPT 
import os
import sys
import time
import argparse
import numpy as np
import xpart as xp
import xtrack as xt
import xcoll as xc
import xobjects as xo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import xsuite_utilities as xutil


def main(config_file='configuration_l000017_z_distribution_matched.yaml', submit='False', merge='False'):

    start_time = time.time()
    ####### call/set config parameters #######
    parameters = xutil.load_configuration_parameters (config_file)
    xutil.correct_parameters_conflicts(parameters)

    ref_param = parameters['reference_parameters']
    beambeam_param = parameters['beam_beam_parameters']
    study_param = parameters['study_parameters']
    inject_param = parameters['injection_parameters']
    field_err_param = parameters['field_error_parameters']
    collimation_param = parameters['collimation_parameters']

    output_dir = study_param['output_dir']
    if submit:
        # submit to htcondor
        xutil.submit_jobs(parameters, config_file)
    elif merge:
        working_directory = parameters['jobsubmission']['working_directory']
        job_output_dir = parameters['jobsubmission']['job_output_dir']
        match_pattern = '*part.hdf*'
        output_file = os.path.join(working_directory, 'part_merged.hdf')
        xutil.load_output(working_directory, job_output_dir, output_file, match_pattern=match_pattern, load_particles=True)
    else:
        os.makedirs(output_dir, exist_ok=True)

        ######################
        ####### xsuite #######
        ######################

        ## Load line from json
        line = xt.Line.from_json(ref_param['line_name'])
        line.config.XTRACK_USE_EXACT_DRIFTS = True

        ## Choose a context
        context = xo.ContextCpu()         # For CPU
        context_tracking = xo.ContextCpu(omp_num_threads='auto') # For CPU with activate multi-core CPU parallelization

        ## Transfer lattice on context and compile tracking code
        line.build_tracker(_context=context)

        ## Input lattice, table and survey
        tab = line.get_table(attr=True)

        # turn off beam-beam 
        if beambeam_param['collisions']: 
            bb_elem_name = tab.rows[tab.element_type=='BeamBeamBiGaussian3D'].name
            for jj in bb_elem_name:
                line[jj].scale_strength = 0
                #line.get(jj).iscollective = True

        # Cycle the line now to have the correct initialitation of the beam 
        line.cycle(name_first_element=study_param['start_element'], inplace=True)
        tab = line.get_table(attr=True)

        ## Enable synchrotron radiation 
        # we choose the `mean` mode in which the mean power loss is applied without
        # stochastic fluctuations (quantum excitation).
        line.configure_radiation(model='mean')
        line.compensate_radiation_energy_loss()

        ## If the line is not cycled to an RF this step is necessary to ensure the compensation at the RF
        tw = line.twiss(eneloss_and_damping=True)
        delta0 = tw.delta[0] - np.mean(tw.delta)
        line.compensate_radiation_energy_loss(delta0=delta0)

        ## Insert monitor at the beam starting point and at the injection bump kickers
        line.discard_tracker()
        # Define monitor
        monitor = xt.ParticlesMonitor(start_at_turn=0, stop_at_turn =study_param['number_of_turns'], num_particles = study_param['max_particles'] , auto_to_numpy=True)

        line.insert_element('monitor_inject_point', monitor.copy(), at_s=tab['s',inject_param['injection_marker_name']]+ 0.01)
        line.insert_element('monitor_bump_kick_left', monitor.copy(), at_s=tab['s','injection_bump_kick_left']+ 0.01)
        line.insert_element('monitor_bump_kick_right', monitor.copy(), at_s=tab['s','injection_bump_kick_right']+ 0.01)

        # Insert monitor at the primary collimator position, also with a small offset
        line.insert_element('monitor_prim_coll',monitor.copy(), at_s=tab['s','tcp.h.b1'] + 0.5)

        # Insert ijection septa collimator if circulating beam is considered
        if any(ii in study_param['ini_cond_type'] for ii in ['matched', 'circulating.halo']):
            if study_param['ini_cond_energy_offset'] == None: # to be sure is only the core and halo cases
                line.insert_element(name="injection_septa.b1", element=xt.Drift(), at_s=tab['s', inject_param['injection_marker_name']] - 40, s_tol=1e-3)
                line.insert_element('injection_septa.b1_aper', element=xt.LimitEllipse(a=0.03, b=0.03), at='injection_septa.b1')
            
            xutil.install_collimators(line, collimation_param, ref_param)
        line.build_tracker(_context=context)

        ## Full twiss 
        tw = line.twiss(eneloss_and_damping=True)
        ref_part = line.particle_ref

        ## Initial conditions 
        line.vars['injection_bump.knob'] = 0
        particles, grid_details = xutil.generate_particle_grid (line, study_param, particle_capacity=study_param['max_particles'], r_range_x=(5,11), r_range_y=(5,11), theta_range_x=(0,2*np.pi), theta_range_y=(0,2*np.pi))
        #particles = xutil.generate_particle_distribution (line, study_param, particle_capacity=study_param['max_particles'], q_factor=1, b_factor=1)

        ## Tracking studies
        line.configure_radiation(model='quantum')
        
        # turn on/off beam-beam and track
        if beambeam_param['collisions']: 
            line.configure_radiation(model='quantum', model_beamstrahlung='quantum') #, model_bhabha="quantum" )
            for jj in bb_elem_name:
                line[jj].scale_strength = 1
                #line.get(jj).iscollective = True
            
            xutil.insert_bb_lens_bounding_apertures(line)

        xutil.activate_dynamic_injection_bump(line, inject_param, tw, peak_turn=10)
        line.enable_time_dependent_vars = True

        ## Change context for multy CPU for tracking
        line.discard_tracker()
        line.build_tracker(_context=context_tracking)

        xutil.generate_lossmap(line, particles, ref_part, collimation_param, study_param, output_dir)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Simulation time: {elapsed_time:.4f} seconds")
        print('Done!')


if __name__ == "__main__":
    # Setup command-line argument parser
    parser = argparse.ArgumentParser(description='Track particles.')
    parser.add_argument('--config_file', type=str, required=True, help='Path to the YAML configuration file.')
    parser.add_argument('--submit', action='store_true', help='Select True to submit to htcondor')
    parser.add_argument('--merge', action='store_true', help='Select True to merge output files')
    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.config_file, args.submit, args.merge)

