import time
import requests
from bs4 import BeautifulSoup
import threading
import random
import csv
import os
from urllib.parse import urlparse


# ---------------- Esc/Results=10 ----------------

EXIT_COMMAND = "esc"
DEFAULT_RESULTS = 10
CSV_FILENAME = "articles/urls.csv"

# ---------------- Colors To Be Defined ----------------

Yellow = "\033[1;33;40m"
Red = "\033[1;31;40m"
Normal = "\033[0;0m"
BM = "\033[1;35;40m"
Green = "\033[1;32;40m"

# ---------------- Blocked Domains ----------------
BLOCKED_DOMAINS = [
    'facebook.com', 'fb.com', 'instagram.com', 'youtube.com', 'm.facebook.com',
    'twitter.com', 'x.com', 'linkedin.com', 'medium.com', 'm.youtube.com', 'slideshare.net'
    'wikipedia.org', 'reddit.com', 'tiktok.com', 'pinterest.com', 'maps.google.co.il', 'maps.google.com', 'accounts.google.com', 'support.google.com'
]

# ---------------- Proxy Configuration ----------------
PROXIES = [
    "http://user:password@ip:port"
]

def get_proxy():
    if not PROXIES:
        return None
    return {'http': random.choice(PROXIES), 'https': random.choice(PROXIES)}

# ---------------- Topic Categories ----------------
TOPICS = {
    "Web3": [
        "AI and Blockchain integrations", "AR and VR in Web3", "Bitcoin", 
        "Blockchain Interoperability", "BlockChains", "Crypto OGs",
        "Crypto Regulation and Compliance", "DAO governance", "Defi",
        "Digital Identity and Privacy", "Gamefi", "Meme Coins",
        "Metaverse Development", "NFT Art", "NFT Utility", "Node Sales",
        "Ordinals", "Real World Asset Tokenization", "Refi & Re-staking",
        "Stablecoins", "Token Projects", "Tokenomics", "Web3 Gaming",
        "Web3 Security", "Zero Knowledge Proofs"
    ],
    "AI": [
        "AI/ML", "AI in Cybersecurity", "AI in Finance", "AI in Healthcare",
        "AI Model Architectures", "AI Safety and Alignment", "Autonomous Systems",
        "Computer Vision", "Ethics in AI", "Explainable AI (XAI)",
        "Federated Learning", "Fine-Tuning and Transfer Learning",
        "Generative AI", "Multimodal AI", "Natural Language Processing (NLP)",
        "Prompt Engineering", "Reinforcement Learning",
        "Retrieval-Augmented Generation (RAG)", "Zero-Shot and Few-Shot Learning"
    ],
    "Politics": [
        "Donald Trump's Campaign", "Kamala Harris's Campaign",
        "Immigration Policies", "Economic Policies", "Healthcare Policies",
        "Climate Change Stances", "Criminal Justice Reform",
        "Election Polls and Endorsements", "Campaign Strategies",
        "Debates and Key Speeches"
    ],
    "Climate": [
        "Climate Science Fundamentals", "Climate Impacts",
        "Mitigation Strategies", "Adaptation Measures",
        "Policy And Governance", "Technological Solutions",
        "Communication and Awareness", "Equity and Social Justice"
    ],
    "Quantum": [
        "Quantum Mechanics Fundamentals", "Quantum Hardware",
        "Quantum Algorithms", "Quantum Software",
        "Quantum Error Correction", "Quantum Communication",
        "Quantum Cryptography"
    ],
    "Nuclear": [
        "Nuclear Physics Fundamentals", "Nuclear Reactor Technologies",
        "Nuclear Fuel Cycle", "Nuclear Safety", "Nuclear Waste Management",
        "Fusion Energy Development"
    ],
    "Pandemic": [
        "Epidemiology", "Pandemic History", "Virus Biology",
        "Public Health Measures", "Healthcare System Response",
        "Vaccine Development", "Economic Impacts"
    ]
}

def is_blocked_url(url):
    try:
        domain = urlparse(url).netloc.lower()
        return any(blocked in domain for blocked in BLOCKED_DOMAINS)
    except:
        return True

