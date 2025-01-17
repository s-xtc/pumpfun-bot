import argparse
import asyncio
import websockets
import json
import requests
import time
import threading
from rich import print


print("[bold magenta]██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗    ██████╗  ██████╗ ████████╗[/bold magenta]")
print("[bold magenta]██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║    ██╔══██╗██╔═══██╗╚══██╔══╝[/bold magenta]")
print("[bold magenta]██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║    ██████╔╝██║   ██║   ██║   [/bold magenta]")
print("[bold magenta]██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║    ██╔══██╗██║   ██║   ██║   [/bold magenta]")
print("[bold magenta]██║        ██║   ██║     ╚██████╔╝██║ ╚████║    ██████╔╝╚██████╔╝   ██║   [/bold magenta]")
print("[bold magenta]╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝  ╚═════╝    ╚═╝   [/bold magenta]")




# Default configuration settings
config = {
    'API_KEY': "api-key",  # Default API key value (replace with your key)
    'TRADE_URL': "https://pumpportal.fun/api/trade?api-key=",
    'WS_URI': "wss://pumpportal.fun/api/data",
    'AUTO_BUY_AMOUNT_SOL': 0.05,
    'AUTO_SELL_WIN_PERCENT': 10,
    'AUTO_SELL_LOSS_PERCENT': 10,
    'AUTO_SELL_TIME_LIMIT': 5,
    'SLIPPAGE': 15,
    'PRIORITY_FEE': 0.0001
}


# Function to execute trades
def execute_trade(action, mint, amount, denominated_in_sol, slippage, priority_fee, pool="pump"):
    print(f"Executing trade for token: {mint}, Action: {action}, Amount: {amount}, Denominated in SOL: {denominated_in_sol}")
    payload = {
        "action": action,
        "mint": mint,
        "amount": amount,
        "denominatedInSol": denominated_in_sol,
        "slippage": slippage,
        "priorityFee": priority_fee,
        "pool": pool,
    }

    response = requests.post(config['TRADE_URL'] + config['API_KEY'], data=payload)
    return response.json()

# Auto-sell function
def auto_sell(mint, buy_price, purchase_time):
    print(f"Auto-sell initiated for token: {mint}, Buy Price: {buy_price}")

    target_sell_win_price = buy_price * (1 + config['AUTO_SELL_WIN_PERCENT'] / 100)
    target_sell_loss_price = buy_price * (1 - config['AUTO_SELL_LOSS_PERCENT'] / 100)

    while True:
        current_price = buy_price  # Replace this with a real price-fetching method

        print(f"Current price of {mint}: {current_price}")

        if current_price >= target_sell_win_price:
            print(f"Target profit reached for {mint}. Selling...")
            sell_result = execute_trade(
                action="sell",
                mint=mint,
                amount="100%",  # Sell all holdings
                denominated_in_sol="false",
                slippage=config['SLIPPAGE'],
                priority_fee=config['PRIORITY_FEE']
            )
            print("Auto-sell result:", sell_result)
            break

        elif current_price <= target_sell_loss_price:
            print(f"Target loss reached for {mint}. Selling...")
            sell_result = execute_trade(
                action="sell",
                mint=mint,
                amount="100%",  # Sell all holdings
                denominated_in_sol="false",
                slippage=config['SLIPPAGE'],
                priority_fee=config['PRIORITY_FEE']
            )
            print("Auto-sell result:", sell_result)
            break

        if time.time() - purchase_time >= config['AUTO_SELL_TIME_LIMIT']:
            print(f"Time limit reached for {mint}. Selling after {config['AUTO_SELL_TIME_LIMIT']} seconds...")
            sell_result = execute_trade(
                action="sell",
                mint=mint,
                amount="100%",  # Sell all holdings
                denominated_in_sol="false",
                slippage=config['SLIPPAGE'],
                priority_fee=config['PRIORITY_FEE']
            )
            print("Auto-sell result:", sell_result)
            break

        time.sleep(5)

# Monitor market for new tokens and execute autobuy
async def monitor_market_and_autobuy():
    while True:
        current_token = None
        buy_price = None
        purchase_time = None

        async with websockets.connect(config['WS_URI']) as websocket:
            await websocket.send(json.dumps({"method": "subscribeNewToken"}))
            print("Subscribed to new token events...\n")

            while True:
                try:
                    message = await websocket.recv()
                    print("Received message from WebSocket:", message)
                    data = json.loads(message)

                    if "mint" in data:
                        mint = data["mint"]
                        print(f"New token detected: {mint}.")

                        if current_token is None:
                            print(f"Processing token {mint}... Executing auto-buy.")
                            current_token = mint

                            # Execute auto-buy
                            buy_result = execute_trade(
                                action="buy",
                                mint=mint,
                                amount=config['AUTO_BUY_AMOUNT_SOL'],
                                denominated_in_sol="true",
                                slippage=config['SLIPPAGE'],
                                priority_fee=config['PRIORITY_FEE']
                            )
                            print("Auto-buy result:", buy_result)

                            if "errors" in buy_result and buy_result["errors"]:
                                print(f"Error during buy: {buy_result['errors']}")
                            else:
                                print(f"Buy [green]successful[/green] for token {mint}.")
                                buy_price = data.get("initialBuy", 0)
                                purchase_time = time.time()
                                auto_sell_thread = threading.Thread(target=auto_sell, args=(mint, buy_price, purchase_time))
                                auto_sell_thread.start()

                                # Wait for the sell process to complete before continuing
                                auto_sell_thread.join()
                                # After the sell is done, reset and repeat the process
                                print(f"Completed trade for {mint}. Restarting market monitoring in 5 seconds...\n")
                                time.sleep(1)
                                print(f"Restarting market monitoring in 4 seconds...\n")
                                time.sleep(1)
                                print(f"Restarting market monitoring in 3 seconds...\n")
                                time.sleep(1)
                                print(f"Restarting market monitoring in 2 seconds...\n")
                                time.sleep(1)
                                print(f"Restarting market monitoring in 1 seconds...\n")
                                time.sleep(1)
                                break  # Restart the outer while loop to handle a new token

                except Exception as e:
                    print(f"Error while receiving WebSocket message: {e}")
                    break


# Function to display the menu and get user input
def show_menu():
    print("\nPumpPortal Automated Trading System")
    print("1. Create wallet")
    print("2. Start market monitoring with auto-buy and auto-sell")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")
    return choice


# Function to configure settings interactively
def create_wallet():
    print("\nConfigure Your Settings")
    
    # Making the request to the API
    response = requests.get(url="https://pumpportal.fun/api/create-wallet")
    
    if response.status_code == 200:  # Check if the request was successful
        # JSON with keys for a newly generated wallet and the linked API key
        data = response.json()
        
        # Save the wallet details to a text file
        with open("wallet_details.txt", "w") as file:
            file.write(str(data))  # Convert data to string and write it to the file
        
        print("[green]Wallet details have been saved to wallet_details.txt.[/green]")
    else:
        print(f"Failed to create wallet. Status code: {response.status_code}")




# Run the automation
def start_automation():
    print("Starting market monitoring with auto-buy and auto-sell...\n")
    asyncio.run(monitor_market_and_autobuy())


# Main function to handle user interaction
def main():
    while True:
        user_choice = show_menu()

        if user_choice == '1':
            create_wallet()

        elif user_choice == '2':
            start_automation()

        elif user_choice == '3':
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
