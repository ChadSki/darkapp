# Copyright (c) 2016, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

from basicstruct import BasicStruct
from basicstruct import field as f
from .halostruct import HaloStruct
from . import halofield as hf


class MapHeader(BasicStruct):
    struct_size = 132
    fields = {
        'integrity': f.Ascii(offset=0, length=4, reverse=True),
        'game_version': f.UInt32(offset=4),
        'map_size': f.UInt32(offset=4),
        'index_offset': f.UInt32(offset=16),
        'metadata_size': f.UInt32(offset=20),
        'map_name': f.Asciiz(offset=32, maxlength=32),
        'map_build': f.Asciiz(offset=64, maxlength=64),
        'map_type': f.UInt32(offset=128)}


class IndexHeader(BasicStruct):
    struct_size = 40
    fields = {
        'primary_magic': f.UInt32(offset=0),
        'base_tag_ident': f.UInt32(offset=4),
        'map_id': f.UInt32(offset=8),
        'tag_count': f.UInt32(offset=12),
        'verticie_count': f.UInt32(offset=16),
        'verticie_offset': f.UInt32(offset=20),
        'indicie_count': f.UInt32(offset=24),
        'indicie_offset': f.UInt32(offset=28),
        'model_data_length': f.UInt32(offset=32),
        'integrity': f.Ascii(offset=36, length=4, reverse=True)}


class TagHeader(HaloStruct):
    struct_size = 32
    fields = {
        'first_class': f.Ascii(offset=0, length=4, reverse=True),
        'second_class': f.Ascii(offset=4, length=4, reverse=True),
        'third_class': f.Ascii(offset=8, length=4, reverse=True),
        'ident': f.UInt32(offset=12),
        'name': hf.AsciizPtr(offset=16),
        'meta_offset_raw': f.UInt32(offset=20),
        'indexed': f.UInt32(offset=24)}
