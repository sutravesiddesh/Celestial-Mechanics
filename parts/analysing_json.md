# Part 1. Manipulating JSON and dictionaries [[toc](../README.md#table-of-content)]

During this section, you will use an extracted dataset from the _NASA's Near Earth Object Web Service_ (NeoWs).
You will have to retrieve information about _Near-Earth Objects_ (NEOs) from a JSON file.

> :exclamation: **Important**
>
> your code for this question should go in a source file called `neos.py` and
> should run without issues by calling the following command in a terminal
> ```shell
> python neos.py
> ```
>
> so don't forget to create this new `neos.py` file :wink:

### Introduction to the data [[toc](../README.md#table-of-content)]

The JSON data is organized hierarchically. Below is a simplified example of what the JSON format for _NEO_ data might look like:

```json
{
    "element_count": 10, # Total number of NEOs in the response
    "near_earth_objects": {
        "2023-10-16": [ # Date in YYYY-MM-DD format
            {
                "links": {
                    "self": "URL to detailed NEO information"
                },
                "id": "12345", # Unique identifier for the NEO
                "name": "Apophis", # Name of the NEO
                "nasa_jpl_url": "URL to JPL's page for this NEO",
                "absolute_magnitude_h": 19.7, # Absolute magnitude
                "estimated_diameter": {
                    "kilometers": {
                        "estimated_diameter_min": 0.186,
                        "estimated_diameter_max": 0.416
                    }
                },
                "is_potentially_hazardous_asteroid": False, # Indicates if the NEO is hazardous
                "close_approach_data": [
                    {
                        "close_approach_date": "2023-10-16", # Date of closest approach
                        "miss_distance": {
                            "astronomical": "0.1 AU", # Miss distance in astronomical units
                            "kilometers": "15,000,000" # Miss distance in kilometers
                        },
                        "relative_velocity": "10.5 km/s" # Relative velocity in km/s
                    }
                ]
            },
            # More NEOs for the same date
        ],
        # More dates with NEOs
    }
}
```

In this example:
- `$.element_count` tells you the total number of _NEOs_ in the file.
- `$.near_earth_objects` contains _NEO_ data organized by date.
- each date inside `$.near_earth_objects` is a key in the format `YYYY-MM-DD`.
- for each _NEO_ on a given date, you have information about its ID, name, URL links, absolute magnitude, estimated diameter, hazard status, and close approach data.

### Question 1.1 [[toc](../README.md#table-of-content)]
#### Creating a NEO class
Define a Python class named `NearEarthObject` that represents a _Near-Earth Object_.
The class should have the following attributes:
- `name`: The name of the _NEO_.
- `diameter`: The diameter of the _NEO_ in meters.
- `is_potentially_hazardous`: A boolean value indicating whether the _NEO_ is potentially hazardous.

Your class should also have a constructor to initialize these attributes.

```python
# You can see how to use the NEO class here
neos = [
    NearEarthObject("(2022 UY)", 47.8674154419, False),
    NearEarthObject("(2022 WL)", 36.3111479288, False),
    NearEarthObject("(2022 WT11)", 85.9092601232, False),
    NearEarthObject("(2023 KD1)", 74.1378485408, False),
    NearEarthObject("(2023 KQ5)", 1066.694310755, False),
    NearEarthObject("(2023 LR1)", 1330.5768979725, False),
    NearEarthObject("(2023 MK1)", 381.979432159, True),
    NearEarthObject("337558 (2001 SG262)", 809.1703835499, True),
    NearEarthObject("(2007 EC)", 210.8822267643, False),
    NearEarthObject("(2017 HG)", 34.201092472, False),
    NearEarthObject("(2017 TM6)", 130.0289270043, False),
    NearEarthObject("(2017 TT6)", 85.9092601232, False),
    NearEarthObject("(2018 UC)", 39.2681081809, False),
    NearEarthObject("(2019 CE4)", 1432.3197447269, True),
    NearEarthObject("(2019 UZ3)", 23.6613750114, False),
    NearEarthObject("(2022 QQ3)", 205.1351006288, False),
    NearEarthObject("(2023 KH4)", 23.4444462214, False),
    NearEarthObject("523585 (1998 MW5)", 986.3702813054, False),
    NearEarthObject("(1998 HH49)", 322.1365318908, True),
    NearEarthObject("(2004 TP1)", 430.566244241, True),
]
```

### Question 1.2 [[toc](../README.md#table-of-content)]
#### Reading JSON data and storing _NEO_ data

Write a function to read the JSON file and return a list of `NearEarth` objects.
For the diameter, use `estimated_diameter_max`, of course, in meters.
> :bulb: **Note**
>
> This is a non-blocking question. If you don't succeed to read data from the JSON file, you can continue with the next question and use the given dataset from [Question 1.1](#question-11-toc).

### Question 1.3 [[toc](../README.md#table-of-content)]
#### Filtering _NEOs_

Write a function `filter_neos` to filter _NEOs_ based on specific criteria. This function takes the following parameters:
- `neos`: list of `NearEarthObject` objects
- `min_diameter`: Minimum diameter (in meters) that a _NEO_ must have to be considered.
- `is_potentially_hazardous`: A boolean value to filter _NEOs_ that are potentially hazardous or not.

The `filter_neos` method should return a new list of `NearEarthObject` objects that meet the specified criteria.
Call this function by giving the `neos` list generated from the previous questions (can be the list from either [Question 1.1](#question-11-toc) or [Question 1.2](#question-12-toc)).
Find the other parameters to print the number of `neos` that are potentially hazardous objects and have a diameter bigger than 400m.

> :bulb: **Note**
>
> To get the number of elements in a `list`, use the `len` function

### Question 1.4 [[toc](../README.md#table-of-content)]
#### Create an analyser

Write a Python class named `NeoAnalyzer` that is responsible for computing additional information about _NEOs_.
The class should have the following methods:
- `__init__(self, neos)`: Constructor that takes a list of `NearEarthObject` objects.
- `average_diameter(self)`: A method to calculate the average diameter of all _NEOs_ and return it.
- `count_potentially_hazardous(self)`: A method to count and return the number of _NEOs_ that are potentially hazardous.

### Question 1.5 [[toc](../README.md#table-of-content)]
#### Analyse the data

Create an instance of the `NeoAnalyzer` class, passing the neos list as a parameter.
Compute and display the average diameter and the count of potentially hazardous _NEOs_ using the `NeoAnalyzer` methods.

> :bulb: **Note**
>
> You have to give to the constructor the `neos` list generated from the previous questions.
> It can be the list generated from the [Question 1.1](#question-11-toc) or the [Question 1.2](#question-12-toc).

### Question 1.6 [[toc](../README.md#table-of-content)]
#### Implementing Comparison for Sorting NEOs

Go back to your `NearEarthObject` class and implement the `__lt__` method (less than) that compares `NearEarthObject` objects and allows you to sort them in ascending order by their `diameter`.

### Question 1.7 [[toc](../README.md#table-of-content)]
#### Sorting data for faster analyse

Create a list of `NearEarthObject` sorted by `diameter`, and print the diameter and the name of the smallest _NEO_.
> :pray: **Help**
>
> The `sorted` function returns a sorted list:
> ```python
> assert (sorted([4, 1, 3, 2]) == [1, 2, 3, 4])
> ```

---
---
> [go to next questions](simulation.md)
