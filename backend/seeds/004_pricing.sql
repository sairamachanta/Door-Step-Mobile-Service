-- Seed Script: Service Pricing
-- Version: 001
-- Description: Realistic pricing for device + service combinations

-- Helpers
CREATE OR REPLACE FUNCTION get_model_id(m_name TEXT) RETURNS UUID AS $$
BEGIN
    RETURN (SELECT id FROM device_models WHERE model_name = m_name LIMIT 1);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_service_id(s_name TEXT) RETURNS UUID AS $$
BEGIN
    RETURN (SELECT id FROM services WHERE service_name = s_name LIMIT 1);
END;
$$ LANGUAGE plpgsql;

-- INSERT PRICING DATA
-- Note: Using common pricing structure for Indian market

-------------------------------------------------------------------------------
-- APPLE IPHONE 15 PRO MAX
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('iPhone 15 Pro Max'), get_service_id('Screen Replacement (Cracked)'), 'Original OLED Panel', 'original', 38000, 2000, 40000, 12, 60, 120),
(get_model_id('iPhone 15 Pro Max'), get_service_id('Screen Replacement (Cracked)'), 'OEM Premium Panel', 'oem', 22000, 2000, 24000, 6, 60, 120),
(get_model_id('iPhone 15 Pro Max'), get_service_id('Battery Replacement'), 'High Capacity Battery', 'original', 8500, 1000, 9500, 12, 30, 45),
(get_model_id('iPhone 15 Pro Max'), get_service_id('Rear Camera Repair'), 'Main Camera Module', 'original', 12000, 1500, 13500, 6, 45, 90);

-------------------------------------------------------------------------------
-- APPLE IPHONE 13
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('iPhone 13'), get_service_id('Screen Replacement (Cracked)'), 'Original OLED Panel', 'original', 18000, 1500, 19500, 12, 45, 90),
(get_model_id('iPhone 13'), get_service_id('Screen Replacement (Cracked)'), 'OEM Premium Panel', 'oem', 11000, 1500, 12500, 6, 45, 90),
(get_model_id('iPhone 13'), get_service_id('Battery Replacement'), 'Replacement Battery', 'original', 5500, 800, 6300, 12, 30, 45);

-------------------------------------------------------------------------------
-- SAMSUNG GALAXY S24 ULTRA
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('Galaxy S24 Ultra'), get_service_id('Screen Replacement (Cracked)'), 'Original AMOLED Display', 'original', 28000, 2000, 30000, 12, 60, 120),
(get_model_id('Galaxy S24 Ultra'), get_service_id('Battery Replacement'), 'Original Samsung Battery', 'original', 4500, 1000, 5500, 12, 30, 60);

-------------------------------------------------------------------------------
-- REDMI NOTE 13 PRO+ 5G
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('Redmi Note 13 Pro+ 5G'), get_service_id('Screen Replacement (Cracked)'), 'Original Curved AMOLED', 'original', 10500, 1000, 11500, 6, 45, 90),
(get_model_id('Redmi Note 13 Pro+ 5G'), get_service_id('Battery Replacement'), 'Original MI Battery', 'original', 2200, 500, 2700, 6, 30, 45);

-------------------------------------------------------------------------------
-- ONEPLUS 12
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('OnePlus 12'), get_service_id('Screen Replacement (Cracked)'), 'Original Fluid AMOLED', 'original', 16500, 1500, 18000, 12, 60, 120),
(get_model_id('OnePlus 12'), get_service_id('Battery Replacement'), 'Original OnePlus Battery', 'original', 3500, 800, 4300, 12, 30, 60);

-------------------------------------------------------------------------------
-- PIXEL 8 PRO
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('Pixel 8 Pro'), get_service_id('Screen Replacement (Cracked)'), 'Original Super Actua Display', 'original', 24000, 2000, 26000, 12, 60, 120),
(get_model_id('Pixel 8 Pro'), get_service_id('Battery Replacement'), 'Original Google Battery', 'original', 4800, 1000, 5800, 12, 30, 60);

-------------------------------------------------------------------------------
-- FEATURE PHONE: GURU MUSIC 2
-------------------------------------------------------------------------------
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max) VALUES
(get_model_id('Guru Music 2'), get_service_id('Screen Replacement (Cracked)'), 'Replacement TFT Screen', 'compatible', 400, 200, 600, 3, 20, 40),
(get_model_id('Guru Music 2'), get_service_id('Battery Replacement'), 'BL-5C Compatible Battery', 'compatible', 300, 0, 300, 3, 5, 10);

-- COMMON DIAGNOSTIC (FREE for all popular models)
-- Note: Usually we'd cross join this, but for seed we can do it for a few
INSERT INTO service_pricing (device_model_id, service_id, part_name, part_grade, part_cost, labor_cost, final_price, warranty_months, estimated_time_min, estimated_time_max)
SELECT dm.id, get_service_id('Complete Diagnostic'), 'N/A', 'original', 0, 0, 0, 0, 15, 30
FROM device_models dm
WHERE dm.is_popular = true;

-- Clean up
DROP FUNCTION get_model_id(TEXT);
DROP FUNCTION get_service_id(TEXT);

-- Verify stats
SELECT count(*) as total_pricing_records FROM service_pricing;
