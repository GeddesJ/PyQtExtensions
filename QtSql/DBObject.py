'''
DBObject
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
from PyQt5.QtSql import QSqlRecord, QSqlField
from PyQt5.QtCore import QVariant
from _RuntimeSchema import _RuntimeSchema
import _DBProperty


class DBObject(object):
    '''
    Decorator which initialises an object as a database object
    '''

    def __init__(self, ModelObject: object) -> Callable:
        '''
        Constructor: Returns the wrapped class
        '''
        self._tableName = ModelObject.__name__
        self._tableSchema = QSqlRecord()
        self._updateRuntimeSchema()

        class WrappedClass(ModelObject):
            pass
        
        return WrappedClass

    def DBProperty(self, index: int, fieldType: type,
                   fget=None, fset=None, fdel=None, fdoc=None,
                   **kwargs) -> Callable:
        '''
        Wrapper for adding DB fields to the schema
        '''
        field = DBObject._createField(fget, fset, fdel, kwargs, fieldType)
        if self._tableSchema.contains(field.name()):
            self._tableSchema.replace(index, field)
        else:
            self._tableSchema.insert(index, field)
            
        self._updateRuntimeSchema()
        
        return _DBProperty

    @staticmethod
    def _createField(fget: Callable, fset: Callable, fdel: Callable,
                     fieldConstraints: Mapping[str, Any],
                     fieldType: type) -> QSqlField:
        '''
        Creates the QSqlField object based on the field constraints.
        The name of the field is defined in the field constraints.
        Otherwise it is scraped from either the name of the
        get method, set method or delete method (in that order).
        If the name cannot be determined the function returns None
        '''
        if (fieldConstraints.get("name") != None):
            fieldName = fieldConstraints["name"]
        elif (fget != None):
            fieldName = fget.__name__
        elif (fset != None):
            fieldName = fset.__name__
        elif (fdel != None):
            fieldName = fdel.__name__
        else:
            return None

        field = QSqlField(fieldName,
                          QVariant.nameToType(fieldType.__name__))

        DBObject._handleFieldConstraints(fieldConstraints, field)
        return field

    @staticmethod
    def _handleFieldConstraints(constraints: Mapping[str, Any],
                                field: QSqlField) -> None:
        '''
        Sets the defined field constraints on the field
        '''
        for keyword in constraints:
            value = constraints[keyword]

            if (keyword == "defaultValue"):
                field.setDefaultValue(QVariant(value))
            elif (keyword == "isAuto"):
                field.setAutoValue(value)
            elif (keyword == "isReadOnly"):
                field.setReadOnly(value)
            elif (keyword == "isRequired"):
                field.setRequired(value)
            elif (keyword == "length"):
                field.setLength(value)
            elif (keyword == "precision"):
                field.setPrecision(value)
            elif (keyword == "isPrimary"):
                # TODO: Handle primary keys
                pass
            elif (keyword == "links"):
                # TODO: Handle foreign keys
                pass
            
    def _updateRuntimeSchema(self):
        '''
        Updates the runtime static object with the current schema of this object
        '''
        _RuntimeSchema.setTableRecord(self._tableName, self._tableSchema)
