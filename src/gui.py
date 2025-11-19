import datetime
import streamlit as st
import pandas as pd
from sql import create, initialize, reinitialize, populate, check_database_exists
import traceback
import time
from queries import (get_tables, get_columns, fetch_all, insert_record, 
                     update_record, delete_record, get_primary_keys,
                     get_threat_report, get_commander_performance, get_latest_mission_casualties,
                     get_active_scout_soldiers, get_success_missions, 
                     get_average_casualties_per_mission, get_recovery_missions,
                     add_new_soldier, update_soldier_rank, delete_equipment_type)

st.set_page_config(
    page_title="Attack on Titans",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def sidebar():
    """Render database initialization and population controls in sidebar."""
    st.sidebar.header("Test Database")
    db_exists = check_database_exists()

    if db_exists:
        if st.sidebar.button("Re-initialize Database"):
            try:
                reinitialize()
                st.sidebar.success("Database re-initialized successfully.")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Re-initialization failed: {e}")
                st.sidebar.write(traceback.format_exc())
    else:
        if st.sidebar.button("Initialize Database"):
            try:
                initialize()
                st.sidebar.success("Database initialized successfully.")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Initialization failed: {e}")
                st.sidebar.write(traceback.format_exc())

    if st.sidebar.button("Populate sample data"):
        try:
            populate()
            st.sidebar.success("Data populated successfully.")
        except Exception as e:
            st.sidebar.error(f"Populate failed: {e}")

def view(connection, tables):
    """Render the View Records section for browsing and editing table data."""
    st.sidebar.header("Tables")
    selected_table = st.sidebar.selectbox(
        "Select a table",
        options=tables,
        index=tables.index(st.session_state.selected_table) if st.session_state.selected_table in tables else 0,
        key="table_selector"
    )
    
    if st.sidebar.button("Reload Tables", width='stretch'):
        st.rerun()
    
    if selected_table != st.session_state.selected_table:
        st.session_state.selected_table = selected_table
        if 'action_mode' in st.session_state:
            del st.session_state.action_mode
        st.rerun()
    
    if st.session_state.selected_table:
        table = st.session_state.selected_table

        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(f"{table}")
        with col2:
            if st.button("Add Record", width='stretch'):
                st.session_state.action_mode = "add"
                st.rerun()
        
        action_mode = st.session_state.get('action_mode', 'view')
        
        if action_mode == "add":
            add(connection, table)
        elif action_mode == "edit":
            edit(connection, table)
        elif action_mode == "delete":
            delete(connection, table)
        else:
            view_table(connection, table)

def add(connection, table):
    """Render form for adding a new record to a table."""
    st.divider()
    columns = get_columns(connection, table)
    st.subheader(f"Add a new record to `{table}`")
    with st.form("add_form"):
        record = {}
        for col in columns:
            name = col['Field']
            record[name] = st.text_input(name)
        col1, col2 = st.columns([1, 4])
        with col1:
            submitted = st.form_submit_button("Insert")
        with col2:
            cancel = st.form_submit_button("Cancel")
        
        if submitted:
            try:
                insert_record(connection, table, record)
                st.success("Record inserted successfully.")
                st.session_state.action_mode = "view"
                st.rerun()
            except Exception as e:
                st.error(f"Insert failed: {e}")
                st.write(traceback.format_exc())
        
        if cancel:
            st.session_state.action_mode = "view"
            st.rerun()

def edit(connection, table):
    """Render form for editing an existing record."""
    st.divider()
    columns = get_columns(connection, table)
    pk_fields = get_primary_keys(columns)
    if not pk_fields:
        st.warning("This table has no primary key defined; edit operations are not supported.")
        if st.button("Back to View"):
            st.session_state.action_mode = "view"
            st.rerun()
    else:
        if 'selected_row' in st.session_state:
            selected = st.session_state.selected_row
        else:
            rows = fetch_all(connection, table)
            if not rows:
                st.info("No records to edit in this table.")
                if st.button("Back to View"):
                    st.session_state.action_mode = "view"
                    st.rerun()
                return
            
            def row_label(r):
                return " | ".join(str(r[k]) for k in pk_fields)

            pk_to_row = {row_label(r): r for r in rows}
            choice = st.selectbox("Select record (by primary key)", options=list(pk_to_row.keys()))
            selected = pk_to_row[choice]

        st.write("Selected record:")
        st.json(selected)

        editable_fields = [c['Field'] for c in columns if c['Field'] not in pk_fields]
        with st.form("edit_form"):
            new_values = {}
            for f in editable_fields:
                new_values[f] = st.text_input(f, value=str(selected.get(f, "")))
            col1, col2 = st.columns([1, 4])
            with col1:
                update = st.form_submit_button("Update")
            with col2:
                cancel = st.form_submit_button("Cancel")
        
            if update:
                try:
                    pk = {k: selected[k] for k in pk_fields}
                    update_record(connection, table, new_values, pk)
                    st.success("Record updated successfully.")
                    st.session_state.action_mode = "view"
                    if 'selected_row' in st.session_state:
                        del st.session_state.selected_row
                    st.rerun()
                except Exception as e:
                    st.error(f"Update failed: {e}")
                    st.write(traceback.format_exc())
            
            if cancel:
                st.session_state.action_mode = "view"
                if 'selected_row' in st.session_state:
                    del st.session_state.selected_row
                st.rerun()

def delete(connection, table):
    """Render form for deleting a record."""
    st.divider()
    columns = get_columns(connection, table)
    pk_fields = get_primary_keys(columns)
    if not pk_fields:
        st.warning("This table has no primary key; delete operation is not supported.")
        if st.button("Back to View"):
            st.session_state.action_mode = "view"
            st.rerun()
    else:
        if 'selected_row' in st.session_state:
            selected_for_delete = st.session_state.selected_row
        else:
            rows = fetch_all(connection, table)
            if not rows:
                st.info("No records to delete in this table.")
                if st.button("Back to View"):
                    st.session_state.action_mode = "view"
                    st.rerun()
                return
            
            def row_label(r):
                return " | ".join(str(r[k]) for k in pk_fields)
            
            pk_to_row = {row_label(r): r for r in rows}
            delete_choice = st.selectbox("Select record to delete (by primary key)", options=list(pk_to_row.keys()))
            selected_for_delete = pk_to_row[delete_choice]
        
        st.warning("Are you sure you want to delete this record?")
        st.json(selected_for_delete)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Delete", type="primary"):
                try:
                    pk = {k: selected_for_delete[k] for k in pk_fields}
                    delete_record(connection, table, pk)
                    st.success("Record deleted successfully.")
                    st.session_state.action_mode = "view"
                    if 'selected_row' in st.session_state:
                        del st.session_state.selected_row
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")
                    st.write(traceback.format_exc())
        with col2:
            if st.button("Cancel"):
                st.session_state.action_mode = "view"
                if 'selected_row' in st.session_state:
                    del st.session_state.selected_row
                st.rerun()

def view_table(connection, table):
    """Render the main table view with data and action buttons."""
    st.divider()

    col1, col2 = st.columns([2, 8])
    with col1:
        limit = st.number_input("Limit rows (0 = all)", min_value=0, value=100, key="limit_input")
    
    rows = fetch_all(connection, table, limit=None if limit == 0 else limit)
    if rows:
        columns = get_columns(connection, table)
        pk_fields = get_primary_keys(columns)
        
        if pk_fields:
            df = pd.DataFrame(rows)
            
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
                column_config={
                    col: st.column_config.Column(
                        width="medium"
                    ) for col in df.columns
                }
            )
            
            st.divider()
            st.write("**Actions:**")
            
            def row_label(r):
                return " | ".join(str(r[k]) for k in pk_fields)
            
            pk_to_row = {row_label(r): r for r in rows}
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                selected_row_label = st.selectbox(
                    "Select record (by primary key)",
                    options=list(pk_to_row.keys()),
                    key="action_row_select"
                )
            with col2:
                if st.button("Edit", type="secondary", width='stretch'):
                    st.session_state.selected_row = pk_to_row[selected_row_label]
                    st.session_state.action_mode = "edit"
                    st.rerun()
            with col3:
                if st.button("Delete", type="primary", width='stretch'):
                    st.session_state.selected_row = pk_to_row[selected_row_label]
                    st.session_state.action_mode = "delete"
                    st.rerun()
        else:
            df = pd.DataFrame(rows)
            st.dataframe(df, width='stretch')
            st.info("This table has no primary key; edit/delete operations are not supported.")
    else:
        st.info("No records found in this table.")

