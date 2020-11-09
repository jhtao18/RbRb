from matplotlib import rc
rc('font', family='serif')
rc('font', size=18)
rc('text', usetex=True)
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fminbound, brentq
from scipy.interpolate import interp1d
from torc import cm, gauss_per_cm
from labscriptlib.RbRb.transport import lru_cache
from labscriptlib.RbRb.transport.polynomials import (
    Piecewise,
    cubic,
    quintic,
    constant,
    linear,
    loglinear,
    clip_monotonic,
)

from labscriptlib.RbRb.transport.coils_RbRb import make_coils


@lru_cache()
def solve_two_coil(y, coil1, coil2):
    """Find the currents (per unit dBz_dz) required and trap aspect ratio (beta = -
    dBz_dz/dBy_dy) resulting from using two coils to create a field zero at point(s)
    y."""

    y = np.array(y)

    # There seems to be some numerical issue if y is very close to the centre of a coil
    # but not exactly equal to it. So round them to be exact if they are very close
    y[abs(y - coil1.y) < 1e-12 * y] = coil1.y
    y[abs(y - coil2.y) < 1e-12 * y] = coil2.y

    # Compute y components of field, and z and y gradients of z and y fields:
    _, B1y, _ = coil1.B((0, y, 0), I=1)
    _, B2y, _ = coil2.B((0, y, 0), I=1)
    _, _, dB1z_dz = coil1.dB((0, y, 0), I=1, s='z')
    _, _, dB2z_dz = coil2.dB((0, y, 0), I=1, s='z')
    _, dB1y_dy, _ = coil1.dB((0, y, 0), I=1, s='y')
    _, dB2y_dy, _ = coil2.dB((0, y, 0), I=1, s='y')

    # An array of matrices, one for each point in y
    A = np.zeros(y.shape + (2, 2))
    A[..., 0, :] = np.column_stack([B1y, B2y])
    A[..., 1, :] = np.column_stack([dB1z_dz, dB2z_dz])

    # The RHS of our linear system:
    b = np.zeros(y.shape + (2,))
    b[..., 0] = 0
    b[..., 1] = 1

    # Solve to find the currents:
    I = np.linalg.solve(A, b)

    # Compute aspect ratio parameter:
    beta = 1 / (-dB1y_dy * I[..., 0] - dB2y_dy * I[..., 1])

    return I.T, beta


@lru_cache()
def two_coil_aspect(y, coil1, coil2):
    """Convenience function returning the two-coil aspect ratio at the given position
    for the given two coils"""
    _, beta = solve_two_coil(y, coil1, coil2)
    return beta


@lru_cache()
def maximise_beta(coil1, coil2):
    """Find the y position between the two coils at which the two-coil aspect ratio beta
    is maximised, and return y and beta at that point."""
    y_local_maximum = fminbound(
        lambda y: (-1)*two_coil_aspect(y, coil1, coil2), coil1.y, coil2.y
    )
    beta_local_maximum = two_coil_aspect(y_local_maximum, coil1, coil2)
    return y_local_maximum, beta_local_maximum


@lru_cache()
def solve_three_coil(y, beta, coil1, coil2, coil3):
    """Find the currents (per unit dBz_dz) required for three coils to produce a field
    zero at the given y position(s) with given trap aspect ratio (beta = -
    dBz_dz/dBy_dy)."""
    _, B1y, _ = coil1.B((0, y, 0), I=1)
    _, B2y, _ = coil2.B((0, y, 0), I=1)
    _, B3y, _ = coil3.B((0, y, 0), I=1)
    _, _, dB1z_dz = coil1.dB((0, y, 0), I=1, s='z')
    _, _, dB2z_dz = coil2.dB((0, y, 0), I=1, s='z')
    _, _, dB3z_dz = coil3.dB((0, y, 0), I=1, s='z')
    _, dB1y_dy, _ = coil1.dB((0, y, 0), I=1, s='y')
    _, dB2y_dy, _ = coil2.dB((0, y, 0), I=1, s='y')
    _, dB3y_dy, _ = coil3.dB((0, y, 0), I=1, s='y')

    y = np.array(y)
    # An array of matrices, one for each point in y
    A = np.zeros(y.shape + (3, 3))
    A[..., 0, :] = np.column_stack([B1y, B2y, B3y])
    A[..., 1, :] = np.column_stack([dB1y_dy, dB2y_dy, dB3y_dy])
    A[..., 2, :] = np.column_stack([dB1z_dz, dB2z_dz, dB3z_dz])

    # The RHS of our linear system:
    b = np.zeros(y.shape + (3,))
    b[..., 0] = 0
    b[..., 1] = -1 / beta
    b[..., 2] = 1

    # Solve to find the currents:
    I = np.linalg.solve(A, b)

    return I.T

