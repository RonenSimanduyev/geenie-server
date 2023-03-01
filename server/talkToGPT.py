import openai

API_Key = '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'
amazon_TOS_doc='https://docs.google.com/document/d/11XvCw-akyBSwKWoMSb5abif-dT7KGGGRUSV39Hc1JXc/edit?usp=sharing'
openai.api_key=API_Key



def askAboutTOS(question: str, regulations: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f'based on amazon TOS{regulations}.{question} ',
        temperature=0.6,
        max_tokens=150,
    )
    message = response.choices[0].text
    return message


def sumReviews(reviews: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f' this is a shereable link from google drive that include reviews from amazon product open the file and tell me how many columns are inside {reviews} ?. ',
        temperature=0.6,
        max_tokens=150,
    )
    message = response.choices[0].text
    return message
