"""
資料準備工具集主入口點 (TOOL-106)

實現 CLI 主入口點與執行流程
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

def clean_command(args):
    """
    清洗命令 (TOOL-106.1)
    
    實現 `python cli.py clean --input ./data_in --output ./data_out` 命令
    """
    logger.info(f"開始清洗命令: {args.input} -> {args.output}")
    
    # 確保輸出目錄存在
    os.makedirs(args.output, exist_ok=True)
    
    # 處理輸入目錄中的所有文件
    for filename in os.listdir(args.input):
        if filename.endswith(('.txt', '.md')):
            input_path = os.path.join(args.input, filename)
            output_path = os.path.join(args.output, f"cleaned_{filename}")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 清洗內容
                cleaned_content = clean_text(content)
                
                # 保存清洗後的內容
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                logger.info(f"成功清洗文件: {filename}")
                
            except Exception as e:
                logger.error(f"清洗文件 {filename} 時出錯: {e}")

def clean_text(text: str) -> str:
    """
    清洗文本
    
    Args:
        text: 原始文本
        
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
        
        # 移除時間戳記
        cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', cleaned_text)
        cleaned_text = re.sub(r'\d{2}:\d{2}:\d{2}', '', cleaned_text)
        
        # 合併斷句
        # 移除過多的換行符，保留段落分隔
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        # 移除多餘空白
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"清洗文本時出錯: {e}")
        # 降級策略：返回原始文本
        return text

def extract_command(args):
    """
    提取命令 (TOOL-106.2)
    
    實現 `python cli.py extract --input ./data_out --review-mode` 命令
    """
    logger.info(f"開始提取命令: {args.input}")
    
    # 處理輸入目錄中的所有清洗後文件
    for filename in os.listdir(args.input):
        if filename.startswith("cleaned_") and filename.endswith(('.txt', '.md')):
            input_path = os.path.join(args.input, filename)
            output_filename = filename.replace("cleaned_", "extracted_") + ".json"
            output_path = os.path.join(args.input, output_filename)
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取知識
                extracted_knowledge = extract_knowledge_from_text(content)
                
                # 保存提取的知識
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted_knowledge, f, ensure_ascii=False, indent=2)
                
                logger.info(f"成功提取知識: {filename}")
                
                # 如果啟用審核模式，顯示提取結果
                if args.review_mode:
                    print(f"\n=== {filename} 提取結果 ===")
                    print(json.dumps(extracted_knowledge, ensure_ascii=False, indent=2))
                    
            except Exception as e:
                logger.error(f"提取知識 {filename} 時出錯: {e}")

def extract_knowledge_from_text(text: str) -> Dict[str, Any]:
    """
    從文本中提取知識
    
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
    症狀抽取
    
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
    練習建議抽取
    
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
    建立結構化知識表示
    
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

def validate_command(args):
    """
    驗證命令 (TOOL-106.3)
    
    實現 `python cli.py validate --input ./data_out` 命令
    """
    logger.info(f"開始驗證命令: {args.input}")
    
    # 處理輸入目錄中的所有提取文件
    validation_reports = []
    
    for filename in os.listdir(args.input):
        if filename.startswith("extracted_") and filename.endswith('.json'):
            input_path = os.path.join(args.input, filename)
            output_filename = filename.replace("extracted_", "validated_")
            output_path = os.path.join(args.input, output_filename)
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    knowledge_data = json.load(f)
                
                # 驗證知識品質
                validation_report = validate_knowledge_quality(knowledge_data)
                
                # 保存驗證報告
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(validation_report, f, ensure_ascii=False, indent=2)
                
                logger.info(f"成功驗證知識品質: {filename}")
                validation_reports.append(validation_report)
                
            except Exception as e:
                logger.error(f"驗證知識品質 {filename} 時出錯: {e}")
    
    # 生成總體驗證報告
    overall_report = generate_overall_validation_report(validation_reports)
    overall_report_path = os.path.join(args.input, "overall_validation_report.json")
    
    with open(overall_report_path, 'w', encoding='utf-8') as f:
        json.dump(overall_report, f, ensure_ascii=False, indent=2)
    
    logger.info("成功生成總體驗證報告")

def validate_knowledge_quality(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證知識品質
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 驗證報告
    """
    try:
        # 檢查症狀名稱唯一性和格式一致性
        symptom_names = knowledge_data.get("symptom_descriptions", [])
        unique_symptoms = len(set(symptom_names))
        total_symptoms = len(symptom_names)
        
        # 驗證練習建議的完整性
        practice_tips = knowledge_data.get("practice_recommendations", [])
        complete_tips = all("action" in tip and "description" in tip for tip in practice_tips)
        
        # 生成驗證報告，標記異常記錄
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

