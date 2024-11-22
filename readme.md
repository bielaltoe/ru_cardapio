# RU Cardápio

RU Cardápio is a Python project designed to manage and display the menu of a university restaurant (RU). It automatically fetches the menu from the restaurant's official website and sends it to a Telegram channel.

## Features
- Automatic fetching of the menu from the official website.
- Formatting and sending the menu to a Telegram channel.
- Scheduled menu updates every 6 minutes.
- Automatic deletion of old messages from Telegram daily at 11:59 PM.

## Technologies Used
- **Python 3.9**
- **Libraries:**
  - `requests`
  - `bs4` (BeautifulSoup)
  - `schedule`
  - `logging`
- **Docker** for containerization.

## Installation and Local Execution
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ru_cardapio.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ru_cardapio
    ```

3. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure the Telegram token in the code (`TELEGRAM_TOKEN`) and the channel ID (`CHANNEL_ID`).

5. Run the main script:
    ```bash
    python api.py
    ```

## Running with Docker

1. Build the Docker image:
    ```bash
    docker build -t cardapio_ru_bot .
    ```

2. Run the container:
    ```bash
    docker run -d \
      --name cardapio_ru \
      --restart unless-stopped \
      cardapio_ru_bot
    ```

## Project Structure
- **`api.py`**: Contains the logic to fetch, format, and send the menu to Telegram.
- **`requirements.txt`**: List of project dependencies.
- **`Dockerfile`**: Configuration for containerizing the project.

## How It Works
1. **Menu Fetching**: The script accesses the RU website and extracts the day's menu.
2. **Formatting and Sending**: The menu is formatted in HTML and sent to the specified Telegram channel.
3. **Periodic Checks**: Every 6 minutes, the script checks for menu updates.
4. **Daily Cleanup**: All old messages are deleted at 11:59 PM daily.

## Contributions
Contributions are welcome! Follow the steps below:

1. Fork the repository.
2. Create a branch for your feature or fix:
    ```bash
    git checkout -b my-feature
    ```
3. Commit your changes:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push to the remote repository:
    ```bash
    git push origin my-feature
    ```
5. Open a pull request in the original repository.

## License
This project is licensed under the terms of the MIT license. See the `LICENSE` file for details.

## Contact
For questions or suggestions, contact via the Telegram channel: [@cardapio_ufes](https://t.me/cardapio_ufes).

