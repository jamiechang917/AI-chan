import gpt.main as gpt
import gpt.jp_translator as translator
import gpt.image_prompt_generator as img_promptor
import imggen.main as img_gernerator
import tts.koeiromap as tts
import emotion.emotion_classifier as emotion_classifier

from multiprocessing.pool import ThreadPool
import customtkinter as ctk
from PIL import Image


ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

IMGSIZE = (548, 412)

class App(ctk.CTk):
    def __init__(self, ai_client, tts_client, translator_client, img_prompt_client, img_generation_client):
        super().__init__()
        self.ai_client = ai_client
        self.tts_client = tts_client
        self.translator_client = translator_client
        self.img_prompt_client = img_prompt_client
        self.img_generation_client = img_generation_client
        
        self.user_message_history = []
        self.assistant_message_history = []

        self.title("AI-chan")
        self.geometry("800x600")
        self.resizable(False, False)
        self.image = Image.open(r"C:\Users\jamiechang917\Desktop\ai-chan\assets\image_placeholder.png")

        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # UI elements
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_button_callbck, width=20)
        self.play_button = ctk.CTkButton(self, text="Play", command=self.play_button_callbck, width=20)
        self.talk_button = ctk.CTkButton(self, text="Talk", command=self.talk_button_callbck, width=20)
        self.input_textbox = ctk.CTkEntry(self, placeholder_text="Enter your message here")
        self.history_textbox = ctk.CTkTextbox(self)
        self.state_textbox = ctk.CTkTextbox(self, state="disabled", font=('Helvetica', 14))
        self.image_box = ctk.CTkLabel(self, image=ctk.CTkImage(dark_image=self.image, size=IMGSIZE), text="", anchor="nw")
        self.logo_label = ctk.CTkLabel(self, text="AI-chan", font=('Helvetica', 20), anchor="center")
        
        self.send_button.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=10, pady=10)
        self.input_textbox.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)
        self.history_textbox.grid(row=0, column=2, rowspan=3, sticky="nsew", padx=10, pady=5)
        self.state_textbox.grid(row=1, column=0, columnspan=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.play_button.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=10, pady=10)
        self.talk_button.grid(row=2, column=1, columnspan=1, sticky="nsew", padx=10, pady=10)
        self.image_box.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.logo_label.grid(row=3, column=2, columnspan=1, sticky="nsew", padx=10, pady=5)

        # Bindings
        self.input_textbox.bind("<Return>", self.update_chat)
        # self.image_box.bind("<Configure>", self._resize_image)

    def send_button_callbck(self):
        # print(self.image_box.winfo_width(), self.image_box.winfo_height())
        self.update_chat(None)
    
    def play_button_callbck(self):
        # print(self.image_box.winfo_width(), self.image_box.winfo_height())
        self.tts_client.play()
        pass

    def talk_button_callbck(self):
        pass

    def update_chat(self, event):
        message = self.input_textbox.get()
        reply = self.ai_client.chat(message)

        # update history
        self.user_message_history.append(message)
        self.assistant_message_history.append(reply)

        # multithreading
        pool = ThreadPool(processes=4)
        translator_client_async = pool.apply_async(self.translator_client.translate, args=(reply,))
        img_prompt_client_async = pool.apply_async(self.img_prompt_client.get_image_prompt, args=(message, reply,))
        emotion_classifier_async = pool.apply_async(emotion_classifier.get_emotion, args=(reply,))

        # get results
        reply_jp = translator_client_async.get()
        print("Translation done")
        img_prompt = img_prompt_client_async.get()
        print("Image prompt done")
        emotion = emotion_classifier_async.get()
        print("Emotion done")

        # generate image and voice
        img_generation_client_async = pool.apply_async(self.img_generation_client.txt2img, args=(
            emotion + ", " + ", ".join(img_prompt) + "golden hair, ponytail, blue eye, cute, JK, high school, high resolution, best quality, extremely detailed CG, official art, detailed background,",
            "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, bad composition, inaccurate eyes, extra digit",
            "", )
        )
        tts_client_async = pool.apply_async(self.tts_client.say, args=(reply_jp, emotion,))

        # get results
        self.image = img_generation_client_async.get()
        print("Image generation done")
        # self.image.show()
        

        # update UI
        self.input_textbox.delete(0, "end")
        self.update_state_textbox(message, reply, reply_jp, emotion, img_prompt)
        self.update_history_textbox()
        self.image_box.configure(image=ctk.CTkImage(dark_image=self.image, size=IMGSIZE))
        
        return

    def update_state_textbox(self, user_message, assistant_message, assistant_message_jp, emotions_prediction, img_prompt):
        cost = self.ai_client.used_tokens / 1000 * 0.002 * 30.67
        total_cost = self.ai_client.used_total_tokens / 1000 * 0.002 * 30.67
        state_text = f"User > {user_message}\nAI-chan > {assistant_message}\nAI-chan (JP) > {assistant_message_jp}\nEmotion: {emotions_prediction}\nImage Prompt: {img_prompt}\nUsed Tokens: {self.ai_client.used_tokens} (TWD: {cost:.3f}), Total Used Tokens: {self.ai_client.used_total_tokens} (TWD: {total_cost:.3f})"
        self.state_textbox.configure(state="normal")
        self.state_textbox.delete("1.0", "end")
        self.state_textbox.insert("end", state_text)
        self.state_textbox.configure(state="disabled")

    def update_history_textbox(self):
        history_text = ""
        for i in range(len(self.user_message_history)):
            history_text += f"User > {self.user_message_history[i]}\nAI-chan > {self.assistant_message_history[i]}\n\n"
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        self.history_textbox.insert("end", history_text)
        self.history_textbox.configure(state="disabled")
        # move scrollbar to bottom
        self.history_textbox.see("end")




if __name__ == '__main__':
    print("Initializing AI-chan...")

    ai_client = gpt.GPTClient()
    tts_client = tts.TTS()
    translator_client = translator.Translator()
    img_prompt_client = img_promptor.ImagePromptGenerator()
    img_generation_client = img_gernerator.ImageGenerator()

    app = App(ai_client, tts_client, translator_client, img_prompt_client, img_generation_client)
    app.mainloop()