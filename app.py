# fetch top 50 cryptocurrencies by market capitalization
import requests
import json
import pandas as pd

# Coinsgecko API Base URL
base_url = "https://api.coingecko.com/api/v3/"

# import upload_data_into_excel_file
def upload_data_into_excel_file(filename):
    print(filename)
    try:
        with open(f"{filename}.json", "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        df.to_excel(f'{filename}.xlsx')
        print(f"File {filename}.xlsx uploaded successfully.")
    except:
        print("Error occurred while reading the file.")


def upload_data_to_json(filename,data_to_uploaded):
    with open(f"{filename}.json","w") as f:
        f.write(json.dumps(data_to_uploaded, indent=4))
    upload_data_into_excel_file(f"{filename}")

def get_top_50_coins():
    req_coins = requests.get(f"{base_url}/coins/list")
    data = json.loads(req_coins.text)
    # print(data)
    upload_data_to_json("coin-list",data)

def coin_list_with_market_data(currency,per_page):
    req_coins = requests.get(f"{base_url}/coins/markets?vs_currency={currency}&per_page={per_page}")
    data = json.loads(req_coins.text)
    # print(data)

    acquire_only_relevent_data = []
    for i in range(0,len(data)):
        coin_data = {}
        coin_data['coin_name'] = data[i]['name']
        coin_data['coin_symbol'] = data[i]['symbol']
        coin_data['coin_current_price'] = round(data[i]['current_price'],3)
        coin_data['coin_market_capitalization'] = data[i]['market_cap']
        coin_data["price_change_24_hr"] = data[i]["price_change_24h"],
        coin_data["percent_change_24_hr"] = data[i]["price_change_percentage_24h"]
        coin_data["coin_min_24h_trading_volume"] = data[i]['low_24h'],
        coin_data["coin_max_24h_trading_volume"] = data[i]['high_24h'],
        coin_data["coin_total_trading_volumne"] = data[i]['low_24h']

        acquire_only_relevent_data.append(coin_data)

    upload_data_to_json("market-coins",acquire_only_relevent_data)


# "https://api.coingecko.com/api/v3/coins/"
def get_top_5_crypto_currencies_byMarket_cap(orderCategory,currency,count_of_coins):
    print(base_url)
    req_coins = requests.get(f"{base_url}coins/markets?order={orderCategory}&vs_currency={currency}&per_page={count_of_coins}")
    data = json.loads(req_coins.text)
    upload_data_to_json("top-5-crypto-curriencies",data)
        
def avg_price_of_top_50_currencies():
    req_coins = requests.get(f"{base_url}coins/markets?vs_currency=usd&per_page=2")
    data = json.loads(req_coins.text)
    print(data)
    total_price = 0
    for coin in data:
        total_price += round(coin['current_price'],3)
    avg_price = total_price / len(data)
    print(f"The average price of the top 50 cryptocurrencies in USD is: {round(avg_price,3)}")

def analyze_the_highest_lowest_24_hr_perc_price_change():
    req_coins = requests.get(f"{base_url}coins/markets?vs_currency=usd&per_page=50")
    data = json.loads(req_coins.text)
    highest_price_change_24_hr = max(data, key = lambda x: x['price_change_percentage_24h'])
    lowest_price_change_24_hr = min(data, key = lambda x: x['price_change_percentage_24h'])
    print(f"The highest 24-hour price change coin is: {highest_price_change_24_hr['name']} with a change of {highest_price_change_24_hr['price_change_percentage_24h']}%")
    print(f"The lowest 24-hour price change coin is: {lowest_price_change_24_hr['name']}%")

if __name__ == "__main__":
    orderCategories =  [ "market_cap_asc", "market_cap_desc", "volume_asc" , "volume_desc" ]
    countOfCryptoCurrencies = 5
    # get_top_5_crypto_currencies_byMarket_cap(orderCategories[1],"usd",countOfCryptoCurrencies)
    # analyze_the_highest_lowest_24_hr_perc_price_change()
    # avg_price_of_top_50_currencies()

    options_to_user = [
        "Press 0 : Get Top 50 currencies",
        "Press 1 :  Get top 50 cryptocurrencies by market capitalization",
        "Press 2 : Get the average price of the top 50 cryptocurrencies",
        "Press 3 :  Analyze the highest and lowest 24-hour price change coins",
        "Press -1 : Exit"
    ]

    for item in options_to_user:
        print(item)


    while True:
        userinput = int(input("Enter Here : "))
        if userinput == -1:
            print("Exiting the program...")
            break
        elif userinput == 0:
            get_top_50_coins()
            break
        elif userinput == 1:
                temp = 0;
                
                for item in orderCategories:
                    print(f"Press {temp+1} to {item}")
                
                get_category = str(input("Enter the Option as shown above : "))
                if get_category in orderCategories:
                    get_top_5_crypto_currencies_byMarket_cap(get_category,"usd",countOfCryptoCurrencies)
                    break
                else:
                    print("Invalid Option!")
                    break
        elif userinput == 2:
            print("The Average Price of top 50 cryptocurrencies !")
            avg_price_of_top_50_currencies()
            break
        elif userinput == 3:
            print("The Highest and Lowest 24-hour Price Change Coins !")
            analyze_the_highest_lowest_24_hr_perc_price_change()
            break
        else:
            break