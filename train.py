import uuid
from datetime import datetime


class InvalidTrainComponent(Exception):
    """Error inherited from the Exception class, raised when a wagon is invalid."""

    pass


class Locomotive:
    """
    A class representing a locomotive and storing information about a train's locomotives.
    Attributes:
        mass (int or float): The mass of the locomotive.
        towable_mass (int or float): The maximum drag mass the locomotive can handle."""

    def __init__(self, mass: float, towable_mass: float) -> None:
        self.mass = mass
        self.towable_mass = towable_mass

    def __json__(self) -> dict:
        return self.__dict__


class Wagon:
    """
    A class representing a wagon and storing information about a train's wagons.
    Attributes:
        mass (int or float): The mass of the wagon.
        load_mass (int or float): The mass of the current load.
        max_load_mass (int or float): The maximum load mass it can have.
        number (int): The ID of the wagon."""

    def __init__(
        self,
        mass: float,
        max_load_mass: float,
        number: int,
        load_mass: float = 0.0,
    ) -> None:
        self.mass = mass
        self.max_load_mass = max_load_mass
        self.load_mass = load_mass
        self.number = number

    def wagon_mass(self) -> float:
        return self.load_mass + self.mass

    def __bool__(self) -> bool:
        if self.load_mass > self.max_load_mass:
            return False
        return True

    def __json__(self) -> dict:
        return self.__dict__


class Train:
    """
    A class representing a train and storing information about a current trains in station.
    Attributes:
        locomotives (list[Locomotive]): The list of all train's locomotives.
        wagons (list[Wagon] | None): The list of all train's wagons (optional)."""

    def __init__(self, locomotives: list, wagons: list) -> None:
        self.locomotives = [
            Locomotive(locomotive["mass"], locomotive["towable_mass"])
            for locomotive in locomotives
        ]
        self.wagons = [
            Wagon(
                wagon["mass"],
                wagon["max_load_mass"],
                wagon["number"],
            )
            for wagon in wagons
        ]
        self.train_id = uuid.uuid4()
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime | None = None

    def all_wagons_max_load_mass(self) -> float:
        """Calculates train's wagons maximum load mass"""
        return sum(wagon.max_load_mass for wagon in self.wagons)

    def remove_locomotive(self, locomotive_index: int) -> bool:
        """Remove locomotive from specific train based on their list index.
        Args:
        locomotive_index (int): Locomotive index specifying witch locomotive to remove.
        """
        if locomotive_index <= len(self.locomotives):
            self.locomotives.pop(locomotive_index)
            return True
        return False

    def remove_wagon(self, wagons_number: list[int]) -> None:
        """Remove wagon from specific train based on their numbers.
        Args:
        wagon_numbers (list[int]): List of wagon specifying witch wagon to remove.
        """
        for wagon in self.wagons:
            if wagon.number in wagons_number:
                self.wagons.remove(wagon)
                self.updated_at = datetime.now()

    def remove_unused_wagons(self, left_load: float) -> list:
        """Removes empty wagons from the train and returns a list of unused wagons.
        Attributes:
            left_load (int or float): The remaining load to distribute among wagons.
        """
        used_wagons = []
        self.wagons.sort(key=lambda wagon: wagon.max_load_mass, reverse=True)
        for wagon in self.wagons:
            if left_load == 0:
                break
            if wagon.max_load_mass < left_load:
                wagon.load_mass = wagon.max_load_mass
                left_load -= wagon.max_load_mass
            else:
                wagon.load_mass = left_load
                left_load = 0
            used_wagons.append(wagon)
        unused_wagons = list(
            filter(lambda unused_wagon: unused_wagon not in used_wagons, self.wagons)
        )
        self.wagons = used_wagons
        self.updated_at = datetime.now()
        return unused_wagons

    def __add__(self, add_train_component: Wagon | Locomotive) -> "Wagon | Locomotive":
        """Dunder add method to add train components into a train.
        Args:
            add_train_component (Wagon or Locomotive): A train component object to be added to the train.
        """
        if isinstance(
            add_train_component, Wagon
        ) and add_train_component.number not in [wagon.number for wagon in self.wagons]:
            self.wagons += [add_train_component]
        elif isinstance(add_train_component, Locomotive):
            self.locomotives += [add_train_component]
        else:
            raise InvalidTrainComponent(
                "Invalid train component or wagon number is already in train."
            )

        self.updated_at = datetime.now()

    def __bool__(self) -> bool:
        total_train_towable_mass = sum(
            locomotive.towable_mass for locomotive in self.locomotives
        )
        total_mass_to_tow = sum(wagon.wagon_mass() for wagon in self.wagons)
        if total_train_towable_mass >= total_mass_to_tow:
            return True
        return False

    def __json__(self) -> dict:
        return {
            "wagons": [wagon.__json__() for wagon in self.wagons],
            "locomotives": [locomotive.__json__() for locomotive in self.locomotives],
        }
