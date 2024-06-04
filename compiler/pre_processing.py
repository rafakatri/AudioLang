import re

class PrePro:

    def filter(source):
        comments = re.sub(r"(?<!\d|-)--.*$", "", source, flags=re.MULTILINE)
        return comments