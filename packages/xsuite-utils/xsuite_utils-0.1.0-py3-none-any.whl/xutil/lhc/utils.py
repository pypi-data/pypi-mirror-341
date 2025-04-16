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

# import nafflib as pnf
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


def make_thin(line_to_thin):
    Strategy = xt.slicing.Strategy
    Teapot = xt.slicing.Teapot
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

    line_to_thin.slice_thick_elements(slicing_strategies=slicing_strategies)