def generate_overall_validation_report(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成總體驗證報告
    
    Args:
        reports: 個別驗證報告列表
        
    Returns:
        Dict[str, Any]: 總體驗證報告
    """
    try:
        total_reports = len(reports)
        successful_reports = sum(1 for r in reports if r.get("validation_status") == "success")
        
        # 計算統計數據
        total_symptoms = sum(r.get("symptom_uniqueness", {}).get("total_count", 0) for r in reports)
        unique_symptoms = sum(r.get("symptom_uniqueness", {}).get("unique_count", 0) for r in reports)
        total_tips = sum(r.get("practice_completeness", {}).get("tip_count", 0) for r in reports)
        complete_tips = sum(1 for r in reports if r.get("practice_completeness", {}).get("complete_tips", False))
        
        # 計算異常記錄
        anomalies = []
        for report in reports:
            report_anomalies = report.get("anomalies", [])
            anomalies.extend(report_anomalies)
        
        return {
            "overall_validation_status": "success",
            "summary": {
                "total_reports": total_reports,
                "successful_reports": successful_reports,
                "validation_rate": round(successful_reports / total_reports * 100, 2) if total_reports > 0 else 0
            },
            "statistics": {
                "total_symptoms": total_symptoms,
                "unique_symptoms": unique_symptoms,
                "symptom_consistency": round(unique_symptoms / total_symptoms * 100, 2) if total_symptoms > 0 else 0,
                "total_tips": total_tips,
                "complete_tips": complete_tips,
                "tip_completion_rate": round(complete_tips / total_tips * 100, 2) if total_tips > 0 else 0
            },
            "anomalies": anomalies[:10]  # 只顯示前10個異常記錄
        }
        
    except Exception as e:
        logger.error(f"生成總體驗證報告時出錯: {e}")
        return {
            "overall_validation_status": "error",
            "message": f"生成總體驗證報告時出錯: {str(e)}"
        }

def import_command(args):
    """
    導入命令 (TOOL-106.4)
    
    實現 `python cli.py import --input ./data_out --chroma-db-path ./backend/chroma_db` 命令
    """
    logger.info(f"開始導入命令: {args.input} -> {args.chroma_db_path}")
    
    # 這里會實現知識庫導入邏輯
    # 實際實現中會調用 ChromaDB 導入功能
    print("知識庫導入功能正在開發中...")
    
    # 處理輸入目錄中的所有驗證通過文件
    for filename in os.listdir(args.input):
        if filename.startswith("validated_") and filename.endswith('.json'):
            input_path = os.path.join(args.input, filename)
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    validation_data = json.load(f)
                
                # 檢查驗證是否通過
                if validation_data.get("validation_status") == "success":
                    print(f"準備導入文件: {filename}")
                    # 這裡會實現實際的導入邏輯
                else:
                    print(f"跳過文件 {filename}：驗證未通過")
                    
            except Exception as e:
                logger.error(f"處理驗證文件 {filename} 時出錯: {e}")
    
    logger.info("知識庫導入完成")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="TurnFix 資料準備工具集")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 清洗命令
    clean_parser = subparsers.add_parser("clean", help="清洗教練答覆和影片逐字稿")
    clean_parser.add_argument("--input", required=True, help="輸入目錄")
    clean_parser.add_argument("--output", required=True, help="輸出目錄")
    
    # 提取命令
    extract_parser = subparsers.add_parser("extract", help="從清洗後資料提取知識")
    extract_parser.add_argument("--input", required=True, help="輸入目錄")
    extract_parser.add_argument("--review-mode", action="store_true", help="進入人工審核模式")
    
    # 驗證命令
    validate_parser = subparsers.add_parser("validate", help="驗證提取知識的品質")
    validate_parser.add_argument("--input", required=True, help="輸入目錄")
    
    # 導入命令
    import_parser = subparsers.add_parser("import", help="導入知識到知識庫")
    import_parser.add_argument("--input", required=True, help="輸入目錄")
    import_parser.add_argument("--chroma-db-path", required=True, help="ChromaDB 路徑")
    
    args = parser.parse_args()
    
    if args.command == "clean":
        clean_command(args)
    elif args.command == "extract":
        extract_command(args)
    elif args.command == "validate":
        validate_command(args)
    elif args.command == "import":
        import_command(args)
    else:
        parser.print_help()
    
    logger.info("資料準備工具執行完成")

if __name__ == "__main__":
    main()