"""
Miscellaneous Support.

.. rubric: Functions
.. autosummary::

    ~axes_to_dict
    ~check_value_in_list
    ~compare_float_dicts
    ~convert_units
    ~dict_device_factory
    ~dynamic_import
    ~flatten_lists
    ~get_run_orientation
    ~get_solver
    ~istype
    ~list_orientation_runs
    ~load_yaml
    ~load_yaml_file
    ~roundoff
    ~solver_factory
    ~solvers
    ~unique_name

.. rubric: Symbols
.. autosummary::

    ~IDENTITY_MATRIX_3X3
    ~SOLVER_ENTRYPOINT_GROUP

.. rubric: Custom Data Types
.. autosummary::

    ~AnyAxesType
    ~AxesArray
    ~AxesDict
    ~AxesList
    ~AxesTuple

.. rubric: Custom Preprocessors
.. autosummary::

    ~ConfigurationRunWrapper

.. rubric: Custom Exceptions
.. autosummary::

    ~Hklpy2Error
    ~ConfigurationError
    ~ConstraintsError
    ~DiffractometerError
    ~LatticeError
    ~CoreError
    ~ReflectionError
    ~SampleError
    ~SolverError
    ~SolverNoForwardSolutions
"""

import logging
import math
import pathlib
import sys
import uuid
import warnings
from collections.abc import Iterable
from importlib.metadata import entry_points
from typing import Any
from typing import Type
from typing import Union

import numpy
import numpy.typing
import pandas as pd
import pint
import tqdm
import yaml
from ophyd import Component
from ophyd import Device

logger = logging.getLogger(__name__)

IDENTITY_MATRIX_3X3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
"""Identity matrix, 2-D, 3 rows, 3 columns."""

SOLVER_ENTRYPOINT_GROUP = "hklpy2.solver"
"""Name by which |hklpy2| backend |solver| classes are grouped."""

DEFAULT_START_KEY = "diffractometers"

# Custom data types

AxesArray = numpy.typing.NDArray[float]
"""Numpy array of axes values."""

AxesDict = dict[str, float]
"""Dictionary of axes names and values."""

AxesList = list[float, ...]
"""List of axes values."""

AxesTuple = tuple[float, ...]
"""Tuple of axes values."""

AnyAxesType = Union[AxesArray, AxesDict, AxesList, AxesTuple]
"""
Any of these types are used to describe both pseudo and real axes.

=============   =========================   ====================
description     example                     type annotation
=============   =========================   ====================
dict            {"h": 0, "k": 1, "l": -1}   AxesDict
namedtuple      (h=0.0, k=1.0, l=-1.0)      AxesTuple
numpy array     numpy.array([0, 1, -1])     AxesArray
ordered list    [0, 1, -1]                  AxesList
ordered tuple   (0, 1, -1)                  AxesTuple
=============   =========================   ====================
"""


# Custom exceptions
class Hklpy2Error(Exception):
    """Any exception from the |hklpy2| package."""


class ConfigurationError(Hklpy2Error):
    """Custom exceptions from :mod:`hklpy2.blocks.configure`."""


class ConstraintsError(Hklpy2Error):
    """Custom exceptions from :mod:`hklpy2.blocks.constraints`."""


class DiffractometerError(Hklpy2Error):
    """Custom exceptions from :class:`~DiffractometerBase`."""


class LatticeError(Hklpy2Error):
    """Custom exceptions from :mod:`hklpy2.blocks.lattice`."""


class CoreError(Hklpy2Error):
    """Custom exceptions from :class:`~Core`."""


class ReflectionError(Hklpy2Error):
    """Custom exceptions from :mod:`hklpy2.blocks.reflection`."""


class SampleError(Hklpy2Error):
    """Custom exceptions from :mod:`hklpy2.blocks.sample`."""


class SolverError(Hklpy2Error):
    """Custom exceptions from a |solver|."""


class SolverNoForwardSolutions(SolverError):
    """A solver did not find any 'forward()' solutions."""


# Custom preprocessors


