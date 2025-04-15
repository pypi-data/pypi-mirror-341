import argparse
from typing import Any
from kwasa.functions.main import GitCloner


class KwasaCliService(GitCloner):
    def handler(self) -> None:
        parser = argparse.ArgumentParser(
            prog="kwasa",
            description="Kwasa CLI - Scaffold and manage your starter projects with ease.",
            epilog="""Examples:
            kwasa clone <directory>
            kwasa clone  --repo https://github.com/your/repo.git
            kwasa update""",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        subparsers = parser.add_subparsers(dest="command", required=True)
        clone_parser = subparsers.add_parser(
            "clone",
            help="Clone starter repo (https://github.com/dlion4/django-quick-starter.git)",
        )
        clone_parser.add_argument(
            "directory", help="Directory to clone into (use '.' for current directory)"
        )
        clone_parser.add_argument(
            "--repo", help="GitHub repository URL (default is the starter repo)"
        )

        subparsers.add_parser("update", help="Update current project (git fetch)")

        args = parser.parse_args()
        if args.command == "clone":
            self.clone(args.repo, args)
        elif args.command == "update":
            self.update(args)


def main() -> None:
    cli: Any = KwasaCliService()
    cli.handler()


if __name__ == "__main__":
    main()
