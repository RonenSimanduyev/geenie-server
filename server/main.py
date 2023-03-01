import openai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time
import time

from scrapper import runScrapperScript
from uploadToSheets import uploadToSheets,remove_scrapper_result
from talkToGPT import sumReviews, askAboutTOS, amazon_TOS_doc

app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def scrape_and_drive(URL: str):
    asin = runScrapperScript(URL)
    filename = f"{asin}.csv"
    drive_url = uploadToSheets(filename)
    remove_scrapper_result(filename)
    return drive_url


async def ask_about_reviews(drive_url: str):
    response = sumReviews(drive_url)
    print(response)
    return response


@app.post('/fullScript')
async def scrape_and_drive_and_ask_about_reviews(request: Request):
    # t = time()
    data = await request.json()
    url = data.get('URL')

    drive_url = await scrape_and_drive(url)
    response = await ask_about_reviews(drive_url)
    # print(time()-t)
    return response


@app.post('/scrapeANDdrive')
async def toSheets(URL):

    t=time()
    asin = runScrapperScript(URL)
    filename = f"{asin}.csv"
    drive_url = uploadToSheets(filename)
    remove_scrapper_result(filename)
    print(time()-t)
    return drive_url


@app.post('/sumReviews')
async def askAboutReviews(request: Request):
    t: float = time()
    data = await request.json()
    question = data.get('question')
    response = sumReviews(question)
    print(response)
    s = (time()-t)
    return response, f'that took {s} seconds'


@app.post('/askBasedOnTOS')
async def ask_based_on_tos(request: Request):
    t: float = time()
    data = await request.json()
    question = data.get('question')
    response = askAboutTOS(question, amazon_TOS_doc)
    print(response)
    s=(time()-t)
    return response, f'that took {s} seconds'



