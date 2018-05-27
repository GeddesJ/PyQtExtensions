'''
_RuntimeSchema
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
from PyQt5.QtSql import QSqlRecord

@staticmethod
class _RuntimeSchema(object):
    '''
    Static class which stores the schema generated from the DBProperties at
    runtime.
    '''
    
    _schema = {}
    
    @staticmethod
    @property
    def Schema() -> map:
        return _RuntimeSchema._schema.copy()
    
    @staticmethod
    def setTableRecord(tableName : str, record : QSqlRecord) -> None:
        '''
        Sets the schema record for the table
        '''
        schema = _RuntimeSchema._schema
        schema[tableName] = record
        
        
        
        
        