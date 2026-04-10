-- Migration: Create Dynamic Database Schema for Mobile Repair Booking System
-- Version: 002 (Robust version)
-- Date: 2026-02-08
-- Description: Complete schema for brands, models, services, pricing, and enhanced bookings

-- Ensure updated_at function exists
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 1. BRANDS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS brands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE
);

ALTER TABLE brands ADD COLUMN IF NOT EXISTS logo_url VARCHAR(500);
ALTER TABLE brands ADD COLUMN IF NOT EXISTS category VARCHAR(20) NOT NULL DEFAULT 'smartphone' CHECK (category IN ('smartphone', 'feature_phone', 'both'));
ALTER TABLE brands ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE brands ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 999;
ALTER TABLE brands ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE brands ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Triggers for brands
DROP TRIGGER IF EXISTS trigger_brands_updated_at ON brands;
CREATE TRIGGER trigger_brands_updated_at
    BEFORE UPDATE ON brands
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 2. DEVICE MODELS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS device_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    model_name VARCHAR(200) NOT NULL,
    UNIQUE(brand_id, model_name)
);

ALTER TABLE device_models ADD COLUMN IF NOT EXISTS model_number VARCHAR(100);
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS release_year INTEGER CHECK (release_year >= 2000 AND release_year <= 2030);
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS category VARCHAR(20) DEFAULT 'smartphone' CHECK (category IN ('smartphone', 'feature_phone', 'tablet', 'smartwatch'));
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS storage_variants JSONB DEFAULT '[]'::jsonb;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS color_variants JSONB DEFAULT '[]'::jsonb;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS original_price DECIMAL(10,2);
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS is_popular BOOLEAN DEFAULT false;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 999;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS repair_complexity INTEGER CHECK (repair_complexity BETWEEN 1 AND 5);
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS avg_repair_time_minutes INTEGER DEFAULT 60;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE device_models ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Triggers for device_models
DROP TRIGGER IF EXISTS trigger_models_updated_at ON device_models;
CREATE TRIGGER trigger_models_updated_at
    BEFORE UPDATE ON device_models
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 3. SERVICES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_name VARCHAR(200) NOT NULL UNIQUE
);

-- Handle conversion if column 'name' exists but 'service_name' doesn't
DO $$ 
BEGIN 
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='services' AND column_name='name') 
       AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='services' AND column_name='service_name') THEN
        ALTER TABLE services RENAME COLUMN name TO service_name;
    END IF;
END $$;

