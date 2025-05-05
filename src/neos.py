import json

# Class to represent a Near-Earth Object with attributes name, diameter, and hazard status.
class NearEarthObject:
    def __init__(self, name, diameter, is_potentially_hazardous):
        # Initialize NearEarthObject with name, diameter, and hazardous status.
        self.name = name
        self.diameter = diameter
        self.is_potentially_hazardous = is_potentially_hazardous

    def __repr__(self):
        # Return a string representation of the NearEarthObject instance.
        return f"NearEarthObject(name={self.name}, diameter={self.diameter}, hazardous={self.is_potentially_hazardous})"

    def __lt__(self, higher):
        # Compare two NearEarthObject instances based on their diameter.
        return self.diameter < higher.diameter

# Function to read NEO data from a JSON file and return a list of NearEarthObject instances.
def read_json(file):
    infile = open(file)  # Open the JSON file.
    data = json.load(infile)  # Load JSON data from the file.
    neos = []  # Initialize an empty list to store Near-Earth Object instances.

    # Iterate over NEOs and create NearEarthObject instances.
    for date, neo_list in data["near_earth_objects"].items():
        for neo_data in neo_list:
            name = neo_data.get("name")
            diameter = neo_data.get("estimated_diameter", {}).get("meters", {}).get("estimated_diameter_max")
            is_potentially_hazardous = neo_data.get("is_potentially_hazardous_asteroid", False)

            if name and diameter is not None:
                neos.append(NearEarthObject(name, diameter, is_potentially_hazardous))
            else:
                print(f"Missing data: {neo_data}")

    return neos  # Return the list of NEOs.

# Function to filter NEOs based on minimum diameter and hazard status.
def filter_neos(neos, min_diameter=400, is_potentially_hazardous=True):
    filtered_neos = [
        neo for neo in neos 
        if neo.diameter >= min_diameter and neo.is_potentially_hazardous == is_potentially_hazardous
    ]
    return filtered_neos

# Class to analyze NEO data for properties like average diameter and hazard count.
class NeoAnalyzer:
    def __init__(self, neos):
        # Initialize NeoAnalyzer with a list of Near-Earth Objects.
        self.neos = neos

    def average_diameter(self):
        # Calculate the average diameter of the NEOs.
        if not self.neos:
            return 0
        tot_dia = sum(neo.diameter for neo in self.neos)
        average = tot_dia / len(self.neos)
        return average

    def count_potentially_hazardous(self):
        # Count the number of potentially hazardous NEOs.
        return sum(1 for neo in self.neos if neo.is_potentially_hazardous)

# Read NEO data from 'neos.json' and store in a list.
neos = read_json('neos.json')

# Filter NEOs based on diameter and hazard status.
danger_neos = filter_neos(neos, min_diameter=400, is_potentially_hazardous=True)
print(f"Potentially hazardous NEOs : {len(danger_neos)}\n")

# Print information of filtered hazardous NEOs.
for neo in danger_neos:
    print(f"Name: {neo.name}, Diameter: {neo.diameter} meters, Hazardous: {neo.is_potentially_hazardous}")

# Create an instance of NeoAnalyzer and calculate the average diameter.
analyzer = NeoAnalyzer(neos)
avg_diameter = analyzer.average_diameter()
print(f"\nAverage diameter of NEOs: {avg_diameter} meters")

# Count potentially hazardous NEOs.
hazard_count = analyzer.count_potentially_hazardous()
print(f"Potentially hazardous NEOs: {hazard_count}")

# Sort NEOs by diameter and print the smallest one.
sorted_neos = sorted(neos)
smallest_neo = sorted_neos[0]
print(f"The smallest NEO is {smallest_neo.name} with a diameter of {smallest_neo.diameter} meters.")