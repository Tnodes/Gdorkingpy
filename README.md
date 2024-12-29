# Google Search Scraper

A Python-based tool for scraping Google search results by predefined categories or custom searches. The tool filters out social media and unwanted domains, saving clean URLs for further processing.

## Features

- Pre-defined search categories:
  - Web3
  - AI
  - Politics
  - Climate
  - Quantum
  - Nuclear
  - Pandemic
- Custom search queries
- Proxy support for avoiding rate limits
- URL filtering to exclude social media and unwanted domains
- Save results to text and CSV formats
- Configurable number of search results

## Requirements

```
requests
beautifulsoup4
```

## Installation

1. Clone the repository:
```bash
git clone 
cd Gdorkingpy
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python main.py
```

### Options:
1. Choose from categories 1-7 for predefined topic searches
2. Select option 8 for custom search queries
3. Use option 9 to convert saved URLs to CSV format
4. Type 'esc' to exit the program

### Output Files
- All URLs are saved to `articles/all_urls.txt`
- CSV format is available at `articles/urls.csv`

## Note
This tool is for educational purposes only. Please respect Google's terms of service and use responsibly. 