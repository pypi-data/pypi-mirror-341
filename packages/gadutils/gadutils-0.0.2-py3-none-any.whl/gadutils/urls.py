import urllib.parse


def checkurl(path: str) -> bool:
    return urllib.parse.urlparse(path).scheme in ("http", "https")
