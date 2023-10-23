import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class HTMLParser:
    """
    HTML parser using BeautifulSoup to return information about fetched pages.

    When constructing, provide a base URL that will be used to resolve relative
    links for <a> and <img> tags.
    """

    def __init__(self, html: str, base_url: str, assets_path: str) -> None:
        self.parsed = BeautifulSoup(html, "html.parser")
        self.base_url = base_url
        self.assets_path = assets_path

    def get_links(self) -> list[str]:
        """
        Return a list of link URLs in the HTML. These are the `href` attributes
        of all `<a>` tags. Relative URLs are resolved using the base URL.
        """
        urls = [link["href"]
                for link in self.parsed.find_all("a", attrs={"href": True})]
        return [urljoin(self.base_url, url) for url in urls]

    def get_images(self) -> list[str]:
        """
        Return a list of image URLs in the HTML. These are the `src` attributes
        of all `<img>` tags. Relative URLs are resolved using the base URL.
        """
        images = [image["src"]
                  for image in self.parsed.find_all("img", attrs={"src": True})]
        return [urljoin(self.base_url, image) for image in images]

    def replace_image_urls(self) -> str:
        """
        Return a new HTML document with all the image `src` attributes replaced
        with the new image URLs.
        """
        for image in self.parsed.find_all("img"):
            # Build a relative path to the downloaded image
            local_path = os.path.join(
                self.assets_path, image["src"].split("/")[-1])
            image["src"] = local_path
        return self.parsed.prettify()
