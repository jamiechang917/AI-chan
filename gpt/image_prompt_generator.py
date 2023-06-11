# Generate Stable Diffusion prompt from messages

import openai
import ast

openai.api_key = '## YOUR OPENAI API KEY ##'

class ImagePromptGenerator:
    def __init__(self) -> None:
        self.system_prompt = """
        Now you are going to generate keywords from the sentences for image-generation. These keywords describe the scenario for the given sentence. For example, you receive a inputs like
        ['user': 'what is your favorite festival?', 'assistant': 'I like Christmas. I was wearing the Santa's clothes and hanging out with my friend last year.']. Then you output ['Christmas', 'Santa's clothes', 'with friends', 'shopping'] in Python style list. 
        """
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": ""}]
    def get_image_prompt(self, user_message, assistant_message) -> list:
        self.messages[1] = {"role": "user", "content": f"['user': '{user_message}', 'assistant': '{assistant_message}'"}
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=1.0,
                max_tokens=2048, # max 4096
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                messages=self.messages,
            )
            reply = response["choices"][0]["message"]["content"] # string
            try:
                reply = ast.literal_eval(reply)
            except:
                print("image_prompt_generator.py: get_image_prompt: ast.literal_eval(reply) failed.")
                reply = []
            return reply
            
        except openai.error.RateLimitError:
            return "Rate limit exceeded, please wait a few minutes and try again."
        
    
if __name__ == "__main__":
    prompt_generator = ImagePromptGenerator()
    while True:
        usr_message = input("Enter your user message: ")
        assistant_message = input("Enter your assistant message: ")
        reply = prompt_generator.get_image_prompt(usr_message, assistant_message)
        print(f"User: {usr_message}\nAssistant: {assistant_message}\nKeywords: {reply[0]}\n")
        print(reply)