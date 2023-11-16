import json
from train import Train


class TrainStation:
    """A class representing a train station and storing information about all trains.
    Attributes:
        filename (str): The JSON file containing data about all trains and their loads.
        trains (list[Train]): A list of Train objects representing the trains at the station.
        unused_wagons (list[Wagon]): A list to store unused wagon objects.
        unused_locomotives (list[Locomative]): A list to store unused locomotive objects.
        load (None or float): The total load to be distributed among trains."""

    unused_wagons: list = []
    unused_locomotives: list = []
    load = None

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.trains = [
            Train(train["locomotives"], train["wagons"])
            for train in self.get_loads_and_trains_data()
        ]
        self.remove_trains_without_locomotives()
        self.sort_trains_by_wagons_mass()

    def get_loads_and_trains_data(self):
        """Gets trains and loads data and checks if there is no train without locomative."""
        trains_data = self.load_from_file(self.filename)
        self.load = sum(trains_data["loads"])
        return trains_data["trains"]

    @staticmethod
    def load_from_file(filename: str) -> list[dict]:
        """Extracts data from a JSON file."""
        if filename:
            with open(filename) as file:
                return json.load(file)
        raise FileNotFoundError("There is no file")

    def remove_trains_without_locomotives(self):
        """Remove trains without locomotives and collect their wagons as unused."""
        for train in self.trains:
            if len(train.locomotives) == 0:
                self.unused_wagons.extend(train.wagons)
                self.trains.remove(train)

    def sort_trains_by_wagons_mass(self):
        return self.trains.sort(
            key=lambda train: train.all_wagons_max_load_mass(), reverse=True
        )

    def distribute_load(self) -> bool:
        """Distributes the load among trains, removing unused trains or wagons if necessary."""
        if self.load == 0:
            print("There is no load")
            return False
        self.remove_trains_without_locomotives()
        used_trains = [
            train for train in self.trains if self.add_load_to_train_wagons(train)
        ]
        self.remove_unused_trains_and_locomotives(used_trains, self.trains)
        self.trains = used_trains
        if self.load == 0 and used_trains:
            return True

        print(f"There isn't enough wagons to distribute left load: {self.load}")
        return False

    def add_load_to_train_wagons(self, train: Train) -> bool:
        """Distributes the load to wagons in the train
        and assigns it to the 'load_mass' attribute if there are wagons in the train.
        Args:
        train (Train): The train to distribute the load to."""

        if self.load and (train_max_load_mass := train.all_wagons_max_load_mass()):
            if train_max_load_mass <= self.load:
                self.load -= train_max_load_mass
                for wagon in train.wagons:
                    wagon.load_mass = wagon.max_load_mass
            else:
                self.unused_wagons += train.remove_unused_wagons(self.load)
                self.load = 0
            return True

        return False

    @classmethod
    def remove_unused_trains_and_locomotives(cls, used_trains: list, trains: list):
        """Removes unused trains and adds their locomotives to the unused_locomotives list.
        Parameters:
            used_trains (list): A list of loaded trains."""
        unused_trains = filter(
            lambda unused_train: unused_train not in used_trains, trains
        )
        cls.unused_locomotives.extend(
            locomotive for train in unused_trains for locomotive in train.locomotives
        )

    def __repr__(self) -> str:
        trains_info = ""
        for train in self.trains:
            trains_info = (
                f"Train info: locomotives {len(train.locomotives)},"
                + f" wagons: {len(train.wagons)}, operatable: {bool(train)}\n"
            )
        return trains_info