class ConfigurationRunWrapper:
    """
    Write configuration of supported device(s) to a bluesky run.

    EXAMPLE::

        crw = ConfigurationRunWrapper(sim4c2)
        RE.preprocessors.append(crw.wrapper)
        RE(bp.rel_scan([noisy], m1, -1.2, 1.2, 11))

    Disable the preprocessor::

        crw.enable = False  # 'True' to enable

    Remove the last preprocessor::

        RE.preprocessors.pop()

    Add another diffractometer::

        crw.devices.append(e4cv)

    .. autosummary::

        ~device_names
        ~devices
        ~enable
        ~known_bases
        ~start_key
        ~validate
        ~wrapper
    """

    devices = []
    """List of devices to be reported."""

    known_bases = []
    """
    Known device base classes.

    Any device (base class) that reports its configuration dictionary in
    the `.read_configuration()` method can be added to this tuple.
    """

    start_key = DEFAULT_START_KEY
    """Top-level key in run's metadata dictionary."""

    def __init__(self, *devices, knowns=None):
        """
        Constructor.

        EXAMPLES::

            ConfigurationRunWrapper(sim4c)
            ConfigurationRunWrapper(e4cv, e6c)

        PARAMETERS

        devices : list
            List of supported objects to be reported.
        knowns : list
            List of base classes that identify supported objects.
            (default: :class:`hklpy2.DiffractometerBase`)
        """
        from .diffract import DiffractometerBase as hklpy2_DiffractometerBase

        self.enable = True
        self.known_bases = knowns or [hklpy2_DiffractometerBase]
        self.validate(devices)
        self.devices = list(devices)

    @property
    def device_names(self) -> [str]:
        """Return list of configured device names."""
        return [dev.name for dev in self.devices]

    @property
    def enable(self) -> bool:
        """Is it permitted to write device configuration?"""
        return self._enable

    @enable.setter
    def enable(self, state: bool) -> None:
        """Set permit to write configuration."""
        self._enable = state

    def validate(self, devices) -> None:
        """Verify all are recognized objects."""
        for dev in devices:
            if not isinstance(dev, tuple(self.known_bases)):
                raise TypeError(f"{dev} is not a recognized object.")

    def wrapper(self, plan):
        """
        Bluesky plan wrapper (preprocessor).

        Writes device(s) configuration to start document metadata.

        Example::

            crw = ConfigurationRunWrapper(e4cv)
            RE.preprocessors.append(crw.wrapper)
        """
        from bluesky import preprocessors as bpp

        if not self._enable or len(self.devices) == 0:
            # Nothing to do here, move on.
            return (yield from plan)

        self.validate(self.devices)

        cfg = {dev.name: dev.configuration for dev in self.devices}

        return (yield from bpp.inject_md_wrapper(plan, {self.start_key: cfg}))


# Functions


def axes_to_dict(input: AnyAxesType, names: list[str]) -> AxesDict:
    """
    Convert any acceptable axes input to standard form (dict).

    User could provide input in several forms:

    * dict: ``{"h": 0, "k": 1, "l": -1}``
    * namedtuple: ``(h=0.0, k=1.0, l=-1.0)``
    * ordered list: ``[0, 1, -1]  (for h, k, l)``
    * ordered tuple: ``(0, 1, -1)  (for h, k, l)``

    PARAMETERS:

    input : AnyAxesType
        Positions, specified as dict, list, or tuple.
    names : [str]
        Expected names of the axes, in order expected by the solver.
    """
    if not isinstance(names, list):
        raise TypeError(f"Expected a list of names, received {names=!r}")
    for name in names:
        if not isinstance(name, str):
            raise TypeError(f"Each name should be text, received {name=!r}")
    if len(input) < len(names):
        raise ValueError(
            f"Expected at least {len(names)} axes,"
            # Always show received
            f" received {len(input)}."
        )
    if len(input) > len(names):
        warnings.warn(
            UserWarning(
                f" Extra inputs will be ignored. Expected {len(names)}."
                #
                f" Received {input=!r}, {names=!r}"
            )
        )

    axes = {}
    if istype(input, AxesDict):  # convert dict to ordered dict
        for name in names:
            value = input.get(name)
            if value is None:
                raise KeyError(
                    f"Missing axis {name!r}."
                    # Always show received
                    f" Received: {input=!r}"
                    # then
                    f" Expected: {names=!r}"
                )
            axes[name] = value

    elif istype(input, Union[AxesList, AxesTuple]):  # convert to ordered dict
        for name, value in zip(names, input):
            axes[name] = value

    else:  # TODO: #57 generic test is Iterable? AxesArray
        raise TypeError(f"Unexpected type: {input!r}.  Expected 'AnyAxesType'.")

    for name, value in axes.items():
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected a number. Received: {value!r}.")

    return axes


def check_value_in_list(title, value, examples, blank_ok=False):
    """Raise ValueError exception if value is not in the list of examples."""
    if blank_ok:
        examples.append("")
    if value not in examples:
        msg = f"{title} {value!r} unknown. Pick one of: {examples!r}"
        raise ValueError(msg)


def compare_float_dicts(a1, a2, tol=1e-4):
    """
    Compare two dictionaries.  Values are all floats.
    """
    if tol <= 0:
        raise ValueError(f"received {tol=}, should be tol >0")

    if sorted(a1.keys()) != sorted(a2.keys()):
        return False

    tests = [True]
    for k, v in a1.items():
        if isinstance(v, float):
            if tol < 1:
                test = math.isclose(a1[k], a2[k], abs_tol=tol)
            else:
                test = round(a1[k], tol) == round(a2[k], tol)
        else:
            test = a1[k] == a2[k]
        if not test:
            return False  # no need to go further
    return False not in tests


