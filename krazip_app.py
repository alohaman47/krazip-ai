import streamlit as st
import google.generativeai as genai
import datetime

# --- Config ---
st.set_page_config(page_title="KraZip AI", layout="wide", page_icon="🍃")

# CSS ตกแต่ง
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
    .stApp { background-color: #F5F7F5; font-family: 'Sarabun', sans-serif; }
    h1, h2, h3, p, div, button { color: #14171A !important; }
    .post-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #ddd; margin-bottom: 15px; }
    .ai-reply { background-color: #E3F2FD; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-top: 10px; color: #0D47A1 !important;}
    </style>
''', unsafe_allow_html=True)

if 'posts' not in st.session_state:
    st.session_state['posts'] = []

def main():
    # --- Sidebar ---
    with st.sidebar:
        st.title("ตั้งค่า AI")
        
        # --- 🟢 จุดสำคัญ: ระบบ Auto-Login ---
        # มันจะเช็คว่าในตู้เซฟ (Secrets) มีกุญแจไหม?
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ เชื่อมต่ออัตโนมัติ (VIP)")
        else:
            # ถ้าไม่มีในตู้เซฟ ค่อยถามหาจากคน
            api_key = st.text_input("ใส่ API Key", type="password")
        
        # เชื่อมต่อ Google
        selected_model = None
        if api_key:
            try:
                genai.configure(api_key=api_key)
                # เลือกโมเดลให้อัตโนมัติ (เอาตัวฟรี Flash)
                selected_model = 'gemini-1.5-flash' 
            except Exception as e:
                st.error("API Key ผิดพลาด")

        st.markdown("---")
        menu = st.radio("เมนู", ["🏠 หน้าแรก (Feed)", "🤖 ผู้ช่วยอัจฉริยะ"])

    # --- Main Content ---
    if not selected_model:
        st.info("👈 กำลังเชื่อมต่อระบบ... (ถ้าหน้านี้นานเกินไป ให้เช็ค API Key ใน Secrets)")
        return

    model = genai.GenerativeModel(selected_model)

    if menu == "🏠 หน้าแรก (Feed)":
        st.title("🏠 KraZip Feed")
        with st.container():
            st.markdown('<div style="background:white; padding:20px; border-radius:15px;">', unsafe_allow_html=True)
            new_text = st.text_area("โพสต์ข้อความ...", height=100)
            if st.button("✨ โพสต์เลย"):
                if new_text:
                    try:
                        reply = model.generate_content(f"ตอบกลับโพสต์นี้อย่างเป็นกันเอง: {new_text}").text
                        st.session_state['posts'].insert(0, {"name": "คุณ", "content": new_text, "ai_comment": reply})
                        st.rerun()
                    except: st.error("AI คิดไม่ออก")
            st.markdown('</div>', unsafe_allow_html=True)
        
        for post in st.session_state['posts']:
            st.markdown(f'<div class="post-card"><b>{post["name"]}</b><br>{post["content"]}<div class="ai-reply">🤖 {post["ai_comment"]}</div></div>', unsafe_allow_html=True)

    elif menu == "🤖 ผู้ช่วยอัจฉริยะ":
        st.title("🤖 ผู้ช่วยส่วนตัว")
        q = st.text_area("ถามอะไรก็ได้...")
        if st.button("🚀 ส่งคำถาม"):
            try:
                ans = model.generate_content(q).text
                st.markdown(f'<div class="post-card"><b>ตอบ:</b><br>{ans}</div>', unsafe_allow_html=True)
            except: st.error("เกิดข้อผิดพลาด")

if __name__ == "__main__":
    main()
