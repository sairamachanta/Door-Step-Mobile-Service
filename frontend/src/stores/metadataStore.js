import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const useMetadataStore = defineStore('metadata', {
    state: () => ({
        categories: {},
        settings: {},
        initialized: false,
        loading: false,
        error: null
    }),

    getters: {
        getOptions: (state) => (category) => {
            return state.categories[category] || []
        },

        getLabel: (state) => (category, code) => {
            const options = state.categories[category] || []
            const found = options.find(o => o.code === code)
            return found ? found.label : code
        },

        getUIConfig: (state) => (category, code) => {
            const options = state.categories[category] || []
            const found = options.find(o => o.code === code)
            return found ? found.ui_config : {}
        },

        getSetting: (state) => (key, defaultValue = null) => {
            return state.settings[key] ?? defaultValue
        }
    },

    actions: {
        async initialize() {
            if (this.initialized) return

            this.loading = true
            try {
                const response = await axios.get(`${API_BASE_URL}/metadata`)
                this.categories = response.data.categories
                this.settings = response.data.settings
                this.initialized = true
                this.error = null
            } catch (err) {
                console.error('Metadata initialization failed:', err)
                this.error = err.message
            } finally {
                this.loading = false
            }
        }
    }
})
