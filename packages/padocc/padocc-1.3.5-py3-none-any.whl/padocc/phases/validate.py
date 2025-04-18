__author__    = "Daniel Westwood"
__contact__   = "daniel.westwood@stfc.ac.uk"
__copyright__ = "Copyright 2023 United Kingdom Research and Innovation"

import json
import random
from datetime import datetime
from typing import Optional, Union

import numpy as np
import xarray as xr

from padocc.core import BypassSwitch, LoggedOperation, ProjectOperation
from padocc.core.errors import ValidationError, worst_error
from padocc.core.filehandlers import JSONFileHandler
from padocc.core.utils import format_tuple, timestamp

SUFFIXES = []
SUFFIX_LIST = []
def mem_to_value(mem) -> float:
    """
    Convert a memory value i.e 2G into a value

    :returns:   Int value of e.g. '2G' in bytes.
    """
    suffix = mem[-1]
    return int(float(mem[:-1]) * SUFFIXES[suffix])

def value_to_mem(value) -> str:
    """
    Convert a number of bytes i.e 1000000000 into a string

    :returns:   String value of the above (1000000000 -> 1M)
    """
    suffix_index = -1
    while value > 1000:
        value = value/1000
        suffix_index += 1
    return f'{value:.0f}{SUFFIX_LIST[suffix_index]}'
        
def check_for_nan(box, bypass, logger, label=None): # Ingest into class structure
    """
    Special function for assessing if a box selection has non-NaN values within it.
    Needs further testing using different data types.
    """
    logger.debug(f'Checking nan values for {label}: dtype: {str(box.dtype)}')

    if not ('float' in str(box.dtype) or 'int' in str(box.dtype)):
        # Non numeric arrays cannot have NaN values.
        return False
    
    arr = np.array(box)

    def handle_boxissue(err):
        if isinstance(err, TypeError):
            return False
        else:
            if bypass.skip_boxfail:
                logger.warning(f'{err} - Uncaught error bypassed')
                return False
            else:
                raise err
            
    def get_origin(arr):
        if len(arr.shape) > 1:
            return get_origin(arr[0])
        else:
            return arr[0]

    if arr.size == 1:
        try:
            isnan = np.isnan(arr)
        except Exception as err:
            isnan = handle_boxissue(err)
    else:
        try:
            #print(get_origin(arr))
            isnan = np.all(arr == np.nan)
        except Exception as err:
            isnan = handle_boxissue(err)

    return isnan

def slice_all_dims(data_arr: xr.DataArray, intval: int, dim_mid: Union[dict[int,None],None] = None):
    """
    Slice all dimensions for the DataArray according 
    to the integer value."""
    shape = tuple(data_arr.shape)
    dims  = tuple(data_arr.dims)

    dim_mid = dim_mid or {}

    slice_applied = []
    for dim, d in zip(dims, shape):
        if d < 8:
            slice_applied.append(slice(0,d))
            continue

        mid = int(d/2)
        if dim_mid.get(dim,None) is not None:
            mid = dim_mid[dim]

        step = int(d/(intval*2))
        slice_applied.append(slice(mid-step,mid+step))
    return tuple(slice_applied)

def format_slice(slice: list[slice]) -> str:
    starts = []
    ends = []
    for s in slice:
        starts.append(str(s.start))
        ends.append(str(s.stop))
    return "(%s)" % ','.join(starts), "(%s)" % ','.join(ends)

def _recursive_set(source: dict, keyset: list, value):
    """
    Method for recursively setting values in a dictionary.
    """
    if len(keyset) > 1:

        # Preserve existing values
        current = {}
        if keyset[0] in source:
            current = source[keyset[0]]

        source[keyset[0]] = _recursive_set(current,keyset[1:], value)
    else:
        source[keyset[0]] = value
    return source

class PresliceSet:
    """
    Preslice Object for handling slices applied to datasets.
    """

    def __init__(self):
        self._preslice_set = {}

    def add_preslice(self, preslice: dict[slice], var: str):
        self._preslice_set[var] = preslice

    def apply(self, data_arr: xr.DataArray, var: str) -> xr.DataArray:
        """
        Apply a preslice operation to a data array"""

        if var not in self._preslice_set:
            return self._default_preslice(data_arr)
        else:
            return data_arr.isel(**self._preslice_set[var])

    def _default_preslice(self, data_arr: xr.DataArray) -> xr.DataArray:
        """
        Default preslice performs no operations on the
        data array.
        """
        return data_arr

