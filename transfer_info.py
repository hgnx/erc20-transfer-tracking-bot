import requests
import re
import time
from bs4 import BeautifulSoup

USER_AGENT                              = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
BASE_URL                                = "https://etherscan.io"

def parse(url, user_agent=USER_AGENT, encoding="utf-8", max_retries=3, wait_time=5):
    headers                             = {"User-Agent": user_agent}
    for retry in range(max_retries):
        try:
            response                    = requests.get(url, headers=headers)
            response.encoding           = encoding
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data from {url} - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    print("Max retries reached. Could not fetch data.")
    return None

def get_last_transaction(targeted_wallet: str, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            MAINPAGE                    = parse(f"{BASE_URL}/address/{targeted_wallet}")

            FROM                        = MAINPAGE.select("#transactions > div > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > span")[0].text
            TO                          = MAINPAGE.select("#transactions > div > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(10) > div > a.hash-tag.text-truncate")[0].text.lstrip()
            TX                          = MAINPAGE.select("#transactions > div > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a")[0].text
            TX_URL                      = f'{BASE_URL}{MAINPAGE.select("#transactions > div > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a")[0].get("href")}'

            SYMBOL                      = parse(TX_URL).select("#wrapperContent > div > div > a")[0].text
            TOKEN_AMOUNT                = parse(TX_URL).select("#ContentPlaceHolder1_maintable > div.card.p-5.mb-3 > div:nth-child(13) > div.col.col-md-9 > div > div > span.d-inline-flex.flex-wrap.align-items-center > span:nth-child(6)")[0].text
            
            try:
                USDT_VALUE              = parse(TX_URL).select("#ContentPlaceHolder1_maintable > div.card.p-5.mb-3 > div:nth-child(13) > div.col.col-md-9 > div > div > span.d-inline-flex.flex-wrap.align-items-center > span.text-muted.me-1")[0].text
                return FROM, TO, TX, TOKEN_AMOUNT, SYMBOL, USDT_VALUE, TX_URL
            except:
                TOKEN_URL               = f'{BASE_URL}{parse(TX_URL).select("#ContentPlaceHolder1_maintable > div.card.p-5.mb-3 > div:nth-child(13) > div.col.col-md-9 > div > div > span.d-inline-flex.flex-wrap.align-items-center > a.d-flex.align-items-center")[0].get("href")}'
                TOKEN_NAME_TEMP         = parse(TOKEN_URL).select("#content > section:nth-child(9) > div > div:nth-child(1) > div > span.fs-base.fw-medium")[0].text
                TOKEN_NAME              = re.sub(" \([A-Z]+\)", "", TOKEN_NAME_TEMP).strip().replace(' ', '-').lower()
                CMC_TOKEN_URL           = f'https://coinmarketcap.com/currencies/{TOKEN_NAME}/'
                try:
                    CMC_CURRENT_PRICE   = float(parse(CMC_TOKEN_URL).select("#section-coin-overview > div.sc-16891c57-0.hqcKQB.flexStart.alignBaseline > span")[0].text[1:])
                except:
                    TOKEN_NAME          = TOKEN_NAME.replace('-token', '')
                    CMC_TOKEN_URL       = f'https://coinmarketcap.com/currencies/{TOKEN_NAME}/'
                    CMC_CURRENT_PRICE   = float(parse(CMC_TOKEN_URL).select("#section-coin-overview > div.sc-16891c57-0.hqcKQB.flexStart.alignBaseline > span")[0].text[1:])
                
                TRANSFERRED_USD         = "(${:,.1f})".format(float(TOKEN_AMOUNT.replace(',', '')) * CMC_CURRENT_PRICE)
                return FROM, TO, TX, TOKEN_AMOUNT, SYMBOL, TRANSFERRED_USD, TX_URL
        except IndexError:
            error_msg                   = "Failed to retrieve the last transaction due to IndexError."
        except Exception as e:
            error_msg                   = f"Error occurred: {str(e)}"
        print(f"Retrying {retry+1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    print("Max retries reached. Moving to the next wallet.")
    return None, None, None, None, None, None, None