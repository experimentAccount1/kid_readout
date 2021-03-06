"""
This module handles the mapping from class name and version number to a fully-qualified class path. This allows data
that was saved using a particular class to still be loaded automatically after the class code has been updated with a
change to the data format.

It is the root of the measurement import tree, so to avoid circular imports it should not import anything from
kid_readout.measurement.
"""


def full_name(class_name, version):
    """
    Return the fully-qualified name of the given class that corresponds to the given version number.

    If `version` is None, `class_name` is treated as unversioned, in which case it can be either a bare class name
    (e.g. Measurement) or a fully-qualified class name (e.g. kid_readout.measurement.core.Measurement'). If this module
    has no entry for an unversioned class it will return the name it was passed.

    Before this version system was put in place, data was saved using fully-qualified class names with no version. Data
    saved in this format should still be readable. If the corresponding class is moved, update the unversioned entry. If
    the format changes but the old code is preserved somewhere, update the original fully-qualified class name to point
    to the preserved class.

    Parameters
    ----------
    class_name : str
        The class name to look up.
    version : int (None for unversioned classes)
        The version number.

    Returns
    -------
    str
        The fully-qualified class name corresponding to `class_name` and `version`, if applicable.

    Raises
    ------
    ValueError
        If `class_name` is listed as versioned here but `version` is None.
    """
    if version is None:
        if class_name in _versioned:
            raise ValueError("{} is versioned but version number is None".format(class_name))
        return _unversioned.get(class_name, class_name)
    else:
        return _versioned[class_name][version]


def latest_version_number(class_name):
    """

    Parameters
    ----------
    class_name : str
        The class name to look up.

    Returns
    -------
    int
        The latest version number for the given class.

    """
    try:
        return max(_versioned[class_name].keys())
    except KeyError:
        raise ValueError("Class {} has no version information.".format(class_name))


# This dict should include entries for all classes with version information that are saved to disk.
# Convention: when a version number is deprecated, add the version number to the end of the name of the class that
# should now load it.
_versioned = {'Measurement': {0: 'kid_readout.measurement.core.Measurement'},
              'MeasurementList': {0: 'kid_readout.measurement.core.MeasurementList'},
              'CornerCases': {0: 'kid_readout.measurement.test.utilities.CornerCases'},
              'ADCSnap': {0: 'kid_readout.measurement.misc.ADCSnap'},
              'RoachMeasurement': {0: 'kid_readout.measurement.basic.RoachMeasurement'},
              'RoachStream': {0: 'kid_readout.measurement.basic.RoachStream0',
                              1: 'kid_readout.measurement.basic.RoachStream'},
              'SingleStream': {0: 'kid_readout.measurement.basic.SingleStream0',
                               1: 'kid_readout.measurement.basic.SingleStream'},
              'StreamArray': {0: 'kid_readout.measurement.basic.StreamArray0',
                              1: 'kid_readout.measurement.basic.StreamArray'},
              'SingleSweep': {0: 'kid_readout.measurement.basic.SingleSweep'},
              'SweepArray': {0: 'kid_readout.measurement.basic.SweepArray'},
              'SingleSweepStream': {0: 'kid_readout.measurement.basic.SingleSweepStream'},
              'SweepStreamArray': {0: 'kid_readout.measurement.basic.SweepStreamArray'},
              'SweepStreamList': {0: 'kid_readout.measurement.basic.SweepStreamList'},
              'SingleSweepStreamList': {0: 'kid_readout.measurement.basic.SingleSweepStreamList'},
              'Scan': {0: 'kid_readout.measurement.basic.Scan'},
              'MMWSweepList': {0: 'kid_readout.measurement.mmw_source_sweep.MMWSweepList'},
              'DistilledSweep': {0: 'kid_readout.analysis.resonator.test.distill.DistilledSweep'},
              }

# This dict includes the IO implementations, which have no version numbers, as well as any classes that have no version
# information. For these, it should map fully-qualified class name to fully-qualified class name.
_unversioned = {'Dictionary': 'kid_readout.measurement.io.memory.Dictionary',
                'NCFile': 'kid_readout.measurement.io.nc.NCFile',
                'NumpyDirectory': 'kid_readout.measurement.io.npy.NumpyDirectory',
                # All of the pre-versioned data formats are identical to version 0 formats.
                # These are the fully-qualified class names that were saved before versioning was implemented.
                'kid_readout.measurement.basic.RoachStream': 'kid_readout.measurement.basic.RoachStream0',
                'kid_readout.measurement.basic.SingleStream': 'kid_readout.measurement.basic.SingleStream0',
                'kid_readout.measurement.basic.StreamArray': 'kid_readout.measurement.basic.StreamArray0',
                # Add entries for these if the corresponding classes are updated past version 0.
                #'kid_readout.measurement.basic.SingleSweep': 'kid_readout.measurement.?',
                #'kid_readout.measurement.basic.SweepArray': 'kid_readout.measurement.?',
                #'kid_readout.measurement.basic.SingleSweepStream': 'kid_readout.measurement.?',
                #'kid_readout.measurement.basic.SweepStreamArray': 'kid_readout.measurement.?',
                #
                }
