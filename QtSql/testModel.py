'''
testModel
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
from QSqlDBObject import QSqlDBObject
from QSqlDBProperty import QSqlDBProperty
from QSqlUpgradeManager import QSqlUpgradeManager

@QSqlDBObject
class Employee(object):
    '''
    test
    '''
    def __init__(self, name, role, salary):
        '''
        Constructor
        '''
        self._name = name
        self._role = role
        self._salary = salary
        
    @QSqlDBProperty(0, str)
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @QSqlDBProperty(1, str)
    def role(self):
        return self._role
    
    @QSqlDBProperty(2, float)
    def salary(self):
        return self._salary
    

bob = Employee("Bob", "Software Engineer", 95000.45)
print (bob.name + " is very happy")
bob.name = "Roberta"
print (bob.name + " is now transgender and has changed her name")

steve = Employee("Steve", "Marketing", 75000)
print(steve.name + " works in " + steve.role)

print(QSqlUpgradeManager.DBObjects)
