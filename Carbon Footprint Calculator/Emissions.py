# -*- coding: utf-8 -*-
"""
Anna Garik
CS 521- Spring 1
2/28/2022
Final Project
Class and dictionary definitions for program calculating user's footprint
"""
#Dictionaries:
#Pounds of carbon emitted per mile
transport_emissions_dict = {"car":0.91, "bus":0.6, "train":0.35}

#Home energy emissions per 1 person per year
home_emissions_dict = {"natural gas":3070.86, "electricity":5455.25, "fuel oil":4848.18, "propane":2243.45}

#Home waste emissions per 1 person per year
waste_emissions_dict = {"metal":-89.38, "plastic":-35.56, "glass":-25.38,
                        "paper":-140.6}

class Emissions_Footprint:
    """Superclass for home energy, transportation, and waste classes"""
    def __init__(self, emissions):
        """Constructor to initiaite class Emissions_Footprint and define addition for the class"""
        self.emissions = emissions
    #Magic method
    def __add__(self, other1):
        """Magic method (overloaded +) to define how to add different Emissions_Footprint subtype instances/objects"""
        return Emissions_Footprint(self.emissions + other1.emissions)   
    def value_total_emissions(self):
        """Get value of total emissions (home energy, transportation, waste)"""
        return(self.emissions)
    def __str__(self):
        """Return human-readble string telling user their total carbon footprint"""
        return("Your total estimated carbon emissions footprint is " + "{:,.2f}".format(self.emissions) + " lbs CO2")

#CO2 emissions per year based on home energy type
class Home_Energy(Emissions_Footprint):
    """Subtype of Emissions_Footprint, specialized for home energy"""
    def __init__(self, energy_type):
        """Constructor to initiaite the Home_Energy class"""
        super().__init__(0)
        #Private attribute
        self.__energy_type = energy_type
    
    def calc_emissions(self):
        """Return emissions from user's home energy type"""
        if self.__energy_type == "natural gas":
            self.emissions = home_emissions_dict["natural gas"]
        elif self.__energy_type == "electricity":
           self.emissions = home_emissions_dict["electricity"]
        elif self.__energy_type == "fuel oil":
            self.emissions = home_emissions_dict["fuel oil"]
        elif self.__energy_type == "propane":
            self.emissions = home_emissions_dict["propane"]
        return(self.emissions)
    
    def __str__(self):
        """Return human-readble string telling user their home energy type emissions"""
        return("Your estimated yearly carbon emissions footprint from home energy is " + "{:,.2f}".format(self.emissions) + " lbs CO2")

#Car: input miles per year or use average
class Transport_Car(Emissions_Footprint):
    """subtype of Emissions_Footprint specialized for transportation type=car."""
    def __init__(self, miles_per_yr='11398'):
        """Constructor to initialize class Transport_Car, input is user's number of miles travelled in car per year, defaults to national average if the user is unsure"""
        super().__init__(0)
        self.miles_per_yr = float(miles_per_yr)
    
    def calc_emissions(self):
        """Return emissions when user's transportation type is car"""
        self.emissions = self.miles_per_yr*transport_emissions_dict["car"]
        return(self.emissions)
    
    def __str__(self):
        """Return human-readble string telling user their transportation emissions if they use a car"""
        return("Your estimated yearly carbon emissions from transportation are " + "{:,.2f}".format(self.emissions) + " lbs CO2")
        
        
#Bus/train: input trips per week
class Transport_Public(Emissions_Footprint):
    """Subtype of Emissions_Footprint, specialized for when user's transportation type is public transport"""
    def __init__(self, trips_per_week):
        """Constructor to initiaite the Transport_Public class"""
        super().__init__(0)
        #Avg 1 way public transit trip in Boston is 3.73 (multiply by 2 to get round trip), 52 weeks in a year
        (avg_round_trip, weeks_yr) = (3.73*2, 52)
        #Miles travelled per year on public transit
        self.trips_per_week = trips_per_week
        self.miles_per_yr = float(self.trips_per_week)*avg_round_trip*weeks_yr
    
    def calc_emissions(self, public_transport_type):    
        """Return emissions when user's transportation type is public transportation"""
        self.public_transport_type = public_transport_type
        if self.public_transport_type == "bus":
            self.emissions = self.miles_per_yr*transport_emissions_dict["bus"]
        elif self.public_transport_type == "train":
            self.emissions = self.miles_per_yr*transport_emissions_dict["train"]
        return(self.emissions)
    
    def __str__(self):
        """Return human-readble string telling user their transportation emissions if they use public transit"""
        return("Your estimated yearly carbon emissions from transportation are " + "{:,.2f}".format(self.emissions) + " lbs CO2")
            
#CO2 emissions per year based on waste disposal
class Waste(Emissions_Footprint):
    """Subtype of Emissions_Footprint, specialized for user's waste habits"""
    def __init__(self):
        """Constructor to initiaite the Waste class"""
        super().__init__(0)
        waste_yearly_avg = 691.5
        self.waste = waste_yearly_avg
    
    #Private method
    """Private method to determine the reduction in user's waste carbon emissions from what they recycle"""
    def __recycling(self, recycling_type):
        if recycling_type.lower() == "none":
            self.carbon_reduction = 0
            return(self.carbon_reduction)
        
        elif recycling_type.lower() != "none":
            #List
            possible_materials = list(waste_emissions_dict.keys())
            carbon_reduction = []
            for i in range(0, len(possible_materials)):
                if str(possible_materials[i]) in recycling_type:
                    carbon_reduction.append(waste_emissions_dict[possible_materials[i]])
            self.carbon_reduction = sum(carbon_reduction)      
            return(self.carbon_reduction)
    
    def calc_emissions(self, recycling_type):
        """Return user's waste emissions"""
        self.emissions = self.waste + self.__recycling(recycling_type)
        return(self.emissions)
    
    def __str__(self):
        """Return human-readble string telling user their waste emissions"""
        return("Your estimated yearly carbon emissions from waste are " + "{:,.2f}".format(self.emissions) + " lbs CO2")
        
 
    


















