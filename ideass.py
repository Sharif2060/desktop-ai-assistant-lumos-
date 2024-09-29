from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

def integrate_hugging_face_tensorflow(query):
    model_name = "facebook/blenderbot-400M-distill"  # TensorFlow equivalent
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Tokenize the input query
    inputs = tokenizer(query, return_tensors="tf")
    
    # Generate the response
    reply_ids = model.generate(**inputs)
    response = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    
    return response

# Example usage
user_query = "Tell me about Virat Kohli"
response = integrate_hugging_face_tensorflow(user_query)
print("AI Assistant says:", response)
