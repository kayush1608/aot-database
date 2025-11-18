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
