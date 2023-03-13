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



# def sumReviews(questions:list) -> str:
#     answer=[]
#     print(questions)
#     print('entered sum reviews')
#     for question in questions :
#         print(f'{question}')
#         completion=openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             max_tokens=150,
#             messages=[{"role":"user","content": f"{question}"}]
#         )
#         print('after question')
#         response = completion['choices'][0]['message']['content'].strip()
#         answer.append(response)
#     return answer






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

def askGPT(values_list: list) -> str:
    print('asked about list')
    fullAnswer=[]
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{
                   "role":"user","content": f"sumarize these reviews {values_list[0:30]}",
                   "role":"user","content": f"sumarize these reviews {values_list[30:60]}",
                   "role":"user","content": f"sumarize these reviews {values_list[30:60]}",
                   "role":"user","content": f"sumarize these reviews {values_list[60:90]}",
                   "role":"user","content": f"sumarize these reviews {values_list[120:150]}",
                   "role":"user","content": f"sumarize these reviews {values_list[150:180]}",}]
                )
    return completion

    


def askGPTaboutAll(completion: list) -> str:
    print('asking about all')
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role":"user","content": f"please analyze over 400 customer reviews for a product on Amazon from this list {completion} 1.Can you provide a summary of all complaints with corresponding percentages in 20 bullets by topic? 2.Can you provide insights into the overall sentiment of the reviews, the most commonly mentioned positive and negative aspects of the product, and any recurring themes or issues mentioned in the reviews?3.Can you identify any correlations or relationships between variables in the data, such as the correlation between the price of the product and the overall customer satisfaction?4.Can you provide visualizations of the data in the form of graphs or charts to help illustrate the insights and trends identified in the analysis?5.Can you please write all common themes negative, positive with corresponding percentages? 6.Can you write HTML code of a pie chart that can be used to show the proportion of each complaint? Each slice of the pie would represent a specific complaint and its corresponding percentage.7. Based on your analysis of the consumer reviews, can you write the common themes that emerged from the feedback? 8. Use descriptive language for all answers"}]
    )
    asnwer= completion['choices'][0]['message']['content'].strip()
    return asnwer





