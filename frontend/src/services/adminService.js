import api from './api'

const adminService = {
    // Stats
    getStats: () => api.get('/admin/stats'),

    // User Management (Generalized)
    getUsers: ({ role = null, status = null, search = null, page = 1, limit = 20 } = {}) =>
        api.get('/admin/users', { params: { role, status, search, page, limit } }),

    updateStaffStatus: (id, status) =>
        api.patch(`/admin/staff/${id}/status`, { status }),

    updateUserRole: (userId, role) =>
        api.patch(`/admin/users/${userId}/role`, { role }),

    updateCustomerStatus: (id, status) =>
        api.patch(`/admin/customers/${id}/status`, { status }),

    deleteUser: (userId) =>
        api.delete(`/admin/users/${userId}`),

    createStaff: (data) => api.post('/admin/staff', data),

    // Booking Management
    getAllBookings: ({ status = null, page = 1, limit = 20 } = {}) =>
        api.get('/admin/bookings', { params: { status, page, limit } }),

    assignBooking: (bookingId, technicianId) =>
        api.patch(`/admin/bookings/${bookingId}/assign`, { technician_id: technicianId }),

    updateBookingStatus: (bookingId, status, adminNotes = null) =>
        api.patch(`/admin/bookings/${bookingId}/status`, { status, admin_notes: adminNotes }),
}

export default adminService
