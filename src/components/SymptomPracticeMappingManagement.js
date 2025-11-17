/**
 * 症狀練習卡映射管理組件 (UI-308.3)
 * 重構：使用自定義 Hook 和子組件，保持簡潔
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMappingManagement } from '../hooks/useMappingManagement';
import MappingForm from './mapping/MappingForm';
import MappingList from './mapping/MappingList';
import '../styles/AdminDashboard.css';

const SymptomPracticeMappingManagement = () => {
  const navigate = useNavigate();
  const {
    mappings,
    symptoms,
    practiceCards,
    loading,
    error,
    setError,
    createMapping,
    updateMapping,
    deleteMapping
  } = useMappingManagement();

  const [showForm, setShowForm] = useState(false);
  const [editingMapping, setEditingMapping] = useState(null);
  const [formData, setFormData] = useState({ symptom_id: '', practice_id: '', order: 0 });

  const handleInputChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.symptom_id || !formData.practice_id) {
      setError('請選擇症狀和練習卡');
      return;
    }

    const data = {
      symptom_id: parseInt(formData.symptom_id),
      practice_id: parseInt(formData.practice_id),
      order: parseInt(formData.order) || 0
    };

    try {
      if (editingMapping) {
        await updateMapping(editingMapping, data);
      } else {
        await createMapping(data);
      }
      resetForm();
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
    if (!window.confirm('確定要刪除此映射關係嗎？')) return;

    try {
      await deleteMapping(symptomId, practiceId);
    } catch (err) {
      setError(`刪除失敗: ${err.message}`);
    }
  };

  const resetForm = () => {
    setFormData({ symptom_id: '', practice_id: '', order: 0 });
    setShowForm(false);
    setEditingMapping(null);
    setError('');
  };

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>症狀練習卡映射管理</h1>
        <div className="header-actions">
          <button className="btn btn-back" onClick={() => navigate('/admin')}>返回</button>
          {!showForm && (
            <button className="btn btn-primary" onClick={() => setShowForm(true)}>新增映射</button>
          )}
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {showForm && (
        <MappingForm
          formData={formData}
          symptoms={symptoms}
          practiceCards={practiceCards}
          editingMapping={editingMapping}
          onInputChange={handleInputChange}
          onSubmit={handleSubmit}
          onCancel={resetForm}
        />
      )}

      <MappingList
        mappings={mappings}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
};

export default SymptomPracticeMappingManagement;
