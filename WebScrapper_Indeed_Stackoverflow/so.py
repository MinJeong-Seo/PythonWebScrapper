import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find("div",{"class":"s-pagination"}).find_all('a')
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  title = html.find("a",{"class":"s-link"})["title"]
  company, location= html.find("h3",{"class":"fs-body1"}).find_all("span",recursive = False)
  company = company.get_text(strip = True)
  location = location.get_text(strip = True)
  job_id = html["data-jobid"]
  job_title = title.replace(" ","-")
  return {'title':title, 'company':company, 'location':location, 'link':f"https://stackoverflow.com/jobs/{job_id}/{job_title}"}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page {page}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text,'html.parser')
    results = soup.find_all("div",{"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
      

def get_jobs():
  last_page = get_last_page()
  #last_page is more than 170. I just need to test the code. 
  #So I use only 10 pages to extract. 
  #If you need to extract all the things, then you should change parameter 10 to last_page.
  jobs = extract_jobs(10)
  return jobs