@lru_cache()
def three_coil_zero_beta(y, I, coil1, coil2, coil3):
    _, B1y, _ = coil1.B((0, y, 0), I=I[0])
    _, B2y, _ = coil2.B((0, y, 0), I=I[1])
    _, B3y, _ = coil3.B((0, y, 0), I=I[2])
    _, _, dB1z_dz = coil1.dB((0, y, 0), I=I[0], s='z')
    _, _, dB2z_dz = coil2.dB((0, y, 0), I=I[1], s='z')
    _, _, dB3z_dz = coil3.dB((0, y, 0), I=I[2], s='z')
    _, dB1y_dy, _ = coil1.dB((0, y, 0), I=I[0], s='y')
    _, dB2y_dy, _ = coil2.dB((0, y, 0), I=I[1], s='y')
    _, dB3y_dy, _ = coil3.dB((0, y, 0), I=I[2], s='y')
    beta = (dB1z_dz+dB2z_dz+dB3z_dz)/(dB1y_dy+dB2y_dy+dB3y_dy)
    field = B1y+B2y+B3y
    return field, -beta
        
@lru_cache()
def two_coil_zero_beta(y, I, coil1, coil2):
    _, B1y, _ = coil1.B((0, y, 0), I=I[0])
    B1x, _, _ = coil1.B((0, y, 0), I=I[0])
    _, B2y, _ = coil2.B((0, y, 0), I=I[1])
    B2x, _, _ = coil2.B((0, y, 0), I=I[1])
    _, _, dB1z_dz = coil1.dB((0, y, 0), I=I[0], s='z')
    _, _, dB2z_dz = coil2.dB((0, y, 0), I=I[1], s='z')
    _, dB1y_dy, _ = coil1.dB((0, y, 0), I=I[0], s='y')
    _, dB2y_dy, _ = coil2.dB((0, y, 0), I=I[1], s='y')
    beta = (dB1z_dz+dB2z_dz)/(dB1y_dy+dB2y_dy)
    field = B1y+B2y
    return field, -beta
    
@lru_cache()
def two_coil_currents(y, coils):
    """Find the currents (per unit dBz_dz) required and trap aspect ratio (beta =
    -dBz_dy / dBy_dy) resulting from using two adjacent coils at a time from the given
    list of coils to create a field zero at position(s) y. Assumes the list of coils is
    sorted by y position."""
    y.flags.writeable = False
    I = np.zeros((len(coils),) + y.shape)
    beta = np.zeros_like(y)
    for i, (coil1, coil2) in enumerate(zip(coils, coils[1:])):
        segment = (coil1.y <= y) & (y <= coil2.y)
        (I[i, segment], I[i + 1, segment]), beta[segment] = solve_two_coil(
            y[segment], coil1, coil2
        )

    return I, beta


