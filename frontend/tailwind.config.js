/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'SF Pro Display', 'Roboto', 'sans-serif'],
            },
            colors: {
                // Neutral Grays
                gray: {
                    50: '#F9FAFB',   // Background
                    100: '#F3F4F6',  // Light backgrounds
                    200: '#E5E7EB',  // Borders
                    300: '#D1D5DB',
                    400: '#9CA3AF',  // Tertiary text
                    500: '#6B7280',  // Secondary text
                    600: '#4B5563',
                    700: '#374151',
                    800: '#1F2937',
                    900: '#111827',  // Primary text
                    950: '#030712',
                },
                // Primary Brand (Blue)
                primary: {
                    50: '#EFF6FF',
                    100: '#DBEAFE',
                    200: '#BFDBFE',
                    300: '#93C5FD',
                    400: '#60A5FA',
                    500: '#3B82F6',
                    600: '#2563EB',
                    700: '#1D4ED8',
                    800: '#1E40AF',
                    900: '#1E3A8A',
                    950: '#172554',
                },
                // Secondary Brand (Orange)
                secondary: {
                    50: '#FFF7ED',
                    100: '#FFEDD5',
                    200: '#FED7AA',
                    300: '#FDBA8C',
                    400: '#FB923C',
                    500: '#F97316',
                    600: '#EA580C',
                    700: '#C2410C',
                    800: '#9A3412',
                    900: '#7C2D12',
                    950: '#431407',
                },
                // Semantic Colors
                success: {
                    DEFAULT: '#10B981',
                    light: '#D1FAE5',
                    dark: '#065F46',
                },
                warning: {
                    DEFAULT: '#F59E0B',
                    light: '#FED7AA',
                    dark: '#92400E',
                },
                error: {
                    DEFAULT: '#EF4444',
                    light: '#FEE2E2',
                    dark: '#991B1B',
                },
                info: {
                    DEFAULT: '#3B82F6',
                    light: '#DBEAFE',
                    dark: '#1E40AF',
                },
            },
            spacing: {
                '4.5': '1.125rem',  // 18px
                '18': '4.5rem',     // 72px
                '22': '5.5rem',     // 88px
                'safe-bottom': 'env(safe-area-inset-bottom)',
            },
            borderRadius: {
                'sm': '4px',   // Badges
                'DEFAULT': '8px',  // Inputs, buttons
                'lg': '12px',  // Cards
                'xl': '16px',  // Large cards
                '2xl': '20px',
                '3xl': '24px',
            },
            boxShadow: {
                'subtle': '0 1px 3px rgba(0, 0, 0, 0.1)',
                'card': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'elevated': '0 10px 25px rgba(0, 0, 0, 0.15)',
                'glow-primary': '0 0 20px rgba(99, 102, 241, 0.3)',
            },
            fontSize: {
                'tiny': ['10px', { lineHeight: '14px' }],
                'xs': ['12px', { lineHeight: '16px' }],
                'sm': ['14px', { lineHeight: '20px' }],
                'base': ['16px', { lineHeight: '24px' }],
                'lg': ['18px', { lineHeight: '28px' }],
                'xl': ['20px', { lineHeight: '28px' }],
                '2xl': ['24px', { lineHeight: '32px' }],
                '3xl': ['30px', { lineHeight: '36px' }],
            },
            fontWeight: {
                normal: '400',
                medium: '500',
                semibold: '600',
                bold: '700',
            },
            transitionDuration: {
                '200': '200ms',
            },
            transitionTimingFunction: {
                'ease': 'ease-in-out',
            },
            animation: {
                'fade-in': 'fadeIn 200ms ease-in-out',
                'slide-up': 'slideUp 200ms ease-in-out',
                'slide-right': 'slideRight 200ms ease-in-out',
                'scale-in': 'scaleIn 200ms ease-in-out',
                'shimmer': 'shimmer 2s infinite',
                'spin-slow': 'spin 3s linear infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideRight: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(0)' },
                },
                scaleIn: {
                    '0%': { opacity: '0', transform: 'scale(0.95)' },
                    '100%': { opacity: '1', transform: 'scale(1)' },
                },
                shimmer: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' },
                },
            },
        },
    },
    plugins: [],
}
