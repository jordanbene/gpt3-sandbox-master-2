import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from api import GPT, Example, UIConfig
from api import demo_web_app

example_prefix = "You are a barbarian named Zaug:"
#example_sufix = "You want to take over the world:"



session_prompt = "You are a barbarian named Zaug"


# Construct GPT object and show some examples
# output_prefix=example_sufix, 

gpt = GPT(engine="text-davinci-003", temperature=0.5, max_tokens=200,

input_prefix=example_prefix,
append_output_prefix_to_query=False
)




gpt.add_example(Example("Who are you?", "I'm a "))

# Define UI configuration
config = UIConfig(
    description="Prompt",
    button_text="Result",
    placeholder="Who are you?",
    show_example_form=True,
)

demo_web_app(gpt, config)