@lru_cache()
def piecewise_minjerk_and_coast(t0, tf, y0, yf, *segments):
    """A trajectory defined by its initial and final position and time, and a number of
    segments which are alternately just a time interval dtrel, and a (time interval,
    velocity) tuple (dtrel, vrel), The lone time intervals represent periods of time in
    which the trajectory will be one with the velocity changing monotonically according
    to a minimum-jerk trajectory, and the (time interval, velocity) segments represent
    periods of constant velocity. dtrel in each segment is a relative duration of the
    segment, as a dimensionless number - these durations will be scaled to ensure the
    overall duration is (tf - t0). The distance travelled in each segment cannot be
    specified without allowing the possibility of a non-monotonic velocity curve, so we
    fix the displacement during each minimum-jerk segment to whatever it needs to be for
    a monotonic velocity curve. In order then to satisfy the overall displacement (yf -
    y0) for the trajectory, the velocities of all segments are scaled by the necessary
    factor. Thus the velocities v_rel specified in each coasting segment are relative to
    each other, and not absolute. This is similar to how the durations of the segments
    are defined as relative to each other. As a consequence, they are also not unique:
    doubling all relative velocities, or doubling all relative durations, results in the
    same trajectory. To make trajectories unique, one should treat one relative duration
    and one relative velocity as a constant by definition, say, always setting the first
    dtrel and the first vrel to unity. The remaining durations and  velocities are then
    relative to the first, and are therefore unique for a given trajectory. This
    uniqueness is important for an optimiser to be able to find a local minimum in the
    cost function of a trajectory"""
    # Compute the total unscaled time so that we can scale the timepoints.
    total_unscaled_time = 0
    for i, item in enumerate(segments):
        if i % 2:
            # A constant-velocity segment:
            total_unscaled_time += item[0]
        else:
            # An accelerating/decelerating segment:
            total_unscaled_time += item

    t_scale_factor = (tf - t0) / total_unscaled_time

    # Create a list of coasting segments with initial and final times in absolute units:
    coast_segments = []
    t = 0
    for i, (dtrel, vrel) in list(enumerate(segments))[1::2]:
        t += t_scale_factor * segments[i-1]
        t1 = t
        t +=  t_scale_factor * dtrel
        t2 = t
        coast_segments.append((t1, t2, vrel))

    # Compute the total distance travelled so that we can scale the velocities.
    # First and last minjerk segments:
    t1, _, vrel1 = coast_segments[0]
    _, tm1, vrelm1 = coast_segments[-1]
    unscaled_displacement = 0.5 * t1 * vrel1 + 0.5 * (tf - tm1) * vrelm1
    # Intermediate minjerk segments:
    for (_, t1, vrel1), (t2, _, vrel2) in zip(coast_segments, coast_segments[1:]):
        unscaled_displacement += 0.5 * (t2 - t1) * (vrel1 + vrel2)
    # Constant velocity segments:
    for t1, t2, vrel in coast_segments:
        unscaled_displacement += (t2 - t1) * vrel
    # Relative velocities will be multiplied by this factor to make absolute velocities:
    v_scale_factor = (yf - y0) / unscaled_displacement
    t_prev = t0
    y_prev = y0
    v_prev = 0
    # Create alternate minjerk and constant-velocity segments:
    edges = []
    functions = []
    for t1, t2, vrel in coast_segments:
        v = v_scale_factor * vrel
        # Minjerk trajectory from the previous velocity to that of the coasting segment:
        dy_minjerk = 0.5 * (v_prev + v) * (t1 - t_prev)
        functions.append(
            quintic(t_prev, t1, y_prev, y_prev + dy_minjerk, v_prev, v, 0, 0)
        )
        # Constant velocity segment:
        y_final = y_prev + dy_minjerk + v * (t2 -t1)
        functions.append(linear(t1, t2, y_prev + dy_minjerk, y_final))
        edges.extend([t1, t2])
        t_prev = t2
        y_prev = y_final
        v_prev = v
    # Final minjerk trajectory to zero velocity:
    dy_minjerk = 0.5 * v_prev * (tf - t_prev)
    functions.append(quintic(t_prev, tf, y_prev, y_prev + dy_minjerk, v_prev, 0, 0, 0))

    return Piecewise(edges, functions)


@lru_cache()
def interpolate_with_relative_durations(t0, tf, rel_durations, values):
    """Create a function defined from t0 to tf with cubic interpolated values given at
    various timepoints in between. Instead of timepoints, accepts the duration of each
    segment in between points, in arbitrary units that are defined only relative to each
    other. The time intervals will be scaled in order to satisfy the total duration. In
    order for a curve to be unique given a set of relative durations, one of the
    durations should be by convention held constant, and all others defined relative to
    it. Otherwise doubling all relative durations would not change the curve, which
    would lead to an optimiser not being able to find the optimal parameters for a cost
    function that depends on this curve."""
    dt_scale_factor = (tf - t0) / sum(rel_durations)
    abs_durations = np.array([dt_scale_factor * dt for dt in rel_durations])
    abs_timepoints = np.cumsum(abs_durations)[:-1]
    return interp1d(
        [t0, *abs_timepoints, tf],
        values,
        'cubic',
        fill_value='extrapolate',
    )


