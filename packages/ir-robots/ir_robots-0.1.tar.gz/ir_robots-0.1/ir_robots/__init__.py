#initiator
#handle challenge such as robot.txt
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def crawl(self, url, depth=3, delay=1):
        if depth == 0 or url in self.visited_urls:
            return

        try:
            # Check robots.txt
            if not self.is_allowed_by_robots(url):
                print(f"Skipping {url} due to robots.txt rules")
                return

            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.index_page(url, soup)
                self.visited_urls.add(url)

                for link in soup.find_all('a', href=True):
                    new_url = link.get('href')
                    if new_url.startswith('http'):
                        time.sleep(delay)  # Delay between requests
                        self.crawl(new_url, depth - 1, delay)
            else:
                print(f"Failed to fetch {url}: Status code {response.status_code}")

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def is_allowed_by_robots(self, url):
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                robots_txt = response.text
                if "User-agent: *" in robots_txt:
                    start_index = robots_txt.find("User-agent: *")
                    end_index = robots_txt.find("User-agent:", start_index + 1)

                    if end_index == -1:
                        end_index = len(robots_txt)

                    relevant_section = robots_txt[start_index:end_index]

                    if "Disallow: /" in relevant_section:
                        return False
            return True
        except requests.RequestException:
            return True  # If robots.txt is unreachable, assume allowed

    def index_page(self, url, soup):
        title = soup.title.string if soup.title else "No title"
        paragraph = soup.find('p').get_text() if soup.find('p') else "No paragraph found"
        print(f"\nIndexing: {url}")
        print(f"Title: {title}")
        print(f"First Paragraph: {paragraph}")
        print("-------------------------------------------------")

# Example usage
if __name__ == "__main__":
    crawler = WebCrawler()
    crawler.crawl("https://www.facebook.com")
