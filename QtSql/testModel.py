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
from QtSql.QSqlDBObject import QSqlDBObject
from QtSql.QSqlDBProperty import QSqlDBProperty
from QtSql.QSqlUpgradeManager import QSqlUpgradeManager

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
        
    @QSqlDBProperty(0)
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @QSqlDBProperty(1)
    def role(self):
        return self._role
    
    @QSqlDBProperty(2)
    def salary(self):
        return self._salary
    
@QSqlDBObject
class Boss(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, "Manager", salary)
        self._department = department
    
    @QSqlDBProperty(3)    
    def department(self):
        return self._department
    

bob = Employee("Bob", "Software Engineer", 95000.45)
print (bob.name + " is very happy")
bob.name = "Roberta"
print (bob.name + " is now transgender and has changed her name")

steve = Employee("Steve", "Marketing", 75000)
print(steve.name + " works in " + steve.role)

john = Boss("John", 125000, "Finance")
print(john.name + " is a " + john.role + " of " + john.department)

print(QSqlUpgradeManager._DBObjects)