def run(connection):
    """Render the custom SQL query section."""
    st.subheader("Run SQL Query")
    
    custom_query = st.text_area(
        "Enter your SQL query", 
        height=200, 
        placeholder="select * from table_name where condition"
    )
    
    if st.button("Execute Query", type="primary", disabled=not custom_query.strip()):
        try:
            with connection.cursor() as cursor:
                cursor.execute(custom_query)
                results = cursor.fetchall()
            
            st.divider()
            st.subheader("Results")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, width='stretch')
                st.success(f"Query returned {len(results)} row(s).")
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            st.write(traceback.format_exc())

def modify(connection):
    """Render the Presets section with preset queries."""
    st.subheader("Preset Queries & Presets")
    st.caption("Common queries and database modifications")
    
    operation = st.selectbox(
        "Select Operation",
        options=[
            "3.1.1 Selection - Active Scout Regiment Soldiers",
            "3.1.2 Projection - Success Mission Names & Objectives",
            "3.1.3 Aggregate - Average Casualties per Mission",
            "3.1.4 Search - Recovery-Related Missions",
            "3.3.a - Add a new soldier to the army",
            "3.3.b - Update the rank of a soldier",
            "3.3.c - Delete an equipment type"
        ]
    )
    
    if "3.1.1" in operation:
        selection_query(connection)
    elif "3.1.2" in operation:
        projection_query(connection)
    elif "3.1.3" in operation:
        aggregate_query(connection)
    elif "3.1.4" in operation:
        search_query(connection)
    elif "3.3.a" in operation:
        add_soldier(connection)
    elif "3.3.b" in operation:
        rank(connection)
    elif "3.3.c" in operation:
        delete_equipment(connection)

