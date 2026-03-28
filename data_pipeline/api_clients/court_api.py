import requests
import json

def fetch_trademark_judgments(keyword):
    """
    這是一個用來模擬去司法院抓取商標判決書的函數。
    """
    print("="*50)
    print(f"🚀 啟動爬蟲任務：尋找含有「{keyword}」的商標判決書...")
    print("="*50)

    # 為了測試我們的 requests 套件有沒有裝好，我們暫時先用一個安全的測試用 API
    # 等測試成功，我們之後再把它換成真實的政府開放資料 API 網址
    test_url = "https://httpbin.org/get"
    
    # 我們要把關鍵字打包，準備傳給伺服器
    payload = {
        "search_term": keyword,
        "law_article": "商標法第29條"
    }

    try:
        # 就像是用瀏覽器輸入網址一樣，我們用程式發送 GET 請求
        print("📡 正在連線至伺服器...")
        response = requests.get(test_url, params=payload)
        
        # 檢查伺服器有沒有正常回應 (狀態碼 200 代表成功)
        response.raise_for_status() 
        
        print("✅ 連線成功！\n")
        
        # 把伺服器回傳的東西轉成我們看得懂的 JSON 格式
        data = response.json()
        
        print("📥 伺服器看懂了我們的搜尋條件：")
        # 印出我們剛剛傳過去的參數，證明伺服器有收到
        print(json.dumps(data["args"], indent=4, ensure_ascii=False))
        
        print("\n💡 下一步：我們將在這裡寫入『拆解法官心證理由』的資料清洗邏輯！")

    except Exception as e:
        print(f"❌ 連線失敗發生錯誤: {e}")

# 這行代表「如果我們直接執行這個檔案，就跑下面的動作」
if __name__ == "__main__":
    # 我們拿機車產業最常碰到的避震器當作測試關鍵字
    fetch_trademark_judgments("機車避震器")