class Report:
    """
    Special report class, capable of utilising recursive
    dictionary value-setting."""
    description = 'Special report class for recursive dictionary value-setting'

    def __init__(self, fh=None):
        self._value = fh or {}

    def __setitem__(self, index, value):
        nest = index.split('.')
        current = {}
        if nest[0] in self._value:
            current = self._value[nest[0]]
        self._value[nest[0]] = _recursive_set(current, nest[1:], value)

    def export(self):
        return self._value

    def __bool__(self):
        return bool(self._value)

    def __dict__(self):
        return self._value.get()
    
    def __repr__(self):
        return json.dumps(self._value)
    
    def __str__(self):
        return json.dumps(self._value, indent=2)

class ValidateDatasets(LoggedOperation):
    """
    ValidateDatasets object for performing validations between two
    pseudo-identical Xarray Dataset objects.

    4th Dec Note:
    Validate metadata using single NetCDF(Xarray) vs Kerchunk
    Validate data using combined NetCDF or CFA vs Kerchunk
    (for best performance)
    """

    def __init__(
            self, 
            datasets: list,
            id: str,
            filehandlers: Optional[Union[list[JSONFileHandler], list[dict]]] = None,
            dataset_labels: list = None,
            preslice_fns: list = None, # Preslice each dataset's DataArrays to make equivalent.
            logger = None,
            label: str = None,
            fh: str = None,
            logid: str = None,
            verbose: int = 0,
        ):
        """
        Initiator for the ValidateDataset Class.
        Given a list of xarray.Dataset objects, all methods applied to 
        all datasets should give the same values as an output - the 
        outputs should be equivalent.
        
        These dataset objects should be identical, just from different sources.
        """

        self._id = id
        self._datasets   = datasets

        self._labels = dataset_labels or [str(i) for i in range(len(datasets))]

        self.variables = None
        self.dimensions = None

        self.fhs = filehandlers or [{},{}]

        self._metadata_report = None
        self._data_report = None

        self._preslice_fns = preslice_fns or [PresliceSet() for d in datasets]

        if len(self._datasets) > 2:
            raise NotImplementedError(
                'Simultaneous Validation of multiple datasets is not supported.'
            )

        super().__init__(
            logger,
            label=label,
            fh=fh,
            logid=logid,
            verbose=verbose
        )

    def __str__(self):
        return f'<PADOCC Validator: {self._id}>'
    
    @property
    def pass_fail(self):
        if self._metadata_report is None or self._data_report is None:
            return None
        if self._data_report:
            return 'Fatal'
        if self._metadata_report:
            return 'Warning'
        return 'Success'
    
    @property
    def data_report(self):
        """Read-only data report"""
        return self._data_report
    
    @property
    def metadata_report(self):
        """Read-only metadata report"""
        return self._metadata_report

    @property
    def report(self):
        if self._metadata_report is None:
            return None
        
        if self._data_report is None:
            return {
                'metadata': self._metadata_report.export()
            }
        
        return {
            'report':{
                'metadata': self._metadata_report.export(),
                'data': self._data_report.export()
            }
        }

    def save_report(self, filehandler=None):

        if filehandler is not None:
            filehandler.set(self.report)
            filehandler.close()
            return
        
        if isinstance(self.fhs[0], JSONFileHandler):
            self.fhs[0].set(self._metadata_report.export())
            self.fhs[0].close()

            self.fhs[1].set(self._data_report.export())
            self.fhs[1].close()
            return
        
        raise ValueError(
            'Filehandler not provided to save report'
        )

    def replace_dataset(
            self, 
            new_ds: xr.Dataset, 
            label: str = None, 
            index: int = None, 
            dstype: str = None
        ) -> None:
        """
        Replace dataset by type, label or index.
        """

        if label is not None:
            index = self._labels.index(label)

        if dstype is not None:
            types = ['test','control']
            index = types.index(dstype)

        if index is not None:
            self._datasets[index] = new_ds
    
    def replace_preslice(
            self, 
            new_preslice: xr.Dataset, 
            label: str = None, 
            index: int = None, 
            dstype: str = None
        ) -> None:
        """
        Replace dataset by type, label or index.
        """

        if label is not None:
            index = self._labels.index(label)

        if dstype is not None:
            types = ['test','control']
            index = types.index(dstype)

        if index is not None:
            self._preslice_fns[index] = new_preslice

    def test_dataset_var(self, var):
        """
        Get a variable DataArray from the test dataset, 
        performing preslice functions.
        """
        return self._dataset_var(var, 0)
    
    def control_dataset_var(self, var):
        """
        Get a variable DataArray from the control dataset, 
        performing preslice functions.
        """
        return self._dataset_var(var, 1)

    def _dataset_var(self, var, id):
        """
        Perform preslice functions on the requested DataArray
        """
        return self._preslice_fns[id].apply(self._datasets[id][var], var)

    def validate_metadata(self, allowances: dict = None) -> dict:
        """
        Run all validation steps on this set of datasets.
        """

        # Reset for new report run
        self._metadata_report = Report()
        self.logger.info('Initialised metadata report')

        allowances = allowances or {}
        ignore_vars, ignore_dims, ignore_globals = None, None, None

        # Validate global attributes
        if 'ignore_global_attrs' in allowances:
            ignore_globals = {'ignore': allowances['ignore_global_attrs']}

        self.validate_global_attrs(allowances=ignore_globals)

        if 'ignore_variables' in allowances:
            ignore_vars = {'ignore': allowances['ignore_variables']}
        if 'ignore_dimensions' in allowances:
            ignore_dims = {'ignore': allowances['ignore_dimensions']}

        # Validate variables/dimensions
        self._validate_variables(allowances=ignore_vars)
        self._validate_dimensions(allowances=ignore_dims)

    def _validate_variables(self, allowances: dict = None):
        """
        Validate variables public method
        """
        self.logger.info('Performing validation checks: Variables')
        self._validate_selector(allowances=allowances, selector='variables')

    def _validate_dimensions(self, allowances: dict = None):
        """
        Validate dimensions public method
        """
        self.logger.info('Performing validation checks: Dimensions')
        self._validate_selector(allowances=allowances, selector='dims')

    def _validate_selector(self, allowances: dict = None, selector: str = 'variables'):
        """
        Ensure all variables/dimensions are consistent across all datasets.
        Allowances dict contains configurations for skipping some variables
        in the case for example of a virtual dimension.

        allowances:
          ignore: [list to ignore]
        """
        ignore_sels = []
        # Determine the set of selectors
        # Only able to compare two datasets at once
        test_set    = list(getattr(self._datasets[0], selector))
        control_set = list(getattr(self._datasets[1], selector))
        all_selectors = set(control_set) | set(test_set)

        ignore_attrs = {all_s:[] for all_s in all_selectors}

        # Collect ignored selectors and attributes
        allowances = allowances or {}
        if 'ignore' in allowances:
            ignore_sels = allowances['ignore']
        if 'attributes' in allowances:
            for scode in allowances['attributes']:
                s, attr = scode.split('.')
                ignore_attrs[s].append(attr)
            
        misordered = False
        if len(test_set) != len(control_set):
            misordered = True

        self.logger.info(f'Checking {selector}:')
        for order, s in enumerate(control_set):
            self.logger.info(f' - {s}')

            # Check for ignored selectors
            if s in ignore_sels:
                self._metadata_report[f'{selector}.{s}'] = {
                    'type': 'ignored'
                }
                continue
                
            # Check for correct selector order
            if not misordered:
                if test_set[order] != s:
                    misordered = True

            # Find selectors missing from the test set
            try:
                test_s = test_set[test_set.index(s)]
            except ValueError:
                # Selector missing from test set
                self._metadata_report[f'{selector}.{s}'] = {
                    'type':'missing',
                    'info':f'missing from {self._labels[0]}'
                }
                continue

            # Check equality for attributes
            self._validate_attrs(
                [
                    self._datasets[0][s].attrs,
                    self._datasets[1][s].attrs
                ], 
                source=s, ignore=ignore_attrs[s]
            )

        # Find selectors missing from the control set
        missing_from_control = set(test_set).difference(control_set)
        for mc in missing_from_control:
            self._metadata_report[f'{selector}.{mc}'] = {
                'type':'missing',
                'info':f'missing from {self._labels[1]}'
            }
        
        setattr(self, selector, set(all_selectors))

        # Set the selector here for further operations.

        if misordered:
            self._metadata_report[f'{selector}.all_{selector}'] = {
                'type': 'order'
            }

            self.logger.warning(
                f'{s} present in a different order between datasets - this has been recorded'
            )

    def validate_global_attrs(self, allowances: dict = None):
        """
        Validate the set of global attributes across all datasets
        """

        allowances = allowances or {}
        ignore = []
        if 'ignore' in allowances:
            ignore = allowances['ignore']

        attrset = []
        for d in self._datasets:
            attrset.append(d.attrs)

        self.logger.info('Checking global attributes:')
        self._validate_attrs(attrset, source='global', ignore=ignore)

    def _validate_attrs(self, attrset: list[dict], source: str = '', ignore: list = None):
        """
        Ensure all values across the sets of attributes are consistent - add results
        to the metadata report.
        """

        ignore = ignore or []
        for attr in attrset[0].keys():

            self.logger.debug(f'  > {attr}')
            # Check for ignored attributes
            if attr in ignore:
                self._metadata_report[f'attributes.{source}.{attr}'] = {
                    'type': 'ignore'
                }
                continue

            # Check for missing attributes in any of the sets
            try:
                set_of_values = []
                for index, aset in enumerate(attrset):
                    set_of_values.append(aset[attr])
            except KeyError:
                self._metadata_report[f'attributes.{source}.{attr}'] = {
                    'type': 'missing',
                    'info': f'missing from {self._labels[index]}'
                }
                continue
                
            # Check for non-equal attributes
            s = set_of_values[0]
            if not np.all(s == np.array(set_of_values[1:])):
                self._metadata_report[f'attributes.{source}.{attr}'] = {
                    'type': 'not_equal'
                }

    def validate_data(self, dim_mid: Union[dict,None] = None):
        """
        Perform data validations using the growbox method for all variable DataArrays.
        """

        if self.variables is None:
            raise ValueError(
                'Unable to validate data, please ensure metadata has been validated first.'
                'Use `validate_metadata()` method.'
            )
        
        # Reset for new report run
        self._data_report = Report()
        self.logger.info('Initialised data report')

        for dim in self.dims:
            self.logger.debug(f'Validating size of {dim}')

            try:
                testdim = self.test_dataset_var(dim)
                test_range = (
                    testdim.head(1),
                    testdim.tail(1)
                )
            except KeyError:
                self.logger.warning(f'{dim} could not be validated for data content')
                continue

            try:
                controldim = self.control_dataset_var(dim)
                control_range = (
                    controldim.head(1),
                    controldim.tail(1)
                )
            except KeyError:
                self.logger.warning(f'{dim} could not be validated for data content')
                continue

            self._validate_dimlens(
                dim,
                testdim.size,
                controldim.size
            )

            self._validate_dimvalues(
                dim,
                test_range,
                control_range
            )

        for var in self.variables:
            self.logger.debug(f'Validating shapes for {var}')
            try:
                testvar = self.test_dataset_var(var)
            except KeyError:
                self.logger.warning(f'{var} could not be validated for data content')
                continue

            try:
                controlvar = self.control_dataset_var(var)
            except KeyError:
                self.logger.warning(f'{var} could not be validated for data content')
                continue

            self._validate_shapes(var, testvar, controlvar)

            # Check access to the source data somehow here
            # Initiate growbox method - recursive increasing box size.
            self.logger.debug(f'Validating data for {var}')
            self._validate_selection(var, testvar, controlvar, dim_mid=dim_mid)

    def _validate_shapes(self, var: str, test, control, ignore=None):
        """
        Ensure all variable shapes are consistent across all datasets.

        Allowances dict contains configurations for skipping some shape tests
        in the case for example of a virtual dimension.
        """
        ignore = ignore or []

        # Check sizes against ignore list
        if 'size' not in ignore:
            if test.size != control.size:
                # Size error
                self._data_report[f'variables.size_errors.{var}'] = {
                    self._labels[0]: test.size,
                    self._labels[1]: control.size
                }

        # Check dimensions individually

        ignore_dims = []
        if 'dims' in ignore:
            ignore_dims = ignore['dims']

        test_dr, control_dr = [],[]
        dim_error = False

        # Check for consistency of number of dimensions
        if len(test.dims) != len(control.dims):
            self._data_report[f'variables.dim_errors.{var}'] = {
                    self._labels[0]: test.dims,
                    self._labels[1]: control.dims
                }
            self.logger.warning(
                f'Dimensions inconsistent for {var} - this has been reported'
            )
            return

        # Check each dimension, filter for ignores or matching sizes
        for i in range(len(control.sizes)):
            if i in ignore_dims:
                test_dr.append('i')
                control_dr.append('i')
                continue

            if test.shape[i] != control.shape[i]:
                test_dr.append(str(test.shape[i]))
                control_dr.append(str(control.shape[i]))
                dim_error = True
            else:
                test_dr.append('X')
                control_dr.append('X')
        
        # Record error if present
        if dim_error:
            self._data_report[f'variables.dim_size_errors.{var}'] = {
                    self._labels[0]: ','.join(test_dr),
                    self._labels[1]: ','.join(control_dr)
                }

    def _validate_dimvalues(self, dim: str, test_range, control_range, ignore=None):
        """
        Validate that the first and last values of the dimension arrays are equal.

        :param dim:         (str) The name of the current dimension.

        :param test_range:        (obj) The cloud-format first and last values.

        :param control_range:     (obj) The native-format first and last values.

        :param ignore:      (bool) Option to ignore specific dimension.
        """
        if ignore:
            self.logger.debug(f'Skipped {dim}')
            return

        if test_range != control_range:
            if test_range[0] == test_range[1]:
                test_range = [test_range[0]]
                
            if control_range[0] == control_range[1]:
                control_range = [control_range[0]]
            self._data_report[f'dimensions.data_errors.{dim}'] = {
                    self._labels[0]: format_tuple(
                        tuple(np.array(test_range, dtype=test_range[0].dtype).tolist())),
                    self._labels[1]: format_tuple(
                        tuple(np.array(control_range, dtype=control_range[0].dtype).tolist())),
                }            

    def _validate_dimlens(self, dim: str, test, control, ignore=None):
        """
        Validate dimension lengths are consistent

        :param dim:     (str) The name of the current dimension.

        :param test:        (obj) The cloud-format (Kerchunk) dataset selection

        :param control:     (obj) The native dataset selection

        :param ignore:      (bool) Option to ignore specific dimension.
        """
        if ignore:
            self.logger.debug(f'Skipped {dim}')
            return
        
        if test != control:
            self._data_report[f'dimensions.size_errors.{dim}'] = {
                    self._labels[0]: test,
                    self._labels[1]: control
                }
        
    def _validate_selection(
            self,
            var: str,
            test: xr.DataArray,
            control: xr.DataArray,
            current : int = 100,
            recursion_limit : int = 1, 
            dim_mid: Union[dict,None] = None,
        ) -> bool:
        """
        General purpose validation for a specific variable from multiple sources.
        Both inputs are expected to be xarray DataArray objects but the control could
        instead by a NetCDF4 Dataset object. We expect both objects to be of the same size.

        :param var:           (str) The name of the variable described by this box selection

        :param test:            (obj) The cloud-format (Kerchunk) dataset selection

        :param control:         (obj) The native dataset selection
        """
        if test.size != control.size:
            self.logger.error(
                'Validation could not be completed for these objects due to differing '
                f'sizes - "{test.size}" and "{control.size}"'
            )
            return

        if current <= recursion_limit:
            self.logger.debug('Maximum recursion depth reached')
            self.logger.info(f'Validation for {var} not performed')

            self._data_report[f'variables.data_errors.{var}'] = {
                'type':'grow_box_exceeded'
            }
            return None
        
        slice_applied = slice_all_dims(test, current, dim_mid=dim_mid)
        self.logger.debug(f'Applying slice {slice_applied} to {var}')
        tbox = test[slice_applied]
        cbox = control[slice_applied]

        if check_for_nan(cbox, BypassSwitch(), self.logger, label=var):
            return self._validate_selection(var, test, control, current-1, recursion_limit=recursion_limit, dim_mid=dim_mid)
        else:
            return self._compare_data(var, slice_applied, tbox, cbox)

    def _compare_data(
        self, 
        vname: str, 
        slice_applied: list[slice],
        test: xr.DataArray, 
        control: xr.DataArray,
        ) -> None:
        """
        Compare a NetCDF-derived ND array to a Kerchunk-derived one. This function takes a 
        netcdf selection box array of n-dimensions and an equally sized test array and
        tests for elementwise equality within selection. If possible, tests max/mean/min calculations 
        for the selection to ensure cached values are the same.

        Expect TypeErrors later from summations which are bypassed. Other errors will exit the run.

        :param vname:           (str) The name of the variable described by this box selection

        :param test:            (obj) The cloud-format (Kerchunk) dataset selection

        :param control:         (obj) The native dataset selection

        :param bypass:          (bool) Single value flag for bypassing numeric data errors (in the
                                case of values which cannot be added).

        :returns:   None but will raise error if data comparison fails.
        """
        self.logger.debug(f'Starting data comparison for {vname}')

        self.logger.debug('1. Flattening Arrays')
        t1 = datetime.now()

        control   = np.array(control).flatten()
        test      = np.array(test).flatten()

        if len(slice_applied) == 0:
            slice_applied = [slice(0, len(control))]
        start, stop = format_slice(slice_applied)

        self.logger.debug(f'2. Calculating Tolerance - {(datetime.now()-t1).total_seconds():.2f}s')
        try: # Tolerance 0.1% of mean value for xarray set
            tolerance = np.abs(np.nanmean(test))/1000
        except TypeError: # Type cannot be summed so skip all summations
            tolerance = None

        self.logger.debug(f'3. Comparing with array_equal - {(datetime.now()-t1).total_seconds():.2f}s')
        testpass = True
        try:
            equality = np.array_equal(control, test, equal_nan=True)
        except TypeError as err:
            equality = np.array_equal(control, test)

        errors, bypassed = [], []

        if not equality:
            self.logger.debug(f'3a. Comparing directly - {(datetime.now()-t1).total_seconds():.2f}s')
            equality = False
            errors.append('not_equal')
                
        self.logger.debug(f'4. Comparing Max values - {(datetime.now()-t1).total_seconds():.2f}s')
        try:
            if np.abs(np.nanmax(test) - np.nanmax(control)) > tolerance:
                self.logger.warning(f'Failed maximum comparison for {vname}')
                self.logger.debug('K ' + str(np.nanmax(test)) + ' N ' + str(np.nanmax(control)))
                testpass = False
                errors.append('max_not_equal')
        except TypeError as err:
            self.logger.warning(f'Max comparison skipped for non-summable values in {vname}')
            bypassed.append('max')

        self.logger.debug(f'5. Comparing Min values - {(datetime.now()-t1).total_seconds():.2f}s')
        try:
            if np.abs(np.nanmin(test) - np.nanmin(control)) > tolerance:
                self.logger.warning(f'Failed minimum comparison for {vname}')
                self.logger.debug('K ' + str(np.nanmin(test)) + ' N ' + str(np.nanmin(control)))
                testpass = False
                errors.append('min_not_equal')
        except TypeError as err:
            self.logger.warning(f'Min comparison skipped for non-summable values in {vname}')
            bypassed.append('min')

        self.logger.debug(f'6. Comparing Mean values - {(datetime.now()-t1).total_seconds():.2f}s')
        try:
            if np.abs(np.nanmean(test) - np.nanmean(control)) > tolerance:
                self.logger.warning(f'Failed mean comparison for {vname}')
                self.logger.debug('K ' + str(np.nanmean(test)) + ' N ' + str(np.nanmean(control)))
                testpass = False
                errors.append('mean_not_equal')
        except TypeError as err:
            self.logger.warning(f'Mean comparison skipped for non-summable values in {vname}')
            bypassed.append('mean')

        if errors:

            # 1.3.5 Error bypass
            if test.size == 1:
                self.logger.warning(f'1.3.5 Warning: 1-dimensional value difference for {vname} - skipped')
                self._data_report[f'variables.bypassed.{vname}'] = '1D-nan'
            else:
                self._data_report[f'variables.data_errors.{vname}'] = {
                    'type':','.join(errors),
                    'topleft':start,
                    'bottomright':stop,
                }
        if bypassed:
            self._data_report[f'variables.bypassed.{vname}'] = ','.join(bypassed)

        self.logger.info(f'Data validation complete for {vname}')

