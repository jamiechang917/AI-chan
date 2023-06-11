# Emotion classfication from text
# https://huggingface.co/bhadresh-savani/bert-base-uncased-emotion

from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

def predict(message, model='bhadresh-savani/bert-base-uncased-emotion') -> list:
    classifier = pipeline("text-classification", model=model, return_all_scores=True)
    prediction = classifier(message)[0]
    prediction = sorted(prediction, key=lambda x: x['score'], reverse=True)
    return prediction
    # [{'label': 'joy', 'score': 0.9972521662712097}, {'label': 'love', 'score': 0.000744332792237401}, {'label': 'anger', 'score': 0.0007404910866171122}, {'label': 'sadness', 'score': 0.0005138230626471341}, {'label': 'surprise', 'score': 0.0004197484813630581}, {'label': 'fear', 'score': 0.00032938504591584206}]

def get_emotion(message, model='bhadresh-savani/bert-base-uncased-emotion') -> str:
    prediction = predict(message, model)
    emotion = prediction[0]['label']
    # emotion in bert-base-uncased-emotion
    #   joy
    #   love
    #   anger
    #   sadness
    #   surprise
    #   fear

    # style in koeiromap TTS
    #   talk: 通常の話し声
    #   happy: 嬉しい
    #   sad: 悲しい
    #   angry: 怒った
    #   fear: 恐怖
    #   surprise: 驚いた
    if emotion == 'joy':
        emotion = 'happy'
    elif emotion == 'love':
        emotion = 'happy'
    elif emotion == 'anger':
        emotion = 'angry'
    elif emotion == 'sadness':
        emotion = 'sad'
    elif emotion == 'surprise':
        emotion = 'surprise'
    elif emotion == 'fear':
        emotion = 'fear'
    else:
        emotion = 'talk'
    return emotion


if __name__ == '__main__':
    print(predict('I love using transformers. The best part is wide range of support and its easy to use'))
