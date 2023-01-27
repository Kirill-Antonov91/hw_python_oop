"""Программа Фитнес-трекер."""
from dataclasses import dataclass
from typing import List
from typing_extensions import ClassVar
from typing_extensions import Final


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TRAINING_MESSAGE = (
        "Тип тренировки: {0}; "
        "Длительность: {1:.3f} ч.; "
        "Дистанция: {2:.3f} км; "
        "Ср. скорость: {3:.3f} км/ч; "
        "Потрачено ккал: {4:.3f}."
    )

    def get_message(self) -> str:
        """Получить сообщение о тренировке."""
        return self.TRAINING_MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: Final[int] = 1000
    M_IN_H: Final[int] = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        """Параметры базового класса Training."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Определите количество затраченных калорий в дочерних классах."
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Метод для подсчета калорий в подклассе Running."""
        calories_running = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.M_IN_H)
        )
        return calories_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER_SPORTS_WALKING: ClassVar[float] = 0.035
    CALORIES_MEAN_SPEED_SPORTS_WALKING: ClassVar[float] = 0.029
    M_IN_SEC: Final[float] = 0.278
    SM_IN_M: Final[int] = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        """Параметры подкласса SportsWalking."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Метод для подсчета калорий в подклассе SportsWalking."""
        mean_speed_m_in_sec = (
            self.get_distance() / self.duration
        ) * self.M_IN_SEC
        height_in_m = self.height / self.SM_IN_M
        calories_sports_walking = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER_SPORTS_WALKING * self.weight
            + (mean_speed_m_in_sec**2 / height_in_m)
            * self.CALORIES_MEAN_SPEED_SPORTS_WALKING
            * self.weight
        ) * (self.duration * self.M_IN_H)
        return calories_sports_walking


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER_SWIMMING: ClassVar[float] = 1.1
    CALORIES_MEAN_SPEED_SWIMMING: ClassVar[int] = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        """Параметры подкласса Swimming."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Метод для подсчета средней скорости в подклассе Swimming."""
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Метод для подсчета калорий в подклассе Swimming."""
        calories_swim = (
            (
                self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_MULTIPLIER_SWIMMING
            )
            * self.CALORIES_MEAN_SPEED_SWIMMING
            * self.weight
            * self.duration
        )
        return calories_swim


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_training_cls_map = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    if workout_type in workout_type_training_cls_map:
        training_object = workout_type_training_cls_map[workout_type](*data)
        return training_object
    else:
        raise ValueError(f"Неизвестная тренировка {workout_type}")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
