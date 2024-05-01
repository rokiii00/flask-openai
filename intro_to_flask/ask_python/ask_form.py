import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
class AskmeForm(Form):
    userprompt = TextAreaField("Your Question",  validators=[DataRequired()])
    systemprompt= TextAreaField("System Personality", validators=[DataRequired()])
    num_tokensprompt= IntegerField("Max number of response tokens", validators=[DataRequired()])
    submit = SubmitField("Send") 