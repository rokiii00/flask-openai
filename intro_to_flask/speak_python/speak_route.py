import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint, Response
from .speak_form import SpeakmeForm

speak_blueprint = Blueprint('speakme', __name__)

@speak_blueprint.route('/speakme',methods=['GET', 'POST'])
@app.route('/speakme',methods=['GET', 'POST'])
def speakme():
  form = SpeakmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('speakme.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/api-reference/images
        client = OpenAI()
        
        speech_file_name = "createspeech.mp3"
        speech_file_path = "intro_to_flask/static/" + speech_file_name

        response = client.audio.speech.create(
          model="tts-1",
          voice="alloy",
          input=form.prompt.data,
        )
        response.stream_to_file(speech_file_path)

        return render_template('speakme.html', speak_me_prompt=form.prompt.data,speak_me_response=speech_file_name,success=True)
      
  elif request.method == 'GET':
      return render_template('speakme.html', form=form)