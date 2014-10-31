#!/usr/bin/env python

# Find the underperformer.

import argparse
import urllib
import json

VERSION = '0.1.0'
INPUT_LIMIT = 2**30 # The string of data must be 1 G or less.
# Array key names.
EMPLOYEE = 'employee'
WORKCOUNT = 'workCount'
TOTAL = 'total'
WEEKS = 'w'
AVG = 'avg'

class MyError( Exception ): # TODO: Is there really no built-in way to do this?
	def __init__( self, value ):
		self.value = value
	def __str__( self ):
		return repr( self.value )

# Return the employee id of the worst employee this week, considering all past weeks (cumulatively).
# @param array emps Array of employees, empid => { TOTAL : total production, WEEKS : weeks }
def weeks_worst_c( emps ):
	worst_id = emps.keys()[0]
	worst_av = ( emps[worst_id][TOTAL] + 0.0 ) / emps[worst_id][WEEKS] # TODO: handle floats better
	for emp in emps:
		if ( ( emps[emp][TOTAL] + 0.0 ) / emps[emp][WEEKS] ) < worst_av:
			worst_id = emp
			worst_av = ( emps[worst_id][TOTAL] + 0.0 ) / emps[worst_id][WEEKS]
	return worst_id

def prod_stddev( prod ):
	# get the array of averages, empid => av
	t = 0.0
	for p in prod:
		prod[p][AVG] = ( prod[p][TOTAL] + 0.0 ) / prod[p][WEEKS]
		t += prod[p][AVG]
	# get the average of the array of averages
	av_av = t / len(prod)
	# for each in the array of averages, get the squared deviation
	sdt = 0.0
	for p in prod:
		sdt += ( av_av - prod[p][AVG] ) ** 2.0
	# get the variance
	v = sdt / len(prod)
	# get the stddev
	return v ** 0.5

def prod_mean( prod rray of averages, empid => av:
    t = 0.0 
    for p in prod:
        prod[p][AVG] = ( prod[p][TOTAL] + 0.0 ) / prod[p][WEEKS]
        t += prod[p][AVG]
    # get the average of the array of averages
    return t / len(prod)
	



# ( prod[] -> id of the underperformer, or null if there is none )
# function underperf( array prod[empid=>[total, weeks]], function test( worst_id, prod[empid=>
	# [total, weeks]] ) )
	# 

# function stdev_test

# function avg_test

# Get command line options.
parser = argparse.ArgumentParser( description='Find the underperformer.' )
parser.add_argument( '--version', help='print the current version and exit', action='version', version=VERSION )
source_group = parser.add_mutually_exclusive_group( required = True )
source_group.add_argument( '--file', '-f', help = 'read performance data from FILE', type = file )
source_group.add_argument( '--url', '-u', help = 'read performance data from URL' )
calc_group = parser.add_mutually_exclusive_group( required = True )
calc_group.add_argument( '--stddevs', '-s', help = 'an underperformer is STDDEVS standard deviations from the next worse performer', type = float )
calc_group.add_argument( '--ratio', '-r', help = 'an underperformer produces RATIO * the average of everyone else, or worse', type = float )
args = parser.parse_args()

# Read in source.
if args.file:
	# Try to read the file to a string.
	try:
		source_string = args.file.read( INPUT_LIMIT )
		args.file.close
	except:
		print "Error reading from %s" % args.file.name
else:
	# Try to read the URL to a string.
	try:
		source_page = urllib.urlopen( args.url )
		source_string = source_page.read( INPUT_LIMIT )
		source_page.close
	except:
		print "Error collecting data from URL %s" % args.url
	
# weeks = json_decode( source_string )
try:
	weeks = json.loads( source_string )
except:
	print "Error decoding source JSON data."

prod = {} # Empty dictionary. Will be: empl_num => [ running total production, num of weeks]. The workforce may vary.
worst_id = None # this week
underperformer = None # overall
week = 0

try:
	while week < len(weeks) and not underperformer:
		emp = 0
		while emp < len ( weeks[week] ):
			if EMPLOYEE in weeks[week][emp]:
				empid = weeks[week][emp][EMPLOYEE]
			else:
				raise MyError("Bad data at week %d, employee %d (0-based)" % ( week, emp ) )
			if not empid in prod:
				prod[empid] = { TOTAL : 0, WEEKS : 0 }
			prod[empid][TOTAL] += weeks[week][emp][WORKCOUNT]
			prod[empid][WEEKS] += 1
			print ( prod[empid][TOTAL] + 0.0 ) / prod[empid][WEEKS]
			emp += 1
		worst_id_c = weeks_worst_c( prod )
		print "The worst employee this week has id %d" % worst_id_c
		all_but_worst = prod.copy()
		all_but_worst.pop( worst_id_c )
		second_worst_id_c = weeks_worst_c( all_but_worst )
		print "The second worst employee this week has id %d" % second_worst_id_c
		stddev = prod_stddev( prod )
		print stddev
		print "Worst to mean is %f stddevs" % 0
		print "Worst to second worst is %f stddevs" % 0
		# underperformer = underperf( prod )
		print ""
		week += 1
except MyError as ie:
	print ie.value

# if !underperformer
	# print no_underperf_message()
# else
	# print underperformer_message( prod )
		




