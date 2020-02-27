from bs4 import BeautifulSoup
import requests

URL = f"http://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword=IT"


# Order
# Get the last page
# Extract all jobs
# Extract details

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div",{"class":"pagination"}).find_all("span")
  pages = []

  for page in pagination:
    pages.append(page.get_text())
  
  last_page = pages[-1]
  return int(last_page)+1

def extract_detail_applying(html):
  title = html.find("div",{"class":"area_job"}).find("h2",{"class":"job_tit"}).find("a")["title"]
  company = html.find("div",{"class":"area_corp"}).find("a")["title"]
  location = html.find("div",{"class":"job_condition"}).find_all("a")
  if len(location) == 2:
    location = location[0].get_text() + " " + location[1].get_text()
  else:
    location = location[0].get_text()
  date = html.find("div",{"class":"job_date"}).find("span").get_text()
  return {"title": title, "company":company
  ,"location":location, "date":date}

def extract_job_applying(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SaramIn: Page {page}")
    result = requests.get(f"{URL}&recruitPage={page+1}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"item_recruit"})
    for result in results:
      job_apply = extract_detail_applying(result)
      jobs.append(job_apply)
  return jobs


def get_applying():
  last_page = get_last_page()
  jobs = extract_job_applying(last_page)
  return jobs