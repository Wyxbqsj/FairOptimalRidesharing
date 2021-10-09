from typing import List
from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving
from orderPackage.GreedyFRM import GFRM



class Passenger:
    def __init__(self, name):
        self.name = name
        self.initial_prefs = []  # a passenger's initial set of preferences
        self.current_prefs = []  # a passenger's current set of preferences

    # class variable to store all the passengers
    ppl = {}

    # somebody is going to propose!!
    def propose(self, somebody):
        somebody.receive(self)

    # when somebody receives a proposal in phase 1
    def receive(self, somebody):
        current_prefs = self.current_prefs

        # need to cross off those behind current proposal
        prefs_to_chop = current_prefs[(current_prefs.index(somebody) + 1):]
        for passenger in prefs_to_chop:
            self.cross_off(passenger)

    # crosses off a potential match
    def cross_off(self, passenger):
        # removes each from each other's preference array
        if passenger in self.current_prefs:
            self.current_prefs.remove(passenger)
        if self in passenger.current_prefs:
            passenger.current_prefs.remove(self)

        # initiate a new proposal
        if len(passenger.current_prefs) > 0:
            passenger.propose(passenger.current_prefs[0])


    # find a passenger who still has a second column
    # return False if there is no passenger left
    @staticmethod
    def find_passenger_with_second_column():
        res = False
        for passenger in Passenger.ppl.values():
            if len(passenger.current_prefs) > 1:
                res = passenger
                break
        return res

    # return just the names of the people in the preference arrays
    def getPrefs(self, time):
        res = []
        if time == 'initial':
            for pref in self.initial_prefs:
                res.append(pref.name)
        else:
            for pref in self.current_prefs:
                res.append(pref.name)
        return res

    # generates the hash to display all people's preferences
    @staticmethod
    def prefsMatrix(time):
        res = {}
        for passenger_name, passenger_object in Passenger.ppl.items():
            res[passenger_name] = passenger_object.getPrefs(time)
        return res

    @staticmethod
    def setup(prefs):
        # create ppl hash which have names as keys
        # and the corresponding passenger objects as values
        for passenger in prefs:
            Passenger.ppl[passenger] = Passenger(passenger)

        # add the appropriate passenger objects to their preference array
        for passenger_name, passenger_object in Passenger.ppl.items():  # the passenger
            for pref_name in prefs[passenger_name]:  # their current_prefs
                # populate the initial preference array
                passenger_object.initial_prefs.append(Passenger.ppl[pref_name])
                # populate the current preference array
                passenger_object.current_prefs.append(Passenger.ppl[pref_name])

    # determines whether everybody was matched
    @staticmethod
    def who_wasnt_matched():
        ppl_without_match = []
        for passenger_name, passenger_object in Passenger.ppl.items():
            if len(passenger_object.current_prefs) != 1:
                # they don't have a match!
                ppl_without_match.append(passenger_object)
        return ppl_without_match

    def better_prefs(self):
        initial_prefs = self.initial_prefs
        # pprint.pprint(initial_prefs)
        final_prefs = self.current_prefs
        match = final_prefs[0]
        better_prefs = initial_prefs[:initial_prefs.index(match)]

        def passenger_name_string(obj):
            return obj.name

        # print(self.name + "," + str(list(map(passenger_name_string,better_prefs))))
        return better_prefs

    @staticmethod
    def was_the_match_stable():
        stable = True
        for my_name, my_object in Passenger.ppl.items():
            my_better_ppl = my_object.better_prefs()
            for passenger in my_better_ppl:
                their_better_ppl = passenger.better_prefs()
                if my_object in their_better_ppl:
                    stable = False
                    break
        return stable

    @staticmethod
    def empty_column():
        empty = False
        for passenger in Passenger.ppl.values():
            if len(passenger.current_prefs) == 0:
                empty = True
                break
        return empty
