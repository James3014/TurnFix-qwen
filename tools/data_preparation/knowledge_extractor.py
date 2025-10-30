"""
知識自動抽取工具 (TOOL-102)

基於關鍵詞和規則的症狀抽取（識別「後坐」、「重心」等症狀詞彙及其上下文）
基於結構的練習建議抽取（識別「動作要點」、「常見錯誤」、「建議次數」等模式）
生成候選知識片段（JSON format with fields: symptom, practice_tips, pitfalls, dosage, source_snippet）
標記為「待審核」狀態（便於人工驗證）
"""
import os
import json
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any
import logging

def extract_symptoms_by_keywords(text: str) -> List[Dict[str, str]]:
    """
    基於關鍵詞和規則的症狀抽取 (TOOL-102.1)
    
    Args:
        text: 輸入文本
        
    Returns:
        List[Dict[str, str]]: 提取的症狀列表
    """
    symptoms = []
    
    # 定義症狀模式
    symptom_patterns = [
        r'(重心.*?太.*?後)',  # 如：重心太後
        r'(後坐|向後坐)',      # 如：後坐
        r'(無法.*?換刃)',     # 如：無法換刃
        r'(重心.*?太.*?前)',  # 如：重心太前
        r'(換刃.*?困難)',     # 如：換刃困難
        r'(轉彎.*?不.*?穩)',  # 如：轉彎不穩
        r'(速度.*?控制.*?不.*?好)', # 如：速度控制不好
        r'(平衡.*?不.*?好)',   # 如：平衡不好
        r'(姿勢.*?不.*?正確)',  # 如：姿勢不正確
        r'(壓力.*?分配.*?不.*?均)', # 如：壓力分配不均
        r'(內刃.*?不足)',     # 如：內刃不足
        r'(外刃.*?過度)',     # 如：外刃過度
    ]
    
    # 搜索症狀
    for pattern in symptom_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in [s.get('name') for s in symptoms]:
                symptoms.append({
                    'name': match.strip(),
                    'category': '技術',
                    'context': extract_context(text, match)
                })
    
    # 特定的症狀關鍵詞
    specific_keywords = [
        '後坐', '重心', '換刃', '轉彎', '平衡', '姿勢', '速度控制', 
        '壓力分配', '內刃', '外刃', '滑行路徑', '腿部彎曲', '軀幹旋轉'
    ]
    
    for keyword in specific_keywords:
        if keyword in text and not any(keyword in s['name'] for s in symptoms):
            symptoms.append({
                'name': keyword,
                'category': '技術',
                'context': extract_context(text, keyword)
            })
    
    return symptoms


def extract_practice_tips_by_structure(text: str) -> List[Dict[str, str]]:
    """
    基於結構的練習建議抽取 (TOOL-102.2)
    
    Args:
        text: 輸入文本
        
    Returns:
        List[Dict[str, str]]: 提取的練習建議列表
    """
    tips = []
    
    # 定義建議模式
    tip_patterns = [
        r'(要點：?|動作要點：?)([^。]*?)[。.。]',  # 如：要點：保持重心向前
        r'(建議.*?：?)([^。]*?)[。.。]',
        r'(應該.*?：?)([^。]*?)[。.。]',
        r'(注意.*?：?)([^。]*?)[。.。]',
    ]
    
    for pattern in tip_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            tips.append({
                'type': 'tip',
                'content': match[1].strip(),
                'context': extract_context(text, match[1])
            })
    
    # 搜索常見錯誤和建議次數
    error_patterns = [
        r'(避免|不要.*?：?)([^。]*?)[。.。]',
        r'(常見錯誤：?)([^。]*?)[。.。]',
        r'(錯誤.*?：?)([^。]*?)[。.。]',
    ]
    
    for pattern in error_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            tips.append({
                'type': 'pitfall',
                'content': match[1].strip(),
                'context': extract_context(text, match[1])
            })
    
    dosage_patterns = [
        r'(\d+)\s*(次|趟|圈|分鐘|組)',
        r'每\s*(\d+)\s*.*?\s*(\d+)\s*[次趟圈分鐘組]',
        r'建議.*?(\d+)\s*次',
        r'做.*?(\d+)\s*[次趟圈分鐘組]',
    ]
    
    for pattern in dosage_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            dosage = ''.join(match) if isinstance(match, tuple) else match
            tips.append({
                'type': 'dosage',
                'content': dosage.strip(),
                'context': extract_context(text, dosage)
            })
    
    return tips


