#initiator

#crawler
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
import time

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def crawl(self, url, depth=3):
        if depth == 0 or url in self.visited_urls:
            return

        try:
            # Add a delay to avoid hammering the server with requests
            time.sleep(1)

            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.index_page(url, soup)
                self.visited_urls.add(url)

                # Crawl each link on the page
                for link in soup.find_all('a', href=True):
                    new_url = link.get('href')
                    new_url = urljoin(url, new_url)  # Convert relative URLs to absolute
                    new_url = urldefrag(new_url)[0]  # Remove any URL fragments

                    # Ensure it's a valid URL and has not been visited before
                    if new_url.startswith('http') and new_url not in self.visited_urls:
                        print(f"Crawling: {new_url}")
                        self.crawl(new_url, depth - 1)  # Recurse with reduced depth

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")
        except Exception as e:
            print(f"Unexpected error crawling {url}: {e}")

    def index_page(self, url, soup):
        """Extracts and indexes the page title and first paragraph."""
        title = soup.title.string if soup.title else "No title"
        paragraph = soup.find('p').get_text() if soup.find('p') else "No paragraph found"

        # Print out indexed page details
        print(f"\nIndexing: {url}")
        print(f"Title: {title}")
        print(f"First Paragraph: {paragraph}\n")


# Main execution
if __name__ == "__main__":
    start_url = "https://example.com"  # Set the starting URL for crawling
    crawler = WebCrawler()
    crawler.crawl(start_url, depth=2)  # Depth can be adjusted for how deep you want to crawl
