import api from './axios'

export const ressourcesApi = {
  getRessources: (params) => api.get('/api/ressources/', { params }),
  getRessource: (id) => api.get(`/api/ressources/${id}/`),
  createRessource: (formData) => api.post('/api/ressources/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  updateRessource: (id, formData) => api.patch(`/api/ressources/${id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  deleteRessource: (id) => api.delete(`/api/ressources/${id}/`),
  getDownloadUrl: (id) => `/api/ressources/${id}/telecharger/`,
  getPreviewUrl: (id) => `/api/ressources/${id}/apercu/`,
}