ALTER TABLE services ADD COLUMN IF NOT EXISTS service_type VARCHAR(50) NOT NULL DEFAULT 'general';
ALTER TABLE services ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE services ADD COLUMN IF NOT EXISTS icon_name VARCHAR(50);
ALTER TABLE services ADD COLUMN IF NOT EXISTS icon_color VARCHAR(7) DEFAULT '#6366F1';
ALTER TABLE services ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE services ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 999;
ALTER TABLE services ADD COLUMN IF NOT EXISTS requires_parts BOOLEAN DEFAULT true;
ALTER TABLE services ADD COLUMN IF NOT EXISTS is_diagnostic BOOLEAN DEFAULT false;
ALTER TABLE services ADD COLUMN IF NOT EXISTS typical_symptoms JSONB DEFAULT '[]'::jsonb;
ALTER TABLE services ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE services ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Triggers for services
DROP TRIGGER IF EXISTS trigger_services_updated_at ON services;
CREATE TRIGGER trigger_services_updated_at
    BEFORE UPDATE ON services
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 4. SERVICE PRICING TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS service_pricing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_model_id UUID NOT NULL REFERENCES device_models(id) ON DELETE CASCADE,
    service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    part_grade VARCHAR(20) CHECK (part_grade IN ('original', 'oem', 'aaa_plus', 'compatible', 'refurbished')),
    effective_from DATE DEFAULT CURRENT_DATE,
    UNIQUE(device_model_id, service_id, part_grade, effective_from)
);

ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS part_name VARCHAR(200);
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS part_cost DECIMAL(10,2) NOT NULL DEFAULT 0;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS labor_cost DECIMAL(10,2) NOT NULL DEFAULT 0;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS total_cost DECIMAL(10,2) GENERATED ALWAYS AS (part_cost + labor_cost) STORED;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS discount_percentage DECIMAL(5,2) DEFAULT 0 CHECK (discount_percentage >= 0 AND discount_percentage <= 100);
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS discounted_price DECIMAL(10,2) GENERATED ALWAYS AS (part_cost + labor_cost - ((part_cost + labor_cost) * discount_percentage / 100)) STORED;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS final_price DECIMAL(10,2) NOT NULL DEFAULT 0;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS estimated_time_min INTEGER DEFAULT 30;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS estimated_time_max INTEGER DEFAULT 60;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS warranty_months INTEGER DEFAULT 6;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS is_doorstep_available BOOLEAN DEFAULT true;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS availability_status VARCHAR(20) DEFAULT 'available' CHECK (availability_status IN ('available', 'limited_stock', 'out_of_stock', 'coming_soon'));
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS effective_to DATE;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE service_pricing ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Triggers for service_pricing
DROP TRIGGER IF EXISTS trigger_pricing_updated_at ON service_pricing;
CREATE TRIGGER trigger_pricing_updated_at
    BEFORE UPDATE ON service_pricing
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 5. SERVICE ADDONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS service_addons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 999,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE service_addons ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE service_addons ADD COLUMN IF NOT EXISTS icon_name VARCHAR(50);

-- ============================================================================
-- 6. COUPONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS coupons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_value DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE coupons ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS discount_type VARCHAR(20) CHECK (discount_type IN ('percentage', 'fixed', 'flat'));
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS min_order_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS max_discount_amount DECIMAL(10,2);
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS valid_from DATE DEFAULT CURRENT_DATE;
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS valid_to DATE;
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS usage_limit INTEGER;
ALTER TABLE coupons ADD COLUMN IF NOT EXISTS used_count INTEGER DEFAULT 0;

-- Rename valid_until to valid_to if exists
DO $$ 
BEGIN 
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='coupons' AND column_name='valid_until') 
       AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='coupons' AND column_name='valid_to') THEN
        ALTER TABLE coupons RENAME COLUMN valid_until TO valid_to;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='coupons' AND column_name='usage_count') 
       AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='coupons' AND column_name='used_count') THEN
        ALTER TABLE coupons RENAME COLUMN usage_count TO used_count;
    END IF;
END $$;

-- ============================================================================
-- 7. TIME SLOTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS time_slots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    slot_time VARCHAR(50) NOT NULL,
    UNIQUE(date, slot_time)
);

ALTER TABLE time_slots ADD COLUMN IF NOT EXISTS total_capacity INTEGER DEFAULT 10;
ALTER TABLE time_slots ADD COLUMN IF NOT EXISTS booked_count INTEGER DEFAULT 0;
ALTER TABLE time_slots ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE time_slots ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- ============================================================================
-- 8. SERVICE CENTERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS service_centers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL
);

ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS address_line1 VARCHAR(200);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS address_line2 VARCHAR(200);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS city VARCHAR(100);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS state VARCHAR(100);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS pincode VARCHAR(10);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS latitude DECIMAL(10,8);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS longitude DECIMAL(11,8);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS operating_hours JSONB;
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE service_centers ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- ============================================================================
-- 9. ENHANCE EXISTING BOOKINGS TABLE
-- ============================================================================

-- Add new columns if they don't exist
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS booking_number VARCHAR(50);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_brand_id UUID REFERENCES brands(id);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_model_id UUID REFERENCES device_models(id);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_id UUID REFERENCES services(id);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_pricing_id UUID REFERENCES service_pricing(id);

