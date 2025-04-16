import os
import h5py
import yaml
import json
import time
import copy
import glob
import shutil
import matplotlib.pyplot as plt

import numpy as np
import math
import re
import pandas as pd

import nafflib as pnf
import xcoll as xc
import xpart as xp
import xtrack as xt
import xfields as xf

from tqdm import tqdm
from pathlib import Path
import scipy.constants as sp_co
from scipy.linalg import cholesky
from scipy.stats import uniform, truncnorm, gamma
import scipy.optimize as opt
from multiprocessing import Pool
from contextlib import redirect_stdout, redirect_stderr, contextmanager


def madx_add_fccee_wigglers(madx, sequence_name="fccee_p_ring"):

    # ! --------------------------------------------------------------------------------------------------
    # ! Wiggler installation script
    # ! Creates MAD-X Wiggler elements follwing the parameters presented in https://arxiv.org/pdf/1909.12245.pdf ,
    # ! and install them in the MAD-X sequence.
    # ! --------------------------------------------------------------------------------------------------

    brhobeam = madx.sequence[sequence_name].beam.brho
    madx.input(f"""brhobeam={brhobeam};""")
    madx.input(f"""sequence_name={sequence_name};""")
    madx.input(
        f"""
    r_asymmetry = 6;
    B_plus = 0.7;
    L_plus = 0.430;
    L_minus = L_plus*r_asymmetry/2.;
    L_dis = 0.250;
    L_qa = 2.9;
    brhobeam = {madx.sequence[sequence_name].beam.brho};

    on_wiggler_h = 0;
    wiggler_angle_h:= on_wiggler_h * B_plus * L_plus / brhobeam;
    on_wiggler_v = 0;
    wiggler_angle_v:= on_wiggler_v * B_plus * L_plus / brhobeam;

    Print, Text="The critical energy of the wiggler is:";
    VALUE, 2.21*10^(-6)*(BEAM->ENERGY)^3/(brhobeam/B_plus/1000);
    Print, Text="MeV.";
    """
    )

    madx.input(
        """
    define_wigglers_as_multipoles() : macro {

        ! MWIM: MULTIPOLE, LRAD=L_minus, knl:={-0.5*wiggler_angle_h}, ksl:={-0.5*wiggler_angle_v};
        ! MWIP: MULTIPOLE, LRAD=L_plus,  knl:={ wiggler_angle_h},     ksl:={wiggler_angle_v};

        ! I put horizontal sbends (will tilt the multipoles in xsuite)
        MWIM: SBEND, L=L_minus, angle:=-0.5*wiggler_angle_v; !, tilt=pi/2;
        MWIP: SBEND, L=L_plus,  angle:=wiggler_angle_v; !, tilt=pi/2;

        MWI.A4RA: MWIM;
        MWI.B4RA: MWIP;
        MWI.C4RA: MWIM;
        MWI.D4RA: MWIM;
        MWI.E4RA: MWIP;
        MWI.F4RA: MWIM;
        MWI.G4RA: MWIM;
        MWI.H4RA: MWIP;
        MWI.I4RA: MWIM;

        MWI.A5RA: MWIM;
        MWI.B5RA: MWIP;
        MWI.C5RA: MWIM;
        MWI.D5RA: MWIM;
        MWI.E5RA: MWIP;
        MWI.F5RA: MWIM;
        MWI.G5RA: MWIM;
        MWI.H5RA: MWIP;
        MWI.I5RA: MWIM;

        MWI.A4RD: MWIM;
        MWI.B4RD: MWIP;
        MWI.C4RD: MWIM;
        MWI.D4RD: MWIM;
        MWI.E4RD: MWIP;
        MWI.F4RD: MWIM;
        MWI.G4RD: MWIM;
        MWI.H4RD: MWIP;
        MWI.I4RD: MWIM;

        MWI.A5RD: MWIM;
        MWI.B5RD: MWIP;
        MWI.C5RD: MWIM;
        MWI.D5RD: MWIM;
        MWI.E5RD: MWIP;
        MWI.F5RD: MWIM;
        MWI.G5RD: MWIM;
        MWI.H5RD: MWIP;
        MWI.I5RD: MWIM;

        MWI.A4RG: MWIM;
        MWI.B4RG: MWIP;
        MWI.C4RG: MWIM;
        MWI.D4RG: MWIM;
        MWI.E4RG: MWIP;
        MWI.F4RG: MWIM;
        MWI.G4RG: MWIM;
        MWI.H4RG: MWIP;
        MWI.I4RG: MWIM;

        MWI.A5RG: MWIM;
        MWI.B5RG: MWIP;
        MWI.C5RG: MWIM;
        MWI.D5RG: MWIM;
        MWI.E5RG: MWIP;
        MWI.F5RG: MWIM;
        MWI.G5RG: MWIM;
        MWI.H5RG: MWIP;
        MWI.I5RG: MWIM;

        MWI.A4RJ: MWIM;
        MWI.B4RJ: MWIP;
        MWI.C4RJ: MWIM;
        MWI.D4RJ: MWIM;
        MWI.E4RJ: MWIP;
        MWI.F4RJ: MWIM;
        MWI.G4RJ: MWIM;
        MWI.H4RJ: MWIP;
        MWI.I4RJ: MWIM;

        MWI.A5RJ: MWIM;
        MWI.B5RJ: MWIP;
        MWI.C5RJ: MWIM;
        MWI.D5RJ: MWIM;
        MWI.E5RJ: MWIP;
        MWI.F5RJ: MWIM;
        MWI.G5RJ: MWIM;
        MWI.H5RJ: MWIP;
        MWI.I5RJ: MWIM;

    }
    """
    )

    madx.input(
        """
    install_wigglers(sequence_name) : macro {
        SEQEDIT, SEQUENCE=sequence_name;
        FLATTEN;
        
            REMOVE, ELEMENT = fwig.1;
            INSTALL, ELEMENT=MWI.A4RA, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.B4RA, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.C4RA, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.D4RA, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.E4RA, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.F4RA, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.G4RA, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.H4RA, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA4.1;
            INSTALL, ELEMENT=MWI.I4RA, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA4.1;
            
            REMOVE, ELEMENT = fwig.2;
            INSTALL, ELEMENT=MWI.A5RA, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.B5RA, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.C5RA, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.D5RA, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.E5RA, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.F5RA, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.G5RA, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.H5RA, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA5.1;
            INSTALL, ELEMENT=MWI.I5RA, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA5.1;

            REMOVE, ELEMENT = fwig.3;
            INSTALL, ELEMENT=MWI.A4RD, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.B4RD, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.C4RD, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.D4RD, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.E4RD, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.F4RD, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.G4RD, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.H4RD, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA4.2;
            INSTALL, ELEMENT=MWI.I4RD, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA4.2;
            
            REMOVE, ELEMENT = fwig.4;
            INSTALL, ELEMENT=MWI.A5RD, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.B5RD, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.C5RD, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.D5RD, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.E5RD, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.F5RD, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.G5RD, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.H5RD, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA5.2;
            INSTALL, ELEMENT=MWI.I5RD, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA5.2;

            REMOVE, ELEMENT = fwig.5;
            INSTALL, ELEMENT=MWI.A4RG, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.B4RG, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.C4RG, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.D4RG, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.E4RG, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.F4RG, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.G4RG, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.H4RG, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA4.3;
            INSTALL, ELEMENT=MWI.I4RG, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA4.3;
            
            REMOVE, ELEMENT = fwig.6;
            INSTALL, ELEMENT=MWI.A5RG, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.B5RG, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.C5RG, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.D5RG, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.E5RG, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.F5RG, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.G5RG, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.H5RG, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA5.3;
            INSTALL, ELEMENT=MWI.I5RG, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA5.3;

            REMOVE, ELEMENT = fwig.7;
            INSTALL, ELEMENT=MWI.A4RJ, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.B4RJ, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.C4RJ, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.D4RJ, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.E4RJ, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.F4RJ, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.G4RJ, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.H4RJ, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA4.4;
            INSTALL, ELEMENT=MWI.I4RJ, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA4.4;
            
            REMOVE, ELEMENT = fwig.8;
            INSTALL, ELEMENT=MWI.A5RJ, AT= L_qa/2. + 1 * L_dis + 0.5 * L_minus + 0.0 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.B5RJ, AT= L_qa/2. + 2 * L_dis + 1.0 * L_minus + 0.5 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.C5RJ, AT= L_qa/2. + 3 * L_dis + 1.5 * L_minus + 1.0 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.D5RJ, AT= L_qa/2. + 4 * L_dis + 2.5 * L_minus + 1.0 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.E5RJ, AT= L_qa/2. + 5 * L_dis + 3.0 * L_minus + 1.5 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.F5RJ, AT= L_qa/2. + 6 * L_dis + 3.5 * L_minus + 2.0 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.G5RJ, AT= L_qa/2. + 7 * L_dis + 4.5 * L_minus + 2.0 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.H5RJ, AT= L_qa/2. + 8 * L_dis + 5.0 * L_minus + 2.5 * L_plus, FROM=QA5.4;
            INSTALL, ELEMENT=MWI.I5RJ, AT= L_qa/2. + 9 * L_dis + 5.5 * L_minus + 3.0 * L_plus, FROM=QA5.4;
        FLATTEN;
        ENDEDIT;

    }
    """
    )

    madx.input("exec, define_wigglers_as_multipoles()")
    madx.input(f"""exec, install_wigglers({sequence_name})""")
    madx.use(sequence=sequence_name)

    return


