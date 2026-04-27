import api from './axios'

export const communiquesApi = {
  getCommuniques: (params) => api.get('/api/communiques/', { params }),
  getCommunique: (id) => api.get(`/api/communiques/${id}/`),
  createCommunique: (data) => api.post('/api/communiques/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  updateCommunique: (id, data) => api.patch(`/api/communiques/${id}/`, data),
  deleteCommunique: (id) => api.delete(`/api/communiques/${id}/`),
  liker: (id) => api.post(`/api/communiques/${id}/liker/`),
  getCommentaires: (id) => api.get(`/api/communiques/${id}/commenter/`),
  commenter: (id, contenu) => api.post(`/api/communiques/${id}/commenter/`, { contenu }),
  supprimerCommentaire: (communiqueId, commentaireId) =>
    api.delete(`/api/communiques/${communiqueId}/commenter/${commentaireId}/`),
  inscrire: (data) => api.post('/api/auth/inscription/', data),
  login: (data) => api.post('/api/auth/login/', data),
}