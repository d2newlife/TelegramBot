# Duane's Professional AI Helper 🤖

A Telegram bot that serves as a professional AI assistant, designed to help users with various tasks through natural conversation. This bot is currently in development and ready for AI integration.

## 🌟 Features

- **Telegram Integration**: Seamless communication through Telegram messaging
- **Text Message Processing**: Handles incoming text messages and provides intelligent responses
- **Voice Message Support**: Downloads and processes voice messages (conversion to text ready for implementation)
- **Group Chat Support**: Welcomes users when added to groups and maintains conversation flow
- **Modular Architecture**: Clean separation of concerns with dedicated modules for different functionalities
- **Extensible Design**: Ready for AI/LLM integration to provide intelligent responses

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- Environment variables configuration

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/duane-ai-helper.git
   cd duane-ai-helper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
duane-ai-helper/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── util/                  # Utility modules
│   └── telegram.py        # Telegram API interactions
├── audio/                 # Voice message storage
└── venv/                  # Virtual environment
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather | ✅ Yes |

### Bot Token Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the provided token
4. Add it to your `.env` file

## 💻 Usage

### Starting the Bot

Once configured, run the bot with:
```bash
python main.py
```

The bot will:
- Connect to Telegram API
- Start polling for messages
- Process incoming text and voice messages
- Send appropriate responses

### Interacting with the Bot

- **Text Messages**: Send any text message to get a response
- **Voice Messages**: Send voice messages (currently downloads and saves audio files)
- **Group Chats**: Add the bot to groups for automated welcome messages

## 🛠️ Development

### Current Implementation

The bot currently handles:
- ✅ Text message reception and basic echo responses
- ✅ Voice message download and storage
- ✅ Group chat integration with welcome messages
- ✅ Error handling and logging
- ✅ Modular architecture for easy extension

### Planned Features

- 🔲 **AI Integration**: Connect to LLM services (OpenAI, Anthropic, etc.)
- 🔲 **Voice-to-Text**: Convert voice messages to text
- 🔲 **Contextual Responses**: Maintain conversation context
- 🔲 **Command System**: Add specific bot commands
- 🔲 **Database Integration**: Store user preferences and conversation history
- 🔲 **Multi-language Support**: Internationalization

### Adding AI Integration

The project is structured to easily add AI capabilities. The `util/llm.py` file is ready for implementation:

```python
# Example integration point in main.py
# Replace: reply_text = f"You said: {text}"
# With: reply_text = llm.generate_response(text)
```

## 🔍 Code Examples

### Basic Message Processing
```python
def process_updates(bot_token: str, updates: list) -> int:
    for update in updates:
        message = update.get('message')
        if message:
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            # Process text message
            if text:
                reply_text = f"You said: {text}"
                telegram.send_message(bot_token, chat_id, reply_text)
```

### Voice Message Handling
```python
elif voice:
    voice_audio_file = telegram.download_voice_message(bot_token, message)
    print(f"Voice message saved to: {voice_audio_file}")
    reply_text = "Voice messages are not supported yet."
    telegram.send_message(bot_token, chat_id, reply_text)
```

## 🧪 Testing

### Manual Testing
1. Start the bot
2. Send text messages to your bot on Telegram
3. Test voice message functionality
4. Add the bot to a group and test welcome messages

### Automated Testing
Consider adding unit tests for:
- Message processing logic
- Telegram API interactions
- Error handling scenarios

## 🚀 Deployment

### Local Deployment
The bot is designed to run locally or on a server with Python 3.7+ support.

### Cloud Deployment Options
- **Heroku**: Easy deployment with free tier available
- **AWS EC2**: Scalable cloud hosting
- **DigitalOcean**: Simple VPS deployment
- **Railway**: Modern cloud platform

### Production Considerations
- Use environment variables for sensitive data
- Implement proper logging
- Set up monitoring and alerting
- Consider using a process manager (PM2, systemd)
- Implement rate limiting for API calls

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## 🙏 Acknowledgments

- Telegram Bot API for messaging platform
- Python community for excellent libraries
- Contributors and testers

## 🔗 Links

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Python Telegram Bot Examples](https://github.com/python-telegram-bot/python-telegram-bot)
- [Project Repository](https://github.com/yourusername/duane-ai-helper)

*Last updated: October 2025*