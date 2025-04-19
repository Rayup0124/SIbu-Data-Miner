import os
import json
import re
from datetime import datetime
from scrapers.wikipedia_scraper import WikipediaScraper

class SibuFoodMiner:
    def __init__(self):
        self.output_dir = 'datasets'
        self.raw_data_dir = 'raw_data'
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in [self.output_dir, self.raw_data_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def extract_dishes(self, text):
        """Extract individual dishes from the text"""
        # Remove the introduction part
        start_idx = text.find("Common dishes that can be found")
        if start_idx != -1:
            text = text[start_idx:]
        
        # Split text into dishes
        dishes = []
        current_dish = ""
        lines = text.split('. ')
        
        for line in lines:
            # Check if this line starts a new dish
            if ' — ' in line or any(line.startswith(name) for name in ["Kampua", "Dian Mian", "Kompia", "Bian Nyuk", "Bazhen", "Sarawak", "Tebaloi", "Kek Lapis", "Manok", "Terung", "Empurau", "Rojak", "You Zhar"]):
                if current_dish:
                    dishes.append(current_dish.strip())
                current_dish = line
            else:
                current_dish += ". " + line
        
        if current_dish:
            dishes.append(current_dish.strip())
            
        return dishes
                
    def process_data(self, raw_data):
        """Process the raw food data into structured format"""
        structured_data = []
        
        if raw_data.get('cuisine'):
            content = raw_data['cuisine'].get('content', '')
            dishes = self.extract_dishes(content)
            
            for dish in dishes:
                # Skip if the dish text is too short
                if len(dish) < 10:
                    continue
                    
                try:
                    # Handle dishes with clear name markers
                    if ' — ' in dish:
                        name_part, description = dish.split(' — ', 1)
                    else:
                        # Try to split at the first sentence
                        parts = dish.split('. ', 1)
                        if len(parts) > 1:
                            name_part, description = parts
                        else:
                            name_part = parts[0]
                            description = ""
                    
                    # Extract main name and Chinese/alternative names
                    if '(' in name_part and ')' in name_part:
                        main_name = name_part[:name_part.find('(')].strip()
                        alt_names = name_part[name_part.find('(')+1:name_part.find(')')].strip()
                        
                        # Process alternative names
                        chinese_name = ""
                        if 'known as' in alt_names:
                            alt_names = alt_names.split('known as')[1].strip()
                        
                        # Extract Chinese characters
                        chinese_chars = re.findall(r'[一-龥]+', alt_names)
                        if chinese_chars:
                            chinese_name = ''.join(chinese_chars)
                        elif '油炸' in alt_names:  # Special case for You Zhar Gui
                            chinese_name = '油炸桧'
                    else:
                        main_name = name_part.strip()
                        chinese_name = ""
                    
                    # Clean up the main name
                    if main_name.startswith('also known as'):
                        main_name = main_name.replace('also known as', '').strip()
                        
                    # Remove trailing comma and extra spaces
                    main_name = main_name.rstrip(',').strip()
                    
                    # Only add dishes with valid names
                    if main_name and not main_name.lower().startswith(('is a', 'are', 'can be', 'one of', 'many', 'common')):
                        dish_data = {
                            'name': main_name,
                            'chinese_name': chinese_name,
                            'description': description.strip(),
                            'type': 'local_cuisine'
                        }
                        structured_data.append(dish_data)
                
                except Exception as e:
                    print(f"Error processing dish: {str(e)}")
                    continue
        
        return structured_data
        
    def save_data(self, data):
        """Save processed data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_path = os.path.join(self.output_dir, f'sibu_food_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"\nData saved to: {json_path}")
        
        # Print a summary of the dishes
        print("\nCollected dishes:")
        for dish in data:
            name_str = dish['name']
            if dish['chinese_name']:
                name_str += f" ({dish['chinese_name']})"
            print(f"- {name_str}")
            
        print(f"\nTotal dishes collected: {len(data)}")
        
    def run(self):
        """Main execution method"""
        print("Starting Sibu Food Data Mining Process...")
        
        # Run Wikipedia scraper
        scraper = WikipediaScraper(self.raw_data_dir)
        raw_data = scraper.run()
        
        # Process data
        if raw_data:
            processed_data = self.process_data(raw_data)
            
            # Save processed data
            self.save_data(processed_data)
            print("Data mining and processing completed!")
        else:
            print("No data was collected!")

if __name__ == "__main__":
    miner = SibuFoodMiner()
    miner.run()
