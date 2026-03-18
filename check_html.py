from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.line_stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            return
        self.stack.append(tag)
        self.line_stack.append(self.getpos()[0])

    def handle_endtag(self, tag):
        if len(self.stack) == 0:
            print(f"Error: Found closing tag </{tag}> at line {self.getpos()[0]} but stack is empty")
            return
        last_tag = self.stack[-1]
        line = self.line_stack[-1]
        if last_tag != tag:
            print(f"Error: Mismatched tag at line {self.getpos()[0]}. Expected </{last_tag}> (opened at line {line}), got </{tag}>")
            # Pop until we find it, or ignore
            # Let's just pop the last one
            self.stack.pop()
            self.line_stack.pop()
        else:
            self.stack.pop()
            self.line_stack.pop()

with open('index.html', 'r', encoding='utf-8') as f:
    parser = MyHTMLParser()
    parser.feed(f.read())
    
if len(parser.stack) > 0:
    print(f"Unclosed tags remaining: {parser.stack}")
    print(f"Opened at lines: {parser.line_stack}")
else:
    print("All tags matched perfectly!")
