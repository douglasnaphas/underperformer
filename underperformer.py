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

# Return the employee id of the worst employee considering only non-cumulative performance this week.
def weeks_worst( emps ):
	return None

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

def prod_mean( prod ):
    t = 0.0 
    for p in prod:
        t += ( prod[p][TOTAL] + 0.0 ) / prod[p][WEEKS]
    # get the average of the array of averages
    return t / len(prod)

# Return True if worst_id_c is the id of an underperformer in employee matrix prod, False otherwise.
def underperf( prod, args, worst_id_c ):
	stddev = prod_stddev( prod )
	mean = prod_mean( prod )
	worst_av = prod[worst_id_c][TOTAL] / prod[worst_id_c][WEEKS]
	# Apply the stddev test.
	stddevs_behind = ( mean - worst_av ) / stddev
	if args.stddevs != None and stddevs_behind >= args.stddevs:
		print "Employee %d is currently %f standard deviations behind the mean of %f." % ( worst_id_c, stddevs_behind, mean )
		return True
	# Apply the ratio test.
	# Get the average of all but the worst.
	if args.ratio != None:
		all_but_worst = prod.copy()
		all_but_worst.pop( worst_id_c )
		mean_rest = prod_mean( all_but_worst )
		if worst_av <= args.ratio * mean_rest:
			print "Employee %d average so far: %f, average for others: %f" % ( worst_id_c, worst_av, mean_rest )
			return True
	return False

# Get command line options.
parser = argparse.ArgumentParser( description='Find the underperformer.', epilog='Data must be JSON like [[{\'employee\':1, \'workCount\':71},{\'employee\':2, \'workCount\':72}], [{\'employee\':1, \'workCount\':21},{\'employee\':2, \'workCount\':52}]]' )
parser.add_argument( '--version', help='print the current version and exit', action='version', version=VERSION )
parser.add_argument( '--verbose', action = 'store_true' )
source_group = parser.add_mutually_exclusive_group( required = True )
source_group.add_argument( '--file', '-f', help = 'read performance data from FILE', type = file )
source_group.add_argument( '--url', '-u', help = 'read performance data from URL' )
calc_group = parser.add_mutually_exclusive_group( required = True )
calc_group.add_argument( '--stddevs', '-s', help = 'an underperformer\'s cumulative output is STDDEVS standard deviations from the mean', type = float )
calc_group.add_argument( '--ratio', '-r', help = 'an underperformer cumulatively produces RATIO * the average of everyone else, or worse', type = float )
calc_group.add_argument( '--row', '-w', help = 'an underperformer is the worst employee for ROW weeks in a row; not implemented' )
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
		if args.verbose:
			print "Week %d" % week
		emp = 0
		while emp < len ( weeks[week] ):
			if EMPLOYEE in weeks[week][emp]:
				empid = weeks[week][emp][EMPLOYEE]
			else:
				raise MyError("Bad data at week %d, employee %d (0-based)" % ( week, emp ) )
			if not empid in prod:
				prod[empid] = { TOTAL : 0.0, WEEKS : 0.0 }
			prod[empid][TOTAL] += weeks[week][emp][WORKCOUNT]
			prod[empid][WEEKS] += 1
			if args.verbose:
				print "Employee %d: %f" % ( empid, ( prod[empid][TOTAL] + 0.0 ) / prod[empid][WEEKS] )
			emp += 1
		worst_id_c = weeks_worst_c( prod )
		if args.verbose:
			print "The worst employee this week has id %d" % worst_id_c
		stddev = prod_stddev( prod )
		mean = prod_mean( prod )
		if args.verbose:
			print "Worst to mean is %f stddevs" % ( ( mean - prod[worst_id_c][TOTAL] / prod[worst_id_c][WEEKS] ) / stddev )
		if args.verbose:
			print ""
		underperformer = underperf( prod, args, worst_id_c )
		if underperformer:
			print "As of week %d, we have an underperformer." % week
			print "Employee %d is underperforming and should be fired." % worst_id_c
		week += 1
except MyError as ie:
	print ie.value

if not underperformer:
	print "All our employees are equally bad."
