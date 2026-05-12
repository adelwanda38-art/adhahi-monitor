import requests
import time

BOT_TOKEN = "8767999011:AAEbg9hcV8NAQFME2HTNq-5drLuo-VkFBmE"
CHAT_ID = "8778723993"

CHECK_INTERVAL = 30  # فحص كل 30 ثانية

WILAYAS = [
    {"name": "أم البواقي", "keyword": "oum el bouaghi"},
    {"name": "قالمة", "keyword": "guelma"},
    {"name": "تبسة", "keyword": "tebessa"},
    {"name": "باتنة", "keyword": "batna"},
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except:
        pass

def check_wilaya(wilaya):
    try:
        response = requests.get("https://adhahi.dz/register", timeout=10)
        content = response.text.lower()
        if wilaya["keyword"] in content:
            if "fermé" not in content and "مغلق" not in content:
                return True
    except:
        pass
    return False

def main():
    send_message("✅ بدأ مراقبة منصة أضاحي للولايات:\n🔹 أم البواقي\n🔹 قالمة\n🔹 تبسة\n🔹 باتنة\nكل 30 ثانية!")
    print("بدأ المراقبة...")

    while True:
        for wilaya in WILAYAS:
            if check_wilaya(wilaya):
                send_message(f"🚨🐑 تنبيه! فُتح الحجز في ولاية {wilaya['name']}!\nادخل الآن: https://adhahi.dz/register")
                print(f"تم إرسال التنبيه لولاية {wilaya['name']}!")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
