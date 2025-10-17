from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask backend is running!"

@app.route("/jobs")
def jobs():
    jobs_data = []

    # Try lightweight scraping from a public site (fallback if fails)
    try:
        url = "https://remoteok.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        for row in soup.select("tr.job")[:8]:
            title = row.select_one(".company_and_position h2").get_text(strip=True) if row.select_one(".company_and_position h2") else "Software Engineer"
            company = row.select_one(".companyLink h3").get_text(strip=True) if row.select_one(".companyLink h3") else "Remote Company"
            location = row.select_one(".location").get_text(strip=True) if row.select_one(".location") else "Remote"
            link_tag = row.select_one("a")
            link = "https://remoteok.com" + link_tag["href"] if link_tag else "#"
            img = row.select_one("img")
            image = img["data-src"] if img and img.has_attr("data-src") else "https://cdn-icons-png.flaticon.com/512/942/942799.png"

            jobs_data.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": random.choice(["₹6–12 LPA", "₹10–18 LPA", "$90,000/yr", "Not Disclosed"]),
                "description": f"Exciting opportunity at {company} as a {title}.",
                "link": link,
                "image": image
            })

    except Exception as e:
        print("⚠️ Scrape failed, using fallback data:", e)

    # Fallback jobs if scraping fails
    if not jobs_data:
        jobs_data = [
            {
                "title": "Frontend Developer",
                "company": "TechNova",
                "location": "Remote / India",
                "salary": "₹8–15 LPA",
                "description": "Work with React and modern frontend tools to build amazing user experiences.",
                "link": "#",
                "image": "https://cdn-icons-png.flaticon.com/512/1055/1055687.png"
            },
            {
                "title": "Python Developer",
                "company": "DataCraft",
                "location": "Bangalore, India",
                "salary": "₹10–20 LPA",
                "description": "Develop backend systems and APIs using Python and Flask.",
                "link": "#",
                "image": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"
            },
            {
                "title": "UI/UX Designer",
                "company": "DesignFlow",
                "location": "Remote",
                "salary": "₹6–12 LPA",
                "description": "Create user-centered designs and collaborate with developers to improve usability.",
                "link": "#",
                "image": "https://cdn-icons-png.flaticon.com/512/2921/2921822.png"
            },
            {
                "title": "Data Analyst",
                "company": "InsightPro",
                "location": "Mumbai, India",
                "salary": "₹9–14 LPA",
                "description": "Analyze datasets to extract insights and improve business decisions.",
                "link": "#",
                "image": "https://cdn-icons-png.flaticon.com/512/1048/1048940.png"
            }
        ]

    return jsonify(jobs_data)


if __name__ == "__main__":
    app.run(debug=True)