def convert_units(value: float, old_units: str, new_units: str) -> float:
    """Convert 'value' from old units to new."""
    return pint.Quantity(value, old_units).to(new_units).magnitude


def dict_device_factory(data: dict, **kwargs):
    """
    Create a ``DictionaryDevice()`` class using the supplied dictionary.

    .. index:: factory; dict_device_factory, dict_device_factory
    """
    from ophyd import Signal

    component_dict = {
        k: Component(Signal, value=v, **kwargs)
        # metadata={"description": "solver extra axis"},
        # kind="hinted",
        for k, v in data.items()
    }
    fc = type("DictionaryDevice", (Device,), component_dict)
    return fc


def dynamic_import(full_path: str) -> type:
    """
    Import the object given its import path as text.

    Motivated by specification of class names for plugins
    when using ``apstools.devices.ad_creator()``.

    EXAMPLES::

        klass = dynamic_import("ophyd.EpicsMotor")
        m1 = klass("gp:m1", name="m1")

        creator = dynamic_import("hklpy2.diffract.creator")
        fourc = creator(name="fourc")

    From the `apstools <https://github.com/BCDA-APS/apstools>`_ package.
    """
    from importlib import import_module

    import_object = None

    if "." not in full_path:
        # fmt: off
        raise ValueError(
            "Must use a dotted path, no local imports."
            f" Received: {full_path!r}"
        )
        # fmt: on

    if full_path.startswith("."):
        # fmt: off
        raise ValueError(
            "Must use absolute path, no relative imports."
            f" Received: {full_path!r}"
        )
        # fmt: on

    module_name, object_name = full_path.rsplit(".", 1)
    module_object = import_module(module_name)
    import_object = getattr(module_object, object_name)

    return import_object


def flatten_lists(xs):
    """
    Convert nested lists into single list.

    https://stackoverflow.com/questions/2158395
    """
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten_lists(x)
        else:
            yield x


def get_solver(solver_name):
    """
    Load a Solver class from a named entry point.

    ::

        import hklpy2
        SolverClass = hklpy2.get_solver("hkl_soleil")
        libhkl_solver = SolverClass()
    """
    if solver_name not in solvers():
        raise SolverError(f"{solver_name=!r} unknown.  Pick one of: {solvers()!r}")
    entries = entry_points(group=SOLVER_ENTRYPOINT_GROUP)
    return entries[solver_name].load()


def get_run_orientation(run, name=None, start_key=DEFAULT_START_KEY):
    """
    Return the orientation information dictionary from a run.

    EXAMPLE::

        In [3]: get_run_orientation(cat[9752], name="sim4c2")
        Out[3]:
        {'_header': {'datetime': '2025-02-27 15:54:33.364719',
        'hklpy2_version': '0.0.26.dev72+gcf9a65a.d20250227',
        'python_class': 'Hklpy2Diffractometer',
        'source_type': 'X-ray',
        'energy_units': 'keV',
        'energy': 12.398419843856837,
        'wavelength_units': 'angstrom',
        'wavelength': 1.0},
        'name': 'sim4c2',
        'axes': {'pseudo_axes': ['h', 'k', 'l'],
        'real_axes': ['omega', 'chi', 'phi', 'tth'],
        'axes_xref': {'h': 'h',
        'k': 'k',
        'l': 'l',
        'omega': 'omega',
        'chi': 'chi',
        'phi': 'phi',
        'tth': 'tth'},
        'extra_axes': {}},
        'sample_name': 'sample',
        'samples': {'sample': {'name': 'sample',
        'lattice': {'a': 1,
            'b': 1,
            'c': 1,
            'alpha': 90.0,
            'beta': 90.0,
            'gamma': 90.0},
        'reflections': {},
        'reflections_order': [],
        'U': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        'UB': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        'digits': 4}},
        'constraints': {'omega': {'label': 'omega',
        'low_limit': -180.0,
        'high_limit': 180.0,
        'class': 'LimitsConstraint'},
        'chi': {'label': 'chi',
        'low_limit': -180.0,
        'high_limit': 180.0,
        'class': 'LimitsConstraint'},
        'phi': {'label': 'phi',
        'low_limit': -180.0,
        'high_limit': 180.0,
        'class': 'LimitsConstraint'},
        'tth': {'label': 'tth',
        'low_limit': -180.0,
        'high_limit': 180.0,
        'class': 'LimitsConstraint'}},
        'solver': {'name': 'hkl_soleil',
        'description': "HklSolver(name='hkl_soleil', version='5.1.2', geometry='E4CV', engine_name='hkl', mode='bissector')",
        'geometry': 'E4CV',
        'real_axes': ['omega', 'chi', 'phi', 'tth'],
        'version': '5.1.2',
        'engine': 'hkl'}}


    Parameters
    ----------
    run : object
        Bluesky run object.
    name : str
        (optional)
        Name of the diffractometer. (default=None, returns all available.)
    start_key : str
        Metadata key where the orientation information is stored in the start
        document.  (default="diffractometers")
    """
    info = run.metadata["start"].get(start_key, {})
    if isinstance(name, str):
        info = info.get(name, {})
    return info


