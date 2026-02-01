import gradio as gr
from transformers import pipeline

# Load ViT model trained for age classification
pipe = pipeline("image-classification", model="nateraw/vit-age-classifier")

def predict(image):
    try:
        results = pipe(image)
        result = results[0]  # top prediction
        label = result["label"]
        score = result["score"]
        return f"Predicted Age Range: {label}\nConfidence: {score:.2%}"
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Face Age Estimation",
    description="Upload a face image to predict age range using a ViT age classifier."
)

demo.launch()