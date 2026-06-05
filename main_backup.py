import argparse

from src import orchestrator


def main():
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument(
        "--list-workers",
        action="store_true",
        help="Discover and list available workers",
    )
    args = parser.parse_args()

    if args.list_workers:
        orchestrator.load_workers()
        workers = orchestrator.list_workers()
        if not workers:
            print("No workers discovered")
            return
        for worker in workers:
            print(f"{worker['name']}: {worker['class']} " f"(category={worker['category']} version={worker['version']})")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
