import axiosInstance from './axios'

export const authApi = {
  login: (credentials) => axiosInstance.post('/auth/login/', credentials),
  logout: () => axiosInstance.post('/auth/logout/'),
  register: (data) => axiosInstance.post('/auth/register/', data),
  refreshToken: (token) => axiosInstance.post('/auth/refresh/', { refresh: token }),
}
