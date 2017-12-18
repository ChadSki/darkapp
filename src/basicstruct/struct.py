# Copyright (c) 2016, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

import copy


class Event(set):

    """A very simple event handler.

    Add an event handler (a function) with += and -= syntax.
    You may remove all handlers at once with `.clear()`.
    Invoke the handler with function call syntax `()`.

    Event handlers should be short and return quickly! Execution cannot
    continue until all event handlers have finished, so make it snappy."""

    def __call__(self, *args, **kwargs):
        for handler in self:
            handler(*args, **kwargs)


class BasicStruct(object):

    """A way of interpreting binary data as a collection of fields.

    Wraps a ByteAccess and implements a struct interface: string field
    names for accessing primitive data types (int, float, string...)

    Attributes
    ----------
    byteaccess : ByteAccess
        The underlying data which a BasicStruct mediates access to.

    fields : Dict[str, BasicField]
        A dictionary of all the fields in the struct, by name.

    property_changed : Event
        This event is triggered by fields when their values are being
        changed via this API's set functions. Changes to the underlying
        struct that didn't go through the set functions will not trigger
        the event.
    """

    def __init__(self, potential_access, offset):
        object.__setattr__(
            self, 'byteaccess', potential_access(offset, type(self).struct_size))
        object.__setattr__(self, 'fields', {})
        for name, field in type(self).fields.items():
            self.fields[name] = copy.copy(field)
            # fields need to access our byteaccess, and trigger our
            # property_changed event
            self.fields[name].parent = self
        object.__setattr__(self, 'property_changed', Event())

    def __str__(self):
        answer = "{"
        for name, field in self.fields.items():
            answer += "\n    {}: ".format(name)
            value = field.getf(self.byteaccess)
            if isinstance(value, list):
                answer += "["
                for each in value:
                    for line in str(each).split('\n'):
                        answer += "\n        {}".format(line)
                    answer += ","
                answer += "\n    ],"
            else:
                value_lines = str(value).split('\n')
                answer += value_lines[0]
                for ii in range(1, len(value_lines)):
                    answer += "\n    {}".format(value_lines[ii])
                answer += ","
        answer += "\n}"
        return answer

    def __getattr__(self, attr_name):
        """Invoke a field, reading from the underlying data.

        This method is called when normal attribute lookup fails. It is here
        used to extend attribute lookup to the `fields` dictionary, so that
        those fields look like normal attributes."""
        if attr_name == 'fields':
            return self.__dict__['fields']

        if attr_name in self.fields:
            try:
                return self.fields[attr_name].getf(self.byteaccess)
            except KeyError as err:
                raise AttributeError(
                    ("Attribute name `{}` does not appear to be a member"
                     "of this struct").format(attr_name)) from err
        else:
            return self.__dict__[attr_name]

    def __setattr__(self, attr_name, newvalue):
        """Invoke a field, writing to the underlying data.

        If the field has changed, invokes the `property_changed` event handler
        and triggers any registered events.

        This method is called when normal attribute lookup fails. It is here
        used to extend attribute lookup to the `fields` dictionary, so that
        those fields look like normal attributes."""
        fields = {}
        try:
            fields = self.fields
        except KeyError:
            pass

        if attr_name in fields.keys():
            oldvalue = fields[attr_name].getf(self.byteaccess)
            fields[attr_name].setf(self.byteaccess, newvalue)
            if oldvalue != newvalue:
                self.property_changed(attr_name)
        else:
            raise AttributeError(
                "Cannot assign to {} because it is not a "
                "member of this struct.".format(attr_name))
