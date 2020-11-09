from __future__ import division
from pylab import *
import numpy as np

# #############################################
# The following functions are part of the
# "standard load" of functions and should not
# be messed with. They are here for reference only.
# #############################################

__all__ = [
           'LineRamp',
           'ExpRamp',
           'EvapRamp',
           'Cf2',
           'Poly4Line',
           'CoilTime',
           'Vmix',
           'Cf4',
           'Cf5',
           'Cf',
           'PolyExp',
           'Poly4',
           'Poly4Asymmetric',
           'PolyHalf1',
           'PolyHalf2',
           'HalfGaussRamp',
           'Blackman',
           'TrnSin',
           'SinRamp',
           'Poly3',
           't_Poly3',
           't_Line',
           't_ExpRamp'
           ]


def LineRamp(t, duration, Initial, Final):
    """Creates a linear ramp from A to B"""
    f = t / duration
    return (1 - f) * Initial + f * Final


def ExpRamp(t, duration, a, b, tau):
    """Creates an exponential ramp from A to B"""
    return (b - a * exp(duration / tau) + (a - b) * exp(t / tau)) / (1 - exp(duration / tau))

def t_ExpRamp(t, duration, a, b, tau):
    """Creates an exponential ramp from A to B"""
    return '('+ str(b - a * exp(duration / tau)) + '+' + str((a - b)) + '*np.exp((f-'+str(t)+')/'+str(tau)+'))/(' + str(1 - exp(duration / tau))+')', [t, t+duration]
    
def SinRamp(t, duration, Offset, A, Freq, Phase):
    """Creates a sinewave"""
    return Offset + A * sin(2 * pi * Freq * t + Phase)


def Blackman(t, duration, Offset, A):
    """Creates a blackman pulse"""
    f = t / duration
    return (Offset + A * sqrt(0.5 * cos(pi * (2 * f - 1)) + 0.08 * cos(2 * pi * (2 * f - 1)) + 0.42))


def HalfGaussRamp(t, duration, a, b, Width):
    """Creates a half-gauss ramp"""
    y = exp(-(duration ** 2) / Width ** 2)
    y = (a - b * y) / (1 - y) + ((b - a) / (1 - y)) * exp(-((t - duration) ** 2) / Width ** 2)
    return y


def EvapRamp(t, duration, a, b, tau):
    """Creates an "O'Hara" ramp from A to B, for dipole evaporation"""
    y = log(a / b) / log(1 + duration / tau)
    y = a * (1 + t / tau) ** (-y)
    return y

def t_Poly3(start, this_duration, t_peak, y_peak):
    f = start
    t0 = start #start time
    tf = t0 + this_duration #end time
    tp = t_peak #peak time
    yp = y_peak #peak amplitude
    L = np.array([[t0**3, t0**2, t0, 1], [tf**3, tf**2, tf, 1], [tp**3, tp**2, tp, 1], [3*tp**2, 2*tp, 1, 0]])
    R = np.array([0, 0, yp, 0])
    x = np.linalg.solve(L, R)
    # if type(f) is np.ndarray:
        # print(f[0],' ', f[-1])
    expr = ''
    for i in range(4):
        expr += '+'+str(x[i])+'*f**'+str(3-i)
    # print(expr+'\n')
    return expr, [f, f+this_duration]
    
def t_Line(start, this_duration, low, high):
    f = start
    s = (high-low)/this_duration
    expr = str(s) + '*(f-' + str(start) + ')+' + str(low)
    # print(expr+'\n')
    return expr, [f, f+this_duration]
    
def Poly3(t, duration, t_peak, y_peak):
    t0 = 0 #start time
    tf = t0 + duration #end time
    tp = t_peak #peak time
    yp = y_peak #peak amplitude
    L = np.array([[t0**3, t0**2, t0, 1], [tf**3, tf**2, tf, 1], [tp**3, tp**2, tp, 1], [3*tp**2, 2*tp, 1, 0]])
    R = np.array([0, 0, yp, 0])
    x = np.linalg.solve(L, R)
    return x[0]*t**3 + x[1]*t**2 + x[2]*t + x[3]
    
# def Poly5(t, duration, c, w):
    # f = t/duration
    # # y = c[0]+c[1]*f+c[2]*f**2+c[3]*f**3+c[4]*f**4
    # expr = c
    # y = eval(expr)
    # return y

def Poly4(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 3
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)


