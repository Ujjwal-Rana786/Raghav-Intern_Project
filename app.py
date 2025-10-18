from flask import Flask, render_template, url_for, redirect
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
import re 
import yfinance as yf


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Global DataFrame to hold scraped data
scraped_data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/scraping')
def scraping():
    return render_template('webscraping.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutMe.html')

@app.route('/aboutCodroid')
def aboutCodroid():
    return render_template('aboutCodroid.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/dataScience')
def dataScience():
    return render_template('dataScience.html')

@app.route('/PowerBI')
def powerBI():
    return render_template('comingSoon.html', page_name="powerBI") )

@app.route('/AIML')
def AIML():
    return render_template('comingSoon.html', page_name="AI/ML")

@app.route('/bookscraping')
def scrape_books():
    global scraped_data
    url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    items = soup.find_all("article", class_="product_pod")

    for item in items:
        name_tag = item.find("h3").find("a")
        price_tag = item.find("p", class_="price_color")

        name = name_tag.get("title") if name_tag else "N/A"
        price = price_tag.get_text(strip=True) if price_tag else "£0"

        # inside the loop
        price_text = price_tag.get_text(strip=True) if price_tag else "£0"
        price_clean = re.sub(r"[^\d.]", "", price_text)   #$4.4 -> 4.4
        price = float(price_clean) if price_clean else 0.0


        products.append([name, price])

    scraped_data = pd.DataFrame(products, columns=["Name", "Price"])
    return render_template("bookscraping.html", table=scraped_data.to_html(index=False, classes="table table-striped"))


@app.route('/gcambala') 
def scrape_data():
    url = 'http://gcambalacantthry.edu.in/Faculty'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Successfully fetched the page!")
    else:
        print(f"Failed to retrieve the page! Status Code: {response.status_code}")
        return "Failed to fetch page", 500

    soup = BeautifulSoup(response.content, 'html.parser')

    faculty_info = []

    faculty_data = soup.find_all('div', {'class': 'contact-box'})

    for data in faculty_data:
        name_span = data.find('span', class_='text-primary')
        dept_span = data.find('span', id=lambda x: x and 'lblSubject' in x)
        post_span = data.find('span', id=lambda x: x and 'lblDesignation' in x)
        img_tag = data.find('img')

        fname = name_span.get_text(strip=True) if name_span else "N/A"
        fdept = dept_span.get_text(strip=True) if dept_span else "N/A"
        fpost = post_span.get_text(strip=True) if post_span else "N/A"
        fimg = img_tag['src'] if img_tag else ""

        faculty_info.append({
            'faculty_name': fname,
            'faculty_post': fpost,
            'faculty_dept': fdept,
            'faculty_photo': fimg
        })

    pd.set_option('display.max_rows', None)
   

    scraped_data = pd.DataFrame(faculty_info, columns=["faculty_name", "faculty_post", "faculty_dept", "faculty_photo"])

    return render_template("gcambala.html", table=scraped_data.to_html(index=False, classes="table table-striped"))


@app.route('/linkedin') 
def job():


   url = "https://www.linkedin.com/jobs/search?keywords=Software+Engineer&location=New+York"

   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

   response = requests.get(url, headers=headers)

   soup = BeautifulSoup(response.content, "html.parser")

   jobs_list = []

   job_posts = soup.find_all("div", {"class": "base-card"})

   for job in job_posts:
      title = job.find("h3")
      company = job.find("h4")
      location = job.find("span", {"class": "job-search-card__location"})
    
      # Replace this with the actual class or tag of "Job Summary" if available
     
    
      job_data = []
      job_data.append(title.get_text(strip=True) if title else None)
      job_data.append(company.get_text(strip=True) if company else None)
      job_data.append(location.get_text(strip=True) if location else None)

    
      jobs_list.append(job_data)

   scraped_data = pd.DataFrame( jobs_list , columns=["title","company","location"])

   return render_template("linkedin.html", table=scraped_data.to_html(index=False, classes="table table-striped"))    


@app.route('/crpyto') 
def crpyto():
  
  crypto_ticker = "BTC-USD"
  btc = yf.Ticker(crypto_ticker)

  data = btc.history(start="2025-01-01", end="2025-09-01", interval="1d")
  
  return render_template(
        "crpyto.html",
        history_table=data.to_html(index=False, classes="table table-bordered")
    ) 







if __name__ == '__main__':
    app.run(debug=False, port=3000, host="0.0.0.0")


