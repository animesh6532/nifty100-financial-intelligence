import axiosInstance from './axios'

export const companyApi = {
  getAll: (params) => axiosInstance.get('/companies/', { params }),
  getById: (id) => axiosInstance.get(`/companies/${id}/`),
  getFinancials: (id) => axiosInstance.get(`/companies/${id}/financial-data/`),
}
