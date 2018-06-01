'''
QSqlDBObject
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
from PyQt5.QtSql import QSqlRecord, QSqlField
from PyQt5.QtCore import QVariant
from QtSql.QSqlDBProperty import _QSqlDBProperty
from QtSql.QSqlUpgradeManager import QSqlUpgradeManager
from typing import *
import inspect

class QSqlDBObject(object):
    '''
    Decorator which initialises an object as a database object
    '''


    def __init__(self, cls):
        '''
        Constructor:
        '''
        inspect.getmro(cls)  # Process any super classes first
        self._class = cls
        self._handleProperties()


    def __call__(self, *args, **kwargs):
        return self._class(args, kwargs)


    def _handleProperties(self):
        """
        Iterates over the class dict looking for QSqlDBProperties.
        Any properties found have their fields generated and added to the schema
        """
        cls = self._class
        schema = QSqlRecord()

        dbProperties = [getattr(cls, method) for method in cls.__dict__
                        if type(getattr(cls, method)) is _QSqlDBProperty]

        for dbProperty in dbProperties:
            index = dbProperty.FieldIndex
            fieldName = dbProperty.PropertyName
            fieldArgs = dbProperty.FieldArguments

            field = QSqlDBObject._createField(fieldName, fieldArgs)
            schema.insert(index, field)

        QSqlUpgradeManager.RegisterDBObject(cls.__name__, schema)


    @staticmethod
    def _createField(fieldName : str, fieldArgs: Mapping[str, Any]) -> QSqlField:
        '''
        Creates the QSqlField object based on the field constraints.
        The name of the field is defined in the field constraints.
        Otherwise it is scraped from either the name of the
        get method, set method or delete method (in that order).
        If the name cannot be determined the function returns None
        '''

        field = QSqlField(fieldName, QVariant(fieldName).type())

        QSqlDBObject._handleFieldConstraints(fieldArgs, field)
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
