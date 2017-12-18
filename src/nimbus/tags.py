# Copyright (c) 2016, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.
"""TODO"""

from basicstruct import field as f
from . import halofield as hf
from .halostruct import HaloStruct

tag_names = {
    'bipd': 'Biped',
    'bitm': 'Bitmap',
    'coll': 'Collision',
    'effe': 'Effect',
    'proj': 'Projectile',
    'vehi': 'Vehicle',
    'weap': 'Weapon',
}


class BipedTag(HaloStruct):
    struct_size = 0x450
    fields = {
        'model': hf.TagReference(offset=0x28),
        'animation': hf.TagReference(offset=0x38),
        'collision': hf.TagReference(offset=0x70),
        'physics': hf.TagReference(offset=0x80),
        'turn_speed': f.Float32(offset=0x2F0),
        'jump_velocity': f.Float32(offset=0x3B4),
        'melee_damage': hf.TagReference(offset=0x288),
        'weapons': hf.StructArray(
            'Weapon', offset=0x2D8, struct_size=36, fields={
                'held_weapon': hf.TagReference(offset=0x0)})}


class EffectTag(HaloStruct):
    struct_size = 0x700
    fields = {
        'events': hf.StructArray(
            'Event', offset=0x34, struct_size=68, fields={
                'parts': hf.StructArray(
                    'Part', offset=0x2C, struct_size=104, fields={
                        'spawned_object': hf.TagReference(offset=0x18)})})}


class ProjectileTag(HaloStruct):
    struct_size = 0x248
    fields = {
        'model': hf.TagReference(offset=0x28),
        'animation': hf.TagReference(offset=0x38),
        'collision': hf.TagReference(offset=0x70),
        'physics': hf.TagReference(offset=0x80),
        'initial_velocity': f.Float32(offset=0x1E4),
        'final_velocity': f.Float32(offset=0x1E8)}


class VehicleTag(HaloStruct):
    struct_size = 0x3F0
    fields = {
        'model': hf.TagReference(offset=0x28),
        'animation': hf.TagReference(offset=0x38),
        'collision': hf.TagReference(offset=0x70),
        'physics': hf.TagReference(offset=0x80),
        'max_forward_velocity': f.Float32(offset=0x2F8),
        'max_reverse_velocity': f.Float32(offset=0x2FC),
        'acceleration': f.Float32(offset=0x300),
        'deceleration': f.Float32(offset=0x304),
        'suspension_sound': hf.TagReference(offset=0x3B0),
        'crash_sound': hf.TagReference(offset=0x3C0)}


class WeaponTag(HaloStruct):
    struct_size = 0x504
    fields = {
        'model': hf.TagReference(offset=0x28),
        'animation': hf.TagReference(offset=0x38),
        'collision': hf.TagReference(offset=0x70),
        'physics': hf.TagReference(offset=0x80),
        'magazines': hf.StructArray(
            'Magazine', offset=0x4F0, struct_size=112, fields={
                'rounds_recharged': f.Int16(offset=0x4),
                'rounds_total_initial': f.Int16(offset=0x6),
                'rounds_total_maximum': f.Int16(offset=0x8),
                'rounds_loaded_maximum': f.Int16(offset=0xA)}),
        'triggers': hf.StructArray(
            'Trigger', offset=0x4FC, struct_size=276, fields={
                'initial_rounds_per_second': f.Float32(offset=0x4),
                'final_rounds_per_second': f.Float32(offset=0x8),
                'rounds_per_shot': f.Int16(offset=0x22),
                'projectiles_per_shot': f.Int16(offset=0x6E),
                'projectile': hf.TagReference(offset=0x94),
                'firing_effects': hf.StructArray(
                    'FiringEffect', offset=0x108, struct_size=132, fields={
                        'fire_effect': hf.TagReference(offset=0x24),
                        'misfire_effect': hf.TagReference(offset=0x34),
                        'no_ammo_effect': hf.TagReference(offset=0x44),
                        'fire_damage': hf.TagReference(offset=0x54),
                        'misfire_damage': hf.TagReference(offset=0x64),
                        'no_ammo_damage': hf.TagReference(offset=0x74)})})}
