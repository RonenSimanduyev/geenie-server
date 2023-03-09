import openai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time
import time
from AmazonReviewsAnalysis import reviewAnalysis
from scrapper import runScrapperScript
from uploadToSheets import uploadToSheets,remove_scrapper_result
from talkToGPT import sumReviews, askAboutTOS, amazon_TOS_doc,askGPTaboutAll,askGPT
import asyncio
import pandas as pd
import requests
import gdown




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def scrape_and_drive(URL: str):
    asin = runScrapperScript(URL)
    filename = f"{asin}.csv"
    drive_url = uploadToSheets(filename)
    return drive_url,filename


async def ask_about_reviews(question1:str ,drive_url: str,question2:str) -> str:
    response = sumReviews(question1 ,drive_url ,question2)
    print(response)
    return response


def downloadCSV(drive_url: str):
    url = drive_url
    # Split the URL into parts using '/' as separator
    url_parts = url.split('/')
    # Get the part of the URL that contains the file ID
    file_id = url_parts[5]
    # Get the file name by making a request to the Google Drive API
    response = requests.get(f"https://drive.google.com/uc?export=download&id={file_id}")
    asin = response.headers['Content-Disposition'].split(';')[1].split('filename=')[1].strip('"')

    print('started download for csv')
    url = drive_url
    fileName = f'{asin}.csv'
    gdown.download(url, fileName, quiet=False,fuzzy=True)
    return fileName
    

@app.post('/fullScript')
async def scrape_and_drive_and_ask_about_reviews(request: Request)->list:
    # list to keep the response from the 2 analysis
    answer=[]
    data = await request.json()
    # getting the first part of the question
    question1 = data.get('question1')
    # getting the url from google drive
    drive_url = data.get('URL')
    # getting the second part of the question 
    question2 = data.get('question2')
    # activate a funciton that scrape the reviews of the product and upload it to the google drive
    
    #@@ drive_url,filename = await scrape_and_drive(url) @@
   
        
    # takes the url dounloadwind the scv and naming it as the asin name
    filename = downloadCSV(drive_url)
    
     # first analysis of the reviews by the csv

    try:
        print('start analysis 1')
        analysis1=reviewAnalysis(filename)
        answer.append(analysis1)
    except:
        print('failed to load analysis 1')
    # second analysis by gpt that get url of the reviews
    try:
        print('start analysis 2')
        analysis2 = await ask_about_reviews(question1 ,drive_url ,question2)
        # seperate the 2 analysis 
        answer.append('@@@@@@@@@@@@@@@@')
        answer.append(analysis2)
    except:
        print('failed to load analysis 2')
    # remove the scrapper result from the root folder
    remove_scrapper_result(filename)
    # return the answer to the front
    return answer


@app.post('/askBasedOnTOS')
async def ask_based_on_tos(request: Request):
    t: float = time()
    data = await request.json()
    question = data.get('question')
    response = askAboutTOS(question, amazon_TOS_doc)
    print(response)
    s=(time()-t)
    return response, f'that took {s} seconds'


@app.post('/askGPT')
async def ask_based_on_tos():
    print('started')
    
    allReviews= []
    values_list = []
    df = pd.read_csv('B00R3Z49G6.csv')
    for i in range(1, len(df),20):
        # Extract the values from the fourth column for the current batch of rows
        values = df.iloc[i:i+20, 3].values.tolist()
        # Add the values to the list
        values_list.extend(values)
        response = askGPT(values_list)
        allReviews.append(response)
        values_list=[]
        values=[]
        print(i)
    response = askGPTaboutAll(allReviews)
    return response