def read_reference_parameters(file_name, operation_mode="z"):
    ref_par_imp = json.load(open(file_name))
    energy = ref_par_imp[operation_mode]["ENERGY"] * 1e9 # eV
    energy_loss_per_turn = ref_par_imp[operation_mode]["ENERGYLOSS_PER_TURN"] * 1e9 # eV
    longitudinal_damping_time = ref_par_imp[operation_mode][
        "LONGITUDINAL_DAMPING_TIME"
    ]  # turns
    emittance_x = ref_par_imp[operation_mode]["EMITTANCE_X"]  # m
    emittance_y = ref_par_imp[operation_mode]["EMITTANCE_Y"]  # m
    bunch_population = ref_par_imp[operation_mode]["BUNCH_POPULATION"]
    energy_spread_SR = ref_par_imp[operation_mode]["ENERGYSPREAD_SR"] * 1e-2
    energy_spread_BS = ref_par_imp[operation_mode]["ENERGYSPREAD_BS"] * 1e-2
    bunch_length_SR = ref_par_imp[operation_mode]["BUNCHLENGTH_SR"] * 1e-3  # m
    bunch_length_BS = ref_par_imp[operation_mode]["BUNCHLENGTH_BS"] * 1e-3  # m
    circumference = ref_par_imp[operation_mode]['CIRCUMFERENCE']
    qx_fractional = ref_par_imp[operation_mode]['Q1']
    qy_fractional = ref_par_imp[operation_mode]['Q2']
    qs = ref_par_imp[operation_mode]['QS']
    dqx = ref_par_imp[operation_mode]['QPRIME1']
    dqy = ref_par_imp[operation_mode]['QPRIME2']
    betastar_x = ref_par_imp[operation_mode]['BETASTAR_X']
    betastar_y = ref_par_imp[operation_mode]['BETASTAR_Y']
    beambeam_tuneshift_x = ref_par_imp[operation_mode]['BEAMBEAM_TUNESHIFT_X']
    beambeam_tuneshift_y = ref_par_imp[operation_mode]['BEAMBEAM_TUNESHIFT_Y']

    reference_parameters = {
        "reference_parameters_file_name": file_name,
        "operation_mode": operation_mode,
        "energy": energy,
        "energy_loss_per_turn": energy_loss_per_turn,  # GeV
        "longitudinal_damping_time": longitudinal_damping_time,  # turns
        "emittance_x": emittance_x,  # m
        "emittance_y": emittance_y,  # m
        "bunch_population": bunch_population,
        "energy_spread_SR": energy_spread_SR,
        "energy_spread_BS": energy_spread_BS,
        "bunch_length_SR": bunch_length_SR,  # m
        "bunch_length_BS": bunch_length_BS,  # m
        "energy_spread": energy_spread_SR,
        "bunch_length": bunch_length_SR,  # m
        "circumference": circumference,
        "qx_fractional": qx_fractional,
        "qy_fractional": qy_fractional,
        "qs": qs,
        "dqx": dqx,
        "dqy": dqy,
        "betastar_x": betastar_x,
        "betastar_y": betastar_y,
        "beambeam_tuneshift_x": beambeam_tuneshift_x,
        "beambeam_tuneshift_y": beambeam_tuneshift_y,
    }

    return reference_parameters


