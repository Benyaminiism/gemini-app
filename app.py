import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ۱. بارگذاری کلید API از فایل .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ۲. تنظیمات صفحه Streamlit
st.set_page_config(page_title="دستیار متنی جمینای", page_icon="🤖")
st.title("🤖 دستیار متنی هوشمند با Gemini")
st.write("متن خود را وارد کنید تا هوش مصنوعی آن را پردازش کند.")

# ۳. راه‌اندازی کلاینت جدید Gemini
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("لطفاً کلید GEMINI_API_KEY را تنظیم کنید.")
    st.stop()

# ۴. فرم دریافت ورودی از کاربر
user_input = st.text_area("متن خود را اینجا بنویسید:", height=200)
option = st.selectbox(
    "می‌خواهید چه عملیاتی انجام شود؟",
    ["خلاصه‌سازی متن", "اصلاح و بهبود لحن", "استخراج نکات کلیدی"]
)

# ۵. دکمه پردازش و فراخوانی API
if st.button("پردازش با Gemini"):
    if not user_input.strip():
        st.warning("لطفاً ابتدا متنی را وارد کنید.")
    else:
        prompts = {
            "خلاصه‌سازی متن": f"لطفاً متن زیر را به صورت روان و کوتاه خلاصه کن:\n\n{user_input}",
            "اصلاح و بهبود لحن": f"لطفاً لحن متن زیر را حرفه‌ای و بدون غلط نگارشی بازنویسی کن:\n\n{user_input}",
            "استخراج نکات کلیدی": f"نکات اصلی و مهم متن زیر را به صورت بالت‌پوینت لیست کن:\n\n{user_input}"
        }
        
        prompt = prompts[option]

        with st.spinner("در حال پردازش توسط Gemini..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                )
                st.success("پردازش با موفقیت انجام شد:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"خطایی رخ داد: {e}")
