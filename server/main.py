import openai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time
import time
# from AmazonReviewsAnalysis import reviewAnalysis
from scrapper import runScrapperScript
from uploadToSheets import uploadToSheets,remove_scrapper_result
from talkToGPT import sumReviews, askAboutTOS, amazon_TOS_doc,askGPTaboutAll,askGPT
import asyncio
import pandas as pd
import requests
import gdown
import json
from fastapi.responses import JSONResponse
from sentiment_Analysis import analyze_reviews_csv
import csv
import os

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


async def ask_about_reviews(questions:str ) -> str:
    print('entered ask about reviwes')
    response = sumReviews(questions)
    print(response)
    return response

def downloadCSV(drive_url: str):
    url = drive_url
    # Split the URL into parts using '/' as separator
    url_parts = url.split('/')
    # Get the part of the URL that contains the file ID
    file_id = url_parts[5]
    # Download the file and get the file name
    response = gdown.download(f"https://drive.google.com/uc?id={file_id}&export=download", quiet=False,fuzzy=True)
    # Remove the .json extension from the file name
    file_name = os.path.splitext(response)[0]
    # Convert the JSON file to a CSV file
    with open(response, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(f"{file_name}.csv", "w", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(data[0].keys())
        # Write the data rows
        for item in data:
            writer.writerow(item.values())
    # Delete the downloaded JSON file
    os.remove(response)
    return f"{file_name}.csv"




async def sendToGPT(filename):
    print('started')
    allReviews= []
    values_list = []
    df = pd.read_csv(f'{filename}')
    print(len(df))
    # Extract the values from the fourth column for the current batch of rows
    values = df.iloc[0:, 3].values.tolist()
     # Add the values to the list
    values_list.extend(values)
    response = askGPT(values_list)
    response = askGPTaboutAll(response)
    return response


@app.post('/fullScript')
async def scrape_and_drive_and_ask_about_reviews(request: Request)->list:
    start_time = time.time()
    # list to keep the response from the 2 analysis
    endList=[]
    data = await request.json()
    # getting a question list
    questions = data.get('questions')
    # getting the url from google drive
    
    drive_url = data.get('URL')
    # activate a funciton that scrape the reviews of the product and upload it to the google drive
    #@@ drive_url,filename = await scrape_and_drive(url) @@
   
    # takes the url download the scv and naming it as the asin name
    filename = downloadCSV(drive_url)
    print(filename)
     # first analysis of the reviews by gpt
    gpt_time = time.time()

    try:
        print('start gpt analysis')
        analysisGPT = await sendToGPT(filename)
        endList.append(analysisGPT)
    except:
        print('failed to load analysis 1')
    gpt_end_time = time.time()
    print(f'took gpt {gpt_end_time - gpt_time}')
    analysis_time = time.time()
    # seconde analysis by script
    try:
        print('start analysis 2')
        analysis_sentiment=analyze_reviews_csv(filename)
        endList.append(analysis_sentiment)
    except:
        print('failed to load analysis 12')
    end_analysis_time = time.time()
    print(end_analysis_time - analysis_time )
    # remove the scrapper result from the root folder
    # remove_scrapper_result(filename)
    # return the answer to the front
    # return answer
    end_time = time.time()
    elapsed_time = end_time - start_time
    return JSONResponse(content=json.dumps(endList))





@app.post('/askBasedOnTOS')
async def ask_based_on_tos(request: Request):
    t: float = time()
    data = await request.json()
    question = data.get('question')
    response = askAboutTOS(question, amazon_TOS_doc)
    print(response)
    s=(time()-t)
    return response, f'that took {s} seconds'


@app.post('/spam')
async def ask_based_on_tos():
    filename='B07CRG94G3.csv'
    analysis_sentiment=analyze_reviews_csv(filename)
    return analysis_sentiment