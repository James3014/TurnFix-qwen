"""
資料準備工具集 CLI 主入口點 (TOOL-101 到 TOOL-107)

實現命令列工具以處理教練答覆和影片逐字稿
"""
import argparse
import json
import os
import sys
from typing import List, Dict, Any
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_coach_responses(input_dir: str, output_dir: str):
    """
    清洗教練答覆資料 (TOOL-101.1)
    
    移除格式化符號、正規化日期、標準化單位
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
    """
    logger.info(f"開始清洗教練答覆資料: {input_dir} -> {output_dir}")
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 處理輸入目錄中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(('.txt', '.md')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"cleaned_{filename}")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 清洗內容
                cleaned_content = preprocess_coach_response(content)
                
                # 保存清洗後的內容
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                logger.info(f"成功清洗文件: {filename}")
                
            except Exception as e:
                logger.error(f"清洗文件 {filename} 時出錯: {e}")

def preprocess_coach_response(text: str) -> str:
    """
    預處理教練答覆 (TOOL-101.1)
    
    Args:
        text: 原始教練答覆文本
        
    Returns:
        str: 清洗後的文本
    """
    try:
        # 移除格式化符號
        cleaned_text = text.replace("*", "").replace("_", "").replace("~", "")
        
        # 正規化日期格式
        import re
        # 將各種日期格式統一為 YYYY-MM-DD
        date_patterns = [
            (r'\d{4}/\d{1,2}/\d{1,2}', lambda m: m.group().replace('/', '-')),
            (r'\d{1,2}/\d{1,2}/\d{4}', lambda m: '-'.join(reversed(m.group().split('/')))),
        ]
        
        for pattern, replacer in date_patterns:
            cleaned_text = re.sub(pattern, replacer, cleaned_text)
        
        # 標準化單位
        unit_patterns = [
            (r'(\d+)\s*kg', r'\1 公斤'),
            (r'(\d+)\s*m', r'\1 公尺'),
            (r'(\d+)\s*cm', r'\1 公分'),
        ]
        
        for pattern, replacement in unit_patterns:
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"預處理教練答覆時出錯: {e}")
        # 降級策略：返回原始文本
        return text

def clean_video_transcripts(input_dir: str, output_dir: str):
    """
    清洗影片逐字稿 (TOOL-101.2)
    
    移除時間戳記、合併斷句、檢測語言
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
    """
    logger.info(f"開始清洗影片逐字稿: {input_dir} -> {output_dir}")
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 處理輸入目錄中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(('.txt', '.md')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"cleaned_{filename}")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 清洗內容
                cleaned_content = preprocess_video_transcript(content)
                
                # 保存清洗後的內容
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                logger.info(f"成功清洗影片逐字稿: {filename}")
                
            except Exception as e:
                logger.error(f"清洗影片逐字稿 {filename} 時出錯: {e}")

def preprocess_video_transcript(text: str) -> str:
    """
    預處理影片逐字稿 (TOOL-101.2)
    
    Args:
        text: 原始影片逐字稿文本
        
    Returns:
        str: 清洗後的文本
    """
    try:
        # 移除時間戳記 (格式：[00:01:23] 或 00:01:23)
        import re
        cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
        cleaned_text = re.sub(r'\d{2}:\d{2}:\d{2}', '', cleaned_text)
        
        # 合併斷句
        # 移除過多的換行符，保留段落分隔
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        # 檢測語言 (簡化實現)
        # 在實際實現中，這會使用語言檢測庫
        language = "zh"  # 預設為中文
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"預處理影片逐字稿時出錯: {e}")
        # 降級策略：返回原始文本
        return text

def segment_text(text: str) -> List[str]:
    """
    文本分段邏輯 (TOOL-101.3)
    
    基於句子或段落分段，保留足夠上下文以供知識抽取
    
    Args:
        text: 原始文本
        
    Returns:
        List[str]: 分段後的文本列表
    """
    try:
        # 基於段落分段
        paragraphs = text.split('\n\n')
        
        # 移除空段落和過短段落
        segments = [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 10]
        
        return segments
        
    except Exception as e:
        logger.error(f"分段文本時出錯: {e}")
        # 降級策略：按句子分段
        import re
        sentences = re.split(r'[。！？]', text)
        segments = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return segments if segments else [text]

def extract_knowledge_from_coach_responses(input_dir: str, output_dir: str):
    """
    從教練答覆中自動提取知識 (DM-250)
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
    """
    logger.info(f"開始從教練答覆中提取知識: {input_dir} -> {output_dir}")
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 處理輸入目錄中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(('.txt', '.md')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"extracted_{filename}.json")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取知識
                extracted_knowledge = extract_knowledge_from_text(content)
                
                # 保存提取的知識
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted_knowledge, f, ensure_ascii=False, indent=2)
                
                logger.info(f"成功提取知識: {filename}")
                
            except Exception as e:
                logger.error(f"提取知識 {filename} 時出錯: {e}")

def extract_knowledge_from_text(text: str) -> Dict[str, Any]:
    """
    從文本中提取知識 (DM-250.1 到 DM-250.4)
    
    Args:
        text: 原始文本
        
    Returns:
        Dict[str, Any]: 提取的知識結構
    """
    try:
        # 簡化實現：模擬知識提取
        # 實際實現中會使用NLP技術
        
        # 提取症狀描述
        symptoms = extract_symptoms(text)
        
        # 提取練習建議
        practice_tips = extract_practice_tips(text)
        
        # 建立結構化知識表示
        knowledge_structure = create_knowledge_structure(symptoms, practice_tips)
        
        # 標記為待審核
        knowledge_structure["status"] = "pending_review"
        
        return knowledge_structure
        
    except Exception as e:
        logger.error(f"提取知識時出錯: {e}")
        # 降級策略：返回空結構
        return {
            "symptoms": [],
            "practice_tips": [],
            "knowledge_structure": {},
            "status": "error"
        }

