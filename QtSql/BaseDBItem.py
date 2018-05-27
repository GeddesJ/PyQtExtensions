'''
BaseDBItem
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

Created on 26 May 2018

@author: jonathan
'''
from PyQt5.QtSql import QSqlRecord, QSqlField
from PyQt5.QtCore import QVariant


class BaseDBItem(QSqlRecord):
    '''
    The base class for a database item
    '''

    class DBProperty(property):
        '''
        Decorator for attributes that are stored in the database.
        '''

        def __init__(self, index: int, fieldType: type,
                     fget=None, fset=None, fdel=None, fdoc=None,
                     **kwargs):
            '''
            Constructor:
            fget - getter method
            fset - setter method
            fdel - clearer method
            fdoc - doc string
            index - the column number of the property
            isPrimary - if the property is a primary key
            linkingProperty - Another DBProperty in another table that
                this property is a foreign key of
            '''
            super().__init__(fget, fset, fdel, fdoc)
            self._index = index
            self._fieldType = fieldType
            self._fieldConstraints = kwargs
            
        def __get__(self, instance : BaseDBItem, owner : type) -> object:
            propertyValue = self.fget(instance)
            dbValue = instance.field(self._index).value().value()
            if (propertyValue != dbValue):
                self.fset(dbValue)
            return self.fget(instance)

        def _createField(self) -> QSqlField:
            '''
            Creates the QSqlField object based on the field constraints.
            The name of the field is defined in the field constraints.
            Otherwise it is scraped from either the name of the
            get method, set method or delete method (in that order).
            If the name cannot be determined the function returns None
            '''
            if (self._fieldConstraints.get("name") != None):
                fieldName = self._fieldConstraints["name"]
            elif (self.fget != None):
                fieldName = self.fget.__name__
            elif (self.fset != None):
                fieldName = self.fset.__name__
            elif (self.fdel != None):
                fieldName = self.fdel.__name__
            else:
                return None

            field = QSqlField(fieldName,
                              QVariant.nameToType(self._fieldType.__name__))

            self._handleFieldConstraints(field)
            return field

        def _handleFieldConstraints(self, field: QSqlField) -> None:
            '''
            Sets the defined field constraints on the field
            '''
            constraints = self._fieldConstraints
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
                    #TODO: Handle primary keys
                    pass
                elif (keyword == "links"):
                    #TODO: Handle foreign keys
                    pass

        def fieldConstraints(self, **kwargs):
            '''
            Sets the field constraints for the DBProperty
            '''
            return type(self)(self._index, self._fieldType,
                              self.fget, self.fset, self.fdel, self.fdoc,
                              kwargs)

    def __init__(self):
        super().__init__(self)

        pass