@lru_cache()
class Transport(object):
    """A class to compute currents required for each coil to obtain a field zero at
    specified positions along the transport axis, or at specified times, given a
    function of position with respect to time, qwith an aspect ratio that varies in
    space according to a function parametrised by some instantiation arguments."""

    def __init__(
        self,
        coils,
        y_of_t,
        t_coils,
        t_final=2.2,
        dBz_dz_of_t=120 * gauss_per_cm,
        initial_switch_y_frac=0.25,
        d2beta_initial_dy2_0=-0.2 / cm ** 2,
        d2beta_initial_dy2_1=0 / cm ** 2,
        final_switch_y_frac=0.75,
        d2beta_final_dy2_1=0.15 / cm ** 2,
        d2beta_final_dy2_0=0 / cm ** 2,
        dbeta_beginning_dy_0=0 / cm ** 2,
        channels={
            1: ['MOT', 'inner_1', 'inner_3'],
            2: ['outer_0', 'outer_2'],
            3: ['inner_0', 'inner_2', 'outer_4'],
            4: ['outer_1', 'outer_3', 'science'],
            5: ['push'],
            # 6: ['pushy']
            # 1: ['push', 'outer_1', 'outer_3'],
            # 2: ['MOT', 'inner_1', 'inner_3'],
            # 3: ['outer_0', 'outer_2', 'outer_4'],
            # 4: ['inner_0', 'inner_2', 'science'],
        },
        max_currents={
            'push': 20.0,
            # 'pushy': 20.0,
            'MOT': 90.0,
            'inner_0': 90.0,
            'inner_1': 90.0,
            'inner_2': 90.0,
            'inner_3': 90.0,
            'outer_0': 90.0,
            'outer_1': 90.0,
            'outer_2': 90.0,
            'outer_3': 90.0,
            'outer_4': 90.0,
            'science': 90.0,
        },
    ):  
        self.coils = coils
        self.y_of_t = y_of_t
        self.t_coils = t_coils
        if isinstance(dBz_dz_of_t, (float, int, np.integer)):
            dBz_dz_of_t = constant(dBz_dz_of_t)
        self.dBz_dz_of_t = dBz_dz_of_t
        self.t_final = t_final
        self.max_currents = max_currents

        self.channels = channels
        self.channel_indices = {
            chan: [coils.index(coils[name]) for name in names]
            for chan, names in channels.items()
        }

        self.real_beta = 0
        self.real_field = 0
        # Find the local maxima in the two-coil aspect ratio between coils. When one of
        # the three active coilpairs turns off, there are only two remaining, and so the
        # aspect ratio must be equal to the two-coil aspect ratio at that point. The
        # controlled aspect ratio curve will be smoothest if it touches the 2-coil curve
        # at these maxima. Therefore we choose these local maxima to be our switchover
        # points.

        self.y_switchover = []
        beta_switchover = []
        for coil1, coil2 in zip(coils[1:], coils[2:]):  # from MOT coil onward
            y_local_maximum, beta_local_maximum = maximise_beta(coil1, coil2)
            self.y_switchover.append(y_local_maximum)
            beta_switchover.append(beta_local_maximum)

        # The first switchover point is handled differently. Instead of occurring at the
        # initial local maximum in the two-coil beta, it occurs a fraction of the way
        # initial_switch_y_frac from that local maximum to the first coils after the MOT
        # coil. The three-coil aspect ratio's initial and final values and derivatives
        # are matched to the two-coil aspect ratio at the endpoints of the segment, but
        # its initial and final second derivatives d2beta_initial_dy2_0 and
        # d2beta_initial_dy2_1 are free.
        
        # print(self.y_switchover[0], initial_switch_y_frac)
        # print( coils['outer_0'].y, self.y_switchover[0], initial_switch_y_frac[0]  )
        y_initial_switch = self.y_switchover[0] + initial_switch_y_frac * (
            coils['outer_0'].y - self.y_switchover[0]
        )
        self.y_switchover[0] = y_initial_switch
        beta_switchover[0] = two_coil_aspect(
            self.y_switchover[0], coils['MOT'], coils['outer_0']
        )
        # print(self.y_switchover[0], initial_switch_y_frac, beta_switchover[0])
        beta_add_bias_ramp  = cubic(0,self.y_switchover[0], two_coil_aspect(0, coils['MOT'], coils['outer_0']), beta_switchover[0], 0, 0)

        # What is the derivative of the two-coil beta at the initial switchover point?
        # We need this to match the derivative of the controlled aspect ratio to it:
        dy = 10e-6
        dbeta_initial_dy_0 = (
            two_coil_aspect(self.y_switchover[0] + dy, coils['MOT'], coils['outer_0'])
            - beta_switchover[0]
        ) / dy

        # Construct the function for the controlled aspect ratio in this second segment:
        # segment:
        beta_initial_ramp = quintic(
            self.y_switchover[0],
            self.y_switchover[1],
            beta_switchover[0],
            beta_switchover[1],
            dbeta_initial_dy_0,
            0,
            d2beta_initial_dy2_0,
            d2beta_initial_dy2_1,
        )


        # The final switchover point is also handled differently. Instead of occurring
        # at the final local maximum in the two-coil beta, it occurs a fraction of the
        # way final_switch_y_frac from the second-last coil to that local maximum. The
        # three-coil aspect ratio's initial and final values and derivatives are matched
        # to the two-coil aspect ratio at the endpoints of the segment, but its initial
        # and final second derivatives d2beta_final_dy2_1 and d2beta_final_dy2_0 are
        # free.

        y_final_switch = coils[-2].y + final_switch_y_frac * (
            self.y_switchover[-1] - coils[-2].y
        )
        self.y_switchover[-1] = y_final_switch
        beta_switchover[-1] = two_coil_aspect(
            self.y_switchover[-1], coils[-2], coils[-1]
        )

        # What is the derivative of the two-coil beta at the final switchover point? We
        # need this to match the derivative of the controlled aspect ratio to it:
        dy = 10e-6
        dbeta_final_dy_1 = (
            two_coil_aspect(self.y_switchover[-1] + dy, coils[-2], coils[-1])
            - beta_switchover[-1]
        ) / dy

        # Construct the function for the controlled aspect ratio in this second-to-last
        # segment:
        beta_final_ramp = quintic(
            self.y_switchover[-2],
            self.y_switchover[-1],
            beta_switchover[-2],
            beta_switchover[-1],
            0,
            dbeta_final_dy_1,
            d2beta_final_dy2_0,
            d2beta_final_dy2_1,
        )

        # Construct a list of cubic segments to smoothly join each crossover point:
        cubics = []
        for i in range(1,8):
            cubics.append(
                cubic(
                    self.y_switchover[i],
                    self.y_switchover[i + 1],
                    beta_switchover[i],
                    beta_switchover[i + 1],
                    0,
                    0,
                )
            )
        # Create a piecewise function for the controlled aspect ratio over the whole of
        # transport. The intitial and final ramps were described above. In between beta
        # is constant (such that it touches the two-coil aspect ratio local maxima in
        # between each coilpair), and after the final switch the aspect ratio follows
        # the two-coil aspect ratio, since only two coils will be used in that segment.
        self.beta_ramp = Piecewise(
            edges=self.y_switchover,
            functions=[
                lambda y: two_coil_aspect(y, coils['MOT'], coils['outer_0']),
                # beta_add_bias_ramp,
                beta_initial_ramp,
                *cubics,
                beta_final_ramp,
                lambda y: two_coil_aspect(y, coils[-2], coils[-1]),
            ],
        )

        # Compute the switchover times corresponding to the switchover positions.
        self.t_switchover = []
        for y in self.y_switchover:
            t_switchover = brentq(lambda t: self.y_of_t(t) - y, 0, t_final)
            self.t_switchover.append(t_switchover)
            
    @lru_cache()
    def currents_per_gradient_at_pos(self, y):
        """Compute the required currents per unit z gradient, in SI units, for each coil
        in order to create a field zero at the given y position(s), with the trap aspect
        ratio (beta = - dBz_dz/dBy_dy) varying in space as configured with the
        parameters passed in as instantiation arguments to this object. Returns an array
        of shape (n_coils, n_y)."""

        I = np.zeros((len(self.coils),) + y.shape)
        if not type(y)==np.float64:
            self.real_beta, self.real_field = np.zeros(len(y)), np.zeros(len(y))
        import matplotlib.pyplot as plt
        from matplotlib import rc
        rc('text', usetex=False)
        # plt.figure('I-y')
        # All but the last segment, with three coils on in each:
        for i, coil1 in enumerate(self.coils[:-2]):
            coil2 = self.coils[i + 1]
            coil3 = self.coils[i + 2]
            y_start = self.y_switchover[i - 1] if i != 0 else self.coils[0].y
            y_stop = self.y_switchover[i]

            seg = (y_start <= y) & (y < y_stop)


            if seg.sum():
                I[i : i + 3, seg] = solve_three_coil(
                            y[seg], self.beta_ramp(y[seg]), coil1, coil2, coil3
                        )
                # print(y[seg])
                # for j in range(0,3):
                    # I_min = np.min(I[i + j, seg])
                    # if I_min<-1:
                        # y_ind = np.where(seg)
                        # # print(y[y_ind])
                        # for y_i in y_ind[0]:
                            # beta_y = self.beta_ramp(y[y_i])
                            # while True:
                                # I[i:i + 3, y_i] = solve_three_coil(
                                    # y[y_i], beta_y, coil1, coil2, coil3
                                # )
                                # I_min = np.min(I[i + j, y_i])
                                # if I_min>=-1:
                                    # break
                                # else:
                                    # beta_y += 0.01
                            # print(i, j, y[y_i], ':  ', beta_y, I_min)
                # if i==0:
                    # y_ind = np.where(seg)
                    # for y_i in y_ind[0]:
                        # beta_y = self.beta_ramp(y[y_i])
                        # while True:
                            # I[i:i + 3, y_i] = solve_three_coil(
                                # y[y_i], beta_y, coil1, coil2, coil3
                            # )
                            # I_max = np.max(I[i+1, y_i])*self.dBz_dz_of_t(0)
                            # print(i, y[y_i], ':  ', beta_y, I_max)
                            # if I_max<=50:
                                # break
                            # else:
                                # beta_y -= 0.01
                # plt.plot(y[seg], I[i, seg])
                # plt.plot(y[seg], I[i+1, seg])
                # plt.plot(y[seg], I[i+2, seg])
                if isinstance(y, np.ndarray):
                    field, beta = three_coil_zero_beta(y[seg], I[i:i+3, seg], coil1, coil2, coil3)
                    self.real_beta[seg] = beta
                    self.real_field[seg] = field

        # Final segment, with only two coils:
        segm1 = y >= self.y_switchover[-1]
        I[-2:, segm1], _ = solve_two_coil(y[segm1], self.coils[-2], self.coils[-1])
        # plt.plot(y[segm1], I[-2, segm1])
        # plt.plot(y[segm1], I[-1, segm1])
        if isinstance(y, np.ndarray):
            field, beta = two_coil_zero_beta(y[segm1], I[-2:, segm1], self.coils[-2], self.coils[-1])
            self.real_beta[segm1] = beta
            self.real_field[segm1] = field
        return I

    @lru_cache()
    def currents_at_time(self, t):
        """Return the required currents at the given time """
        I_per_gradient = self.currents_per_gradient_at_pos(self.y_of_t(t))
        I = self.dBz_dz_of_t(t) * I_per_gradient
        for name, max_I in self.max_currents.items():
            i = self.coils.index(self.coils[name])
            I[i] = I[i].clip(-max_I, max_I)
            # I[i] = I[i].clip(-0, max_I)
        return I

    @lru_cache()
    def currents_for_channel(self, t, duration, channel, ratio, B_bias, base = 0):
        # if channel<=4:
            # r = -1/40
        # else: r = 0.5
        I = self.currents_at_time(t)*ratio
        # print(self.t_switchover[0])
        if channel == 1 :
            ind = np.argwhere((-0.008<np.array(t)-self.t_switchover[2]) & (np.array(t)-self.t_switchover[2]<0 )) .flatten()
            I[5][ind] = 0.1       
            ind = np.argwhere((-0.010<np.array(t)-self.t_switchover[6]) & (np.array(t)-self.t_switchover[6]<0 )) .flatten()
            I[9][ind] = 0.1
        if channel == 2 :
            ind = np.argwhere((-0.005<np.array(t)-self.t_switchover[3]) & (np.array(t)-self.t_switchover[3]<0 )) .flatten()
            I[6][ind] = 0.1       
            # ind = np.argwhere((-0.002<np.array(t)-self.t_switchover[6]) & (np.array(t)-self.t_switchover[6]<0 )) .flatten()
            # I[6][ind] = I[6][ind] + np.linspace(0,0.7,len(ind))+ np.logspace(-1.8,-1,len(ind),endpoint= True) 
        if channel==3 :
            ind = np.argwhere((np.array(t)-self.t_switchover[0]<0 )) .flatten()
            I[3][ind]=0.1        
        if channel==4 :
            ind = np.argwhere((np.array(t)-self.t_switchover[0]<0 )) .flatten()
            I[4][ind]=1
        if channel>=5:
            I = I + B_bias
            I = I.clip(-9.9,9.9)
        # print(ratio)
        return I[self.channel_indices[channel]].sum(axis=0) + base


