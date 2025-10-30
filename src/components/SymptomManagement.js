/**
 * 症狀管理組件 (UI-308.1)
 * 
 * 設計並實作症狀管理頁面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const SymptomManagement = () => {
  const navigate = useNavigate();
  const [symptoms, setSymptoms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingSymptom, setEditingSymptom] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    synonyms: '',
    level_scope: '',
    terrain_scope: '',
    style_scope: ''
  });

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockSymptoms = [
      {
        id: 1,
        name: "重心太後",
        category: "技術",
        synonyms: ["後坐", "重心後移"],
        level_scope: ["初級", "中級"],
        terrain_scope: ["綠線", "藍線"],
        style_scope: ["平花"]
      },
      {
        id: 2,
        name: "重心不穩",
        category: "技術",
        synonyms: ["晃", "不穩"],
        level_scope: ["初級", "中級"],
        terrain_scope: ["綠線"],
        style_scope: ["平花"]
      },
      {
        id: 3,
        name: "換刃困難",
        category: "技術",
        synonyms: ["刃", "換刃"],
        level_scope: ["初級", "中級"],
        terrain_scope: ["綠線", "藍線"],
        style_scope: ["平花"]
      }
    ];
    
    setSymptoms(mockSymptoms);
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
      if (!formData.name.trim()) {
        setError('症狀名稱不能為空');
        return;
      }
      
      // 處理陣列字段
      const symptomData = {
        ...formData,
        synonyms: formData.synonyms.split(',').map(s => s.trim()).filter(s => s),
        level_scope: formData.level_scope.split(',').map(l => l.trim()).filter(l => l),
        terrain_scope: formData.terrain_scope.split(',').map(t => t.trim()).filter(t => t),
        style_scope: formData.style_scope.split(',').map(s => s.trim()).filter(s => s)
      };
      
      if (editingSymptom) {
        // 更新症狀
        const response = await fetch(`/api/v1/admin/symptoms/${editingSymptom.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(symptomData)
        });
        
        if (response.ok) {
          const updatedSymptom = await response.json();
          setSymptoms(prev => prev.map(s => 
            s.id === editingSymptom.id ? updatedSymptom.symptom : s
          ));
          setEditingSymptom(null);
        } else {
          throw new Error('更新症狀失敗');
        }
      } else {
        // 創建症狀
        const response = await fetch('/api/v1/admin/symptoms', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(symptomData)
        });
        
        if (response.ok) {
          const newSymptom = await response.json();
          setSymptoms(prev => [...prev, newSymptom.symptom]);
        } else {
          throw new Error('創建症狀失敗');
        }
      }
      
      // 重置表單
      setFormData({
        name: '',
        category: '',
        synonyms: '',
        level_scope: '',
        terrain_scope: '',
        style_scope: ''
      });
      setShowForm(false);
      setError('');
    } catch (err) {
      setError(`操作失敗: ${err.message}`);
    }
  };

  const handleEdit = (symptom) => {
    setEditingSymptom(symptom);
    setFormData({
      name: symptom.name,
      category: symptom.category,
      synonyms: symptom.synonyms.join(', '),
      level_scope: symptom.level_scope.join(', '),
      terrain_scope: symptom.terrain_scope.join(', '),
      style_scope: symptom.style_scope.join(', ')
    });
    setShowForm(true);
  };

  const handleDelete = async (symptomId) => {
    if (!window.confirm('確定要刪除此症狀嗎？')) {
      return;
    }
    
    try {
      const response = await fetch(`/api/v1/admin/symptoms/${symptomId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setSymptoms(prev => prev.filter(s => s.id !== symptomId));
      } else {
        throw new Error('刪除症狀失敗');
      }
    } catch (err) {
      setError(`刪除失敗: ${err.message}`);
    }
  };

  const renderForm = () => (
    <div className="management-page">
      <div className="page-header">
        <h1>{editingSymptom ? '編輯症狀' : '新增症狀'}</h1>
        <p>創建或修改滑雪問題症狀</p>
      </div>
      
      <form onSubmit={handleSubmit} className="management-form">
        <div className="form-content">
          <div className="form-group">
            <label htmlFor="name">症狀名稱 *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="例如：重心太後"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="category">類別 *</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              required
            >
              <option value="">請選擇</option>
              <option value="技術">技術</option>
              <option value="裝備">裝備</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="synonyms">同義詞 (逗號分隔)</label>
            <input
              type="text"
              id="synonyms"
              name="synonyms"
              value={formData.synonyms}
              onChange={handleInputChange}
              placeholder="例如：後坐, 重心後移"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="level_scope">適用等級範圍 (逗號分隔)</label>
            <input
              type="text"
              id="level_scope"
              name="level_scope"
              value={formData.level_scope}
              onChange={handleInputChange}
              placeholder="例如：初級, 中級"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="terrain_scope">適用地形範圍 (逗號分隔)</label>
            <input
              type="text"
              id="terrain_scope"
              name="terrain_scope"
              value={formData.terrain_scope}
              onChange={handleInputChange}
              placeholder="例如：綠線, 藍線"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="style_scope">適用滑行風格 (逗號分隔)</label>
            <input
              type="text"
              id="style_scope"
              name="style_scope"
              value={formData.style_scope}
              onChange={handleInputChange}
              placeholder="例如：平花"
            />
          </div>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-actions">
          <button 
            type="button" 
            className="cancel-button"
            onClick={() => {
              setShowForm(false);
              setEditingSymptom(null);
              setFormData({
                name: '',
                category: '',
                synonyms: '',
                level_scope: '',
                terrain_scope: '',
                style_scope: ''
              });
              setError('');
            }}
          >
            取消
          </button>
          <button type="submit" className="submit-button">
            {editingSymptom ? '更新症狀' : '創建症狀'}
          </button>
        </div>
      </form>
    </div>
  );

  const renderSymptomList = () => (
    <div className="management-page">
      <div className="list-header">
        <h1>🩺 症狀管理</h1>
        <p>管理滑雪問題症狀庫</p>
        <button 
          className="add-button"
          onClick={() => {
            setEditingSymptom(null);
            setFormData({
              name: '',
              category: '',
              synonyms: '',
              level_scope: '',
              terrain_scope: '',
              style_scope: ''
            });
            setShowForm(true);
            setError('');
          }}
        >
          + 新增症狀
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>類別</th>
              <th>同義詞數量</th>
              <th>等級範圍</th>
              <th>地形範圍</th>
              <th>滑行風格</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {symptoms.map(symptom => (
              <tr key={symptom.id}>
                <td>{symptom.id}</td>
                <td>{symptom.name}</td>
                <td>{symptom.category}</td>
                <td>{symptom.synonyms.length}</td>
                <td>{symptom.level_scope.join(', ')}</td>
                <td>{symptom.terrain_scope.join(', ')}</td>
                <td>{symptom.style_scope.join(', ')}</td>
                <td>
                  <button 
                    className="action-button edit"
                    onClick={() => handleEdit(symptom)}
                  >
                    編輯
                  </button>
                  <button 
                    className="action-button delete"
                    onClick={() => handleDelete(symptom.id)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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

  return (
    <div className="symptom-management">
      {showForm ? renderForm() : renderSymptomList()}
    </div>
  );
};

export default SymptomManagement;