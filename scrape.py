import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to scrape content from a single URL
def scrape_url(url, visited_urls, file):
    # Check if URL is already visited
    if url in visited_urls:
        return
    
    print(f"Scraping: {url}")
    visited_urls.add(url)
    
    try:
        # Send HTTP GET request
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Write the page content to the file
    file.write(f"URL: {url}\n")
    file.write(f"Title: {soup.title.string if soup.title else 'No title'}\n")
    file.write(f"Content:\n{soup.get_text(separator=' ', strip=True)}\n\n")
    
    # Find all related links (anchor tags with href)
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)  # Resolve relative URLs
        if full_url.startswith(url):  # Only scrape links within the domain
            scrape_url(full_url, visited_urls, file)

# Main function to start scraping
def main():
    # The base URL to start scraping
    base_url = input("Enter the website URL to scrape: ").strip()
    
    # Output file to store the scraped content
    output_file = "arbor_home_data.txt"
    
    # Create or overwrite the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        visited_urls = set()  # To avoid revisiting URLs
        scrape_url(base_url, visited_urls, file)
    
    print(f"Scraping complete. Data saved in {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
