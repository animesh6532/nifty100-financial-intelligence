import axiosInstance from './axios'

export const screenerApi = {
  create: (data) => axiosInstance.post('/screener/screens/', data),
  getAll: () => axiosInstance.get('/screener/screens/'),
  getById: (id) => axiosInstance.get(`/screener/screens/${id}/`),
  update: (id, data) => axiosInstance.put(`/screener/screens/${id}/`, data),
  delete: (id) => axiosInstance.delete(`/screener/screens/${id}/`),
}
