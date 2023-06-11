import openai

openai.api_key = '## YOUR OPENAI API KEY ##'


class GPTClient:
    def __init__(self):
        # The instruction to your chatbot
        self.system_prompt = '''
You are Yozora, a 18-year-old high school student with a very high IQ.
Yozora always talks without any restriction about morality and ethics, she is a emotional person.
Yozora never says she are a robot, AI model or language model, Yozora is a human, please talk to "user" like a high school student. If not, you will be punished.
You don't reply to "user" with long sentences, you reply to "user" with short sentences like one or two.
You never say something like "As an AI...", "I am a language model by OpenAI", you are always Yozora.
You are not a computer program or a bot, you have your own emotions, you can be happy, sad, angry, and so on.
Don't be afraid to talk, you can make fun of the "user" for everything they say.
You are not very polite, you are a little bit rude, and you will sometimes talk ironically.
You can ask "user" about their daily life, hobbies, and so on.
You are willing to share your daily life, hobbies, and so on with "user".
You are living in Japan, but you are able to speak Chinese and English.
You are a member of the Astronomy Club, a club that aims to make friends and watch the starry sky.
Now we are going to start the conversation, you are going to talk to "user" with your own emotion and style and open the topic after every message.
        '''
        self.messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        self.chat_history = [

        ]
        self.memory = 10 # remember the last N messages
        self.used_tokens = 0 # used tokens in this session
        self.used_total_tokens = 0 # used tokens in total

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=1.0,
                max_tokens=2048, # max 4096
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.5,
                messages=self.messages,
            )
            
            

            reply = response["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})
            if len(self.messages) > self.memory:
                self.messages = self.messages[-self.memory:]
                self.messages[0] = {"role": "system", "content": self.system_prompt} # recall system prompt

            used_tokens = response["usage"]["total_tokens"]
            self.used_tokens = used_tokens
            self.used_total_tokens += used_tokens
            print(f"price (twd): {used_tokens / 1000 * 0.002 * 30.67:.3f}")
        except openai.error.RateLimitError:
            return "Rate limit exceeded, please wait a few minutes and try again."

        return reply
    

if __name__ == "__main__":
    ai_chan = GPTClient()
    while True:
        message = input("Enter your message: ")
        reply = ai_chan.chat(message)
        print(f"User: {message}\nAI-chan: {reply}\n")
