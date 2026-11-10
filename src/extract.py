import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://itpro.lk/jobs/ai-and-data/internship/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def extract_jobs():
    print(f"[*] Fetching data from: {TARGET_URL}")
    
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error occurred: {e}")
        return

    # Convert the raw HTML into a searchable tree
    soup = BeautifulSoup(response.text, "html.parser")
    job_records = []

    # Target the specific 'article' tag that holds the job card
    job_cards = soup.find_all("article", class_=lambda x: x and "job-card" in x)
    print(f"[*] Found {len(job_cards)} internship listings to process.")

    for card in job_cards:
        # Target the exact classes we saw in the DOM inspector
        title_tag = card.find("h2", class_="jc-title")
        company_info_tag = card.find("div", class_="jc-company-info")
        date_tag = card.find("time", class_=lambda x: x and "time-posted" in x)

        # Clean the extracted text
        # We use .contents[0] for the title to avoid grabbing the "Marked as applied" span text
        job_title = title_tag.contents[0].strip() if title_tag else None
        
        if job_title:
            # The company info div contains both company and location
            company_and_location = company_info_tag.get_text(separator=" | ", strip=True) if company_info_tag else "N/A"
            date_posted = date_tag.get_text(strip=True) if date_tag else "Unknown Date"

            job_records.append({
                "job_title": job_title,
                "company_info": company_and_location, 
                "date_posted": date_posted,
                "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_url": TARGET_URL
            })

    # Save output to data/raw/
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "raw_itpro_jobs.csv")
    
    if job_records:
        keys = job_records[0].keys()
        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(job_records)
        print(f"[+] Successfully saved {len(job_records)} raw records to {output_file}")
    else:
        print("[!] No records extracted.")

if __name__ == "__main__":
    extract_jobs()