import time
from google import genai
from google.auth import default

# Sử dụng Application Default Credentials
credentials, project = default()

client = genai.Client(
    vertexai=True,
    project="cosmic-attic-473011-m8",
    credentials=credentials
)

print("="*60)
print("🔬 DEEP RESEARCH WITH ADC")
print("="*60)

# Deep Research yêu cầu background=True
interaction = client.interactions.create(
    input="Research the latest trends in AI in 2025",
    agent="deep-research-preview-04-2026",
    background=True,
)

print(f"Research started: {interaction.id}")

while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print("\n✅ Research completed!")
        print(interaction.output_text)
        break
    elif interaction.status == "failed":
        print(f"Failed: {interaction.error}")
        break
    print("In progress...")
    time.sleep(10)
