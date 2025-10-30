"""
逐字稿清洗 CLI 工具 (TOOL-101)

支援 .txt 和 .md 文本檔清洗（移除雜訊、正規化格式、檢測語言）
實現分段邏輯（按段落或句子分割，保留足夠上下文以供知識抽取）
生成清洗後的中間格式（JSON with metadata: source, timestamp, language）
支援批量處理（輸入整個資料夾，輸出對應的清洗結果）
"""
import os
import re
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any
import logging

def clean_noise(text: str) -> str:
    """
    移除雜訊 (TOOL-101.1)
    
    Args:
        text: 原始文本
        
    Returns:
        str: 清洗後的文本
    """
    # 移除時間戳記
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    text = re.sub(r'\d{2}:\d{2}:\d{2}', '', text)
    
    # 移除特殊符號和標記
    text = re.sub(r'[-=#*]{3,}', '', text)  # 移除分隔符
    text = re.sub(r'\[\w\s\W\[\]\(\)]{2,}', '', text)  # 移除奇怪的標記
    
    # 清理多餘空白
    text = re.sub(r'\n{3,}', '\n\n', text)  # 最多兩個換行符
    text = re.sub(r'[ \t]{2,}', ' ', text)  # 多個空格替換為一個空格
    text = text.strip()
    
    return text


def normalize_format(text: str) -> str:
    """
    正規化格式 (TOOL-101.1)
    
    Args:
        text: 原始文本
        
    Returns:
        str: 格式化後的文本
    """
    # 統一換行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 統一日時格式
    # 將各種日期格式統一為 YYYY-MM-DD
    date_patterns = [
        (r'\d{4}/\d{1,2}/\d{1,2}', lambda m: m.group().replace('/', '-')),
        (r'\d{1,2}/\d{1,2}/\d{4}', lambda m: '-'.join(reversed(m.group().split('/')))),
    ]
    
    for pattern, replacer in date_patterns:
        text = re.sub(pattern, replacer, text)
    
    # 標準化單位
    unit_patterns = [
        (r'(\d+)\s*kg', r'\1 公斤'),
        (r'(\d+)\s*m', r'\1 公尺'),
        (r'(\d+)\s*cm', r'\1 公分'),
    ]
    
    for pattern, replacement in unit_patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def detect_language(text: str) -> str:
    """
    檢測語言 (TOOL-101.1)
    
    Args:
        text: 輸入文本
        
    Returns:
        str: 檢測到的語言代碼
    """
    # 簡化的語言檢測邏輯
    # 計算中文字符和英文字符的比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    if chinese_chars > english_chars:
        return 'zh'
    elif english_chars > 0:
        return 'en'
    else:
        return 'unknown'


def segment_text(text: str, max_length: int = 500) -> List[str]:
    """
    分段邏輯 (TOOL-101.2)
    
    按段落或句子分割，保留足夠上下文以供知識抽取
    
    Args:
        text: 原始文本
        max_length: 最大段落長度
        
    Returns:
        List[str]: 分段後的文本列表
    """
    # 基於段落分段
    paragraphs = text.split('\n\n')
    
    segments = []
    for para in paragraphs:
        para = para.strip()
        if len(para) > max_length:
            # 如果段落過長，按句子分段
            sentences = re.split(r'[。！？.!?]', para)
            current_segment = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                if len(current_segment + sentence) <= max_length:
                    current_segment += sentence + "。"
                else:
                    if current_segment:
                        segments.append(current_segment.strip())
                    current_segment = sentence + "。"
            
            if current_segment:
                segments.append(current_segment.strip())
        else:
            if para:  # 只添加非空段落
                segments.append(para)
    
    # 移除過短的段落
    segments = [seg for seg in segments if len(seg) > 10]
    
    return segments


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
        
        # 開始處理步驟
        cleaned_content = clean_noise(content)
        normalized_content = normalize_format(cleaned_content)
        language = detect_language(normalized_content)
        segments = segment_text(normalized_content)
        
        # 生成元數據
        metadata = {
            'source_file': os.path.basename(input_path),
            'source_path': input_path,
            'language': language,
            'processing_timestamp': datetime.now().isoformat(),
            'total_segments': len(segments),
            'original_length': len(content),
            'cleaned_length': len(normalized_content)
        }
        
        # 生成輸出內容
        output_data = {
            'metadata': metadata,
            'segments': segments
        }
        
        # 寫入 JSON 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"成功處理文件: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"處理文件時出錯 {input_path}: {e}")
        return False


def process_directory(input_dir: str, output_dir: str) -> Dict[str, Any]:
    """
    批量處理目錄中的文件 (TOOL-101.4)
    
    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
        
    Returns:
        Dict[str, Any]: 處理結果
    """
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 獲取所有 .txt 和 .md 文件
    input_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.txt', '.md')):
                input_files.append(os.path.join(root, file))
    
    results = {
        'processed_files': 0,
        'successful': 0,
        'failed': 0,
        'failed_files': [],
        'processing_timestamp': datetime.now().isoformat()
    }
    
    for input_file in input_files:
        # 構建輸出文件路徑
        rel_path = os.path.relpath(input_file, input_dir)
        output_file = os.path.join(output_dir, rel_path + '.json')
        
        # 確保輸出文件的目錄存在
        output_file_dir = os.path.dirname(output_file)
        os.makedirs(output_file_dir, exist_ok=True)
        
        # 處理文件
        success = process_file(input_file, output_file)
        results['processed_files'] += 1
        
        if success:
            results['successful'] += 1
        else:
            results['failed'] += 1
            results['failed_files'].append(input_file)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='逐字稿清洗 CLI 工具 (TOOL-101)')
    parser.add_argument('--input', '-i', required=True, help='輸入文件或目錄路徑')
    parser.add_argument('--output', '-o', required=True, help='輸出文件或目錄路徑')
    parser.add_argument('--max-length', '-m', type=int, default=500, help='最大段落長度 (默認為500)')
    
    args = parser.parse_args()
    
    # 設置日誌
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 更新全局最大長度
    global MAX_SEGMENT_LENGTH
    MAX_SEGMENT_LENGTH = args.max_length
    
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
        logging.info(f"目錄處理完成: {results['successful']} 成功, {results['failed']} 失敗")
    else:
        logging.error(f"輸入路徑不存在: {args.input}")


if __name__ == "__main__":
    main()