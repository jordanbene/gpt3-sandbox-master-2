"""Creates the Example and GPT classes for a user to interface with the OpenAI
API."""

import openai
import uuid
import sys
import re
import os 
import json 

messages_data_file = "../src/messagesData.json"
formatted_messages_file = "../src/new_messages.json"

def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key


class Example:
    """Stores an input, output pair and formats it to prime the model."""
    def __init__(self, inp, out):
        self.input = inp
        self.output = out
        self.id = uuid.uuid4().hex

    def get_input(self):
        """Returns the input of the example."""
        return self.input

    def get_output(self):
        """Returns the intended output of the example."""
        return self.output

    def get_id(self):
        """Returns the unique ID of the example."""
        return self.id

    def as_dict(self):
        return {
            "input": self.get_input(),
            "output": self.get_output(),
            "id": self.get_id(),
        }


class GPT:
    """The main class for a user to interface with the OpenAI API.

    A user can add examples and set parameters of the API request.
    """
    def __init__(self, 
                 engine='text-davinci-003',
                 temperature=0.5,
                 max_tokens=100,
                 input_prefix="input: ",
                 input_suffix="\n",
                 output_prefix="output: ",
                 output_suffix="\n\n",
                 append_output_prefix_to_query=False):
                 
        self.examples = {}
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens    
        self.input_prefix = input_prefix
        self.input_suffix = input_suffix
        self.output_prefix = output_prefix
        self.output_suffix = output_suffix
        self.append_output_prefix_to_query = append_output_prefix_to_query
        self.stop = (output_suffix + input_prefix).strip()
        

       
        
        self.logContext=True
        self.topic="Text Adventure Game: ZaugQuest"  # TODO: change it to your topic name, allow user to change this to change chat save name
        self.log_path='./history'
        self.current_context=""
        self.last_context=""
        self.full_context=""

        self.keep_context=True
        self.context_log = self.log_path + '/' + re.sub('[^0-9a-zA-Z]+', '', self.topic) + 'context_log.log'
        self.prompt_log = self.log_path + '/' + re.sub('[^0-9a-zA-Z]+', '', self.topic) + '_prompts.log'

        
        

    def add_example(self, ex):
        """Adds an example to the object.

        Example must be an instance of the Example class.
        """
        assert isinstance(ex, Example), "Please create an Example object."
        self.examples[ex.get_id()] = ex

    def delete_example(self, id):
        """Delete example with the specific id."""
        if id in self.examples:
            del self.examples[id]

    def get_example(self, id):
        """Get a single example."""
        return self.examples.get(id, None)

    def get_all_examples(self):
        """Returns all examples as a list of dicts."""
        return {k: v.as_dict() for k, v in self.examples.items()}

    def get_prime_text(self):
        """Formats all examples to prime the model."""
        return "".join(
            [self.format_example(ex) for ex in self.examples.values()])

    def get_engine(self):
        """Returns the engine specified for the API."""
        return self.engine

    def get_temperature(self):
        """Returns the temperature specified for the API."""
        return self.temperature

    def get_max_tokens(self):
        """Returns the max tokens specified for the API."""
        return self.max_tokens

    def write_logs(self, file_path, payload):
        file = open(file_path, "a")
        file.write(payload)
        file.close()

    def create_log_files(self):
        """Creates the log file if it doesn't already exist"""
        
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        if not os.path.isfile(self.context_log):
            open(self.context_log, 'w').close()
            
        if not os.path.isfile(self.prompt_log):
            open(self.prompt_log, 'w').close()
            print("Created log files: ", os.path.isfile(self.prompt_log), self.prompt_log)

    def clear_log(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write('') #clears the file by overwriting it with an empty string
            print(f'Successfully cleared log file at {file_path}')
        except Exception as e:
            print(f'An error occurred while clearing log file at {file_path}')
            print(e)
    def clear_json_file(self, file_path):
        with open(file_path, "w") as file:
            file.write("{}")
            
    def extract_log_text(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    def clear_all_logged_context(self):
        self.clear_log(self.context_log)
        self.clear_log(self.prompt_log)
        self.clear_json_file(formatted_messages_file)

        self.current_context=""
    

#where the query is actually crafted
    def craft_query(self, prompt):
        """Creates the query for the API request."""
        q = self.get_prime_text(
        ) + self.input_prefix + prompt + self.input_suffix
        
        if self.append_output_prefix_to_query:
            q = q + self.output_prefix
       
       
        if self.logContext:
            #clear log on start
            #self.clear_log(self.context_log)
            
            #print("Initial Query:  ", q + "   End of Query")

            #first create log files if there arent any
            self.create_log_files()
            
            #get the context from the log file
            log_text = self.extract_log_text(self.context_log)
            
            #append the context to the query
            q = log_text + q
            print("CURRENT CONTEXT: " + self.current_context + " END OF CONTEXT" + "   FULL CONTEXT:  ", self.full_context + "   End of Full Context:" + "Log Text:  ", log_text + "   End of Log Text"     )
            
        return q

    def submit_request(self, prompt):
        """Calls the OpenAI API with the specified parameters."""
        response = openai.Completion.create(engine=self.get_engine(),
                                            prompt=self.craft_query(prompt),
                                            max_tokens=self.get_max_tokens(),
                                            temperature=self.get_temperature(),
                                            top_p=1,
                                            n=1,
                                            stream=False,
                                            stop=self.stop)
        #print("GPT object created", response)

        #append the response to the prompt_log 
        self.write_logs(self.prompt_log, prompt + '\n')

        #append the response to the context_log
        #self.current_context = "Recent Story Context: " + prompt + response['choices'][0]['text'] + '\n'
        self.current_context = self.last_context + prompt + response['choices'][0]['text'] + '\n'
        self.full_context = "Recent Story Context: " + prompt + response['choices'][0]['text'] + '\n'
        self.last_context = prompt + response['choices'][0]['text'] + '\n'

        #write the context to the context_log
        self.write_logs(self.context_log, self.current_context)

        #print("Prompts: " + self.input_prefix + prompt + self.input_suffix)
        print("CONTEXT: " + self.current_context)

        # append the prompt to the Messages Data file
        self.write_message_to_file(prompt, 'true')
        self.write_message_to_file(response['choices'][0]['text'], 'false')

        messages = self.format_messagesdata()
        print(messages)
        self.write_to_json_new_messages(messages,formatted_messages_file )

        #add to front end log
        return response

    def write_message_to_file(self, message, is_user):
        print("PATH   ", messages_data_file)
        data = {"message": message, "isUser": is_user}
        with open(messages_data_file, "r") as f:
            messages = json.load(f)
        messages.append(data)
        with open(messages_data_file, "w") as f:
            json.dump(messages, f)

    def format_messagesdata(self):
        with open(messages_data_file, "r") as f:
            data = json.load(f)

        result = []
        for i, message_info in enumerate(data):
            result.append({"index": i + 1, "message": message_info["message"], "isUser": message_info["isUser"]})

        return result

    def write_to_json_new_messages(self, results, file_name):
        with open(file_name, 'w') as file:
            json.dump(results, file)
            

    def get_top_reply(self, prompt):
        """Obtains the best result as returned by the API."""
        response = self.submit_request(prompt)
        return response['choices'][0]['text']

    def format_example(self, ex):
        """Formats the input, output pair."""
        return self.input_prefix + ex.get_input(
        ) + self.input_suffix + self.output_prefix + ex.get_output(
        ) + self.output_suffix
    




    
