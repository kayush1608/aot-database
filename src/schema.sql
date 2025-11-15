create database if not exists attack_on_titan_db;
use attack_on_titan_db;

create table if not exists Bloodline (
    name varchar(127) primary key
);

create table if not exists Power (
    code varchar(5),
    definition text not null,
    power_level integer not null check (power_level between 0 and 100),
    primary key (code)
);

create table if not exists Bloodline_Possesses_Power (
    bloodline_name varchar(127),
    power_code varchar(5),
    primary key (bloodline_name, power_code),
    foreign key (bloodline_name) references Bloodline(name) on delete cascade on update cascade,
    foreign key (power_code) references Power(code) on delete cascade on update cascade
);

create table if not exists Titan_Type (
    name varchar(127) primary key,
    avg_height decimal(8,2) not null check (avg_height > 0),
    threat_level decimal(4,2) check (threat_level between 0 and 20),
    intelligence_level decimal(4,2) check (intelligence_level between 0 and 20)
);

create table if not exists Titan_Has_Power (
    titan_name varchar(127),
    power_code varchar(5),
    primary key (titan_name, power_code),
    foreign key (titan_name) references Titan_Type(name) on delete cascade on update cascade,
    foreign key (power_code) references Power(code) on delete cascade on update cascade
);

create table if not exists District (
    name varchar(127),
    wall enum('Rose', 'Maria', 'Sina') not null,
    population integer check (population >= 0),
    primary key (name)
);

create table if not exists Equipment (
    model varchar(127) primary key,
    type varchar(127) not null,
    quantity integer not null default 0 check (quantity >= 0),
    desired_quantity integer not null default 0 check (desired_quantity >= 0),
    equipment_condition enum('Working', 'Broken', 'Due_for_repairs') not null default 'Working'
);

create table if not exists Mission (
    name varchar(127) primary key,
    date date,
    time time,
    objective text not null,
    status enum('Planning', 'Active', 'Success', 'Failure', 'Dropped')
);

create table if not exists Mission_Occurs_In_District (
    mission_name varchar(127),
    district_name varchar(127),
    primary key (mission_name, district_name),
    foreign key (mission_name) references Mission(name) on delete cascade on update cascade,
    foreign key (district_name) references District(name) on delete cascade on update cascade
);

create table if not exists Soldier (
    id varchar(10) primary key,
    firstname varchar(127) not null,
    lastname varchar(127),
    dob date,
    soldier_rank enum('Cadet', 'Soldier', 'Squad_leader', 'Commander', 'Captain', 'General') not null default 'Cadet',
    regiment enum('Scout', 'Garrison', 'MP', 'Researcher') not null,
    status enum('Active', 'Deceased', 'MIA') not null default 'Active',
    enlistment_date date not null default (current_date),
    bloodline_name varchar(127) not null,
    shifter boolean not null default false,
    current_state enum('Soldier', 'Titan') not null default 'Soldier',
    foreign key (bloodline_name) references Bloodline(name) on delete restrict on update cascade
);

create table if not exists Scout_Soldier (
    soldier_id varchar(10) primary key,
    specialty_terrain varchar(127) not null,
    expeditions_count integer not null default 0,
    foreign key (soldier_id) references Soldier(id) on delete cascade on update cascade
);

create table if not exists Garrison_Soldier (
    soldier_id varchar(10) primary key,
    district_name varchar(127) not null,
    defense_rating decimal(3,2) check (defense_rating between 0 and 5),
    foreign key (soldier_id) references Soldier(id) on delete cascade on update cascade,
    foreign key (district_name) references District(name) on delete restrict on update cascade
);

create table if not exists Military_Police_Soldier (
    soldier_id varchar(10) primary key,
    clearance_level decimal(3,2) check (clearance_level between 0 and 5),
    foreign key (soldier_id) references Soldier(id) on delete cascade on update cascade
);

create table if not exists MP_Patrol_Zones (
    soldier_id varchar(10),
    district_name varchar(127),
    primary key (soldier_id, district_name),
    foreign key (soldier_id) references Military_Police_Soldier(soldier_id) on delete cascade on update cascade,
    foreign key (district_name) references District(name) on delete cascade on update cascade
);

create table if not exists Equipment_Maintenance (
    equipment_model varchar(127),
    maintenance_date date,
    maintenance_time time not null,
    maintainer_id varchar(10),
    remarks text,
    primary key (equipment_model, maintenance_date, maintenance_time),
    foreign key (equipment_model) references Equipment(model) on delete cascade on update cascade,
    foreign key (maintainer_id) references Soldier(id) on delete set null on update cascade
);

create table if not exists Casualty (
    soldier_id varchar(10) primary key,
    mission_name varchar(127) not null,
    titan_type_name varchar(127),
    cause_of_death text,
    district_name varchar(127) not null,
    date date not null,
    time time not null,
    foreign key (soldier_id) references Soldier(id) on delete cascade on update cascade,
    foreign key (mission_name) references Mission(name) on delete restrict on update cascade,
    foreign key (titan_type_name) references Titan_Type(name) on delete restrict on update cascade,
    foreign key (district_name) references District(name) on delete restrict on update cascade
);

create table if not exists Sighting (
    id varchar(10) primary key,
    reported_by varchar(10),
    mission_name varchar(127),
    district_name varchar(127),
    sighting_date date not null,
    sighting_time time not null,
    foreign key (reported_by) references Soldier(id) on delete set null on update cascade,
    foreign key (mission_name) references Mission(name) on delete set null on update cascade,
    foreign key (district_name) references District(name) on delete set null on update cascade
);

create table if not exists Sighting_Titan_Type (
    sighting_id varchar(10),
    titan_type_name varchar(127),
    number_of_titans integer not null default 0 check (number_of_titans >= 0),
    primary key (sighting_id, titan_type_name),
    foreign key (sighting_id) references Sighting(id) on delete cascade on update cascade,
    foreign key (titan_type_name) references Titan_Type(name) on delete restrict on update cascade
);

create table if not exists Deployment (
    soldier_id varchar(10),
    equipment_model varchar(127),
    mission_name varchar(127) not null,
    location varchar(127) not null,
    deployment_date date not null,
    deployment_time time not null,
    role_assigned varchar(127) not null,
    primary key (soldier_id, equipment_model, mission_name, location),
    foreign key (soldier_id) references Soldier(id) on delete restrict on update cascade,
    foreign key (equipment_model) references Equipment(model) on delete restrict on update cascade,
    foreign key (mission_name) references Mission(name) on delete restrict on update cascade,
    foreign key (location) references District(name) on delete restrict on update cascade
);