import re
import nltk
import tensorflow as tf
from nltk.corpus import stopwords
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.saving import register_keras_serializable
from transformers import TFAutoModel, AutoTokenizer

nltk.download("stopwords")

MAX_LENGTH = 64
MODEL_NAME = r"sentence-transformers/paraphrase-mpnet-base-v2"
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
PRETRAINED_MODEL = TFAutoModel.from_pretrained(MODEL_NAME)

# Normalize Text
def normalize_text(text):
    text = text.lower()
    text = text.strip() 
    text = re.sub(r'[^\w\s\n]', '', text)
    text = text.replace('\n\n', '\n')
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
 
    return text

# Tokenizer the input
def encode_text(text, max_length = MAX_LENGTH):
    encoding = TOKENIZER(
        normalize_text(str(text)),
        padding = 'max_length',          # Pad to the longest sequence in the batch
        truncation = True,       # Truncate sequences if they are longer than the model's max length
        return_tensors = "tf",    # Return TensorFlow tensors
        max_length = max_length,
    )
    return encoding

# Build model
@register_keras_serializable()
class EncodingModel(Model):
    def __init__(self, hidden_size = 128, **kwargs):
        super(EncodingModel, self).__init__()
        self.pretrained_model = PRETRAINED_MODEL
        self.ave = layers.GlobalAveragePooling1D()
        self.fc = layers.Dense(hidden_size, activation = 'gelu')
    
    def __call__(self, inputs):    
        location_input, description_input = str(inputs["location"]), str(inputs["description"])
                
        location_x = encode_text(location_input, 13)
        description_x = encode_text(description_input)
        
        location_x = self.pretrained_model(location_x).last_hidden_state
        description_x = self.pretrained_model(description_x).last_hidden_state
        
        location_x = self.ave(location_x)
        description_x = self.ave(description_x)
        
        location_output = self.fc(location_x)
        description_output = self.fc(description_x)
        return (location_output, description_output)
    
    def get_config(self):  # Add get_config to save model configuration
        config = super(EncodingModel, self).get_config()
        config.update({
            "hidden_size": self.fc.units,
            "pretrained_model": self.pretrained_model  # Ensure pretrained model can be handled
        })
        return config

    @classmethod
    def from_config(cls, config):
        hidden_size = config.pop("hidden_size", 128)
        pretrained_model = config.pop("pretrained_model", None)  # Adjust as needed
        return cls(pretrained_model=pretrained_model, hidden_size=hidden_size, **config)

def load_model(MODEL_FILE, WEIGHTS_FILE):
    model = tf.keras.models.load_model(
        MODEL_FILE,
        custom_objects = {"EncodingModel": EncodingModel})

    dummy_input = {"location": "dummy_location", "description": "dummy_description"}
    model.build(input_shape = {"location": (None, 1), "description": (None, 1)})
    test = model(dummy_input)  # Initialize the model state

    model.load_weights(WEIGHTS_FILE)
    return model