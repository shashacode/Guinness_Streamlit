# 🍺 Guinness Selfie Generator - Streamlit App

Generate legendary selfies with Messi or Ronaldo while holding a pint of Guinness!
Link to access it: https://guinnessapp-hbwaslwcp6atedsvjr7aab.streamlit.app/

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your OpenRouter API Key

1. Visit [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up or log in
3. Create a new API key
4. Copy your API key

### 3. Run the App

```bash
streamlit run guinness_selfie_streamlit.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Key**: Paste your OpenRouter API key in the sidebar
2. **Configure Options**: Choose your footballer (Messi, Ronaldo, or Both) and style
3. **Upload Photo**: Upload a clear photo of yourself
4. **Generate**: Click "Generate Selfie" and wait 10-30 seconds
5. **Download**: Download your legendary selfie!

## ⚙️ Features

- ✨ Generate selfies with Messi, Ronaldo, or both
- 🎨 Multiple style options (Casual, Photorealistic, Cinematic, Professional)
- 📸 Easy photo upload
- 💾 Download generated images
- 📂 View generation history
- 🔒 Secure API key input

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash (via OpenRouter)
- **API**: OpenRouter (OpenAI SDK compatible)

## 💡 Tips

- Use clear, well-lit photos for best results
- Keep image size under 5MB
- Portrait orientation works best
- The AI preserves your face from the original photo

## 🐛 Troubleshooting

If generation fails:

1. **Check API Key**: Ensure your OpenRouter API key is valid
2. **Check Credits**: Verify you have credits/quota on OpenRouter
3. **Check Logs**: Visit [https://openrouter.ai/activity](https://openrouter.ai/activity) to see API logs
4. **Image Size**: Try a smaller image (< 5MB)
5. **Try Free Model**: Add `:free` to model name in the code for testing

## 📊 Cost

- The model used is `google/gemini-2.5-flash-image-preview`
- Check current pricing at [https://openrouter.ai/models](https://openrouter.ai/models)
- Free tier option available: `google/gemini-2.5-flash-image-preview:free`

## 🔗 Useful Links

- [OpenRouter Dashboard](https://openrouter.ai/)
- [API Keys](https://openrouter.ai/keys)
- [Usage Stats](https://openrouter.ai/activity)
- [Documentation](https://openrouter.ai/docs)

## 📝 License

This project is for educational and entertainment purposes.

---

Made with ❤️ using OpenRouter + Gemini 🍺⚽✨
