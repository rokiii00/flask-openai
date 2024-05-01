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
                               choices=[('openai_expert', 'I am an expert in educational uses of ChatGPT for computer science'), 
                                        ('none', 'None.'), 
                                        ('student', 'I am a socially competent, 4th year university computer science student who uses ChatGPT'), 
                                        ('professor', 'I am an old computer science professor who is experimenting with ChatGPT'), 
                                        ('child','I am a 10 year old child who likes science'),
                                        ('humorous', 'I am a comedian'),
                                        ('poet', 'I am a poet'),
                                        ('elisa','Elisa DeFord. Elisa is a highly organized project manager and program developer with 15+ years of experience in higher education, specializing in student development, administration, and fundraising. She excels in managing projects efficiently and possess strong communication skills, enabling her to coach STEM students towards their goals and foster connections with alumni and employers. Outside of work, Elisa enjoys dog training, gardening, and aquarium keeping, showcasing her patient and nurturing personality.'),
                                        ('stephen','Stephen Smyth. Stephen is an excellent coder. He is a computer science student. He has built an AI teaching assistant using OpenAI apis'),
                                        ('mason','Mason Melead. Mason is the president of the university student chapter of ACM-AI. He has co-hosted several AI workshops for college students'),
                                        ('daryl','Daryl Cartwright. Daryl is an excellent coder.  She is a 4th year computer science student and a former highschool teacher.  She has built a web based vacation planning app using OpenAI apis')
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