# mAgIc The Hazarding

## Overview
This is a simple Python Flask web application which connects with OpenAI APIs to create 'Magic The Gathering' like cards.
'Hazarding', in the project name, refers to a joke with the fact tha A.I. accomplishments can be scary, treathening, but facinating at the same time.


![Screenshot](path/to/screenshot.png)

## Prerequisites
You will need :
- Python 3.12
- MongoDB: Any instance of MongoDB running locally or remote. You can specificy the connection URL in the config file.
- A valid API key from OpenAI (you can get one from your account settings: https://platform.openai.com/account/api-keys)

## Getting Started
1. Clone the repository: `git clone https://github.com/coelhofb/mtg_openai.git`
2. Navigate to the project directory: `cd mtg_openai`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure the application:
   - check the DOT_ENV file and fill in the necessesary information.
   - You will create a copy of that file and will save as '.env' in the root folder of the cloned repo. 

## Running the Application
```bash
flask run
````
Visit http://localhost:5000 in your web browser.
