import api from './axios'

export const catalogueApi = {
  // Instituts
  getInstituts: (params) => api.get('/api/catalogue/instituts/', { params }),
  getInstitut: (id) => api.get(`/api/catalogue/instituts/${id}/`),
  getInstitutFilieres: (id) => api.get(`/api/catalogue/instituts/${id}/filieres/`),
  createInstitut: (data) => api.post('/api/catalogue/instituts/', data),
  updateInstitut: (id, data) => api.patch(`/api/catalogue/instituts/${id}/`, data),
  deleteInstitut: (id) => api.delete(`/api/catalogue/instituts/${id}/`),

  // Filières
  getFilieres: (params) => api.get('/api/catalogue/filieres/', { params }),
  getFiliere: (id) => api.get(`/api/catalogue/filieres/${id}/`),
  getFiliereNiveaux: (id) => api.get(`/api/catalogue/filieres/${id}/niveaux/`),
  createFiliere: (data) => api.post('/api/catalogue/filieres/', data),
  updateFiliere: (id, data) => api.patch(`/api/catalogue/filieres/${id}/`, data),
  deleteFiliere: (id) => api.delete(`/api/catalogue/filieres/${id}/`),

  // Niveaux
  getNiveaux: (params) => api.get('/api/catalogue/niveaux/', { params }),
  getNiveau: (id) => api.get(`/api/catalogue/niveaux/${id}/`),
  getNiveauMatieres: (id) => api.get(`/api/catalogue/niveaux/${id}/matieres/`),
  createNiveau: (data) => api.post('/api/catalogue/niveaux/', data),
  updateNiveau: (id, data) => api.patch(`/api/catalogue/niveaux/${id}/`, data),
  deleteNiveau: (id) => api.delete(`/api/catalogue/niveaux/${id}/`),

  // Matières
  getMatieres: (params) => api.get('/api/catalogue/matieres/', { params }),
  getMatiere: (id) => api.get(`/api/catalogue/matieres/${id}/`),
  createMatiere: (data) => api.post('/api/catalogue/matieres/', data),
  updateMatiere: (id, data) => api.patch(`/api/catalogue/matieres/${id}/`, data),
  deleteMatiere: (id) => api.delete(`/api/catalogue/matieres/${id}/`),
}