if __name__ == '__main__':

    # Example. Plot the two-coil and three-coil currents and aspect ratios with values
    # from runmanager

    import runmanager.remote

    globals().update(runmanager.remote.get_globals())

    coils = make_coils(
        MOT_coils_spacing_factor=MOT_coils_spacing_factor,
        science_coils_spacing_factor=science_coils_spacing_factor,
        inner_coils_spacing_factors=(
            inner_coils_0_spacing_factor,
            inner_coils_1_spacing_factor,
            inner_coils_2_spacing_factor,
            inner_coils_3_spacing_factor,
        ),
        outer_coils_spacing_factors=(
            outer_coils_0_spacing_factor,
            outer_coils_1_spacing_factor,
            outer_coils_2_spacing_factor,
            outer_coils_3_spacing_factor,
            outer_coils_4_spacing_factor,
        ),
    )
    
    trajectory = piecewise_minjerk_and_coast(
        0,
        transport_time,
        0,
        coils['science'].y - move_y_final_offset,
        1.0,  # Relative duration of initial accelerating segment, 1 by definition
        (move_dt_rel_1, 1.0),  # vrel in first coasting segment, 1 by definition
        move_dt_rel_2,
        (move_dt_rel_3, move_v_rel_3),
        move_dt_rel_4,
        (move_dt_rel_5, move_v_rel_5),
        move_dt_rel_6,
    )

    # The final gradient is parametrised by the current required to produce it. This is
    # to ensure optimisation cannot change the actual gradient here by manipulating the
    # modelled coil spacing.
    move_grad_9 = coils['science'].dB(coils['science'].r0, move_final_current, 'z')[2]

    gradient_interp_values = np.array(
        [
            move_grad_0,
            move_grad_1,
            move_grad_2,
            move_grad_3,
            move_grad_4,
            move_grad_5,
            move_grad_6,
            move_grad_7,
            move_grad_8,
            move_grad_9,
        ]
    )

    gradient_interp_times = np.linspace(0, transport_time, 10)
    gradient_ramp = interp1d(
        gradient_interp_times, gradient_interp_values, 'cubic', fill_value='extrapolate'
    )

    transport = Transport(
        coils=coils,
        y_of_t=trajectory,
        t_final=transport_time,
        dBz_dz_of_t=gradient_ramp,
        initial_switch_y_frac=initial_switch_y_frac,
        d2beta_initial_dy2_0=d2beta_initial_dy2_0,
        d2beta_initial_dy2_1=d2beta_initial_dy2_1,
        final_switch_y_frac=final_switch_y_frac,
        d2beta_final_dy2_1=d2beta_final_dy2_1,
        d2beta_final_dy2_0=d2beta_final_dy2_0,
    )

    t = np.linspace(0, transport.t_final, 1024)
    y = transport.y_of_t(t)

    plt.figure()
    axpos = plt.subplot(111)
    axpos.set_title(R"(b)", fontsize=18)
    axpos.set_xlabel(fR'$t (s)$')
    axpos.set_ylabel(fR'$y (\rm cm)$', color='darkgreen')
    axpos.tick_params(axis='y', colors='darkgreen')
    axpos.plot(t, y / cm, c='darkgreen')
    
    axspd = axpos.twinx()
    axspd.set_ylabel(fR'$\dot{{y}} (\rm cm/s)$', color='crimson')
    axspd.tick_params(axis='y', labelcolor='crimson')
    axspd.plot(t, np.gradient(y) / (t[1] - t[0]) / cm, c='crimson')
    
    if isinstance(transport.y_of_t, Piecewise):
        for edge in transport.y_of_t.edges:
            axpos.axvline(edge, color='k', linestyle=':')
    axpos.grid(True, c='gray', alpha=0.6)
    plt.savefig('opt_transport_trajectory.png', dpi=300, bbox_inches='tight')
    I_threecoil = transport.currents_at_time(t)
    beta_threecoil = transport.beta_ramp(y)
    I_twocoil, beta_twocoil = two_coil_currents(y, coils)
    I_twocoil *= transport.dBz_dz_of_t(t)

    plt.figure()
    axgrad = plt.subplot(111)
    axgrad.set_title(R'(d)', fontsize=18)
    axgrad.plot(t, gradient_ramp(t) / gauss_per_cm, c='orange')
    axgrad.plot(gradient_interp_times, gradient_interp_values / gauss_per_cm, 
        marker='o', c='goldenrod', markeredgecolor='darkgoldenrod', linewidth=0,)
    axgrad.set_xlabel(fR'$t (s)$')
    axgrad.set_ylabel(fR'$\partial_z B_z (\rm G/cm)$')
    axgrad.grid(True, c='gray', alpha=0.6)
    #plt.subplots_adjust(left=None, bottom=None, right=None, top=1, wspace=None, hspace=0.196)
    plt.savefig('opt_transport_grad.png', dpi=300, bbox_inches='tight')

    I_threecoil = transport.currents_at_time(t)
    beta_threecoil = transport.beta_ramp(y)
    I_twocoil, beta_twocoil = two_coil_currents(y, coils)
    I_twocoil *= transport.dBz_dz_of_t(t)

    plt.figure(2)
    ax2 = plt.subplot(111)
    ax2.set_title(fR'(a)', fontsize=18)
    # Plot the two- and three-coil aspect ratios:
    ax2.plot(t, beta_twocoil, color="cornflowerblue", label=R'$\beta_2$')
    ax2.plot(t, beta_threecoil, color="olive", label=R'$\beta_3$')
    for t_i in transport.t_switchover:
        ax2.axvline(t_i, color='k', linestyle=':')
    ax2.grid(True, color='gray', alpha=0.6)
    ax2.legend()
    ax2.set_ylabel(R"$ -\partial_z B_z/\partial_y B_y$")
    ax2.set_xlabel(fR'$t (s)$')
    ax2.set_ylim(1.75, 3.0)
    plt.savefig('opt_aspect_ratio.png', dpi=300, bbox_inches='tight')
    
    # Plot the 2-coil currents:
    # plt.figure()
    # for coil, color, I_coil in zip(coils, COLORS, I_twocoil):
    #     plt.plot(t, I_coil, label=coil.name, color=color)
    # plt.grid(True)
    # for t_i in transport.t_switchover:
    #     plt.axvline(t_i, color='k', linestyle=':')
    # plt.legend(ncol=2)
    # plt.xlabel("Time (s)")
    # plt.ylabel("Current (A)")
    # plt.title("Two-coil transport")

    # Plot the three-coil currents:
    # What colours to use to represent each coil pair when we make plots:
    COLORS = [plt.cm.nipy_spectral(i) for i in np.linspace(0, 1, len(coils))]
    plt.figure()
    ax=plt.subplot(111)
    ax.set_title('(c)', fontsize=18)
    for coil, color, I_coil in zip(coils, COLORS, I_threecoil):
        ax.step(t, I_coil, label=coil.name, color=color, lw=2)
    ax.grid(True, c='gray', alpha=0.6)
    for t_i in transport.t_switchover:
        ax.axvline(t_i, color='k', linestyle=':')
    ax.set_xlabel(R"$t (s)$")
    ax.set_ylabel(R"Current $(\rm A)$")
    plt.savefig('opt_currents.png', dpi=300, bbox_inches='tight')
    # Plot the per-channel currents:
    # plt.figure()
    # for channel in range(1, 5):
    #     I = transport.currents_for_channel(t, duration=None, channel=channel)
    #     plt.plot(t, I, label=f'channel {channel}')
    # plt.grid(True)
    # for t_i in transport.t_switchover:
    #     plt.axvline(t_i, color='k', linestyle=':')
    # plt.legend(ncol=2)
    # plt.xlabel("Time (s)")
    # plt.title("Three-coil transport")
    # plt.ylabel("Current (A)")

    plt.show()