def selection_query(connection):
    """Render 3.1.1 selection query with dropdowns."""
    st.divider()
    st.subheader("3.1.1 Selection Query")
    st.caption("Retrieve soldiers by regiment and status")
    
    col1, col2 = st.columns(2)
    with col1:
        regiment = st.selectbox("Regiment", options=["Scout", "Garrison", "MP", "Researcher"])
    with col2:
        status = st.selectbox("Status", options=["Active", "Deceased", "MIA"])
    
    if st.button("Execute Query", type="primary"):
        try:
            st.info(f"**Query:** Retrieve all soldier records where regiment is {regiment} and status is {status}")
            results = get_active_scout_soldiers(connection, regiment, status)
            
            st.divider()
            st.subheader("Results")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, width='stretch', hide_index=True)
                st.success(f"Query returned {len(results)} row(s).")
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            st.write(traceback.format_exc())

def projection_query(connection):
    """Render 3.1.2 projection query with dropdown."""
    st.divider()
    st.subheader("3.1.2 Projection Query")
    st.caption("Display mission names and objectives by status")
    
    mission_status = st.selectbox("Mission Status", options=["Success", "Failure", "Active", "Planning", "Dropped"])
    
    if st.button("Execute Query", type="primary"):
        try:
            st.info(f"**Query:** Display the mission name and objective for all {mission_status} missions")
            results = get_success_missions(connection, mission_status)
            
            st.divider()
            st.subheader("Results")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, width='stretch', hide_index=True)
                st.success(f"Query returned {len(results)} row(s).")
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            st.write(traceback.format_exc())

def aggregate_query(connection):
    """Render 3.1.3 aggregate query."""
    st.divider()
    st.subheader("3.1.3 Aggregate Query")
    st.caption("Calculate the average number of casualties per mission")
    
    if st.button("Execute Query", type="primary"):
        try:
            st.info("**Query:** Calculate the average number of casualties per mission")
            results = get_average_casualties_per_mission(connection)
            
            st.divider()
            st.subheader("Results")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, width='stretch', hide_index=True)
                st.success(f"Query returned {len(results)} row(s).")
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            st.write(traceback.format_exc())

def search_query(connection):
    """Render 3.1.4 search query with keyword input."""
    st.divider()
    st.subheader("3.1.4 Search Query")
    st.caption("Find missions by keyword in objective")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("Search Keyword", value="recover", placeholder="Enter keyword to search in mission objectives")
    with col2:
        st.write("")
        st.caption("*Try: recover, reclaim, rescue, defend, etc.*")
    
    if st.button("Execute Query", type="primary"):
        try:
            st.info(f"**Query:** Find missions where the objective contains '{keyword}'")
            results = get_recovery_missions(connection, keyword)
            
            st.divider()
            st.subheader("Results")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, width='stretch', hide_index=True)
                st.success(f"Query returned {len(results)} row(s).")
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            st.write(traceback.format_exc())

