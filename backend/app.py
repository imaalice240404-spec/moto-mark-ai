def check_mock_database(trademark_name, product_class):
    """
    這是一個模擬的智慧局商標資料庫。
    實務上，未來這段程式碼會被替換成呼叫 TIPO API 的邏輯。
    """
    # 這裡我們只放第 12 類機車相關的真實商標來模擬
    mock_db = {
        "KRV": {"owner": "光陽工業股份有限公司", "status": "註冊核准", "class": "第 12 類 - 機車"},
        "DRG": {"owner": "三陽工業股份有限公司", "status": "註冊核准", "class": "第 12 類 - 機車"},
        "JET": {"owner": "三陽工業股份有限公司", "status": "註冊核准", "class": "第 12 類 - 機車"}
    }
    
    # 如果名字一模一樣，且類別一樣，就回傳命中資料
    if trademark_name.upper() in mock_db and "12" in product_class:
        return mock_db[trademark_name.upper()]
    return None

def generate_risk_report(trademark_name, product_class, cleaned_reasoning=""):
    print("="*60)
    print(f"🧠 AI 代理人正在評估商標「{trademark_name}」 (指定：{product_class})...")
    print("="*60)

    # --- 第一關：資料庫「絕對死刑」攔截 ---
    db_result = check_mock_database(trademark_name, product_class)
    
    if db_result:
        # 如果在資料庫找到了，直接判定商標法第 30 條第 1 項第 10 款 (近似衝突)
        report = f"""
### 【商標核駁風險評估意見書】

📌 **擬申請商標：** {trademark_name}  
📁 **指定商品：** {product_class}  
🚦 **預測核准率：** ⬛ **極低（具備致命前案衝突）**

---
#### 🛑 【致命傷診斷：前案衝突】
系統於智慧局資料庫中檢索到**完全相同**之已註冊商標：
* **前案商標：** {trademark_name}
* **權利人：** {db_result['owner']}
* **案件狀態：** {db_result['status']}

👉 **AI 診斷：** 您的商標與前案構成「相同商標使用於同一或類似商品」，審查委員將依「商標法第 30 條第 1 項第 10 款」直接予以核駁。

---
#### 💡 【資深代理人 - 解套策略建議】
此情況屬高度風險，幾無答辯空間，本所強烈建議：
1. **放棄此名稱：** 重新發想商標名稱，避免侵權訴訟風險。
2. **徵求並存同意：** 若具有強烈商業必要性，須向「{db_result['owner']}」取得商標並存同意書（難度極高）。
        """
        return report

    # --- 第二關：如果資料庫沒人註冊，進入 AI 法理診斷 (例如：極度避震) ---
    report = f"""
### 【商標核駁風險評估意見書】

📌 **擬申請商標：** {trademark_name}  
📁 **指定商品：** {product_class}  
🚦 **預測核准率：** 🔴 **低（具備高度核駁風險）**

---
#### ⚠️ 【致命傷診斷：缺乏識別性】
系統未發現完全相同之前案，但比對歷史判決（112年度商訴字第15號），法官心證指出：  
> 「*{cleaned_reasoning}*」

👉 **AI 診斷：** 您的商標屬對產品功效之直接說明。極高機率會以「商標法第 29 條第 1 項第 1 款（說明性文字）」發出核駁先行通知書。

---
#### 💡 【資深代理人 - 敗部復活策略建議】
1. **建議更改命名：** 將功能性字眼轉化，加入無意義的英文字首「X-」。
2. **建議圖形化解套：** 設計具高度特殊性之 Logo，並主動對文字部分「聲明不專用」。
    """
    return report