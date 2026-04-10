-- Seed Script: Device Models
-- Version: 001
-- Description: Popular models for top brands in India

-- Function to get brand ID by name
CREATE OR REPLACE FUNCTION get_brand_id(brand_name TEXT) RETURNS UUID AS $$
BEGIN
    RETURN (SELECT id FROM brands WHERE name = brand_name LIMIT 1);
END;
$$ LANGUAGE plpgsql;

-- Insert Apple Models
INSERT INTO device_models (brand_id, model_name, model_number, release_year, category, is_popular, display_order, storage_variants, color_variants, original_price) VALUES
(get_brand_id('Apple'), 'iPhone 15 Pro Max', 'A3106', 2023, 'smartphone', true, 1, '["256GB", "512GB", "1TB"]', '["Natural Titanium", "Blue Titanium", "White Titanium", "Black Titanium"]', 159900),
(get_brand_id('Apple'), 'iPhone 15 Pro', 'A3102', 2023, 'smartphone', true, 2, '["128GB", "256GB", "512GB", "1TB"]', '["Natural Titanium", "Blue Titanium", "White Titanium", "Black Titanium"]', 134900),
(get_brand_id('Apple'), 'iPhone 15', 'A3090', 2023, 'smartphone', true, 3, '["128GB", "256GB", "512GB"]', '["Pink", "Yellow", "Green", "Blue", "Black"]', 79900),
(get_brand_id('Apple'), 'iPhone 14 Pro Max', 'A2894', 2022, 'smartphone', false, 4, '["128GB", "256GB", "512GB", "1TB"]', '["Deep Purple", "Gold", "Silver", "Space Black"]', 139900),
(get_brand_id('Apple'), 'iPhone 13', 'A2633', 2021, 'smartphone', false, 5, '["128GB", "256GB", "512GB"]', '["Starlight", "Midnight", "Blue", "Pink", "Red"]', 69900),
(get_brand_id('Apple'), 'iPhone 11', 'A2221', 2019, 'smartphone', false, 6, '["64GB", "128GB", "256GB"]', '["Black", "Green", "Yellow", "Purple", "White"]', 49900);

-- Insert Samsung Models
INSERT INTO device_models (brand_id, model_name, model_number, release_year, category, is_popular, display_order, storage_variants, color_variants, original_price) VALUES
(get_brand_id('Samsung'), 'Galaxy S24 Ultra', 'SM-S928B', 2024, 'smartphone', true, 1, '["256GB", "512GB", "1TB"]', '["Titanium Gray", "Titanium Black", "Titanium Violet", "Titanium Yellow"]', 129999),
(get_brand_id('Samsung'), 'Galaxy S23 FE', 'SM-S711B', 2023, 'smartphone', true, 2, '["128GB", "256GB"]', '["Mint", "Graphite", "Purple", "Cream"]', 59999),
(get_brand_id('Samsung'), 'Galaxy A54 5G', 'SM-A546B', 2023, 'smartphone', true, 3, '["128GB", "256GB"]', '["Awesome Lime", "Awesome Violet", "Awesome Graphite", "Awesome White"]', 38999),
(get_brand_id('Samsung'), 'Galaxy M34 5G', 'SM-M346B', 2023, 'smartphone', false, 4, '["128GB"]', '["Midnight Blue", "Prism Silver", "Waterfall Blue"]', 18999),
(get_brand_id('Samsung'), 'Galaxy Z Fold 5', 'SM-F946B', 2023, 'smartphone', false, 5, '["256GB", "512GB", "1TB"]', '["Icy Blue", "Phantom Black", "Cream"]', 154999),
(get_brand_id('Samsung'), 'Guru Music 2', 'B310E', 2014, 'feature_phone', true, 10, '["NA"]', '["White", "Blue", "Gold", "Black"]', 1999);

-- Insert Xiaomi/Redmi/POCO Models
INSERT INTO device_models (brand_id, model_name, model_number, release_year, category, is_popular, display_order, storage_variants, color_variants, original_price) VALUES
(get_brand_id('Xiaomi'), 'Redmi Note 13 Pro+ 5G', '23090RA98I', 2024, 'smartphone', true, 1, '["256GB", "512GB"]', '["Fusion White", "Fusion Purple", "Fusion Black"]', 31999),
(get_brand_id('Xiaomi'), 'Redmi 12 5G', '23076RN8DY', 2023, 'smartphone', true, 2, '["128GB", "256GB"]', '["Jade Black", "Moonstone Silver", "Pastel Blue"]', 11999),
(get_brand_id('Xiaomi'), 'Xiaomi 14', '23127PN0CG', 2024, 'smartphone', true, 3, '["512GB"]', '["Black", "White", "Jade Green"]', 69999),
(get_brand_id('Xiaomi'), 'POCO X6 Pro 5G', '2311DRK48I', 2024, 'smartphone', true, 4, '["256GB", "512GB"]', '["Spectre Black", "Racing Grey", "POCO Yellow"]', 26999);

-- Insert OnePlus Models
INSERT INTO device_models (brand_id, model_name, model_number, release_year, category, is_popular, display_order, storage_variants, color_variants, original_price) VALUES
(get_brand_id('OnePlus'), 'OnePlus 12', 'CPH2573', 2024, 'smartphone', true, 1, '["256GB", "512GB"]', '["Flowy Emerald", "Silky Black"]', 64999),
(get_brand_id('OnePlus'), 'OnePlus Nord CE 3 Lite 5G', 'CPH2467', 2023, 'smartphone', true, 2, '["128GB", "256GB"]', '["Pastel Lime", "Chromatic Gray"]', 19999),
(get_brand_id('OnePlus'), 'OnePlus 11R 5G', 'CPH2487', 2023, 'smartphone', true, 3, '["128GB", "256GB"]', '["Galactic Silver", "Sonic Black"]', 39999);

-- Insert Google Models
INSERT INTO device_models (brand_id, model_name, model_number, release_year, category, is_popular, display_order, storage_variants, color_variants, original_price) VALUES
(get_brand_id('Google'), 'Pixel 8 Pro', 'GC3VE', 2023, 'smartphone', true, 1, '["128GB", "256GB", "512GB"]', '["Bay", "Porcelain", "Obsidian"]', 106999),
(get_brand_id('Google'), 'Pixel 7a', 'GWKK3', 2023, 'smartphone', true, 2, '["128GB"]', '["Charcoal", "Sea", "Snow", "Coral"]', 43999);

-- Clean up function
DROP FUNCTION get_brand_id(TEXT);

-- Verify
SELECT b.name as brand, dm.model_name, dm.release_year, dm.is_popular 
FROM device_models dm 
JOIN brands b ON dm.brand_id = b.id 
ORDER BY b.name, dm.display_order;
