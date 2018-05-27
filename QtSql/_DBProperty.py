'''
_DBProperty
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
class _DBProperty(property):
        '''
        Decorator for attributes that are stored in the database.
        '''

        def __init__(self, index: int, fget=None, fset=None, 
                     fdel=None, fdoc=None):
            '''
            Constructor:
            fget - getter method
            fset - setter method
            fdel - clearer method
            fdoc - doc string
            index - the column number of the property
            isPrimary - if the property is a primary key
            linkingProperty - Another _DBProperty in another table that
                this property is a foreign key of
            '''
            super().__init__(fget, fset, fdel, fdoc)
            self._index = index
            
