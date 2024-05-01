import os
import random
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint,send_from_directory, url_for
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

        response = client.audio.speech.create(
          model="tts-1",
          voice="alloy",
          input=response.choices[0].message.content,
        )
        response.stream_to_file(speech_file_path)
        speech_url = url_for('temp.gettempfile', filename=speech_file_name)

        print(speech_url) 

        return render_template('askme.html', ask_me_prompt=form.userprompt.data,ask_me_response=display_text,ask_me_audio=speech_url,success=True)
      
  elif request.method == 'GET':
      return render_template('askme.html', form=form)