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

class QSqlUpgradeManager(QObject):
    '''
    Automatically upgrades the database schema based on defined @QSqlDBObject
    and their corresponding @QSqlDBProperty decorators. Also automatically
    performs data and schema upgrades which are defined by classes which
    implement the QSqlDataUpgrade and QSqlSchemaUpgrade abstract classes. 
    '''
    DBObjects = {}
    
    @staticmethod
    def RegisterDBObject(name: str, schema: QSqlRecord):
        '''
        Adds a QSqlDBObject to the upgrade manager. This function is handled by the
        QSqlDBObject decorator so you shouldn't have to worry about calling it.
        '''
        QSqlUpgradeManager.DBObjects[name] = schema
        
    @staticmethod
    def RegisterUpgradeOperation(Upgrade):
        '''
        Adds a data upgrade operation to the upgrade manager. This function is
        handled by the QSqlDataUpgrade QSqlSchemaUpgrade classes so you
        shouldn't have to worry about calling it.
        '''
        raise NotImplementedError("TODO: Implement Upgrade Operations")
        
    def __init__(self, db = QSqlDatabase()):
        '''
        Constructor: Creates a QSqlUpgradeManager with a connection to db.
        
        If db is invalid the default db connection is used.
        '''
        self._query = QSqlQuery(db)
        
        #Perform upgrades...