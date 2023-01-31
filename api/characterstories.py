import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(sys.path.append(os.path.dirname(os.path.realpath(__file__))))
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from api.gpt import GPT, Example
from api import UIConfig, master_prompt_loader
#UIConfig, master_prompt_loader
#from api import GPT, Example, UIConfig, master_prompt_loader
from api import demo_web_app

text = master_prompt_loader.get_master_prompt("ZaugQuest")
session_prompt = text + "\n"
start_sequence = "\n:"
restart_sequence = "\n\n"

question_prefix =  'Player: '
question_suffix = "\n"
answer_prefix = session_prompt + "Adim Dungeon Master: "
answer_suffix = "\n\n"



# Construct GPT object and show some examples
gpt = GPT(engine="text-davinci-003",
          temperature=0.8,
          max_tokens=100,
          input_prefix=question_prefix,
          input_suffix=question_suffix,
          output_prefix=answer_prefix,
          output_suffix=answer_suffix,
          append_output_prefix_to_query=True
          
          )

gpt.add_example(Example('I look around',
                        'To the north is {insert an event}, to the south is {insert an event}, to the east is {insert an event} and to the west {insert an event}. What do you do? '))


# Define UI configuration
config = UIConfig(description="Input",
                  button_text="Continue",
                  placeholder="What do you do?")




demo_web_app(gpt, config)
