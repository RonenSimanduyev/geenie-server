from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import math
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Host": "www.amazon.com",
    "Accept-Encoding": "gzip, deflate",
}

data: list = []

wanted_pages: int = 50

def setENV(URL):
    if len(URL) <90:
        asin: str = URL.split('/')[-1]
        URL="https://www.amazon.com/dp/"+asin
        print(URL)
    elif len(URL) >90:
        asin: str = URL.split('/')[-2]
        URL="https://www.amazon.com/dp/"+asin
        print(URL)
    else :
        asin=URL
        URL="https://www.amazon.com/dp/"+asin
        print(URL)
    try:
        response = requests.get(URL, headers=HEADERS)

    except requests.exceptions.RequestException:
        try:
            response = requests.get( headers=HEADERS)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Both attempts to make a request failed: {e}")

    soup = BeautifulSoup(response.content, "html.parser")
    print('sleep')
    time.sleep(5)
    print('wokeup')
    try:
        
        see_all_reviews_link = soup.find("a", {"data-hook":"see-all-reviews-link-foot"})["href"]
        URL_ALL_REVIEWS = "https://www.amazon.com" + see_all_reviews_link
        print('by data hook')
    
    except:
        URL_ALL_REVIEWS=  "https://www.amazon.com/product-reviews/"+asin+"/reviewerType=all_reviews"  
        print('by class')

    response = requests.get(URL_ALL_REVIEWS, headers=HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the element that contains the ratings with reviews and extract the text
    ratings_with_reviews_elem = soup.find("div", {"id": "filter-info-section"})
    ratings_with_reviews_text = ratings_with_reviews_elem.get_text().strip()

    #get just the reviews amount
    reviews_count = re.search(r'(\d+,*\d*)\s+with reviews', ratings_with_reviews_text).group(1)
    
    return asin, URL_ALL_REVIEWS, reviews_count


def scrape_reviews(page_url: str, headers: dict) -> list:
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = soup.find_all('div', {'data-hook': 'review'})
    page_data = []
    for review in reviews:
        profile_name = review.find("span", {"class": "a-profile-name"}).get_text()
        title_elem = review.find("a", {"data-hook": "review-title"})
        title = title_elem.get_text().strip() if title_elem else ""
        body = review.find("span", {"data-hook": "review-body"}).get_text().strip()
        stars_elem = review.find("i", {"data-hook": "review-star-rating"})
        stars = float(stars_elem.span.get_text().split()[0]) if stars_elem and stars_elem.span else None
        time=review.find("span", {"data-hook": "review-date"}).get_text().strip()
        vine_voice_elem = review.find("span", {"class": "a-size-mini a-color-link c7yBadgeAUI c7yTopDownDashedStrike c7y-badge-text a-text-bold"})
        vine_voice = vine_voice_elem.text.strip() if vine_voice_elem else ""
        page_data.append([profile_name, title, body, stars,time,vine_voice])
    return page_data


def execute(asin: str, URL_ALL_REVIEWS: str, reviews_count: str) -> list:
    global data
    with ThreadPoolExecutor() as executor:
        page_num = math.ceil(float(reviews_count.replace(",",""))/10)
        pages = [f"{URL_ALL_REVIEWS}&pageNumber={i+1}" for i in range(wanted_pages)]
        results = executor.map(scrape_reviews, pages, [HEADERS]*len(pages))
        for result in results:
            data += result
    df = pd.DataFrame(data, columns=['Name', 'Title', 'Body', 'Stars','Time','Vine Voice'])
    df.to_csv(f'{asin}.csv')
    return data




def runScrapperScript(URL):
    df = ''
    asin, URL_ALL_REVIEWS, reviews_count = setENV(URL)
    try:
        t: float = time()
        print('started')
        review: list = execute(asin, URL_ALL_REVIEWS, reviews_count)
        print(time()-t)
        return asin
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error occurred during scraping {e}"

