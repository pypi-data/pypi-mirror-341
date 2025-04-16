from phystool.helper import greptex
from phystool.__about__ import about


def run_A() -> None:
    for f in greptex("ress", "/home/jdufour/travail/teaching/src-phys/physdb", silent=False):
        print(f)


def run_B() -> None:
    print(about())


def run_C() -> None:
    print(Path(__file__))
    print(Path(__file__).parents[2])


if __name__ == "__main__":
    run_B()
