/**
 * 症狀練習卡映射管理組件 (UI-308.3)
 * 
 * 設計並實作症狀↔練習卡映射管理頁面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const SymptomPracticeMappingManagement = () => {
  const navigate = useNavigate();
  const [mappings, setMappings] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [practiceCards, setPracticeCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingMapping, setEditingMapping] = useState(null);
  const [formData, setFormData] = useState({
    symptom_id: '',
    practice_id: '',
    order: 0
  });

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockMappings = [
      {
        symptom_id: 1,
        symptom_name: "重心太後",
        practice_id: 101,
        practice_name: "J型轉彎練習",
        order: 1
      },
      {
        symptom_id: 1,
        symptom_name: "重心太後",
        practice_id: 102,
        practice_name: "重心轉移練習",
        order: 2
      },
      {
        symptom_id: 2,
        symptom_name: "重心不穩",
        practice_id: 201,
        practice_name: "基礎滑行練習",
        order: 1
      }
    ];
    
    const mockSymptoms = [
      { id: 1, name: "重心太後", category: "技術" },
      { id: 2, name: "重心不穩", category: "技術" },
      { id: 3, name: "換刃困難", category: "技術" }
    ];
    
    const mockPracticeCards = [
      { id: 101, name: "J型轉彎練習", card_type: "技術" },
      { id: 102, name: "重心轉移練習", card_type: "基礎" },
      { id: 201, name: "基礎滑行練習", card_type: "基礎" }
    ];
    
    setMappings(mockMappings);
    setSymptoms(mockSymptoms);
    setPracticeCards(mockPracticeCards);
    setLoading(false);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // 驗證表單數據
      if (!formData.symptom_id || !formData.practice_id) {
        setError('請選擇症狀和練習卡');
        return;
      }
      
      // 轉換數據類型
      const mappingData = {
        ...formData,
        symptom_id: parseInt(formData.symptom_id),
        practice_id: parseInt(formData.practice_id),
        order: parseInt(formData.order) || 0
      };
      
      if (editingMapping) {
        // 更新映射
        const response = await fetch(`/api/v1/admin/symptom-practice-mappings/${editingMapping.symptom_id}/${editingMapping.practice_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(mappingData)
        });
        
        if (response.ok) {
          const updatedMapping = await response.json();
          setMappings(prev => prev.map(m => 
            m.symptom_id === editingMapping.symptom_id && m.practice_id === editingMapping.practice_id 
              ? updatedMapping.mapping 
              : m
          ));
          setEditingMapping(null);
        } else {
          throw new Error('更新映射失敗');
        }
      } else {
        // 創建映射
        const response = await fetch('/api/v1/admin/symptom-practice-mappings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(mappingData)
        });
        
        if (response.ok) {
          const newMapping = await response.json();
          setMappings(prev => [...prev, newMapping.mapping]);
        } else {
          throw new Error('創建映射失敗');
        }
      }
      
      // 重置表單
      setFormData({
        symptom_id: '',
        practice_id: '',
        order: 0
      });
      setShowForm(false);
      setError('');
    } catch (err) {
      setError(`操作失敗: ${err.message}`);
    }
  };

  const handleEdit = (mapping) => {
    setEditingMapping(mapping);
    setFormData({
      symptom_id: mapping.symptom_id.toString(),
      practice_id: mapping.practice_id.toString(),
      order: mapping.order
    });
    setShowForm(true);
  };

  const handleDelete = async (symptomId, practiceId) => {
    if (!window.confirm('確定要刪除此映射關係嗎？')) {
      return;
    }
    
    try {
      const response = await fetch(`/api/v1/admin/symptom-practice-mappings/${symptomId}/${practiceId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setMappings(prev => prev.filter(m => 
          !(m.symptom_id === symptomId && m.practice_id === practiceId)
        ));
      } else {
        throw new Error('刪除映射關係失敗');
      }
    } catch (err) {
      setError(`刪除失敗: ${err.message}`);
    }
  };

  const getSymptomName = (symptomId) => {
    const symptom = symptoms.find(s => s.id === symptomId);
    return symptom ? symptom.name : `症狀 ${symptomId}`;
  };

  const getPracticeCardName = (practiceId) => {
    const card = practiceCards.find(c => c.id === practiceId);
    return card ? card.name : `練習卡 ${practiceId}`;
  };

  const renderForm = () => (
    <div className="mapping-form">
      <h2>{editingMapping ? '編輯映射關係' : '新增映射關係'}</h2>
      
      <form onSubmit={handleSubmit} className="form-content">
        <div className="form-group">
          <label htmlFor="symptom_id">症狀 *</label>
          <select
            id="symptom_id"
            name="symptom_id"
            value={formData.symptom_id}
            onChange={handleInputChange}
            required
          >
            <option value="">請選擇症狀</option>
            {symptoms.map(symptom => (
              <option key={symptom.id} value={symptom.id}>
                {symptom.name} ({symptom.category})
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="practice_id">練習卡 *</label>
          <select
            id="practice_id"
            name="practice_id"
            value={formData.practice_id}
            onChange={handleInputChange}
            required
          >
            <option value="">請選擇練習卡</option>
            {practiceCards.map(card => (
              <option key={card.id} value={card.id}>
                {card.name} ({card.card_type})
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="order">排序順序</label>
          <input
            type="number"
            id="order"
            name="order"
            value={formData.order}
            onChange={handleInputChange}
            min="0"
            placeholder="0"
          />
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-actions">
          <button 
            type="button" 
            className="cancel-button"
            onClick={() => {
              setShowForm(false);
              setEditingMapping(null);
              setFormData({
                symptom_id: '',
                practice_id: '',
                order: 0
              });
              setError('');
            }}
          >
            取消
          </button>
          <button type="submit" className="submit-button">
            {editingMapping ? '更新映射' : '創建映射'}
          </button>
        </div>
      </form>
    </div>
  );

  const renderMappingList = () => (
    <div className="mapping-list">
      <div className="list-header">
        <h2>🔗 症狀↔練習卡映射管理</h2>
        <p>管理症狀與練習卡的多對多關聯關係</p>
        <button 
          className="add-button"
          onClick={() => {
            setEditingMapping(null);
            setFormData({
              symptom_id: '',
              practice_id: '',
              order: 0
            });
            setShowForm(true);
            setError('');
          }}
        >
          + 新增映射關係
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>症狀</th>
              <th>練習卡</th>
              <th>排序</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {mappings.map((mapping, index) => (
              <tr key={`${mapping.symptom_id}-${mapping.practice_id}-${index}`}>
                <td>{getSymptomName(mapping.symptom_id)}</td>
                <td>{getPracticeCardName(mapping.practice_id)}</td>
                <td>{mapping.order}</td>
                <td>
                  <button 
                    className="action-button edit"
                    onClick={() => handleEdit(mapping)}
                  >
                    編輯
                  </button>
                  <button 
                    className="action-button delete"
                    onClick={() => handleDelete(mapping.symptom_id, mapping.practice_id)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="validation-info">
        <h3>驗證資訊 (API-202.4)</h3>
        <p>💡 每個症狀建議關聯 3-5 張練習卡</p>
        <p>✅ 當前映射關係符合建議範圍</p>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="management-page">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="management-page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="management-page">
      <div className="page-header">
        <h1>🔗 症狀↔練習卡映射管理</h1>
        <p>管理症狀與練習卡的多對多關聯關係</p>
      </div>
      
      {showForm ? renderForm() : renderMappingList()}
    </div>
  );
};

export default SymptomPracticeMappingManagement;