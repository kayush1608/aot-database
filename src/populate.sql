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
insert into Mission (name, date, time, objective, status) values
('Operation_Reclaim','2025-03-10','06:00:00','Reclaim Shiganshina outer perimeter','Success'),
('Trost_Defense','2024-11-07','03:30:00','Defend Trost district from titan incursion','Active'),
('Wall_Repair','2024-10-15','08:00:00','Repair breach in Wall Maria','Success'),
('Scout_Expedition_57','2024-09-20','05:00:00','Long-range reconnaissance beyond walls','Failure'),
('Stohess_Capture','2024-12-01','14:30:00','Capture rogue shifter in Stohess','Success'),
('Utopia_Evacuation','2025-04-06','09:00:00','Evacuate civilians from Utopia','Success'),
('Krolva_Sweep','2025-05-01','07:30:00','Sweep Krolva farmlands for Abnormals','Active'),
('Orvud_Defense','2024-08-12','12:00:00','Defend Orvud district from Beast Titan','Failure'),
('Wall_Rose_Patrol','2025-02-05','06:15:00','Routine patrol along Wall Rose','Active'),
('Maria_Resupply','2024-11-15','16:00:00','Resupply forward outposts near Wall Maria','Dropped'),
('Dauper_Relief','2025-06-10','13:00:00','Deliver aid to Dauper village','Success'),
('Mitras_Security_Sweep','2025-01-12','10:00:00','Security sweep operations within Mitras','Active'),
('Shiganshina_Rebuild','2025-04-20','08:30:00','Rebuild defenses and infrastructure in Shiganshina','Active'),
('Founding_Intel_Raid','2025-03-02','22:15:00','Recover intelligence related to Founding Titan','Dropped');

-- Mission locations
insert into Mission_Occurs_In_District (mission_name, district_name) values
('Operation_Reclaim','Shiganshina'),
('Trost_Defense','Trost'),
('Wall_Repair','Shiganshina'),
('Scout_Expedition_57','Karanes'),
('Stohess_Capture','Stohess'),
('Utopia_Evacuation','Utopia'),
('Krolva_Sweep','Krolva'),
('Orvud_Defense','Orvud'),
('Wall_Rose_Patrol','Karanes'),
('Maria_Resupply','Shiganshina'),
('Dauper_Relief','Dauper'),
('Mitras_Security_Sweep','Mitras'),
('Shiganshina_Rebuild','Shiganshina'),
('Founding_Intel_Raid','Stohess');

-- Soldiers
insert into Soldier (id, firstname, lastname, dob, soldier_rank, regiment, status, enlistment_date, bloodline_name, shifter, current_state) values
('S0001','Levi','Ackerman','1988-12-25','Captain','Scout','Active','2006-05-01','Ackerman',0,'Soldier'),
('S0002','Armin','Arlert','1995-09-15','Soldier','Scout','Active','2013-04-10','Fritz',0,'Soldier'),
('S0003','Mikasa','Ackerman','1992-02-10','Soldier','Scout','Active','2010-08-12','Ackerman',0,'Soldier'),
('S0004','Hange','Zoë','1985-07-02','Commander','Researcher','Active','2005-01-20','Reiss',0,'Soldier'),
('S0005','Nile','Dok','1986-06-30','Soldier','MP','Active','2007-11-11','Yeager',0,'Soldier'),
('S0006','Eren','Yeager','1994-03-30','Squad_leader','Scout','Deceased','2012-09-09','Yeager',1,'Titan'),
('S0007','Jean','Kirstein','1995-04-07','Squad_leader','Scout','Active','2013-04-10','Fritz',0,'Soldier'),
('S0008','Connie','Springer','1995-05-02','Soldier','Scout','Active','2013-04-10','Braun',0,'Soldier'),
('S0009','Sasha','Blouse','1995-07-26','Soldier','Scout','Deceased','2013-04-10','Leonhart',0,'Soldier'),
('S0010','Erwin','Smith','1981-10-14','Commander','Scout','Deceased','2003-06-01','Reiss',0,'Soldier'),
('S0011','Marco','Bott','1995-06-16','Cadet','Garrison','Deceased','2013-04-10','Tybur',0,'Soldier'),
('S0012','Annie','Leonhart','1996-03-22','Soldier','MP','MIA','2013-04-10','Leonhart',1,'Soldier'),
('S0013','Reiner','Braun','1993-08-01','Soldier','Scout','MIA','2013-04-10','Braun',1,'Soldier'),
('S0014','Dot','Pixis','1970-01-15','General','Garrison','Active','1990-03-01','Fritz',0,'Soldier'),
('S0015','Bertolt','Hoover','1993-12-30','Soldier','Scout','MIA','2011-04-10','Hoover',1,'Titan'),
('S0016','Porco','Galliard','1995-11-21','Soldier','Scout','MIA','2013-04-10','Galliard',1,'Soldier'),
('S0017','Pieck','Finger','1996-08-05','Soldier','MP','Active','2014-06-01','Finger',1,'Soldier'),
('S0018','Falco','Grice','1999-02-10','Cadet','Scout','Active','2020-07-01','Grice',0,'Soldier'),
('S0019','Historia','Reiss','1996-01-15','Commander','Researcher','Active','2012-01-01','Reiss',0,'Soldier'),
('S0020','Hannes',null,'1975-06-05','Captain','Garrison','Deceased','1993-03-01','Fritz',0,'Soldier'),
('S0021','Ymir',null,'1990-08-17','Soldier','Scout','MIA','2008-04-01','Fritz',1,'Soldier'),
('S0022','Petra','Rall','1990-12-06','Soldier','Scout','Deceased','2008-04-01','Braus',0,'Soldier'),
('S0023','Mike','Zacharias','1981-11-01','Captain','Scout','Deceased','2000-03-01','Fritz',0,'Soldier'),
('S0024','Rico','Brzenska','1987-06-19','Squad_leader','Garrison','Active','2007-11-11','Tybur',0,'Soldier'),
('S0025','Nifa',null,'1992-04-14','Soldier','Scout','Deceased','2010-05-01','Fritz',0,'Soldier'),
('S0026','Oruo','Bozad','1988-07-03','Soldier','Scout','Deceased','2006-04-01','Fritz',0,'Soldier'),
('S0027','Eld','Jinn','1987-01-09','Soldier','Scout','Deceased','2005-06-01','Fritz',0,'Soldier'),
('S0028','Gunther','Schulz','1988-03-22','Soldier','Scout','Deceased','2006-04-01','Fritz',0,'Soldier'),
('S0029','Nanaba',null,'1984-09-27','Squad_leader','Scout','Deceased','2003-05-01','Fritz',0,'Soldier'),
('S0030','Gelgar',null,'1985-11-18','Soldier','Scout','Deceased','2004-03-01','Fritz',0,'Soldier'),
('S0031','Moblit','Berner','1986-12-02','Soldier','Researcher','Deceased','2004-11-01','Reiss',0,'Soldier'),
('S0032','Marlo','Freudenberg','1996-02-07','Soldier','MP','Active','2014-04-01','Tybur',0,'Soldier'),
('S0033','Hitch','Dreyse','1996-05-05','Soldier','MP','Active','2014-04-01','Tybur',0,'Soldier'),
('S0034','Keiji',null,'1992-10-11','Soldier','Scout','Deceased','2010-05-01','Fritz',0,'Soldier');

-- Specialized soldier tables
insert into Scout_Soldier (soldier_id, specialty_terrain, expeditions_count) values
('S0001','Urban',50),
('S0002','Forest',12),
('S0003','Mountain',30),
('S0006','Plains',8),
('S0007','Urban',15),
('S0008','Forest',11),
('S0009','Plains',14),
('S0010','All-terrain',67),
('S0015','Urban',7),
('S0016','Forest',5),
('S0018','Plains',2),
('S0021','Mountain',9),
('S0022','Urban',12),
('S0023','Forest',41),
('S0025','Urban',6),
('S0026','Forest',18),
('S0027','Urban',22),
('S0028','Forest',15),
('S0029','Mountain',28),
('S0030','Plains',19),
('S0034','Plains',7);

insert into Garrison_Soldier (soldier_id, district_name, defense_rating) values
('S0004','Mitras',4.25),
('S0011','Trost',3.50),
('S0014','Trost',5.00),
('S0020','Trost',3.80),
('S0024','Orvud',4.10);

insert into Military_Police_Soldier (soldier_id, clearance_level) values
('S0005',4.50),
('S0012',3.75),
('S0017',4.20),
('S0032',3.60),
('S0033',3.40);

insert into MP_Patrol_Zones (soldier_id, district_name) values
('S0005','Mitras'),
('S0005','Stohess'),
('S0012','Stohess'),
('S0012','Mitras'),
('S0017','Mitras'),
('S0017','Stohess'),
('S0032','Mitras'),
('S0033','Stohess');

-- Equipment maintenance records
insert into Equipment_Maintenance (equipment_model, maintenance_date, maintenance_time, maintainer_id, remarks) values
('ODM-Standard','2025-01-12','09:30:00','S0004','Routine lubrication and blade inspection'),
('Cannon-Field','2025-02-02','14:00:00','S0004','Barrel alignment and parts replacement'),
('Thunder-Spear','2025-01-20','10:00:00','S0004','Trigger mechanism repair'),
('ODM-Advanced','2025-02-10','11:15:00','S0004','Gas cylinder replacement'),
('Blade-Set-A','2025-02-15','13:45:00','S0004','Sharpening and quality check'),
('ODM-MkII','2025-03-01','10:30:00','S0001','Gas regulator calibration'),
('Rifle-Standard','2025-03-03','15:10:00','S0014','Barrel cleaning and spring check'),
('Medical-Kit','2025-03-05','09:05:00','S0024','Inventory restock and sterilization'),
('Reinforced-Blade','2025-03-12','12:20:00','S0004','Edge tempering and balance check'),
('Grapple-Hook','2025-03-14','09:50:00','S0024','Cable inspection and hook replacement'),
('Portable-Shield','2025-03-16','16:40:00','S0014','Hinge reinforcement and strap repair');

-- Casualty
insert into Casualty (soldier_id, mission_name, titan_type_name, cause_of_death, district_name, date, time) values
('S0006','Operation_Reclaim','Colossal Titan','Kinetic trauma and absorption','Shiganshina','2025-03-10','06:45:00'),
('S0009','Scout_Expedition_57','Jaw Titan','Bite wound','Karanes','2024-09-20','07:15:00'),
('S0010','Operation_Reclaim','Beast Titan','Projectile impact','Shiganshina','2025-03-10','08:30:00'),
('S0011','Trost_Defense','Female Titan','Crushing injury','Trost','2024-11-07','04:20:00'),
('S0020','Trost_Defense','Pure Titan','Overpowered while protecting civilians','Trost','2024-11-07','04:35:00'),
('S0023','Orvud_Defense','Beast Titan','Crushed during engagement','Orvud','2024-08-12','12:40:00'),
('S0026','Scout_Expedition_57','Female Titan','Crushed during pursuit','Karanes','2024-09-20','07:40:00'),
('S0027','Scout_Expedition_57','Female Titan','Killed in engagement','Karanes','2024-09-20','07:42:00'),
('S0028','Scout_Expedition_57','Female Titan','Impaled during charge','Karanes','2024-09-20','07:44:00'),
('S0029','Orvud_Defense','Beast Titan','Overrun defending tower','Orvud','2024-08-12','12:50:00'),
('S0030','Orvud_Defense','Beast Titan','Fell during retreat','Orvud','2024-08-12','12:55:00'),
('S0031','Operation_Reclaim','Beast Titan','Sacrificed while covering retreat','Shiganshina','2025-03-10','08:10:00'),
('S0034','Stohess_Capture','Female Titan','Crushed amidst urban clash','Stohess','2024-12-01','15:05:00');

-- Sightings
insert into Sighting (id, reported_by, mission_name, district_name, sighting_date, sighting_time) values
('SG001','S0002','Operation_Reclaim','Shiganshina','2025-03-09','22:10:00'),
('SG002','S0003','Trost_Defense','Trost','2024-11-06','02:45:00'),
('SG003','S0007','Scout_Expedition_57','Karanes','2024-09-20','06:30:00'),
('SG004','S0001','Stohess_Capture','Stohess','2024-12-01','14:00:00'),
('SG005','S0008','Wall_Repair','Shiganshina','2024-10-15','09:20:00'),
('SG006','S0018','Wall_Rose_Patrol','Karanes','2025-02-05','06:45:00'),
('SG007','S0017','Utopia_Evacuation','Utopia','2025-04-06','08:30:00'),
('SG008','S0007','Krolva_Sweep','Krolva','2025-05-01','07:10:00'),
('SG009','S0002','Maria_Resupply','Shiganshina','2024-11-15','15:20:00'),
('SG010','S0008','Orvud_Defense','Orvud','2024-08-12','11:45:00'),
('SG011','S0025','Shiganshina_Rebuild','Shiganshina','2025-04-20','08:45:00'),
('SG012','S0032','Mitras_Security_Sweep','Mitras','2025-01-12','10:20:00'),
('SG013','S0033','Mitras_Security_Sweep','Mitras','2025-01-12','10:40:00'),
('SG014','S0029','Orvud_Defense','Orvud','2024-08-12','11:20:00'),
('SG015','S0002','Dauper_Relief','Dauper','2025-06-10','12:30:00'),
('SG016','S0010','Founding_Intel_Raid','Stohess','2025-03-02','22:05:00');