def save_article(topic, url, results_count):
    filename = "articles/all_urls.txt"

    os.makedirs("articles", exist_ok=True)
    
    mode = 'w' if results_count == 1 else 'a'
    
    try:
        with open(filename, mode, encoding='utf-8') as f:
            f.write(f"{url}\n")
            
        print(f"{Green}Saved URL to {filename}{Normal}")
    except Exception as e:
        print(f"{Red}Error saving URL: {str(e)}{Normal}")

def convert_to_csv():
    try:
        
        with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            with open("articles/all_urls.txt", 'r', encoding='utf-8') as txt_file:
                urls = [line.strip() for line in txt_file if line.strip()]
                for url in urls:
                    writer.writerow([url])
        
        print(f"{Green}Successfully converted URLs to {CSV_FILENAME}{Normal}")
    except Exception as e:
        print(f"{Red}Error converting to CSV: {str(e)}{Normal}")

def Banner_Show():
    banner = f'''{Yellow}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    Google Search Scraper                      ║
    ║                                                               ║
    ║  A tool to scrape and save Google search results by category  ║
    ╚═══════════════════════════════════════════════════════════════╝{Normal}
            (URLs will be saved to 'articles/all_urls.txt')
    '''
    print(banner)

def G_Examples():
    print(f'''
{Red}Available Categories:{Normal}
1. Web3
2. AI
3. Politics
4. Climate
5. Quantum
6. Nuclear
7. Pandemic
8. Custom Search
9. Convert URLs to CSV

{Green}Usage:{Normal}
- Enter category number to get random topic search
- Or enter custom search query
- Use '9' to convert saved URLs to CSV
- Use 'esc' to exit
''')

def GetSearchResult(search_query, num_results=DEFAULT_RESULTS):
    total = 0
    valid_results = 0
    payload = f"q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582",
        "Method": "GET"
    }
    url = f"https://www.google.co.il/search?{payload}&num={num_results}"
    
    try:
        proxy = get_proxy()
        r = requests.get(url, params=headers, proxies=proxy, timeout=10)
    except requests.RequestException as e:
        print(f"{Red}Error with proxy request: {str(e)}{Normal}")
        
        r = requests.get(url, params=headers)
    
    if r.status_code != 200:
        print("Something went wrong, please try again...")
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.findAll("a", href=True)
    for link in links:
        try:
            link_href = link.get("href")
            if "url?q=" in link_href and not "webcache" in link_href:
                url = link_href.split("/url?q=")[1].split('&sa=U')[0]
                total += 1
                
                if not is_blocked_url(url):
                    valid_results += 1
                    print(f"{valid_results}>> {url}")
                    save_article(search_query, url, valid_results)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
    print(f"{Yellow}Results: Total of {valid_results} valid URLs were found (filtered {total - valid_results} social media URLs).{Normal}")

def get_random_topic_search(category):
    if category not in TOPICS:
        return None
    topic = random.choice(TOPICS[category])
    return f'intitle:"{topic}" site:.*'

Banner_Show()
time.sleep(1.5)
G_Examples()

while True:
    try:
        choice = input(f"\nEnter category number (1-9) or search query ('{Yellow}{EXIT_COMMAND}{Normal}' for exit): ")
        
        if choice == EXIT_COMMAND:
            break
            
        if choice == "9":
            convert_to_csv()
            continue
            
        search_query = ""
        if choice.isdigit() and 1 <= int(choice) <= 8:
            category_map = {
                "1": "Web3", "2": "AI", "3": "Politics",
                "4": "Climate", "5": "Quantum", "6": "Nuclear",
                "7": "Pandemic"
            }
            
            if choice == "8":
                search_query = input("Enter custom search query: ")
            else:
                search_query = get_random_topic_search(category_map[choice])
                print(f"\n{Green}Selected Topic Search:{Normal} {search_query}")
        else:
            search_query = choice
            
        try:
            Num_Results = int(input("Results As Possible (Default is 10): "))
        except ValueError:
            Num_Results = DEFAULT_RESULTS
            
        s_thread = threading.Thread(target=GetSearchResult, args=(search_query, Num_Results))
        s_thread.start()
        s_thread.join()
        
    except KeyboardInterrupt:
        print("\nExiting...")
        break