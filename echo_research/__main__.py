import argparse

from .pipeline import run


def main() -> None:
    p = argparse.ArgumentParser(prog="echo_research")
    p.add_argument("topic")
    p.add_argument("--top", type=int, default=6)
    p.add_argument("--out", help="write report to this file")
    a = p.parse_args()
    md = run(a.topic, top=a.top)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
    else:
        print(md)


if __name__ == "__main__":
    main()
