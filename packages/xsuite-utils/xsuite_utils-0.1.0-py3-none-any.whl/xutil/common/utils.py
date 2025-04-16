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
from pylhc_submitter.job_submitter import main as htcondor_submit

import logging

logger = logging.getLogger("xutil")
logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def save_dict_to_h5(filename, data_dict):
    """
    Saves a dictionary to an HDF5 file. Supports both flat and nested dictionaries.

    :param filename: Name of the HDF5 file (e.g., 'data.h5')
    :param data_dict: Dictionary containing NumPy arrays (can be nested)
    """

    def recursively_save(group, dictionary):
        for key, value in dictionary.items():
            if isinstance(
                value, dict
            ):  # If value is a nested dictionary, create a subgroup
                subgroup = group.create_group(key)
                recursively_save(subgroup, value)  # Recursive call
            else:
                group.create_dataset(key, data=value)  # Save NumPy arrays

    with h5py.File(filename, "w") as f:
        recursively_save(f, data_dict)  # Call recursive function

    logger.info(f"Dictionary saved to {filename}")


def load_dict_from_h5(filename):
    """
    Loads an HDF5 file into a dictionary, automatically handling nested structures.

    :param filename: Name of the HDF5 file to load
    :return: Dictionary with the same structure as the original data
    """

    def recursively_load(group):
        result = {}
        for key, item in group.items():
            if isinstance(item, h5py.Group):  # If it's a group, recurse
                result[key] = recursively_load(item)
            else:  # If it's a dataset, load it as a NumPy array
                result[key] = item[()]
        return result

    with h5py.File(filename, "r") as f:
        return recursively_load(f)


def ensure_list(value):
    # Check if the value is a single string
    if isinstance(value, (str, int, float)):
        return [value]
    # Return as-is if it's already a list or another iterable
    return value


def save_config_file(file_name, dict_to_save):
    with open(file_name, "w") as file:
        # Save to a YAML file
        if file_name.split(".")[-1] == "yaml":
            clean_dict_to_save = convert_types(dict_to_save)
            yaml.dump(
                clean_dict_to_save, file, default_flow_style=False, sort_keys=False
            )
        # Save to a JSON file
        elif file_name.split(".")[-1] == "json":
            json.dump(dict_to_save, file, indent=4)


def load_config_file(file_name):
    with open(file_name, "r") as file:
        # Load YAML file into a dictionary
        if file_name.split(".")[-1] == "yaml":
            config_dict = yaml.safe_load(file)
        # Load JSON file into a dictionary
        elif file_name.split(".")[-1] == "json":
            config_dict = json.load(file)

    return config_dict


def convert_types(obj):
    """Recursively convert complex data types to native Python types."""

    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert NumPy arrays to lists
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj)  # Convert NumPy floats to Python floats
    elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)  # Convert NumPy integers to Python ints
    elif isinstance(obj, set):
        return list(obj)  # Convert sets to lists (YAML does not support sets)
    elif isinstance(obj, tuple):
        return list(obj)  # Convert tuples to lists
    elif isinstance(obj, dict):
        return {
            k: convert_types(v) for k, v in obj.items()
        }  # Recursive for dictionaries
    elif isinstance(obj, list):
        return [convert_types(i) for i in obj]  # Recursive for lists
    elif obj is None:
        return None  # Keep None as null in YAML
    else:
        return obj  # Fallback: return as-is


def element_selection_from_line(
    line, selection_criteria, get_thin_element_parent=False, regex=False
):

    tt = line.get_table(attr=True)
    sv = line.survey()

    # Extract regex patterns and element types from selection_criteria
    regex_patterns = [re.compile(item) for item in selection_criteria if regex]

    # Extract relevant elements dynamically
    filtered_elements = []
    for name in line.element_names:
        if (
            ~line[name].isthick
            and "_parent" in line[name].get_expr().keys()
            and get_thin_element_parent
        ):
            if name.startswith("drift_"):
                continue
            else:
                element = line[name]._parent
                element_type = element.__class__.__name__
                element_name = name.split("..")[0]
                elem_name_for_s = element_name + "_entry"
        else:
            element = line[name]
            element_type = element.__class__.__name__
            element_name = name
            elem_name_for_s = element_name
        if element_type in selection_criteria or any(
            pattern.match(name) for pattern in regex_patterns
        ):
            filtered_elements.append(
                {
                    "name": element_name,
                    "type": element_type,  # Get the element type
                    "s": elem_name_for_s,  # Get the longitudinal position (s)
                    "X": elem_name_for_s,  # Get the survey position (X)
                    "Y": elem_name_for_s,  # Get the survey position (Y)
                    "Z": elem_name_for_s,  # Get the survey position (Z)
                    # "length": getattr(element, "length", 0),  # Length of element
                    # "k1": getattr(element, "k1", 0),  # Quadrupole strength
                    # "k1s": getattr(element, "k1s", 0),  # Skew Quadrupole strength
                    # "k2": getattr(element, "k2", 0),  # Sextupole strength
                    # "k2s": getattr(element, "k2s", 0),  # Skew Sextupole strength
                    # "k3": getattr(element, "k3", 0),  # Octupole strength
                    # "k3s": getattr(element, "k3s", 0),  # Skew Octupole strength
                    # "shift_x": getattr(element, "shift_x", 0),  # X shift of the element
                    # "shift_y": getattr(element, "shift_y", 0),  # Y shift of the element
                    # "shift_s": getattr(element, "shift_s", 0),  # S shift of the element
                }
            )

    # Convert to Pandas DataFrame
    df = (
        pd.DataFrame(filtered_elements)
        .drop_duplicates(subset=["name"], keep="first")
        .set_index("name", drop=False)
        .rename_axis(None)
    )
    df["s"] = tt.rows[df.s[:]].s
    df["X"] = sv.rows[df.X[:]].X
    df["Y"] = sv.rows[df.Y[:]].Y
    df["Z"] = sv.rows[df.Z[:]].Z

    return df


def add_misalignment_error(
    line,
    element_familys,
    error_class="systematic",
    seeds=[201, 202, 203, 204],
    shift_x=0,
    shift_y=0,
    shift_s=0,
    rot_s_rad=0,
):
    """
    loop over the element_familys entris and add errors
    for every entry an error knob is generated

    element_familys: 'Dipole', 'Quadrupole', ... or 'sf.*', 'sd.*', ...
    error_class: 'systematic', 'random' (in 3sigma)
    seeds: seed number for each shift or rotation
    """

    tt = line.get_table(attr=True)
    tt_no_parent_elem = tt.rows[tt.parent_name == "None"]
    tt_no_marker_no_parent_elem = tt_no_parent_elem.rows[
        tt_no_parent_elem.element_type != "Marker"
    ]

    element_family_list = ensure_list(element_familys)

    for element_family in element_family_list:

        mis_switch_name = (
            "mis_" + element_family + "_" + error_class[:3] + "_" + str(seeds)
        )
        line[mis_switch_name] = 1

        ## in order to includ the parent elements if the line has thin element
        parent_names = [item for item in tt.parent_name if item is not None]
        if len(parent_names) > 0:
            parent_types = [
                line[parent_names[ii]].__class__.__name__
                for ii in range(len(parent_names))
            ]
        else:
            parent_types = []

        if element_family in np.unique(np.append(tt.element_type, parent_types)):
            parent_type_names = [
                name
                for ii, name in enumerate(parent_names)
                if parent_types[ii] == element_family
            ]
            element_names = np.append(
                tt_no_marker_no_parent_elem.rows[
                    tt_no_marker_no_parent_elem.element_type == element_family
                ].name,
                parent_type_names,
            )
        else:
            parent_type_names = [
                name for name in parent_names if re.match(element_family, name)
            ]
            element_names = np.append(
                tt_no_marker_no_parent_elem.rows[element_family].name, parent_type_names
            )

        size = len(element_names)

        if error_class == "systematic":
            shift_values_x = np.full(shift_x, size)
            shift_values_y = np.full(shift_y, size)
            shift_values_s = np.full(shift_s, size)
            rot_values_s = np.full(rot_s_rad, size)
        elif error_class == "random":
            mean = 0
            std_dev = 1
            lower_bound = -3  # in sigma
            upper_bound = 3  # in sigma
            for ii, name in enumerate(["sx", "sy", "ss", "rs"]):
                if name == "sx":
                    np.random.seed(seeds[ii])
                    shift_values_x = shift_x * truncnorm.rvs(
                        lower_bound, upper_bound, loc=mean, scale=std_dev, size=size
                    )
                elif name == "sy":
                    np.random.seed(seeds[ii])
                    shift_values_y = shift_y * truncnorm.rvs(
                        lower_bound, upper_bound, loc=mean, scale=std_dev, size=size
                    )
                elif name == "ss":
                    np.random.seed(seeds[ii])
                    shift_values_s = shift_s * truncnorm.rvs(
                        lower_bound, upper_bound, loc=mean, scale=std_dev, size=size
                    )
                elif name == "rs":
                    np.random.seed(seeds[ii])
                    rot_values_s = rot_s_rad * truncnorm.rvs(
                        lower_bound, upper_bound, loc=mean, scale=std_dev, size=size
                    )

        for ii, name in enumerate(element_names):
            line[name].shift_x = line.ref[mis_switch_name] * shift_values_x[ii]
            line[name].shift_y = line.ref[mis_switch_name] * shift_values_y[ii]
            line[name].shift_s = line.ref[mis_switch_name] * shift_values_s[ii]
            line[name].rot_s_rad = line.ref[mis_switch_name] * rot_values_s[ii]

    return


def add_field_error(
    line,
    element_familys,
    error_class="systematic",
    seed=0,
    error_type=None,
    error_category="relative",
    error_strength=1,
    reference_radius=1e-2,
    B_ref=None,
):
    """
    loop over the element_familys entris and add erros
    for evry entry an error knob is generated

    element_familys: 'Dipole', 'Quadrupole', ... or 'sf.*', 'sd.*', ...
    error_class: 'systematic', 'random' (in 3sigma)
    error_type: 'b1', 'a1', 'b2', 'a2', ... k0, k1, k1s, ...
    error_category: 'relative', 'absolute'
    """

    tt = line.get_table(attr=True)
    tt_no_parent_elem = tt.rows[tt.parent_name == "None"]
    tt_no_marker_no_parent_elem = tt_no_parent_elem.rows[
        tt_no_parent_elem.element_type != "Marker"
    ]

    element_family_list = ensure_list(element_familys)

    for element_family in element_family_list:

        error_switch_name = (
            "err_"
            + element_family
            + "_"
            + error_type
            + "_"
            + error_category[:3]
            + "_"
            + error_class[:3]
            + "_"
            + str(seed)
        )
        line[error_switch_name] = 1

        ## in order to includ the parent elements if the line has thin element
        parent_names = [item for item in tt.parent_name if item is not None]
        if len(parent_names) > 0:
            parent_types = [
                line[parent_names[ii]].__class__.__name__
                for ii in range(len(parent_names))
            ]
        else:
            parent_types = []

        if element_family in np.unique(np.append(tt.element_type, parent_types)):
            parent_type_names = [
                name
                for ii, name in enumerate(parent_names)
                if parent_types[ii] == element_family
            ]
            element_names = np.append(
                tt_no_marker_no_parent_elem.rows[
                    tt_no_marker_no_parent_elem.element_type == element_family
                ].name,
                parent_type_names,
            )
        else:
            parent_type_names = [
                name for name in parent_names if re.match(element_family, name)
            ]
            element_names = np.append(
                tt_no_marker_no_parent_elem.rows[element_family].name, parent_type_names
            )

        size = len(element_names)

        if error_class == "systematic":
            error_values = np.ones(size) * error_strength
        elif error_class == "random":
            np.random.seed(seed)
            std_dev = 1
            mean = 0
            lower_bound = -3  # in sigma
            upper_bound = 3  # in sigma
            error_values = error_strength * truncnorm.rvs(
                lower_bound, upper_bound, loc=mean, scale=std_dev, size=size
            )

        if error_type[0] == "k":
            if error_type[-1] == "s":
                normal_skew = "s"
                order = int(error_type[1:-1])
            else:
                normal_skew = "n"
                order = int(error_type[1:])

        if error_type[0] in ["b", "a"]:
            order = int(error_type[1:])
            if error_type[0] == "b":
                normal_skew = "n"
            else:
                normal_skew = "s"

        for ii, name in enumerate(element_names):
            elem_tt = line[name].get_table()
            main_k_name = elem_tt.name[np.argmax(np.abs(elem_tt.value[:2]))]
            main_k_value = elem_tt.rows[main_k_name].value[0]
            main_order = int(main_k_name[1:]) + 1

            if error_category == "relative":
                error_values[ii] = error_values[ii] * main_k_value

                if error_type[0] in ["b", "a"]:
                    factorial_ratio = math.factorial(order - 1) / math.factorial(
                        main_order - 1
                    )
                    rref_term = reference_radius ** (main_order - order)
                    error_values[ii] = error_values[ii] * factorial_ratio * rref_term

            if error_category == "absolute":
                if error_type[0] in ["b", "a"]:
                    if B_ref is None:
                        raise ValueError("The B_ref is needed!")
                    else:
                        Brho = (line.particle_ref.p0c / sp_co.c) / line.particle_ref.q0
                        rref_term = reference_radius ** (order - 1)
                        error_values[ii] = (
                            error_values[ii]
                            * B_ref
                            * math.factorial(order - 1)
                            / (rref_term * Brho)
                        )
                        if normal_skew == "s":
                            error_values[ii] = -error_values[ii]

            # Add multipolar components to elements
            if normal_skew == "n":
                line[name].knl[order - 1] = (
                    line.ref[error_switch_name]
                    * error_values[ii]
                    * elem_tt.rows["length"].value[0]
                )
            if normal_skew == "s":
                line[name].ksl[order - 1] = (
                    line.ref[error_switch_name]
                    * error_values[ii]
                    * elem_tt.rows["length"].value[0]
                )

    return


