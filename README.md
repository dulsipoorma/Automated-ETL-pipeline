# Automated Tech Internship ETL Pipeline

An automated, end-to-end Data Engineering pipeline built in Python to aggregate, clean, store, and monitor software and data engineering internship opportunities.

## 🏗️ Architecture & Workflow
1. **Extract (`extract.py`):** Scrapes target job listings using `BeautifulSoup`, handling pagination and HTTP requests.
2. **Transform (`transform.py`):** Uses `Pandas` to normalize dates, strip HTML tags, drop nulls, and parse description text for specific tech stack keywords (Python, SQL, Java, etc.).
3. **Load (`load.py`):** Connects via `SQLAlchemy` to upsert records into a relational database with idempotency to prevent duplicate entries.
4. **Orchestrate & Alert (`pipeline.py`):** Runs the pipeline on a scheduled timer, logs execution status via Python's `logging` module, and dispatches automated summary alerts.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Libraries:** Pandas, BeautifulSoup4, SQLAlchemy, Schedule
* **Database:** SQLite / PostgreSQL

## ⚙️ Getting Started
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/automated-etl-pipeline.git](https://github.com/your-username/automated-etl-pipeline.git)
