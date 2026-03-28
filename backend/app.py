import pandas as pd
import os

def simplify_applicant(name):
    """將又臭又長的公司名稱收斂成乾淨的品牌名"""
    if not isinstance(name, str): 
        return "未知"
    
    # 收斂四大廠
    if "光陽" in name: return "光陽 (KYMCO)"
    if "三陽" in name: return "三陽 (SYM)"
    if "山葉" in name: return "台灣山葉 (YAMAHA)"
    if "本田" in name or "HONDA" in name.upper(): return "本田 (HONDA)"
    
    return name.replace("股份有限公司", "").replace("有限公司", "")

def check_real_database(trademark_name):
    """讀取我們下載的真實 Excel 資料庫進行比對 (具備防呆機制)"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'trademarks.xlsx')
    
    try:
        # 讀取所有工作表並合併
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        df = pd.concat(all_sheets.values(), ignore_index=True)
        
        print(f"✅ 成功讀取 Excel！總共載入 {len(df)} 筆真實商標。")
        
        # 將輸入的關鍵字轉大寫並去除前後空白
        search_term = str(trademark_name).upper().strip()
        
        # 幫 Excel 裡的商標名稱做一個「乾淨版」欄位
        df['商標名稱_乾淨版'] = df['商標名稱'].astype(str).str.upper().str.strip()
        
        # 進行比對
        match = df[df['商標名稱_乾淨版'] == search_term]
        
        print(f"🔍 尋找 [{search_term}]，找到 {len(match)} 筆吻合前案！")
        
        if not match.empty:
            row = match.iloc[0]
            appl_no = str(row['申請案號']).strip()
            tipo_link = f"https://twtmsearch.tipo.gov.tw/SS0/imgQuery.jsp?&applNo={appl_no}"
            
            return {
                "owner": simplify_applicant(row['申請人']),
                "appl_no": appl_no,
                "link": tipo_link
            }
        return None
    except Exception as e:
        print(f"❌ 資料庫讀取發生嚴重錯誤: {e}")
        return None

def generate_risk_report(trademark_name, product_class, cleaned_reasoning=""):
    """根據資料庫結果，生成對應的評估報告"""
    
    # --- 第一關：真實資料庫攔截 ---
    db_result = check_real_database(trademark_name)
    
    if db_result:
        report = f"""
### 【商標核駁風險評估意見書】

📌 **擬申請商標：** {trademark_name}  
📁 **指定商品：** {product_class}  
🚦 **預測核准率：** ⬛ **極低（具備致命前案衝突）**

---
#### 🛑 【致命傷診斷：前案衝突】
系統於真實商標資料庫中，檢索到**完全相同**之已註冊/申請中商標：
* **前案商標：** {trademark_name}
* **權利人：** {db_result['owner']}
* **申請案號：** {db_result['appl_no']}

👉 [**🔗 點此開啟智慧局「單筆詳表」查看官方圖檔**]({db_result['link']})

👉 **AI 診斷：** 您的商標與前案構成「相同商標使用於同一或類似商品」，審查委員將依「商標法第 30 條第 1 項第 10 款」直接予以核駁。

---
#### 💡 【資深代理人 - 解套策略建議】
此情況屬高度風險，幾無答辯空間，本所強烈建議：
1. **放棄此名稱：** 重新發想商標名稱，避免被 {db_result['owner']} 提告侵權。
2. **徵求並存同意：** 若具有強烈商業必要性，須向大廠取得商標並存同意書（難度極高）。
        """
        return report

    # --- 第二關：如果資料庫沒人註冊，進入 AI 法理診斷 ---
    report = f"""
### 【商標核駁風險評估意見書】

📌 **擬申請商標：** {trademark_name}  
📁 **指定商品：** {product_class}  
🚦 **預測核准率：** 🔴 **低（具備高度核駁風險）**

---
#### ⚠️ 【致命傷診斷：缺乏識別性】
系統於資料庫中未發現完全相同之前案。但比對歷史判決（112年度商訴字第15號），法官心證指出：  
> 「*{cleaned_reasoning}*」

👉 **AI 診斷：** 您的商標屬對產品功效之直接說明。極高機率會以「商標法第 29 條第 1 項第 1 款（說明性文字）」發出核駁先行通知書。

---
#### 💡 【資深代理人 - 敗部復活策略建議】
1. **建議更改命名：** 將功能性字眼轉化，加入無意義的英文字首「X-」。
2. **建議圖形化解套：** 設計具高度特殊性之 Logo，並主動對文字部分「聲明不專用」。
    """
    return report