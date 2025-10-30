/**
 * 驗證工具函數
 */

/**
 * 驗證用戶輸入的問題描述
 * @param {string} input - 用戶輸入的文本
 * @returns {boolean} 驗證結果
 */
export const validateInputText = (input) => {
  if (!input || typeof input !== 'string') {
    return false;
  }
  
  // 檢查最小長度
  if (input.trim().length < 2) {
    return false;
  }
  
  // 檢查最大長度
  if (input.length > 500) {
    return false;
  }
  
  return true;
};

/**
 * 驗證等級選項
 * @param {string} level - 選擇的等級
 * @returns {boolean} 驗證結果
 */
export const validateLevel = (level) => {
  const validLevels = ['', '初級', '中級', '高級'];
  return validLevels.includes(level);
};

/**
 * 驗證地形選項
 * @param {string} terrain - 選擇的地形
 * @returns {boolean} 驗證結果
 */
export const validateTerrain = (terrain) => {
  const validTerrains = ['', '綠線', '藍線', '黑線', '雙黑線', '野雪'];
  return validTerrains.includes(terrain);
};

/**
 * 驗證滑行風格選項
 * @param {string} style - 選擇的滑行風格
 * @returns {boolean} 驗證結果
 */
export const validateStyle = (style) => {
  const validStyles = ['', '平花', '回轉', '野雪', '競速'];
  return validStyles.includes(style);
};

/**
 * 驗證反饋評分
 * @param {string} rating - 評分 (not_applicable, partially_applicable, applicable)
 * @returns {boolean} 驗證結果
 */
export const validateRating = (rating) => {
  const validRatings = ['', 'not_applicable', 'partially_applicable', 'applicable'];
  return validRatings.includes(rating);
};

/**
 * 驗證星數評分
 * @param {number} rating - 星數評分 (1-5)
 * @returns {boolean} 驗證結果
 */
export const validateStarRating = (rating) => {
  return Number.isInteger(rating) && rating >= 1 && rating <= 5;
};