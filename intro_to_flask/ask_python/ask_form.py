import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
class AskmeForm(Form):
    userprompt = TextAreaField("Your Question",  validators=[DataRequired()])
    basic_systemprompt = SelectField("Basic System Personalities", 
                               choices=[('none', 'None.'), 
                                        ('student', 'I am a 4th year university computer science student who uses ChatGPT'), 
                                        ('professor', 'I am a computer science professor who is experimenting with ChatGPT'), 
                                        ('child','I am a 10 year old child who likes science'),
                                        ('humorous', 'I am funny'),
                                        ('poet', 'I am a poet')
                                        ],
                               validators=[DataRequired()],
                               coerce=str)
    additional_systemprompt= TextAreaField("Additional System Personality Features")
    gpt_model = SelectField("OpenAI Model", 
                               choices=[('GPT-3.5 Turbo', 'gpt-3.5-turbo-0125'),
                                        ('GPT-4', 'gpt-4'),
                                        ('GPT-4 Turbo', 'gpt-4-turbo')
                                        ],
                               validators=[DataRequired()],
                               coerce=str)
    num_tokensprompt= IntegerField("Max number of response tokens", validators=[DataRequired()], default=150)
    submit = SubmitField("Send") 