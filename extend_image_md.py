from markdown.inlinepatterns import ImagePattern, IMAGE_LINK_RE
from markdown.extensions import Extension
import re

"""Extension allows you to specify the width and height of the image in markdown
    ![AgriInnovate Logo]({filename}/images/sms_controller/agri_innovate.jpg =400x600)
    ![AgriInnovate Logo]({filename}/images/sms_controller/agri_innovate.jpg =400x)
"""


class ImageExtensions(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['image_link'] = ImageWithSize(IMAGE_LINK_RE, md)


class Match(object):
    def __init__(self):
        self.data = dict()

    def set(self, key, value):
        self.data[key] = value

    def group(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

REGEX_MATCH = '.*(?:=(\d+)x(\d*)).*'
REGEX_REPL = '=(\d+)x(\d*)'


class ImageWithSize(ImagePattern):
    def handleMatch(self, m):
        regex_repl = re.compile(REGEX_REPL)
        src_string = m.group(9)
        width, height = "", ""

        if regex_repl.search(m.group(9)):
            regex_match = re.compile(REGEX_MATCH)
            width, height = regex_match.match(src_string).groups()
            src_string = regex_repl.sub("", src_string)

        match = Match()
        match.set(2, m.group(2))
        match.set(9, src_string)
        tree = super().handleMatch(match)
        if width:
            tree.set('width', width)
        if height:
            tree.set('height', height)
        return tree
