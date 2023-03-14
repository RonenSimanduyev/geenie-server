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




def sumReviews(questions:list) -> str:
    answer=[]
    for question in questions : 
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'{question} ',
            temperature=0.6,
            max_tokens=2048,
        )
        message = response.choices[0].text
        answer.append(message)
    return answer



def askGPTchunks(values_list: list) -> str:
    print('asked about list')
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
                    "role":"user","content": f"sumarize these reviews {values_list[0:30]}",
                    "role":"user","content": f"sumarize these reviews {values_list[30:60]}",
                    "role":"user","content": f"sumarize these reviews {values_list[30:60]}",
                    "role":"user","content": f"sumarize these reviews {values_list[60:90]}",
                    "role":"user","content": f"sumarize these reviews {values_list[120:150]}",
                    "role":"user","content": f"sumarize these reviews {values_list[150:180]}",
                    "role":"user","content": f"sumarize these reviews {values_list[180:210]}",
                    "role":"user","content": f"sumarize these reviews {values_list[210:240]}",
                    "role":"user","content": f"sumarize these reviews {values_list[240:270]}",
                    "role":"user","content": f"sumarize these reviews {values_list[270:300]}",
                    "role":"user","content": f"sumarize these reviews {values_list[330:360]}",
                    "role":"user","content": f"sumarize these reviews {values_list[360:390]}",
                    "role":"user","content": f"sumarize these reviews {values_list[390:400]}",
                   }]
                )
    return completion

    


def askGPTaboutAll(before:str ,completion: list,after:str) -> str:
    print('asking about all')
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role":"user","content": f"{before} {completion} {after}"}]
    )
    
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer


def askGPTdirectly(questions: str) -> str:
    print('asked directly')
    fullAnswer=[]
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
                  
                    "role":"user","content": f"{questions}"}]
                )
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer



