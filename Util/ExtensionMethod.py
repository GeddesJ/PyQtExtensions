'''
Util.ExtensionMethod
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
from typing import Callable

class ExtensionMethod(object):
    '''
    Decorator for extending existing classes with extension methods. Similar
    to the C# concept. Essentially the new method is monkey patched into the 
    class. 
    Warning: This can't be used to override methods     
    '''


    def __init__(self, extendingClass : type):
        '''
        Constructor: Takes the type that is being extended
        '''
        self._extendingClass = extendingClass
        
    def __call__(self, f : Callable):
        '''
        Applies the decoration to the function
        '''
        if not hasattr(self._extendingClass, f.__name__):
            setattr(self._extendingClass, f.__name__, f)
        else:
            raise AttributeError("Extension methods can't override existing "
                                 + "methods. Subclass the object instead.")
            
        return lambda *args: f(*args)
        