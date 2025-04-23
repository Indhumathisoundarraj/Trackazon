📊 Trackazon – E-Commerce Price Tracker

Trackazon is a smart Python-based price tracking tool inspired by Amazon's dynamic pricing. It auto-scrapes product data, tracks price changes, stores history, and sends email alerts when the price drops!

🚀 Features
- Amazon product scraping using Playwright
- Automatic scheduling (hourly/daily)
- CSV-based price history tracking
- Email alerts when price drops
- CI/CD-ready (GitHub Actions)

🛠 Tech Stack
Python • Playwright • Schedule • SMTP • GitHub Actions

🔧 How to Run
pip install -r requirements.txt
python trackazon.py

🛍️ Note:
Due to Amazon's scraping restrictions on public/cloud servers, you can use sample/dummy product data to demonstrate automation and alerting. The original script supports real-time scraping when run locally.
