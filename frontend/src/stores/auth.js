import { defineStore } from 'pinia';
import api from '../services/api';
import { EncryptionService } from '../utils/crypto';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
        loading: false,
        error: null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        currentUser: (state) => state.user,
        userRole: (state) => state.user?.role,
    },

    actions: {
        async signup(userData) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt(userData);
                const response = await api.post('/auth/signup', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Signup failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async verifyOTP(phone, otp_code, otp_type) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt({ phone, otp_code, otp_type });
                const response = await api.post('/auth/verify-otp', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }

                const { access_token, refresh_token, user } = data;
                this.setAuthData(access_token, refresh_token, user);
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'OTP Verification failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async login(phone, password) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt({ phone, password });
                const response = await api.post('/auth/login', encryptedPayload);

                let loginData = response.data;
                // If response is encrypted (has ciphertext), decrypt it
                if (loginData.ciphertext) {
                    loginData = await EncryptionService.decrypt(loginData, encryptedPayload.symmetric_key);
                }

                const { access_token, refresh_token, user } = loginData;
                this.setAuthData(access_token, refresh_token, user);
                return loginData;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Login failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async loginWithOTP(phone) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt({ phone });
                const response = await api.post('/auth/login-otp', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Failed to send OTP';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async forgotPassword(phone) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt({ phone });
                const response = await api.post('/auth/forgot-password', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Request failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async resetPassword(phone, otp_code, new_password, confirm_password) {
            this.loading = true;
            this.error = null;
            try {
                const payload = { phone, otp_code, new_password, confirm_password };
                const encryptedPayload = await EncryptionService.encrypt(payload);
                const response = await api.post('/auth/reset-password', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Reset Password failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async resendOTP(phone, otp_type) {
            try {
                const encryptedPayload = await EncryptionService.encrypt({ phone, otp_type });
                await api.post('/auth/resend-otp', encryptedPayload);
            } catch (error) {
                throw error;
            }
        },

        async logout() {
            // 1. Clear local state IMMEDIATELY to prevent loop cycles
            const tokenSnapshot = this.accessToken;
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');

            try {
                if (tokenSnapshot) {
                    // 2. Call API with _retry: true to tell interceptor NOT to try refreshing this specific call if it fails (401)
                    await api.post('/auth/logout', {}, { _retry: true });
                }
            } catch (e) {
                console.error("Logout API failed (expected if token expired)", e);
            } finally {
                // 3. Centralized redirection
                window.location.href = '/login';
            }
        },

        async refreshAccessToken() {
            try {
                if (!this.refreshToken) throw new Error('No refresh token');

                // We cannot use the 'api' instance here directly if it has interceptors that use the store
                // which might cause circular dependency or infinite loop if not careful.
                // However, we implemented the interceptor to only retry if 401. 
                // Here we make a direct call, or a call that skips the interceptor logic for 401 retry?
                // Actually, the interceptor handles the calling of this function.
                // We should use a clean axios instance or `api` but ensure we don't loop.
                // The token endpoint doesn't need auth header usually for refresh (it sends refresh token in body).

                // Let's use `api` but manually handle the request without the interceptor's "retry on 401" logic 
                // (which is bound to response interceptor, so if this fails with 401, it might loop if we are not careful).
                // Since `refresh_token` in body is what matters.

                // Important: Update: interceptors.request adds header. 

                const response = await api.post('/auth/refresh', { refresh_token: this.refreshToken });
                const { access_token, refresh_token } = response.data;

                this.accessToken = access_token;
                localStorage.setItem('accessToken', access_token);

                if (refresh_token) {
                    this.refreshToken = refresh_token;
                    localStorage.setItem('refreshToken', refresh_token);
                }

                return access_token;
            } catch (error) {
                this.logout();
                throw error;
            }
        },

        async fetchUserProfile() {
            try {
                const response = await api.get('/auth/me');
                this.user = response.data;
                localStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                console.error("Fetch profile failed", error);
            }
        },

        async updateProfile(profileData) {
            this.loading = true;
            this.error = null;
            try {
                const encryptedPayload = await EncryptionService.encrypt(profileData);
                const response = await api.patch('/users/me', encryptedPayload);

                let data = response.data;
                if (data.ciphertext) {
                    data = await EncryptionService.decrypt(data, encryptedPayload.symmetric_key);
                }

                this.user = data;
                localStorage.setItem('user', JSON.stringify(this.user));
                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Update failed';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        setAuthData(accessToken, refreshToken, user) {
            this.accessToken = accessToken;
            this.refreshToken = refreshToken;
            this.user = user;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
            localStorage.setItem('user', JSON.stringify(user));

            // Setup axios header immediately? Interceptor handles it.
        }
    },
});
