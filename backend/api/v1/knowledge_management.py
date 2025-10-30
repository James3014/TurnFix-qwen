"""
應用側的知識庫管理 API (TOOL-107)

與工具相互配合的API端點
實現知識上傳、審核管理等功能
"""
from fastapi import APIRouter, UploadFile, File, Query, Depends, HTTPException
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import json
import uuid
from ...database.base import get_db
from ...models.symptom import Symptom
from ...database.repositories import SymptomRepository
from ...services.data_extraction_service import extract_and_structure_knowledge

router = APIRouter()


@router.post("/knowledge/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上傳清洗後的 JSON 檔案 (TOOL-107.1)
    
    接收清洗後的 JSON 檔案（供工具上傳）
    
    Args:
        file: 上傳的JSON文件
        db: 數據庫連接
        
    Returns:
        Dict[str, Any]: 處理結果
    """
    try:
        # 讀取上傳的文件內容
        content = await file.read()
        json_content = json.loads(content.decode('utf-8'))
        
        # 提取知識片段
        for snippet in json_content.get('knowledge_snippets', []):
            # 標記為待審核狀態
            snippet['review_status'] = 'pending'
            snippet['needs_human_verification'] = True
        
        # 保存到數據庫或緩存中等待後續處理
        # 在實際實現中，這會保存到臨時存儲中
        processed_data = {
            'original_filename': file.filename,
            'total_snippets': len(json_content.get('knowledge_snippets', [])),
            'processed_at': __import__('datetime').datetime.now().isoformat(),
            'status': 'uploaded_pending_review'
        }
        
        return {
            "status": "success",
            "message": "知識檔案上傳成功，等待審核",
            "processed_data": processed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上傳知識檔案時出錯: {str(e)}")


@router.get("/knowledge/list-pending-review")
async def list_pending_review_knowledge(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100, description="返回記錄數量"),
    offset: int = Query(0, ge=0, description="偏移量")
):
    """
    列出待審核項目 (TOOL-107.2)
    
    返回需要人工審核的知識片段列表
    
    Args:
        db: 數據庫連接
        limit: 返回記錄數量
        offset: 偏移量
        
    Returns:
        Dict[str, Any]: 待審核項目列表
    """
    try:
        # 在實際實現中，這會從數據庫或臨時存儲中查詢
        # 現在模擬返回一些待審核項目
        pending_knowledge = [
            {
                'id': str(uuid.uuid4()),
                'symptom': '重心太後',
                'practice_tips': ['保持上身直立', '重心向前移'],
                'pitfalls': ['避免後坐', '不要過度彎曲膝蓋'],
                'dosage': '藍線6次/趟×3趟',
                'source_snippet': '當重心太後時，會導致後坐，建議保持上身直立，重心向前移...',
                'confidence': 0.85,
                'source_file': 'coach_response_001.json',
                'uploaded_at': '2025-10-29T10:30:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'symptom': '無法換刃',
                'practice_tips': ['增加壓力轉移', '提前準備換刃動作'],
                'pitfalls': ['避免突然換刃', '不要過度用力'],
                'dosage': '綠線5次/趟×2趟',
                'source_snippet': '很多學員無法順利換刃，這通常是由於壓力轉移不夠...',
                'confidence': 0.72,
                'source_file': 'video_transcript_002.json',
                'uploaded_at': '2025-10-29T11:15:00Z'
            }
        ]
        
        # 應用分頁
        start_index = offset
        end_index = min(offset + limit, len(pending_knowledge))
        paginated_knowledge = pending_knowledge[start_index:end_index]
        
        return {
            "status": "success",
            "count": len(pending_knowledge),
            "pending_knowledge": paginated_knowledge,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取待審核項目時出錯: {str(e)}")


@router.post("/knowledge/approve/{knowledge_id}")
async def approve_knowledge(
    knowledge_id: str,
    db: Session = Depends(get_db)
):
    """
    審核批准知識片段 (TOOL-107.3)
    
    將知識片段標記為已批准
    
    Args:
        knowledge_id: 知識片段ID
        db: 數據庫連接
        
    Returns:
        Dict[str, Any]: 審核結果
    """
    try:
        # 在實際實現中，這會更新數據庫中的狀態
        # 現在模擬批准操作
        return {
            "status": "success",
            "message": f"知識片段 {knowledge_id} 已批准",
            "knowledge_id": knowledge_id,
            "approved_at": __import__('datetime').datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批准知識片段時出錯: {str(e)}")


@router.post("/knowledge/reject/{knowledge_id}")
async def reject_knowledge(
    knowledge_id: str,
    db: Session = Depends(get_db)
):
    """
    審核拒絕知識片段 (TOOL-107.3)
    
    將知識片段標記為已拒絕
    
    Args:
        knowledge_id: 知識片段ID
        db: 數據庫連接
        
    Returns:
        Dict[str, Any]: 審核結果
    """
    try:
        # 在實際實現中，這會更新數據庫中的狀態
        # 現在模擬拒絕操作
        return {
            "status": "success",
            "message": f"知識片段 {knowledge_id} 已拒絕",
            "knowledge_id": knowledge_id,
            "rejected_at": __import__('datetime').datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"拒絕知識片段時出錯: {str(e)}")


@router.get("/knowledge/export")
async def export_approved_knowledge(
    db: Session = Depends(get_db),
    format: str = Query("json", regex="^(json|csv)$", description="導出格式")
):
    """
    導出已批准的知識片段 (TOOL-107.4)
    
    將已批准的知識片段導出為 JSON 格式（供工具導入 ChromaDB）
    
    Args:
        db: 數據庫連接
        format: 導出格式
        
    Returns:
        Dict[str, Any]: 匯出結果
    """
    try:
        # 在實際實現中，這會從數據庫中查詢已批准的知識片段
        # 現在模擬返回一些已批准的知識片段
        approved_knowledge = [
            {
                'id': str(uuid.uuid4()),
                'symptom': '重心太後',
                'practice_tips': ['保持上身直立', '重心向前移'],
                'pitfalls': ['避免後坐', '不要過度彎曲膝蓋'],
                'dosage': '藍線6次/趟×3趟',
                'source_snippet': '當重心太後時，會導致後坐，建議保持上身直立，重心向前移...',
                'review_status': 'approved',
                'confidence': 0.85,
                'source_file': 'coach_response_001.json',
                'approved_at': '2025-10-29T10:30:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'symptom': '無法換刃',
                'practice_tips': ['增加壓力轉移', '提前準備換刃動作'],
                'pitfalls': ['避免突然換刃', '不要過度用力'],
                'dosage': '綠線5次/趟×2趟',
                'source_snippet': '很多學員無法順利換刃，這通常是由於壓力轉移不夠...',
                'review_status': 'approved',
                'confidence': 0.72,
                'source_file': 'video_transcript_002.json',
                'approved_at': '2025-10-29T11:15:00Z'
            }
        ]
        
        if format == "json":
            return {
                "status": "success",
                "exported_knowledge": approved_knowledge,
                "format": "json",
                "exported_at": __import__('datetime').datetime.now().isoformat(),
                "count": len(approved_knowledge)
            }
        else:
            # CSV 格式處理（簡化實現）
            return {
                "status": "success",
                "message": "CSV格式導出功能待實現",
                "format": "csv",
                "exported_at": __import__('datetime').datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"導出知識片段時出錯: {str(e)}")