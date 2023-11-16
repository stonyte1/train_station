import json
from train_station import TrainStation
from train import Wagon, Locomotive


def save_train_station_data(train_station: TrainStation) -> None:
    train_station.sort_trains_by_wagons_mass()
    train_sation_data = {
        "trains": [train.__json__() for train in train_station.trains],
        "unused_wagons": [wagon.__json__() for wagon in train_station.unused_wagons],
        "unused_locomotives": [
            locomotive.__json__() for locomotive in train_station.unused_locomotives
        ],
    }
    with open("train_station.json", "w") as file:
        json.dump(train_sation_data, file, indent=4)


if __name__ == "__main__":
    train_station = TrainStation("FilesToLoad/trains.json")
    print(train_station)

    wagon = Wagon(**{"mass": 30, "max_load_mass": 130, "number": 15})
    wagon1 = Wagon(**{"mass": 30, "max_load_mass": 230, "number": 100})
    wagon2 = Wagon(**{"mass": 30, "max_load_mass": 300, "number": 22})
    train_station.trains[1].__add__(wagon)
    train_station.trains[0].__add__(wagon1)
    train_station.trains[0].__add__(wagon2)
    train_station.trains[0].remove_wagon([7, 6])

    locomotive = Locomotive(**{"mass": 0.55, "towable_mass": 1000})
    train_station.trains[0].__add__(locomotive)
    train_station.trains[0].remove_locomotive(0)

    train_station.distribute_load()

    print(train_station)

    # save_train_station_data(train_station)
