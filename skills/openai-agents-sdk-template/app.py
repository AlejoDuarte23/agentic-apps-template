import argparse

from dotenv import load_dotenv

from agent.runner import run_once


load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the OpenAI Agents SDK template.")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Say hello and explain what this template does in one sentence.",
    )
    args = parser.parse_args()
    print(run_once(args.prompt))


if __name__ == "__main__":
    main()