def extract_context(text: str, target: str, context_length: int = 100) -> str:
    """
    提取目標詞彙的上下文
    
    Args:
        text: 原始文本
        target: 目標詞彙
        context_length: 上下文長度
        
    Returns:
        str: 上下文文本
    """
    pos = text.find(target)
    if pos == -1:
        return ""
    
    start = max(0, pos - context_length // 2)
    end = min(len(text), pos + len(target) + context_length // 2)
    
    context = text[start:end].strip()
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    
    return context


def generate_candidate_knowledge_snippets(symptoms: List[Dict[str, str]], 
                                        practice_tips: List[Dict[str, str]], 
                                        source_text: str) -> List[Dict[str, Any]]:
    """
    生成候選知識片段 (TOOL-102.3)
    
    Args:
        symptoms: 症狀列表
        practice_tips: 練習建議列表
        source_text: 原始文本
        
    Returns:
        List[Dict[str, Any]]: 候選知識片段列表
    """
    snippets = []
    
    # 為每個症狀創建知識片段
    for symptom in symptoms:
        snippet = {
            'symptom': symptom['name'],
            'practice_tips': [],
            'pitfalls': [],
            'dosage': [],
            'source_snippet': symptom['context'],
            'confidence': 0.8,  # 默認置信度
            'review_status': 'pending',  # 標記為待審核 (TOOL-102.4)
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        # 添加相關的練習建議
        for tip in practice_tips:
            if tip['type'] == 'tip':
                snippet['practice_tips'].append(tip['content'])
            elif tip['type'] == 'pitfall':
                snippet['pitfalls'].append(tip['content'])
            elif tip['type'] == 'dosage':
                snippet['dosage'].append(tip['content'])
        
        snippets.append(snippet)
    
    # 如果沒有症狀，但有練習建議，創建通用片段
    if not symptoms and practice_tips:
        snippet = {
            'symptom': '一般技術問題',
            'practice_tips': [],
            'pitfalls': [],
            'dosage': [],
            'source_snippet': source_text[:200] + "..." if len(source_text) > 200 else source_text,
            'confidence': 0.6,  # 較低的置信度
            'review_status': 'pending',  # 標記為待審核 (TOOL-102.4)
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        for tip in practice_tips:
            if tip['type'] == 'tip':
                snippet['practice_tips'].append(tip['content'])
            elif tip['type'] == 'pitfall':
                snippet['pitfalls'].append(tip['content'])
            elif tip['type'] == 'dosage':
                snippet['dosage'].append(tip['content'])
        
        snippets.append(snippet)
    
    return snippets


def process_file(input_path: str, output_path: str) -> bool:
    """
    處理單個文件
    
    Args:
        input_path: 輸入文件路徑
        output_path: 輸出文件路徑
        
    Returns:
        bool: 是否成功處理
    """
    try:
        # 讀取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取症狀和練習建議
        symptoms = extract_symptoms_by_keywords(content)
        practice_tips = extract_practice_tips_by_structure(content)
        
        # 生成候選知識片段
        snippets = generate_candidate_knowledge_snippets(symptoms, practice_tips, content)
        
        # 生成元數據
        metadata = {
            'source_file': os.path.basename(input_path),
            'source_path': input_path,
            'processing_timestamp': datetime.now().isoformat(),
            'total_snippets': len(snippets),
            'total_symptoms': len(symptoms),
            'total_tips': len(practice_tips)
        }
        
        # 生成輸出內容
        output_data = {
            'metadata': metadata,
            'knowledge_snippets': snippets
        }
        
        # 寫入 JSON 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"成功處理文件: {input_path} -> {output_path}, 生成 {len(snippets)} 個知識片段")
        return True
        
    except Exception as e:
        logging.error(f"處理文件時出錯 {input_path}: {e}")
        return False


def process_directory(input_dir: str, output_dir: str) -> Dict[str, Any]:
    """
    批量處理目錄中的文件
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
        
    Returns:
        Dict[str, Any]: 處理結果
    """
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 獲取所有 .json 文件 (這些是由清洗工具產生的)
    input_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.json'):
                input_files.append(os.path.join(root, file))
    
    results = {
        'processed_files': 0,
        'successful': 0,
        'failed': 0,
        'failed_files': [],
        'total_snippets': 0,
        'processing_timestamp': datetime.now().isoformat()
    }
    
    for input_file in input_files:
        # 構建輸出文件路徑
        rel_path = os.path.relpath(input_file, input_dir)
        output_file = os.path.join(output_dir, rel_path)
        
        # 確保輸出文件的目錄存在
        output_file_dir = os.path.dirname(output_file)
        os.makedirs(output_file_dir, exist_ok=True)
        
        # 處理文件
        success = process_file(input_file, output_file)
        results['processed_files'] += 1
        
        if success:
            # 統計知識片段數量
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results['total_snippets'] += len(data.get('knowledge_snippets', []))
            results['successful'] += 1
        else:
            results['failed'] += 1
            results['failed_files'].append(input_file)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='知識自動抽取工具 (TOOL-102)')
    parser.add_argument('--input', '-i', required=True, help='輸入文件或目錄路徑')
    parser.add_argument('--output', '-o', required=True, help='輸出文件或目錄路徑')
    
    args = parser.parse_args()
    
    # 設置日誌
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if os.path.isfile(args.input):
        # 處理單個文件
        success = process_file(args.input, args.output)
        if success:
            logging.info("文件處理完成")
        else:
            logging.error("文件處理失敗")
    elif os.path.isdir(args.input):
        # 批量處理目錄
        results = process_directory(args.input, args.output)
        logging.info(f"目錄處理完成: {results['successful']} 成功, {results['failed']} 失敗, {results['total_snippets']} 知識片段")
    else:
        logging.error(f"輸入路徑不存在: {args.input}")


if __name__ == "__main__":
    main()