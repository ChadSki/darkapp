# Copyright (c) 2016, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

from basicstruct import BasicStruct


class HaloStruct(BasicStruct):

    """A way of interpreting binary data as a collection of fields.

    HaloStruct is mostly the same as BasicStruct, except that it
    has a reference to the map object and can therefore contain
    HaloFields."""

    def __init__(self, halomap, offset):
        object.__setattr__(self, 'halomap', halomap)
        super().__init__(halomap.map_access, offset)
