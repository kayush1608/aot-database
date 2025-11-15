-- Bloodlines
insert into Bloodline (name) values
('Ackerman'),
('Fritz'),
('Reiss'),
('Yeager'),
('Braun'),
('Leonhart'),
('Tybur'),
('Braus'),
('Hoover'),
('Galliard'),
('Finger'),
('Grice');

-- Powers
insert into Power (code, definition, power_level) values
('CRD','Coordinate other Titans or control subjects',99),
('HRD','Hardening of the body for defensive/offensive use',28),
('REG','Accelerated regeneration and recovery',75),
('TRN','Ability to transform between Titan and human form',80),
('JMP','Enhanced agility and jumping capability',60),
('STM','Enhanced stamina and endurance',70),
('CRY','Crystallization ability',10),
('BRZ','Berserker-like offensive surge',85),
('SNS','Heightened perception and senses',55);
-- Map bloodlines to powers (some many-to-many examples)
insert into Bloodline_Possesses_Power (bloodline_name, power_code) values
('Fritz','CRD'),
('Reiss','CRD'),
('Yeager','TRN'),
('Ackerman','JMP'),
('Braun','HRD'),
('Leonhart','CRY'),
('Tybur','HRD'),
('Hoover','TRN'),
('Galliard','JMP'),
('Finger','STM'),
('Grice','SNS'),
('Braus','SNS');

-- Titan types
insert into Titan_Type (name, avg_height, threat_level, intelligence_level) values
('Colossal Titan',60.00,19.50,3.00),
('Armored Titan',15.50,17.00,6.00),
('Female Titan',14.00,16.00,10.00),
('Beast Titan',17.25,15.00,12.00),
('Jaw Titan',8.00,13.00,9.00),
('Cart Titan',4.00,8.00,11.00),
('War Hammer Titan',15.00,18.00,14.00),
('Attack Titan',15.00,16.50,8.00),
('Pure Titan',10.00,5.00,2.00),
('Abnormal Titan',12.50,9.00,6.00);

-- Titan powers mapping
insert into Titan_Has_Power (titan_name, power_code) values
('Colossal Titan','HRD'),
('Armored Titan','HRD'),
('Female Titan','REG'),
('Beast Titan','CRD'),
('Jaw Titan','JMP'),
('Cart Titan','STM'),
('War Hammer Titan','CRY'),
('Attack Titan','TRN'),
('Pure Titan','STM'),
('Abnormal Titan','JMP');

-- Districts
insert into District (name, wall, population) values
('Shiganshina','Maria',12000),
('Trost','Rose',30000),
('Mitras','Sina',45000),
('Stohess','Sina',35000),
('Karanes','Rose',28000),
('Chlorba','Maria',8000),
('Utopia','Rose',15000),
('Krolva','Rose',12000),
('Orvud','Sina',10000),
('Dauper','Maria',6000),
('Ehrmich','Rose',9000);

-- Equipment
insert into Equipment (model, type, quantity, desired_quantity, equipment_condition) values
('ODM-Standard','Maneuver',120,200,'Working'),
('Cannon-Field','Cannon',12,20,'Due_for_repairs'),
('Survey-Drone','Recon',8,10,'Working'),
('ODM-Advanced','Maneuver',45,100,'Working'),
('Thunder-Spear','Weapon',200,300,'Working'),
('Flare-Gun','Signal',80,100,'Working'),
('Blade-Set-A','Weapon',500,800,'Broken'),
('ODM-MkII','Maneuver',30,120,'Working'),
('Barricade-Kit','Fortification',25,60,'Working'),
('Medical-Kit','Aid',400,700,'Working'),
('Rifle-Standard','Weapon',150,250,'Due_for_repairs'),
('Reinforced-Blade','Weapon',320,600,'Working'),
('Grapple-Hook','Utility',210,350,'Working'),
('Signal-Smoke','Signal',140,220,'Working'),
('Portable-Shield','Defense',60,120,'Due_for_repairs');

-- Missions
