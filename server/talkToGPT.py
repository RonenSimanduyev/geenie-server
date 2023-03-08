import openai
import os
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



def sumReviews(question1:str ,reviews: str ,question2: str) -> str:
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role":"user","content": f"{question1},{reviews},{question2}"}]
    )
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer
