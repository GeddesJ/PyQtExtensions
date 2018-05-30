'''
QtSql.QSqlQueryExtensions
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

Created on 30 May 2018

@author: jonathan
'''
from PyQt5.QtSql import QSqlRecord, QSqlQuery, QSqlField
from Util.ExtensionMethod import ExtensionMethod
from PyQt5.QtCore import QVariant
from QtSql import QSqlRecordExtensions

@ExtensionMethod(QSqlQuery)
def CreateTable(self, tableName : str, tableSchema : QSqlRecord):
    """
    Executes a create table statement to create a table with the schema.
    If a table with that name already exists, throws a QSqlQueryException.
    """
    columnStatement = ""

    for field in tableSchema:
        columnStatement += _constructColumnStatement(field)
        columnStatement += ", "

    # Chop off last comma
    columnStatement = columnStatement[0:-2]

    createTableStatement = "CREATE TABLE {} ( {} ) ;".format(tableName,
                                                             columnStatement)
    self.exec(createTableStatement)

    if self.lastError() != None:
        _throwException(self.lastError().databaseText(),
                                             self.lastError().driverText())

@ExtensionMethod(QSqlQuery)
def AlterTableAddColumn(self, tableName : str, newColumn : QSqlField):
    """
    Executes an alter table statement to add a new column.
    If a column with the same name exists, throws a QSqlQueryException.
    """
    statement = "ALTER TABLE {} ADD {};".format(
        tableName, _constructColumnStatement(newColumn))

    self.exec(statement)

    if self.lastError() != None:
        _throwException(self.lastError().databaseText(),
                                             self.lastError().driverText())

@ExtensionMethod(QSqlQuery)
def AlterTableDropColumn(self, tableName : str, column : QSqlField):
    """
    Executes an alter table statement to drop a column.
    If the column does not exist, throws a QSqlQueryException.
    """
    statement = "ALTER TABLE {} DROP COLUMN {};".format(tableName,
                                                        column.name())

    self.exec(statement)

    if self.lastError() != None:
        _throwException(self.lastError().databaseText(),
                                             self.lastError().driverText())

@ExtensionMethod(QSqlQuery)
def DropTable(self, tableName : str):
    """
    Executes a drop table statement to delete a table and all its contents.
    Be careful with this command.
    """
    statement = "DROP TABLE {};".format(tableName)
    self.exec(statement)

    if self.lastError() != None:
        _throwException(self.lastError().databaseText(),
                        self.lastError().driverText())

@staticmethod
def _throwException(self, databaseText: str, driverText: str):
    raise QSqlQueryException("Failed to create table.\n Database reported: "
                                 +databaseText + "\n Driver Reported: "
                                 +driverText)

@staticmethod
def _handleFieldType(field : QSqlField) -> str:
    """
    Returns a valid SQL type based on the type of the field.
    """
    fieldType = field.type()

    if (fieldType == QVariant.Bool):
        return "BOOLEAN"
    elif (fieldType == QVariant.Char):
        return "VARCHAR({})".format(field.length())
    elif (fieldType == QVariant.Date):
        return "DATE"
    elif (fieldType == QVariant.DateTime):
        return "DATETIME"
    elif (fieldType == QVariant.Double):
        return "DOUBLE({}, {})".format(field.length(). field.precision())
    elif (fieldType == QVariant.Int or fieldType == QVariant.UInt):
        return "INT({})".format(field.length())
    elif (fieldType == QVariant.String or fieldType == QVariant.Url):
        return "TEXT"
    elif (fieldType == QVariant.Time):
        return "TIME"
    else:
        return "BLOB"

@staticmethod
def _constructColumnStatement(field : QSqlField) -> str:
    """
    Constructs the statement components necessary for creating a column in a
    create table or alter table statement
    """
    columnStatement = field.name() + " " + _handleFieldType(field)

    if field.requiredStatus() == QSqlField.Required:
        columnStatement += " NOT NULL "

    if field.defaultValue() != None:
        columnStatement += " DEFAULT " + field.defaultValue()

    return columnStatement

class QSqlQueryException(BaseException):
    """
    Raised when errors occur when executing DDL statements
    """
    pass
