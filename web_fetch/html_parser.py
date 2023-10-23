from bs4 import BeautifulSoup

class HTMLParser:
    """
    HTML parser using BeautifulSoup to return information about fetched pages
    """
    def __init__(self, html: str) -> None:
        self.parsed = BeautifulSoup(html, "html.parser")

    def get_links(self) -> list[str]:
        """
        Return a list of links in the HTML. These are the `href` attributes of
        all `<a>` tags.
        """
        return [link["href"] for link in self.parsed.find_all("a")]
    
    def get_images(self) -> list[str]:
        """
        Return a list of images in the HTML. These are the `src` attributes of
        all `<img>` tags.
        """
        return [image["src"] for image in self.parsed.find_all("img")]