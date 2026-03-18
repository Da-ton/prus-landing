from html.parser import HTMLParser

class DOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.in_main_div = False
        self.main_div_depth = -1
        
    def handle_starttag(self, tag, attrs):
        if tag in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            return
            
        cls = next((v for k, v in attrs if k == "class"), "")
        id_attr = next((v for k, v in attrs if k == "id"), "")
        
        if tag == "div" and "mx-auto max-w-[1200px]" in cls and not self.in_main_div:
            self.in_main_div = True
            self.main_div_depth = self.depth
            print(f"{'  '*self.depth}<{tag} class='{cls}'>")
            self.depth += 1
            return
            
        if self.in_main_div:
            if self.depth == self.main_div_depth + 1:
                # Direct child of main div
                print(f"{'  '*self.depth}<{tag} id='{id_attr}' class='{cls}'>")
                
        self.depth += 1

    def handle_endtag(self, tag):
        if tag in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            return
        self.depth -= 1
        if self.in_main_div and self.depth == self.main_div_depth:
            self.in_main_div = False
            print(f"{'  '*self.depth}</{tag}> (main div closed)")

with open("index.html") as f:
    DOMParser().feed(f.read())