def make_thin(line_to_thin):
    Strategy = xt.slicing.Strategy
    Teapot = xt.slicing.Teapot
    slicing_strategies = [
        Strategy(slicing=Teapot(1)),  # Default catch-all as in MAD-X
        Strategy(slicing=Teapot(3), element_type=xt.Bend),
        Strategy(slicing=Teapot(3), element_type=xt.CombinedFunctionMagnet),
        # Strategy(slicing=Teapot(50), element_type=xt.Quadrupole), # Starting point
        Strategy(slicing=Teapot(10), name=r"^qf.*"),
        Strategy(slicing=Teapot(10), name=r"^qd.*"),
        Strategy(slicing=Teapot(5), name=r"^qfg.*"),
        Strategy(slicing=Teapot(5), name=r"^qdg.*"),
        Strategy(slicing=Teapot(5), name=r"^ql.*"),
        Strategy(slicing=Teapot(5), name=r"^qs.*"),
        Strategy(slicing=Teapot(10), name=r"^qb.*"),
        Strategy(slicing=Teapot(10), name=r"^qg.*"),
        Strategy(slicing=Teapot(10), name=r"^qh.*"),
        Strategy(slicing=Teapot(10), name=r"^qi.*"),
        Strategy(slicing=Teapot(10), name=r"^qr.*"),
        Strategy(slicing=Teapot(10), name=r"^qu.*"),
        Strategy(slicing=Teapot(10), name=r"^qx.*"),
        Strategy(slicing=Teapot(10), name=r"^qy.*"),
        Strategy(slicing=Teapot(50), name=r"^qa.*"),
        Strategy(slicing=Teapot(50), name=r"^qc.*"),
        Strategy(slicing=Teapot(130), name=r"^qf1b.*"),
        Strategy(slicing=Teapot(130), name=r"^qf1a.*"),
        Strategy(slicing=Teapot(130), name=r"^qd0b.*"),
        Strategy(slicing=Teapot(130), name=r"^qd0a.*"),
        Strategy(slicing=Teapot(20), name=r"^sy.*"),
        Strategy(slicing=Teapot(20), name=r"^sc.*"),
        Strategy(slicing=Teapot(10), name=r"^sf.*"),
        Strategy(slicing=Teapot(10), name=r"^sd.*"),
    ]

    line_to_thin.slice_thick_elements(slicing_strategies=slicing_strategies)