def set_integrator(line):
    tt = line.get_table()
    tt_bend = tt.rows[(tt.element_type == "Bend") | (tt.element_type == "RBend")]
    tt_quad = tt.rows[(tt.element_type == "Quadrupole")]
    tt_sext = tt.rows[(tt.element_type == "Sextupole")]

    # line.set(tt_bend, integrator='uniform', num_multipole_kicks=3, model='mat-kick-mat') #'drift-kick-drift-exact')
    # line.set(tt_quad, integrator='uniform', num_multipole_kicks=3, model='mat-kick-mat')
    # line.set(tt_sext, integrator='yoshida4', num_multipole_kicks=1)

    line.set(tt_bend, integrator="yoshida4", num_multipole_kicks=1)
    line.set(tt_quad, integrator="yoshida4", num_multipole_kicks=1)
    line.set(tt_sext, integrator="yoshida4", num_multipole_kicks=1)

    return


def make_thin_and_rematch(line_to_thin, target_twiss, machine="FCCee"):
    Strategy = xt.slicing.Strategy
    Teapot = xt.slicing.Teapot
    if machine == "FCCee":
        slicing_strategies = [
            Strategy(slicing=Teapot(1)),  # Default catch-all as in MAD-X
            Strategy(slicing=Teapot(3), element_type=xt.Bend),
            Strategy(slicing=Teapot(3), element_type=xt.CombinedFunctionMagnet),
            # Strategy(slicing=Teapot(50), element_type=xt.Quadrupole), # Starting point
            Strategy(slicing=Teapot(30), name=r"^mwi\..*"),
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
    elif machine == "LHC":
        slicing_strategies = [
            Strategy(slicing=Teapot(1)),  # Default catch-all as in MAD-X
            Strategy(slicing=Teapot(2), element_type=xt.Bend),
            Strategy(slicing=None, element_type=xt.Solenoid),
            Strategy(slicing=Teapot(2), element_type=xt.Quadrupole),
            Strategy(slicing=Teapot(2), element_type=xt.Sextupole),
            Strategy(slicing=Teapot(2), element_type=xt.Octupole),
            Strategy(slicing=Teapot(4), name=r"^mbx.*"),
            Strategy(slicing=Teapot(4), name=r"^mbrb.*"),
            Strategy(slicing=Teapot(4), name=r"^mbrc.*"),
            Strategy(slicing=Teapot(4), name=r"^mbrs.*"),
            Strategy(slicing=Teapot(4), name=r"^mbh.*"),
            Strategy(slicing=Teapot(2), name=r"^mq.*"),
            Strategy(slicing=Teapot(16), name=r"^mqxa.*"),
            Strategy(slicing=Teapot(16), name=r"^mqxb.*"),
            Strategy(slicing=Teapot(4), name=r"^mqwa.*"),
            Strategy(slicing=Teapot(4), name=r"^mqwb.*"),
            Strategy(slicing=Teapot(4), name=r"^mqy.*"),
            Strategy(slicing=Teapot(4), name=r"^mqm.*"),
            Strategy(slicing=Teapot(4), name=r"^mqmc.*"),
            Strategy(slicing=Teapot(4), name=r"^mqml.*"),
            Strategy(slicing=Teapot(2), name=r"^mqtlh.*"),
            Strategy(slicing=Teapot(2), name=r"^mqtli.*"),
            Strategy(slicing=Teapot(2), name=r"^mqt.*"),
        ]
    else:
        raise Exception("The slicing of asked machine is not suported yet!")

    line_to_thin.slice_thick_elements(slicing_strategies=slicing_strategies)

    ## Transfer lattice on context and compile tracking code
    line_to_thin.build_tracker()

    ## Compute thin lattice functions withoud rf and radiation before rematching
    tw_thin_4d_no_rad_before = line_to_thin.twiss(method="4d")
    # line_to_thin.twiss(start=line_to_thin.element_names[0], end=line_to_thin.element_names[-1],
    # method='4d', init=target_twiss.get_twiss_init(0))

    # Compare tunes
    logger.info("Before rematching:")

    logger.info("Tunes thick model:")
    logger.info(target_twiss.qx, target_twiss.qy)
    logger.info("Tunes thin model:")
    logger.info(tw_thin_4d_no_rad_before.mux[-1], tw_thin_4d_no_rad_before.muy[-1])

    logger.info("Beta beating at ips:")
    logger.info(
        "H:",
        np.max(
            np.abs(
                tw_thin_4d_no_rad_before.rows["ip.*"].betx
                / target_twiss.rows["ip.*"].betx
                - 1
            )
        ),
    )
    logger.info(
        "V:",
        np.max(
            np.abs(
                tw_thin_4d_no_rad_before.rows["ip.*"].bety
                / target_twiss.rows["ip.*"].bety
                - 1
            )
        ),
    )

    # logger.info('Number of elements: ', len(line))
    logger.info("\n")

    if "k1qf2" in line_to_thin.vars.get_table().name:
        opt_tune = line_to_thin.match(
            method="4d",
            # start=line_to_thin.element_names[0], end=line_to_thin.element_names[-1],
            # init=target_twiss.get_twiss_init(0),
            vary=[
                xt.VaryList(
                    [
                        "k1qf4",
                        "k1qf2",
                        "k1qd3",
                        "k1qd1",
                    ],
                    step=1e-8,
                    tag="quad",
                ),
            ],
            targets=[
                # xt.TargetSet(at=xt.END, mux=target_twiss.qx, muy=target_twiss.qy, tol=1e-5),
                xt.TargetSet(
                    qx=target_twiss.qx, qy=target_twiss.qy, tol=1e-5, tag="tune"
                ),
                # xt.TargetSet(betx=target_twiss['betx','ip.8'], bety=target_twiss['bety','ip.8'], at='ip.8', tol=1e-5),
            ],
        )

    elif "kqf2" in line_to_thin.vars.get_table().name:
        opt_tune = line_to_thin.match(
            method="4d",
            # start=line_to_thin.element_names[0], end=line_to_thin.element_names[-1],
            # init=target_twiss.get_twiss_init(0),
            vary=[
                xt.VaryList(
                    [
                        "kqf2",
                        "kqf4",
                        "kqf6",
                        "kqd1",
                        "kqd3",
                        "kqd5",
                    ],
                    step=1e-8,
                    tag="quad",
                ),
            ],
            targets=[
                # xt.TargetSet(at=xt.END, mux=target_twiss.qx, muy=target_twiss.qy, tol=1e-5),
                xt.TargetSet(
                    qx=target_twiss.qx, qy=target_twiss.qy, tol=1e-5, tag="tune"
                ),
                # xt.TargetSet(betx=target_twiss['betx','ip.8'], bety=target_twiss['bety','ip.8'], at='ip.8', tol=1e-5),
            ],
        )

    opt_tune.solve()

    opt_chroma = line_to_thin.match(
        method="4d",
        vary=[
            xt.VaryList(
                [
                    "sf.k2n.chroma.knob",
                    "sd.k2n.chroma.knob",
                ],
                step=1e-3,
                tag="sext",
            ),
        ],
        targets=[
            xt.TargetSet(
                dqx=target_twiss.dqx, dqy=target_twiss.dqy, tol=1e-2, tag="chrom"
            ),
        ],
    )
    opt_chroma.solve()

    # Inspect optimization outcome
    opt_tune.target_status()
    opt_tune.vary_status()
    opt_chroma.target_status()
    opt_chroma.vary_status()

    tw_thin_4d_no_rad = line_to_thin.twiss(method="4d")

    logger.info("After rematching:")
    logger.info("Tunes thick model:")
    logger.info(target_twiss.qx, target_twiss.qy)
    logger.info("Tunes thin model:")
    logger.info(tw_thin_4d_no_rad.qx, tw_thin_4d_no_rad.qy)

    logger.info("Beta beating at ips:")
    logger.info(
        "H:",
        np.max(
            np.abs(
                tw_thin_4d_no_rad.rows["ip.*"].betx / target_twiss.rows["ip.*"].betx - 1
            )
        ),
    )
    logger.info(
        "V:",
        np.max(
            np.abs(
                tw_thin_4d_no_rad.rows["ip.*"].bety / target_twiss.rows["ip.*"].bety - 1
            )
        ),
    )

    # logger.info('Number of elements: ', len(line))

    logger.info("Change on arc quadrupoles:")
    logger.info(opt_tune.log().vary[-1] / opt_tune.log().vary[0] - 1)

    logger.info("\n Beta at the IPs:")
    tw_thin_4d_no_rad.rows["ip.*"].cols["betx bety"].show()

    return


def match_tune_chroma(line, target_twiss, method="6d", machine="FCCee"):
    if machine == "FCCee":
        if "k1qf2" in line.vars.get_table().name:
            opt_tune = line.match(
                method=method,
                vary=[
                    xt.VaryList(
                        [
                            "k1qf4",
                            "k1qf2",
                            "k1qd3",
                            "k1qd1",
                        ],
                        step=1e-8,
                        tag="quad",
                    ),
                ],
                targets=[
                    xt.TargetSet(
                        qx=target_twiss.qx, qy=target_twiss.qy, tol=1e-5, tag="tune"
                    ),
                ],
            )
            opt_tune.solve()

        elif "kqf2" in line.vars.get_table().name:
            opt_tune = line.match(
                method=method,
                vary=[
                    xt.VaryList(
                        [
                            "kqf2",
                            "kqf4",
                            "kqf6",
                            "kqd1",
                            "kqd3",
                            "kqd5",
                        ],
                        step=1e-8,
                        tag="quad",
                    ),
                ],
                targets=[
                    xt.TargetSet(
                        qx=target_twiss.qx, qy=target_twiss.qy, tol=1e-5, tag="tune"
                    ),
                ],
            )
            opt_tune.solve()

        opt_chroma = line.match(
            method=method,
            vary=[
                xt.VaryList(
                    [
                        "sf.k2n.chroma.knob",
                        "sd.k2n.chroma.knob",
                    ],
                    step=1e-3,
                    tag="sext",
                ),
            ],
            targets=[
                xt.TargetSet(
                    dqx=target_twiss.dqx, dqy=target_twiss.dqy, tol=1e-2, tag="chrom"
                ),
            ],
        )
        opt_chroma.solve()

    elif machine == "LHC":
        if "dqx.b1" in line.vars.get_table().name:
            opt_tune = line.match(
                method=method,
                vary=[
                    xt.VaryList(
                        [
                            "dqx.b1",
                            "dqy.b1",
                        ],
                        step=1e-8,
                        tag="quad",
                    ),
                ],
                targets=[
                    xt.TargetSet(
                        qx=target_twiss.qx, qy=target_twiss.qy, tol=1e-5, tag="tune"
                    ),
                ],
            )
            opt_tune.solve()

        opt_chroma = line.match(
            method=method,
            vary=[
                xt.VaryList(
                    [
                        "dqpx.b1",
                        "dqpy.b1",
                    ],
                    step=1e-3,
                    tag="sext",
                ),
            ],
            targets=[
                xt.TargetSet(
                    dqx=target_twiss.dqx, dqy=target_twiss.dqy, tol=1e-2, tag="chrom"
                ),
            ],
        )
        opt_chroma.solve()

    else:
        raise Exception("The matching of asked machine is not suported yet!")

    opt_tune.target_status()
    opt_tune.vary_status()
    opt_chroma.target_status()
    opt_chroma.vary_status()

    return


def initial_conditions_grid(
    study,
    energy_spread=None,
    ini_cond_type=None,
    min_r_y=None,
    max_r_y=None,
    num_r_y_points=None,
    min_theta_x=None,
    max_theta_x=None,
    num_theta_x_points=None,
    r_range_x=(5, 10),
    r_range_y=(5, 10),
    theta_range_x=(0, 2 * np.pi),
    theta_range_y=(0, 2 * np.pi),
    delta_initial_values=None,
    num_particles=None,
    rnd_seed=101,
):
    """
    Generate initial conditions grid for a given study.

    Parameters
    ----------
    study : str
        Study type. Can be 'DA', 'MA' or 'circulating_halo'.
    energy_spread : float
        Energy spread of the beam.
    ini_cond_type : str
        Type of initial condition for 'DA' and 'MA' studies. Can be 'cartesian' or 'polar'.
    min_r_y : float
        Minimum y for cartesian initial conditions or minimum radius for polar.
    max_r_y : float
        Maximum y for cartesian initial conditions or maximum radius for polar.
    num_r_y_points : int
        Number of points in y or radial plane.
    min_theta_x : float
        Minimum x for cartesian initial conditions or minimum theta for polar.
    max_theta_x : float
        Maximum x for cartesian initial conditions or minimum theta for polar.
    num_theta_x_points : int
        Number of points in x or theta plane.
    r_range_x : tuple
        Range of radial distances in phase space for horizontal coordinates for halo.
    r_range_y : tuple
        Range of radial distances in phase space for vertical coordinates for halo.
    theta_range_x : tuple
        Range of thata angles in phase space for horizontal coordinates for halo.
    theta_range_y : tuple
        Range of thata angles in phase space for vertical coordinates for halo.
    delta_initial_values : array_like
        Initial values of delta.
    num_particles : int
        Number of particles needed only for halo distribution.
    rnd_seed : int
        Random number seed.

    Returns for 'MA' and 'DA'
    -------
    x_normalized : array_like
        Normalized x coordinates of the particles.
    y_normalized : array_like
        Normalized y coordinates of the particles.
    delta_init : array_like
        Initial values of delta.
    num_theta_x_points : int
        Number of points in x plane.
    num_r_y_points : int
        Number of points in y plane.
    num_delta : int
        Number of initial values of delta.
    num_particles : int
        Number of particles.

    Returns for 'circulating_halo'
    -------
    x_normalized : array_like
        Normalized x coordinates of the particles.
    y_normalized : array_like
        Normalized y coordinates of the particles.
    px_normalized : array_like
        Normalized px coordinates of the particles.
    py_normalized : array_like
        Normalized py coordinates of the particles.
    """

    np.random.seed(rnd_seed)

    if min_r_y is None:
        if study in ["DA", "MA"]:
            min_r_y = 0

    if max_r_y is None:
        if study == "DA":
            max_r_y = 50
        elif study == "MA":
            max_r_y = 30

    if num_r_y_points is None:
        if study == "DA":
            num_r_y_points = 51
        elif study == "MA":
            num_r_y_points = 31

    if min_theta_x is None:
        if study == "DA":
            min_theta_x = -20
        elif study == "MA":
            min_theta_x = np.pi / 4

    if max_theta_x is None:
        if study == "DA":
            max_theta_x = 20
        elif study == "MA":
            max_theta_x = np.pi / 4

    if num_theta_x_points is None:
        if study == "DA":
            num_theta_x_points = 41
        elif study == "MA":
            num_theta_x_points = 1

    if delta_initial_values is None:
        if study == "DA":
            delta_initial_values = 0
        elif study == "MA":
            delta_initial_values = np.linspace(
                -25 * energy_spread, 25 * energy_spread, 51
            )

    if study == "DA":
        if ini_cond_type is None or ini_cond_type == "cartesian":
            x_norm_points = np.linspace(min_theta_x, max_theta_x, num_theta_x_points)
            y_norm_points = np.linspace(min_r_y, max_r_y, num_r_y_points)
            x_norm_grid, y_norm_grid = np.meshgrid(x_norm_points, y_norm_points)
            x_normalized = x_norm_grid.flatten()
            y_normalized = y_norm_grid.flatten()

        elif ini_cond_type == "polar":
            x_normalized, y_normalized, r_xy, theta_xy = xp.generate_2D_polar_grid(
                r_range=(min_r_y, max_r_y),  # beam sigmas
                theta_range=(min_theta_x, max_theta_x),
                nr=num_r_y_points,
                ntheta=num_theta_x_points,
            )

    if study == "MA":
        if ini_cond_type is None or ini_cond_type == "polar":
            x_normalized, y_normalized, r_xy, theta_xy = xp.generate_2D_polar_grid(
                r_range=(min_r_y, max_r_y),  # beam sigmas
                theta_range=(min_theta_x, max_theta_x),
                nr=num_r_y_points,
                ntheta=num_theta_x_points,
            )

        elif ini_cond_type == "cartesian":
            x_norm_points = np.linspace(min_theta_x, max_theta_x, num_theta_x_points)
            y_norm_points = np.linspace(min_r_y, max_r_y, num_r_y_points)
            x_norm_grid, y_norm_grid = np.meshgrid(x_norm_points, y_norm_points)
            x_normalized = x_norm_grid.flatten()
            y_normalized = y_norm_grid.flatten()

    if study in ["DA", "MA"]:
        num_delta = np.size(delta_initial_values)
        num_particles = num_delta * num_theta_x_points * num_r_y_points
        if num_delta != 1:
            x_normalized = np.tile(x_normalized, num_delta)
            y_normalized = np.tile(y_normalized, num_delta)
            delta_init = np.repeat(
                delta_initial_values, np.size(x_normalized) / num_delta
            )
        else:
            delta_init = delta_initial_values

    if study == "circulating.halo":
        (x_normalized, px_normalized, r_points, theta_points) = (
            xp.generate_2D_uniform_circular_sector(
                num_particles=num_particles,
                r_range=r_range_x,  # beam sigmas
                theta_range=theta_range_x,
            )
        )

        (y_normalized, py_normalized, r_points, theta_points) = (
            xp.generate_2D_uniform_circular_sector(
                num_particles=num_particles,
                r_range=r_range_y,  # beam sigmas
                theta_range=theta_range_y,
            )
        )
        return (x_normalized, y_normalized, px_normalized, py_normalized)

    return (
        x_normalized,
        y_normalized,
        delta_init,
        num_theta_x_points,
        num_r_y_points,
        num_delta,
        num_particles,
    )


def univariate_q_gaussian(size, q, beta=1):
    """
    Generate univariate q-Gaussian samples with an arbitrary β.
    """

    if q == 1:
        # Standard Gaussian with variance 1/(2β)
        return np.random.normal(scale=np.sqrt(1 / (2 * beta)), size=size)

    elif q > 1:
        # Heavy-tailed case: Variance rescaling
        nu = 2 / (q - 1) - 1  # Degrees of freedom
        W = np.random.gamma(shape=nu / 2, scale=2 / nu, size=size)
        Z = np.random.normal(size=size)
        return Z / np.sqrt(W * beta)

    elif q < 1:
        # Compact support: Rejection sampling
        samples = []
        while len(samples) < size:
            Z = np.random.uniform(-1, 1, size=1)  # Proposal
            pdf_ratio = (1 - (1 - q) * beta * Z**2) ** (1 / (1 - q))
            if uniform.rvs() < pdf_ratio:
                samples.append(Z[0])

    return np.array(samples) * np.sqrt(1 / beta)  # Adjust scaling


def multivariate_q_gaussian(mean, cov, q, beta=1, size=1):
    """
    Generate multivariate q-Gaussian samples for any beta value.
    """
    mean = np.asarray(mean)
    d = len(mean)  # Dimensionality
    # Decompose covariance matrix: Σ = L L^T (Cholesky)
    L = cholesky(cov, lower=True)
    # Generate independent q-Gaussian samples
    Z = np.array(
        [univariate_q_gaussian(size, q, beta) for _ in range(d)]
    ).T  # Shape (size, d)
    # Transform into correlated samples
    samples = Z @ L.T + mean  # Apply covariance structure

    return samples


def initial_conditions_distribution(
    twiss,
    normalized_emittance_x,
    normalized_emittance_y,
    emittance_zeta,
    number_particles=500,
    qq=1,
    bb=1,
    rnd_seed=101,
):
    """
    Generate initial conditions of particles in phase space.

    Parameters
    ----------
    twiss : xtrack.Twiss
        Twiss data of the machine.
    normalized_emittance_x : float
        Normalized emittance in x.
    normalized_emittance_y : float
        Normalized emittance in y.
    emittance_zeta : float
        Longitudinal emittance.
    number_particles : int
        Number of particles.
    qq : float
        q parameter of the q-Gaussian distribution.
    bb : float
        beta parameter of the q-Gaussian distribution.
    rnd_seed : int
        Random seed.

    Returns
    -------
    x, px, y, py, zeta, delta : tuple of arrays
        Initial conditions of particles in phase space.
    """
    np.random.seed(rnd_seed)

    closed_orbit = [
        twiss.x[0],
        twiss.px[0],
        twiss.y[0],
        twiss.py[0],
        twiss.zeta[0],
        twiss.delta[0],
    ]

    covariance = twiss.get_beam_covariance(
        nemitt_x=normalized_emittance_x,
        nemitt_y=normalized_emittance_y,
        gemitt_zeta=emittance_zeta,
    )

    if qq == 1:
        part_inj = np.random.multivariate_normal(
            mean=closed_orbit, cov=covariance.Sigma[0], size=number_particles
        )
    else:
        part_inj = multivariate_q_gaussian(
            closed_orbit, covariance, qq, beta=bb, size=number_particles
        )

    x = part_inj[:, 0]
    px = part_inj[:, 1]
    y = part_inj[:, 2]
    py = part_inj[:, 3]
    zeta = part_inj[:, 4]
    delta = part_inj[:, 5]

    return (x, px, y, py, zeta, delta)


def get_off_momentum_twiss(line, delta_offset):
    """
    Get the twiss parameters for an off-momentum closed orbit.

    If the closed orbit can be found directly, this function simply calls
    `line.twiss` with the given `delta_offset`. Otherwise, it performs a
    search for the closed orbit by starting from the on-momentum orbit and
    gradually increasing the delta offset.

    For a null delta offset this function returns the on-momentum twiss.

    Parameters
    ----------
    line : Line
        The lattice to be used.
    delta_offset : float
        The off-momentum value.

    Returns
    -------
    tw : Twiss
        The twiss parameters for the off-momentum closed orbit.
    """
    try:
        # Try to find the closed orbit directly
        return line.twiss(eneloss_and_damping=True, delta0=delta_offset)
    except Exception:
        # If the closed orbit can't be found directly, perform a search
        ini_delta = delta_offset / 2
        step_delta = delta_offset / 10
        fin_delta = delta_offset + step_delta
        co_guess = line.find_closed_orbit(delta0=ini_delta - step_delta)
        for delta in np.arange(ini_delta, fin_delta, step_delta):
            co_guess = line.find_closed_orbit(co_guess=co_guess, delta0=delta)
        # Now find the twiss parameters for the off-momentum closed orbit
        return line.twiss(
            eneloss_and_damping=True, co_guess=co_guess, delta0=delta_offset
        )


def generate_particle_distribution(
    line, study_param, particle_capacity=None, q_factor=1, b_factor=1, rnd_seed=101
):

    if particle_capacity is None:
        capacity = study_param["number_particles"]
    else:
        capacity = particle_capacity

    if "distribution" in study_param["ini_cond_type"]:
        if "matched" in study_param["ini_cond_type"]:  # relies on twiss used tw_matched
            delta_offset = study_param["ini_cond_energy_offset"]
            tw_matched = get_off_momentum_twiss(line, delta_offset)
            x_in, px_in, y_in, py_in, zeta_in, delta_in = (
                initial_conditions_distribution(
                    tw_matched,
                    study_param["ini_cond_nemittance_x"],
                    study_param["ini_cond_nemittance_y"],
                    study_param["ini_cond_bunch_length"]
                    * study_param["ini_cond_energy_spread"],
                    number_particles=study_param["number_particles"],
                    qq=q_factor,
                    bb=b_factor,
                    rnd_seed=rnd_seed,
                )
            )

        else:
            raise ValueError(f"Unknown initial condition!")

        particles = line.build_particles(
            _capacity=capacity,
            x=x_in,
            px=px_in,
            y=y_in,
            py=py_in,
            zeta=zeta_in,
            delta=delta_in,
        )

    return particles


def generate_particle_grid(
    line,
    study_param,
    particle_capacity=None,
    ini_cond_type=None,
    min_r_y=None,
    max_r_y=None,
    num_r_y_points=None,
    min_theta_x=None,
    max_theta_x=None,
    num_theta_x_points=None,
    r_range_x=(5, 10),
    r_range_y=(5, 10),
    theta_range_x=(0, 2 * np.pi),
    theta_range_y=(0, 2 * np.pi),
    delta_initial_values=None,
    rnd_seed=101,
):

    tw = line.twiss(eneloss_and_damping=True)
    ref_part = line.particle_ref
    if "grid" in study_param["ini_cond_type"]:
        # The longitudinal closed orbit needs to be manually supplied for now
        zeta_co = tw.zeta[0]
        delta_co = tw.delta[0]
        if "circulating.halo" in study_param["ini_cond_type"]:
            # Circulating halo beam physical coordinates

            (x_normalized, y_normalized, px_normalized, py_normalized) = (
                initial_conditions_grid(
                    "circulating.halo",
                    r_range_x=r_range_x,
                    r_range_y=r_range_y,
                    theta_range_x=theta_range_x,
                    theta_range_y=theta_range_y,
                    num_particles=study_param["number_particles"],
                    rnd_seed=rnd_seed,
                )
            )

            print(
                f"Paramter sigma_z > 0, preparing a longitudinal distribution matched to the RF bucket"
            )
            zeta, delta = xp.generate_longitudinal_coordinates(
                line=line,
                num_particles=study_param["number_particles"],
                distribution="gaussian",
                sigma_z=study_param["ini_cond_bunch_length"],
                particle_ref=ref_part,
            )
            zeta = zeta + zeta_co
            delta = delta + delta_co

            grid_details = {}

        elif any(ii in study_param["ini_cond_type"] for ii in ["DA", "MA"]):
            found = next(
                ii for ii in ["DA", "MA"] if ii in study_param["ini_cond_type"]
            )
            (
                x_normalized,
                y_normalized,
                delta_init,
                num_theta_x_points,
                num_r_y_points,
                num_delta,
                num_particles,
            ) = initial_conditions_grid(
                found,
                study_param["ini_cond_energy_spread"],
                ini_cond_type=ini_cond_type,
                min_r_y=min_r_y,
                max_r_y=max_r_y,
                num_r_y_points=num_r_y_points,
                min_theta_x=min_theta_x,
                max_theta_x=max_theta_x,
                num_theta_x_points=num_theta_x_points,
                delta_initial_values=delta_initial_values,
                rnd_seed=rnd_seed,
            )
            px_normalized = 0
            py_normalized = 0
            zeta = zeta_co
            delta = delta_init + delta_co

            grid_details = {
                "num_theta_x_points": num_theta_x_points,
                "num_r_y_points": num_r_y_points,
                "num_delta": num_delta,
                "num_particles": num_particles,
            }

        else:
            raise ValueError(f"Unknown initial condition!")

        if particle_capacity is None:
            capacity = len(x_normalized)
        else:
            capacity = particle_capacity

        particles = line.build_particles(
            _capacity=capacity,
            x_norm=x_normalized,
            y_norm=y_normalized,
            px_norm=px_normalized,
            py_norm=py_normalized,
            nemitt_x=study_param["ini_cond_nemittance_x"],
            nemitt_y=study_param["ini_cond_nemittance_y"],
            zeta=zeta,
            delta=delta,
        )

    return (particles, grid_details)


def install_beam_beam_elements(
    line,
    normalized_emittance_x,
    normalized_emittance_y,
    bunch_length,
    bunch_population,
    half_xing_angle,
    xing_plane,
    beamstrahlung_on,
    num_slices,
    binning_mode,
    ip_list=["ip.1", "ip.3", "ip.5", "ip.7"],
):

    # set the oposit sign for the other reference particle
    particle_ref_rev = line.particle_ref.copy()
    particle_ref_rev.q0 = -particle_ref_rev.q0

    # use the revers method due to the lack of the other beam lattice (for now)
    tw_rev = line.twiss(method="4d", particle_ref=particle_ref_rev, reverse=True)

    # definition and installation of beam beam
    line.discard_tracker()  # needed to modify the line structure
    bb_elem_name = []
    sigmas = tw_rev.get_betatron_sigmas(
        nemitt_x=normalized_emittance_x, nemitt_y=normalized_emittance_y
    )
    # z_centroid, z_cuts, n_part_slice = constant_charge_slicing_gaussian(bunch_population, bunch_length, 70)
    slicer = xf.TempSlicer(n_slices=num_slices, sigma_z=bunch_length, mode=binning_mode)
    for ii in ip_list:

        bb_elem_name.append("beambeam_" + ii)

        bb_element = xf.BeamBeamBiGaussian3D(
            phi=half_xing_angle,
            alpha=xing_plane,
            other_beam_q0=particle_ref_rev.q0,
            slices_other_beam_num_particles=slicer.bin_weights
            * bunch_population,  # n_part_slice[::-1],
            slices_other_beam_zeta_center=slicer.bin_centers,  # z_centroid[::-1],
            slices_other_beam_Sigma_11=sigmas["Sigma11", ii],
            slices_other_beam_Sigma_12=sigmas["Sigma12", ii],
            slices_other_beam_Sigma_13=sigmas["Sigma13", ii],
            slices_other_beam_Sigma_14=sigmas["Sigma14", ii],
            slices_other_beam_Sigma_22=sigmas["Sigma22", ii],
            slices_other_beam_Sigma_23=sigmas["Sigma23", ii],
            slices_other_beam_Sigma_24=sigmas["Sigma24", ii],
            slices_other_beam_Sigma_33=sigmas["Sigma33", ii],
            slices_other_beam_Sigma_34=sigmas["Sigma34", ii],
            slices_other_beam_Sigma_44=sigmas["Sigma44", ii],
            slices_other_beam_zeta_bin_width_star_beamstrahlung=(
                None
                if not beamstrahlung_on
                else slicer.bin_widths_beamstrahlung / np.cos(half_xing_angle)
            ),
        )

        # bb_element.iscollective = True

        line.insert_element(bb_elem_name[-1], bb_element, at=ii)

        # switch off beambeam
        line[bb_elem_name[-1]].scale_strength = 0

    line.build_tracker()

    return bb_elem_name


def save_track_to_h5(monitor, monitor_name="0", output_dir="plots"):
    """Saves multi-particle tracking data to an HDF5 file with gzip compression."""

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"merged_data_{monitor_name}.h5")

    # Define attributes and expected NumPy types
    attributes = {
        "x": np.float32,
        "px": np.float32,
        "y": np.float32,
        "py": np.float32,
        "zeta": np.float32,
        "delta": np.float32,
        "s": np.float32,
        "at_turn": np.int32,
    }

    try:
        with h5py.File(file_path, "w") as h5f:
            for attr, dtype in attributes.items():
                data = getattr(monitor, attr, None)

                if data is not None:
                    data = np.asarray(data, dtype=dtype)  # Ensure NumPy array

                    # Handle empty arrays gracefully
                    if data.size > 0:
                        h5f.create_dataset(attr, data=data, compression="gzip")

        logger.info(f"Data successfully saved to {file_path}")

    except Exception as e:
        raise RuntimeError(f"Failed to save data to {file_path}: {e}")


