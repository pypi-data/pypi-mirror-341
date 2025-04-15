import ssl
import certifi
import os
import time
import json
import random
import threading
import warnings
import soundcard as sc
import soundfile as sf
from mtranslate import translate
import ollama
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

try:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except:
    ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "374giayfaud738q"
kullanici_key = None
SETTINGS_PATH = "data.json"

def set_api(key):
    global kullanici_key
    if key != API_KEY:
        raise ValueError("❌ Geçersiz API anahtarı!")
    kullanici_key = key
    print("✅ API key doğrulandı!")

def delay_sure_belirle():
    olasiliklar = [
        (range(10, 21), 30),
        (range(20, 41), 25),
        (range(40, 71), 20),
        (range(70, 101), 15),
        (range(100, 131), 10),
        ("PASS", 5)
    ]
    secim = random.choices(olasiliklar, weights=[o[1] for o in olasiliklar])[0]
    return secim if secim == "PASS" else random.choice(secim[0])

def kaydet_ayarlar(data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

def yukle_ayarlar():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def baslat():
    if kullanici_key != API_KEY:
        raise PermissionError("❌ API doğrulanmadı!")

    ayarlar = yukle_ayarlar()

    print("\n📋 Menü:")
    print("1 - Devam Et")
    print("2 - Ayarla")
    secim = input("Seçim yap (1/2): ").strip()

    if secim == "2":
        site = input("🌐 Girilecek site adresi: ").strip()
        xpath_input = input("✏️ Mesaj input XPath'i: ").strip()
        xpath_buton = input("📤 Gönder buton XPath'i: ").strip()
        ayarlar = {
            "site": site,
            "input_xpath": xpath_input,
            "buton_xpath": xpath_buton
        }
        kaydet_ayarlar(ayarlar)
        print("✅ Ayarlar kaydedildi.")
        return

    if not ayarlar:
        print("⚠️ Ayarlar bulunamadı. Lütfen önce '2 - Ayarla' yapın.")
        return

    profile_path = os.path.join(os.getcwd(), "borsaiti_chrome_profile")
    os.makedirs(profile_path, exist_ok=True)
    options = uc.ChromeOptions()
    options.user_data_dir = profile_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"❌ Chrome başlatılamadı: {e}")
        return

    driver.get(ayarlar["site"])
    print("🕒 AI sistemi 60 saniye sonra devreye girecek...")

    SAMPLE_RATE = 48000
    RECORD_SEC = 10
    use_file_index = 1
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant in a Kick livestream. Speak in a short, natural, human way. "
            "Be very casual and realistic. Reply in 1 short sentence only. No robotic tone."
        )
    }
    chat_history = []
    follow_up_questions = [
        "Senin düşüncen ne bu konuda?",
        "Sence bu yayında ne eksik?",
        "Chat buna ne diyor?",
        "Sen olsan ne yapardın?",
        "Daha iyisi nasıl olurdu sence?"
    ]

    def build_prompt(user_input):
        chat_history.append({"role": "user", "content": user_input})
        return [system_prompt] + chat_history[-5:]

    def start_ai():
        nonlocal use_file_index
        while True:
            file_current = f"out{use_file_index}.wav"
            file_to_delete = f"out{(use_file_index % 3) + 1}.wav"

            print(f"🎧 Masaüstü sesi dinleniyor ({file_current})...")
            try:
                with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                    sf.write(file_current, data[:, 0], samplerate=SAMPLE_RATE)
                    time.sleep(0.2)
            except Exception as e:
                print(f"🎙️ Kayıt hatası: {e}")
                continue

            try:
                if os.path.exists(file_to_delete):
                    time.sleep(0.3)
                    os.remove(file_to_delete)
            except Exception as e:
                print(f"🗑️ Dosya silme hatası: {e}")

            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_current) as source:
                    audio = recognizer.record(source)
                turkish_text = recognizer.recognize_google(audio, language="tr-TR")
                print("🧑 (Sen):", turkish_text)
            except Exception as e:
                print(f"❌ Ses tanıma hatası: {e}")
                use_file_index = (use_file_index % 3) + 1
                continue

            try:
                translated_text = translate(turkish_text, "en", "tr")
                prompt = build_prompt(translated_text)
                response = ollama.chat(model="gemma:2b", messages=prompt)
                english_reply = response["message"]["content"].strip().split(".")[0].strip() + "."
                translated_reply = translate(english_reply, "tr", "en")

                if random.random() < 0.1:
                    translated_reply += " " + random.choice(follow_up_questions)

                delay = delay_sure_belirle()
                if delay == "PASS":
                    print("⏭️ Bu mesaj atlanıyor...")
                    continue

                print(f"⌛ Cevap {delay} sn sonra geliyor...")
                time.sleep(delay)
                print("🤖 (AI):", translated_reply)
                chat_history.append({"role": "assistant", "content": english_reply})

                try:
                    chat_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ayarlar["input_xpath"]))
                    )
                    chat_input.click()
                    chat_input.send_keys(translated_reply)
                    send_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ayarlar["buton_xpath"]))
                    )
                    send_button.click()
                    print("📤 Gönderildi!")
                except Exception as msg_err:
                    print(f"❗ Mesaj gönderme hatası: {msg_err}")

                use_file_index = (use_file_index % 3) + 1
            except Exception as final_err:
                print(f"🔥 AI işlem hatası: {final_err}")

    threading.Timer(60, start_ai).start()
