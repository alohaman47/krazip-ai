
import streamlit as st
import google.generativeai as genai
import datetime
import time

# --- Config ---
st.set_page_config(page_title="KraZip AI", layout="wide", page_icon="🍃")

st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
    .stApp { background-color: #F5F7F5; font-family: 'Sarabun', sans-serif; }
    h1, h2, h3, p, div, button, label { color: #14171A !important; }
    .post-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #ddd; margin-bottom: 15px; }
    .ai-reply { background-color: #E3F2FD; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-top: 10px; color: #0D47A1 !important;}
    </style>
''', unsafe_allow_html=True)

if 'posts' not in st.session_state:
    st.session_state['posts'] = []

def main():
    # --- Sidebar ---
    with st.sidebar:
        st.title("🔑 ตั้งค่า AI")
        api_key = st.text_input("1. ใส่ API Key ที่นี่", type="password")
        
        selected_model = None
        if api_key:
            st.success("✅ รับทราบ Key แล้ว")
            try:
                genai.configure(api_key=api_key)
                model_list = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        model_list.append(m.name)
                
                if model_list:
                    selected_model = st.selectbox("2. เลือกโมเดล", model_list, index=0)
                else:
                    st.error("ไม่พบโมเดล")
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        menu = st.radio("เมนู", ["🏠 หน้าแรก (Feed)", "🤖 ผู้ช่วยอัจฉริยะ"])

    # --- Main ---
    if not selected_model:
        st.info("👈 กรุณาใส่ API Key และเลือกโมเดลที่ด้านซ้ายก่อนเริ่มใช้งาน")
        return

    model_engine = genai.GenerativeModel(selected_model)

    if menu == "🏠 หน้าแรก (Feed)":
        st.title(f"🏠 KraZip Feed")
        with st.container():
            st.markdown('<div style="background:white; padding:20px; border-radius:15px;">', unsafe_allow_html=True)
            new_text = st.text_area("โพสต์ข้อความ... (AI พร้อมตอบ)", height=100)
            if st.button("✨ โพสต์เลย"):
                if new_text:
                    with st.spinner("AI กำลังพิมพ์ตอบ..."):
                        try:
                            response = model_engine.generate_content(f"ตอบกลับโพสต์นี้ในฐานะเพื่อนที่แสนดี สั้นๆ อบอุ่น: {new_text}")
                            st.session_state['posts'].insert(0, {"name": "คุณ", "content": new_text, "time": datetime.datetime.now().strftime("%H:%M"), "ai_comment": response.text})
                            st.rerun()
                        except Exception as e: st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        for post in st.session_state['posts']:
            st.markdown(f'<div class="post-card"><b>{post["name"]}</b><br>{post["content"]}<div class="ai-reply">🤖 <b>AI:</b> {post["ai_comment"]}</div></div>', unsafe_allow_html=True)

    elif menu == "🤖 ผู้ช่วยอัจฉริยะ":
        st.title("🤖 ถามจินี่ (AI)")
        q = st.text_area("ถามอะไรก็ได้ครับ...")
        if st.button("🚀 ส่งคำถาม"):
            with st.spinner("กำลังประมวลผล..."):
                try:
                    ans = model_engine.generate_content(q).text
                    st.markdown(f'<div class="post-card"><b>คำตอบ:</b><br>{ans}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