def install_collimators(line, collimation_params, reference_params):
    line.discard_tracker()

    # Load collimator database and install collimators
    collimator_db = xc.CollimatorDatabase.from_json(
        collimation_params["collimator_file"],
        nemitt_x=reference_params["normalized_emittance_x"],
        nemitt_y=reference_params["normalized_emittance_y"],
    )
    collimator_db.install_geant4_collimators(verbose=False, line=line)

    # Calculate twiss parameters
    twiss_parameters = line.twiss(method="6d")

    # Update optics for collimators and build the tracker
    line.build_tracker()
    line.collimators.assign_optics(
        nemitt_x=reference_params["normalized_emittance_x"],
        nemitt_y=reference_params["normalized_emittance_y"],
        twiss=twiss_parameters,
    )

    # Discard and rebuild tracker with updated global aperture limit
    line.discard_tracker()
    line.config.global_xy_limit = 1e3

    return twiss_parameters


def _save_particles_hdf(
    particles=None, lossmap_data=None, filename="part", reduce_particles_size=False
):
    if not filename.endswith(".hdf"):
        filename += ".hdf"

    fpath = Path(filename)
    # Remove a potential old file as the file is open in append mode
    if fpath.exists():
        fpath.unlink()

    if particles is not None:
        df = particles.to_pandas(compact=True)
        if reduce_particles_size:
            for dtype in ("float64", "int64"):
                thistype_columns = df.select_dtypes(include=[dtype]).columns
                df[thistype_columns] = df[thistype_columns].astype(
                    dtype.replace("64", "32")
                )

        df.to_hdf(
            fpath,
            key="particles",
            format="table",
            mode="a",
            complevel=9,
            complib="blosc",
        )

    if lossmap_data is not None:
        for key, lm_df in lossmap_data.items():
            lm_df.to_hdf(
                fpath, key=key, mode="a", format="table", complevel=9, complib="blosc"
            )


