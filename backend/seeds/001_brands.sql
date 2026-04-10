-- Seed Script: Mobile Brands for India
-- Version: 001
-- Description: Comprehensive list of all mobile brands available in India

-- Clear existing data (optional - comment out if you want to keep existing data)
-- TRUNCATE brands CASCADE;

-- Insert all mobile brands available in India
INSERT INTO brands (name, logo_url, category, is_active, display_order) VALUES
-- Tier 1: Premium Smartphones (Display Order 1-10)
('Apple', 'https://logo.clearbit.com/apple.com', 'smartphone', true, 1),
('Samsung', 'https://logo.clearbit.com/samsung.com', 'both', true, 2),
('Google', 'https://logo.clearbit.com/google.com', 'smartphone', true, 3),
('OnePlus', 'https://logo.clearbit.com/oneplus.com', 'smartphone', true, 4),
('Sony', 'https://logo.clearbit.com/sony.com', 'smartphone', true, 5),

-- Tier 2: Popular Chinese Brands (Display Order 11-25)
('Xiaomi', 'https://logo.clearbit.com/mi.com', 'smartphone', true, 11),
('Realme', 'https://logo.clearbit.com/realme.com', 'smartphone', true, 12),
('Vivo', 'https://logo.clearbit.com/vivo.com', 'smartphone', true, 13),
('Oppo', 'https://logo.clearbit.com/oppo.com', 'smartphone', true, 14),
('Nothing', 'https://logo.clearbit.com/nothing.tech', 'smartphone', true, 15),
('iQOO', 'https://logo.clearbit.com/iqoo.com', 'smartphone', true, 16),
('Honor', 'https://logo.clearbit.com/hihonor.com', 'smartphone', true, 17),
('Infinix', 'https://logo.clearbit.com/infinixmobility.com', 'smartphone', true, 18),
('Tecno', 'https://logo.clearbit.com/tecno-mobile.com', 'smartphone', true, 19),
('POCO', 'https://logo.clearbit.com/poco.net', 'smartphone', true, 20),

-- Tier 3: International Brands (Display Order 26-35)
('Motorola', 'https://logo.clearbit.com/motorola.com', 'smartphone', true, 26),
('Nokia', 'https://logo.clearbit.com/nokia.com', 'both', true, 27),
('Asus', 'https://logo.clearbit.com/asus.com', 'smartphone', true, 28),
('Lenovo', 'https://logo.clearbit.com/lenovo.com', 'smartphone', true, 29),

-- Tier 4: Indian Brands (Display Order 36-50)
('Lava', 'https://logo.clearbit.com/lavamobiles.com', 'both', true, 36),
('Micromax', 'https://logo.clearbit.com/micromaxinfo.com', 'both', true, 37),
('Karbonn', 'https://logo.clearbit.com/karbonnmobiles.com', 'both', true, 38),
('Intex', 'https://logo.clearbit.com/intex.in', 'both', true, 39),

-- Tier 5: Feature Phone Brands (Display Order 51-60)
('itel', 'https://logo.clearbit.com/itel-mobile.com', 'both', true, 51),
('Jio', 'https://logo.clearbit.com/jio.com', 'feature_phone', true, 52)

ON CONFLICT (name) DO UPDATE SET
    logo_url = EXCLUDED.logo_url,
    category = EXCLUDED.category,
    display_order = EXCLUDED.display_order,
    updated_at = CURRENT_TIMESTAMP;

-- Verify insertion
SELECT COUNT(*) as total_brands FROM brands WHERE is_active = true;
SELECT name, category, display_order FROM brands ORDER BY display_order LIMIT 10;
