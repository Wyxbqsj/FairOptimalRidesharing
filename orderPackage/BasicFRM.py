
from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving
from setting import *
import sys
from preference.passenger import Passenger


def execute(prefs, recursion_limit=10000):
	# adjust the system's recursion call depth limit
	# system default is 1000
	sys.setrecursionlimit(recursion_limit)

	# SETUP --> CREATE PERSON OBJECTS
	Passenger.setup(prefs)

	# PHASE 1
	for passenger in Passenger.ppl.values():
		if len(passenger.current_prefs) > 0:
			passenger.propose_to(passenger.current_prefs[0])  # propose to your top choice


	# PHASE 2
	current_passenger = Passenger.find_passenger_with_second_column()
	num_rotations = 1    # number of rotations so far...
	while current_passenger:
		current_pref = current_passenger.current_prefs[1]
		current_pref.cross_off(current_pref.current_prefs[-1])
		# has_empty_column_after_phase_one = Passenger.empty_column()
		# if has_empty_column_after_phase_one:
		# 	break
		num_rotations = num_rotations + 1
		current_passenger = Passenger.find_passenger_with_second_column()

	ppl_without_match = Passenger.who_wasnt_matched() #没有被匹配上的人


	return Passenger.prefsMatrix('current')

if __name__ == '__main__':
	from datadeal.problem import ProblemInstance
	problemInstance = ProblemInstance(data_path, 1000)
	currentTime = problemInstance.startTime+60
	orders, drivers = problemInstance.batch(currentTime)
	T = cost_saving(orders)
	prefs = {}
	for i in T.keys():
		li = []
		for j in T[i]:
			prefs.setdefault(i,li).append(j.match_id)

	# execute the match!!
	A = execute(prefs)