def generate_lossmap(
    line, particles, ref_part, collimation_param, study_param, output_dir="plots"
):
    """
    Generate a loss map of particles in a lattice with scattering.

    Parameters
    ----------
    line : Line
        The lattice with scattering.
    particles : Particles
        The particles to track.
    ref_part : Particles
        The reference particles.
    collimation_param : dict
        The collimation parameters.
    study_param : dict
        The study parameters.
    output_dir : str, optional
        The directory to save the loss map. Defaults to "plots".
    impact : bool, optional
        Whether to save the impacts of the Geant4 engine. Defaults to True.

    Returns
    -------
    None
    """
    num_turns = study_param["number_of_turns"]
    impacts = xc.InteractionRecord.start(line=line)

    xc.Geant4Engine.start(
        line=line,
        particle_ref=ref_part,
        seed=collimation_param["inv2"],
        bdsim_config_file=collimation_param["bdsim_config"],
        relative_energy_cut=0.165,
        batch_mode=True,
    )
    # batch_mode = False
    line.scattering.enable()
    line.enable_time_dependent_vars = True

    for turn in range(num_turns):
        line.track(particles, num_turns=1)

        if particles._num_active_particles == 0:
            logger.warning(f"All particles lost by turn {turn}, teminating.")
            break

    particles.remove_unused_space()
    monitors, names = line.get_elements_of_type(xt.ParticlesMonitor)

    for mon, name in zip(monitors, names):
        save_track_to_h5(mon, name, output_dir)

    line.scattering.disable()
    line.enable_time_dependent_vars = False

    xc.Geant4Engine.stop()
    # print(f'Tracking {num_particles} turns done in: {time.time()-t0} s')

    impacts.stop()
    # Saving impacts table
    df = impacts.to_pandas()
    df.to_csv(os.path.join(output_dir, "impacts_line.csv"), index=False)

    aper_interp = collimation_param["aperture_interp"]
    # Make loss map
    weights = collimation_param.get("weights", "none")

    line.cycle(name_first_element="l000017$start", inplace=True)

    df_line = line.to_pandas()
    beam_start_index = df_line[df_line["name"] == study_param["start_element"]].index[0]
    max_index = df_line.index.max()
    beam_start_s = df_line[df_line["name"] == study_param["start_element"]]["s"].values[
        0
    ]
    s_max = df_line["s"].max()

    particles = particles.remove_unused_space()

    particles.s = (particles.s + beam_start_s) % s_max
    particles.at_element = (
        (particles.at_element + beam_start_index) % max_index
    ).astype(int)

    file_path = os.path.join(output_dir, f"merged_lossmap_full.json")

    if weights == "energy":
        part_mass_ratio = particles.charge_ratio / particles.chi
        part_mass = part_mass_ratio * particles.mass0
        p0c = particles.p0c
        f_x = lambda x: 1  # No modification for x
        f_px = lambda px: 1  # No modification for px
        f_y = lambda y: 1  # No modification for y
        f_py = lambda py: 1  # No modification for py
        f_zeta = lambda zeta: 1
        f_delta = lambda delta: np.sqrt(
            ((delta + 1) * p0c * part_mass_ratio) ** 2 + part_mass**2
        )
        weight_function = [f_x, f_px, f_y, f_py, f_zeta, f_delta]

    LossMap_full = xc.LossMap(
        line=line,
        part=particles,
        line_is_reversed=False,
        interpolation=aper_interp,
        weights=None,
        weight_function=weight_function,
    )
    LossMap_full.to_json(file_path)
    logger.info(f"Lossmap for all turns saved to {file_path}")

    output_file = os.path.join(output_dir, f"part.hdf")
    _save_particles_hdf(LossMap_full.part, lossmap_data=None, filename=output_file)


def madx_add_collimators(
    madx, aperture_dir="fcc-ee-lattice-V25_GHC/aperture", sequence_name="fccee_p_ring"
):
    """
    Install collimators in predefined locations in a MAD-X sequence.

    This function installs various types of collimators (primary, secondary, tertiary, and
    synchrotron radiation) in a MAD-X sequence. The collimators are installed from predefined MAD-X
    script files located in the specified aperture directory.

    Args:
        madx: MAD-X instance to which the collimators will be added
        aperture_dir (str, optional): Directory containing the collimator installation scripts.
            Defaults to "fcc-ee-lattice-V25_GHC/aperture"
        sequence_name (str, optional): Name of the MAD-X sequence where collimators will be
            installed. Defaults to "fccee_p_ring"

    Note:
        - The function expects the following MAD-X script files to be present in the aperture
        directory:
            - install_primary_secondary_collimators.madx
            - install_tertiary_collimators.madx
            - install_synchrotron_radiation_collimators.madx
            - install_synchrotron_radiation_mask.madx
        - For collimation studies, elements should be implemented as COLLIMATOR type to ensure
            correct apertures when translating to xtrack line
        - For non-collimation studies, MARKER elements are sufficient

    Returns:
        None
    """
    madx_files = [
        "install_primary_secondary_collimators.madx",
        "install_tertiary_collimators.madx",
        "install_synchrotron_radiation_collimators.madx",
        "install_synchrotron_radiation_mask.madx",
    ]

    for madx_file in madx_files:
        file_path = os.path.join(aperture_dir, madx_file)

        # Read and replace {SEQUENCE_NAME} with the actual sequence name
        with open(file_path, "r") as file:
            madx_script = file.read().replace("{SEQUENCE_NAME}", sequence_name)

        # Pass the modified script to MAD-X
        madx.input(madx_script)

    madx.use(sequence=sequence_name)

    return


