import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from api import GPT

master_prompts_path = os.getcwd() + "/master_prompt.json"

def load_json(file_path):
    try_load_json( file_path)
    with open(file_path, 'r') as json_file:
        prompts = json.load(json_file)
    return prompts
    
def store_master_prompt( character, prompt):
        
    prompts = load_json(master_prompts_path)
    prompts[character] = prompt
    with open(master_prompts_path, 'w') as json_file:
        json.dump(prompts, json_file)


def get_master_prompt(character):
    prompts = load_json( master_prompts_path)
    return prompts.get(character)

def try_load_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open(file_path, "w") as f:
            json.dump(data, f)