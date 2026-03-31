import chromadb
import os

# 1. 建立或連線到本機端的向量資料庫 (它會在你的專案裡建立一個 chroma_db 資料夾)
client = chromadb.PersistentClient(path="./chroma_db")

# 2. 創建一個專屬的「商標歷史案件」書櫃
collection = client.get_or_create_collection(name="trademark_cases")

# 3. 準備你要灌錄的歷史經驗 (實務上這裡會寫程式去自動讀取你的 Word/PDF 資料夾)
# 這裡我先幫你寫好三個「頂級歷史經驗」作為測試種子
historical_cases = [
    {
        "id": "case_001",
        "title": "優格 vs 優隔 - 讀音高度近似核駁案",
        "content": "【歷史答辯經驗】：在中文字商標中，若字形完全不同但讀音相同（如優格與優隔），在連貫唱呼及異時異地隔離觀察下，極易導致消費者混淆。本所過去處理此類案件時，若無法證明兩商標在市場上已有明顯區隔，通常建議客戶直接放棄文字，改以極具獨創性之圖形作為主要識別標識申請。"
    },
    {
        "id": "case_002",
        "title": "KRV vs KRU - 外觀近似與字首法則",
        "content": "【歷史答辯經驗】：針對英文字母商標，智慧局審查時極度看重「字首相同」與「特定字母形似」。實務上，字母 U 與 V、I 與 1、O 與 0 在視覺上極易混淆。本所在處理 KRV 相關案件時發現，只要前兩碼 KR 相同，且字尾為形似的 U/V，審查委員幾乎 100% 判定構成外觀近似。解套策略通常需要取得大廠的並存同意書。"
    },
    {
        "id": "case_003",
        "title": "大廠保護傘條款 - 光陽/三陽知名度",
        "content": "【歷史答辯經驗】：若前案權利人為國內知名機車大廠（如光陽 KYMCO、三陽 SYM、山葉 YAMAHA），其商標具備高度市場熟悉度。在此情況下，審查基準的「消費者對商標熟悉度」因素權重會大幅提升。他人申請之商標即使僅有微小近似，也會因前案保護範圍廣泛而被核駁。"
    }
]

# 4. 把資料灌進資料庫！
print("📦 正在將歷史案件轉換為向量並存入資料庫...")
for case in historical_cases:
    collection.upsert(
        documents=[case["content"]],
        metadatas=[{"title": case["title"]}],
        ids=[case["id"]]
    )

print(f"✅ 知識庫建立完成！目前資料庫共有 {collection.count()} 筆歷史經驗。")