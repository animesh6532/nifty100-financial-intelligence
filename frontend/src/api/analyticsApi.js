import axiosInstance from './axios'

export const analyticsApi = {
  getMetrics: (companyId) => axiosInstance.get(`/analytics/metrics/?company=${companyId}`),
  getSectorAnalysis: () => axiosInstance.get('/analytics/sectors/'),
}
