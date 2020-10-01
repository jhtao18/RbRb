import numpy as np
import numpy.polynomial


class Polynomial(numpy.polynomial.Polynomial):
    """Hashable subclass of Polynomial"""
    def __hash__(self):
        return hash(self.coef.tobytes())


class Piecewise(object):
    """Make a piecewise function defined by a list of edges and a list of
    functions of one argument. Edges array or list must be sorted, and
    len(edges) must be len(functions) -1 (the domain of the first and last
    functions are extended to ± infinity). Functions should return scalars or
    arrays depending on their input argument, like numpy ufuncs do. When
    called, if an x value is exactly on an edge, the function to the left of
    that edge will be used.
    """

    def __init__(self, edges, functions):
        if len(edges) != len(functions) - 1:
            # print(edges, len(functions))
            raise ValueError("len(edges) must be len(functions) -1")
        if not edges == sorted(edges):
            # We don't sort automatically because unsorted edges probably indicate user
            # error:
            raise ValueError("Edges not sorted")
        self.edges = edges
        self.domains = np.zeros((len(edges) + 1, 2))
        self.domains[0, 0] = -np.inf
        self.domains[1:, 0] = self.domains[:-1, 1] = edges
        self.domains[-1, 1] = np.inf
        self.functions = functions
        if not all([callable(f) for f in functions]):
            raise TypeError("Non callable object provided")

    def __call__(self, x):
        """Evaluate the piecewise function for np.array or scalar x"""
        if not isinstance(x, np.ndarray):
            function = self.functions[self.domains[1:, 0].searchsorted(x)]
            return function(x)
        results = []
        for f, (xmin, xmax) in zip(self.functions, self.domains):
            points_in_domain = x[(xmin < x) & (x <= xmax)]
            if len(points_in_domain):
                results.append(f(points_in_domain))
        return np.concatenate(results)

    def __eq__(self, other):
        return (
            np.array_equal(self.domains, other.domains)
            and self.functions == other.functions
        )

    def __hash__(self):
        return hash((tuple(self.functions), self.domains.tobytes()))


def quintic(x0, x1, y0, y1, dydx0, dydx1, d2y_dx20, d2y_dx21):
    """Return a np.polynomial.Polynomial object for a quantic with the given
    values, derivatives and second derivatives at two points."""
    # print(x0, x1, y0, y1, dydx0, dydx1, d2y_dx20, d2y_dx21)
    x0, x1, y0, y1, dydx0, dydx1, d2y_dx20, d2y_dx21 = float(x0), float(x1), float(y0), float(y1), float(dydx0), float(dydx1), float(d2y_dx20), float(d2y_dx21)
    coeffs = np.linalg.solve(
        [
            [1, x0, x0 ** 2, x0 ** 3, x0 ** 4, x0 ** 5],
            [1, x1, x1 ** 2, x1 ** 3, x1 ** 4, x1 ** 5],
            [0, 1, 2 * x0, 3 * x0 ** 2, 4 * x0 ** 3, 5 * x0 ** 4],
            [0, 1, 2 * x1, 3 * x1 ** 2, 4 * x1 ** 3, 5 * x1 ** 4],
            [0, 0, 2, 6 * x0, 12 * x0 ** 2, 20 * x0 ** 3],
            [0, 0, 2, 6 * x1, 12 * x1 ** 2, 20 * x1 ** 3],
        ],
        [y0, y1, dydx0, dydx1, d2y_dx20, d2y_dx21],
    )
    return Polynomial(coeffs)


def cubic(x0, x1, y0, y1, dydx0, dydx1):
    coeffs = np.linalg.solve(
        [
            [1, x0, x0 ** 2, x0 ** 3],
            [1, x1, x1 ** 2, x1 ** 3],
            [0, 1, 2 * x0, 3 * x0 ** 2],
            [0, 1, 2 * x1, 3 * x1 ** 2],
        ],
        [y0, y1, dydx0, dydx1],
    )
    return Polynomial(coeffs)


def quadratic(x0, x1, y0, y1, dydx0):
    coeffs = np.linalg.solve(
        [[1, x0, x0 ** 2], [1, x1, x1 ** 2], [0, 1, 2 * x0]], [y0, y1, dydx0]
    )
    return Polynomial(coeffs)


def linear(x0, x1, y0, y1):
    coeffs = np.linalg.solve([[1, x0], [1, x1]], [y0, y1])
    return Polynomial(coeffs)


def constant(y_0):
    return Polynomial([y_0])


def loglinear(x0, x1, y0, y1):
    A = np.log(y1 / y0) / (x1 - x0)
    C = y0 * np.exp(-A * x0)
    return lambda x: C * np.exp(A * x)


def real_roots(p):
    """Return only the real roots of a polynomial"""
    return [x.real for x in p.roots() if np.isreal(x)]


def clip_monotonic(x0, x1, p):
    """Takes a numpy.polynomial.Polynomial object p, and clips regions between x0 and x1
    where it is not monotonic, such that the function remains constant rather than
    reversing direction. If the function is clipped in this way, a Piecewise object will
    be returned containing segments of the original polynomial as well as constant
    segments. Assumes that p'(x0), p'(x1), and p(x1) - p(x0) are all nonzero and have
    the same sign."""
    extrema = [x for x in real_roots(p.deriv()) if x0 < x < x1 and p.deriv(2)(x) != 0]
    if not extrema:
        return p
    constant_segs = []
    y0, y1 = p(x0), p(x1)
    for x, x_next in zip(extrema, extrema[1:]):
        # Skip over extrema already covered by constant segments:
        if constant_segs and x < constant_segs[-1][1]:
            continue
        y = p(x)
        if not (y0 < y < y1 or y1 < y < y0):
            # function has already passed its final value. Insert a constant segment
            # from where if first did so until the end:
            x_start = min(x_start for x_start in real_roots(p - y1) if x_start > x0)
            constant_segs.append((x_start, x1, constant(y1)))
            break
        # Where does the function next attain this value? We know it will be after the
        # next extremum:
        x_stop = min(x_stop for x_stop in real_roots(p - y) if x_stop > x_next)
        constant_segs.append((x, x_stop, constant(y)))
    # Assemble a piecewise function:
    functions = [p]
    edges = []
    for x_start, x_stop, func in constant_segs:
        edges.append(x_start)
        functions.append(func)
        edges.append(x_stop)
        functions.append(p)
    return Piecewise(edges, functions)