class ValidateOperation(ProjectOperation):
    """
    Encapsulate all validation testing into a single class. Instantiate for a specific project,
    the object could then contain all project info (from detail-cfg) opened only once. Also a 
    copy of the total datasets (from native and cloud sources). Subselections can be passed
    between class methods along with a variable index (class variables: variable list, dimension list etc.)

    Class logger attribute so this doesn't need to be passed between functions.
    Bypass switch contained here with all switches.
    """
    def __init__(
            self, 
            proj_code,
            workdir,
            parallel: bool = False,
            **kwargs):
        """
        No current validate-specific parameters
        """

        self.phase = 'validate'
        super().__init__(proj_code, workdir, **kwargs)
        if parallel:
            self.update_status(self.phase, 'Pending',jobid=self._logid)

    def _run(
            self,
            mode: str = 'kerchunk',
            dim_mid: Union[dict,None] = None,
            **kwargs
        ) -> None:
        """
        Run hook for project operation run method

        :param mode:    (str) Cloud format to use, overriding the known cloud format from 
            previous steps.
        """
        self.set_last_run(self.phase, timestamp())
        self.logger.info("Starting validation")

        if mode != self.cloud_format and mode is not None:
            self.cloud_format = mode

        test   = self.dataset.open_dataset()
        sample = self._open_sample()

        meta_fh = JSONFileHandler(self.dir, 'metadata_report',logger=self.logger, **self.fh_kwargs)
        data_fh = JSONFileHandler(self.dir, 'data_report',logger=self.logger, **self.fh_kwargs)

        vd = ValidateDatasets(
            [test,sample],
            f'validator-padocc-{self.proj_code}',
            dataset_labels=[self.cloud_format, self.source_format], 
            filehandlers=[meta_fh, data_fh],
            logger=self.logger)

        # Run metadata testing
        vd.validate_metadata()

        if self.cfa_enabled:
            self.logger.info('CFA-enabled validation')
            control = self._open_cfa()
            vd.replace_dataset(control, label=self.source_format)
        else:
            self.logger.info('Source-slice validation')
            preslice = self._get_preslice(test, sample, test.variables)

            vd.replace_preslice(preslice, label=self.cloud_format)

        vd.validate_data(dim_mid=dim_mid)

        # Save report
        vd.save_report()

        err = worst_error(vd.report) or 'Success'
        self.update_status('validate',err, jobid=self._logid)
        
        return vd.pass_fail

    def _open_sample(self):
        """
        Open a random sample dataset for validation checking.
        """
        randomfile = random.randint(0,len(self.allfiles)-1)
        file = self.allfiles[randomfile]
        return xr.open_dataset(file)

    def _open_cfa(self):
        """
        Open the CFA dataset for this project
        """
        return self.cfa_dataset.open_dataset()

    def _get_preslice(self, test, sample, variables):
        """Match timestamp of xarray object to kerchunk object.
        
        :param test:     (obj) An xarray dataset representing the cloud product.
        
        :param sample:   (obj) An xarray dataset representing the source file(s).
        
        :returns:   A slice object to apply to the test dataset to map directly
            to the sample dataset.
        """

        preslice = PresliceSet()
        for var in variables:
            preslice_var = {}
            for dim in sample[var].dims:

                if len(sample[dim]) < 2:

                    dim_array = np.array(test[dim])
                    index = np.where(dim_array == np.array(sample[dim][0]))[0][0]
                    stop = index + 1
                    pos0 = index #np.array(test[dim][index], dtype=test[dim].dtype)
                    end = stop # np.array(test[dim][stop], dtype=test[dim].dtype)

                else:
                    # Switch to selection not iselection if needed later?
                    #pos0 = np.array(sample[dim][0], dtype=sample[dim].dtype)
                    #pos1 = np.array(sample[dim][1], dtype=sample[dim].dtype)

                    #end = np.array(sample[dim][-1], dtype=sample[dim].dtype) + (pos1-pos0)
                    pos0 = 0
                    end  = len(sample[dim])

                slice_dim = slice(
                    pos0,
                    end
                )
                preslice_var[dim] = slice_dim
            preslice.add_preslice(preslice_var, var)

        return preslice
