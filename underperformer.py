#!/usr/bin/env python

# Find the underperformer.

# constants
	# default params

# Get command line options: --file=FILE, --url=URL, --threshold=NUMBER, --help, --stdevs=STDEVS

# Read in source.

# weeks = json_decode( source )

# prod = array() # empl_num => running average production per week, number of weeks.
		     # The workforce may vary.
# worst_id = null

# underperformer = null

# while ( week < count( weeks ) && !underperformer )
	# for emp in weeks[week] # Get running average weekly production for each.
		# empid = weeks[week][emp][employee]
		# if ( array_key_exists( empid in prod ) )
			# Update totals.
			# prod[empid][total] += weeks[week][emp][workCount]
			# prod[empid][w]++
	# Find the worst employee (all weeks).
	# underperformer = underperf( prod )

# if !underperformer
	# print no_underperf_message()
# else
	# print underperformer_message( prod )
		

# ( prod[] -> id of the underperformer, or null if there is none )
# function underperf( array prod[empid=>[total, weeks]], function test( worst_id, prod[empid=>
	# [total, weeks]] ) )
	# 

# function stdev_test

# function avg_test
