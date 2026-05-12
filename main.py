import requests
import time
import threading

BOT_TOKEN = "8767999011:AAEbg9hcV8NAQFME2HTNq-5drLuo-VkFBmE"
CHAT_ID = "8778723993"

CHECK_INTERVAL = 30

WILAYAS = [
    {"name": "أم البواقي", "keyword": "oum el bouaghi"},
    {"name": "قالمة", "keyword": "guelma"},
    {"name": "تبسة", "keyword": "tebessa"},
    {"name": "باتنة", "keyword": "batna"},
]

last_update_id = 0

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

def do_check():
    send_message("🔍 جاري الفحص الآن...")
    found = False
    for wilaya in WILAYAS:
        if check_wilaya(wilaya):
            send_message(f"🚨🐑 فُتح الحجز في ولاية {wilaya['name']}!\nادخل الآن: https://adhahi.dz/register")
            found = True
    if not found:
        send_message("❌ لا يزال الحجز مغلقاً في جميع الولايات.")

def listen_commands():
    global last_update_id
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=10"
            response = requests.get(url, timeout=15)
            data = response.json()
            for update in data.get("result", []):
                last_update_id = update["update_id"]
                message = update.get("message", {})
                text = message.get("text", "")
                if text == "/status":
                    send_message("✅ البوت يعمل بشكل طبيعي!\n🔍 يراقب الولايات كل 30 ثانية:\n🔹 أم البواقي\n🔹 قالمة\n🔹 تبسة\n🔹 باتنة\n\nأرسل /check لفحص فوري")
                elif text == "/check":
                    threading.Thread(target=do_check).start()
        except:
            pass
        time.sleep(2)

def main():
    send_message("✅ بدأ مراقبة منصة أضاحي!\n🔹 أم البواقي\n🔹 قالمة\n🔹 تبسة\n🔹 باتنة\n\n📋 الأوامر المتاحة:\n/status - حالة البوت\n/check - فحص فوري الآن")
    print("بدأ المراقبة...")

    t = threading.Thread(target=listen_commands)
    t.daemon = True
    t.start()

    while True:
        do_check()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
