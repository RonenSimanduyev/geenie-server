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



def sumReviews(questions:list ,reviews: str) -> str:
    asnwer=[]
    for question in questions :
        completion=openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role":"user","content": f"{question},{reviews}"}]
        )
        resposnse= completion['choices'][0]['message']['content'].strip()
        answer.append(resposnse)
    return asnwer



def askGPT(values_list: list) -> str:
    print('asked about list')
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role":"user","content": f"As Amazon seller, we want to analyze the customer reviews and search for sentiment in each review, so we could learn where we should put our focus on to improve, product-wise.Create a report of sentiments for the list below. Each review is separated by ##Example:'One the weakest products I’ve ever bought the smallest bump shift movement will make it fall and disassemble.'Extracted sentiment:(Quality: Negative, Value: Negative){values_list}"}]
                )
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer


def askGPTq():
    print('staring')
    completion=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "what is the 2 feet in cm?"},
        {"role": "user", "content": "what is the color of the sky"}
    ])
    
    return completion['choices']['message']['content']
# [0]['message']['content']
    


def askGPTaboutAll(allReviews: list) -> str:
    print('asking about all')
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role":"user","content": f"Please give me a list of the topic's sentiments and their hit rate %, divided by negative and positive {allReviews}"}]
    )
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer





