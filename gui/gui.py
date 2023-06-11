import customtkinter as ctk
from PIL import Image

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI-chan")
        self.geometry("800x600")
        self.resizable(False, False)
        self.image = Image.open(r"C:\Users\jamiechang917\Desktop\ai-chan\assets\image_placeholder.png")
        
        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
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
        self.image_box = ctk.CTkLabel(self, image=ctk.CTkImage(dark_image=self.image, size=(512, 512)), text="", anchor="nw")
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
        pass

    def talk_button_callbck(self):
        pass

    def update_chat(self, event):
        message = self.input_textbox.get()
        self.input_textbox.delete(0, "end")
        self.update_state_textbox("Hello", "Hi", "こんにちは", "Happy", "202")
        print(message)
        return

    def update_state_textbox(self, user_message, assistant_message, assistant_message_jp, emotions_prediction, used_tokens):
        state_text = f"User > {user_message}\nAI-chan > {assistant_message}\nAI-chan (JP) > {assistant_message_jp}\nEmotion: {emotions_prediction}\nUsed Tokens: {used_tokens}"
        self.state_textbox.configure(state="normal")
        self.state_textbox.delete("1.0", "end")
        self.state_textbox.insert("end", state_text)
        self.state_textbox.configure(state="disabled")




if __name__ == '__main__':
    app = App()
    app.mainloop()