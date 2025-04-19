import os
import json
import requests
import re

class WikipediaScraper:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.page_title = "Sibu"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_page_content(self):
        """Fetch Wikipedia page content using the API"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'titles': self.page_title,
                'prop': 'extracts',
                'explaintext': True,
                'exsectionformat': 'wiki'
            }
            
            print("Fetching Wikipedia content...")
            response = requests.get(self.api_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            content = pages[page_id]['extract']
            
            print(f"Successfully fetched {len(content)} characters of content")
            return content
            
        except Exception as e:
            print(f"Error fetching Wikipedia content: {str(e)}")
            return None

    def extract_cuisine_section(self, content):
        """Extract cuisine section from content"""
        if not content:
            return ""
            
        # Try different section titles
        section_names = ["Cuisine", "Food", "Local cuisine", "Local food"]
        section_text = ""
        
        for section_name in section_names:
            # Create pattern to match section heading and content
            pattern = f"=+ {section_name} =+\n(.*?)(?=\n=+ [^=]|$)"
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                section_text = match.group(1).strip()
                if section_text:
                    print(f"Found content in section: {section_name}")
                    return section_text
                    
        return ""

    def clean_text(self, text):
        """Clean Wikipedia text"""
        if not text:
            return ""
        # Remove citation references
        text = re.sub(r'\[\d+\]', '', text)
        # Remove edit links
        text = re.sub(r'\[edit\]', '', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def save_data(self, data, filename):
        """Save scraped data to a JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        """Main method to run the scraper"""
        print("Starting Wikipedia scraper...")
        content = self.get_page_content()
        
        if content:
            # Extract cuisine section
            cuisine_content = self.extract_cuisine_section(content)
            
            if cuisine_content:
                # Clean the text
                cuisine_content = self.clean_text(cuisine_content)
                
                # Create data structure
                data = {
                    "cuisine": {
                        "category": "food",
                        "subcategory": "local_cuisine",
                        "content": cuisine_content
                    }
                }
                
                # Save raw data
                self.save_data(data, "wikipedia_data.json")
                print(f"Successfully extracted {len(cuisine_content)} characters of cuisine content")
                return data
            else:
                print("No cuisine content found")
        else:
            print("Failed to fetch Wikipedia content")
            
        return None
