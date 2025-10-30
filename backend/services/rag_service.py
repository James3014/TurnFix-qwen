"""
RAG 服務 (RAG-251 到 RAG-255)

實現檢索增強生成(RAG)系統
"""
from typing import List, Dict, Optional, Tuple, Any
from sqlalchemy.orm import Session
import json
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from ..core.config import settings
from ..models.symptom import Symptom
from ..models.practice_card import PracticeCard
from ..database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository
)

logger = logging.getLogger(__name__)

class RAGService:
    """
    RAG 服務類 (RAG-251 到 RAG-255)
    
    實現檢索增強生成系統
    """
    
    def __init__(self):
        # 初始化嵌入模型
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # 初始化向量數據庫
        self.client = chromadb.Client(Settings(
            persist_directory=settings.VECTOR_DB_PATH,
            anonymized_telemetry=False
        ))
        
        # 創建集合用於存儲知識片段
        try:
            self.collection = self.client.get_collection("knowledge_fragments")
        except:
            # 如果集合不存在，創建一個新的
            self.collection = self.client.create_collection(
                "knowledge_fragments",
                metadata={"hnsw:space": "cosine"}
            )
    
    def add_knowledge_fragment(self, fragment_id: str, content: str, metadata: Dict[str, Any] = None):
        """
        添加知識片段到向量數據庫 (RAG-251.1)
        
        Args:
            fragment_id: 知識片段ID
            content: 知識片段內容
            metadata: 元數據
        """
        try:
            # 生成嵌入向量
            embedding = self.embedding_model.encode([content])[0].tolist()
            
            # 添加到集合中
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata or {}],
                ids=[fragment_id]
            )
            
            logger.info(f"成功添加知識片段: {fragment_id}")
        except Exception as e:
            logger.error(f"添加知識片段時出錯: {e}")
            raise
    
    def search_knowledge(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相關知識片段 (RAG-253)
        
        Args:
            query: 查詢文本
            n_results: 返回結果數量
            
        Returns:
            List[Dict[str, Any]]: 搜索結果
        """
        try:
            # 生成查詢的嵌入向量
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # 搜索相關片段
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # 格式化結果
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            logger.info(f"成功搜索知識片段: {len(formatted_results)} 結果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"搜索知識片段時出錯: {e}")
            # 降級策略：返回空列表
            return []
    
    def generate_practice_card_from_knowledge(
        self, 
        user_input: str, 
        symptom: Symptom, 
        relevant_knowledge: List[Dict[str, Any]]
    ) -> Optional[PracticeCard]:
        """
        根據檢索到的知識和用戶輸入生成練習卡 (RAG-255)
        
        Args:
            user_input: 使用者輸入
            symptom: 識別的症狀
            relevant_knowledge: 相關知識片段
            
        Returns:
            Optional[PracticeCard]: 生成的練習卡
        """
        try:
            if not relevant_knowledge:
                return None
            
            # 從知識片段中提取信息來創建練習卡
            first_knowledge = relevant_knowledge[0]
            content = first_knowledge['content']
            
            # 在簡化實現中，我們直接從知識內容創建一個示例練習卡
            # 實際實現中，這些內容會由LLM生成
            practice_card = PracticeCard(
                name=f"針對{symptom.name}的練習",
                goal=f"改善{symptom.name}問題",
                tips=["進行適當練習", "保持正確姿勢", "注意動作要點"],
                pitfalls="避免常見錯誤",
                dosage="建議次數/時長",
                level=["初級", "中級"],  # 預設等級
                terrain=["綠線", "藍線"],  # 預設地形
                self_check=["檢查練習效果"],
                card_type="技術"
            )
            
            logger.info(f"成功生成練習卡: {practice_card.name}")
            return practice_card
            
        except Exception as e:
            logger.error(f"生成練習卡時出錯: {e}")
            return None
    
    def process_user_input(self, user_input: str) -> List[Dict[str, Any]]:
        """
        處理用戶輸入，進行RAG檢索和生成 (RAG-254)
        
        Args:
            user_input: 使用者輸入
            
        Returns:
            List[Dict[str, Any]]: 處理結果
        """
        try:
            # 搜索相關知識
            knowledge_fragments = self.search_knowledge(user_input)
            
            # 在實際實現中，這里會將知識片段與用戶輸入結合，
            # 生成更精準的練習建議，這裡僅返回檢索到的知識
            logger.info(f"成功處理用戶輸入，檢索到 {len(knowledge_fragments)} 個知識片段")
            return knowledge_fragments
            
        except Exception as e:
            logger.error(f"處理用戶輸入時出錯: {e}")
            # 降級策略：返回空列表
            return []

# 創建全局RAG服務實例
rag_service = RAGService()

def preprocess_coach_responses(text: str) -> str:
    """
    教練答覆資料清洗 (RAG-251.1)
    
    移除格式化符號、正規化日期、標準化單位
    
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
        
        logger.info("成功清洗教練答覆資料")
        return cleaned_text
        
    except Exception as e:
        logger.error(f"清洗教練答覆資料時出錯: {e}")
        # 降級策略：返回原始文本
        return text

def preprocess_video_transcripts(text: str) -> str:
    """
    影片逐字稿清洗 (RAG-251.2)
    
    移除時間戳記、合併斷句、檢測語言
    
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
        
        logger.info(f"成功清洗影片逐字稿資料，檢測語言: {language}")
        return cleaned_text
        
    except Exception as e:
        logger.error(f"清洗影片逐字稿資料時出錯: {e}")
        # 降級策略：返回原始文本
        return text

def segment_text(text: str) -> List[str]:
    """
    文本分段邏輯 (RAG-251.3)
    
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
        
        logger.info(f"成功分段文本: {len(segments)} 段")
        return segments
        
    except Exception as e:
        logger.error(f"分段文本時出錯: {e}")
        # 降級策略：按句子分段
        import re
        sentences = re.split(r'[。！？]', text)
        segments = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return segments if segments else [text]

def create_vector_database_structure():
    """
    設計並實作向量資料庫 (RAG-252)
    
    建立知識片段存儲結構（text、metadata、source、timestamps）
    """
    try:
        # 配置 ChromaDB 持久化存儲 (RAG-252.1)
        client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # 創建知識片段存儲結構 (RAG-252.2)
        collection = client.get_or_create_collection(
            "knowledge_fragments",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info("成功建立向量資料庫結構")
        return collection
        
    except Exception as e:
        logger.error(f"建立向量資料庫結構時出錯: {e}")
        raise

def import_knowledge_fragments(fragments: List[Dict[str, Any]]):
    """
    知識導入腳本 (RAG-252.3)
    
    從清洗後的教練答覆和影片逐字稿導入知識片段
    
    Args:
        fragments: 知識片段列表，格式：
        [
          {
            "id": "fragment_001",
            "text": "知識片段內容",
            "metadata": {
              "source": "coach_response/video_transcript",
              "source_id": "原始來源ID",
              "timestamp": "2025-10-29T10:00:00Z",
              "language": "zh"
            }
          }
        ]
    """
    try:
        # 創建向量資料庫結構
        collection = create_vector_database_structure()
        
        # 初始化嵌入模型
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # 批量處理知識片段
        fragment_ids = []
        texts = []
        metadatas = []
        
        for fragment in fragments:
            fragment_ids.append(fragment["id"])
            texts.append(fragment["text"])
            metadatas.append(fragment["metadata"])
        
        # 生成嵌入向量
        embeddings = embedding_model.encode(texts).tolist()
        
        # 批量導入到向量資料庫
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=fragment_ids
        )
        
        logger.info(f"成功導入 {len(fragments)} 個知識片段")
        
    except Exception as e:
        logger.error(f"導入知識片段時出錯: {e}")
        raise

def similarity_search(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    相似度搜尋 (RAG-253.2)
    
    返回 Top-K 最相關的知識片段
    
    Args:
        query: 查詢文本
        k: 返回結果數量
        
    Returns:
        List[Dict[str, Any]]: 相關知識片段列表
    """
    try:
        # 創建向量資料庫結構
        collection = create_vector_database_structure()
        
        # 初始化嵌入模型
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # 生成查詢向量
        query_embedding = embedding_model.encode([query]).tolist()[0]
        
        # 執行相似度搜尋
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # 格式化結果
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "similarity": 1 - results['distances'][0][i]  # 轉換為相似度分數
            })
        
        logger.info(f"成功執行相似度搜尋: {len(formatted_results)} 結果")
        return formatted_results
        
    except Exception as e:
        logger.error(f"執行相似度搜尋時出錯: {e}")
        # 降級策略：返回空列表
        return []

def hybrid_search(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    混合搜尋機制 (RAG-253.3)
    
    向量相似度 + 關鍵詞匹配
    
    Args:
        query: 查詢文本
        k: 返回結果數量
        
    Returns:
        List[Dict[str, Any]]: 相關知識片段列表
    """
    try:
        # 執行向量相似度搜尋
        vector_results = similarity_search(query, k * 2)  # 獲取更多結果以進行混合排序
        
        # 執行關鍵詞匹配搜尋
        keyword_results = keyword_search(query, k * 2)
        
        # 合併結果並重新排序
        merged_results = merge_and_rank_results(vector_results, keyword_results, k)
        
        logger.info(f"成功執行混合搜尋: {len(merged_results)} 結果")
        return merged_results
        
    except Exception as e:
        logger.error(f"執行混合搜尋時出錯: {e}")
        # 降級策略：僅使用向量搜尋
        return similarity_search(query, k)

def keyword_search(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    關鍵詞匹配搜尋
    
    Args:
        query: 查詢文本
        k: 返回結果數量
        
    Returns:
        List[Dict[str, Any]]: 匹配的知識片段列表
    """
    # 簡化實現：模擬關鍵詞搜尋
    # 實際實現中會使用全文檢索引擎
    return []

def merge_and_rank_results(vector_results: List[Dict[str, Any]], 
                         keyword_results: List[Dict[str, Any]], 
                         k: int) -> List[Dict[str, Any]]:
    """
    合併並重新排序搜尋結果
    
    Args:
        vector_results: 向量搜尋結果
        keyword_results: 關鍵詞搜尋結果
        k: 返回結果數量
        
    Returns:
        List[Dict[str, Any]]: 合併並排序後的結果
    """
    # 簡化實現：模擬結果合併
    # 實際實現中會使用更複雜的排序演算法
    return vector_results[:k]

def generate_prompt_template(context: str, query: str) -> str:
    """
    提示詞模板設計 (RAG-254.1)
    
    包含症狀辨識、練習卡生成、追問邏輯三個場景
    
    Args:
        context: 上下文信息（檢索出的知識片段）
        query: 用戶查詢
        
    Returns:
        str: 生成的提示詞模板
    """
    template = f"""
基於以下知識片段和用戶查詢，請提供滑雪技巧建議：

知識片段：
{context}

用戶查詢：
{query}

請根據知識片段中的信息，為用戶提供針對性的滑雪練習建議。
    """
    
    return template

def assemble_context(rag_results: List[Dict[str, Any]], 
                    user_input: str, 
                    slot_info: Dict[str, Any]) -> str:
    """
    上下文組裝邏輯 (RAG-254.2)
    
    將 RAG 檢索結果、使用者輸入、Slot 資訊組合
    
    Args:
        rag_results: RAG檢索結果
        user_input: 使用者輸入
        slot_info: Slot資訊
        
    Returns:
        str: 組裝後的上下文
    """
    context_parts = []
    
    # 添加使用者輸入
    context_parts.append(f"使用者輸入: {user_input}")
    
    # 添加Slot資訊
    if slot_info:
        slot_parts = []
        for key, value in slot_info.items():
            if value:
                slot_parts.append(f"{key}: {value}")
        if slot_parts:
            context_parts.append(f"Slot資訊: {', '.join(slot_parts)}")
    
    # 添加RAG檢索結果
    if rag_results:
        knowledge_parts = []
        for i, result in enumerate(rag_results):
            knowledge_parts.append(f"知識片段 {i+1}: {result['text']}")
        if knowledge_parts:
            context_parts.append(f"相關知識:\n{'\n'.join(knowledge_parts)}")
    
    return '\n\n'.join(context_parts)

def optimize_prompt_length(prompt: str, max_length: int = 2048) -> str:
    """
    提示詞優化機制 (RAG-254.3)
    
    長度控制、關鍵資訊優先級
    
    Args:
        prompt: 原始提示詞
        max_length: 最大長度限制
        
    Returns:
        str: 優化後的提示詞
    """
    if len(prompt) <= max_length:
        return prompt
    
    # 簡化實現：截斷提示詞
    # 實際實現中會使用更智能的摘要或關鍵資訊提取
    return prompt[:max_length] + "... (內容已截斷)"

def configure_llm_api():
    """
    選擇並配置 LLM API (RAG-255.1)
    
    如 OpenAI、Hugging Face、本地模型
    """
    # 簡化實現：返回配置信息
    # 實際實現中會初始化LLM客戶端
    return {
        "provider": settings.AI_PROVIDER,
        "model": settings.EMBEDDING_MODEL
    }

def generate_practice_card_content(prompt: str) -> Dict[str, Any]:
    """
    練習卡內容生成 (RAG-255.2)
    
    生成 goal、tips、pitfalls、dosage、self_check
    
    Args:
        prompt: 提示詞
        
    Returns:
        Dict[str, Any]: 生成的練習卡內容
    """
    # 簡化實現：模擬LLM生成結果
    # 實際實現中會調用LLM API
    return {
        "goal": "完成外腳承重再過中立",
        "tips": ["視線外緣", "外腳 70–80%", "中立後換刃"],
        "pitfalls": "避免提前壓內腳",
        "dosage": "藍線 6 次/趟 ×3 趟",
        "self_check": ["是否在換刃前感到外腳壓力峰值？"]
    }

def assist_symptom_identification(prompt: str) -> str:
    """
    症狀辨識輔助 (RAG-255.3)
    
    讓 LLM 根據使用者輸入和 RAG 檢索結果判斷症狀
    
    Args:
        prompt: 提示詞
        
    Returns:
        str: 識別的症狀名稱
    """
    # 簡化實現：模擬LLM生成結果
    # 實際實現中會調用LLM API
    return "重心太後"

def generate_followup_questions(prompt: str) -> List[Dict[str, str]]:
    """
    追問建議生成 (RAG-255.4)
    
    讓 LLM 根據置信度判斷是否需要追問及生成追問問題
    
    Args:
        prompt: 提示詞
        
    Returns:
        List[Dict[str, str]]: 追問問題列表
    """
    # 簡化實現：模擬LLM生成結果
    # 實際實現中會調用LLM API
    return [
        {"question": "請問您目前的滑雪等級是？(初級/中級/高級)", "type": "level"},
        {"question": "您通常在哪種地形滑行？(綠線/藍線/黑線)", "type": "terrain"}
    ]

# 兼容性接口 - 保持與舊版API的兼容性
def process_rag_request(user_input: str, **kwargs) -> Dict[str, Any]:
    """
    處理RAG請求的兼容性接口
    
    保持與舊版API的兼容性
    """
    level = kwargs.get('level')
    terrain = kwargs.get('terrain')
    style = kwargs.get('style')
    
    # 使用RAG服務處理請求
    rag_results = rag_service.process_user_input(user_input)
    
    return {
        "status": "success",
        "rag_results": rag_results,
        "count": len(rag_results)
    }