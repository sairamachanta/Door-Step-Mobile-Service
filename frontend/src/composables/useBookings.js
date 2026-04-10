import { ref } from 'vue';
import { bookingsAPI } from '../services/dashboard';

export function useBookings() {
    const bookings = ref([]);
    const currentBooking = ref(null);
    const loading = ref(false);
    const error = ref(null);
    const pagination = ref({
        page: 1,
        limit: 10,
        total: 0,
        totalPages: 0,
    });

    const fetchBookings = async (params = {}) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await bookingsAPI.getBookings(params);
            bookings.value = response.bookings || response.data || [];
            if (response.pagination) {
                pagination.value = response.pagination;
            }
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load bookings';
            console.error('Error fetching bookings:', err);
        } finally {
            loading.value = false;
        }
    };

    const fetchBookingDetails = async (bookingId) => {
        loading.value = true;
        error.value = null;
        try {
            currentBooking.value = await bookingsAPI.getBookingDetails(bookingId);
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to load booking details';
            console.error('Error fetching booking details:', err);
        } finally {
            loading.value = false;
        }
    };

    const cancelBooking = async (bookingId, reason = '') => {
        loading.value = true;
        error.value = null;
        try {
            await bookingsAPI.cancelBooking(bookingId, reason);
            // Refresh bookings list
            await fetchBookings({ page: pagination.value.page });
            return true;
        } catch (err) {
            error.value = err.response?.data?.message || 'Failed to cancel booking';
            console.error('Error cancelling booking:', err);
            return false;
        } finally {
            loading.value = false;
        }
    };

    const trackBooking = async (bookingId) => {
        try {
            return await bookingsAPI.trackBooking(bookingId);
        } catch (err) {
            console.error('Error tracking booking:', err);
            return null;
        }
    };

    return {
        bookings,
        currentBooking,
        loading,
        error,
        pagination,
        fetchBookings,
        fetchBookingDetails,
        cancelBooking,
        trackBooking,
    };
}
