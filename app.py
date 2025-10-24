import streamlit as st
import pandas as pd
import pickle
import os

# --- Config: ชื่อไฟล์โมเดล ---
MODEL_FILENAME = 'model-reg-67130701928.pkl'

# --- Step 1: ฟังก์ชันโหลดโมเดล (พร้อม Caching) ---
# @st.cache_resource จะเก็บโมเดลไว้ในหน่วยความจำ
# เพื่อไม่ให้ต้องโหลดใหม่ทุกครั้งที่มีการโต้ตอบกับหน้าเว็บ
@st.cache_resource
def load_model(model_path):
    """
    โหลดโมเดล .pkl จาก path ที่กำหนด
    คืนค่า model object ถ้าสำเร็จ, คืนค่า None ถ้าไม่สำเร็จ
    """
    if not os.path.exists(model_path):
        print(f"ข้อผิดพลาด: ไม่พบไฟล์โมเดล '{model_path}'")
        return None
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print(f"โหลดโมเดล '{model_path}' สำเร็จ")
        return model
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
        return None

# --- เริ่มสร้างหน้าเว็บ Streamlit ---
st.title('แอปคาดการณ์ยอดขาย (Sales Prediction App) 📈')
st.write(f"ใช้โมเดลที่ผ่านการเทรน (`{MODEL_FILENAME}`)")

# --- โหลดโมเดล ---
model = load_model(MODEL_FILENAME)

# --- ตรวจสอบว่าโหลดโมเดลสำเร็จหรือไม่ ---
if model is None:
    st.error(f"ข้อผิดพลาด: ไม่พบไฟล์โมเดล '{MODEL_FILENAME}'")
    st.warning("กรุณารันสคริปต์ 'regression_model.py' (หรือสคริปต์ที่ใช้สร้างโมเดล) เพื่อสร้างไฟล์โมเดลก่อน แล้วรีเฟรชหน้านี้")
else:
    st.success(f"โหลดโมเดล '{MODEL_FILENAME}' สำเร็จ!")

    # --- Step 2: สร้างฟอร์มสำหรับรับ Input ---
    st.header('กรุณาป้อนงบประมาณโฆษณา (Budget):')

    # ใช้ st.columns เพื่อจัดเลย์เอาต์ให้สวยงาม
    col1, col2, col3 = st.columns(3)

    with col1:
        # ใช้ value=50.0 เพื่อให้ค่าเริ่มต้นเป็น 50 เหมือนในโค้ดเดิม
        youtube_budget = st.number_input('YouTube', min_value=0.0, value=50.0, step=1.0, format="%.2f")

    with col2:
        tiktok_budget = st.number_input('TikTok', min_value=0.0, value=50.0, step=1.0, format="%.2f")

    with col3:
        instagram_budget = st.number_input('Instagram', min_value=0.0, value=50.0, step=1.0, format="%.2f")

    # --- Step 3: ปุ่มสำหรับทำนายผล ---
    st.divider() # เส้นคั่น

    if st.button('คำนวณยอดขาย (Predict Sales)', type="primary"):
        
        # สร้าง DataFrame จากข้อมูลที่ผู้ใช้ป้อน
        data_to_predict = {
            'youtube': [youtube_budget],
            'tiktok': [tiktok_budget],
            'instagram': [instagram_budget]
        }
        new_df = pd.DataFrame(data_to_predict)

        st.write("ข้อมูลที่ใช้คาดการณ์:")
        st.dataframe(new_df)

        # ทำนายผล
        try:
            prediction = model.predict(new_df)
            predicted_sales = prediction[0]

            # แสดงผลลัพธ์
            st.success(f"🎉 ผลการคาดการณ์ยอดขาย (Predicted Sales):")
            # st.metric ให้การแสดงผลตัวเลขที่สวยงาม
            st.metric(label="Sales Units (หน่วย)", value=f"{predicted_sales:,.2f}")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดระหว่างการทำนายผล: {e}")
            st.error("กรุณาตรวจสอบว่าชื่อคอลัมน์ (youtube, tiktok, instagram) ตรงกับที่โมเดลใช้ฝึก")

st.sidebar.info("นี่คือแอปที่สร้างโดย Streamlit เพื่อใช้โมเดล Machine Learning ที่คุณสร้างไว้")


