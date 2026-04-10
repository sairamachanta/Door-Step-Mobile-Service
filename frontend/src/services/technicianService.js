import api from './api'

const technicianService = {
    // Stats for the logged-in technician
    getStats: () => api.get('/technician/stats'),

    // Assigned bookings
    getMyBookings: ({ status = null, page = 1, limit = 20 } = {}) =>
        api.get('/technician/bookings', { params: { status, page, limit } }),

    getBookingDetail: (bookingId) => api.get(`/technician/bookings/${bookingId}`),

    // Update booking status
    updateBookingStatus: (bookingId, status, technicianNotes = null) =>
        api.patch(`/technician/bookings/${bookingId}/status`, {
            status,
            technician_notes: technicianNotes,
        }),

    // Customer Management (Technicians "control user")
    getCustomers: ({ status = null, search = null, page = 1, limit = 20 } = {}) =>
        api.get('/technician/customers', { params: { status, search, page, limit } }),

    updateCustomerStatus: (id, status) =>
        api.patch(`/technician/customers/${id}/status`, { status }),
}

export default technicianService