def check_and_insert_aperture(line_thick, line_thin):
    """
    Check if there are any elements in the thin lattice without apertures and
    insert apertures from the thick lattice if needed.

    Parameters
    ----------
    line_thick: Line object for thick lattice
    line_thin: Line object for thin lattice
    """
    # Check which elements in the thin lattice have no aperture
    aper = line_thin.check_aperture()

    if aper.has_aperture_problem.any():
        # Get the elements with no aperture
        aper_miss = aper[aper["has_aperture_problem"]].copy()
        new_s_values = aper_miss["s"].values
        tab = line_thick.get_table()

        # Extract aperture values from thick lattice
        apers = tab.rows[tab.element_type == "LimitEllipse"].s
        aper_x = [
            line_thick[nn].a
            for nn, ee in zip(tab.name, tab.element_type)
            if ee.startswith("LimitEllipse")
        ]
        aper_y = [
            line_thick[nn].b
            for nn, ee in zip(tab.name, tab.element_type)
            if ee.startswith("LimitEllipse")
        ]

        # Interpolate apertures values along the ring
        sorted_indices = np.argsort(apers)
        aper_miss.loc[:, "a"] = np.interp(
            new_s_values, apers[sorted_indices], np.array(aper_x)[sorted_indices]
        )
        aper_miss.loc[:, "b"] = np.interp(
            new_s_values, apers[sorted_indices], np.array(aper_y)[sorted_indices]
        )

        # Insert missing aperture elements
        for idx, row in aper_miss.iterrows():
            line_thin.insert_element(
                name=str(row["name"]) + "_aper",  # Ensure string
                element=xt.LimitEllipse(a=row["a"], b=row["b"]),
                at_s=row["s"],
                s_tol=1e-3,
            )

        # Check aperture again
        new_aper = line_thin.check_aperture()
        if new_aper.has_aperture_problem.any():
            logger.warning(
                "Aperture missing even after adding missing ones, please check the lattice..."
            )
        else:
            logger.info("Aperture missing have been added successfully")


def install_two_kick_injection_bump(
    line,
    injection_marker_name,
    injection_bump_height,
    phase_adv_left_of_inj_marker=0.25,
):
    """
    Installs a two-kick injection bump in the specified accelerator line.

    injection marker and inserts markers for these kicks. It then matches the
    kick angles to achieve the desired injection bump height at the marker.

    Parameters:
    - line: Line object where the injection bump is installed.
    - injection_marker_name: Name of the injection point marker where the injection bump should be centered.
    - injection_bump_height: Desired height of the injection bump at the marker.
    - phase_adv_left_of_inj_marker: Phase advance to the left of the injection marker (default is 0.25).

    The function iteratively searches for drifts suitable for placing the kicks
    by adjusting phase advances. It then calculates the required kick angles and
    inserts the kick elements at the appropriate positions.
    """

    tw0 = line.twiss(method="4d")
    tt0 = line.get_table(attr=True)
    tt0_use = tt0.rows[
        (tt0.element_type == "Drift")
        | ((tt0.element_type == "Marker") & (tt0.name == injection_marker_name))
    ]
    index = tt0_use.name.tolist().index(injection_marker_name)
    index_left = index - 1
    index_right = index + 1
    phase_advance_left = phase_adv_left_of_inj_marker
    phase_advance_right = 0.5 - phase_advance_left
    s_shift_left = None
    s_shift_right = None

    def drift_phase_advance_x(index, length=None):
        if length is not None:
            return np.arctan2(
                1,
                tw0.rows[tt0_use.rows[index].name].betx / length
                - tw0.rows[tt0_use.rows[index].name].alfx,
            ) / (2 * np.pi)
        else:
            if tt0_use.rows[index].length[0] == 0:
                return 0
            else:
                return np.arctan2(
                    1,
                    tw0.rows[tt0_use.rows[index].name].betx
                    / tt0_use.rows[index].length[0]
                    - tw0.rows[tt0_use.rows[index].name].alfx,
                ) / (2 * np.pi)

    length_shift = lambda index, phase_advance: tw0.rows[
        tt0_use.rows[index].name
    ].betx / (
        1 / np.tan(phase_advance * 2 * np.pi) + tw0.rows[tt0_use.rows[index].name].alfx
    )
    delta_mux_func = (
        lambda l_index, r_index: tw0.rows[tt0_use.rows[r_index].name].mux
        - tw0.rows[tt0_use.rows[l_index].name].mux
    )

    jj = 0
    exit = False
    repeat = False
    while jj < 2:

        while s_shift_left is None:

            delta_mux = delta_mux_func(index_left, index)
            drift_phase_adv = drift_phase_advance_x(index_left)
            if delta_mux >= phase_advance_left:
                if delta_mux - drift_phase_adv <= phase_advance_left:
                    s_shift_left = length_shift(
                        index_left, delta_mux - phase_advance_left
                    )
                    jj += 1

                    while s_shift_right is None:

                        delta_mux = delta_mux_func(index, index_right)
                        drift_phase_adv = drift_phase_advance_x(index_right)
                        if delta_mux + drift_phase_adv >= phase_advance_right:
                            if delta_mux <= phase_advance_right:
                                s_shift_right = length_shift(
                                    index_right, phase_advance_right - delta_mux
                                )
                                jj += 1
                            else:
                                index_left = index - 1
                                index_right = index + 1
                                if phase_advance_left + 0.01 <= 0.45:
                                    phase_advance_left = phase_advance_left + 0.00001
                                else:
                                    repeat = True
                                    exit = True
                                    print(
                                        "Not possible to find requited possition for left and right kicks, search stoped!"
                                    )
                                    break
                                phase_advance_right = 0.5 - phase_advance_left
                                s_shift_left = None
                                s_shift_right = None
                                repeat = True
                                jj -= 1
                                break
                        else:
                            index_right += 1

                    if repeat:
                        break

                else:
                    index_left = index - 1
                    index_right = index + 1
                    if phase_advance_left + 0.01 <= 0.45:
                        phase_advance_left = phase_advance_left + 0.00001
                    else:
                        exit = True
                        print(
                            "Not possible to find requited possition for left and right kicks, search stoped!"
                        )
                        break
                    phase_advance_right = 0.5 - phase_advance_left
                    s_shift_left = None
                    s_shift_right = None
                    break
            else:
                index_left -= 1

        if exit:
            break

        if jj == 2:
            print(f"phase_advance_left conclude to {phase_advance_left}")
            print(f"phase_advance_right conclude to {phase_advance_right}")

    drift_name_left = tt0_use.rows[index_left].name
    drift_name_right = tt0_use.rows[index_right].name

    if s_shift_left is not None and s_shift_right is not None:
        line.discard_tracker()
        line.insert_element(
            "kick_marker_left",
            xt.Marker(),
            at_s=s_shift_left[0] + tt0_use.rows[drift_name_left].s[0],
        )
        line.insert_element(
            "kick_marker_right",
            xt.Marker(),
            at_s=s_shift_right[0] + tt0_use.rows[drift_name_right].s[0],
        )

        line.build_tracker()
        tw1 = line.twiss(method="4d")
        line.discard_tracker()

        line.vars["injection_bump.knob"] = 1

        line.vars["kick_angle_left"] = 1e-7
        line.vars["kick_angle_right"] = (
            line.vars["kick_angle_left"]
            * np.sqrt(
                tw1.rows["kick_marker_left"].betx / tw1.rows["kick_marker_right"].betx
            )[0]
        )

        line.insert_element(
            "injection_bump_kick_left",
            xt.Multipole(
                knl=[
                    0,
                ]
            ),
            at="kick_marker_left",
        )
        line["injection_bump_kick_left"].knl = "injection_bump.knob*kick_angle_left"
        line.insert_element(
            "injection_bump_kick_right",
            xt.Multipole(
                knl=[
                    0,
                ]
            ),
            at="kick_marker_right",
        )
        line["injection_bump_kick_right"].knl = "injection_bump.knob*kick_angle_right"
        line.build_tracker()
        tw2 = line.twiss(method="4d")

        opt_kick = line.match(
            method="4d",
            start="injection_bump_kick_left",
            end="kick_marker_right",
            init=tw2,
            init_at="injection_bump_kick_left",
            vary=[
                xt.VaryList(["kick_angle_left"], step=1e-8, tag="kick_left"),
            ],
            targets=[
                xt.TargetSet(
                    x=injection_bump_height,
                    at=injection_marker_name,
                    tol=1e-8,
                    tag="bump_hight",
                ),
            ],
        )
        opt_kick.solve()

        line.vars["injection_bump.knob"] = 0
        line.discard_tracker()
        line.remove("kick_marker_left")
        line.remove("kick_marker_right")
        line.build_tracker()

    return


def activate_dynamic_injection_bump(line, inject_param, twiss, peak_turn=10, dt=0):
    """
    Control the bumpers with a modulated piecewise function of time.

    The pulse is defined by the following parameters:
    - the risetime and falltime of the pulse
    - the turn at which the peak of the pulse has to be reached
    - the duration of the flat top

    The pulse is defined by a piecewise linear function of time.
    The function has the following points:
    - t=0: knob=0
    - t=peak_time - left_kick_dt - risefall_t/2: knob=0.5
    - t=peak_time - left_kick_dt: knob=1
    - t=peak_time - left_kick_dt + flattop_t: knob=1
    - t=peak_time - left_kick_dt + flattop_t + risefall_t/2: knob=0.5
    - t=peak_time - left_kick_dt + flattop_t + risefall_t: knob=0

    Parameters
    ----------
    line: line object
    inject_param: injection parameters dictionary
    twiss: twiss parameters
    peak_turn: the turn number of the peak of the pulse
    dt: time shift
    """
    # Constants
    rev_t_s = twiss.T_rev0  # revolution time in seconds
    bump_risefall_dt_s = inject_param[
        "bump_risefall_time"
    ]  # risetime and falltime of the pulse in seconds
    bump_flattop_dt_s = inject_param[
        "bump_flattop_time"
    ]  # duration of the flat top in seconds

    # Calculate the time difference between needed
    start_to_inj_point_dt_s = (
        twiss.rows[inject_param["injection_marker_name"]].s
        * rev_t_s
        / twiss.circumference
    )[0]
    left_kick_dt_s = (
        (
            twiss.rows[inject_param["injection_marker_name"]].s
            - twiss.rows["injection_bump_kick_left"].s
        )
        * rev_t_s
        / twiss.circumference
    )[0]
    right_kick_dt_s = (
        (
            twiss.rows["injection_bump_kick_right"].s
            - twiss.rows[inject_param["injection_marker_name"]].s
        )
        * rev_t_s
        / twiss.circumference
    )[0]

    # Calculate the time of the peak of the pulse from twiss start
    peak_time_s = peak_turn * rev_t_s + start_to_inj_point_dt_s + dt

    # Create the piecewise linear function
    line.functions["bump_pulse"] = xt.FunctionPieceWiseLinear(
        x=np.array(
            [
                peak_time_s - left_kick_dt_s - bump_risefall_dt_s,  # 0
                peak_time_s - left_kick_dt_s - bump_risefall_dt_s / 2,  # 0.5
                peak_time_s - left_kick_dt_s,  # 1
                peak_time_s,  # 1
                peak_time_s + right_kick_dt_s,  # 1
                peak_time_s + bump_flattop_dt_s,  # 1
                peak_time_s + bump_flattop_dt_s + bump_risefall_dt_s / 2,  # 0.5
                peak_time_s + bump_flattop_dt_s + bump_risefall_dt_s,  # 0
            ]
        ),  # s
        y=np.array([0, 0.5, 1, 1, 1, 1, 0.5, 0]),  # knob value
    )

    # Set the knob value of the injection bump to the value of the pulse
    line.vars["injection_bump.knob"] = line.functions["bump_pulse"](
        line.vars["t_turn_s"]
    )


def find_apertures(line):
    i_apertures = []
    apertures = []
    for ii, ee in enumerate(line.elements):
        if ee.__class__.__name__.startswith("Limit"):
            i_apertures.append(ii)
            apertures.append(ee)
    return np.array(i_apertures), np.array(apertures)


def find_bb_lenses(line):
    i_apertures = []
    apertures = []
    for ii, ee in enumerate(line.elements):
        if ee.__class__.__name__.startswith("BeamBeamBiGaussian3D"):
            i_apertures.append(ii)
            apertures.append(ee)
    return np.array(i_apertures), np.array(apertures)


def insert_bb_lens_bounding_apertures(line):
    # Place aperture defintions around all beam-beam elements in order to ensure
    # the correct functioning of the aperture loss interpolation
    # the aperture definitions are taken from the nearest neighbour aperture in the line
    s_pos = line.get_s_elements(mode="upstream")
    apert_idx, apertures = find_apertures(line)
    apert_s = np.take(s_pos, apert_idx)

    bblens_idx, bblenses = find_bb_lenses(line)
    bblens_names = np.take(line.element_names, bblens_idx)
    bblens_s_start = np.take(s_pos, bblens_idx)
    bblens_s_end = np.take(s_pos, bblens_idx + 1)

    # Find the nearest neighbour aperture in the line
    bblens_apert_idx_start = np.searchsorted(apert_s, bblens_s_start, side="left")
    bblens_apert_idx_end = bblens_apert_idx_start + 1

    aper_start = apertures[bblens_apert_idx_start]
    aper_end = apertures[bblens_apert_idx_end]

    idx_offset = 0
    for ii in range(len(bblenses)):
        line.insert_element(
            name=bblens_names[ii] + "_aper_start",
            element=aper_start[ii].copy(),
            at=bblens_idx[ii] + idx_offset,
        )
        idx_offset += 1

        line.insert_element(
            name=bblens_names[ii] + "_aper_end",
            element=aper_end[ii].copy(),
            at=bblens_idx[ii] + 1 + idx_offset,
        )
        idx_offset += 1


