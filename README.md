# Task: Train operations

The Train Station program is designed to manage information about trains and their loads from a JSON file. It provides functionalities to work with trains, locomotives, and wagons, as well as the ability to distribute loads among trains, remove unnecessary wagons and locomotives, and save data back to a JSON file.


## Features

The program reads train data and load information from a JSON file and initializes the Train Station with this data, obtaining the load to be distributed.

It displays a list of operable trains, which are valid and have locomotives and wagons.

Distributes a given load to all trains, removing unnecessary wagons and locomotives as needed to optimize the load distribution.

The program sorts the data by train's wagon max_load_mass and saves the sorted data back to the JSON file.

Wagons and locomotives are constructed within the Train class. The program provides methods to add, remove, and manage wagons and locomotives within a train:

    **__add__**: Add wagon or locomotive to train.
    **remove_wagon(wagons_number)**: Remove a wagon from a train by wagon number.
    **remove_locomotive(locomotive_index)**: Remove a locomotive from a train by index.

## Usage
Here's how you can use the Train Station program:

1. Initialize the Train Station with data from a JSON file that follows this structure:
```python
train_station = TrainStation("example_data.json")
```
json file example:

```json
{
    "trains": [
        {
            "locomotives": [
                {"mass": 0.1, "towable_mass": 1800}
            ],
            "wagons": [
                {"mass": 25.0, "max_load_mass": 120.0, "number": 2}
            ]
        }
    ],
    "loads": [1000.0]
}
```
2. Display trains information:
```python
print(train_station)
```

3. Manage wagons and locomotives within a train (inside the Train class):
```python
train = train_station.trains[0]  # Get a specific train
wagon = Wagon(**{"mass": int | float, "max_load_mass": int | float, "number": int})
locomotive = Locomotive(**{"mass": int | float, "towable_mass": int | float})
train.__add__(wagon)  # Add a wagon to the train
train.__add__(locomotive)  # Add a locomotive to the train
train.remove_wagon([wagon_number])  # Remove wagons from the train
train.remove_locomotive(locomotive_index)  # Remove a locomotive from the train
```

4. Distribute load:
```python
train_station.distribute_load()
```
