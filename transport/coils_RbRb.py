import matplotlib.pyplot as plt
# %matplotlib qt
from torc import (
    RacetrackCoil,
    CloverleafCoil,
    BiasCoil1,
    BiasCoil2,
    RoundCoil,
    Container,
    CoilPair,
    BiasPair,
    inch,
    mm,
    X,
    Y,
    Z,
    show,
    SILVER,
    COPPER,
)
import numpy as np

from labscriptlib.RbRb.transport import lru_cache

"""This module creates magnetic coil objects with the specifications of the RbChip lab's
transport coils, which can then be used to compute fields and gradients"""

MOTCellSize = 1.5 * inch
MOTCellClearance = 0.10*inch


@lru_cache()
def make_coils(
    BIAS_N_TURNS1=60,
    BIAS_N_TURNS2=55,
    MOT_N_TURNS=60,
    SCIENCE_N_TURNS=60,
    INNER_TRANS_N_TURNS=60,
    OUTER_TRANS_N_TURNS=60,
    custom_bias=True,
    MOT_coils_spacing_factor=1,
    science_coils_spacing_factor=1,
    inner_coils_spacing_factors=(1, 1, 1, 1),
    outer_coils_spacing_factors=(1, 1, 1, 1, 1),
    
    
):
    """Return a torc.Container containing all the coil (pairs). Includes two parameters
    to account for imperfect geometry of the coils: the deviation from design spacing
    between coilpairs at the MOT position, and the deviation at the science coil
    position. The spacing of the coils will be modelled as having a deviation from their
    design spacings that is a linear function of y, defined by the deviations at these
    two points."""
    
    #added by Mingshu, the polarity of the bias coil is designed for bias X or Y (confused to me), if needs to change the polarity, you have to change the direction of n_coil in the torc.py
    # Four pair of these, but number of turns are different, two of them are 55, the other two are 60
    BIAS_WIDTH=0.78 * inch
    BIAS_LENGTH=2.969 * inch
    BIAS_HEIGHT=0.25 * inch
    BIAS_R_INNER=0.2 * inch
    BIAS_R_OA=0.8 * inch
    # BIAS_N_TURNS1=60
    # BIAS_N_TURNS2=55

    # One pair of these
    MOT_R_INNER = 1.595 * inch
    MOT_R_OUTER = 2.375 * inch
    MOT_HEIGHT = 0.3 * inch
    MOT_Z_POS =  MOTCellSize/2 + MOTCellClearance + MOT_HEIGHT/2

    # One pair of these:
    SCIENCE_R_INNER = 1.595 * inch
    SCIENCE_R_OUTER = 2.375 * inch
    SCIENCE_HEIGHT = 0.3 * inch
    SCIENCE_Z_POS = MOTCellSize/2 + MOTCellClearance + MOT_HEIGHT/2

    # Four pairs of these
    INNER_TRANS_R_INNER = 0.795 * inch
    INNER_TRANS_R_OUTER = 1.575 * inch
    INNER_TRANS_HEIGHT = 0.3 * inch
    INNER_TRANS_Z_POS = MOTCellSize/2 + MOTCellClearance + MOT_HEIGHT/2

    # Five pairs of these:
    OUTER_TRANS_R_INNER = 0.795 * inch
    OUTER_TRANS_R_OUTER = 1.575 * inch
    OUTER_TRANS_HEIGHT = 0.5 * inch
    OUTER_TRANS_Z_POS = MOTCellSize/2 + MOTCellClearance + MOT_HEIGHT + OUTER_TRANS_HEIGHT/2

    # # One of these
    PUSH_WIDTH = 37 * mm
    PUSH_HEIGHT = 0.5 * inch
    # I think the push coil's inner edge is 86.5mm below the MOT centre. This is PushY =
    # 86.5 in Abby's code and it looks to be describing the edge and not the centre.
    PUSH_Y_POS = -36.5 * mm - PUSH_HEIGHT / 2
    PUSH_N_TURNS = 52
    PUSH_R_INNER = 0
    PUSH_R_OUTER = (
        PUSH_N_TURNS / OUTER_TRANS_N_TURNS * (OUTER_TRANS_R_OUTER - OUTER_TRANS_R_INNER)
    )

    coils = Container()

    # bias coils
    # coils.add(
        # BiasCoil(    
        # r0=(0, 0, 0),
        # n=Z,
        # displacement_z=(MOT_Z_POS + MOT_HEIGHT / 2 + BIAS_HEIGHT /2),
        # width=BIAS_WIDTH,
        # length=BIAS_LENGTH,
        # height=BIAS_HEIGHT,
        # R_inner=BIAS_R_INNER,
        # R_oa=BIAS_R_OA,
        # n_turns=BIAS_N_TURNS1,
        # arc_segs=12,
        # cross_sec_segs=12,
        # name='push',))
            # bias coils
    # coils.add(
        # BiasCoil1(    
        # r0=(0, 0, 0),
        # n=Z,
        # displacement_z=(MOT_Z_POS + MOT_HEIGHT / 2 + BIAS_HEIGHT /2),
        # width=BIAS_WIDTH,
        # length=BIAS_LENGTH,
        # height=BIAS_HEIGHT,
        # R_inner=BIAS_R_INNER,
        # R_oa=BIAS_R_OA,
        # n_turns=BIAS_N_TURNS1,
        # arc_segs=12,
        # cross_sec_segs=12,
        # name='pushx',))
            
    # coils.add(
        # BiasCoil2(    
        # r0=(0, 0, 0),
        # n=Z,
        # displacement_z=(MOT_Z_POS + MOT_HEIGHT / 2 + BIAS_HEIGHT /2),
        # width=BIAS_WIDTH,
        # length=BIAS_LENGTH,
        # height=BIAS_HEIGHT,
        # R_inner=BIAS_R_INNER,
        # R_oa=BIAS_R_OA,
        # n_turns=BIAS_N_TURNS2,
        # arc_segs=12,
        # cross_sec_segs=12,
        # name='pushy',))
        
    if custom_bias:
        coils.add(
            BiasPair(    
            r0=(0, 0, 0),
            n=Z,
            displacement_z=(MOT_Z_POS + MOT_HEIGHT / 2 + BIAS_HEIGHT /2),
            n_turns1=BIAS_N_TURNS1,
            n_turns2=BIAS_N_TURNS2,
            width=BIAS_WIDTH,
            length=BIAS_LENGTH,
            height=BIAS_HEIGHT,
            R_inner=BIAS_R_INNER,
            R_oa=BIAS_R_OA,
            arc_segs=12,
            cross_sec_segs=12,
            name='push',))
    else:
        # Push coil
        coils.add(
            RacetrackCoil(
                r0=(0, PUSH_Y_POS, 0),
                n=Y,
                n_perp=X,
                width=PUSH_WIDTH,
                length=PUSH_WIDTH,
                height=PUSH_HEIGHT,
                R_inner=PUSH_R_INNER,
                R_outer=PUSH_R_OUTER,
                n_turns=PUSH_N_TURNS,
                name='push',
            )
        )

    # MOT coils
    coils.add(
        CoilPair(
            coiltype=RoundCoil,
            r0=(0, 0, 0),
            n=Z,
            displacement=MOT_Z_POS * MOT_coils_spacing_factor,
            R_inner=MOT_R_INNER,
            R_outer=MOT_R_OUTER,
            height=MOT_HEIGHT,
            n_turns=MOT_N_TURNS,
            parity='anti-helmholtz',
            name='MOT',
        )
    )

    # Outer transport coils
    first_y = MOT_R_OUTER
    for i, y in enumerate(np.linspace(first_y, first_y + 8 * OUTER_TRANS_R_OUTER, 5)):
        coils.add(
            CoilPair(
                coiltype=RoundCoil,
                r0=(0, y, 0),
                n=Z,
                displacement=OUTER_TRANS_Z_POS * outer_coils_spacing_factors[i],
                R_inner=OUTER_TRANS_R_INNER,
                R_outer=OUTER_TRANS_R_OUTER,
                height=OUTER_TRANS_HEIGHT,
                n_turns=OUTER_TRANS_N_TURNS,
                parity='anti-helmholtz',
                name=f'outer_{i}',
            )
        )

    # Inner transport coils
    first_y = MOT_R_OUTER + INNER_TRANS_R_OUTER
    for i, y in enumerate(np.linspace(first_y, first_y + 6 * INNER_TRANS_R_OUTER, 4)):
        coils.add(
            CoilPair(
                coiltype=RoundCoil,
                r0=(0, y, 0),
                n=Z,
                displacement=INNER_TRANS_Z_POS * inner_coils_spacing_factors[i],
                R_inner=INNER_TRANS_R_INNER,
                R_outer=INNER_TRANS_R_OUTER,
                height=INNER_TRANS_HEIGHT,
                n_turns=INNER_TRANS_N_TURNS,
                parity='anti-helmholtz',
                name=f'inner_{i}',
            )
        )

    # Science coils:
    science_y = MOT_R_OUTER + 8 * INNER_TRANS_R_OUTER + SCIENCE_R_OUTER
    coils.add(
        CoilPair(
            coiltype=RoundCoil,
            r0=(0, science_y, 0),
            n=Z,
            displacement=SCIENCE_Z_POS * science_coils_spacing_factor,
            R_inner=SCIENCE_R_INNER,
            R_outer=SCIENCE_R_OUTER,
            height=SCIENCE_HEIGHT,
            n_turns=SCIENCE_N_TURNS,
            parity='anti-helmholtz',
            name='science',
        )
    )

    # Sort by y positions
    coils.children.sort(key=lambda coil: coil.y)
    return coils

# coils = make_coils()

if __name__ == '__main__':
    #Show a 3D rendering of the coils
    # coils.show(lines=True, surfaces=False, color=SILVER)
    
    coils.show(lines=False, surfaces=True, opacity=0.5, color=COPPER)
    coils.show()
    # show()
