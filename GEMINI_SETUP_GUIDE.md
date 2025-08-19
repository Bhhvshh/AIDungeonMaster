# 🤖 Setting up Google Gemini API

Follow these steps to get your free Gemini API key and enable full AI functionality:

## Step 1: Get Your Free Gemini API Key

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. **Sign in**: Use your Google account to sign in

3. **Create API Key**: Click "Create API Key" button

4. **Copy Your Key**: Copy the generated API key (it starts with `AI...`)

## Step 2: Configure Your Environment

1. **Create .env file**: In your project folder, copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. **Add Your Key**: Open the `.env` file and replace `your_gemini_api_key_here` with your actual key:

   ```
   GEMINI_API_KEY=AIzaSyC-YourActualAPIKeyHere
   ```

3. **Save the file**: Make sure to save the `.env` file

## Step 3: Run the Game

```bash
python main.py
```

## ✅ You're All Set!

The game will now use Google's Gemini AI to create dynamic, intelligent stories for your adventures!

## 🆓 Free Tier Limits

- **Free API calls**: Generous free tier with 60 requests per minute
- **No credit card required**: Start playing immediately
- **Rate limits**: Sufficient for casual gaming

## 🔒 Security Note

- Never commit your `.env` file to version control
- Keep your API key private
- The `.env` file is already in `.gitignore`

Enjoy your AI-powered adventures! 🏰⚔️
