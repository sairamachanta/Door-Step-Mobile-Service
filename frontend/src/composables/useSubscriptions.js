import { ref } from 'vue';
import { subscriptionAPI } from '../services/subscription';

export function useSubscriptions() {
    const plans = ref([]);
    const mySubscription = ref(null);
    const loading = ref(false);
    const error = ref(null);
    const purchaseLoading = ref(false);

    const fetchPlans = async () => {
        loading.value = true;
        error.value = null;
        try {
            plans.value = await subscriptionAPI.getPlans();
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load plans';
            console.error('Error fetching plans:', err);
        } finally {
            loading.value = false;
        }
    };

    const fetchMySubscription = async () => {
        try {
            mySubscription.value = await subscriptionAPI.getMySubscription();
        } catch (err) {
            console.error('Error fetching active subscription:', err);
        }
    };

    const purchasePlan = async (planId) => {
        purchaseLoading.value = true;
        try {
            const res = await subscriptionAPI.purchasePlan(planId);
            await fetchMySubscription();
            return res;
        } catch (err) {
            error.value = err.response?.data?.message || 'Purchase failed';
            throw err;
        } finally {
            purchaseLoading.value = false;
        }
    };

    return {
        plans,
        mySubscription,
        loading,
        error,
        purchaseLoading,
        fetchPlans,
        fetchMySubscription,
        purchasePlan,
    };
}
