import time
from transfer_info import get_last_transaction
from message import telegram_send_message


TARGETED_WALLETS                    = [
                                        "ETHEREUM WALLET ADDRESS 1",
                                        "ETHEREUM WALLET ADDRESS 2",
                                        "ETHEREUM WALLET ADDRESS 3"
                                      ]

last_transactions                   = {wallet: None for wallet in TARGETED_WALLETS}

while True:
    for wallet in TARGETED_WALLETS:
        current_transaction         = get_last_transaction(wallet)
        if None in current_transaction:
            continue

        current_transaction_tx      = current_transaction[2]

        if current_transaction_tx:
            if not last_transactions[wallet]:
                message             = f"<b>Last transaction for {wallet}:</b>\n" \
                                      f"----------\n" \
                                      f"{current_transaction[0]}\n->\n{current_transaction[1]}\n" \
                                      f"----------\n" \
                                      f"{current_transaction[3]} {current_transaction[4]} {current_transaction[5]}\n" \
                                      f"<a href='{current_transaction[6]}'><b>CHECK ON ETHERSCAN</b></a>"
                telegram_send_message(message)
                last_transactions[wallet] = current_transaction_tx
            elif last_transactions[wallet] != current_transaction_tx:
                message             = f"<b>New transaction detected for {wallet}:</b>\n" \
                                      f"----------\n" \
                                      f"{current_transaction[0]}\n->\n{current_transaction[1]}\n" \
                                      f"----------\n" \
                                      f"{current_transaction[3]} {current_transaction[4]} {current_transaction[5]}\n" \
                                      f"<a href='{current_transaction[6]}'><b>CHECK ON ETHERSCAN</b></a>"
                telegram_send_message(message)
                last_transactions[wallet] = current_transaction_tx
        time.sleep(5)
    time.sleep(60)