def match_wiggler_for_eq_emitt(line, target_eq_em_x=None, target_eq_em_y=None):
    if target_eq_em_x is not None and target_eq_em_y is not None:
        line.vars["on_wiggler_h"] = 0.1
        line.vars["on_wiggler_v"] = 0.1
        opt_eq_em = line.match(
            method="6d",
            eneloss_and_damping=True,
            vary=[
                xt.VaryList(["on_wiggler_h", "on_wiggler_v"], step=1e-3, tag="wigg"),
            ],
            targets=[
                xt.TargetSet(eq_gemitt_x=target_eq_em_x, tol=1e-15, tag="eq_emit_x"),
                xt.TargetSet(eq_gemitt_y=target_eq_em_y, tol=1e-15, tag="eq_emit_y"),
            ],
        )
        opt_eq_em.solve()

    elif target_eq_em_x is not None and target_eq_em_y is None:
        line.vars["on_wiggler_h"] = 0.1
        opt_eq_em = line.match(
            method="6d",
            eneloss_and_damping=True,
            vary=[
                xt.VaryList(["on_wiggler_h"], step=1e-3, tag="wigg_x"),
            ],
            targets=[
                xt.TargetSet(eq_gemitt_x=target_eq_em_x, tol=1e-15, tag="eq_emit_x"),
            ],
        )
        opt_eq_em.solve()

    elif target_eq_em_x is None and target_eq_em_y is not None:
        line.vars["on_wiggler_v"] = 0.1
        opt_eq_em = line.match(
            method="6d",
            eneloss_and_damping=True,
            vary=[
                xt.VaryList(["on_wiggler_v"], step=1e-3, tag="wigg_y"),
            ],
            targets=[
                xt.TargetSet(
                    eq_gemitt_y=target_eq_em_y, tol=1e-15, tag="eq_emit_y"
                ),  # tol=10**(np.floor(np.log10(abs(target_eq_em_y)))-2)
            ],
        )
        opt_eq_em.solve()

    else:

        raise Exception("The wigglers target values not set correctly!")

    opt_eq_em.target_status()
    opt_eq_em.vary_status()


def madx_add_apertures(
    madx, aperture_dir="fcc-ee-lattice-V25_GHC/aperture", sequence_name="fccee_p_ring"
):
    # ! --------------------------------------------------------------------------------------------------
    # ! Aperture installation scriptand install them in the MAD-X sequence.
    # ! Assuming the aperture definition file is in the lattice repository and kept up to date by the collimation team
    # ! --------------------------------------------------------------------------------------------------

    aperture_file_path = os.path.join(aperture_dir, "FCCee_aper_definitions.madx")

    madx.input("""option,update_from_parent=true;""")
    madx.input(f"""sequence_name={sequence_name};""")
    madx.call(f"{aperture_file_path}")
    madx.use(sequence=sequence_name)

    return
