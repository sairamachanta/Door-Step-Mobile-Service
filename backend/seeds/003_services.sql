-- Seed Script: Repair Services
-- Version: 001
-- Description: Comprehensive list of repair services/issues

INSERT INTO services (service_name, service_type, description, icon_name, icon_color, display_order, requires_parts, is_diagnostic, typical_symptoms) VALUES
-- General / Diagnostic
('Complete Diagnostic', 'general', 'Full checkup of your device to identify any hidden issues. Recommended if you are unsure what is wrong.', 'Search', '#6366F1', 1, false, true, '["Phone hanging", "Unusual behavior", "Unknown issue"]'),
('Phone Not Turning On', 'general', 'Expert analysis and repair for devices that are completely dead or stuck on logo.', 'Power', '#EF4444', 2, true, false, '["Black screen", "Stuck on logo", "Not charging"]'),

-- Screen / Display
('Screen Replacement (Cracked)', 'screen', 'High-quality screen replacement for cracked or shattered glass. Restores touch and display.', 'Smartphone', '#3B82F6', 10, true, false, '["Cracked glass", "Shattered screen"]'),
('Display Not Working', 'screen', 'Repair or replacement for screens with no display, black spots, or vertical lines.', 'Monitor', '#3B82F6', 11, true, false, '["Black screen", "Inky spots", "Vertical lines"]'),
('Touch Not Responsive', 'screen', 'Fix for touch screens that are Lagging, ghost touching, or completely unresponsive.', 'Fingerprint', '#3B82F6', 12, true, false, '["Touch not working", "Ghost touch", "Dead zones"]'),

-- Battery
('Battery Replacement', 'battery', 'Replacement of old or swollen battery with a new high-capacity one to restore battery life.', 'Battery', '#10B981', 20, true, false, '["Fast draining", "Phone heating", "Battery swollen"]'),
('Battery Not Charging', 'battery', 'Fix for devices that show charging but percentage does not increase, or not detecting charger.', 'Zap', '#10B981', 21, true, false, '["Not charging", "Slow charging", "Cable loose"]'),

-- Charging
('Charging Port Repair', 'charging', 'Repair or replacement of the USB-C / Lightning port if it is loose or damaged.', 'Plug', '#F59E0B', 30, true, false, '["Loose port", "Not detecting cable", "Moisture error"]'),

-- Camera
('Rear Camera Repair', 'camera', 'Fix for blurry photos, focus issues, or complete camera failure of the back camera.', 'Camera', '#EC4899', 40, true, false, '["Blurry photos", "Camera app crash", "Black view"]'),
('Front Camera Repair', 'camera', 'Fix for selfie camera issues including FaceID / Face Unlock problems.', 'UserSquare', '#EC4899', 41, true, false, '["Selfie issues", "Face ID failure", "Blurry selfies"]'),
('Camera Glass Replacement', 'body', 'Replacement of the protective glass cover of the rear camera if it is cracked.', 'Maximize', '#EC4899', 42, true, false, '["Cracked lens", "Flash reflecting"]'),

-- Audio
('Earpiece Speaker Fix', 'audio', 'Fix for low volume or distorted sound during calls when you hold the phone to your ear.', 'Volume1', '#8B5CF6', 50, true, false, '["Can''t hear caller", "Low voice", "Crackling sound"]'),
('Loudspeaker Repair', 'audio', 'Repair for speaker issues when playing music, videos, or on speakerphone.', 'Volume2', '#8B5CF6', 51, true, false, '["No sound", "Distorted music", "Ringtone not working"]'),
('Microphone Replacement', 'audio', 'Fix for when others cannot hear you clearly during calls or voice recordings.', 'Mic', '#8B5CF6', 52, true, false, '["Caller can''t hear me", "Voice not recording", "Static noise"]'),

-- Body / Housing
('Back Glass Replacement', 'body', 'Premium glass replacement for devices with shattered back panels.', 'Layers', '#6B7280', 60, true, false, '["Broken back glass", "Shattered panel"]'),
('Frame/Housing Replacement', 'body', 'Complete replacement of the device frame if it is bent or heavily scratched.', 'Box', '#6B7280', 61, true, false, '["Bent frame", "Deep scratches", "Structural damage"]'),

-- Software
('OS Installation/Update', 'software', 'Professional software flashing and update to restore device performance or fix bugs.', 'Cpu', '#06B6D4', 70, false, false, '["Phone slow", "App crashes", "Software bugs"]'),
('Phone Unlock', 'software', 'Removal of forgotten pattern, PIN, or password locks (Requires proof of ownership).', 'Lock', '#06B6D4', 71, false, false, '["Forgot pattern", "Phone disabled", "PIN lock"]'),

-- Water Damage
('Water Damage Treatment', 'water_damage', 'Professional ultrasonic cleaning and moisture removal for liquid damaged devices.', 'Droplets', '#34D399', 80, false, false, '["Dropped in water", "Moisture detected", "Corrosion check"]');

-- Verify
SELECT service_type, COUNT(*) as count FROM services GROUP BY service_type ORDER BY count DESC;
