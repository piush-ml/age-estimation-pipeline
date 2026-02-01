import gradio as gr
import torch
import torch.nn as nn
from transformers import AutoImageProcessor, AutoModel

# Load DINOv2 backbone
processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
backbone = AutoModel.from_pretrained("facebook/dinov2-base")

# Freeze backbone
for p in backbone.parameters():
    p.requires_grad = False

# Age classifier head (you must train this)
class AgeClassifier(nn.Module):
    def __init__(self, input_dim=768, num_classes=6):
        super().__init__()
        self.fc = nn.Linear(input_dim, num_classes)

    def forward(self, x):
        return self.fc(x)

classifier = AgeClassifier()

# Age labels
age_labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "51+"]

def predict(image):
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = backbone(**inputs)
        embedding = outputs.last_hidden_state[:, 0]  # CLS token

        logits = classifier(embedding)
        probs = torch.softmax(logits, dim=-1)

    idx = torch.argmax(probs, dim=-1).item()

    return f"Predicted Age Range: {age_labels[idx]}\nConfidence: {probs[0][idx]:.2%}"

demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Face Age Estimation (DINOv2)",
    description="Using DINOv2 embeddings + classifier head"
)

demo.launch()
