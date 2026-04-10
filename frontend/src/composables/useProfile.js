import { ref } from 'vue';
import userService from '../services/user';

export function useProfile() {
    const stats = ref(null);
    const addresses = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const fetchStats = async () => {
        try {
            loading.value = true;
            stats.value = await userService.getProfileStats();
        } catch (err) {
            error.value = err.message || 'Failed to fetch stats';
        } finally {
            loading.value = false;
        }
    };

    const fetchAddresses = async () => {
        try {
            loading.value = true;
            addresses.value = await userService.getAddresses();
        } catch (err) {
            error.value = err.message || 'Failed to fetch addresses';
        } finally {
            loading.value = false;
        }
    };

    const addAddress = async (addressData) => {
        try {
            loading.value = true;
            const newAddress = await userService.addAddress(addressData);
            addresses.value.push(newAddress);
            return newAddress;
        } catch (err) {
            error.value = err.message || 'Failed to add address';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const removeAddress = async (addressId) => {
        try {
            loading.value = true;
            await userService.deleteAddress(addressId);
            addresses.value = addresses.value.filter(a => a.id !== addressId);
        } catch (err) {
            error.value = err.message || 'Failed to delete address';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    return {
        stats,
        addresses,
        loading,
        error,
        fetchStats,
        fetchAddresses,
        addAddress,
        removeAddress
    };
}
