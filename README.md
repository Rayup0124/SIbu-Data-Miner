🍜 Sibu Food Data Miner

*Sibu Food Data Miner* is a web scraper built to collect local food information from *Sibu, Sarawak*. This tool extracts structured data from Wikipedia and organizes it into a dataset suitable for machine learning applications.

---

📌 Features

- 🔍 Automatically scrapes food-related content about Sibu from Wikipedia
- 🧾 Extracts dish names (in English and Chinese) with detailed descriptions
- 📦 Outputs structured data in JSON format
- 🤖 Ideal for use in training AI or building food recommendation systems

---

⚙ Installation Steps

1. Create a virtual environment

Windows:
bash
python -m venv venv
venv\Scripts\activate


macOS / Linux:
bash
python3 -m venv venv
source venv/bin/activate


---

2. Install dependencies
bash
pip install -r requirements.txt


---

3. Run the scraper
bash
python main.py
```

---

📂 Output Files

After running the program, you will get:

- datasets/sibu_food_[timestamp].json  
  Structured food data (name, Chinese name, and description)

- raw_data/wikipedia_data.json  
  Raw scraped Wikipedia content for reference

---

📊 Use Cases

The generated dataset can be used for:
- Training machine learning models to understand Sibu cuisine
- Building a local food recommendation engine
- Developing a food guide app for Sibu

---

🖥 Requirements

- Python 3.6+
- Internet connection (to access Wikipedia)

---

🍴 Enjoy mining Sibu's delicious culture — one dish at a time!
```

