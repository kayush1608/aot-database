# Attack on Titan Database Management System

A comprehensive database management interface for managing Attack on Titan military operations, soldiers, missions, and titan-related data.

A demo of this application is hosted on `https://dna.eastasia.cloudapp.azure.com` (even we don't know why we did this).

## Database Connection Interface
The landing page of the application gives an option to either use environment as mentioned in .env file or put in their own credentials.

## Database Setup Commands
1. **Initialize Database** - Creates the database schema with all tables based on the schema.sql file.
2. **Re-initialize Database** - Drops and recreates the entire database, removing all existing data and resetting to the initial schema.
3. **Populate Sample Data** - Loads sample data into the database from populate.sql.

## Main Application Features
### Preset Queries Section (From Phase 1)
4. **Selection Query (3.1.1) - Filter Soldiers by Regiment and Status** - Retrieve soldiers based on selected regiment and status.
5. **Projection Query (3.1.2) - Display Mission Names and Objectives** - Show mission names and objectives filtered by mission status.
6. **Aggregate Query (3.1.3) - Calculate Average Casualties per Mission** - Compute the average number of casualties across all missions.
7. **Search Query (3.1.4) - Find Missions by Keyword** - Search for missions containing a specific keyword in their objectives.
8. **Add New Soldier to Army** - Insert a new soldier with complete details. Automatically creates bloodline record if it doesn't exist.
9. **Update Soldier Rank** - Change the rank of an existing soldier by selecting from the soldier list and choosing a new rank.
10. **Delete Equipment Type** - Remove an equipment type from the database by model name, with confirmation checkbox and warnings about foreign key constraints.

### Analysis Reports Section (From Phase 1)
11. **Generate Threat Report** - Displays total titan sightings and soldier casualties grouped by district and wall, ordered by threat level. Includes summary metrics for total districts and casualties.
12. **Generate Commander Performance Report** - Shows missions led by commanders (Commander, Captain, General, Squad_leader ranks) along with associated casualties and mission names. Includes metrics for total commanders, missions led, and casualties.
13. **Generate Latest Mission Casualties Report** - Provides detailed analysis of all soldiers who died in the most recent mission, including age at death, years of service, cause of death, titan type, and demographics. Shows breakdown by rank and average statistics.

### View Records Section
14. **Browse Database Tables** - Select and view any table from the database with customizable row limits.
15. **Add New Record** - Insert a new record into any selected table by filling out a dynamic form.
16. **Edit Existing Record** - Select a record by its primary key and update its field values.
17. **Delete Record** - Select and remove a specific record from any table.

### Custom SQL Section
> This is just implemented for this testing app, a production app will not have these kind of things normally.
18. **Execute Custom SQL Queries** - Run any custom SQL query through a text area interface, with results displayed in a formatted table and error display for invalid queries.

## Pre-requisites
- MySQL80 or similar version should be installed and running.
- Python 3.10 or above with respective pip version.

## How to Run the Application
```
pip install -r requirements.txt
cp src/.env.example src/.env
streamlit run src/main_app.py
```
Feel free to edit .env files or just use the login screen to put desired values.

*Generative AI was partially used (believe us, it failed to do a few things, so we did those) to make the GUI and give us functions for the same in which sql queries were written.*