def tracking_data_process(
    tracking_data,
    monitor_twiss=None,
    norm_emit_x=None,
    norm_emit_y=None,
    sigma_z=None,
    sigma_delta=None,
    particle_id_to_use="all",
):

    # Create set of particles to use
    if particle_id_to_use == "all":
        part_mask = np.any(tracking_data.state == 1, axis=1)
    elif particle_id_to_use == "survived":
        part_mask = np.all(tracking_data.state == 1, axis=1)
    elif particle_id_to_use == "lost":
        part_mask = np.any(tracking_data.state == 0, axis=1)
    elif isinstance(particle_id_to_use, (list, np.ndarray)):
        part_mask = np.all(
            np.isin(tracking_data.particle_id, particle_id_to_use), axis=1
        )

    # After a particle is lost, a zero value is used therefor,
    # a mask with these zero locations is constracted so to set them to nan
    turns = tracking_data.at_turn[part_mask]
    turns = turns.astype(float)
    turns_mask = tracking_data.state[part_mask] == 0
    turns[turns_mask] = np.nan

    # Used coordinates
    x_cor = tracking_data.x[part_mask]
    x_cor[turns_mask] = np.nan
    px_cor = tracking_data.px[part_mask]
    px_cor[turns_mask] = np.nan
    y_cor = tracking_data.y[part_mask]
    y_cor[turns_mask] = np.nan
    py_cor = tracking_data.py[part_mask]
    py_cor[turns_mask] = np.nan
    z_cor = tracking_data.zeta[part_mask]
    z_cor[turns_mask] = np.nan
    delta_cor = tracking_data.delta[part_mask]
    delta_cor[turns_mask] = np.nan

    if monitor_twiss is not None:
        sigmas = monitor_twiss.get_betatron_sigmas(
            nemitt_x=norm_emit_x, nemitt_y=norm_emit_y
        )

        geom_emit_x = norm_emit_x / (monitor_twiss.beta0 * monitor_twiss.gamma0)
        x_s = x_cor / sigmas["sigma_x", 0]
        x_n = x_cor / np.sqrt(monitor_twiss.betx[0])
        px_s = px_cor / sigmas["sigma_px", 0]
        px_n = x_n * monitor_twiss.alfx[0] + px_cor * np.sqrt(monitor_twiss.betx[0])
        act_x = (x_n**2 + px_n**2) / 2
        phi_x = np.arctan2(-px_n, x_n)

        geom_emit_y = norm_emit_y / (monitor_twiss.beta0 * monitor_twiss.gamma0)
        y_s = y_cor / sigmas["sigma_y", 0]
        y_n = y_cor / np.sqrt(monitor_twiss.bety[0])
        py_s = py_cor / sigmas["sigma_py", 0]
        py_n = y_n * monitor_twiss.alfy[0] + py_cor * np.sqrt(monitor_twiss.bety[0])
        act_y = (y_n**2 + py_n**2) / 2
        phi_y = np.arctan2(-py_n, y_n)

        z_s = z_cor / sigma_z
        delta_s = delta_cor / sigma_delta

    else:
        x_s = np.zeros(np.shape(x_cor)) * np.nan
        x_n = np.zeros(np.shape(x_cor)) * np.nan
        px_s = np.zeros(np.shape(x_cor)) * np.nan
        px_n = np.zeros(np.shape(x_cor)) * np.nan
        act_x = np.zeros(np.shape(x_cor)) * np.nan
        phi_x = np.zeros(np.shape(x_cor)) * np.nan
        y_s = np.zeros(np.shape(x_cor)) * np.nan
        y_n = np.zeros(np.shape(x_cor)) * np.nan
        py_s = np.zeros(np.shape(x_cor)) * np.nan
        py_n = np.zeros(np.shape(x_cor)) * np.nan
        act_y = np.zeros(np.shape(x_cor)) * np.nan
        phi_y = np.zeros(np.shape(x_cor)) * np.nan
        z_s = np.zeros(np.shape(x_cor)) * np.nan
        delta_s = np.zeros(np.shape(x_cor)) * np.nan

    sigma_matrix, emitttanses = sigma_matrix_and_emittances_from_tracking(
        {
            "x": x_cor,
            "px": px_cor,
            "y": y_cor,
            "py": py_cor,
            "zeta": z_cor,
            "delta": delta_cor,
        }
    )

    x_s_dist_evol = x_cor / np.sqrt(sigma_matrix[0, 0, :])
    x_n_dist_evol = x_s_dist_evol * np.sqrt(emitttanses[0, :])
    px_s_dist_evol = px_cor / np.sqrt(sigma_matrix[1, 1, :])
    px_n_dist_evol = -x_n_dist_evol * sigma_matrix[0, 1, :] / emitttanses[
        0, :
    ] + px_cor * np.sqrt(sigma_matrix[0, 0, :] / emitttanses[0, :])
    act_x_dist_evol = (x_n_dist_evol**2 + px_n_dist_evol**2) / 2
    phi_x_dist_evol = np.arctan2(-px_n_dist_evol, x_n_dist_evol)

    y_s_dist_evol = y_cor / np.sqrt(sigma_matrix[2, 2, :])
    y_n_dist_evol = y_s_dist_evol * np.sqrt(emitttanses[2, :])
    py_s_dist_evol = py_cor / np.sqrt(sigma_matrix[3, 3, :])
    py_n_dist_evol = -y_n_dist_evol * sigma_matrix[2, 3, :] / emitttanses[
        2, :
    ] + py_cor * np.sqrt(sigma_matrix[2, 2, :] / emitttanses[2, :])
    act_y_dist_evol = (y_n_dist_evol**2 + py_n_dist_evol**2) / 2
    phi_y_dist_evol = np.arctan2(-py_n_dist_evol, y_n_dist_evol)

    z_s_dist_evol = z_cor / np.sqrt(sigma_matrix[4, 4, :])
    delta_s_dist_evol = delta_cor / np.sqrt(sigma_matrix[5, 5, :])

    particle_id_used = tracking_data.particle_id[part_mask][:, 0]

    state_org = tracking_data.state

    trackind_data_postprossesed = {
        "x": x_cor,
        "x_sigma": x_s,
        "nx": x_n,
        "px": px_cor,
        "px_sigma": px_s,
        "npx": px_n,
        "action_x": act_x,
        "phi_x": phi_x,
        "y": y_cor,
        "y_sigma": y_s,
        "ny": y_n,
        "py": py_cor,
        "py_sigma": py_s,
        "npy": py_n,
        "action_y": act_y,
        "phi_y": phi_y,
        "zeta": z_cor,
        "zeta_sigma": z_s,
        "delta": delta_cor,
        "delta_sigma": delta_s,
        "at_turn": turns,
        "state": state_org,
        "particle_id_list": particle_id_used,
        "x_sigma_using_distribution_evolution": x_s_dist_evol,
        "nx_using_distribution_evolution": x_n_dist_evol,
        "px_sigma_using_distribution_evolution": px_s_dist_evol,
        "npx_using_distribution_evolution": px_n_dist_evol,
        "action_x_using_distribution_evolution": act_x_dist_evol,
        "phi_x_using_distribution_evolution": phi_x_dist_evol,
        "y_sigma_using_distribution_evolution": y_s_dist_evol,
        "ny_using_distribution_evolution": y_n_dist_evol,
        "py_sigma_using_distribution_evolution": py_s_dist_evol,
        "npy_using_distribution_evolution": py_n_dist_evol,
        "action_y_using_distribution_evolution": act_y_dist_evol,
        "phi_y_using_distribution_evolution": phi_y_dist_evol,
        "zeta_sigma_using_distribution_evolution": z_s_dist_evol,
        "delta_sigma_using_distribution_evolution": delta_s_dist_evol,
        "emit_x": emitttanses[0, :],
        "emit_px": emitttanses[1, :],
        "emit_y": emitttanses[2, :],
        "emit_py": emitttanses[3, :],
        "emit_zeta": emitttanses[4, :],
        "emit_delta": emitttanses[5, :],
        "sigma_matrix": sigma_matrix,
    }

    return trackind_data_postprossesed


# # Sigma matrix from data
def sigma_matrix_and_emittances_from_tracking(dic_coordinates):
    antisimmetric_matrix = np.zeros((6, 6))
    antisimmetric_matrix[0, 1] = 1
    antisimmetric_matrix[1, 0] = -1
    antisimmetric_matrix[2, 3] = 1
    antisimmetric_matrix[3, 2] = -1
    antisimmetric_matrix[4, 5] = 1
    antisimmetric_matrix[5, 4] = -1

    x = dic_coordinates["x"]
    px = dic_coordinates["px"]
    y = dic_coordinates["y"]
    py = dic_coordinates["py"]
    z = dic_coordinates["zeta"]
    dd = dic_coordinates["delta"]

    turns = len(x[0, :])
    n_part = len(x[:, 0])

    # Store covariance matrices for each turn
    cov_matrices = []

    # Loop over turns
    for t in range(turns):
        # Extract data for this turn (shape: n_part × 6)
        data_turn = np.column_stack(
            (x[:, t], px[:, t], y[:, t], py[:, t], z[:, t], dd[:, t])
        )

        # Remove rows with NaN values
        data_turn = data_turn[~np.isnan(data_turn).any(axis=1)]

        # Compute covariance matrix only if data remains
        if data_turn.shape[0] > 1:
            cov_matrix = np.cov(data_turn, rowvar=False)
            # Adjust the covariance matrix by multiplying by (n-1)/n to replace Bessel's correction
            cov_matrix *= (data_turn.shape[0] - 1) / data_turn.shape[0]
        else:
            cov_matrix = np.full((6, 6), np.nan)  # If no valid data, fill with NaNs

        # Store covariance matrix
        cov_matrices.append(cov_matrix)

    # Convert to numpy array with shape (6, 6, n_turn)
    cov_matrices = np.array(cov_matrices).transpose(1, 2, 0)

    # sigma matrix 6x6xturns
    # for x -> 6xturns
    s11 = np.nanmean(x * x, axis=0)
    s12 = np.nanmean(x * px, axis=0)
    s13 = np.nanmean(x * y, axis=0)
    s14 = np.nanmean(x * py, axis=0)
    s15 = np.nanmean(x * z, axis=0)
    s16 = np.nanmean(x * dd, axis=0)
    # for px -> 6xturns
    s21 = np.nanmean(px * x, axis=0)
    s22 = np.nanmean(px * px, axis=0)
    s23 = np.nanmean(px * y, axis=0)
    s24 = np.nanmean(px * py, axis=0)
    s25 = np.nanmean(px * z, axis=0)
    s26 = np.nanmean(px * dd, axis=0)
    # for y -> 6xturns
    s31 = np.nanmean(y * x, axis=0)
    s32 = np.nanmean(y * px, axis=0)
    s33 = np.nanmean(y * y, axis=0)
    s34 = np.nanmean(y * py, axis=0)
    s35 = np.nanmean(y * z, axis=0)
    s36 = np.nanmean(y * dd, axis=0)
    # for py -> 6xturns
    s41 = np.nanmean(py * x, axis=0)
    s42 = np.nanmean(py * px, axis=0)
    s43 = np.nanmean(py * y, axis=0)
    s44 = np.nanmean(py * py, axis=0)
    s45 = np.nanmean(py * z, axis=0)
    s46 = np.nanmean(py * dd, axis=0)
    # for z -> 6xturns
    s51 = np.nanmean(z * x, axis=0)
    s52 = np.nanmean(z * px, axis=0)
    s53 = np.nanmean(z * y, axis=0)
    s54 = np.nanmean(z * py, axis=0)
    s55 = np.nanmean(z * z, axis=0)
    s56 = np.nanmean(z * dd, axis=0)
    # for py -> 6xturns
    s61 = np.nanmean(dd * x, axis=0)
    s62 = np.nanmean(dd * px, axis=0)
    s63 = np.nanmean(dd * y, axis=0)
    s64 = np.nanmean(dd * py, axis=0)
    s65 = np.nanmean(dd * z, axis=0)
    s66 = np.nanmean(dd * dd, axis=0)

    # sigma = np.array([[s11,s12,s13,s14,s15,s16],
    #                   [s21,s22,s23,s24,s25,s26],
    #                   [s31,s32,s33,s34,s35,s36],
    #                   [s41,s42,s43,s44,s45,s46],
    #                   [s51,s52,s53,s54,s55,s56],
    #                   [s61,s62,s63,s64,s65,s66]])

    sigma = cov_matrices

    # Initialize empty arrays to store the result

    sigma_dot_antisimmetric = np.zeros((6, 6, turns)) * np.nan
    emittances = np.zeros((6, turns)) * np.nan

    # Perform matrix manipulations for each slice
    for ii in range(turns):
        if np.isnan(sigma[:, :, ii]).any() or len(x[:, ii][~np.isnan(x[:, ii])]) < 119:
            logger.warning(
                "Not enough particles (poor statistics) for acurate calculation of the sigma matrix and emittances therefore, are set to Nan !"
            )
            break

        sigma_dot_antisimmetric[:, :, ii] = np.dot(
            sigma[:, :, ii], antisimmetric_matrix
        )
        eigenvalues, eigenvectors = np.linalg.eig(sigma_dot_antisimmetric[:, :, ii])

        max_indices = np.argmax(np.abs(eigenvectors), axis=0)

        # restor of the corrext order (x,y,z) of the emittances
        for jj in range(3):

            if 2 * jj in max_indices:
                indice = np.where(max_indices == 2 * jj)[0][0]
                emittances[2 * jj, ii] = np.abs(1j * eigenvalues[indice])
            elif 2 * jj + 1 in max_indices:
                indice = np.where(max_indices == 2 * jj + 1)[0][0]
                emittances[2 * jj, ii] = np.abs(1j * eigenvalues[indice])

            if 2 * jj + 1 in max_indices:
                indice = np.where(max_indices == 2 * jj + 1)[0][0]
                emittances[2 * jj + 1, ii] = np.abs(1j * eigenvalues[indice])
            elif 2 * jj in max_indices:
                indice = np.where(max_indices == 2 * jj)[0][0]
                emittances[2 * jj + 1, ii] = np.abs(1j * eigenvalues[indice])

    return (cov_matrices, emittances)


