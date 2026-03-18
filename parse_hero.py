from html.parser import HTMLParser

class HeroParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.inside_hero = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            # Just print the first few chars of class to identify
            cls = next((v for k, v in attrs if k == "class"), "")
            if "py-16" in cls and "grid" in cls:
                self.inside_hero = True
                self.depth = 1
                return
            if self.inside_hero:
                self.depth += 1

    def handle_endtag(self, tag):
        if self.inside_hero and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                print(f"Hero grid closed exactly at line {self.getpos()[0]}")
                self.inside_hero = False

with open("index.html") as f:
    HeroParser().feed(f.read())
