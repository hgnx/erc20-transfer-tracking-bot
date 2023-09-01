# ERC20 Token Transfer Tracking Bot

The ERC20 Token Transfer Tracking Bot is an automation tool designed to monitor ERC-20 token transactions on the Ethereum blockchain. The bot scrapes the web to gather detailed information on token transfers, including the addresses of both the sender and recipient, transaction hashes, token symbols, and transferred quantities. Additionally, it computes the equivalent USD value of each transaction for streamlined analysis.

## Features

- Monitors ERC-20 token transfers on Etherscan in real-time, fetching transaction details at 1-minute intervals.
- Provides comprehensive details for each transfer, including the addresses of both the sender and the recipient, the transaction hash, and if available, any associated labels or identifiers.
- Clearly identifies the tokens involved in each transaction by fetching their names.
- Offers two methods to ascertain the USD value of the transferred tokens:
  - Directly fetches the USD equivalent from Etherscan when available.
  - If Etherscan does not provide USD values, calculates the amount using real-time price data from CoinMarketCap.
- Capable of tracking multiple Ethereum addresses simultaneously.
- Utilizes a Telegram bot to notify you whenever a new transaction occurs. The notification includes all relevant transaction details and a link to view it on Etherscan.
- Incorporates built-in error handling and retry mechanisms to counter intermittent connectivity issues or rate limits from data sources.

## Setup

- Before running the main script (`main.py`), configure your Telegram bot token and chat ID using the `setup.py` script. You will be prompted to provide your Telegram bot token and chat ID, which will be stored in a config.ini file for the main script to reference.

## Installation and Usage

1. Download the project code.
```
git clone https://github.com/hgnx/erc20-transfer-tracking-bot.git
```

2. Install the required libraries.
```
pip install -r requirements.txt
```

3. Contact [@Botfather](https://t.me/botfather) on Telegram to create a new bot and acquire the bot token.

4. Get the unique identifier for your group.
    - 4-1. Log in to [Telegram Web](https://web.telegram.org/a/) and navigate to the group where you want to receive notifications.
    - 4-2. Add the bot to the group.
    - 4-3. In the address bar, you'll find the URL that looks like this: "https://web.telegram.org/a/#-XXXXXXXXX". The sequence "**-XXXXXXXXX**" is your group's unique identifier.
    - 4-4. If your group is classified as a supergroup, prefix the unique identifier with "-100". For example, "**-100XXXXXXXXX**".

5. Run the setup script and enter your Telegram bot token and chat ID (the unique identifier of your group).
```
python setup.py
```

6. In `main.py`, assign the Ethereum wallet address you want to track to the `TARGETED_WALLETS` variable.
   - You can add as many addresses as you want to the list. However, adding too many addresses may cause connection issues.
   - Ethereum wallet address must always start with "0x".

7. Run the main script.
```
python main.py
```

## Example

### Last transaction
  
![alt text](https://github.com/hgnx/erc20-transfer-tracking-bot/blob/main/screenshots/last.png?raw=true)

### New transaction

![alt text](https://github.com/hgnx/erc20-transfer-tracking-bot/blob/main/screenshots/new.png?raw=true)

## Disclaimer
This script is for informational purposes only and should not be used as the basis for any financial decisions. I take no responsibility for any personal financial loss. Use this script at your own risk.