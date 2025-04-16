import argparse
from .main import HackerGpt
import asyncio



async def main():
    parser = argparse.ArgumentParser(description="HackerGpt Library" , add_help=False )
    parser.add_argument("-p", "--prompt", type=str, help="Your prompt to HackerGpt")
    parser.add_argument("-img", "--imager", type=str, help="Your prompt to Generation images")
    parser.add_argument("-h", "--help", action="store_true", help="Show custom help Message .")
    parser.add_argument("-v", "--version", action="store_true", help="Show Version Of Libarary .")
    args = parser.parse_args()
    gpt = HackerGpt()

    if args.prompt:
        print(gpt.prompt(args.prompt))

    if args.imager:
        gpt.generate_image(args.imager)
        print(f"Image saved as: {args.imager}.png")

    if args.help:
        print(gpt.help())

    if args.version:
        print(gpt.version())


if __name__ == "__main__":
    asyncio.run(main())


def main_sync():
    import asyncio
    asyncio.run(main())

