# Telegram Chat Bot

## Description
This project implements a chatbot for Telegram that processes user queries, makes decisions based on functional rules, and generates appropriate responses. The bot provides functionalities related to weather information and currency exchange rates.

## Features
- **User Interaction**: Engages with users through text messages, commands, and responses.
- **Weather Information**: Retrieves current weather data for a specified city using the OpenWeatherMap API and provides temperature details.
- **Currency Exchange Rates**: Fetches real-time currency exchange rates against the Russian Ruble (RUB) from the Free Forex API and converts currencies as per user requests.
- **User State Management**: Manages user states to track ongoing conversations and handle user input accordingly.

## Installation
1. Clone the repository: `git clone https://github.com/username/repository.git`
2. Navigate to the project directory: `cd repository`
3. Install the required dependencies: `pip install -r requirements.txt`

## Configuration
1. Obtain API tokens:
   - Telegram Bot API token
   - OpenWeatherMap API token
   - Free Forex API token
2. Update the respective tokens in the code.

## Usage
1. Start the bot by executing the script.
2. Interact with the bot through Telegram by sending messages and commands.
3. Use the "/start" command to begin a conversation and "/help" command to view available functionalities.
4. Request weather information by sending the command "/weather" followed by the city name.
5. Inquire about currency exchange rates using the command "/exchange" followed by the currency code (e.g., USD, EUR, GBP).

## Dependencies
- Telebot (`telebot`)
- Requests (`requests`)

Search in telegram: @chat_1223bot

