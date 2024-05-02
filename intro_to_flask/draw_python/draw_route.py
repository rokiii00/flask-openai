import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .draw_form import DrawmeForm
from ..utilities.form_parsing  import parse_SelectField_choices

draw_blueprint = Blueprint('drawme', __name__)

@draw_blueprint.route('/drawme',methods=['GET', 'POST'])
@app.route('/drawme',methods=['GET', 'POST'])
def drawme():
  form = DrawmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('drawme.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/api-reference/images
        client = OpenAI()


        response = client.images.generate(
          model="dall-e-3",
          prompt=form.prompt.data,
          quality=form.image_quality.data,
          size=form.image_size.data,
          n=1,
        )
        display_image_url = response.data[0].url
        revised_prompt=response.data[0].revised_prompt
        return render_template('drawme.html', draw_me_prompt=form.prompt.data,draw_me_response=display_image_url, draw_me_revised=revised_prompt,success=True)
      
  elif request.method == 'GET':
      return render_template('drawme.html', form=form)