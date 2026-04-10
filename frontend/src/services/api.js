import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore();
        if (authStore.accessToken) {
            config.headers.Authorization = `Bearer ${authStore.accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const authStore = useAuthStore();

        // 1. Skip interceptor for refresh or logout calls to prevent loops
        const isAuthLoop = originalRequest.url.includes('/auth/refresh') || originalRequest.url.includes('/auth/logout');

        if (error.response?.status === 401 && !originalRequest._retry && !isAuthLoop) {
            originalRequest._retry = true;

            try {
                await authStore.refreshAccessToken();
                originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`;
                return api(originalRequest);
            } catch (refreshError) {
                authStore.logout();
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default api;
