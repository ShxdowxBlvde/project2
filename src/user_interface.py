import requests
from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.base_saver import BaseSaver


def get_top_n_by_altitude(
    aeroplanes: list[Aeroplane],
    n: int,
) -> list[Aeroplane]:
    """Возвращает N самолётов с наибольшей высотой полёта"""

    if n <= 0:
        raise ValueError("Количество самолётов должно быть больше нуля")

    planes_with_altitude = [
        plane for plane in aeroplanes if plane.baro_altitude is not None
    ]

    return sorted(
        planes_with_altitude,
        key=lambda plane: plane.baro_altitude,
        reverse=True,
    )[:n]


def get_by_origin_country(
    aeroplanes: list[Aeroplane],
    country: str,
) -> list[Aeroplane]:
    """Возвращает самолёты по стране происхождения"""

    if not country.strip():
        raise ValueError("Название страны не может быть пустым")

    return [
        plane
        for plane in aeroplanes
        if plane.origin_country.casefold() == country.strip().casefold()
    ]


def display_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит информацию о самолётах"""

    if not aeroplanes:
        print("Самолёты не найдены.")
        return

    for index, plane in enumerate(aeroplanes, start=1):
        altitude = (
            f"{plane.baro_altitude} м"
            if plane.baro_altitude is not None
            else "Нет данных"
        )

        velocity = (
            f"{plane.velocity} м/с" if plane.velocity is not None else "Нет данных"
        )

        print(f"\nСамолёт №{index}")
        print(f"ICAO24: {plane.icao24}")
        print(f"Позывной: {plane.callsign or 'Нет данных'}")
        print(f"Страна происхождения: {plane.origin_country}")
        print(f"Высота: {altitude}")
        print(f"Скорость: {velocity}")
        print(f"Вертикальная скорость: {plane.vertical_rate}")


def run_user_interface(
    api: AeroplanesAPI,
    saver: BaseSaver,
) -> None:
    """Запускает консольный интерфейс программы"""

    while True:
        country = input(
            "\nВведите название страны для поиска самолётов " "или 0 для выхода: "
        ).strip()

        if country == "0":
            print("Программа завершена.")
            break

        if not country:
            print("Название страны не может быть пустым.")
            continue

        try:
            aeroplanes = api.get_aeroplanes(country)
            saver.add_aeroplanes(aeroplanes)
        except (ValueError, IndexError) as error:
            print(f"Ошибка получения данных: {error}")
            continue
        except requests.RequestException as error:
            print(f"Ошибка HTTP-запроса: {error}")
            continue

        print(f"\nНайдено самолётов над {country}: {len(aeroplanes)}")

        while True:
            print("\nВыберите действие:")
            print("1. Показать топ N самолётов по высоте")
            print("2. Найти самолёты по стране происхождения")
            print("3. Выполнить новый поиск по другой стране")
            print("0. Выйти из программы")

            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                try:
                    n = int(input("Введите количество самолётов: "))
                    result = get_top_n_by_altitude(aeroplanes, n)
                    display_aeroplanes(result)
                except ValueError as error:
                    print(f"Некорректное значение: {error}")

            elif choice == "2":
                origin_country = input("Введите страну происхождения самолётов: ")

                try:
                    result = get_by_origin_country(
                        aeroplanes,
                        origin_country,
                    )
                    display_aeroplanes(result)
                except ValueError as error:
                    print(error)

            elif choice == "3":
                break

            elif choice == "0":
                print("Программа завершена")
                return

            else:
                print("Неизвестная команда. Попробуйте ещё раз")
