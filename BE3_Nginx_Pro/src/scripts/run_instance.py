#!/usr/bin/env python3
import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Store API instance without Flask reloader")
    parser.add_argument("--api-src", required=True, help="Path to BE2 API src directory")
    parser.add_argument("--port", type=int, required=True, help="Port to bind")
    parser.add_argument("--config", default="production", help="Config profile for create_app")
    args = parser.parse_args()

    sys.path.insert(0, os.path.abspath(args.api_src))

    from app import create_app  # pylint: disable=import-error

    app = create_app(args.config)
    app.run(host="0.0.0.0", port=args.port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
