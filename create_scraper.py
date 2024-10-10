import os
import requests
from bs4 import BeautifulSoup

def detect_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tags = {
        'articles': len(soup.find_all('article')),
        'divs': len(soup.find_all('div')),
        'headers': len(soup.find_all(['h1', 'h2', 'h3'])),
        'paragraphs': len(soup.find_all('p'))
    }
    return tags

def create_scraper_for_website(website_name, url_pattern):
    # Create a new directory for the website
    if not os.path.exists(website_name):
        os.makedirs(website_name)

    # Detect common tags on the website
    tags = detect_tags(f"https://{url_pattern}")
    tag_info = ', '.join([f"{tag}: {count}" for tag, count in tags.items()])

    # Write a new scraper file with detected tags
    with open(f"{website_name}/scraper.py", "w") as f:
        f.write(f"""
import requests
from bs4 import BeautifulSoup

def scrape_{website_name}(url):
    if '{url_pattern}' not in url:
        return 'Unsupported URL pattern.'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example scraping logic based on detected tags: {tag_info}
    content = [tag.text for tag in soup.find_all('p')]  # Adjust as needed
    return content
""")

if __name__ == "__main__":
    # Example: Create a scraper for a new website
    create_scraper_for_website("www.cyberblogindia.in/blog", "cyberblogindia.in")
