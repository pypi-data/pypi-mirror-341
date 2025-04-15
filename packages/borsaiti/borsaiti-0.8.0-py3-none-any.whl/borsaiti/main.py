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
MODEL_PATH = "model.json"
PROMPTS_PATH = "prompts.txt"
SYSTEM_PROMPT_PATH = "system_prompt.json"

def set_api(key):
    global kullanici_key
    if key != API_KEY:
        raise ValueError("❌ Invalid API key!")
    kullanici_key = key
    print("✅ API key verified!")

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

def yukle_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("model", None)
    return None

def kaydet_model(model):
    with open(MODEL_PATH, "w", encoding="utf-8") as f:
        json.dump({"model": model}, f)

def system_prompt_ekle():
    satir = input("➕ Add line to system prompt: ").strip()
    if not os.path.exists(SYSTEM_PROMPT_PATH):
        with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
            json.dump({"lines": []}, f)
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["lines"].append(satir)
    with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("✅ Line added to system prompt.")

def system_prompt_sil():
    if not os.path.exists(SYSTEM_PROMPT_PATH):
        print("⚠️ No system prompt found.")
        return
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i, line in enumerate(data.get("lines", [])):
        print(f"{i+1}: {line}")
    try:
        index = int(input("❌ Enter line number to delete: ")) - 1
        if 0 <= index < len(data["lines"]):
            data["lines"].pop(index)
            with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("✅ Line deleted.")
        else:
            print("❌ Invalid number.")
    except:
        print("❌ Invalid input.")

def model_sec():
    print("\n🧠 Select AI Model:")
    print("1 - gemma:2b")
    print("2 - mistral")
    print("3 - llama3")
    secim = input("Your choice (1/2/3): ").strip()
    if secim == "1": kaydet_model("gemma:2b")
    elif secim == "2": kaydet_model("mistral")
    elif secim == "3": kaydet_model("llama3")
    else: print("❌ Invalid selection")

def oku_system_prompt():
    if os.path.exists(SYSTEM_PROMPT_PATH):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return " ".join(data.get("lines", []))
    return "You are an AI assistant in a Kick livestream. Speak like a human. Be brief, casual, realistic, and not robotic."

def baslat():
    if kullanici_key != API_KEY:
        raise PermissionError("❌ API not verified!")

    if yukle_model() is None:
        print("⚠️ First launch: AI model not selected.")
        model_sec()

    while True:
        print("\n📋 Menu:")
        print("1 - Continue")
        print("2 - Configure")
        print("3 - Prompt Settings")
        print("4 - Select AI Model")
        print("5 - System Prompt Settings")
        secim = input("Choose (1/2/3/4/5): ").strip()

        if secim == "2":
            site = input("🌐 Enter site URL: ").strip()
            xpath_input = input("✏️ Input XPath: ").strip()
            xpath_buton = input("📤 Send button XPath: ").strip()
            ayarlar = {
                "site": site,
                "input_xpath": xpath_input,
                "buton_xpath": xpath_buton
            }
            kaydet_ayarlar(ayarlar)
            print("✅ Settings saved.")
            continue

        elif secim == "3":
            continue

        elif secim == "4":
            model_sec()
            continue

        elif secim == "5":
            print("\n⚙️ System Prompt Settings:")
            print("1 - Add Line")
            print("2 - Delete Line")
            alt_secim = input("Choose (1/2): ").strip()
            if alt_secim == "1":
                system_prompt_ekle()
            elif alt_secim == "2":
                system_prompt_sil()
            else:
                print("❌ Invalid selection")
            continue

        elif secim == "1":
            break

        else:
            print("❌ Invalid selection")

    ayarlar = yukle_ayarlar()
    model = yukle_model()
    prompt_text = oku_system_prompt()

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
        print(f"❌ Chrome error: {e}")
        return

    driver.get(ayarlar["site"])
    print("🕒 AI will start in 60 seconds...")

    SAMPLE_RATE = 48000
    RECORD_SEC = 10
    use_file_index = 1

    system_prompt = {
        "role": "system",
        "content": prompt_text
    }
    chat_history = []
    follow_up_questions = []

    def build_prompt(user_input):
        chat_history.append({"role": "user", "content": user_input})
        return [system_prompt] + chat_history[-5:]

    def start_ai():
        nonlocal use_file_index
        while True:
            file_current = f"out{use_file_index}.wav"
            file_to_delete = f"out{(use_file_index % 3) + 1}.wav"

            try:
                with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                    sf.write(file_current, data[:, 0], samplerate=SAMPLE_RATE)
                    time.sleep(0.2)
            except Exception as e:
                print(f"🎙️ Recording error: {e}")
                continue

            try:
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)
            except Exception as e:
                print(f"🗑️ Delete error: {e}")

            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_current) as source:
                    audio = recognizer.record(source)
                turkish_text = recognizer.recognize_google(audio, language="tr-TR")
                print("🧑 (You):", turkish_text)
            except Exception as e:
                print(f"❌ Recognition error: {e}")
                use_file_index = (use_file_index % 3) + 1
                continue

            translated_text = translate(turkish_text, "en", "tr")
            prompt = build_prompt(translated_text)
            response = ollama.chat(model=model, messages=prompt)
            english_reply = response["message"]["content"].strip().split(".")[0].strip() + "."
            translated_reply = translate(english_reply, "tr", "en")

            if random.random() < 0.1:
                translated_reply += " " + random.choice(follow_up_questions)

            delay = delay_sure_belirle()
            if delay == "PASS":
                print("⏭️ Skipping message...")
                continue

            print(f"⌛ Reply in {delay} sec...")
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
                print("📤 Sent!")
            except Exception as msg_err:
                print(f"❗ Send error: {msg_err}")

            use_file_index = (use_file_index % 3) + 1

    threading.Timer(60, start_ai).start()