def pynaff_tune_calculation(
    q_coordinates,
    pq_coordinates=None,
    particle_id_list=None,
    number_harmonics=1,
    data_skipped_from_start=0,
    remove_nan_from_data="no",
):

    # Dataframe input
    results = np.zeros((np.shape(q_coordinates)[0], number_harmonics * 4 + 1)) * np.nan
    columns = ["particle_id"]
    for ii in range(number_harmonics):
        columns = columns + [f"Q{ii+1}", f"A{ii+1}", f"Re[A{ii+1}]", f"Im[A{ii+1}]"]

    jj = 0
    for ii in range(np.shape(q_coordinates)[0]):

        if particle_id_list is not None:
            results[jj, 0] = particle_id_list[ii]
        else:
            results[jj, 0] = ii

        if remove_nan_from_data == "yes":
            q_data = q_coordinates[ii, :][~np.isnan(q_coordinates[ii, :])]
            if pq_coordinates is not None:
                pq_data = pq_coordinates[ii, :][~np.isnan(pq_coordinates[ii, :])]
                q_ef_data = q_data - 1j * pq_data - np.mean(q_data - 1j * pq_data)
            else:
                q_ef_data = q_data - np.mean(q_data)

        elif remove_nan_from_data == "no":
            if pq_coordinates is not None:
                q_ef_data = (
                    q_coordinates[ii, :]
                    - 1j * pq_coordinates[ii, :]
                    - np.mean(q_coordinates[ii, :] - 1j * pq_coordinates[ii, :])
                )
            else:
                q_ef_data = q_coordinates[ii, :] - np.mean(q_coordinates[ii, :])

        tunes_amps = pnf.naff(
            q_ef_data,
            turns=len(q_ef_data) - 1,
            nterms=number_harmonics,
            skipTurns=data_skipped_from_start,
            getFullSpectrum=True,
            window=1,
        )

        for kk in range(number_harmonics):
            if kk + 1 <= np.shape(tunes_amps)[0]:
                if tunes_amps[kk, 1] > 0.5:
                    results[jj, 1 + 4 * kk] = np.abs(tunes_amps[kk, 1] - 1)
                else:
                    results[jj, 1 + 4 * kk] = np.abs(tunes_amps[kk, 1])
                results[jj, 2 + 4 * kk : 5 + 4 * kk] = tunes_amps[kk, 2:]

        jj += 1
        logger.info(ii, "/", np.shape(q_coordinates)[0])

    df_table = pd.DataFrame(results, columns=columns)
    df_table["particle_id"] = df_table["particle_id"].astype(int)

    return df_table


def naffuv_tune_calculation(
    q_coordinates,
    pq_coordinates=None,
    particle_id_list=None,
    number_harmonics=1,
    remove_nan_from_data="no",
    data_type="c",
    data_reading_step=1,
    sampling_frequency=1.0,
    frequency_window="han_1",
    amplitude_window="hft",
    modified_GS=1,
):

    control_file_input = [
        "input_data.txt",
        data_type,
        "full",
        "0",
        "500",
        str(int(data_reading_step)),
        str(float(data_reading_step)),
        str(int(number_harmonics)),
        "0",
        frequency_window,
        amplitude_window,
        str(int(modified_GS)),
        "freqiencies_and_amplitudes.txt",
    ]

    with open("naff_uv_control_file.txt", "r") as control_file:
        control_file_lines = control_file.readlines()
    jj = 0
    for ii in range(len(control_file_lines)):
        if control_file_lines[ii][0] == "#":
            continue
        else:
            control_file_lines[ii] = control_file_input[jj] + "\n"
            jj += 1
    control_file = open("naff_uv_control_file.txt", "w")
    control_file.writelines(control_file_lines)
    control_file.close()

    # Dataframe input
    results = np.zeros((np.shape(q_coordinates)[0], number_harmonics * 4 + 1)) * np.nan
    columns = ["particle_id"]
    for ii in range(number_harmonics):
        columns = columns + [f"Q{ii+1}", f"A{ii+1}", f"Re[A{ii+1}]", f"Im[A{ii+1}]"]

    jj = 0
    for ii in range(np.shape(q_coordinates)[0]):

        if particle_id_list is not None:
            results[jj, 0] = particle_id_list[ii]
        else:
            results[jj, 0] = ii

        if remove_nan_from_data == "yes":
            q_data = q_coordinates[ii, :][~np.isnan(q_coordinates[ii, :])]
            if pq_coordinates is not None:
                pq_data = pq_coordinates[ii, :][~np.isnan(pq_coordinates[ii, :])]
        elif remove_nan_from_data == "no":
            q_data = q_coordinates[ii, :]
            if pq_coordinates is not None:
                pq_data = pq_coordinates[ii, :]

        if data_type == "c":
            q_ef_data = np.array([q_data, -pq_data]).T
        elif data_type == "r":
            q_ef_data = q_data
        else:
            logger.warning("Not supported data_type value in naffuv_tune_calculation")

        np.savetxt("input_data.txt", q_ef_data, fmt="%1.16e")
        os.system("./abc")
        tunes_amps_x = np.loadtxt("freqiencies_and_amplitudes.txt")
        os.system("rm -rf input_data.txt freqiencies_and_amplitudes.txt")

        if number_harmonics == 1:
            tunes_amps = tunes_amps.reshape(number_harmonics, len(tunes_amps))
        else:
            tunes_amps = tunes_amps[tunes_amps[:, 2].argsort()[::-1], :]

        for kk in range(number_harmonics):
            if kk + 1 <= np.shape(tunes_amps)[0]:
                if tunes_amps[kk, 1] > 0.5:
                    results[jj, 1 + 4 * kk] = np.abs(tunes_amps[kk, 1] - 1)
                else:
                    results[jj, 1 + 4 * kk] = np.abs(tunes_amps[kk, 1])
                results[jj, 2 + 4 * kk : 5 + 4 * kk] = tunes_amps[kk, 2:]

        jj += 1
        logger.info(ii, "/", np.shape(q_coordinates)[0])

    df_table = pd.DataFrame(results, columns=columns)
    df_table["particle_id"] = df_table["particle_id"].astype(int)

    return df_table


# Define the Gaussian function
def gaussian(dd, mu, sigma):
    return (1 / np.sqrt(2 * np.pi * sigma**2)) * np.exp(-0.5 * ((dd - mu) / sigma) ** 2)


# Define the q-Gaussian function
def q_gaussian_pdf(dd, mu, beta, q):
    pdf = np.sqrt(beta) * np.maximum((1 + (q - 1) * beta * (dd - mu) ** 2), 0) ** (
        1 / (1 - q)
    )
    if q < 1:
        norm_fuctor = (
            2
            * np.sqrt(np.pi)
            * gamma(1 / (1 - q))
            / ((3 - q) * np.sqrt(1 - q) * gamma((3 - q) / (2 - 2 * q)))
        )
    elif q > 1:
        norm_fuctor = (
            np.sqrt(np.pi)
            * gamma((3 - q) / (2 - 2 * q))
            / (np.sqrt(q - 1) * gamma(1 / (q - 1)))
        )
    return pdf / norm_fuctor


