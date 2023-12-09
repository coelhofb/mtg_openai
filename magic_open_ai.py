import os
import json
import openai
import urllib.request
import hashlib
import numpy as np

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GPT_MODEL = "gpt-3.5-turbo"
GPT_MODEL = "gpt-3.5-turbo-1106"
GPT_MODEL_PARAMS = {"temperature": 1, "max_tokens": 256, "top_p":1, "frequency_penalty":0,"presence_penalty":0}

def generate_mtg_card(theme):
   query = """You are a Magic The Gathering Card designer.
   You need to create a card based on a theme asked by the user.
   When asked you will return  only a JSON object containing:
   {
   "name":  maximum 35 characters,
   "color":  list object with possible values Red, Black, Blue, Green, White, Colorless
   "mana_cost":  only numbers and letters
   "type":  
   "ability":  maximum of 300 characters. Each mana cost or tap need to be enclosure  { }
   "rarity": 
   "power":  integer
   "toughness":  integer
   }

   Create a card based on """ + theme + "."

   openai.api_key = OPENAI_API_KEY
   response = openai.ChatCompletion.create(
    model=GPT_MODEL,
    response_format={ "type": "json_object" },
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
   if mtg_card["type"].find('Land') > -1:
    mtg_card["color_code"] = 'Land'
    mtg_card["mana_cost"] = ''
   elif mtg_card["color_qty"] > 1:
    mtg_card["color_code"] = 'Golden'
   # elif mtg_card["type"].find('Land') in ['Land', 'Legendary Land']:
   elif mtg_card["color_qty"] == 0:
    mtg_card["color_code"] = 'Colorless'
   else: mtg_card["color_code"] = mtg_card["color"][0]
    
   pt = ''
   if mtg_card["toughness"] is not None and mtg_card["toughness"] not in [0,'Null','','None','-','--']:
    pt = str(mtg_card["power"])+'/'+str(mtg_card["toughness"])
   mtg_card["pt"] = pt
  
   return mtg_card

def generate_illustration_dall2(theme, card_name,card_type,out_file_path):
   openai.api_key = OPENAI_API_KEY
   response = openai.Image.create(
    prompt="Create an ilustration based on " + theme + " " + card_name + " " + card_type + '. The illustration should use Magic The Gathering artwork illustration only style.',
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

def generate_illustration(theme, card_name,card_type,out_file_path):
   openai.api_key = OPENAI_API_KEY
   response = openai.Image.create(
    model="dall-e-3",
    prompt="Create an ilustration based on " + theme + " " + card_name + " " + card_type + '. The illustration should use Magic The Gathering artwork style.',
    n=1,
    size="1024x1024",
    quality="standard"
   )
   image_url = response['data'][0]['url']

   salt = str(np.random.randint(100, size=1))
   hashstr = hashlib.md5(str(image_url[-10:]+salt).encode()).hexdigest() # 32 character hexadecimal
   mtg_img_file = hashstr[0:23]+'.png'
   mtg_img_path = out_file_path+mtg_img_file

   urllib.request.urlretrieve(image_url, filename=mtg_img_path)

   return(mtg_img_file)

     
def adjust_ability(ability):  

   adjusted_ability = []  
   for ability_line in ability:
      ability_line=ability_line.replace("{"+"T"+"}",'<span><img class="mana_text" src= "../static/img/T_mana.png"></span>')
      ability_line=ability_line.replace("{"+"R"+"}",'<span"><img class="mana_text" src= "../static/img/R_mana.png"></span>')
      ability_line=ability_line.replace("{"+"B"+"}",'<span"><img class="mana_text" src= "../static/img/B_mana.png"></span>')
      ability_line=ability_line.replace("{"+"U"+"}",'<span"><img class="mana_text" src= "../static/img/U_mana.png"></span>')
      ability_line=ability_line.replace("{"+"W"+"}",'<span"><img class="mana_text" src= "../static/img/W_mana.png"></span>')
      ability_line=ability_line.replace("{"+"G"+"}",'<span"><img class="mana_text" src= "../static/img/G_mana.png"></span>')
      ability_line=ability_line.replace("{"+"C"+"}",'<span"><img class="mana_text" src= "../static/img/1_mana.png"></span>')
      
      for i in range(10):
        s = str(i)
        ability_line=ability_line.replace("{"+s+"}",'<span"><img class="mana_text" src= "../static/img/'+s+'_mana.png"></span>')
      adjusted_ability.append(ability_line)
   return adjusted_ability
