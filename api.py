import requests
from bs4 import BeautifulSoup
import hashlib
import schedule
import time
import datetime


# Informações do Telegram
TELEGRAM_TOKEN = "7189241611:AAHzeL7NqMr5EG9NIV7wCq7iHS_nRA4c6Ts"
CHANNEL_ID = "@cardapio_ufes"


# Função para enviar mensagem para o Telegram
def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    response = requests.post(url, data=payload)
    if response.ok:
        message_id = response.json().get("result", {}).get("message_id")
        
        # Salva o ID da mensagem em um arquivo
        if message_id:
            with open("message_ids.txt", "a") as file:
                file.write(f"{message_id}\n")
                
        return message_id
    return None


# Função para apagar mensagens do Telegram
def delete_message_from_telegram(message_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteMessage"
    payload = {"chat_id": CHANNEL_ID, "message_id": message_id}
    response = requests.post(url, data=payload)
    return response.ok


# Função para obter mensagens enviadas pelo bot (necessário para exclusão)
# def get_bot_messages():
#     url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
#     response = requests.get(url)
#     print(response)
#     if response.status_code == 200:
#         updates = response.json().get("result", [])
#         print(updates)
#         message_ids = []
#         for update in updates:
#             if "message" in update and update["message"]["chat"]["id"] == int(
#                 CHANNEL_ID.replace("@", "")
#             ):
#                 message_ids.append(update["message"]["message_id"])
#         return message_ids
#     return []


# Função para apagar todas as mensagens à meia-noite
def delete_all_messages():
    print("Apagando mensagens...")
    try:
        with open("message_ids.txt", "r") as file:
            message_ids = file.readlines()
        
        for message_id in message_ids:
            message_id = message_id.strip()
            if message_id:
                delete_message_from_telegram(int(message_id))
                
        # Após apagar as mensagens, limpe o arquivo
        with open("message_ids.txt", "w") as file:
            file.write("")
        
        print("Mensagens apagadas com sucesso!")
    except FileNotFoundError:
        print("Nenhuma mensagem para apagar.")

# Função para obter o conteúdo do cardápio (almoço e jantar)
def get_menu_content():
    today_date = datetime.date.today()
    url = f"https://ru.ufes.br/cardapio/{today_date}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        menu = {}
        titles = soup.find_all("div", class_="views-field-title")
        bodies = soup.find_all("div", class_="views-field-body")

        for title, body in zip(titles, bodies):
            meal_title = title.find("span", class_="field-content").get_text(strip=True)
            meal_content = body.find("div", class_="field-content").get_text(
                separator="\n", strip=True
            )

            if "Almoço" in meal_title:
                menu["Almoço"] = meal_content
            elif "Jantar" in meal_title:
                menu["Jantar"] = meal_content

        return menu
    else:
        print(f"Erro ao acessar o cardápio: {response.status_code}")
        return None


def format_menu(menu):
    
    formated_menu = menu.split("\n")
    # print(formated_menu)
    output_menu = ""
    forbidden_words = ["sujeito", "Informamos", "Opção"]
    for item in formated_menu:

        skip_next = False

        for fb in forbidden_words:
            if fb in item:
                skip_next = True
                break
        if skip_next:
            continue

        item = item.split("(")[0]

        if item == "Salada":
            output_menu += f"\n🥗 <b>{item}</b>: \n"
            continue
        elif item == "Prato Principal":
            output_menu += f"\n🍛 <b>{item}</b>: \n"
            continue
        elif item == "Guarnição":
            output_menu += f"\n🍚 <b>{item}</b>: \n"
            continue
        elif item == "Acompanhamento":
            output_menu += f"\n🍟 <b>{item}</b>: \n"
            continue
        elif item == "Sobremesa":
            output_menu += f"\n🍨 <b>{item}</b>: \n"
            continue
        else:
            for item in item.split(", "):
                for item in item.split(" e "):
                    output_menu += f"    - {item}\n"
            
    return output_menu


# Função para formatar a mensagem para o Telegram com a data incluída
def format_message(menu):
    if not menu:
        return None

    today_date = datetime.date.today().strftime("%d/%m/%Y")
    message = ""

    if "Jantar" in menu:
        message += f"<b>📅 Jantar do dia {today_date}</b>\n\n"

        output_menu = format_menu(menu["Jantar"])
    else:
        message += f"<b>📅 Almoço do dia {today_date}</b>\n\n"
        output_menu = format_menu(menu["Almoço"])
    message += output_menu

    return message


# Função para verificar atualizações e enviar o cardápio para o Telegram
def check_update():
    menu = get_menu_content()

    if menu:
        menu_text = "\n\n".join(menu.values())
        current_hash = hashlib.md5(menu_text.encode("utf-8")).hexdigest()

        try:
            with open("menu_hash.txt", "r") as file:
                previous_hash = file.read()
        except FileNotFoundError:
            previous_hash = None

        if current_hash != previous_hash:
            with open("menu_hash.txt", "w") as file:
                file.write(current_hash)

            message = format_message(menu)
            if message:
                print("Cardápio atualizado!")
                print(message)
                send_message_to_telegram(message)
        else:
            print("Nenhuma alteração no cardápio")
    else:
        print("Erro ao acessar o cardápio")


# Agendar a execução a cada 6 minutos para o envio do cardápio
schedule.every(0.1).minutes.do(check_update)

# Agendar a exclusão das mensagens à meia-noite
schedule.every().day.at("23:59").do(delete_all_messages)

print("Monitoramento iniciado...")
while True:
    schedule.run_pending()
    time.sleep(1)