insert into Sighting_Titan_Type (sighting_id, titan_type_name, number_of_titans) values
('SG001','Colossal Titan',1),
('SG002','Female Titan',2),
('SG003','Jaw Titan',3),
('SG003','Beast Titan',1),
('SG004','Female Titan',1),
('SG005','Armored Titan',1),
('SG005','Attack Titan',1),
('SG006','Abnormal Titan',1),
('SG007','Pure Titan',3),
('SG008','Abnormal Titan',2),
('SG009','Armored Titan',1),
('SG010','Beast Titan',1),
('SG011','Abnormal Titan',1),
('SG012','Pure Titan',2),
('SG013','Pure Titan',1),
('SG014','Beast Titan',1),
('SG015','Pure Titan',3),
('SG016','Female Titan',1);

-- Deployments
insert into Deployment (soldier_id, equipment_model, mission_name, location, deployment_date, deployment_time, role_assigned) values
('S0001','ODM-Standard','Operation_Reclaim','Shiganshina','2025-03-10','05:30:00','Lead assault'),
('S0002','ODM-Standard','Operation_Reclaim','Shiganshina','2025-03-10','05:45:00','Support'),
('S0005','Cannon-Field','Trost_Defense','Trost','2024-11-07','03:00:00','Artillery support'),
('S0003','ODM-Advanced','Operation_Reclaim','Shiganshina','2025-03-10','05:30:00','Assault team'),
('S0007','Thunder-Spear','Stohess_Capture','Stohess','2024-12-01','14:15:00','Anti-titan specialist'),
('S0008','ODM-Standard','Scout_Expedition_57','Karanes','2024-09-20','04:45:00','Scout'),
('S0010','ODM-Advanced','Operation_Reclaim','Shiganshina','2025-03-10','05:30:00','Commander'),
('S0014','Cannon-Field','Trost_Defense','Trost','2024-11-07','03:00:00','Defense coordinator'),
('S0015','ODM-MkII','Wall_Rose_Patrol','Karanes','2025-02-05','06:00:00','Scout'),
('S0017','Rifle-Standard','Utopia_Evacuation','Utopia','2025-04-06','08:00:00','Rear guard'),
('S0024','Cannon-Field','Orvud_Defense','Orvud','2024-08-12','11:30:00','Artillery coordinator'),
('S0016','Thunder-Spear','Krolva_Sweep','Krolva','2025-05-01','07:05:00','Anti-titan support'),
('S0022','ODM-Standard','Wall_Rose_Patrol','Karanes','2025-02-05','06:10:00','Escort'),
('S0025','ODM-Advanced','Shiganshina_Rebuild','Shiganshina','2025-04-20','08:15:00','Perimeter scout'),
('S0032','Rifle-Standard','Mitras_Security_Sweep','Mitras','2025-01-12','09:55:00','Checkpoint guard'),
('S0033','Rifle-Standard','Mitras_Security_Sweep','Mitras','2025-01-12','09:57:00','Patrol'),
('S0029','ODM-Standard','Orvud_Defense','Orvud','2024-08-12','11:00:00','Tower defense'),
('S0030','ODM-Standard','Orvud_Defense','Orvud','2024-08-12','11:02:00','Tower defense'),
('S0031','ODM-Advanced','Operation_Reclaim','Shiganshina','2025-03-10','05:40:00','Research support'),
('S0026','Reinforced-Blade','Scout_Expedition_57','Karanes','2024-09-20','04:40:00','Assault team'),
('S0027','Reinforced-Blade','Scout_Expedition_57','Karanes','2024-09-20','04:41:00','Assault team'),
('S0028','Reinforced-Blade','Scout_Expedition_57','Karanes','2024-09-20','04:42:00','Assault team'),
('S0025','Signal-Smoke','Dauper_Relief','Dauper','2025-06-10','12:50:00','Signal coordination');


-- End of seed file
