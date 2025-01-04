import random
import string


class URLShortener:
    def __init__(self):
        self.url_map = {}

    def generate_short_id(self, length=6):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def shorten_url(self, long_url):
        short_id = self.generate_short_id()
        while short_id in self.url_map:  # Ensure uniqueness
            short_id = self.generate_short_id()
        self.url_map[short_id] = long_url
        return f"http://localhost:8000/{short_id}"

    def resolve_url(self, short_id):
        return self.url_map.get(short_id)


if __name__ == "__main__":
    shortener = URLShortener()
    short_url = shortener.shorten_url(
        "https://chatgpt.com/c/67791027-d2c0-8004-b2b7-479d3c392647"
    )
    print("Short URL:", short_url)
    print("Original URL:", shortener.resolve_url(short_url))
