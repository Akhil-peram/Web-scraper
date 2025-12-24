import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        data = {
            "title": soup.title.string.strip()
            if soup.title and soup.title.string
            else "No title",
            "headings": {
                "h1": [h.get_text().strip() for h in soup.find_all("h1")],
                "h2": [h.get_text().strip() for h in soup.find_all("h2")],
                "h3": [h.get_text().strip() for h in soup.find_all("h3")],
            },
            "links": [],
        }

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href:
                full_url = urljoin(url, href)
                link_text = link.get_text().strip()
                if link_text:
                    data["links"].append({"text": link_text, "url": full_url})

        return data

    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"Parsing failed: {e}"}


def main():
    url = input("Enter URL to scrape: ").strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"Scraping {url}...")
    result = scrape_page(url)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nTitle: {result['title']}")
        print(f"\nHeadings:")
        for level, headings in result["headings"].items():
            if headings:
                print(f"  {level.upper()}:")
                for heading in headings[:5]:
                    print(f"    - {heading}")
                if len(headings) > 5:
                    print(f"    ... and {len(headings) - 5} more")

        print(f"\nLinks (first 10):")
        for link in result["links"][:10]:
            print(f"  - {link['text']} -> {link['url']}")
        if len(result["links"]) > 10:
            print(f"  ... and {len(result['links']) - 10} more links")


if __name__ == "__main__":
    main()
