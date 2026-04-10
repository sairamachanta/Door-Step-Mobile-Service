import api from './api';

// Dashboard API endpoints
export const dashboardAPI = {
    // Get dashboard statistics
    async getStats() {
        const response = await api.get('/dashboard/stats');
        return response.data;
    },

    // Get active booking
    async getActiveBooking() {
        const response = await api.get('/bookings/active');
        return response.data;
    },

    // Get recent bookings
    async getRecentBookings(limit = 3) {
        const response = await api.get(`/bookings/recent?limit=${limit}`);
        return response.data;
    },

    // Get quick actions
    async getQuickActions() {
        const response = await api.get('/dashboard/quick-actions');
        return response.data;
    },
};

// Services API endpoints
export const servicesAPI = {
    // Get all service categories
    async getCategories() {
        const response = await api.get('/services/categories');
        return response.data;
    },

    // Get services by category
    async getServices(urlOrParams) {
        let url = '/services';
        if (typeof urlOrParams === 'string') {
            url = urlOrParams;
        } else if (urlOrParams) {
            const params = new URLSearchParams(urlOrParams).toString();
            url += `?${params}`;
        }
        const response = await api.get(url);
        return response.data;
    },

    // Get featured services
    async getFeaturedServices() {
        const response = await api.get('/services/featured');
        return response.data;
    },

    // Get service details
    async getServiceDetails(serviceId) {
        const response = await api.get(`/services/${serviceId}`);
        return response.data;
    },
};

// Bookings API endpoints
export const bookingsAPI = {
    // Get user bookings with filters
    async getBookings(params = {}) {
        const { status, page = 1, limit = 10 } = params;
        let url = `/bookings?page=${page}&limit=${limit}`;
        if (status) url += `&status=${status}`;
        const response = await api.get(url);
        return response.data;
    },

    // Get booking details
    async getBookingDetails(bookingId) {
        const response = await api.get(`/bookings/${bookingId}`);
        return response.data;
    },

    // Cancel booking
    async cancelBooking(bookingId, reason = '') {
        const response = await api.put(`/bookings/${bookingId}/cancel`, { reason });
        return response.data;
    },

    // Track booking status
    async trackBooking(bookingId) {
        const response = await api.get(`/bookings/${bookingId}/track`);
        return response.data;
    },
};

// Subscriptions API endpoints
export const subscriptionsAPI = {
    // Get available plans
    async getPlans() {
        const response = await api.get('/subscriptions/plans');
        return response.data;
    },

    // Get current subscription
    async getCurrentSubscription() {
        const response = await api.get('/subscriptions/current');
        return response.data;
    },

    // Subscribe to a plan
    async subscribe(planId, paymentMethodId) {
        const response = await api.post('/subscriptions/subscribe', {
            plan_id: planId,
            payment_method_id: paymentMethodId,
        });
        return response.data;
    },

    // Upgrade subscription
    async upgradeSubscription(newPlanId) {
        const response = await api.put('/subscriptions/upgrade', {
            new_plan_id: newPlanId,
        });
        return response.data;
    },

    // Cancel subscription
    async cancelSubscription(reason = '') {
        const response = await api.put('/subscriptions/cancel', { reason });
        return response.data;
    },
};

// Profile API endpoints
export const profileAPI = {
    // Get user profile
    async getProfile() {
        const response = await api.get('/users/profile');
        return response.data;
    },

    // Update user profile
    async updateProfile(data) {
        const response = await api.put('/users/profile', data);
        return response.data;
    },

    // Get saved addresses
    async getAddresses() {
        const response = await api.get('/users/addresses');
        return response.data;
    },

    // Add new address
    async addAddress(addressData) {
        const response = await api.post('/users/addresses', addressData);
        return response.data;
    },

    // Update address
    async updateAddress(addressId, addressData) {
        const response = await api.put(`/users/addresses/${addressId}`, addressData);
        return response.data;
    },

    // Delete address
    async deleteAddress(addressId) {
        const response = await api.delete(`/users/addresses/${addressId}`);
        return response.data;
    },

    // Get payment methods
    async getPaymentMethods() {
        const response = await api.get('/users/payment-methods');
        return response.data;
    },
};

export default {
    dashboard: dashboardAPI,
    services: servicesAPI,
    bookings: bookingsAPI,
    subscriptions: subscriptionsAPI,
    profile: profileAPI,
};
