/**
 * 症狀管理組件 (UI-308.1)
 *
 * 重構後:使用自定義 Hook 和拆分的子組件
 * 遵循 Linus 原則:
 * - 單一職責:只負責協調子組件
 * - DRY:使用共享的 Hook 和組件
 * - 簡單:< 100 行
 */
import React, { useState } from 'react';
import { useSymptoms } from '../hooks/useSymptoms';
import SymptomForm from './admin/SymptomForm';
import SymptomList from './admin/SymptomList';
import '../styles/AdminDashboard.css';

const SymptomManagement = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingSymptom, setEditingSymptom] = useState(null);

  const {
    symptoms,
    loading,
    error,
    createSymptom,
    updateSymptom,
    deleteSymptom
  } = useSymptoms();

  const handleAdd = () => {
    setEditingSymptom(null);
    setShowForm(true);
  };

  const handleEdit = (symptom) => {
    setEditingSymptom(symptom);
    setShowForm(true);
  };

  const handleSubmit = async (symptomData) => {
    if (editingSymptom) {
      await updateSymptom(editingSymptom.id, symptomData);
    } else {
      await createSymptom(symptomData);
    }
    setShowForm(false);
    setEditingSymptom(null);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingSymptom(null);
  };

  const handleDelete = async (symptomId) => {
    await deleteSymptom(symptomId);
  };

  // Loading 狀態
  if (loading && symptoms.length === 0) {
    return (
      <div className="management-page">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  // Error 狀態
  if (error && symptoms.length === 0) {
    return (
      <div className="management-page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="symptom-management">
      {showForm ? (
        <SymptomForm
          symptom={editingSymptom}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          loading={loading}
        />
      ) : (
        <SymptomList
          symptoms={symptoms}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onAdd={handleAdd}
        />
      )}
    </div>
  );
};

export default SymptomManagement;
