import os
import random
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .ask_form import AskmeForm

ask_blueprint = Blueprint('askme', __name__)

@ask_blueprint.route('/askme',methods=['GET', 'POST'])
@app.route('/askme',methods=['GET', 'POST'])
def askme():
  form = AskmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('askme.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/api-reference/chat/create
        client = OpenAI()
        # Find the selected basic_systemprompt
        for prompt_key, prompt_value in form.basic_systemprompt.choices:
          if prompt_key == form.basic_systemprompt.data:
            basic_systemprompt = prompt_value
            break
        # Test if basic_systemprompt has been assigned
        try:
          test = basic_systemprompt
        except:
          basic_systemprompt = "Professional"
        # Concatentate the basic_systemprompt and the additonal_systemprompt
        system_personality = basic_systemprompt + ". " + form.additional_systemprompt.data
        
        # Find the selected gpt model
        for model_key, model_value in form.gpt_model.choices:
          if model_key == form.gpt_model.data:
            gpt_model = model_value
            break
        # Test if gpt_model has been assigned
        try:
          test = gpt_model
        except:
          gpt_model = "gpt-4-turbo"
        
        # Get the response to the prompts
        response = client.chat.completions.create(
          model=gpt_model,
          messages=[
              {"role": "system", "content": system_personality},
              {"role": "user", "content": form.userprompt.data}
            ],
          max_tokens=form.num_tokensprompt.data
        #  stop=["."]
        )
        # Retrieve the text of the response
        display_text = response.choices[0].message.content
        
        # Convert the response text into audio
        speech_file_name = "askme_response.mp3"
        speech_file_path = os.path.join("intro_to_flask/temp/",speech_file_name)

        display_text = response.choices[0].message.content
        return render_template('askme.html', ask_me_prompt=form.prompt.data,ask_me_response=display_text,success=True)
      
  elif request.method == 'GET':
      return render_template('askme.html', form=form)