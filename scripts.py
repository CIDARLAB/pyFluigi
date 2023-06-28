import datetime
import subprocess


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(["pytest", "-vv"], check=True)


def benchmark():
    """
    Run all the benchmarks
    """
    # "%Y-%m-%d_%H-%M-%S"
    now = datetime.datetime.now().strftime(r"%d-%m-%Y-%H:%M:%S")
    f = open(f"./scripts/par-log_{now}.log", "w")
    subprocess.call(
        ["sh", "par.sh"],
        cwd="./scripts",
        stderr=f,
        stdout=f,
    )
