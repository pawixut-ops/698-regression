import streamlit as st
import pandas as pd
import pickle
import os

--- 1. ฟังก์ชันโหลดโมเดล (ใช้ Cache เพื่อความเร็ว) ---

ใช้ @st.cache_resource สำหรับโหลดโมเดล

@st.cache_resource
def load_model(filename):
"""
โหลดโมเดลจากไฟล์ .pkl
คืนค่า None ถ้าไม่พบไฟล์หรือมีข้อผิดพลาด
"""
try:
# ตรวจสอบว่าไฟล์มีอยู่จริง
if not os.path.exists(filename):
st.error(f"ข้อผิดพลาด: ไม่พบไฟล์โมเดล '{filename}'")
st.info("กรุณารันสคริปต์ 'regression_model.py' เพื่อสร้างไฟล์โมเดลก่อน")
return None

    # เปิดและโหลดโมเดล
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model
    
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
    return None


--- 2. ส่วนหลักของแอป Streamlit ---

st.title('แอปคาดการณ์ยอดขาย (Sales Prediction App)')

โหลดโมเดล

model_filename = 'model-reg-67130701928.pkl'
model = load_model(model_filename)

--- 3. ตรวจสอบว่าโหลดโมเดลสำเร็จหรือไม่ ---

if model is None:
st.warning("ไม่สามารถเริ่มการคาดการณ์ได้ กรุณาตรวจสอบไฟล์โมเดล")
st.stop() # หยุดการทำงานของแอปหากโหลดโมเดลไม่สำเร็จ
else:
st.success(f"โหลดโมเดล '{model_filename}' สำเร็จ!")

# --- 4. ส่วนรับข้อมูลจากผู้ใช้ ---
st.header('ป้อนงบโฆษณา (บาท)')

# ใช้ st.columns เพื่อจัดวาง 3 ช่อง
col1, col2, col3 = st.columns(3)

with col1:
    # Step 2 (แบบรับค่า): รับค่า youtube
    youtube = st.number_input('YouTube', min_value=0.0, value=50.0, step=1.0)

with col2:
    # Step 2 (แบบรับค่า): รับค่า tiktok
    tiktok = st.number_input('TikTok', min_value=0.0, value=50.0, step=1.0)

with col3:
    # Step 2 (แบบรับค่า): รับค่า instagram
    instagram = st.number_input('Instagram', min_value=0.0, value=50.0, step=1.0)

# --- 5. ปุ่มและการคาดการณ์ ---
# เมื่อผู้ใช้กดปุ่ม
if st.button('คำนวณยอดขาย', type="primary"):
    try:
        # สร้าง DataFrame ใหม่จากข้อมูลที่ผู้ใช้ป้อน
        input_data = pd.DataFrame({
            'youtube': [youtube],
            'tiktok': [tiktok],
            'instagram': [instagram]
            # ตรวจสอบว่าชื่อคอลัมน์ตรงกับตอนฝึกโมเดล
        })
        
        # Step 3: ทำนายผล (คาดการณ์ 'sales')
        prediction = model.predict(input_data)
        predicted_sales = prediction[0]
        
        # แสดงผลลัพธ์
        st.subheader(f'ยอดขายที่คาดการณ์: {predicted_sales:,.2f} หน่วย')
    
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดระหว่างการคาดการณ์: {e}")
        st.info("กรุณาตรวจสอบว่าชื่อคอลัมน์ (youtube, tiktok, instagram) ตรงกับที่โมเดลใช้ฝึก")
