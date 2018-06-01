'''
QtSql.QtSqlAbstractUpgrade
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
    
Created on 1 Jun. 2018

@author: jonathan
'''
from PyQt5.QtSql import QSqlDatabase

class QtSqlAbstractUpgrade(object):
    '''
    Abstract class for database upgrades. 
    Subclass from QtSqlSchemaUpgrade or QtSqlDataUpgrade for actual upgrades.
    '''
    
    @classmethod
    def Version(cls):
        """
        Returns the version number of the upgrade
        """
        raise NotImplementedError()
    
    @classmethod
    def UpgradeDate(cls):
        """
        Returns the date of the upgrade. Useful for ensuring that upgrades are
        performed in chronological order.
        """
        raise NotImplementedError()
    
    @classmethod
    def Description(cls):
        """
        Returns a description of what the upgrade does.
        """
        raise NotImplementedError()
    
    @classmethod
    def PerformUpgrade(cls, db: QSqlDatabase):
        """
        Performs the tasks necessary for the upgrade.
        Requires a reference to the database connection
        """
        raise NotImplementedError()
        