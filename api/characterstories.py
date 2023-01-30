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
answer_prefix = session_prompt + "Adim - Dungeon Master: "
answer_suffix = "\n\n"



# Construct GPT object and show some examples
gpt = GPT(engine="text-davinci-003",
          temperature=0.5,
          max_tokens=100,
          input_prefix=question_prefix,
          input_suffix=question_suffix,
          output_prefix=answer_prefix,
          output_suffix=answer_suffix,
          append_output_prefix_to_query=True
          
          )

gpt.add_example(Example('I try to open the door.',
                        'The door opens to reveal a dimly lit room with a single table. There is a note on the table.'))


# Define UI configuration
config = UIConfig(description="Input",
                  button_text="Continue",
                  placeholder="What do you do?")




demo_web_app(gpt, config)
