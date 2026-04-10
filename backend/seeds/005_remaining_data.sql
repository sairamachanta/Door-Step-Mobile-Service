-- Seed Script: Remaining Tables (Addons, Coupons, Time Slots, Service Centers)
-- Version: 001

-- 1. Service Addons
INSERT INTO service_addons (name, description, price, icon_name, is_active, display_order) VALUES
('Device Insurance', 'Covers accidental damage for 1 year', 200.00, 'Shield', true, 1),
('Screen Protector', 'Premium tempered glass with free installation', 499.00, 'Smartphone', true, 2),
('Back Protection', 'Scratch resistant transparent film for back panel', 299.00, 'Layers', true, 3),
('Extended Warranty', 'Additional 6 months warranty on this repair', 999.00, 'Clock', true, 4);

-- 2. Coupons
INSERT INTO coupons (code, description, discount_type, discount_value, min_order_amount, max_discount_amount, is_active) VALUES
('WELCOME100', 'Flat ₹100 off on your first repair', 'flat', 100.00, 500.00, 100.00, true),
('FESTIVE20', '20% off on all repairs up to ₹500', 'percentage', 20.00, 1000.00, 500.00, true),
('FREEDIAG', 'Free diagnostic service', 'flat', 0.00, 0.00, 0.00, true);

-- 3. Time Slots (Next 7 days)
DO $$
DECLARE
    d DATE;
    t TEXT;
    slots TEXT[] := ARRAY['09:00 AM - 12:00 PM', '12:00 PM - 03:00 PM', '03:00 PM - 06:00 PM', '06:00 PM - 09:00 PM'];
BEGIN
    FOR i IN 0..7 LOOP
        d := CURRENT_DATE + i;
        FOREACH t IN ARRAY slots LOOP
            INSERT INTO time_slots (date, slot_time, total_capacity) 
            VALUES (d, t, 10)
            ON CONFLICT (date, slot_time) DO NOTHING;
        END LOOP;
    END LOOP;
END $$;

-- 4. Service Centers
INSERT INTO service_centers (name, address_line1, city, state, pincode, phone, email, is_active) VALUES
('Premium Care Tiruppur', '123, Green Park Residency, Avinashi Road', 'Tiruppur', 'Tamil Nadu', '641601', '9876543210', 'tiruppur@doorstep.com', true),
('Tech Hub Coimbatore', '45, Lakshmi Complex, Gandhipuram', 'Coimbatore', 'Tamil Nadu', '641012', '9876543211', 'coimbatore@doorstep.com', true);
