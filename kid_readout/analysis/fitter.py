from __future__ import division
import numpy as np
import lmfit
import scipy.optimize


def line_model(params, x):
    slope = params['slope'].value
    offset = params['offset'].value
    return slope*x + offset


def line_guess(x, y):
    offset_guess = y[abs(x).argmin()]
    slope_guess = y.ptp()/x.ptp()
    params = lmfit.Parameters()
    params.add('offset', value=offset_guess)
    params.add('slope', value=slope_guess)
    return params


def x_intercept(params):
    slope = params['slope'].value
    offset = params['offset'].value
    return -offset/slope

    
default_functions = {}

# Example use of default_functions functionality:
# default_functions = {"x_intercept": x_intercept}

class Fitter(object):
    """
    This class makes it easier to use lmfit. All of the
    model-dependent behavior is contained in functions that are
    supplied to the class. There is a little bit of Python magic that
    allows for easy access to the fit parameters and functions of only
    the fit parameters.
    """
   
    def __init__(self, x_data, y_data,
                 model=line_model, guess=line_guess, functions=default_functions, 
                 mask=None, errors=None, weight_by_errors=True):
        """
        Arguments:
        model: a function y(params, x) that returns the modeled values.
        guess: a function guess(x_data, y_data) that returns a
        good-enough initial guess at all of the fit parameters.
        functions: a dictionary that maps keys that are valid Python
        variables to functions that take a Parameters object as their
        only argument.
        mask: a boolean array of the same length as f and data; only
        points x_data[mask] and y_data[mask] are used to fit the
        data, and the default is to use all data.
        errors: an array of the same size as y_data with the
        corresponding error values.

        Returns:
        A new Fitter using the given data and model.
        """
        self.x_data = x_data
        self.y_data = y_data
        self._model = model
        self._functions = functions
        if mask is None:
            if errors is None:
                self.mask = np.ones_like(x_data).astype(np.bool)
            else:
                self.mask = abs(errors) < np.median(abs(errors))*3
        else:
            self.mask = mask
        self.errors = errors
        self.weight_by_errors = weight_by_errors
        self.fit(guess(x_data[self.mask], y_data[self.mask]))

    def __getattr__(self, attr):
        """
        Return a fit parameter or value derived from the fit
        parameters. This allows syntax like r.Q_i after a fit has been
        performed.
        """
        try:
            return self.result.params[attr].value
        except KeyError:
            pass
        try:
            return self._functions[attr](self.result.params)
        except KeyError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, attr))

    def __dir__(self):
        return (dir(super(Fitter, self)) +
                self.__dict__.keys() +
                self.result.params.keys() +
                self._functions.keys())
    
    def fit(self, initial):
        """
        Fit using the data and model given at
        instantiation. Parameter initial is a Parameters object
        containing initial values. It is modified by lmfit.
        """
        self.result = lmfit.minimize(self.residual, initial, ftol=1e-6)
                               
    def residual(self, params=None):
        """
        This is the residual function used by lmfit. Only data where
        mask is True is used for the fit.
        
        Note that the residual needs to be purely real, and should *not* include abs.
        The minimizer needs the signs of the residuals to properly evaluate the gradients.
        """
        # in the following, .view('float') will take a length N complex array 
        # and turn it into a length 2*N float array.
        
        if params is None:
            params = self.result.params
        if self.errors is None or not self.weight_by_errors:
            return ((self.y_data[self.mask] - self.model(params)[self.mask]).view('float'))
        else:
            errors = self.errors[self.mask]
            if np.iscomplexobj(self.y_data) and not np.iscomplexobj(errors):
                errors = errors.astype('complex')
                errors = errors + 1j*errors
            return ((self.y_data[self.mask].view('float') - self.model(params)[self.mask].view('float')) /
                    errors.view('float'))

    def model(self, params=None, x=None):
        """
        Return the model evaluated with the given parameters at the
        given x-values. Defaults are the fit-derived params and the
        x-values corresponding to the data.
        """
        if params is None:
            params = self.result.params
        if x is None:
            x = self.x_data
        return self._model(params, x)
    
    def approx_gradient(self, x, params=None):
        """
        Estimate the model gradient dy/dx at the given x-values using
        a two-point approximation.

        Note that this is currently written to use a fixed fractional
        step size in x, not a fixed step size, so be careful if x
        spans a large range of values or includes zero.
        """
        dx = x / 1e9  # this should be OK for many purposes
        x1 = x + dx
        y = self.model(params, x)
        y1 = self.model(params, x1)
        gradient = (y1 - y) / dx
        return gradient
    
    def inverse(self, y, params=None, guess=None):
        """
        Find the modeled x-values that correspond to the given y-values.
        """
        if params is None:
            params = self.result.params
        def resid(x, y):
            return np.abs(y - self._model(params, x))
        isscalar = np.isscalar(y)
        if isscalar:
            y = np.array([y])
        def _find_inverse(y):
            if guess is None:
                x0 = self.x_data[np.argmin(np.abs(y - self.y_data))]
            else:
                x0 = guess
            return scipy.optimize.fsolve(resid, x0, args=(y,))
        result = np.vectorize(_find_inverse)(y)
        if isscalar:
            result = result[0]
        return result
