import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    withCredentials: true,
});

// Add request interceptor for tokens if needed
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const subscriptionAPI = {
    async getPlans() {
        const response = await api.get('/plans');
        return response.data;
    },

    async getMySubscription() {
        const response = await api.get('/subscriptions/my');
        return response.data;
    },

    async purchasePlan(planId) {
        const response = await api.post('/subscriptions/purchase', { plan_id: planId });
        return response.data;
    }
};
