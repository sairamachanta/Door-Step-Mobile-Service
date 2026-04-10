import { ref } from 'vue';
import { dashboardAPI } from '../services/dashboard';

export function useDashboard() {
    const stats = ref(null);
    const activeBooking = ref(null);
    const recentBookings = ref([]);
    const quickActions = ref([]);

    const loading = ref({
        stats: false,
        activeBooking: false,
        recentBookings: false,
        quickActions: false,
    });

    const error = ref({
        stats: null,
        activeBooking: null,
        recentBookings: null,
        quickActions: null,
    });

    const fetchStats = async () => {
        loading.value.stats = true;
        error.value.stats = null;
        try {
            stats.value = await dashboardAPI.getStats();
        } catch (err) {
            error.value.stats = err.response?.data?.message || 'Failed to load statistics';
            console.error('Error fetching stats:', err);
        } finally {
            loading.value.stats = false;
        }
    };

    const fetchActiveBooking = async () => {
        loading.value.activeBooking = true;
        error.value.activeBooking = null;
        try {
            activeBooking.value = await dashboardAPI.getActiveBooking();
        } catch (err) {
            if (err.response?.status === 404) {
                // No active booking - this is not an error
                activeBooking.value = null;
            } else {
                error.value.activeBooking = err.response?.data?.message || 'Failed to load active booking';
                console.error('Error fetching active booking:', err);
            }
        } finally {
            loading.value.activeBooking = false;
        }
    };

    const fetchRecentBookings = async (limit = 3) => {
        loading.value.recentBookings = true;
        error.value.recentBookings = null;
        try {
            recentBookings.value = await dashboardAPI.getRecentBookings(limit);
        } catch (err) {
            error.value.recentBookings = err.response?.data?.message || 'Failed to load recent bookings';
            console.error('Error fetching recent bookings:', err);
        } finally {
            loading.value.recentBookings = false;
        }
    };

    const fetchQuickActions = async () => {
        loading.value.quickActions = true;
        error.value.quickActions = null;
        try {
            quickActions.value = await dashboardAPI.getQuickActions();
        } catch (err) {
            error.value.quickActions = err.response?.data?.message || 'Failed to load quick actions';
            console.error('Error fetching quick actions:', err);
        } finally {
            loading.value.quickActions = false;
        }
    };

    const fetchAll = async () => {
        await Promise.all([
            fetchStats(),
            fetchActiveBooking(),
            fetchRecentBookings(),
            fetchQuickActions(),
        ]);
    };

    const retry = (type) => {
        switch (type) {
            case 'stats':
                return fetchStats();
            case 'activeBooking':
                return fetchActiveBooking();
            case 'recentBookings':
                return fetchRecentBookings();
            case 'quickActions':
                return fetchQuickActions();
            default:
                return fetchAll();
        }
    };

    return {
        stats,
        activeBooking,
        recentBookings,
        quickActions,
        loading,
        error,
        fetchStats,
        fetchActiveBooking,
        fetchRecentBookings,
        fetchQuickActions,
        fetchAll,
        retry,
    };
}
