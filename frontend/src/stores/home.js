import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const useHomeStore = defineStore('home', {
    state: () => ({
        banners: [],
        quickActions: [],
        userDevices: [],
        activeSubscription: null,
        recentBookings: [],
        featuredReviews: [],
        loading: false,
        error: null
    }),

    actions: {
        async fetchDashboardData() {
            this.loading = true
            this.error = null
            try {
                // Fetch banners
                const bannersRes = await axios.get(`${API_BASE_URL}/banners/active`)
                this.banners = bannersRes.data.banners || []

                // Fetch quick actions
                const actionsRes = await axios.get(`${API_BASE_URL}/services/quick-actions`)
                this.quickActions = actionsRes.data || []

                // Mock data for other sections (no backend endpoints yet)
                this.userDevices = []
                this.activeSubscription = null
                this.recentBookings = []

                this.featuredReviews = [
                    {
                        id: '1',
                        customer_name: 'Rajesh K.',
                        rating: 5,
                        review_text: 'Excellent service! Technician was very professional.',
                        created_at: '2024-01-18',
                        is_verified: true,
                        service_name: 'Screen Replacement'
                    },
                    {
                        id: '2',
                        customer_name: 'Priya S.',
                        rating: 5,
                        review_text: 'Quick and efficient battery replacement. Highly recommended!',
                        created_at: '2024-01-15',
                        is_verified: true,
                        service_name: 'Battery Replacement'
                    }
                ]

            } catch (err) {
                this.error = 'Failed to load dashboard data'
                console.error(err)
            } finally {
                this.loading = false
            }
        }
    }
})
