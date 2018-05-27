'''
BaseDBList
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
from PyQt5.QtSql import *
import BaseDBItem
import PyQt5.Qt
from typing import overload

class BaseDBList(QSqlRelationalTableModel):
    """
    Stores a list of DBItems in an sql database
    """
    
    def __init__(self):
        """
        Constructor: 
        Establishes a connection to a table in a database. Checks if the schemas
        are the same and applies any changes to the schema.
        """
        QSqlRelationalTableModel.__init__(self)
