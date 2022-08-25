"""
Anna Garik
CS 521- Spring 1
2/28/2022
Final Project
Program with multiple class types and functions that provide user's carbon print based on their home energy type, transportation, and waste habits. A breakdown of the user' carbon footprint can be exported to a text file.
"""
#Import necessary classes and dictionaries from Emissions.py
from Emissions import Home_Energy
from Emissions import Transport_Car
from Emissions import Transport_Public
from Emissions import Waste 
from Emissions import waste_emissions_dict


def export_info(activity_selected, activity_emissions, total_emissions_value):  
    """Compile useful information on user's carbon footprint input to be exported to a text file"""
    activity_emissions = round(activity_emissions, 2)
    activity_percent_total = "{:,.2f}".format(100*(activity_emissions/total_emissions_value))+"%"
    #Tuple:
    tuple_activity_info = (activity_selected, activity_emissions, activity_percent_total)
    return(tuple_activity_info)

def export_carbon_footprint(file_name):
    """Export compiled information on user's carbon footprint to a text file created by the user"""
    file_name = file_name+".txt"            
    output_file = open(file_name, "w") 
    output_text = total_carbon_footprint + "\n" + "Breakdown:\n"+"Based on your selection (" + str(home_energy_export[0]) + "), your yearly home energy carbon emissions are " + str(home_energy_export[1]) + " lbs of CO2, which is equal to " + str(home_energy_export[2]) + " of your total carbon footprint.\n" + "Based on your selection (" + str(transport_export[0]) + "), your yearly transportation carbon emissions are " + str(transport_export[1]) + " lbs of CO2, which is equal to " + str(transport_export[2]) + " of your total carbon footprint.\n" + "Based on your selection (" + str(waste_export[0]) + "), your yearly waste carbon emissions are " + str(waste_export[1]) + " lbs of CO2, which is equal to " + str(waste_export[2]) + " of your total carbon footprint.\n"
    output_file.writelines(output_text)
    print("Your carbon footprint information has successfully been exported. Thank you!")
    output_file.close()

#Get user input on home energy type
while True:
    home_energy_input = input("Please enter your home energy type from the following list: natural gas, electricity, fuel oil, propane: ")
    home_energy_selected = home_energy_input.lower()
    if home_energy_selected == "natural gas" or home_energy_selected == "electricity" or home_energy_selected == "fuel oil" or home_energy_selected == "propane":
        home_energy_instance = Home_Energy(home_energy_selected)
        home_energy_emissions = home_energy_instance.calc_emissions()
        print(home_energy_instance)
        break
    else: 
        print("Please enter one of the options listed.")
        continue

#Get user input on transport type
while True:   
    transport_input = input("Please enter your primary mode of transportation from the following list: car, bus, or train: ")
    transport_selected = transport_input.lower()
    if transport_selected == "car" or transport_selected == "bus" or transport_selected == "train":
        break
    else:
        print("Please choose only one mode of transportation from the given options.")
        continue


if transport_selected == "car":
    while True:
        try:
            input_car_miles = input("Please enter the number of miles you travel per year by car. If you do not know, pleaase enter a 0 and the national average will be used: ")
            input_car_miles = float(input_car_miles)
        
        except ValueError:
            print("Please enter a numeric value.")
            continue
            
        if input_car_miles == 0:
            transport_instance = Transport_Car()
            transport_emissions = transport_instance.calc_emissions()
            print(transport_instance)
            break
        
        else:
            transport_instance = Transport_Car(input_car_miles)
            transport_emissions = transport_instance.calc_emissions()
            print(transport_instance)
            break
            

if transport_selected == "bus":          
    while True:
        try:
            input_weekly_trips = input("Please enter the number of trips you make by bus per week: ")
            input_weekly_trips = float(input_weekly_trips)
        except ValueError:
            print("Please enter an integer.")
            continue
            
        transport_instance = Transport_Public(input_weekly_trips)
        transport_emissions = transport_instance.calc_emissions(transport_selected)
        print(transport_instance)
        break
            
        
if transport_selected == "train":          
    while True:
        try:
            input_weekly_trips = input("Please enter the number of trips you make by train per week: ")
            input_weekly_trips = float(input_weekly_trips)
            
        except ValueError:
            print("Please enter an integer.")
            continue
            
        transport_instance = Transport_Public(input_weekly_trips)
        transport_emissions = transport_instance.calc_emissions(transport_selected)
        print(transport_instance)
        break

#Get user input on waste activities           
while True:
    recycling_input = input("Please enter what you recycle from the following list: metal, plastic, glass, paper. If you are entering more than one item, please use only commas to separate them. If you do not recycle any of these items, please enter \"none\": ")
    recycling_selected = recycling_input.lower()  
    list_recycling_selected = recycling_selected.split(",")  
    #Set: If user enters same value twice, make sure it's only counted once
    set_recycling_selected = set(list_recycling_selected)
    error_check = []
    for item in set_recycling_selected:
        if item not in waste_emissions_dict.keys() and item != "none":
            error_check.append("error")

    if len(error_check) >0:
        print("Please be sure to select only from the given items.")
        continue


    elif len(error_check) == 0 and recycling_selected == "none":
        waste_selected = "baseline waste emissions for one person with no recycling"
        waste_instance = Waste()
        waste_emissions = waste_instance.calc_emissions(recycling_selected)
        print(waste_instance)
        break
    
    elif len(error_check) == 0 and recycling_selected != "none":
        waste_selected = "baseline waste minus emissions saved from materials recycled: " + recycling_selected
        waste_instance = Waste()
        waste_emissions = waste_instance.calc_emissions(recycling_selected)
        print(waste_instance)
        break

#Return user's total yearly carbon footprint
total_carbon_footprint = str(home_energy_instance + transport_instance + waste_instance)
print("\n"+total_carbon_footprint)

#Option for user to export their carbon footprint information
export_wanted = input("If you would like to export your carbon footprint assessment, please enter \"yes\". If not, please enter \"no\": ")

if export_wanted == "yes":
    total_emissions_value = (home_energy_emissions + transport_emissions + waste_emissions)
    home_energy_export = export_info(home_energy_selected, home_energy_emissions, total_emissions_value)
    transport_export = export_info(transport_selected, transport_emissions, total_emissions_value)
    waste_export = export_info(waste_selected, waste_emissions, total_emissions_value)
    
    file_name = input("Please enter what you would like to name the text file where your carbon footprint information will be stored. Please note that this will create a new text file in this directory or will overwrite an existing text file with the same name: ")
    export_carbon_footprint(file_name)

else:
    print("Thank you for participating!")
    

#Unit Tests      
if __name__ == "__main__":
    try:
        #Enter home energy as electricity and calculate emissions
        my_home_energy = Home_Energy("electricity")
        assert my_home_energy.calc_emissions() == 5455.25
        assert str(my_home_energy) == "Your estimated yearly carbon emissions footprint from home energy is 5,455.25 lbs CO2"
        my_transportation = Transport_Car()
        assert my_transportation.calc_emissions()== 10372.18
        assert str(my_transportation) == "Your estimated yearly carbon emissions from transportation are 10,372.18 lbs CO2"
        print("Unit test successful")
    
    except AssertionError:
       print("Unit test was unsuccessful")







       
    
        















