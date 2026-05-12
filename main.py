import requests
import time
import threading

BOT_TOKEN = "8767999011:AAEbg9hcV8NAQFME2HTNq-5drLuo-VkFBmE"
CHAT_ID = "8778723993"
CHANNEL_ID = "@adh89m"

CHECK_INTERVAL = 30

WILAYAS = [
    {"name": "أم البواقي", "keyword": "oum el bouaghi"},
    {"name": "قالمة", "keyword": "guelma"},
    {"name": "تبسة", "keyword": "tebessa"},
    {"name": "باتنة", "keyword": "batna"},
    {"name": "خنشلة", "keyword": "khenchela"},
]

last_update_id = 0

def send_message(text, target=None):
    if target is None:
        target = CHAT_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": target, "text": text}
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

def do_check(manual=False):
    if manual:
        send_message("🔍 جاري الفحص الآن...")
    found = False
    for wilaya in WILAYAS:
        if check_wilaya(wilaya):
            alert = f"🚨🐑 فُتح الحجز في ولاية {wilaya['name']}!\nادخل الآن: https://adhahi.dz/register"
            send_message(alert, target=CHAT_ID)
            send_message(alert, target=CHANNEL_ID)
            found = True
    if manual and not found:
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
                    send_message("✅ البوت يعمل!\n🔍 يراقب كل 30 ثانية:\n🔹 أم البواقي\n🔹 قالمة\n🔹 تبسة\n🔹 باتنة\n🔹 خنشلة\n\nأرسل /check لفحص فوري")
                elif text == "/check":
                    threading.Thread(target=lambda: do_check(manual=True)).start()
        except:
            pass
        time.sleep(2)

def main():
    send_message("✅ بدأ مراقبة منصة أضاحي!\n🔹 أم البواقي\n🔹 قالمة\n🔹 تبسة\n🔹 باتنة\n🔹 خنشلة\n\n📋 الأوامر:\n/status - حالة البوت\n/check - فحص فوري")
    print("بدأ المراقبة...")

    t = threading.Thread(target=listen_commands)
    t.daemon = True
    t.start()

    while True:
        do_check(manual=False)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
