import requests
import time

# ضع هنا Token البوت الجديد بعد ما تجدده من BotFather
BOT_TOKEN = "8767999011:AAEbg9hcV8NAQFME2HTNq-5drLuo-VkFBmE"
CHAT_ID = "8778723993"

URL_TO_CHECK = "https://adhahi.dz/register"
CHECK_INTERVAL = 60  # فحص كل 60 ثانية

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except:
        pass

def check_site():
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        content = response.text.lower()
        # إذا وجد كلمة تدل على فتح الحجز
        if "احجز" in content or "حجز" in content or "register" in content:
            if "fermé" not in content and "مغلق" not in content:
                return True
    except:
        pass
    return False

def main():
    send_message("✅ بدأ مراقبة منصة أضاحي... سأخبرك فور فتح الحجز!")
    print("بدأ المراقبة...")

    while True:
        if check_site():
            send_message("🚨🐑 تنبيه! فُتح الحجز على منصة أضاحي!\nادخل الآن: https://adhahi.dz/register")
            print("تم إرسال التنبيه!")
            break
        else:
            print("الموقع لا يزال مغلقاً... سأتحقق مجدداً بعد دقيقة")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