def add_soldier(connection):
    """Render form for adding a new soldier."""
    st.divider()
    st.subheader("Add New Soldier")
    
    with st.form("add_soldier"):
        col1, col2 = st.columns(2)
        with col1:
            soldier_id = st.text_input("Soldier ID*", placeholder="e.g., S001")
            firstname = st.text_input("First Name*", placeholder="e.g., Eren")
            lastname = st.text_input("Last Name", placeholder="e.g., Yeager")
            dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today().replace(year=datetime.date.today().year - 21))
            regiment = st.selectbox("Regiment*", options=["Scout", "Garrison", "MP", "Researcher"])
        with col2:
            rank = st.selectbox("Rank*", options=["Cadet", "Soldier", "Squad_leader", "Commander", "Captain", "General"])
            status = st.selectbox("Status*", options=["Active", "Deceased", "MIA"])
            enlistment_date = st.date_input("Enlistment Date")
            bloodline_name = st.text_input("Bloodline Name*", placeholder="e.g., Eldian(It will auto add Bloodline record if not exists)")
            shifter = st.checkbox("Titan Shifter")
        
        submitted = st.form_submit_button("Add Soldier", type="primary")
        
        if submitted:
            if not all([soldier_id, firstname, regiment, bloodline_name]):
                st.error("Please fill all required fields marked with *")
            else:
                try:
                    data = {
                        'id': soldier_id,
                        'firstname': firstname,
                        'lastname': lastname if lastname else None,
                        'dob': dob,
                        'soldier_rank': rank,
                        'regiment': regiment,
                        'status': status,
                        'enlistment_date': enlistment_date,
                        'bloodline_name': bloodline_name,
                        'shifter': shifter,
                        'current_state': 'Soldier'
                    }
                    add_new_soldier(connection, data)
                    st.success(f"Soldier {firstname} {lastname or ''} added successfully!")
                except Exception as e:
                    st.error(f"Failed to add soldier: {e}")
                    st.write(traceback.format_exc())

def rank(connection):
    """Render form for updating soldier rank."""
    st.divider()
    st.subheader("Update Soldier Rank")
    
    try:
        soldiers = fetch_all(connection, 'soldier')
        if soldiers:
            soldier_options = {f"{s['id']} - {s['firstname']} {s['lastname'] or ''}": s for s in soldiers}
            
            with st.form("update_rank_form"):
                selected_soldier = st.selectbox("Select Soldier", options=list(soldier_options.keys()))
                new_rank = st.selectbox("New Rank", options=["Cadet", "Soldier", "Squad_leader", "Commander", "Captain", "General"])
                
                submitted = st.form_submit_button("Update Rank", type="primary")
                
                if submitted:
                    try:
                        soldier = soldier_options[selected_soldier]
                        update_soldier_rank(connection, soldier['id'], new_rank)
                        st.success(f"Rank updated to {new_rank} for soldier {soldier['firstname']} {soldier['lastname'] or ''}")
                    except Exception as e:
                        st.error(f"Failed to update rank: {e}")
                        st.write(traceback.format_exc())
        else:
            st.info("No soldiers found in the database.")
    except Exception as e:
        st.error(f"Failed to fetch soldiers: {e}")

def delete_equipment(connection):
    """Render form for deleting equipment."""
    st.divider()
    st.subheader("Delete Equipment Type")
    st.caption("You may not be able to delete equipment types that were used by soldiers in missions. In such cases, consider making desired_quantity zero instead.")
    
    try:
        equipment = fetch_all(connection, 'equipment')
        if equipment:
            equipment_options = {f"{e['model']} ({e['type']})": e for e in equipment}
            
            with st.form("delete_equipment"):
                selected_equipment = st.selectbox("Select Equipment to Delete", options=list(equipment_options.keys()))
                confirm = st.checkbox("I confirm I want to delete this equipment type")
                
                submitted = st.form_submit_button("Delete Equipment", type="primary")
                
                if submitted:
                    if not confirm:
                        st.error("Please confirm the deletion by checking the checkbox.")
                    else:
                        try:
                            equipment_item = equipment_options[selected_equipment]
                            delete_equipment_type(connection, equipment_item['model'])
                            st.success(f"Equipment {equipment_item['model']} deleted successfully!")
                        except Exception as e:
                            st.error(f"Failed to delete equipment: {e}")
                            st.write(traceback.format_exc())
        else:
            st.info("No equipment found in the database.")
    except Exception as e:
        st.error(f"Failed to fetch equipment: {e}")

def reports(connection):
    """Render the reports section."""
    st.subheader("Analysis Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Threat Report",
            "Commander Performance",
            "Latest Mission Casualties"
        ]
    )
    
    if st.button("Generate Report", type="primary"):
        try:
            if report_type == "Threat Report":
                threat(connection)
            elif report_type == "Commander Performance":
                performance(connection)
            elif report_type == "Latest Mission Casualties":
                casualties(connection)
        except Exception as e:
            st.error(f"Report generation failed: {e}")
            st.write(traceback.format_exc())

