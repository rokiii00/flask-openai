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
from ..utilities.form_parsing  import parse_SelectField_choices

ask_blueprint = Blueprint('askme', __name__)

@ask_blueprint.route('/askme',methods=['GET', 'POST'])
@app.route('/askme',methods=['GET', 'POST'])
def askme():
  form = AskmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('askme.html', form=form)
      else:

        client = OpenAI()
        
        # Find the selected basic_systemprompt
        basic_systemprompt = parse_SelectField_choices(form.basic_systemprompt,"Professional")
        system_personality = basic_systemprompt + ". " + form.additional_systemprompt.data
        
        # Find the selected gpt model
        gpt_model = parse_SelectField_choices(form.gpt_model,"gpt-4-turbo")

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
        return render_template('askme.html', ask_me_prompt=form.userprompt.data,ask_me_response=display_text,success=True)
      
  elif request.method == 'GET':
      return render_template('askme.html', form=form)