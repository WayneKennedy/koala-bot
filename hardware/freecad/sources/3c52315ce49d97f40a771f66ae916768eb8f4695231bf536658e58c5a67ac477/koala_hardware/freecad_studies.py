# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Native documents for retained kinematic and rear-leg study generators.

These replay the generators with the archived revision's parameters. Historical
STEP files remain separate frozen references to their original exported state.
"""
from .cad import Compound, Rot


def named_compound(items):
    shapes=[]
    for name,shape,*_ in items:
        shape.label=name
        shapes.append(shape)
    return Compound(shapes)


def body_master(pose):
    from . import body_plan
    return named_compound(body_plan.cad_items(pose,body_plan.poses()[pose]))


def rear_leg(pose,variant):
    from . import rear_leg_review as review
    old=review.THIGH_OPTIONS,review.THIGH_FLAT
    try:
        review.THIGH_OPTIONS=variant=='options'
        review.THIGH_FLAT=variant=='flat'
        review.nominal.cache_clear()
        return named_compound(review.nominal(pose))
    finally:
        review.THIGH_OPTIONS,review.THIGH_FLAT=old
        review.nominal.cache_clear()


def pitch_socket_45():
    from . import assembly,body_plan,pitch_socket_tilt_study as study
    from .parts import links,pelvis
    frame=study.socket_frame('quadruped',-45)
    limb=body_plan.poses()['quadruped']['rear']
    carrier_frame=assembly.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
    return named_compound([
        ('retained_carrier',carrier_frame*links.carrier(False)),
        ('retained_root_socket',frame*pelvis.root_socket()),
        ('proposed_torso_face_patch',frame*study.mount_face()),
    ])