def threat(connection):
    """Render the threat report."""
    st.divider()
    st.subheader("Threat Report")
    st.caption("Total Titan sightings and soldier casualties for missions in each district")
    
    results = get_threat_report(connection)
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, width='stretch', hide_index=True)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Districts", len(results))
        with col2:
            total_casualties = sum(row['Soldier_Casualties'] for row in results)
            st.metric("Total Casualties", total_casualties)
    else:
        st.info("No threat data available.")

def performance(connection):
    """Render the commander performance report."""
    st.divider()
    st.subheader("Commander Performance Report")
    st.caption("Missions led by commanders and associated casualties")
    
    results = get_commander_performance(connection)
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, width='stretch', hide_index=True)
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Commanders", len(results))
        with col2:
            total_missions = sum(row['Missions_Led'] for row in results)
            st.metric("Total Missions Led", total_missions)
        with col3:
            total_casualties = sum(row['Total_Casualties'] for row in results)
            st.metric("Total Casualties", total_casualties)
    else:
        st.info("No commander performance data available.")

def casualties(connection):
    """Render the latest mission casualties report."""
    st.divider()
    st.subheader("Latest Mission Casualties")
    st.caption("Detailed analysis of soldiers who died in the most recent mission")
    
    results = get_latest_mission_casualties(connection)
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, width='stretch', hide_index=True)
        
        st.divider()
        if results:
            mission_name = results[0]['Mission']
            st.write(f"**Mission:** {mission_name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Casualties", len(results))
            with col2:
                avg_age = sum(row['Age_at_Death'] or 0 for row in results) / len(results) if results else 0
                st.metric("Average Age", f"{avg_age:.1f} years")
            with col3:
                avg_service = sum(row['Years_of_Service'] or 0 for row in results) / len(results) if results else 0
                st.metric("Avg Years of Service", f"{avg_service:.1f} years")
            
            st.divider()
            st.write("**Casualties by Rank:**")
            rank_counts = {}
            for row in results:
                rank = row['Rank']
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
            rank_df = pd.DataFrame(list(rank_counts.items()), columns=['Rank', 'Count'])
            st.dataframe(rank_df, width='stretch', hide_index=True)
    else:
        st.info("No casualty data available for recent missions.")

def get_credentials():
    use_default = st.checkbox("Use default credentials from environment", value=True)
    if use_default:
        st.info("Using credentials from environment variables (.env file)")
    with st.form("credentials_form"):
        if use_default:
            host = None
            port = None
            user = None
            password = None
        else:
            col1, col2 = st.columns(2)
            with col1:
                host = st.text_input("Host", value="localhost")
                user = st.text_input("Username", value="")
            with col2:
                port = st.number_input("Port", value=3306, min_value=1, max_value=65535)
                password = st.text_input("Password", type="password", value="")
        submitted = st.form_submit_button("Connect", use_container_width=True)
        if submitted:
            st.session_state.db_credentials = {
                'host': host,
                'port': port,
                'user': user,
                'password': password
            }
            st.rerun()
    return None

def app():
    """Main application entry point."""
    st.title("Attack on Titan")
    st.caption("Interface for querying and editing the database.")

    connection=create(use_db=False)
    sidebar()
    if not connection:
        st.error("Failed to connect to the database. Check your connection settings.")
        countdown_placeholder = st.empty()
        for i in range(5, 0, -1):
            countdown_placeholder.info(f"Reloading connection form in {i}...")
            time.sleep(1)
        countdown_placeholder.empty()
        
        st.session_state.pop('db_credentials', None)
        st.rerun()
        return
    connection.close()
    connection=create(use_db=True)
    if not connection:
        st.error("Database not initialized. Please initialize the database from the sidebar.")
        return

    else:
        try:
            tables = get_tables(connection)
        except Exception as e:
            st.error(f"Error fetching tables: {e}")
            return

    st.sidebar.header("Actions")
    action = st.sidebar.radio("Action", options=["Presets", "Reports", "View Records", "Run Query"], label_visibility="collapsed")

    if 'selected_table' not in st.session_state:
        st.session_state.selected_table = tables[0] if tables else None
    
    if action == "View Records":
        view(connection, tables)
    elif action == "Run Query":
        run(connection)
    elif action == "Presets":
        modify(connection)
    elif action == "Reports":
        reports(connection)
