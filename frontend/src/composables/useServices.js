import { ref } from 'vue';
import { servicesAPI } from '../services/dashboard';

export function useServices() {
    const categories = ref([]);
    const services = ref([]);
    const featuredServices = ref([]);
    const currentService = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const fetchCategories = async () => {
        loading.value = true;
        error.value = null;
        try {
            categories.value = await servicesAPI.getCategories();
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load categories';
            console.error('Error fetching categories:', err);
        } finally {
            loading.value = false;
        }
    };

    const fetchServices = async (params = {}) => {
        loading.value = true;
        error.value = null;
        try {
            const { categoryId, search } = params;
            let url = '/services?';
            if (categoryId && categoryId !== 'All') url += `category=${categoryId}&`;
            if (search) url += `search=${search}&`;

            services.value = await servicesAPI.getServices(url);
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load services';
            console.error('Error fetching services:', err);
        } finally {
            loading.value = false;
        }
    };

    const fetchFeaturedServices = async () => {
        loading.value = true;
        error.value = null;
        try {
            featuredServices.value = await servicesAPI.getFeaturedServices();
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load featured services';
            console.error('Error fetching featured services:', err);
        } finally {
            loading.value = false;
        }
    };

    const fetchServiceDetails = async (serviceId) => {
        loading.value = true;
        error.value = null;
        try {
            currentService.value = await servicesAPI.getServiceDetails(serviceId);
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load service details';
            console.error('Error fetching service details:', err);
        } finally {
            loading.value = false;
        }
    };

    return {
        categories,
        services,
        featuredServices,
        currentService,
        loading,
        error,
        fetchCategories,
        fetchServices,
        fetchFeaturedServices,
        fetchServiceDetails,
    };
}
