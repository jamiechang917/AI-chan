import gpt.main as gpt
import gpt.jp_translator as translator
import gpt.image_prompt_generator as img_promptor
import tts.koeiromap as tts
import imggen.main as img_gernerator
import emotion.emotion_classifier as emotion_classifier

from multiprocessing.pool import ThreadPool

if __name__ == '__main__':
    ai_chan = gpt.GPTClient()
    tts_service = tts.TTS()
    translate_service = translator.Translator()
    img_prompt_service = img_promptor.ImagePromptGenerator()
    img_generate_service = img_gernerator.ImageGenerator()
    
    
    while True:
        message = input("Enter your message: ")
        reply = ai_chan.chat(message)

        pool = ThreadPool(processes=4)
        translate_async = pool.apply_async(translate_service.translate, args=(reply,))
        img_prompt_async = pool.apply_async(img_prompt_service.get_image_prompt, args=(message, reply,))
        emotion_async = pool.apply_async(emotion_classifier.get_emotion, args=(reply,))

        jp_reply = translate_async.get()
        img_prompt = img_prompt_async.get()
        emotion = emotion_async.get()

        img_gen_async = pool.apply_async(img_generate_service.txt2img, args=(
            emotion + ", " + ", ".join(img_prompt) + "golden hair, ponytail, blue eye, cute, JK, high school, high resolution, best quality, extremely detailed CG, official art, detailed background,",
            "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, bad composition, inaccurate eyes, extra digit",
            "", )
        )
        tts_async = pool.apply_async(tts_service.say, args=(jp_reply, emotion,))
        img = img_gen_async.get()
        
        print(img_prompt)
        print(f"User: {message}\nAI-chan: {reply}\nAI-Chan(JP): {jp_reply}\nEmotion: {emotion}\nImage Prompt: {img_prompt}\n")
        img.show()