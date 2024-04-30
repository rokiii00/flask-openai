import sys 
sys.dont_write_bytecode = True

def parse_SelectField_choices(form_prompt,default_choice):
    for prompt_key, prompt_value in form_prompt.choices:
        if prompt_key == form_prompt.data:
            return_value = prompt_value
            break
        # Test if basic_systemprompt has been assigned
    try:
        test = return_value
    except:
        return_value = "Professional"
    return return_value
        