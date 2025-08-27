import requests
import schedule
import time
import os

# ===============================
# 🔹 Config (replace with your own or set via env vars)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# ===============================
# 🔹 Fetch Jobs from LinkedIn API
# ===============================
def fetch_jobs():
    url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
    querystring = {
        "limit": "5",   # number of jobs
        "offset": "0",
        "title_filter": "Data Engineer",
        "location_filter": "United States OR United Kingdom"
    }
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        jobs = []
        for job in data.get("data", []):
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company"),
                "link": job.get("job_url")
            })
        return jobs
    except Exception as e:
        print("❌ Error fetching jobs:", e)
        return []

# ===============================
# 🔹 Send Message to Telegram
# ===============================
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        if res.status_code == 200:
            print(f"✅ Sent to user: {text}")   # <-- log success
        else:
            print("❌ Telegram Error:", res.text)
    except Exception as e:
        print("❌ Error sending message:", e)

# ===============================
# 🔹 Scheduled Task
# ===============================
def send_jobs():
    print("⏳ Fetching jobs...")
    jobs = fetch_jobs()
    if jobs:
        for job in jobs:
            msg = f"💼 {job['title']} at {job['company']}\n🔗 {job['link']}"
            send_message(msg)  # logs handled inside send_message
    else:
        send_message("No new jobs found today.")

# ===============================
# 🔹 Scheduler (runs daily)
# ===============================
schedule.every().day.at("17:00").do(send_jobs)  # 16:50 UTC = 22:20 IST

print("✅ Job Bot is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
