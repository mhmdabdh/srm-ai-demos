import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
warnings.filterwarnings("ignore", category=DeprecationWarning)


from google import genai

# The client will automatically pick up the API key from the
# environment variable 'GEMINI_API_KEY'
client = genai.Client(api_key="put the api key here")

# Choose a model, e.g., 'gemini-2.5-flash' for general tasks
model = "gemini-2.5-flash"

# Make a request to generate content
response = client.models.generate_content(
    model=model,
    contents="""Tell me in 150 words about Computer Sciences Faculty in SRM Institute of Science and Technology at Tiruchirappalli. Please mention details of any three professors of this department in Tiruchirappalli"""
)

# Print the model's response text
print(response.text)
