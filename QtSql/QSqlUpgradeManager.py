'''
QSqlUpgradeManager
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

Created on 28 May 2018

@author: jonathan
'''
from PyQt5.QtCore import QObject, qDebug
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
from QtSql import QSqlQueryExtensions, QSqlRecordExtensions
from typing import *

class QSqlUpgradeManager(QObject):
    '''
    Automatically upgrades the database schema based on defined @QSqlDBObject
    and their corresponding @QSqlDBProperty decorators. Also automatically
    performs data and schema upgrades which are defined by classes which
    implement the QSqlDataUpgrade and QSqlSchemaUpgrade abstract classes.
    '''
    _DBObjects = {}
    _schemaUpgrades = []
    _dataUpgrades = []


    @staticmethod
    def RegisterDBObject(name: str, schema: QSqlRecord):
        '''
        Adds a QSqlDBObject to the upgrade manager. This function is handled by the
        QSqlDBObject decorator so you shouldn't have to worry about calling it.
        '''
        QSqlUpgradeManager._DBObjects[name] = schema


    @staticmethod
    def RegisterSchemaUpgradeOperation(upgrade: Callable[[QSqlDatabase], None]):
        '''
        Adds a schema upgrade operation to the upgrade manager. This function is
        handled by the QtSqlSchemaUpgrade class so you
        shouldn't have to worry about calling it.
        '''
        QSqlUpgradeManager._schemaUpgrades.append(upgrade)
    
    @staticmethod
    def RegisterDataUpgradeOperation(upgrade: Callable[[QSqlDatabase], None]):
        """
        Adds a data upgrade operation to the upgrade manager. This function is
        handled by the QtSqlDataUpgrade class so you shouldn't have to worry
        about calling it.
        """
        QSqlUpgradeManager._dataUpgrades.append(upgrade)


    def __init__(self, db = QSqlDatabase(), dangerousMode = False):
        '''
        Constructor: Creates a QSqlUpgradeManager with a connection to db.

        If db is invalid the default db connection is used.

        If dangerousMode is set to True, then any redundant columns and tables
        in the database will be deleted.
        '''
        self._db = db
        self._query = QSqlQuery(db)
        self._dangerousMode = dangerousMode

        # TODO: Perform schema upgrades first

        self._handleDBObjects()
        
        # TODO: Perform data upgrades
        
    
    def _handleSchemaUpgrades(self):
        """
        Runs all new schema upgrades
        """
        
    
    def _handleDataUpgrades(self):
        """
        Runs all new data upgrades
        """


    def _handleDBObjects(self):
        """
        Compares the existing tables in the database with the registered
        objects and adds tables and columns for any changes.
        If dangerousMode is set then redundant tables and columns will be
        deleted
        """
        existingDBModel = self._constructDBModel()
        newModel = QSqlUpgradeManager._DBObjects
        existingDBTables = set(existingDBModel.keys())
        newTables = set(newModel.keys())

        # Create new tables
        for tableName in newTables.difference(existingDBTables):
            schema = newModel[tableName]
            self._query.CreateTable(tableName, schema)
            qDebug("Created new table " + tableName)

        # Update tables
        for tableName in existingDBTables.intersection(newTables):
            existingSchema = existingDBModel[tableName]
            newSchema = newModel[tableName]

            if existingSchema != newSchema:
                self._handleNewColumns(tableName, existingSchema, newSchema)

        # Remove any redundant tables if dangerousMode is on
        if self._dangerousMode:
            for tableName in existingDBTables.difference(newTables):
                self._query.DropTable(tableName)
                qDebug("Dropped table " + tableName)


    def _handleNewColumns(self, tableName:str, existingSchema: QSqlRecord,
                             newSchema: QSqlRecord):
        """
        Compares the existing schema with the new schema to work out what
        changes need to be made.
        Note: To modify a table column or insert a new column between existing
        columns (as opposed to just appending at the end), a schema upgrade
        routine will need to be written.
        """
        i = 0
        while i < min(existingSchema.count(), newSchema.count()):
            if existingSchema.field(i) != newSchema.field(i):
                raise UpgradeException("New schema cannot modify field " +
                                       "properties or ordering without a schema" +
                                       " upgrade routine.")
            i += 1

        if newSchema.count() > existingSchema.count():
            while i < newSchema.count():
                self._query.AlterTableAddColumn(tableName, newSchema.field(i))
                i += 1

        elif newSchema.count() < existingSchema.count() and self._dangerousMode:
            while i < existingSchema.count():
                self._query.AlterTableDropColumn(tableName, existingSchema.field(i))
                i += 1



    def _constructDBModel(self) -> Mapping[str, QSqlRecord]:
        """
        Constructs the existing data model of the database
        """
        existingDBModel = {}

        for tableName in self._db.tables():
            existingDBModel[tableName] = self._db.record(tableName)

        return existingDBModel


class UpgradeException(BaseException):
    """
    Raised when errors occur running the automatic upgrades
    """
    pass

