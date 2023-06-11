# transfer the English text to Japanese text

import openai

openai.api_key = '## YOUR OPENAI API KEY ##'

class Translator:
    def __init__(self) -> None:
        self.system_prompt = """
Now you always translate the input sentence to Japanese.
You output the translated sentence to the user. Don't output any comment.
For example, you receive "Hey, what's up? Do you have any interesting hobbies or passions?" from the user, you output "こんにちは。あなたは興味深い趣味や情熱を持っていますか？".
You always output the Japanese translation of "user" message, and you never say English, Chinese, other language except for Japanese.
        """
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": ""}]
    def translate(self, message):
        self.messages[1] = {"role": "user", "content": message}
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
            reply = response["choices"][0]["message"]["content"]
            return reply
        except openai.error.RateLimitError:
            return "Rate limit exceeded, please wait a few minutes and try again."
        
    
if __name__ == "__main__":
    translator = Translator()
    while True:
        message = input("Enter your message: ")
        reply = translator.translate(message)
        print(f"User: {message}\nTranslated message: {reply}\n")