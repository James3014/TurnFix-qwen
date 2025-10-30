"""
資料驗證與品質檢查工具 (TOOL-103)

檢查症狀名稱唯一性和格式一致性
驗證練習建議的完整性（是否包含 goal、tips、pitfalls、dosage、self_check）
生成驗證報告，標記異常記錄（缺少字段、過短描述等）
"""
import os
import json
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

def validate_symptom_name_format(name: str) -> Tuple[bool, str]:
    """
    檢查症狀名稱格式 (TOOL-103.1)
    
    Args:
        name: 症狀名稱
        
    Returns:
        Tuple[bool, str]: (是否有效, 錯誤信息)
    """
    if not name or len(name.strip()) == 0:
        return False, "症狀名稱不能為空"
    
    if len(name) > 100:
        return False, "症狀名稱過長"
    
    # 檢查是否包含不當字符
    if re.search(r'[<>:"/\\|?*]', name):
        return False, "症狀名稱包含不當字符"
    
    return True, ""


def validate_practice_card_completeness(card: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    驗證練習建議的完整性 (TOOL-103.2)
    
    Args:
        card: 練習卡數據
        
    Returns:
        Tuple[bool, List[str]]: (是否完整, 缺失字段列表)
    """
    required_fields = ['goal', 'tips']
    missing_fields = []
    
    for field in required_fields:
        value = card.get(field)
        if not value or (isinstance(value, list) and len(value) == 0) or (isinstance(value, str) and len(value.strip()) == 0):
            missing_fields.append(field)
    
    # 檢查tips是否為列表
    tips = card.get('tips', [])
    if not isinstance(tips, list):
        missing_fields.append('tips (格式應為列表)')
    
    # 檢查self_check是否為列表（如果提供）
    self_check = card.get('self_check', [])
    if self_check and not isinstance(self_check, list):
        missing_fields.append('self_check (格式應為列表)')
    
    # 檢查level、terrain是否為列表（如果提供）
    for field in ['level', 'terrain']:
        value = card.get(field, [])
        if value and not isinstance(value, list):
            missing_fields.append(f'{field} (格式應為列表)')
    
    return len(missing_fields) == 0, missing_fields


def check_data_quality(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    檢查數據品質
    
    Args:
        data: 要檢查的數據
        
    Returns:
        Dict[str, Any]: 品質檢查結果
    """
    issues = []
    
    # 檢查知識片段
    snippets = data.get('knowledge_snippets', [])
    for i, snippet in enumerate(snippets):
        # 檢查症狀名稱格式
        is_valid, error_msg = validate_symptom_name_format(snippet.get('symptom', ''))
        if not is_valid:
            issues.append({
                'type': 'symptom_format',
                'index': i,
                'field': 'symptom',
                'error': error_msg,
                'value': snippet.get('symptom', '')
            })
        
        # 檢查練習建議完整性
        practice_data = {
            'goal': snippet.get('symptom', ''),  # 使用症狀作為目標的替代
            'tips': snippet.get('practice_tips', []),
            'pitfalls': snippet.get('pitfalls', []),
            'dosage': snippet.get('dosage', []),
            'self_check': []  # 空列表以進行完整性檢查
        }
        is_complete, missing_fields = validate_practice_card_completeness(practice_data)
        if not is_complete:
            issues.append({
                'type': 'incomplete_practice',
                'index': i,
                'field': 'practice_data',
                'error': f'缺少字段: {", ".join(missing_fields)}',
                'value': snippet.get('symptom', '')
            })
        
        # 檢查描述長度
        source_snippet = snippet.get('source_snippet', '')
        if len(source_snippet) < 10:
            issues.append({
                'type': 'short_description',
                'index': i,
                'field': 'source_snippet',
                'error': '描述過短',
                'value': source_snippet[:50] + "..."
            })
    
    return {
        'total_snippets': len(snippets),
        'issues_found': len(issues),
        'issues': issues
    }


def generate_validation_report(input_dir: str, output_file: str) -> Dict[str, Any]:
    """
    生成驗證報告 (TOOL-103.3)
    
    Args:
        input_dir: 輸入目錄
        output_file: 輸出文件路徑
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    # 獲取所有 .json 文件
    input_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.json'):
                input_files.append(os.path.join(root, file))
    
    report = {
        'validation_timestamp': datetime.now().isoformat(),
        'total_files': len(input_files),
        'files_checked': [],
        'summary': {
            'total_snippets': 0,
            'total_issues': 0,
            'issue_types': {}
        }
    }
    
    all_issues = []
    
    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            quality_check = check_data_quality(data)
            
            file_result = {
                'file_path': file_path,
                'snippets_count': quality_check['total_snippets'],
                'issues_count': quality_check['issues_found'],
                'issues': quality_check['issues']
            }
            
            report['files_checked'].append(file_result)
            report['summary']['total_snippets'] += quality_check['total_snippets']
            report['summary']['total_issues'] += quality_check['issues_found']
            
            # 統計問題類型
            for issue in quality_check['issues']:
                issue_type = issue['type']
                if issue_type not in report['summary']['issue_types']:
                    report['summary']['issue_types'][issue_type] = 0
                report['summary']['issue_types'][issue_type] += 1
            
            all_issues.extend(quality_check['issues'])
            
        except Exception as e:
            logging.error(f"檢查文件時出錯 {file_path}: {e}")
    
    # 添加詳細問題列表到報告
    report['all_issues'] = all_issues
    
    # 寫入報告文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logging.info(f"驗證報告已生成: {output_file}")
    return report


def main():
    parser = argparse.ArgumentParser(description='資料驗證與品質檢查工具 (TOOL-103)')
    parser.add_argument('--input', '-i', required=True, help='輸入目錄路徑')
    parser.add_argument('--output', '-o', required=True, help='輸出報告文件路徑')
    
    args = parser.parse_args()
    
    # 設置日誌
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if not os.path.isdir(args.input):
        logging.error(f"輸入目錄不存在: {args.input}")
        return
    
    report = generate_validation_report(args.input, args.output)
    
    logging.info(f"驗證完成:")
    logging.info(f"  - 檢查文件數: {report['summary']['total_snippets']}")
    logging.info(f"  - 發現問題數: {report['summary']['total_issues']}")
    logging.info(f"  - 問題類型: {list(report['summary']['issue_types'].keys())}")


if __name__ == "__main__":
    main()