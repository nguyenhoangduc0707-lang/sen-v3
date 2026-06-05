import argparse
import os


def scaffold_worker(name, category):
    # T?o folder category n?u chua cÃ³
    folder = os.path.join("fullwork", category)
    os.makedirs(folder, exist_ok=True)

    # Ãu?ng d?n file
    file_path = os.path.join(folder, f"{name.lower()}.py")

    # Template n?i dung file
    template = f"""from src.base_worker import BaseWorker
from src.registry import register_worker

@register_worker("{category}.{name.lower()}")
class {name.capitalize()}Worker(BaseWorker):
    def __init__(self):
        super().__init__("{category}.{name.lower()}")

    def run(self, **kwargs):
        # TODO: Implement logic t?i dÃ¢y
        return {{"status": "success", "message": "Worker {name} works!"}}
"""

    with open(file_path, "w") as f:
        f.write(template)
    print(f"? ÃÃ£ t?o worker m?i t?i: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEN V3 Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # L?nh t?o worker
    scaffold = subparsers.add_parser("scaffold")
    scaffold.add_argument("--name", required=True, help="TÃªn worker (vÃ­ d?: downloader)")
    scaffold.add_argument("--category", required=True, help="TÃªn category (vÃ­ d?: tiktok)")

    args = parser.parse_args()

    if args.command == "scaffold":
        scaffold_worker(args.name, args.category)
