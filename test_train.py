import pytest
from unittest import TestCase
from freezegun import freeze_time
from datetime import datetime
from unittest.mock import patch
from train_station import TrainStation
from train import Wagon, Locomotive, InvalidTrainComponent


class TestTrainStation(TestCase):
    def test_with_filename(self):
        self.assertTrue(
            isinstance(TrainStation("FilesToLoad/trains.json"), TrainStation)
        )

    def test_without_filename(self):
        with pytest.raises(FileNotFoundError) as error_information:
            self.assertEqual(TrainStation(""), error_information)


class TestTrainAddMethod(TestCase):
    def setUp(cls) -> None:
        cls.train_station = TrainStation("FilesToLoad/trains.json")

    def test_when_wagon_with_correct_parametres(self):
        wagon = Wagon(**{"mass": 30, "max_load_mass": 130, "number": 0})
        self.train_station.trains[1] + wagon
        self.assertTrue(wagon in self.train_station.trains[1].wagons)

    def test_when_locomotive_with_correct_parametres(self):
        locomotive = Locomotive(**{"mass": 0.55, "towable_mass": 1000})
        self.train_station.trains[0] + locomotive
        self.assertTrue(locomotive in self.train_station.trains[0].locomotives)

    def test_when_there_is_same_number_wagon(self):
        wagon = Wagon(**{"mass": 30, "max_load_mass": 130, "number": 2})
        with pytest.raises(InvalidTrainComponent) as error_information:
            self.train_station.trains[1] + wagon
            self.assertEqual(self.train_station.trains[1], error_information)

    def test_when_parametres_are_invalid(self):
        with pytest.raises(InvalidTrainComponent) as error_information:
            self.train_station.trains[1] + 2
            self.assertEqual(self.train_station.trains[1], error_information)


@freeze_time("2023-10-09 12:00:00")
class TestTrainAttributeTime(TestCase):
    def test_train_create_time(self):
        train_station = TrainStation("FilesToLoad/trains.json")
        self.assertEqual(
            train_station.trains[0].created_at,
            datetime.now(),
        )

    @patch("train.Train")
    def test_train_update_time(self, TrainMock):
        train_mock = TrainMock.return_value
        train_mock.updated_at = datetime(2023, 10, 9, 12, 0, 0)
        self.assertEqual(
            train_mock.updated_at,
            datetime.now(),
        )


class TestDistributionMethod(TestCase):
    def test_distribution_method(self):
        self.assertFalse(
            TrainStation("FilesToLoad/only_locomative.json").distribute_load()
        )
        self.assertFalse(TrainStation("FilesToLoad/no_load.json").distribute_load())
        self.assertTrue(TrainStation("FilesToLoad/trains.json").distribute_load())
