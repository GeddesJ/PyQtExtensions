'''
DBManager
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
from PyQt5.QtCore import QObject, qCritical
from PyQt5.QtSql import QSqlDatabase, QSqlDriver

class DBManager(QObject):
    '''
    Manages a connection and initialising tables of an SQLite database
    '''


    def __init__(self, DatabaseName : str):
        '''
        Constructor: Initialises a connection to the database
        '''
        super.__init__(self)
        self._schema = {}
        
        self._db = QSqlDatabase(QSqlDriver.SQLite)
        self._db.setDatabaseName(DatabaseName)
        
        if not self._db.open():
            qCritical("Failed to establish connection with database " 
                      + DatabaseName)
            return
        
        self._initSchema()
        
        
    def _initSchema(self):
        '''
        Initialises the table schema of the database
        '''
        for tablename in self._db.tables():
            record = self._db.record(tablename)
            self._schema[tablename] = record
                
        
        