def PolyExp(t, duration, step, A, B, C, D, Cf=None):
    """Transfer coil function, standard three segment with exponent
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 3
    return Poly4Asymmetric(f0, None, A, B, C, D, time_argument_is_f=True)


def PolyHalf1(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step + 0) / 4
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)


def PolyHalf2(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step + 2) / 4
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)


def Poly4Line(t, duration, step, A, B, C, Initial, Final, Cf=None):
    """Transfer coil function, standard two segment
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 2
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True) + (1 - f0) * Initial + f0 * Final


def Poly4Asymmetric(t, duration, A, B, C, D, Cf=None, time_argument_is_f=False):
    """Transfer coil function, standard one segment
    
    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:
    
    f = Cf_func(t, duration, *Cf_args)
    
    instead of:
    
    f = t / duration.
    
    if time_argument_is_f == True, then duration and Cf must be None.
    In this case the first argument, t, will be interpreted as an already
    scaled time coordinate:
    
    f = t
    """
    if not time_argument_is_f:
        if Cf is None:
            f = t / duration
        else:
            Cf_func = Cf[0]
            Cf_args = Cf[1:]
            f = Cf_func(t, duration, *Cf_args)
    else:
        if duration is not None or Cf is not None:
            raise TypeError('If time_argument_is_f == True, then t is interpreted as the already scaled ' 
                            'time coordinate, f. In this case duration and Cf are not used and must be None.')
        f = t
    return 4 * A * f * (1 - f) * exp(-(((f - 1 / 2) - C) ** 2 / B ** 2) ** abs(D))

# Functions that are designed for specifying velocities #
# given known current to position conversions #
# These still have to be divided into fractions 1,2,3 to denote center of coils
# In this version I will assume a uniform acceleration


def CoilTime(d, v1, v2):
    """Function to compute duration of line #
    Need to know distance between Nth and Nth+1 coil"""
    return 2 * d / (v1 + v2)

# In the current to position curves, position is expressed as a fraction f
# from 0 to 1 so take the actual fraction in the line and convert that to
# a positional fraction.


def Cf(t, duration, d, v1, v2):
    f = t / duration
    f0 = f * ((v2 - v1) * f + 2 * v1) / (v1 + v2)
    return f0


def Cf2(t, duration, d, v1, v2):
    f = t / duration
    f0 = (2 * v1 * f + (v2 - v1) * (2 * f ** 3 - f ** 4)) / (v1 + v2)
    return f0


def Cf4(t, duration, fm, v1, v2):
    f = t / duration
    f0 = where(f < fm,
              # If f < fm:
              (3 * fm * v1 * f + (-v1 + v2) * f ** 3) / (fm * (v1 + fm * v1 + 2 * v2 - fm * v2)),
              # Otherwise:
              ((fm ** 2 * (v1 - v2) + 3 * fm * v2 * f + f * (v2 * (-3 + f) * f - v1 * (3 - 3 * f + f ** 2))) / 
              ((-1 + fm) * (v1 + fm * v1 + 2 * v2 - fm * v2))))
    return f0


def Cf5(t, duration, fm, v1, v2):
    f = t / duration
    fint = f / fm
    f0 = where(fint <= 1,
               # If fint <= 1:
               (2 * v1 * (fint) + (v2 - v1) * (2 * fint ** 3 - fint ** 4)) / 2,
               # Otherwise:
               (v1 + v2) / 2 + v2 * (fint - 1))
    return 2 * f0 * fm / (fm * v1 + (2 - fm) * v2)


def Vmix(t, duration, Vhalf, rate, max, base):
    f = t / duration
    f0 = Vhalf - rate * log((max / (f - base)) - 1)
    # Clip negative or NaN to zero
    f0[(f0 < 0) | isnan(f0)] = 0
    return f0


def TrnSin(t, duration, T0, tconst, n):
    f = t / duration
    t0 = f * T0
    f0 = where((t0 <= n * tconst) | (t0 >= (n + 2) * tconst),
               # where the above is True:
               0,
               # Otherwise:
               (sin(pi * t0 / tconst / 2 + n * pi / 2)) ** 2)
    return f0

    

if __name__ == '__main__':
    # Run all functions with random inputs as a test:
    import types
    import inspect
    t = linspace(0, 1, 1000)
    for name in __all__:
        function = globals()[name]
        print( 'testing', name )
        argspec = inspect.getargspec(function)
        try:
            n_args = len(argspec.args) - (len(argspec.defaults) if argspec.defaults is not None else 0)
        except Exception:
            import IPython
            IPython.embed()
        print(n_args)
        y = function(t, *rand(n_args-1))
        plot(t, y, label=function.__name__)
        legend()
        grid(True)
        xlabel('t')
        ylabel('y')
        title('testing all the functions')
        show()
        clf()