def extract_symptoms(text: str) -> List[str]:
    """
    症狀抽取 (DM-250.1)
    
    Args:
        text: 原始文本
        
    Returns:
        List[str]: 抽取的症狀關鍵詞和描述
    """
    # 簡化實現：使用關鍵詞匹配
    keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
    symptoms = []
    
    for keyword in keywords:
        if keyword in text:
            symptoms.append(keyword)
    
    return symptoms

def extract_practice_tips(text: str) -> List[Dict[str, Any]]:
    """
    練習建議抽取 (DM-250.2)
    
    Args:
        text: 原始文本
        
    Returns:
        List[Dict[str, Any]]: 抽取的練習建議
    """
    # 簡化實現：模擬練習建議抽取
    tips = [
        {"action": "視線外緣", "description": "保持視線在外緣方向"},
        {"action": "外腳 70–80%", "description": "外腳承重 70–80%"},
        {"action": "中立後換刃", "description": "通過中立位置後再換刃"}
    ]
    
    return tips

def create_knowledge_structure(symptoms: List[str], 
                            practice_tips: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    建立結構化知識表示 (DM-250.3)
    
    Args:
        symptoms: 症狀列表
        practice_tips: 練習建議列表
        
    Returns:
        Dict[str, Any]: 結構化知識表示
    """
    # 簡化實現：建立基本知識結構
    return {
        "symptom_descriptions": symptoms,
        "practice_recommendations": practice_tips,
        "knowledge_mapping": {
            "symptom_to_practice": {symptom: [tip["action"] for tip in practice_tips] for symptom in symptoms}
        }
    }

def validate_extracted_knowledge(input_dir: str, output_dir: str):
    """
    驗證提取的知識品質 (TOOL-103)
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
    """
    logger.info(f"開始驗證提取的知識品質: {input_dir} -> {output_dir}")
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 處理輸入目錄中的所有JSON文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"validated_{filename}")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    knowledge_data = json.load(f)
                
                # 驗證知識品質
                validation_report = validate_knowledge_quality(knowledge_data)
                
                # 保存驗證報告
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(validation_report, f, ensure_ascii=False, indent=2)
                
                logger.info(f"成功驗證知識品質: {filename}")
                
            except Exception as e:
                logger.error(f"驗證知識品質 {filename} 時出錯: {e}")

def validate_knowledge_quality(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證知識品質 (TOOL-103.1 到 TOOL-103.3)
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 驗證報告
    """
    try:
        # 檢查症狀名稱唯一性和格式一致性 (TOOL-103.1)
        symptom_names = knowledge_data.get("symptom_descriptions", [])
        unique_symptoms = len(set(symptom_names))
        total_symptoms = len(symptom_names)
        
        # 驗證練習建議的完整性 (TOOL-103.2)
        practice_tips = knowledge_data.get("practice_recommendations", [])
        complete_tips = all("action" in tip and "description" in tip for tip in practice_tips)
        
        # 生成驗證報告，標記異常記錄 (TOOL-103.3)
        report = {
            "validation_status": "success",
            "symptom_uniqueness": {
                "unique_count": unique_symptoms,
                "total_count": total_symptoms,
                "consistency": unique_symptoms == total_symptoms
            },
            "practice_completeness": {
                "complete_tips": complete_tips,
                "tip_count": len(practice_tips)
            },
            "anomalies": []
        }
        
        # 檢查異常記錄
        if not complete_tips:
            report["anomalies"].append("練習建議缺少必要的字段")
        
        if unique_symptoms != total_symptoms:
            report["anomalies"].append("症狀名稱存在重複")
        
        # 檢查描述長度
        for symptom in symptom_names:
            if len(symptom) < 2:
                report["anomalies"].append(f"症狀描述過短: {symptom}")
        
        for tip in practice_tips:
            if len(tip.get("description", "")) < 5:
                report["anomalies"].append(f"練習建議描述過短: {tip.get('action', '')}")
        
        return report
        
    except Exception as e:
        logger.error(f"驗證知識品質時出錯: {e}")
        # 降級策略：返回錯誤報告
        return {
            "validation_status": "error",
            "message": f"驗證知識品質時出錯: {str(e)}"
        }

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="TurnFix 資料準備工具集")
    parser.add_argument("command", choices=["clean", "extract", "validate", "import"], 
                       help="要執行的命令")
    parser.add_argument("--input", required=True, help="輸入目錄")
    parser.add_argument("--output", required=True, help="輸出目錄")
    parser.add_argument("--review-mode", action="store_true", 
                       help="進入人工審核模式")
    
    args = parser.parse_args()
    
    if args.command == "clean":
        # 清洗資料
        clean_coach_responses(args.input, args.output)
        clean_video_transcripts(args.input, args.output)
    elif args.command == "extract":
        # 提取知識
        extract_knowledge_from_coach_responses(args.input, args.output)
    elif args.command == "validate":
        # 驗證知識品質
        validate_extracted_knowledge(args.input, args.output)
    elif args.command == "import":
        # 導入知識庫
        logger.info(f"導入知識庫: {args.input} -> {args.output}")
        # 這裡會實現知識庫導入邏輯
    
    logger.info("資料準備工具執行完成")

if __name__ == "__main__":
    main()