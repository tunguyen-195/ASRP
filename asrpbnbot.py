import requests

TOKEN = "7991446285:AAEsV-s1cBPJKbhUO385MKa6YREUVaBfkcY"  # Thay bằng token của bot
CHAT_IDS = ["5759963691", ]  # Danh sách các chat ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data)
        if not response.ok:
            print(f"Failed to send message to {chat_id}: {response.text}")
    return response.json()

# Gửi tin nhắn thử nghiệm
send_telegram_message("🔔 Server thông báo: Dịch vụ đang hoạt động!")
