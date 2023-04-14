class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: int,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        part = (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
        calories = (part * self.weight / self.M_IN_KM * self.duration
                    * self.MIN_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035
    K_2 = 0.029
    M_IN_S = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        part_1 = self.K_1 * self.weight
        part_2 = ((self.get_mean_speed() * self.M_IN_S) ** 2
                  / (self.height / self.CM_IN_M))
        return ((part_1 + part_2 * self.K_2 * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K_3 = 1.1
    K_4 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        part_4 = (self.get_mean_speed() + self.K_3)
        calories = part_4 * self.K_4 * self.weight * self.duration
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_type_of_training = {'SWM': Swimming,
                             'RUN': Running,
                             'WLK': SportsWalking}
    workout_type = dict_type_of_training[workout_type](*data)
    return workout_type


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
