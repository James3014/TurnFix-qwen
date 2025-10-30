"""
知識庫導入工具 (TOOL-105)

將審核後的知識片段轉換為向量格式（使用 Sentence Transformers）
批量導入到 ChromaDB（包含 metadata: source, snippet_id, last_updated）
驗證導入成功（檢查向量化是否完成、是否可檢索）
生成導入報告（導入數量、耗時、任何錯誤）
"""
import os
import json
import time
import logging
from typing import Dict, List, Any
from datetime import datetime
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from ..core.config import settings

def convert_to_vector_format(snippets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    將審核後的知識片段轉換為向量格式 (TOOL-105.1)
    
    Args:
        snippets: 審核後的知識片段列表
        
    Returns:
        Dict[str, Any]: 轉換後的向量格式數據
    """
    try:
        # 初始化嵌入模型
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # 準備文本進行向量化
        texts = []
        metadatas = []
        ids = []
        
        for snippet in snippets:
            # 組合文本內容以進行向量化
            text_parts = [
                snippet.get('symptom', ''),
                ' '.join(snippet.get('practice_tips', [])),
                ' '.join(snippet.get('pitfalls', [])),
                snippet.get('dosage', ''),
                snippet.get('source_snippet', '')
            ]
            combined_text = ' '.join(text_parts).strip()
            
            if combined_text:  # 確保文本不為空
                texts.append(combined_text)
                
                # 創建元數據
                metadata = {
                    'symptom': snippet.get('symptom', ''),
                    'practice_tips': json.dumps(snippet.get('practice_tips', []), ensure_ascii=False),
                    'pitfalls': json.dumps(snippet.get('pitfalls', []), ensure_ascii=False),
                    'dosage': snippet.get('dosage', ''),
                    'source_snippet': snippet.get('source_snippet', ''),
                    'source_file': snippet.get('source_file', ''),
                    'snippet_id': snippet.get('id', ''),
                    'review_status': snippet.get('review_status', ''),
                    'confidence': snippet.get('confidence', 0.0),
                    'last_updated': datetime.now().isoformat()
                }
                metadatas.append(metadata)
                
                # 生成唯一ID
                snippet_id = snippet.get('id', f"snippet_{len(ids)+1}")
                ids.append(str(snippet_id))
        
        # 生成嵌入向量
        embeddings = embedding_model.encode(texts).tolist()
        
        return {
            'embeddings': embeddings,
            'documents': texts,
            'metadatas': metadatas,
            'ids': ids
        }
        
    except Exception as e:
        logging.error(f"轉換為向量格式時出錯: {e}")
        raise


def import_to_chromadb(vector_data: Dict[str, Any]) -> bool:
    """
    批量導入到 ChromaDB (TOOL-105.2)
    
    Args:
        vector_data: 向量格式數據
        
    Returns:
        bool: 是否導入成功
    """
    try:
        # 初始化向量數據庫
        client = chromadb.Client(Settings(
            persist_directory=settings.VECTOR_DB_PATH,
            anonymized_telemetry=False
        ))
        
        # 獲取或創建集合
        try:
            collection = client.get_collection("knowledge_fragments")
        except:
            # 如果集合不存在，創建一個新的
            collection = client.create_collection(
                "knowledge_fragments",
                metadata={"hnsw:space": "cosine"}
            )
        
        # 批量添加到集合
        collection.add(
            embeddings=vector_data['embeddings'],
            documents=vector_data['documents'],
            metadatas=vector_data['metadatas'],
            ids=vector_data['ids']
        )
        
        logging.info(f"成功導入 {len(vector_data['ids'])} 個知識片段到 ChromaDB")
        return True
        
    except Exception as e:
        logging.error(f"導入到 ChromaDB 時出錯: {e}")
        return False


def validate_import_success(ids: List[str]) -> Dict[str, Any]:
    """
    驗證導入成功 (TOOL-105.3)
    
    Args:
        ids: 導入的ID列表
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 初始化向量數據庫
        client = chromadb.Client(Settings(
            persist_directory=settings.VECTOR_DB_PATH,
            anonymized_telemetry=False
        ))
        
        # 獲取集合
        collection = client.get_collection("knowledge_fragments")
        
        # 檢查指定ID的文檔是否都存在
        results = collection.get(ids=ids, include=['metadatas'])
        
        imported_count = len(results['ids'])
        expected_count = len(ids)
        
        success = imported_count == expected_count
        
        validation_result = {
            'success': success,
            'expected_count': expected_count,
            'imported_count': imported_count,
            'missing_ids': list(set(ids) - set(results['ids'])),
            'validation_timestamp': datetime.now().isoformat()
        }
        
        if success:
            logging.info(f"導入驗證成功: {imported_count}/{expected_count} 片段已確認存在")
        else:
            logging.warning(f"導入驗證部分成功: {imported_count}/{expected_count} 片段存在")
        
        return validation_result
        
    except Exception as e:
        logging.error(f"驗證導入時出錯: {e}")
        return {
            'success': False,
            'error': str(e),
            'validation_timestamp': datetime.now().isoformat()
        }


def generate_import_report(import_results: Dict[str, Any], validation_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成導入報告 (TOOL-105.4)
    
    Args:
        import_results: 導入結果
        validation_results: 驗證結果
        
    Returns:
        Dict[str, Any]: 導入報告
    """
    report = {
        'report_timestamp': datetime.now().isoformat(),
        'import_results': import_results,
        'validation_results': validation_results,
        'status': 'success' if (import_results.get('success', False) and 
                                validation_results.get('success', False)) else 'failed'
    }
    
    return report


def import_approved_knowledge_snippets(file_path: str, report_path: str = None) -> Dict[str, Any]:
    """
    導入已批准的知識片段主函數
    
    Args:
        file_path: 包含審核後知識片段的JSON文件路徑
        report_path: 可選的報告文件路徑
        
    Returns:
        Dict[str, Any]: 匯入過程結果
    """
    start_time = time.time()
    
    try:
        # 讀取審核後的知識片段
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 過濾出已批准的片段
        approved_snippets = [
            snippet for snippet in data.get('knowledge_snippets', [])
            if snippet.get('review_status') == 'approved'
        ]
        
        if not approved_snippets:
            logging.info("沒有找到已批准的知識片段")
            return {
                'success': True,
                'imported_count': 0,
                'message': '沒有找到已批准的知識片段',
                'duration': time.time() - start_time
            }
        
        # 轉換為向量格式
        vector_data = convert_to_vector_format(approved_snippets)
        
        # 導入到ChromaDB
        import_success = import_to_chromadb(vector_data)
        
        import_result = {
            'success': import_success,
            'imported_count': len(vector_data['ids'])
        }
        
        # 驗證導入結果
        if import_success:
            validation_result = validate_import_success(vector_data['ids'])
        else:
            validation_result = {
                'success': False,
                'error': '導入失敗，未進行驗證'
            }
        
        # 生成報告
        report = generate_import_report(import_result, validation_result)
        
        # 保存報告
        if report_path:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        
        total_duration = time.time() - start_time
        
        final_result = {
            'success': import_result['success'] and validation_result['success'],
            'imported_count': import_result['imported_count'],
            'duration': total_duration,
            'report_path': report_path
        }
        
        logging.info(f"知識片段導入完成: {final_result['imported_count']} 個片段, 耗時 {total_duration:.2f} 秒")
        
        return final_result
        
    except Exception as e:
        logging.error(f"導入知識片段時出錯: {e}")
        return {
            'success': False,
            'error': str(e),
            'duration': time.time() - start_time
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='知識庫導入工具 (TOOL-105)')
    parser.add_argument('--input', '-i', required=True, help='包含審核後知識片段的JSON文件路徑')
    parser.add_argument('--report', '-r', help='導出報告文件路徑')
    
    args = parser.parse_args()
    
    # 設置日誌
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    result = import_approved_knowledge_snippets(args.input, args.report)
    
    if result['success']:
        print(f"導入成功: {result['imported_count']} 個知識片段已導入，耗時 {result['duration']:.2f} 秒")
    else:
        print(f"導入失敗: {result.get('error', '未知錯誤')}")


if __name__ == "__main__":
    main()