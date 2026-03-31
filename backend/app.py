import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import difflib
from pypinyin import lazy_pinyin
import chromadb # 🌟 導入向量資料庫

# --- 1. 喚醒 AI 靈魂 ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ 警告：找不到 GEMINI_API_KEY，請確認 .env 檔案！")
else:
    genai.configure(api_key=api_key)

# 🌟 連線到長期知識庫 (ChromaDB) 🌟
chroma_client = chromadb.PersistentClient(path="./chroma_db")
kb_collection = chroma_client.get_or_create_collection(name="trademark_cases")

# --- 2. 輔助與資料庫函數 ---
def simplify_applicant(name):
    if not isinstance(name, str): return "未知"
    name = str(name)
    if "光陽" in name: return "光陽 (KYMCO)"
    if "三陽" in name: return "三陽 (SYM)"
    if "山葉" in name: return "台灣山葉 (YAMAHA)"
    if "本田" in name or "HONDA" in name.upper(): return "本田 (HONDA)"
    return name.replace("股份有限公司", "").replace("有限公司", "")

def get_pinyin_string(text):
    if not isinstance(text, str): return ""
    return "".join(lazy_pinyin(str(text))).lower()

def check_real_database(trademark_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'trademarks.xlsx')
    try:
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        df = pd.concat(all_sheets.values(), ignore_index=True)
        
        search_term_clean = str(trademark_name).upper().replace(" ", "").strip()
        df['商標名稱_淨身版'] = df['商標名稱'].astype(str).str.upper().str.replace(" ", "", regex=False).str.strip()
        
        search_term_pinyin = get_pinyin_string(search_term_clean)
        df['商標名稱_拼音'] = df['商標名稱_淨身版'].apply(get_pinyin_string)
        
        all_clean_names = df['商標名稱_淨身版'].dropna().unique().tolist()
        
        # 🚀 三引擎全開雷達 🚀
        contains_matches = [name for name in all_clean_names if search_term_clean in name]
        fuzzy_matches = difflib.get_close_matches(search_term_clean, all_clean_names, n=5, cutoff=0.6)
        pinyin_matches = df[df['商標名稱_拼音'].str.contains(search_term_pinyin, na=False)]['商標名稱_淨身版'].tolist() if search_term_pinyin else []
        
        combined_matches = list(set(contains_matches + fuzzy_matches + pinyin_matches))
        
        if combined_matches:
            match = df[df['商標名稱_淨身版'].isin(combined_matches)]
            results = []
            for _, row in match.head(3).iterrows(): # 最多抓 3 筆前案
                appl_no = str(row['申請案號']).strip()
                results.append({
                    "name": row['商標名稱'],
                    "owner": simplify_applicant(row['申請人']),
                    "link": f"https://twtmsearch.tipo.gov.tw/SS0/imgQuery.jsp?&applNo={appl_no}"
                })
            return results
        return None
    except Exception as e:
        print(f"❌ 資料庫讀取發生嚴重錯誤: {e}")
        return None

# --- 3. 核心大腦：結合長期知識庫與 TIPO 八大因素的報告生成 ---
def generate_risk_report(trademark_name, product_class):
    db_results = check_real_database(trademark_name)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 🌟 自動檢索 RAG 魔法 🌟
    # 系統自動去資料庫找出最相關的歷史經驗
    results = kb_collection.query(
        query_texts=[trademark_name],
        n_results=1
    )
    
    retrieved_case_law = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        retrieved_case_law = results['documents'][0][0]

    formatting_rules = """
    【視覺排版與專業深度並重紀律】
    1. 報告結構必須嚴格遵守以下板塊：🚦 **核心結論**、🛑 **前案衝突列表** (必須用Markdown表格)、⚖️ **TIPO 審查基準與歷史經驗分析**、💡 **代理人解套策略**。
    2. 在「⚖️ TIPO 審查基準與歷史經驗分析」中，**絕對不要只寫一句話**！請將【長期知識庫檢索結果】的經驗完美融合進你的法理論述中，用 3~4 句話進行具備法理深度的論述。
    3. 論述時，請善用**粗體字**標示關鍵法理詞彙（例如：**異時異地隔離觀察**、**連貫唱呼**、**高度知名度**、**先天識別性**）。
    4. 絕對禁止信件廢話（無問候語、結語、署名）。
    """

    tipo_rules = """
    【TIPO 官方「混淆誤認之虞」審查基準 (深入論述要求)】
    請挑選最致命的 3~4 個因素進行深度法理論述：
    1. 商標是否近似：若為讀音相同(如優隔/優格)或外觀近似(如U/V)，請明確指出在「異時異地隔離觀察」及「連貫唱呼」下，消費者極易產生混淆。
    2. 消費者對商標熟悉度：前案若為國內知名車廠(光陽/三陽/山葉/本田)，應強調其商標具備高度知名度，受保護範圍較廣，他人稍有近似即構成混淆。
    3. 商標識別性之強弱：前案若為獨創性詞彙，請說明其具備強烈之先天識別性，審查時會給予較大保護。
    """

    rag_section = f"【長期知識庫檢索結果 (本所歷史經驗)】：\n{retrieved_case_law}\n" if retrieved_case_law else ""

    if db_results:
        conflict_info = ""
        for i, res in enumerate(db_results):
            conflict_info += f"- 商標：「{res['name']}」 | 權利人：「{res['owner']}」 | 連結：{res['link']}\n"
        
        prompt = f"""
        擬申請商標：「{trademark_name}」 (類別：「{product_class}」)
        
        【系統檢索結果：發現高度近似商標】
        {conflict_info}
        
        {rag_section}
        
        請撰寫評估報告，包含：
        1. 🚦 預測核准率：極低（具備前案衝突風險）。
        2. ⚖️ TIPO 審查基準與歷史經驗分析：
           {tipo_rules}
           請具體說明為何「{trademark_name}」與前案構成混淆，並「強烈引用」長期知識庫的歷史經驗來佐證觀點。如果字形不同但讀音相同，務必點出「讀音完全相同，消費者聽覺上極易混淆」，並附上前案官方連結。
        3. 💡 代理人解套策略：給出 2 個具體解套建議。
        
        {formatting_rules}
        """
    else:
        prompt = f"""
        擬申請商標：「{trademark_name}」 (類別：「{product_class}」)
        【系統檢索結果】：未發現近似前案。
        
        {rag_section}
        
        請撰寫評估報告，包含：
        1. 🚦 預測核准率：依據法理給出 (高/中/低)。
        2. ⚖️ 識別性風險深入分析：深度評估是否違反商標法第29條第1項第1款(說明性文字)，或說明其為何具備先天識別性。並參考歷史經驗進行補充。
        3. 💡 代理人解套/優化策略：給出 2 個註冊策略。
        
        {formatting_rules}
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI 報告生成失敗：{e}"