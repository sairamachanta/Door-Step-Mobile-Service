import { defineStore } from 'pinia'
import axios from 'axios'
import dayjs from 'dayjs'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const useBookingStore = defineStore('booking', {
    state: () => ({
        // Flow Data
        selectedBrandId: null,
        selectedModelId: null,
        selectedPricingId: null,

        // Data Cache (Dynamic)
        brands: [],
        models: [],
        services: [],
        pricingDetails: null,
        addresses: [],

        selectedAddons: [],
        appliedCoupon: null,
        selectedDate: null,
        selectedTimeSlot: null,
        serviceLocation: 'doorstep',
        selectedAddress: null,

        // Device Info
        deviceStorage: '',
        deviceColor: '',
        devicePhotos: [],
        deviceIMEI: '',
        deviceConditionDescription: '',
        customerNotes: '',

        // Safety & Privacy
        dataBackupRequested: false,
        privacyAgreementSigned: false,
        deviceInsuranceOpted: false,

        // Payment
        paymentMethod: 'cash',
        useWallet: false,

        // General
        loading: false,
        error: null
    }),

    getters: {
        selectedBrand: (state) => state.brands.find(b => b.id === state.selectedBrandId),
        selectedModel: (state) => state.models.find(m => m.id === state.selectedModelId),
        selectedService: (state) => state.pricingDetails?.service,

        finalPrice: (state) => {
            if (!state.pricingDetails) return 0
            let total = parseFloat(state.pricingDetails.final_price)

            // Add addons
            state.selectedAddons.forEach(addon => {
                total += parseFloat(addon.price)
            })

            // Subtract Coupon
            if (state.appliedCoupon) {
                if (state.appliedCoupon.discount_type === 'flat') {
                    total -= state.appliedCoupon.discount_value
                } else if (state.appliedCoupon.discount_type === 'percentage') {
                    total -= (total * state.appliedCoupon.discount_value / 100)
                }
            }

            // Insurance price from DB or static if not in DB
            if (state.deviceInsuranceOpted) {
                total += 200
            }

            return Math.max(0, total)
        }
    },

    actions: {
        async fetchBrands() {
            this.loading = true
            try {
                const response = await axios.get(`${API_BASE}/brands?active_only=true`)
                this.brands = response.data
            } catch (err) {
                this.error = 'Failed to load brands'
            } finally {
                this.loading = false
            }
        },

        async fetchModels(brandId) {
            this.loading = true
            try {
                const response = await axios.get(`${API_BASE}/models?brandId=${brandId}`)
                this.models = response.data
            } catch (err) {
                this.error = 'Failed to load models'
            } finally {
                this.loading = false
            }
        },

        async fetchServices(modelId) {
            this.loading = true
            try {
                const response = await axios.get(`${API_BASE}/services/pricing?modelId=${modelId}`)
                this.services = response.data
            } catch (err) {
                this.error = 'Failed to load services'
            } finally {
                this.loading = false
            }
        },

        async fetchPricingDetails(pricingId) {
            this.loading = true
            try {
                const response = await axios.get(`${API_BASE}/pricing/${pricingId}/details`)
                this.pricingDetails = response.data
                this.selectedPricingId = pricingId
            } catch (err) {
                this.error = 'Failed to load pricing details'
            } finally {
                this.loading = false
            }
        },

        async fetchAddresses() {
            this.loading = true
            try {
                const response = await axios.get(`${API_BASE}/users/me/addresses`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                    }
                })
                this.addresses = response.data
                // Auto select default if none selected
                if (!this.selectedAddress) {
                    this.selectedAddress = this.addresses.find(a => a.is_default) || this.addresses[0] || null
                }
            } catch (err) {
                console.error('Failed to fetch addresses:', err)
            } finally {
                this.loading = false
            }
        },

        async addAddress(addressData) {
            this.loading = true
            try {
                const response = await axios.post(`${API_BASE}/users/me/addresses`, addressData, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                    }
                })
                this.addresses.push(response.data)
                this.selectedAddress = response.data
                return { success: true }
            } catch (err) {
                return { success: false, message: err.response?.data?.detail || 'Failed to add address' }
            } finally {
                this.loading = false
            }
        },

        setBrand(brandId) {
            this.selectedBrandId = brandId
            this.selectedModelId = null
            this.selectedPricingId = null
            this.services = []
            this.pricingDetails = null
        },

        setModel(modelId) {
            this.selectedModelId = modelId
            this.selectedPricingId = null
            this.pricingDetails = null
        },

        setPricing(pricingId) {
            this.selectedPricingId = pricingId
        },

        toggleAddon(addon) {
            const index = this.selectedAddons.findIndex(a => a.id === addon.id)
            if (index === -1) {
                this.selectedAddons.push(addon)
            } else {
                this.selectedAddons.splice(index, 1)
            }
        },

        async createBooking() {
            this.loading = true
            this.error = null
            try {
                const payload = {
                    device_brand_id: this.selectedBrandId,
                    device_model_id: this.selectedModelId,
                    service_id: this.pricingDetails?.service_id,
                    service_pricing_id: this.selectedPricingId,
                    device_storage: this.deviceStorage,
                    device_color: this.deviceColor,
                    device_imei: this.deviceIMEI,
                    is_under_warranty: false, // Default or toggle
                    device_condition_description: this.deviceConditionDescription,
                    device_photos: this.devicePhotos.filter(p => p !== null),
                    preferred_date: this.selectedDate,
                    preferred_time_slot: this.selectedTimeSlot,
                    service_location: this.serviceLocation,
                    address_id: this.selectedAddress?.id,
                    data_backup_requested: this.dataBackupRequested,
                    privacy_agreement_signed: this.privacyAgreementSigned,
                    device_insurance_opted: this.deviceInsuranceOpted,
                    customer_notes: this.customerNotes,
                    payment_method: this.paymentMethod
                }

                const response = await axios.post(`${API_BASE}/bookings/create`, payload, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                    }
                })

                return {
                    success: true,
                    booking_id: response.data.id,
                    message: 'Booking created successfully'
                }
            } catch (err) {
                this.error = err.response?.data?.detail || 'Failed to create booking'
                return { success: false, message: this.error }
            } finally {
                this.loading = false
            }
        },

        clearBookingFlow() {
            this.$reset()
        }
    }
})
