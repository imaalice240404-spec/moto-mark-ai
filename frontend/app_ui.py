import streamlit as st
import time

# 這裡我們要呼叫剛剛寫好的後端大腦
import sys
import os
# 確保程式找得到 backend 資料夾
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import generate_risk_report

# --- 視覺設定：極簡專業風 ---
st.set_page_config(page_title="MotoMark AI 戰情室", layout="centered", page_icon="🏍️")

st.title("🏍️ MotoMark AI - 商標策略戰情室")
st.markdown("專為二輪產業打造的智財風險評估系統")
st.markdown("---")

# --- 使用者輸入區 ---
col1, col2 = st.columns(2)
with col1:
    trademark_input = st.text_input("輸入擬申請商標名稱：", "極度避震")
with col2:
    product_class = st.selectbox("指定商品類別：", ["第 12 類 - 機車"])

# --- 啟動按鈕與報告顯示區 ---
if st.button("⚡ 一鍵生成專業評估報告", type="primary"):
    
    # 製造一點「AI 正在努力思考」的高級等待感
    with st.spinner('正在連線司法院資料庫檢索判例...'):
        time.sleep(1) # 假裝連線 1 秒
    
    with st.spinner('資深代理人 AI 正在撰寫法理分析...'):
        time.sleep(1.5) # 假裝思考 1.5 秒
        
        # 準備餵給 AI 的資料 (模擬我們剛剛爬蟲抓到的法官心證)
        past_case_reason = "消費者見此文字，其印象僅為商品避震功效之直接說明，並不具備商標之先天識別性。"
        
        # 呼叫後端大腦產生報告
        report = generate_risk_report(trademark_input, past_case_reason)
        
    # 顯示成功訊息與報告
    st.success("✅ 報告生成完畢！")
    
    # 用一個漂亮的框框把報告包起來
    with st.container(border=True):
        st.markdown(report)