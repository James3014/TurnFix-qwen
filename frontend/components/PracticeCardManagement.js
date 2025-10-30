/**
 * 練習卡管理組件 (UI-308.2)
 * 
 * 設計並實作練習卡管理頁面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const PracticeCardManagement = () => {
  const navigate = useNavigate();
  const [practiceCards, setPracticeCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingCard, setEditingCard] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    goal: '',
    tips: '',
    pitfalls: '',
    dosage: '',
    level: '',
    terrain: '',
    self_check: '',
    card_type: ''
  });

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockPracticeCards = [
      {
        id: 101,
        name: "J型轉彎練習",
        goal: "完成外腳承重再過中立",
        tips: ["視線外緣", "外腳 70–80%", "中立後換刃"],
        pitfalls: "避免提前壓內腳",
        dosage: "藍線 6 次/趟 ×3 趟",
        level: ["初級", "中級"],
        terrain: ["綠線", "藍線"],
        self_check: ["是否在換刃前感到外腳壓力峰值？"],
        card_type: "技術"
      },
      {
        id: 102,
        name: "重心轉移練習",
        goal: "改善重心控制",
        tips: ["身體前傾", "膝蓋彎曲", "重心保持在腳掌中心"],
        pitfalls: "避免重心過後或過前",
        dosage: "平地 10 次 ×3 組",
        level: ["初級", "中級"],
        terrain: ["綠線"],
        self_check: ["重心是否能穩定在腳掌中心？"],
        card_type: "基礎"
      },
      {
        id: 201,
        name: "基礎滑行練習",
        goal: "提升基本滑行穩定性",
        tips: ["膝蓋微彎", "重心稍前", "保持平衡"],
        pitfalls: "避免僵直站立",
        dosage: "平地 5 分鐘",
        level: ["初級"],
        terrain: ["綠線"],
        self_check: ["滑行時是否感到穩定？"],
        card_type: "基礎"
      }
    ];
    
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
      if (!formData.name.trim() || !formData.goal.trim()) {
        setError('練習卡名稱和目標不能為空');
        return;
      }
      
      // 處理陣列字段
      const cardData = {
        ...formData,
        tips: formData.tips.split(',').map(t => t.trim()).filter(t => t),
        level: formData.level.split(',').map(l => l.trim()).filter(l => l),
        terrain: formData.terrain.split(',').map(t => t.trim()).filter(t => t),
        self_check: formData.self_check.split(',').map(s => s.trim()).filter(s => s)
      };
      
      if (editingCard) {
        // 更新練習卡
        const response = await fetch(`/api/v1/admin/practice-cards/${editingCard.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(cardData)
        });
        
        if (response.ok) {
          const updatedCard = await response.json();
          setPracticeCards(prev => prev.map(c => 
            c.id === editingCard.id ? updatedCard.practice_card : c
          ));
          setEditingCard(null);
        } else {
          throw new Error('更新練習卡失敗');
        }
      } else {
        // 創建練習卡
        const response = await fetch('/api/v1/admin/practice-cards', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(cardData)
        });
        
        if (response.ok) {
          const newCard = await response.json();
          setPracticeCards(prev => [...prev, newCard.practice_card]);
        } else {
          throw new Error('創建練習卡失敗');
        }
      }
      
      // 重置表單
      setFormData({
        name: '',
        goal: '',
        tips: '',
        pitfalls: '',
        dosage: '',
        level: '',
        terrain: '',
        self_check: '',
        card_type: ''
      });
      setShowForm(false);
      setError('');
    } catch (err) {
      setError(`操作失敗: ${err.message}`);
    }
  };

  const handleEdit = (card) => {
    setEditingCard(card);
    setFormData({
      name: card.name,
      goal: card.goal,
      tips: card.tips.join(', '),
      pitfalls: card.pitfalls,
      dosage: card.dosage,
      level: card.level.join(', '),
      terrain: card.terrain.join(', '),
      self_check: card.self_check.join(', '),
      card_type: card.card_type
    });
    setShowForm(true);
  };

  const handleDelete = async (cardId) => {
    if (!window.confirm('確定要刪除此練習卡嗎？')) {
      return;
    }
    
    try {
      const response = await fetch(`/api/v1/admin/practice-cards/${cardId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setPracticeCards(prev => prev.filter(c => c.id !== cardId));
      } else {
        throw new Error('刪除練習卡失敗');
      }
    } catch (err) {
      setError(`刪除失敗: ${err.message}`);
    }
  };

  const renderForm = () => (
    <div className="management-page">
      <div className="page-header">
        <h1>{editingCard ? '編輯練習卡' : '新增練習卡'}</h1>
        <p>創建或修改滑雪練習建議卡</p>
      </div>
      
      <form onSubmit={handleSubmit} className="management-form">
        <div className="form-content">
          <div className="form-group">
            <label htmlFor="name">練習卡名稱 *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="例如：J型轉彎練習"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="goal">練習目標 *</label>
            <textarea
              id="goal"
              name="goal"
              value={formData.goal}
              onChange={handleInputChange}
              placeholder="例如：完成外腳承重再過中立"
              rows={3}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="tips">練習要點 (逗號分隔)</label>
            <input
              type="text"
              id="tips"
              name="tips"
              value={formData.tips}
              onChange={handleInputChange}
              placeholder="例如：視線外緣, 外腳 70–80%, 中立後換刃"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="pitfalls">常見錯誤修正</label>
            <textarea
              id="pitfalls"
              name="pitfalls"
              value={formData.pitfalls}
              onChange={handleInputChange}
              placeholder="例如：避免提前壓內腳"
              rows={2}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="dosage">建議次數/時長</label>
            <input
              type="text"
              id="dosage"
              name="dosage"
              value={formData.dosage}
              onChange={handleInputChange}
              placeholder="例如：藍線 6 次/趟 ×3 趟"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="level">適用等級 (逗號分隔)</label>
            <input
              type="text"
              id="level"
              name="level"
              value={formData.level}
              onChange={handleInputChange}
              placeholder="例如：初級, 中級"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="terrain">適用地形 (逗號分隔)</label>
            <input
              type="text"
              id="terrain"
              name="terrain"
              value={formData.terrain}
              onChange={handleInputChange}
              placeholder="例如：綠線, 藍線"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="self_check">自我檢查點 (逗號分隔)</label>
            <input
              type="text"
              id="self_check"
              name="self_check"
              value={formData.self_check}
              onChange={handleInputChange}
              placeholder="例如：是否在換刃前感到外腳壓力峰值？"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="card_type">練習卡類型</label>
            <select
              id="card_type"
              name="card_type"
              value={formData.card_type}
              onChange={handleInputChange}
            >
              <option value="">請選擇</option>
              <option value="技術">技術</option>
              <option value="基礎">基礎</option>
              <option value="進階">進階</option>
            </select>
          </div>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-actions">
          <button 
            type="button" 
            className="cancel-button"
            onClick={() => {
              setShowForm(false);
              setEditingCard(null);
              setFormData({
                name: '',
                goal: '',
                tips: '',
                pitfalls: '',
                dosage: '',
                level: '',
                terrain: '',
                self_check: '',
                card_type: ''
              });
              setError('');
            }}
          >
            取消
          </button>
          <button type="submit" className="submit-button">
            {editingCard ? '更新練習卡' : '創建練習卡'}
          </button>
        </div>
      </form>
    </div>
  );

  const renderPracticeCardList = () => (
    <div className="management-page">
      <div className="list-header">
        <h1>📋 練習卡管理</h1>
        <p>管理滑雪練習建議卡庫</p>
        <button 
          className="add-button"
          onClick={() => {
            setEditingCard(null);
            setFormData({
              name: '',
              goal: '',
              tips: '',
              pitfalls: '',
              dosage: '',
              level: '',
              terrain: '',
              self_check: '',
              card_type: ''
            });
            setShowForm(true);
            setError('');
          }}
        >
          + 新增練習卡
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>目標</th>
              <th>類型</th>
              <th>適用等級</th>
              <th>適用地形</th>
              <th>要點數量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {practiceCards.map(card => (
              <tr key={card.id}>
                <td>{card.id}</td>
                <td>{card.name}</td>
                <td>{card.goal.substring(0, 30)}...</td>
                <td>{card.card_type}</td>
                <td>{card.level.join(', ')}</td>
                <td>{card.terrain.join(', ')}</td>
                <td>{card.tips.length}</td>
                <td>
                  <button 
                    className="action-button edit"
                    onClick={() => handleEdit(card)}
                  >
                    編輯
                  </button>
                  <button 
                    className="action-button delete"
                    onClick={() => handleDelete(card.id)}
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

  if (error) {
    return (
      <div className="management-page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="practice-card-management">
      {showForm ? renderForm() : renderPracticeCardList()}
    </div>
  );
};

export default PracticeCardManagement;