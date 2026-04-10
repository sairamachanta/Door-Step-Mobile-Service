import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import SplashScreen from '../views/SplashScreen.vue';
import LoginPage from '../views/LoginPage.vue';
import SignupPage from '../views/SignupPage.vue';
import VerifyOTP from '../views/VerifyOTP.vue';
import ForgotPassword from '../views/ForgotPassword.vue';
import LandingPage from '../views/LandingPage.vue';
import DashboardPage from '../views/DashboardPage.vue';

const routes = [
    { path: '/', component: LandingPage, meta: { requiresAuth: false } },
    { path: '/login', component: LoginPage, meta: { requiresGuest: true } },
    { path: '/signup', component: SignupPage, meta: { requiresGuest: true } },
    { path: '/verify-otp', component: VerifyOTP, meta: { requiresGuest: true } },
    { path: '/forgot-password', component: ForgotPassword, meta: { requiresGuest: true } },

    // Shared authenticated routes (all roles)
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
    { path: '/home', redirect: '/dashboard' },
    { path: '/profile', component: () => import('../views/profile/ProfilePage.vue'), meta: { requiresAuth: true } },

    // Customer-facing routes
    {
        path: '/services',
        component: () => import('../views/services/ServicesPage.vue'),
        meta: { requiresAuth: true, requiredRoles: ['customer'] }
    },
    {
        path: '/bookings',
        component: () => import('../views/bookings/MyBookingsPage.vue'),
        meta: { requiresAuth: true, requiredRoles: ['customer'] }
    },
    {
        path: '/subscriptions',
        component: () => import('../views/subscriptions/MySubscriptionPage.vue'),
        meta: { requiresAuth: true, requiredRoles: ['customer'] }
    },

    // Booking Flow (customer only)
    { path: '/booking/select-brand', component: () => import('../views/booking/SelectBrand.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/select-model/:brandId', component: () => import('../views/booking/SelectModel.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/select-service/:modelId', component: () => import('../views/booking/SelectService.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/service-details', component: () => import('../views/booking/ServiceDetails.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/schedule', component: () => import('../views/booking/ScheduleBooking.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/address', component: () => import('../views/booking/SelectAddress.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/device-info', component: () => import('../views/booking/DeviceInfo.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/payment', component: () => import('../views/booking/PaymentPage.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },
    { path: '/booking/success/:bookingId', component: () => import('../views/booking/BookingSuccess.vue'), meta: { requiresAuth: true, requiredRoles: ['customer'] } },

    // Admin routes (role: admin — superadmin tier)
    {
        path: '/admin/dashboard',
        component: () => import('../views/admin/AdminDashboard.vue'),
        meta: { requiresAuth: true, requiredRoles: ['admin'] }
    },

    // Technician routes (role: technician)
    {
        path: '/technician/dashboard',
        component: () => import('../views/admin/TechnicianDashboard.vue'),
        meta: { requiresAuth: true, requiredRoles: ['technician'] }
    },

    // Legal
    { path: '/terms', component: () => import('../views/TermsPage.vue'), meta: { requiresAuth: false } },
    { path: '/privacy', component: () => import('../views/PrivacyPage.vue'), meta: { requiresAuth: false } },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.isAuthenticated;
    const userRole = authStore.userRole;

    console.log(`[Router] → ${to.path} | auth: ${isAuthenticated} | role: ${userRole}`);

    // 1. Must be authenticated
    if (to.meta.requiresAuth && !isAuthenticated) {
        return next('/login');
    }

    // 2. Guest-only routes (redirect logged-in users to their dashboard)
    if (to.meta.requiresGuest && isAuthenticated) {
        return next(getRoleDashboard(userRole));
    }

    // 3. Role-gated routes
    if (to.meta.requiredRoles && isAuthenticated) {
        if (!to.meta.requiredRoles.includes(userRole)) {
            console.warn(`[Router] Role '${userRole}' not allowed on ${to.path}. Redirecting.`);
            return next(getRoleDashboard(userRole));
        }
    }

    next();
});

/** Returns the default home route for each role */
export function getRoleDashboard(role) {
    switch (role) {
        case 'admin': return '/admin/dashboard';
        case 'technician': return '/technician/dashboard';
        default: return '/dashboard';
    }
}

export default router;
