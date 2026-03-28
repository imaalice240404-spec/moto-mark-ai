import json

def fetch_and_clean_judgments(keyword):
    print("="*50)
    print(f"🚀 啟動智財戰情室：尋找與「{keyword}」相關的商標判決...")
    print("="*50)

    # 模擬從司法院 API 抓回來的真實 JSON 資料結構
    # 實務上這會是一篇好幾千字的文言文判決書
    official_api_response = {
        "status": "success",
        "total_results": 1,
        "judgments": [
            {
                "case_num": "112年度商訴字第15號",
                "date": "2023-08-15",
                "sys": "行政/商標爭議",
                "full_text": "原告因商標註冊事件，不服經濟部訴願決定，提起行政訴訟。按商標法第29條第1項第1款規定，商品之通用名稱或說明性文字不得註冊。查原告申請之「極度避震」商標，指定使用於第12類機車避震器商品。消費者見此文字，其印象僅為商品避震功效之直接說明，並不具備商標之先天識別性。原處分予以核駁，並無違誤，原告之訴駁回。"
            }
        ]
    }

    print("📡 成功取得判決書原始檔！")
    print("⏳ 啟動「資深代理人視角」進行資料清洗與萃取...\n")

    # 這是系統最值錢的地方：資料清洗 (Data Cleaning)
    # 我們要把幾千字的廢話濾掉，只留下「法官心證」跟「實務標籤」
    for case in official_api_response["judgments"]:
        print(f"📜 正在分析案號：【{case['case_num']}】")
        
        # 1. 自動打上實務標籤 (Metadata Tagging)
        tags = []
        if "第29條" in case["full_text"] and "說明性" in case["full_text"]:
            tags.append("[識別性不足-說明性文字]")
        if "駁回" in case["full_text"] or "核駁" in case["full_text"]:
            tags.append("[維持核駁處分]")
            
        print(f"🏷️  系統自動標註：{', '.join(tags)}")

        # 2. 萃取法官心證 (擷取關鍵理由)
        # 我們讓程式自動找出「按商標法...」到「...識別性」這段精華
        start_keyword = "按商標法"
        end_keyword = "識別性。"
        
        start_idx = case["full_text"].find(start_keyword)
        end_idx = case["full_text"].find(end_keyword) + len(end_keyword)
        
        if start_idx != -1 and end_idx != -1:
            core_reason = case["full_text"][start_idx:end_idx]
            print(f"⚖️  法官心證淨化結果：\n   「{core_reason}」")
            print("-" * 50)
            print("💡 這段『淨化後的法官心證』，就是未來要存入向量資料庫，並餵給 AI 寫答辯報告的頂級燃料！")

if __name__ == "__main__":
    fetch_and_clean_judgments("機車避震器")