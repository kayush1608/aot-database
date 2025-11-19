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
