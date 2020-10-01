from labscript_utils import import_or_reload
from labscript import *
from labscriptlib.common.functions import *

from labscriptlib.RbRb.transport import (
    Transport,
    piecewise_minjerk_and_coast,
    make_coils,
    lru_cache,
    linear,
    solve_two_coil,
    
)
from labscriptlib.RbRb.transport.currents import two_coil_zero_beta

from scipy.interpolate import interp1d


coils = make_coils(
    BIAS_N_TURNS1=BIAS_N_TURNS1,
    BIAS_N_TURNS2=BIAS_N_TURNS2,
    MOT_N_TURNS=MOT_N_TURNS,
    SCIENCE_N_TURNS=SCIENCE_N_TURNS,
    INNER_TRANS_N_TURNS=INNER_TRANS_N_TURNS,
    OUTER_TRANS_N_TURNS=OUTER_TRANS_N_TURNS,
    custom_bias=True,
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
# coils = make_coils()
# (move_dt_rel_1,  move_dt_rel_2, move_dt_rel_3, move_dt_rel_4, move_dt_rel_5, move_dt_rel_6)=(2.55, 1.24,1.85,1.05,1.47,1.27)
# (move_v_rel_3, move_v_rel_5)=(0.83, 0.83)
if __name__ == '__main__':
    import_or_reload('labscriptlib.RbRb.connection_table')
    transport_time = dur_transport
else:
    # print(dur_transport)
    transport_time = dur_transport

transport_trajectory = piecewise_minjerk_and_coast(
    0,
    transport_time,
    0,
    coils['science'].y,# - move_y_final_offset,
    1.0,  # Relative duration of initial accelerating segment, 1 by definition
    (move_dt_rel_1, 1.0),  # vrel in first coasting segment, 1 by definition
    move_dt_rel_2,
    (move_dt_rel_3, move_v_rel_3),
    move_dt_rel_4,
    (move_dt_rel_5, move_v_rel_5),
    move_dt_rel_6
)

# The final transport gradient is parametrised by the current required to produce it.
# This is to ensure optimisation cannot change the actual gradient here by manipulating
# the modelled coil spacing.
# move_final_current = 40
# move_grad_0=1.1
# move_grad_1=1.61
# move_grad_2=1.89
# move_grad_3=1.99
# move_grad_4=2.06
# move_grad_5=1.92
# move_grad_6=1.61
# move_grad_7=1.26
# move_grad_8=1
move_grad_final = coils['science'].dB(coils['science'].r0, move_final_current, 'z')[2]

transport_gradient_ramp = interp1d(
    np.linspace(0, transport_time, 10),
    [
        move_grad_0,#=0.44,
        move_grad_1,#=1.61,
        move_grad_2,#=1.89,
        move_grad_3,#=1.99,
        move_grad_4,#=2.06,
        move_grad_5,#=1.92,
        move_grad_6,#=1.61,
        move_grad_7,#=1.26,
        move_grad_8,#=1.01,
        move_grad_final,
    ],
    'cubic',
    fill_value='extrapolate',
)
# print(transport_gradient_ramp)

# initial_switch_y_frac=0.27
# d2beta_initial_dy2_0=800
# d2beta_initial_dy2_1=786
# final_switch_y_frac=0.63
# d2beta_final_dy2_1=155
# d2beta_final_dy2_0=786
transport = Transport(
    coils=coils,
    y_of_t=transport_trajectory,
    t_final=transport_time,
    dBz_dz_of_t=transport_gradient_ramp,
    initial_switch_y_frac=initial_switch_y_frac,
    d2beta_initial_dy2_0=d2beta_initial_dy2_0,
    d2beta_initial_dy2_1=d2beta_initial_dy2_1,
    final_switch_y_frac=final_switch_y_frac,
    d2beta_final_dy2_1=d2beta_final_dy2_1,
    d2beta_final_dy2_0=d2beta_final_dy2_0,
    dbeta_beginning_dy_0 = dbeta_beginning_dy_0
)

if __name__ == '__main__':
    start()
    curr = transport.currents_at_time(0.6)
    ys = transport.y_of_t
    from matplotlib import rc
    rc('text', usetex=False)
    tt = np.linspace(0,transport_time,200)
    fig, ax = plt.subplots()
    cc = transport.currents_at_time(tt)
    for ncoil in range(len(curr)):
        ax.plot(tt, cc[ncoil], label=str(ncoil))
        ax.legend(ncol=2)
    figure('y')
    plot(tt, ys(tt))
    # figure('push')
    # plot(tt,cc[0 ])
    # figure('beta')
    # plot(ys(tt), transport.beta_ramp(tt))
    figure('beta_real')
    plot(tt, transport.real_beta)
    figure('dbdz')
    plot(tt, transport.dBz_dz_of_t(tt),label='dbdz')
    plot(tt,transport.dBz_dz_of_t(tt)/transport.real_beta,label='dbdx')
    plt.legend()
    plt.title('dbdx_min='+str(np.min(transport.dBz_dz_of_t(tt)/transport.real_beta)))
   
    
    show()
    stop(2)