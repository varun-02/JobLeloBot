import requests
import schedule
import time

# Telegram Bot Credentials
BOT_TOKEN = "8401671419:AAG0ZTkeIHiwhNUzpqGOa5QR79Y-_YbBNG4"
CHAT_ID = "1111556993"

# Example: Fetch Jobs (replace with real API or scraper)
def fetch_jobs():
    # For now, hardcoded sample jobs
    jobs = [
        {"title": "Software Engineer", "link": "https://example.com/job1"},
        {"title": "Backend Developer", "link": "https://example.com/job2"},
    ]
    return jobs

# Send Message to Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# Job Scheduler Task
def send_jobs():
    jobs = fetch_jobs()
    if jobs:
        for job in jobs:
            send_message(f"{job['title']}\nApply: {job['link']}")
    else:
        send_message("No new jobs found today.")

# Schedule at 9 AM daily
schedule.every().day.at("20:55").do(send_jobs)

print("Job Bot is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