-- Device details
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_storage VARCHAR(50);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_color VARCHAR(50);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_purchase_date DATE;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS is_under_warranty BOOLEAN DEFAULT false;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_condition_description TEXT;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_photos JSONB DEFAULT '[]'::jsonb;

-- Pricing details (snapshot)
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS selected_part_grade VARCHAR(20);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS quoted_part_cost DECIMAL(10,2);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS quoted_labor_cost DECIMAL(10,2);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS quoted_subtotal DECIMAL(10,2);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS discount_amount DECIMAL(10,2) DEFAULT 0;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(50);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS final_price DECIMAL(10,2);

-- Scheduling
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS preferred_date DATE;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS preferred_time_slot VARCHAR(50);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS estimated_duration_minutes INTEGER;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS actual_start_time TIMESTAMP;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS actual_end_time TIMESTAMP;

-- Location
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_location VARCHAR(20) CHECK (service_location IN ('doorstep', 'service_center'));
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS full_address_snapshot JSONB;

-- Assignment
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS technician_id UUID REFERENCES technicians(id);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS assigned_at TIMESTAMP;

-- Status tracking
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS payment_status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50);

-- Safety & Insurance
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS data_backup_requested BOOLEAN DEFAULT false;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS privacy_agreement_signed BOOLEAN DEFAULT false;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS device_insurance_opted BOOLEAN DEFAULT false;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS insurance_premium DECIMAL(10,2);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS insurance_coverage_amount DECIMAL(10,2);

-- Notes
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS customer_notes TEXT;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS technician_notes TEXT;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS admin_notes TEXT;

-- Cancellation
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS cancelled_by UUID REFERENCES users(id);
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS cancellation_reason TEXT;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS cancelled_at TIMESTAMP;

-- Additional timestamps
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS confirmed_at TIMESTAMP;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;

-- Handle renames and aliases
-- If user_id exists but customer_id doesn't, we'll keep using user_id in the app.
-- The plan mentioned customer_id, so let's add it if missing as a duplicate or rethink.
-- Actually, let's keep it simple: use user_id.

-- ============================================================================
-- 10. INDEXES
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_brands_active ON brands(is_active, display_order);
CREATE INDEX IF NOT EXISTS idx_brands_category ON brands(category) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_models_brand ON device_models(brand_id, is_active);
CREATE INDEX IF NOT EXISTS idx_models_popular ON device_models(is_popular, display_order) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_services_type ON services(service_type, display_order) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_services_diagnostic ON services(is_diagnostic) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_pricing_model_service ON service_pricing(device_model_id, service_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status, created_at DESC);

-- ============================================================================
-- 11. TRIGGERS & FUNCTIONS
-- ============================================================================

-- Function to generate booking number
CREATE OR REPLACE FUNCTION generate_booking_number()
RETURNS TRIGGER AS $$
DECLARE
    sequence_num INTEGER;
    date_part VARCHAR(8);
BEGIN
    -- Get date part (YYYYMMDD)
    date_part := TO_CHAR(CURRENT_DATE, 'YYYYMMDD');
    
    -- Get sequence number for today
    SELECT COALESCE(MAX(CAST(SUBSTRING(booking_number FROM 12) AS INTEGER)), 0) + 1
    INTO sequence_num
    FROM bookings
    WHERE booking_number LIKE 'B-' || date_part || '-%';
    
    -- Generate booking number: B-YYYYMMDD-NNNN
    NEW.booking_number := 'B-' || date_part || '-' || LPAD(sequence_num::TEXT, 4, '0');
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-generate booking number
DROP TRIGGER IF EXISTS trigger_generate_booking_number ON bookings;
CREATE TRIGGER trigger_generate_booking_number
    BEFORE INSERT ON bookings
    FOR EACH ROW
    WHEN (NEW.booking_number IS NULL)
    EXECUTE FUNCTION generate_booking_number();

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
