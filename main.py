from src.api import AeroplanesAPI
from src.saver import JSONSaver
from src.user_interface import run_user_interface


def main() -> None:
    api = AeroplanesAPI()
    saver = JSONSaver("data/aeroplanes.json")

    run_user_interface(api, saver)


if __name__ == "__main__":
    main()
