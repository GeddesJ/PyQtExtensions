'''
QSqlDBProperty
    Copyright (C) 2018     Jonathan Geddes - jonathanericgeddes@protonmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Created on 27 May 2018

@author: jonathan
'''
from typing import *

class QSqlDBProperty(object):
    '''
    Decorator for attributes that are stored in the database.
    This is just a factory for the _QSqlDBProperty class which contains the
    logic
    '''

    def __init__(self, index: int, **kwargs):
        """
        Constructor:
        """
        self._index = index
        self._fieldArgs = kwargs

    def __call__(self, fget = None, fset = None, fdel = None, fdoc = None):
        """
        Returns a new instance of the property
        """
        index = self._index
        fieldArgs = self._fieldArgs
        return _QSqlDBProperty(index, fieldArgs, fget, fset, fdel, fdoc)


class _QSqlDBProperty(property):
    """
    Helper class which contains the actual logic for the QSqlDBProperty class.
    The afformentioned class is actually just a factory for this class.
    """


    def __init__(self, index: int, fieldArgs, fget = None,
                      fset = None, fdel = None, fdoc = None):
            '''
            Constructor:
            '''
            super().__init__(fget, fset, fdel, fdoc)
            self._index = index
            self._fieldArgs = fieldArgs


    @property
    def PropertyName(self) -> str:
        '''
        Gets the name of the property from either a name argument in the
        fieldArgs, or from the name of the getter, setter or deleter.
        If none of those attributes can be determined, returns None.
        '''
        if (self._fieldArgs.get("name") != None):
            return self._fieldArgs["name"]

        elif (self.fget != None):
            return self.fget.__name__

        elif (self.fset != None):
            return self.fset.__name__

        elif (self.fdel != None):
            return self.fdel.__name__

        else:
            return None


    @property
    def FieldArguments(self) -> Mapping[str, Any]:
        '''
        Gets the field arguments for the property
        '''
        return self._fieldArgs


    @property
    def FieldIndex(self) -> int:
        '''
        Returns the field index of the property
        '''
        return self._index


    def getter(self, fget):
        """
        Sets a new get method for the QSqlDBProperty
        Overrides from property
        """
        return type(self)(self._index, self._fieldArgs, fget, self.fset, self.fdel)

    def setter(self, fset):
        """
        Sets a new set method for the QSqlDBProperty
        Overrides from property
        """
        return type(self)(self._index, self._fieldArgs, self.fget, fset, self.fdel)


    def deleter(self, fdel):
        """
        Sets a new delete method for the QSqlDBProperty
        Overrides from property
        """
        return type(self)(self._index, self._fieldArgs, self.fget, self.fset, fdel)

