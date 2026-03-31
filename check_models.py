import os
import google.generativeai as genai
from dotenv import load_dotenv

# 讀取你的隱形保險箱
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 找不到 API Key，請確認 .env 檔案與變數名稱！")
else:
    genai.configure(api_key=api_key)
    print("✅ API Key 讀取成功！正在連線 Google 伺服器盤點模型...\n")
    print("-" * 30)
    
    try:
        # 詢問 Google 伺服器
        for m in genai.list_models():
            # 我們只印出「可以生成文字」的模型
            if 'generateContent' in m.supported_generation_methods:
                print(f"可用模型：{m.name}")
        print("-" * 30)
    except Exception as e:
        print(f"❌ 連線失敗，錯誤訊息：{e}")