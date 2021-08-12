#!/usr/bin/python3

'''
Print Helpers.

Copyright (C) 2021 Dr. Sergey Kolevatov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

from termcolor import colored

##########################################################

def print_fatal( s ):
    pref = colored( 'FATAL: ', 'magenta' )
    print( pref + s )

##########################################################

def print_error( s ):
    pref = colored( 'ERROR: ', 'red' )
    print( pref + s )

##########################################################

def print_warning( s ):
    pref = colored( 'WARNING: ', 'yellow' )
    print( pref + s )

##########################################################

def print_info( s ):
    print( "INFO: " + s )

##########################################################

def print_debug( s, end_par = "\n", flush_par = False ):
    pref = colored( 'DEBUG: ' + s, 'grey', attrs=['bold'] )
    print( pref, end=end_par, flush=flush_par )

##########################################################

def print_trace( s ):
    pref = colored( 'TRACE: ' + s, 'grey', attrs=['bold'] )
    print( pref )

##########################################################
