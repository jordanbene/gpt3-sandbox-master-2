"""Runs the web app given a GPT object and UI configuration."""

from http import HTTPStatus
import json
import subprocess
import openai

from flask import Flask, request, Response, jsonify

from api.gpt import set_openai_key, Example
from api.ui_config import UIConfig

from dotenv import load_dotenv
import os

load_dotenv()

#CONFIG_VAR = "OPENAI_CONFIG"
#KEY_NAME = "OPENAI_KEY"
KEY_NAME = os.getenv("OPENAI_KEY") #env variable instead of public so it doesn't get published on deplpoy


def demo_web_app(gpt, config=UIConfig(), starting_prompt=" "):
    """Creates Flask app to serve the React app."""
    app = Flask(__name__)
    
    #app.config.from_envvar(CONFIG_VAR)
    #set_openai_key(app.config[KEY_NAME])
    set_openai_key(KEY_NAME)
    
        
    @app.route("/params", methods=["GET"])
    def get_params():
        # pylint: disable=unused-variable
        response = config.json()
        return response

    def error(err_msg, status_code):
        return Response(json.dumps({"error": err_msg}), status=status_code)

    def get_example(example_id):
        """Gets a single example or all the examples."""
        # return all examples
        if not example_id:
            return json.dumps(gpt.get_all_examples())

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)
        return json.dumps(example.as_dict())

    def post_example():
        """Adds an empty example."""
        new_example = Example("", "")
        gpt.add_example(new_example)
        return json.dumps(gpt.get_all_examples())

    def put_example(args, example_id):
        """Modifies an existing example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)

        if "input" in args:
            example.input = args["input"]
        if "output" in args:
            example.output = args["output"]

        # update the example
        gpt.add_example(example)
        return json.dumps(example.as_dict())

    def delete_example(example_id):
        """Deletes an example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        gpt.delete_example(example_id)
        return json.dumps(gpt.get_all_examples())

    def prompt_openai_naked(prompt):
        """Prompts OpenAI without any formatting."""
        response = openai.Completion.create(
            engine=config.engine,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            prompt=prompt,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            #stop=["\n", " Human:", " AI:"],
        )
        return response

    def prompt_openai(prompt):
        #request.json[prompt]
        response = gpt.submit_request(prompt)
        offset = 0
        if not gpt.append_output_prefix_to_query:
            offset = len(gpt.output_prefix)
        return {'text': response['choices'][0]['text'][offset:]}
    
    #with app.test_request_context():
        #response = prompt_openai(starting_prompt)

    @app.route(
        "/examples",
        methods=["GET", "POST"],
        defaults={"example_id": ""},
    )
    @app.route(
        "/examples/<example_id>",
        methods=["GET", "PUT", "DELETE"],
    )
    def examples(example_id):
        method = request.method
        args = request.json
        if method == "GET":
            return get_example(example_id)
        if method == "POST":
            return post_example()
        if method == "PUT":
            return put_example(args, example_id)
        if method == "DELETE":
            return delete_example(example_id)
        return error("Not implemented", HTTPStatus.NOT_IMPLEMENTED)

    @app.route("/translate", methods=["GET", "POST"])
    def translate():
        # pylint: disable=unused-variable
        prompt = request.json["prompt"]
        response = gpt.submit_request(prompt)
        offset = 0
        if not gpt.append_output_prefix_to_query:
            offset = len(gpt.output_prefix)
        return {'text': response['choices'][0]['text'][offset:]}
   
    @app.route("/clear-history", methods=['POST'])
    def clear_history():
        with open('../src/messagesData.json', 'w') as json_file:
            json.dump([{"message": "Adim AI loading...\n Welcome to Zaug Quest! This is a game of freedom, chaos, and Joy-Slaying fun! Play as Zaug, the Dark Lord Prince as he battles his way across Kadarz. Use your imagination to procceed.","isUser": "false"}], json_file)
            gpt.clear_all_logged_context() 
        #return jsonify({"message": "History cleared"})

    subprocess.Popen(["yarn", "start"], shell=True)
    
    #app.run()#host='0.0.0.0', port=5000
    #app.run(host='0.0.0.0', port=5000)

