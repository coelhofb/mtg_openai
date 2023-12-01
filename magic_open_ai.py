import os
import json
import openai
import urllib.request
import hashlib
import numpy as np

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo"
GPT_MODEL_PARAMS = {"temperature": 1, "max_tokens": 256, "top_p":1, "frequency_penalty":0,"presence_penalty":0}

def generate_mtg_card(theme):
   query = """Create 1 Magic the gathering card based on """ + theme + """ theme. The Mana cost needs to follow standard MTG rules.
                       
            Return only a json object containing card data with all attributes: name, color, mana_cost, type, ability, rarity, power, toughness.
            name can have a maximum of 35 characters. 
            color should be a list with possible values: Red, Black, Blue, Green, White, Colorless, Null
            mana_cost needs to contain only numbers and letters.
            ability text can have a maximum of 300 characters. 

            """
   openai.api_key = OPENAI_API_KEY
   response = openai.ChatCompletion.create(
    model=GPT_MODEL,
    messages=[
      {
        "role": "user",
        "content": query
      },
    ],
    temperature=GPT_MODEL_PARAMS["temperature"],
    max_tokens=GPT_MODEL_PARAMS["max_tokens"],
    top_p=GPT_MODEL_PARAMS["top_p"],
    frequency_penalty=GPT_MODEL_PARAMS["frequency_penalty"],
    presence_penalty=GPT_MODEL_PARAMS["presence_penalty"]
   )
   
   raw_card = str(response["choices"][0]["message"]["content"])
   print(raw_card)
   mtg_card = json.loads(raw_card)
   
   mtg_card["theme"] = theme
   
   ability =[]
   ability = mtg_card["ability"].splitlines()   
   mtg_card["ability"] = ability

   color_qty = 0
   for color in mtg_card["color"]:
      if color not in ["", 'Null', 'None', 'Colorless']:
         color_qty = color_qty +1	
   mtg_card["color_qty"] = color_qty

   if mtg_card["color_qty"] > 1:
    mtg_card["color_code"] = 'Golden'
   elif mtg_card["type"] == 'Land':
    mtg_card["color_code"] = 'Land'
   elif mtg_card["color_qty"] == 0:
    mtg_card["color_code"] = 'Colorless'
   else: mtg_card["color_code"] = mtg_card["color"][0]
    
   pt = ''
   if mtg_card["power"] not in ['Null','','None','-','--']:
    pt = str(mtg_card["power"])+'/'+str(mtg_card["toughness"])
   mtg_card["pt"] = pt
  
   return mtg_card

def generate_mtg_card_bkp(theme):
   query = """can you create 1 Magic the gathering card based on """ + theme + """ theme? The Mana cost needs to follow standard MTG rules.
            Put the results in the following format:

            Name: 
            Mana Cost:
            List of Different Colors: 
            Type: 
            Rarity: 
            Power/Toughness: 
            Ability:
            """
   openai.api_key = OPENAI_API_KEY
   response = openai.ChatCompletion.create(
    model=GPT_MODEL,
    messages=[
      {
        "role": "user",
        "content": query
      },
    ],
    temperature=GPT_MODEL_PARAMS["temperature"],
    max_tokens=GPT_MODEL_PARAMS["max_tokens"],
    top_p=GPT_MODEL_PARAMS["top_p"],
    frequency_penalty=GPT_MODEL_PARAMS["frequency_penalty"],
    presence_penalty=GPT_MODEL_PARAMS["presence_penalty"]
   )
   
   lines = response["choices"][0]["message"]["content"].splitlines()
   lines_size = len(lines)
   colors = lines[2].split(": ")[1].split(" ")
   color_qty = 0
   for color in colors:
      if color not in ["", 'None']:
         color_qty = color_qty +1	
   mtg_card = {
    "theme": theme
    ,"name":lines[0].split(": ")[1]
    ,"mana_cost":lines[1].split(": ")[1].replace("{","").replace("}","").replace("(","").replace(")","")
    ,"color": colors
    ,"color_qty": color_qty
    ,"color_code" : ""
    ,"type": lines[3].split(": ")[1]
    ,"rarity":lines[4].split(": ")[1]
    ,"pt":lines[5].split(": ")[1]
    ,"ability":[]
   }
   if mtg_card["color_qty"] > 1:
      mtg_card["color_code"] = 'Golden'
   elif mtg_card["type"] == 'Land':
      mtg_card["color_code"] = 'Land'
   elif mtg_card["color_qty"] == 0:
      mtg_card["color_code"] = 'Colorless'
   else: mtg_card["color_code"] = mtg_card["color"][0]

   for i in range(6,lines_size):
      ability = lines[i].split("Ability: ")[-1]
      if ability:
         mtg_card["ability"].append(ability)

   return mtg_card

def generate_illustration(theme, card_name,card_type,out_file_path):
   openai.api_key = OPENAI_API_KEY
   response = openai.Image.create(
    prompt="Create an ilustration based on " + theme + " " + card_name + " " + card_type + '. The illustration should use Magic The Gathering artwork style.',
    n=1,
    size="512x512"
   )
   image_url = response['data'][0]['url']

   salt = str(np.random.randint(100, size=1))
   hashstr = hashlib.md5(str(image_url[-10:]+salt).encode()).hexdigest() # 32 character hexadecimal
   mtg_img_file = hashstr[0:15]+'.png'
   mtg_img_path = out_file_path+mtg_img_file

   urllib.request.urlretrieve(image_url, filename=mtg_img_path)

   return(mtg_img_file)


