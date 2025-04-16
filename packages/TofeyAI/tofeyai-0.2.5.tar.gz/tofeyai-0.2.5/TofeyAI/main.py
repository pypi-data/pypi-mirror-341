import requests

class TofeyAI:
    def __init__(self):
        self.url = "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/Hacker.php"
        self.imager = "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/imger.php?img="

        """Generate response `str`
        Args:
            prompt (str): Prompt to be sent
        Returns:
            str: Response generated
        """
    def prompt(self, request: str ):
        json_data = {
            "text": request,
            "api_key": "PyCodz"         # You Can Get More By Contact Me .
        }
        return requests.post(
            url=self.url, json=json_data
                                    ).text

    def generate_image(self, prompt: str):
        img = requests.get(self.imager + prompt)
        with open(f"{prompt}.png", "wb") as f:
            f.write(img.content)

    def help(self) -> str:
        return """
    Usage: HackerGpt -[OPTIONS] "[PROMPT]"

    Options:
      -p, --prompt        Start Chatting.
      -img, --imager      Generate image by prompt.
      -h, --help          Show this message and exit.
    """

    def version(self):
        return (
        f"MyAi\n"
        f"Version: 0.8.0\n"
        "Author : PyCodz\n"
    )

    @staticmethod
    def chat(prompt: str) -> str:
        return TofeyAI().prompt(prompt)


