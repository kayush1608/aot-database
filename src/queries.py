import datetime

def get_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        rows = cursor.fetchall()
        tables = [list(r.values())[0] for r in rows]
    return tables

def get_columns(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(f"show columns from `{table}`")
        return cursor.fetchall()

def fetch_all(connection, table, limit=None):
    with connection.cursor() as cursor:
        q = f"select * from `{table}`"
        if limit:
            q += f" limit {int(limit)}"
        cursor.execute(q)
        return cursor.fetchall()

def insert_record(connection, table, data):
    cols = ", ".join(f"`{c}`" for c in data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = [None if v == "" else v for v in data.values()]
    q = f"insert into `{table}` ({cols}) values ({placeholders})"
    with connection.cursor() as cursor:
        cursor.execute(q, values)
    connection.commit()

def update_record(connection, table, data, pk):
    set_clause = ", ".join(f"`{k}` = %s" for k in data.keys())
    where_clause = " and ".join(f"`{k}` = %s" for k in pk.keys())
    values = [None if v == "" else v for v in data.values()] + list(pk.values())
    q = f"update `{table}` set {set_clause} where {where_clause}"
    with connection.cursor() as cursor:
        cursor.execute(q, values)
    connection.commit()

def delete_record(connection, table, pk):
    where_clause = " and ".join(f"`{k}` = %s" for k in pk.keys())
    q = f"delete from `{table}` where {where_clause}"
    with connection.cursor() as cursor:
        cursor.execute(q, list(pk.values()))
    connection.commit()

def get_primary_keys(columns):
    return [col['Field'] for col in columns if col.get('Key') == 'PRI']

def get_threat_report(connection):
    query = """
        select 
            d.name as District,
            d.wall as Wall,
            coalesce(sum(stt.number_of_titans), 0) as Total_Titan_Sightings,
            count(distinct c.soldier_id) as Soldier_Casualties
        from District d
        left join Sighting s on d.name = s.district_name
        left join Sighting_Titan_Type stt on s.id = stt.sighting_id
        left join Casualty c on d.name = c.district_name
        group by d.name, d.wall
        order by Total_Titan_Sightings desc, Soldier_Casualties desc
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def get_commander_performance(connection):
    query = """
        select 
            s.id as Commander_ID,
            concat(s.firstname, ' ', coalesce(s.lastname, '')) as Commander_Name,
            s.soldier_rank as `Rank`,
            s.regiment as Regiment,
            count(d.mission_name) as Missions_Led,
            count(c.soldier_id) as Total_Casualties,
            group_concat(d.mission_name order by d.mission_name separator ', ') as Mission_Names
        from Soldier s
        join Deployment d on s.id = d.soldier_id
        left join Casualty c on d.mission_name = c.mission_name
        where s.soldier_rank in ('Commander', 'Captain', 'General', 'Squad_leader')
            and (d.role_assigned like '%Commander%' or d.role_assigned like '%Leader%')
        group by s.id, s.firstname, s.lastname, s.soldier_rank, s.regiment
        order by Missions_Led desc, Total_Casualties desc
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def get_latest_mission_casualties(connection):
    query = """
        select 
            s.id as Soldier_ID,
            concat(s.firstname, ' ', coalesce(s.lastname, '')) as Soldier_Name,
            s.soldier_rank as `Rank`,
            s.regiment as Regiment,
            timestampdiff(year, s.dob, c.date) as Age_at_Death,
            c.mission_name as Mission,
            c.titan_type_name as Killed_By_Titan_Type,
            c.cause_of_death as Cause_of_Death,
            c.district_name as District,
            c.date as Date_of_Death,
            c.time as Time_of_Death,
            timestampdiff(year, s.enlistment_date, c.date) as Years_of_Service
        from Casualty c
        join Soldier s on c.soldier_id = s.id
        where c.mission_name = (
            select c2.mission_name 
            from Casualty c2 
            order by c2.date desc, c2.time desc 
            limit 1
        )
        order by s.soldier_rank, Age_at_Death
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

# Preset Query Functions
def get_active_scout_soldiers(connection, regiment='Scout', status='Active'):
    query = "select * from Soldier where regiment = %s and status = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (regiment, status))
        return cursor.fetchall()

def get_success_missions(connection, status='Success'):
    query = "select name, objective from Mission where status = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (status,))
        return cursor.fetchall()

def get_average_casualties_per_mission(connection):
    query = """
        select avg(casualty_count) as Average_Casualties_Per_Mission 
        from (
            select count(*) as casualty_count 
            from Casualty 
            group by mission_name
        ) as mission_casualties
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def get_recovery_missions(connection, keyword='recover'):
    query = "select * from Mission where objective like %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (f'%{keyword}%',))
        return cursor.fetchall()

# Modification Operation Functions
def add_new_soldier(connection, soldier_data):
    if soldier_data.get('dob') and soldier_data['dob'] > (datetime.date.today() - datetime.timedelta(days=21*365)):
        raise ValueError("Soldier must be at least 21 years old.")
    query = "select 1 from Bloodline where name = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (soldier_data.get('bloodline', {}).get('name'),))
        exists = cursor.fetchone()
    if not exists:
        insert_record(connection, 'Bloodline', {'name': soldier_data.get('bloodline_name', {})})
    insert_record(connection, 'Soldier', soldier_data)

def update_soldier_rank(connection, soldier_id, new_rank):
    pk = {'id': soldier_id}
    data = {'soldier_rank': new_rank}
    update_record(connection, 'Soldier', data, pk)

def delete_equipment_type(connection, equipment_model):
    pk = {'model': equipment_model}
    delete_record(connection, 'Equipment', pk)