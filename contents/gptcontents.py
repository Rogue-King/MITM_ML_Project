from trash_objects import objects_list
import os
import openai
import config #key stored in config.py
openai.api_key = config.OPENAI_API_KEY

my_list = objects_list()

def diy_generation(query):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional hobbyist, with vast experience in DIY projects."},
            #{"role": "user", "content": 'Come up with a DIY project using the following materials:  "{text}.format(text=query)}"'}
            {"role": "user", "content": f'Come up with a DIY project using the following materials: "{query}"'}
            
        ]
    )
        

    #print(response) to find format of gpt response
    if 'choices' in response:
        if len(response['choices']) > 0:
            raw_answer = response['choices'][0]['message']['content']
        else:
            "Sorry, I don't have an answer for that."
    else:
        "Sorry, I don't have an answer for that."
    
    return raw_answer
    


    
