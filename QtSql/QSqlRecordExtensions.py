'''
QtSql.QSqlRecordExtensions
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
from Util.ExtensionMethod import ExtensionMethod
from PyQt5.QtSql import QSqlRecord

"""
Extends the QSqlRecord by making it iterable
"""

@ExtensionMethod(QSqlRecord)
def __iter__(self):
    self.current = 0
    return self


@ExtensionMethod(QSqlRecord)
def __next__(self):
    if self.current >= self.count():
        raise StopIteration
    else:
        self.current += 1
        return self.field(self.current - 1)