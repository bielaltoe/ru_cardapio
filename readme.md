# RU Cardapio

## Description
RU Cardapio is a Python project designed to manage and display the menu of a restaurant. It allows users to add, update, and view the daily menu items.

## Features
- Add new menu items
- Update existing menu items
- View the daily menu

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/yourusername/ru_cardapio.git
    ```
2. Navigate to the project directory:
    ```
    cd ru_cardapio
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script to start the application:
    ```
    python main.py
    ```
2. Follow the on-screen instructions to manage the menu.

## Docker Execution
1. Build the Docker image:
    ```
    docker build -t cardapio_ru_bot .
    ```
2. Run the Docker container:
    ```
    docker run -d --name cardapio_ru --restart unless-stopped cardapio_ru_bot
    ```

## Contributing
1. Fork the repository.
2. Create a new branch:
    ```
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```
    git push origin feature-branch
    ```
5. Open a pull request.

## License
This project is licensed under the MIT License.