from huggingface_hub import InferenceClient
import traceback

MODEL = "HuggingFaceH4/zephyr-7b-beta"
TOKEN = "insert_your_HF_token"  # Replace with your real key

print("🚀 Starting Hugging Face connection test...")

try:
    client = InferenceClient(model=MODEL, token=TOKEN)

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain what Kubernetes is in one paragraph."}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.7,
    )

    print("\n✅ Response from Hugging Face:\n")
    print(response.choices[0].message["content"])

except Exception as e:
    print("❌ Error during API request:")
    traceback.print_exc()
