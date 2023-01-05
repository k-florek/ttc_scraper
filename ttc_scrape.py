import os,sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

# url for getting UW Job Titles
url = "https://hr.wisc.edu/standard-job-descriptions/"

# set browser to headless to hide
chrome_options = Options()
chrome_options.add_argument("--headless")

# load selenium driver and open page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=chrome_options)) 
driver.get(url) 

#scrape with beautiful soup
html = driver.page_source
soup = BeautifulSoup(html, 'html5lib')

#job class
class Job:
    def __init__(self):
        self.title = ""
        self.jobCode = ""
        self.salary = ""
        self.employeeCategory = ""
        self.jobGroup = ""
        self.jobSubgroup = ""
        self.jobSummary = ""
        self.jobResponsibilities = ""
        self.education = ""
        self.flsa = ""
        self.institutionJob = ""
        self.reqSup = ""
        self.scaledJob = ""
        self.fullJobCode = ""
        self.link = ""
    
    def print(self):
        print()
        print("Title: ", self.title)
        print("Job Code: ", self.jobCode)
        print("Salary: ", self.salary)
        print("Employee Category: ", self.employeeCategory)
        print("Job Group: ", self.jobGroup)
        print("Job Subgroup: ", self.jobSubgroup)
        print("Job Summary: ", self.jobSummary)
        print("Job Responsibilities: ", self.jobResponsibilities)
        print("Education: ", self.education)
        print("FLSA Status: ", self.flsa)
        print("Institution Job: ", self.institutionJob)
        print("Require Supervisor: ", self.reqSup)
        print("Scaled Job: ", self.scaledJob)
        print("Full Job Code: ", self.fullJobCode)
        print("URL: ", self.link)
        print("------------------------------------------------")
    
    def getList(self):
        l = [
            self.title,
            self.jobCode,
            self.salary,
            self.employeeCategory,
            self.jobGroup,
            self.jobSubgroup,
            self.jobSummary,
            self.jobResponsibilities,
            self.education,
            self.flsa,
            self.institutionJob,
            self.reqSup,
            self.scaledJob,
            self.fullJobCode,
            self.link
        ]
        return l

#object to store jobs by job code
data = {}

#need to expand all job details
number_li_elems=len(driver.find_elements(By.XPATH, "/html/body/div[3]/main/article/div/div/div/div/div/div[6]/div/table/tbody/tr/td/button"))
number_li_elem = number_li_elems * 2
for x in range(number_li_elems):
    if x%2 == 1:
        button = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(" + str(x) + ") > td.job-details > button")
        button.click()
    x += 1

jd_row = soup.find_all("tr", class_="jd-row")
for row in jd_row:
    if "isSearched" in row["class"]:
        try:
            j = Job()
            j.title = row.find("td", class_="job-title").text
            j.jobCode = row.find("td", class_="job-code").text
            j.salary = row.find("td", class_="Salary")["data-val"]
            j.employeeCategory = row.find("td", class_="Category")["data-val"]
            j.jobGroup = row.find("td", class_="job-group").find("span", onclick=True).text
            j.jobSubgroup = row.find("td", class_="job-subgroup").find("span", onclick=True).text
        except Exception as e:
            print(e)
            print("Error on:","\n",row.prettify())
            continue

        data[j.jobCode] = j
    elif "jd-row-expand" in row["class"]:
        jc = row.find("div", class_="job-code-detail").find("p").text.split(':')[0].strip()
        j = data[jc]
        try:
            j.jobSummary = row.find("div", class_="summary").find("p").text
            #j.jobResponsibilities = row.find("div", class_="responsibilities").find_all("p")
            j.education = row.find("div", class_="education").find("p").text
            j.flsa = row.find("div", class_="flsa").find("p").text
            j.institutionJob = row.find("div", class_="job-scope").find("p").text
            j.reqSup = row.find("div", class_="fte").find("p").text
            j.scaledJob = row.find("div", class_="scaled").find("p").text
            j.fullJobCode = row.find("div", class_="job-code-detail").find("p").text
            j.link = row.find("div", class_="job-permalink").find("a")['href']
        except Exception as e:
            print(e)
            print("Error on:","\n",row.prettify())
            continue
    else:
        print("No data matching in row")

with open("ttc_scraping.csv",'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",", quotechar="|")
    writer.writerow([
            "title",
            "jobCode",
            "salary",
            "employeeCategory",
            "jobGroup",
            "jobSubgroup",
            "jobSummary",
            "jobResponsibilities",
            "education",
            "flsa",
            "institutionJob",
            "reqSup",
            "scaledJob",
            "fullJobCode",
            "link"
    ])
    for job in data.keys():
        j = data[job]
        writer.writerow(j.getList())

