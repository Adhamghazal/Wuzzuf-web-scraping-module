import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

def pages(field):
  resp=requests.get(f"https://wuzzuf.net/search/jobs?q={field}")
  soup=BeautifulSoup(resp.content,'lxml')
  num_of_available_jobs=soup.find('strong')

  #removing any commas or un needed spaces from the number of pages
  num_of_available_jobs = num_of_available_jobs.text.replace(',', '').strip()
  num_of_available_jobs=int(num_of_available_jobs)

  #returning number of pages
  return math.ceil(num_of_available_jobs/15)

def scrap(field):
  #getting our link ready to be used
  field=field.replace(' ','%20')
  num_of_pages=pages(field)
  #Defining empty lists for our attributes to be exctracted
  job_titles=[]
  locations=[]
  requirements=[]
  job_type=[]
  job_links=[]
  job={}

  for x in range(0,num_of_pages):
    #requesting data for each page in the search results
    resp=requests.get(f"https://wuzzuf.net/search/jobs?q={field}&start={x}")

    #getting the content in the response using our parser
    soup=BeautifulSoup(resp.content,'lxml')

    #extracting job titles and links
    titles_and_links=soup.find_all('h2',class_='css-193uk2c')
    links=[link.a['href'] for link in titles_and_links]
    titles=[title.text.strip() for title in titles_and_links]

    #Saving the titles and the links for each page
    job_titles+=titles
    job_links+=links

    #etracting the location and saving it
    location=soup.find_all('span',class_="css-16x61xq")
    location=[loc.text.strip() for loc in location]
    locations+=location

    #extracting the requirements and saving them
    specifications=soup.find_all('div',class_="css-1rhj4yg")
    specifications=[spec.text for spec in specifications]
    requirements+=specifications

    #Type of the job
    j_type=soup.find_all('div',class_="css-5jhz9n")
    j_type=[job.text for job in j_type]
    job_type+=j_type


  #loading the results into a dictonary
  jobs={
        'Job_Title':job_titles,
        'Location': locations,
        'Job_Type' : job_type,
        'Requirements' : requirements,
        'Job_Link' : job_links
        }

  #Inserting the data into a dataframe
  df=pd.DataFrame(jobs)
  return df
if __name__=="__main__":
  scrapped_data=scrap("data analysis")
  #Saving results into a csv file
  scrapped_data.to_csv('Jobs.csv',index=False)