# # Fit Gaussian or q-Gaussian function to the histogram data
def fit_distribution(data, q):
    hist, bins = np.histogram(data, bins=100, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # For Gaussian
    if q == 1:

        def error_func(params, dd, tar):
            mu, sigma = params
            return gaussian(dd, mu, sigma) - tar

        result = opt.least_squares(
            error_func,
            x0=[0, 1],
            bounds=([-np.inf, 0], [np.inf, np.inf]),
            args=(bin_centers, hist),
            loss="soft_l1",
        )

    # For q-Gaussian
    else:

        def error_func(params, dd, tar):
            mu, beta, q = params
            return q_gaussian_pdf(dd, mu, beta, q) - tar

        if q > 1:
            result = opt.least_squares(
                error_func,
                x0=[0, 1, q],
                bounds=([-np.inf, 0, 1], [np.inf, np.inf, 3]),
                args=(bin_centers, hist),
                loss="soft_l1",
            )
        elif q < 1:
            result = opt.least_squares(
                error_func,
                x0=[0, 1, q],
                bounds=([-np.inf, 0, -np.inf], [np.inf, np.inf, 1]),
                args=(bin_centers, hist),
                loss="soft_l1",
            )

    # popt_x_q = fit_distribution(x,1.1)
    # popt_y_q = fit_distribution(y,1.1)

    return result.x


def save_track_along_ring_to_h5(monitor, output_dir="plots"):
    """
    Saves monitor data (assumed shape: (num_part, 201358)) to an HDF5 file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"merged_data_along_ring.h5")

    try:
        with h5py.File(file_path, "w") as h5f:
            # Extract and store relevant properties
            for attr in ["x", "px", "y", "py", "zeta", "delta", "s", "at_turn"]:
                data = getattr(monitor, attr, None)
                if data is not None:
                    dtype = np.float32 if data.dtype.kind in "fc" else np.int32
                    h5f.create_dataset(
                        attr, data=data.astype(dtype), compression="gzip", chunks=True
                    )

        logger.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logger.info(f"Failed to save data to {file_path}: {e}")


@contextmanager
def set_directory(path: Path):
    """
    Taken from: https://dev.to/teckert/changing-directory-with-a-python-context-manager-2bj8
    """
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def resolve_and_cache_paths(iterable_obj, resolved_iterable_obj, cache_destination):
    if isinstance(iterable_obj, (dict, list)):
        for k, v in (
            iterable_obj.items()
            if isinstance(iterable_obj, dict)
            else enumerate(iterable_obj)
        ):
            possible_path = Path(str(v))
            if (
                not isinstance(v, (dict, list))
                and possible_path.exists()
                and possible_path.is_file()
            ):
                shutil.copy(possible_path, cache_destination)
                resolved_iterable_obj[k] = possible_path.name
            resolve_and_cache_paths(v, resolved_iterable_obj[k], cache_destination)


def dump_dict_to_yaml(dict_obj, file_path):
    with open(file_path, "w") as yaml_file:
        yaml.dump(dict_obj, yaml_file, default_flow_style=False, sort_keys=False)


def submit_jobs(config_dict, config_file):
    # Relative path from the config file should be relative to
    # the file itself, not to where the script is executed from
    if config_file:
        conf_path = Path(config_file).resolve()
        conf_dir = conf_path.parent
        conf_fname = conf_path.name
    else:
        conf_dir = Path().resolve()
        conf_fname = "configuration.yaml"  #'config_collimation.yaml'
        conf_path = Path(conf_dir, conf_fname)

    with set_directory(conf_dir):
        # config_dict = CONF_SCHEMA.validate(config_dict)

        sub_dict = config_dict["jobsubmission"]
        workdir = str(Path(sub_dict["working_directory"]).resolve())
        num_jobs = sub_dict["num_jobs"]
        replace_dict_in = sub_dict.get("replace_dict", {})
        executable = sub_dict.get("executable", "bash")
        mask_abspath = str(Path(sub_dict["mask"]).resolve())

        max_local_jobs = 10
        if sub_dict.get("run_local", False) and num_jobs > max_local_jobs:
            raise Exception(
                f"Cannot run more than {max_local_jobs} jobs locally,"
                f" {num_jobs} requested."
            )

        # Make a directory to copy the files for the submission
        input_cache = Path(workdir, "input_cache")
        os.makedirs(workdir)
        os.makedirs(input_cache)

        # Copy the files to the cache and replace the path in the config
        # Copy the configuration file
        if conf_path.exists():
            shutil.copy(conf_path, input_cache)
        else:
            # If the setup came from a dict a dictionary still dump it to archive
            dump_dict_to_yaml(config_dict, Path(input_cache, conf_path.name))

        exclude_keys = {
            "jobsubmission",
        }  # The submission block is not needed for running
        # Preserve the key order
        reduced_config_dict = {
            k: config_dict[k] for k in config_dict.keys() if k not in exclude_keys
        }
        resolved_config_dict = copy.deepcopy(reduced_config_dict)
        resolve_and_cache_paths(reduced_config_dict, resolved_config_dict, input_cache)

        resolved_conf_file = (
            f"for_jobs_{conf_fname}"  # config file used to run each job
        )
        dump_dict_to_yaml(resolved_config_dict, Path(input_cache, resolved_conf_file))

        # compress the input cache to reduce network traffic
        shutil.make_archive(input_cache, "gztar", input_cache)
        # for fpath in input_cache.iterdir():
        #     fpath.unlink()
        # input_cache.rmdir()

        # Set up the jobs
        inv1 = config_dict["study_parameters"]["inv1"]
        inv2 = config_dict["study_parameters"]["inv2"]

        # Creating a dictionary with inv1 and inv2 values, instead of seed
        replace_dict_base = {
            "inv1": inv1,
            "inv2": inv2,
            "config_file": resolved_conf_file,
            "input_cache_archive": str(input_cache) + ".tar.gz",
        }

        # Pass through additional replace dict option and other job_submitter flags
        if replace_dict_in:
            replace_dict = {**replace_dict_base, **replace_dict_in}
        else:
            replace_dict = replace_dict_base

        processed_opts = {"working_directory", "num_jobs", "executable", "mask"}
        submitter_opts = list(set(sub_dict.keys()) - processed_opts)
        submitter_options_dict = {op: sub_dict[op] for op in submitter_opts}

        # Send/run the jobs via the job_submitter interface
        htcondor_submit(
            mask=mask_abspath,
            working_directory=workdir,
            executable=executable,
            replace_dict=replace_dict,
            **submitter_options_dict,
        )

        logger.info("Done!")


def _read_particles_hdf(filename):
    return pd.read_hdf(filename, key="particles")


def load_output(
    directory,
    job_output_dir,
    output_file,
    match_pattern="*part.hdf*",
    imax=None,
    load_lossmap=False,
    load_particles=False,
):

    t0 = time.time()

    job_dirs = glob.glob(
        os.path.join(directory, "Job.*")
    )  # find directories to loop over

    job_dirs_sorted = []
    for i in range(len(job_dirs)):
        # Very inefficient, but it sorts the directories by their numerical index
        job_dir_idx = job_dirs.index(os.path.join(directory, "Job.{}".format(i)))
        job_dirs_sorted.append(job_dirs[job_dir_idx])

    part_hdf_files = []
    part_dataframes = []
    lossmap_dicts = []

    tqdm_ncols = 100
    tqdm_miniters = 10
    logger.info(f"Parsing directories...")
    dirs_visited = 0
    files_loaded = 0
    for i, d in tqdm(
        enumerate(job_dirs_sorted),
        total=len(job_dirs_sorted),
        ncols=tqdm_ncols,
        miniters=tqdm_miniters,
    ):
        if imax is not None and i > imax:
            break

        # print(f'Processing {d}')
        dirs_visited += 1
        output_dir = os.path.join(d, job_output_dir)
        output_files = glob.glob(os.path.join(output_dir, match_pattern))
        if output_files:
            of = output_files[0]
            part_hdf_files.append(of)
            files_loaded += 1
        else:
            logger.warning(f"No output found in {d}")

    part_merged = None
    if load_particles:
        logger.info(f"Loading particles...")
        with Pool() as p:
            part_dataframes = list(
                tqdm(
                    p.imap(_read_particles_hdf, part_hdf_files),
                    total=len(part_hdf_files),
                    ncols=tqdm_ncols,
                    miniters=tqdm_miniters,
                )
            )
        part_objects = [
            xp.Particles.from_pandas(pdf)
            for pdf in tqdm(
                part_dataframes,
                total=len(part_dataframes),
                ncols=tqdm_ncols,
                miniters=tqdm_miniters,
            )
        ]

        logger.info("Particles load finished, merging...")
        part_merged = xp.Particles.merge(
            list(
                tqdm(
                    part_objects,
                    total=len(part_objects),
                    ncols=tqdm_ncols,
                    miniters=tqdm_miniters,
                )
            )
        )

    _save_particles_hdf(particles=part_merged, lossmap_data=None, filename=output_file)

    logger.info(
        "Directories visited: {}, files loaded: {}".format(dirs_visited, files_loaded)
    )
    logger.info(f"Processing done in {time.time() -t0} s")


def generate_bash_script(
    enviroment_source="/afs/cern.ch/work/g/gnigrell/public/setup_env.sh",
    input_file="run_tracking.py",
    output_file="mask_jobsubmission.sh",
):
    # Find run_tracking.py in the same folder
    python_script_path = Path(input_file)
    if not python_script_path.exists():
        raise FileNotFoundError(f"{python_script_path} not found!")

    # Convert to absolute paths
    python_script_path = python_script_path.resolve()

    # Prepare environment source line (if provided)
    env_source_line = (
        f"source {Path(enviroment_source).resolve()}\n" if enviroment_source else ""
    )

    # Define the script content (FIX: Escaped Bash variables properly)
    script_content = f"""#!/usr/bin/env bash

# Source the Conda initialization script
#source /afs/cern.ch/work/k/kskoufar/private/miniforge3/etc/profile.d/conda.sh

# Manually set the conda base path
#export PATH=/afs/cern.ch/work/k/kskoufar/private/miniforge3/bin:$PATH

# Activate the Conda environment
#conda activate xsuite_env

PYTHON_SCRIPT={python_script_path}

# Mask variables - replaced by the script, should only be edited by experts
INPUT_ARCHIVE=%(input_cache_archive)s
INV1=%(inv1)s
INV2=%(inv2)s
CONFIGFILE=%(config_file)s

# Copy the input files to the node
cp $INPUT_ARCHIVE .
tar -xzvf *.tar.gz

#Convert inv1 and inv2 from lists to single values (fix YAML formatting)
sed -i -E "/^  inv1:/,/^  inv2:/ s/^  inv1:.*/  inv1: ${{INV1}}/" ${{CONFIGFILE}}
sed -i -E "/^  inv2:/,/^.+/ s/^  inv2:.*/  inv2: ${{INV2}}/" ${{CONFIGFILE}}

sed -i -E "/^  inv1:/,/^  inv2:/ {{/^  - /d}}" ${{CONFIGFILE}}
sed -i -E "/^  inv2:/,/^$/ {{/^  - /d}}" ${{CONFIGFILE}}

# Run the script
python $PYTHON_SCRIPT --config_file ${{CONFIGFILE}} > tracker_${{INV1}}_${{s}}.log
"""

    # Write the script safely
    temp_file = f"{output_file}.tmp"
    with open(temp_file, "w") as file:
        file.write(script_content)

    # Rename temp file to final output (atomic operation)
    Path(temp_file).rename(output_file)

    logger.info(f"Bash script generated: {output_file}")


def DA_vs_turns(
    particles,
    num_r_steps,
    num_theta_steps,
    x_norm,
    y_norm,
    delta_initial,
    delta_plots=False,
):
    if isinstance(particles, dict):
        max_turns = np.shape(particles["x"])[1] - 1  # minus 1 for the initial condition
        part_at_turn = np.nanmax(particles["at_turn"], axis=1)
    else:
        max_turns = np.max(
            particles.filter(particles.at_element == 0).at_turn
        )  # normally I should pass the maximum number (n_turn) of asked turns
        part_at_turn = particles.at_turn

    if delta_plots and np.size(delta_initial) > 1:

        for ii in np.unique(delta_initial):
            delta_index = np.where(delta_initial == ii)[0]

            x_norm_1d = x_norm[delta_index]
            y_norm_1d = y_norm[delta_index]
            part_at_turn_1d = part_at_turn[delta_index]
            x_norm_2d = x_norm_1d.reshape(num_r_steps, num_theta_steps)
            y_norm_2d = y_norm_1d.reshape(num_r_steps, num_theta_steps)
            part_at_turn_2d = part_at_turn_1d.reshape(num_r_steps, num_theta_steps)

            x_DA = np.full(num_theta_steps, np.nan)
            y_DA = np.full(num_theta_steps, np.nan)
            for jj in range(num_theta_steps):
                for ii in range(num_r_steps):
                    if part_at_turn_2d[ii, jj] != max_turns:
                        x_DA[jj] = x_norm_2d[ii, jj]
                        y_DA[jj] = y_norm_2d[ii, jj]
                        break

            min_DA = np.nanmin(np.round(np.sqrt(x_DA**2 + y_DA**2), 1))
            where_min_DA = np.where(
                np.round(np.sqrt(x_DA**2 + y_DA**2), 1) == min_DA
            )[0]

            # Plot DA using scatter and pcolormesh
            fig = plt.subplots()
            plt.scatter(x_norm_1d, y_norm_1d, c=part_at_turn_1d)
            plt.plot(x_DA, y_DA, "-", color="r", label="DA for $\delta$=%.1E" % (ii))
            plt.plot(
                x_DA[where_min_DA],
                y_DA[where_min_DA],
                "o",
                color="r",
                label="DA$_{min}$=%.1f$\sigma$" % (min_DA),
            )
            plt.xlabel(r"$\hat{x}$ [$\sqrt{\varepsilon_x}$]")
            plt.ylabel(r"$\hat{y}$ [$\sqrt{\varepsilon_y}$]")
            cb = plt.colorbar()
            cb.set_label("Lost at turn")
            plt.legend(fontsize="small", loc="best")

            fig = plt.subplots()
            plt.pcolormesh(x_norm_2d, y_norm_2d, part_at_turn_2d, shading="gouraud")
            plt.plot(x_DA, y_DA, "-", color="r", label="DA for $\delta$=%.1E" % (ii))
            plt.plot(
                x_DA[where_min_DA],
                y_DA[where_min_DA],
                "o",
                color="r",
                label="DA$_{min}$=%.1f$\sigma$" % (min_DA),
            )
            plt.xlabel(r"$\hat{x}$ [$\sqrt{\varepsilon_x}$]")
            plt.ylabel(r"$\hat{y}$ [$\sqrt{\varepsilon_y}$]")
            ax = plt.colorbar()
            ax.set_label("Lost at turn")
            plt.legend(fontsize="small", loc="best")

    else:

        if not delta_plots and np.size(delta_initial) > 1:
            closest_to_zero_delta = delta_initial[(np.abs(delta_initial - 0)).argmin()]
            delta_index = np.where(delta_initial == closest_to_zero_delta)[0]
            x_norm_1d = x_norm[delta_index]
            y_norm_1d = y_norm[delta_index]
            part_at_turn_1d = part_at_turn[delta_index]
        else:
            x_norm_1d = x_norm
            y_norm_1d = y_norm
            part_at_turn_1d = part_at_turn

        x_norm_2d = x_norm_1d.reshape(num_r_steps, num_theta_steps)
        y_norm_2d = y_norm_1d.reshape(num_r_steps, num_theta_steps)
        part_at_turn_2d = part_at_turn_1d.reshape(num_r_steps, num_theta_steps)
        x_DA = np.full(num_theta_steps, np.nan)
        y_DA = np.full(num_theta_steps, np.nan)
        for jj in range(num_theta_steps):
            for ii in range(num_r_steps):
                if part_at_turn_2d[ii, jj] != max_turns:
                    x_DA[jj] = x_norm_2d[ii, jj]
                    y_DA[jj] = y_norm_2d[ii, jj]
                    break

        min_DA = np.nanmin(np.round(np.sqrt(x_DA**2 + y_DA**2), 1))
        where_min_DA = np.where(np.round(np.sqrt(x_DA**2 + y_DA**2), 1) == min_DA)[0]

        # Plot DA using scatter and pcolormesh
        fig = plt.subplots()
        plt.scatter(x_norm_1d, y_norm_1d, c=part_at_turn_1d)
        plt.plot(x_DA, y_DA, "-", color="r", label="DA")
        plt.plot(
            x_DA[where_min_DA],
            y_DA[where_min_DA],
            "o",
            color="r",
            label="DA$_{min}$=%.1f$\sigma$" % (min_DA),
        )
        plt.xlabel(r"$\hat{x}$ [$\sqrt{\varepsilon_x}$]")
        plt.ylabel(r"$\hat{y}$ [$\sqrt{\varepsilon_y}$]")
        cb = plt.colorbar()
        cb.set_label("Lost at turn")
        plt.legend(fontsize="small", loc="best")

        fig = plt.subplots()
        plt.pcolormesh(x_norm_2d, y_norm_2d, part_at_turn_2d, shading="gouraud")
        plt.plot(x_DA, y_DA, "-", color="r", label="DA")
        plt.plot(
            x_DA[where_min_DA],
            y_DA[where_min_DA],
            "o",
            color="r",
            label="DA$_{min}$=%.1f$\sigma$" % (min_DA),
        )
        plt.xlabel(r"$\hat{x}$ [$\sqrt{\varepsilon_x}$]")
        plt.ylabel(r"$\hat{y}$ [$\sqrt{\varepsilon_y}$]")
        ax = plt.colorbar()
        ax.set_label("Lost at turn")
        plt.legend(fontsize="small", loc="best")

    return (x_DA, y_DA, where_min_DA)
