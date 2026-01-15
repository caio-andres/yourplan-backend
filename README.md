> YourPlan Back-end 😼

## Getting Started to the application

**1.** Create your `API Key` with Gemini at https://aistudio.google.com/api-keys.

**2.** Rename .env.example to .env `only`. Then, assign your API Key value created in Google AI Studio to the following varibale:

```env
GOOGLE_GEMINI_API_KEY=add_your_api_key_here
```

**3.** Generate the binary files of `knowledge source` running the following command in your terminal:

```bash
python -m src.genai.rag.create_load_index
```

> ℹ️ Once you ran, it will create. Then, it will just load.
