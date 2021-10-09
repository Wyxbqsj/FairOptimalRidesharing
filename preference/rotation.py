from preference.costSaving import cost_saving
from orderPackage.GreedyFRM import GFRM
from preference.passenger import Passenger

class Rotation:
    def __init__(self) -> None:
        self.rotation = list()

    def addPair(self, x: Passenger,y: Passenger):
        pair=[x,y]
        self.rotation.append(pair)

    #def eliminate(self):
