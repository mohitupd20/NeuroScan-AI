/**
 * API Service for Backend Communication
 * Handles all requests to the NeuroPath AI backend server
 */

const API_BASE_URL = "http://localhost:8000";

export const apiClient = {
  /**
   * Upload image and get classification result
   */
  async classify(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/classify`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Classification failed: ${response.statusText}`);
    }

    return await response.json();
  },

  /**
   * Upload image and get segmentation result
   */
  async segment(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/segment`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Segmentation failed: ${response.statusText}`);
    }

    return await response.json();
  },

  /**
   * Upload image and get detection result
   */
  async detect(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/detect`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Detection failed: ${response.statusText}`);
    }

    return await response.json();
  },

  /**
   * Upload image and get complete analysis (all three models)
   */
  async analyze(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return await response.json();
  },

  /**
   * Check health status of backend
   */
  async checkHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error("Backend is not available");
    }

    return await response.json();
  },
};
