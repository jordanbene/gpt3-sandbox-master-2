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
session_prompt = str(text) + "\n"
start_sequence = "\n:"
restart_sequence = "\n\n"

question_prefix =  'Player: '
question_suffix = "\n"
answer_prefix = session_prompt + "Adim Dungeon Master: "
answer_suffix = "\n\n"



# Construct GPT object and show some examples
gpt = GPT(engine="text-davinci-003",
          temperature=0.8,
          max_tokens=200,
          input_prefix=question_prefix,
          input_suffix=question_suffix,
          output_prefix=answer_prefix,
          output_suffix=answer_suffix,
          append_output_prefix_to_query=True
          
          )


gpt.add_example(Example('I jump over the spikes and enter the castle',
'The spikes are too high to jump over. You can try to find another way into the castle or choose another direction to go. What do you do? '))

gpt.add_example(Example('What commands can I use?','The commands available to you are: Do - to do an action. Look - to look around your environment. Move (place) - to go somewhere within the enviorment. Fight - to engage in combat with an enemy. Flee - to run away from an enemy. Inventory - to view the items in your inventory. Use - to use an item in your inventory or environment. Pick Up - to pick up an item. '))

gpt.add_example(Example('I explore the ruined tower',
'As you approach the ruined tower, you see that it is unstable and could collapse at any moment. Do you want to enter the tower or choose another direction to go? '))

gpt.add_example(Example('How many pieces of the Chronus sword are in my inventory?','Youve collected one piece of the Chronus Sword.'))
# Define UI configuration
config = UIConfig(description="Input",
                  button_text="Continue",
                  placeholder="What do you do?")



demo_web_app(gpt, config, "What commands can I use?")
