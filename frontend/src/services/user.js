import api from './api';

export default {
    async getProfileStats() {
        const response = await api.get('/users/me/stats');
        return response.data;
    },

    async updateProfile(profileData) {
        const response = await api.patch('/users/me', profileData);
        return response.data;
    },

    async getAddresses() {
        const response = await api.get('/users/me/addresses');
        return response.data;
    },

    async addAddress(addressData) {
        const response = await api.post('/users/me/addresses', addressData);
        return response.data;
    },

    async deleteAddress(addressId) {
        await api.delete(`/users/me/addresses/${addressId}`);
    }
};
