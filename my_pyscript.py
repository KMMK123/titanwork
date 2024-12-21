import requests
import json
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import codecs

def scrape_stackoverflow_titles():
    url = "https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize=50"
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Error: Status code {}".format(response.status_code))
            return None
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all question titles
        titles = soup.find_all('h3', class_='s-post-summary--content-title')
        
        # Extract question titles and links
        questions = []
        for title in titles:
            link = title.find('a', class_='s-link')
            if link:
                questions.append({
                    'title': link.text.strip(),
                    'url': 'https://stackoverflow.com{}'.format(link['href'])
                })
        
        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = 'stackoverflow_questions_{}.csv'.format(timestamp)
        
        # Python 2 compatible file handling
        with open(filename, 'wb') as csvfile:
            fieldnames = ['title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for question in questions:
                # Encode strings for Python 2
                row = {
                    'title': question['title'].encode('utf-8')
                    
                }
                writer.writerow(row)
            
        print("Successfully scraped {} questions and saved to {}".format(len(questions), filename))
        return questions
        
    except requests.exceptions.RequestException as e:
        print("Error making request: {}".format(e))
        return None
    except Exception as e:
        print("An error occurred: {}".format(e))
        return None

if __name__ == "__main__":
    scrape_stackoverflow_titles()