def istype(value: Any, annotation: Type) -> bool:
    """
    Check if 'value' matches the type 'annotation'.

    EXAMPLE::

        >>> istype({"a":1}, AxesDict)
        True
    """
    # https://stackoverflow.com/a/57813576/1046449
    from typeguard import TypeCheckError
    from typeguard import check_type

    try:
        check_type(value, annotation)
        return True
    except TypeCheckError:
        return False


def list_orientation_runs(catalog, limit=10, start_key=DEFAULT_START_KEY, **kwargs):
    """
    List the runs with orientation information.

    EXAMPLE::

        In [42]: list_orientation_runs(cat, limit=5, date="_header.datetime")
        Out[42]:
            scan_id      uid  sample diffractometer geometry      solver                        date
        0      9752  41f71e9  sample         sim4c2     E4CV  hkl_soleil  2025-02-27 15:54:33.364719
        1      9751  36e38bc  sample         sim4c2     E4CV  hkl_soleil  2025-02-27 15:54:33.364719
        2      9750  62e425d  sample         sim4c2     E4CV  hkl_soleil  2025-02-27 15:54:33.364719
        3      9749  18b11f0  sample         sim4c2     E4CV  hkl_soleil  2025-02-27 15:53:55.958929
        4      9748  bf9912f  sample         sim4c2     E4CV  hkl_soleil  2025-02-27 15:53:55.958929

    Returns
    -------
    Table of orientation runs: Pandas DataFrame object

    Parameters
    ----------
    catalog : object
        Instance of a databroker catalog.
    limit : int
        Limit the list to at most ``limit`` runs. (default=10)
        It could take a long time to search an entire catalog.
    start_key : str
        Metadata key where the orientation information is stored in the start
        document.  (default="diffractometers")
    **kwargs : dict[str:str]
        Keyword parameters describing data column names to be displayed. The
        value of each column name is the dotted path to the orientation
        information (in the start document's metadata).
    """
    buffer = []
    _count = 0
    columns = dict(
        sample="sample_name",
        diffractometer="name",
        geometry="solver.geometry",
        solver="solver.name",
    )
    columns.update(**kwargs)
    limit = min(limit, len(catalog.v2))
    with tqdm.tqdm(total=limit, file=sys.stdout, leave=False) as progress_bar:
        for full_uid in catalog.v2:
            _count += 1
            run = catalog.v2[full_uid]
            start_md = run.metadata.get("start", {})
            info = get_run_orientation(run, start_key=start_key)
            if info is not None:

                def get_subdict_value(biblio, full_key):
                    value = biblio
                    for key in full_key.split("."):
                        value = (value or {}).get(key)
                    return value

                for device in sorted(info):
                    orientation = info[device]
                    row = dict(
                        scan_id=start_md.get("scan_id", 0),
                        uid=full_uid[:7],
                    )
                    for f, addr in columns.items():
                        value = get_subdict_value(orientation, addr)
                        if value is not None:
                            row[f] = value
                    buffer.append(row)

            progress_bar.update()
            if _count >= limit:
                break
    return pd.DataFrame(buffer)


def load_yaml(text: str):
    """Load YAML from text."""
    return yaml.load(text, yaml.Loader)


def load_yaml_file(file):
    """Return contents of a YAML file as a Python object."""
    path = pathlib.Path(file)
    if not path.exists():
        raise FileExistsError(f"YAML file '{path}' does not exist.")
    return load_yaml(open(path, "r").read())


def roundoff(value, digits=4):
    """Round a number to specified precision."""
    return round(value, ndigits=digits) or 0  # "-0" becomes "0"


def solver_factory(solver_name: str, geometry: str, **kwargs):
    """
    Create a |solver| object with geometry and axes.
    """
    solver_class = get_solver(solver_name)
    return solver_class(geometry, **kwargs)


def solvers():
    """
    Dictionary of available Solver classes, mapped by entry point name.

    ::

        import hklpy2
        print(hklpy2.solvers())
    """
    # fmt: off
    entries = {
        ep.name: ep.value
        for ep in entry_points(group=SOLVER_ENTRYPOINT_GROUP)
    }
    # fmt: on
    return entries


def unique_name(prefix="", length=7):
    """
    Short, unique name, first 7 (at most) characters of a unique, random uuid.
    """
    return prefix + str(uuid.uuid4())[: max(1, min(length, 7))]
