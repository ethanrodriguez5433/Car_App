import random


class Car:
    def __init__(self, Make='none', Model='none', Year='none', Name='none'):
        self.make = Make
        self.model = Model
        self.year = Year
        self.name = Name

        self.id = f'{random.randint(0, 9999999):07}'
        self.check()

    def check(self):
        if (self.model == self.make == self.name == 'none'):
            return 1

    def getLog(self):
        return

    def addMaintenance(self, name, date, unit, freq):
        return

    def addMod(self, date, mech, part, track):
        return

    

class Maintenance:
    def __init__(self, Name, Description, Unit, Freq, LastDate):
        self.name = Name
        self.description = Description
        self.unit = Unit
        self.freq = Freq
        self.lastdate = LastDate

    def updateLastDate(self):
        return
    

class Mod:
    def __init__(self, Mechanic, PartName, Description, Tracker):
        self.mechanic = Mechanic
        self.partname = PartName
        self.description = Description
        self.tracker = Tracker

        
        
    