import psycopg2
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="db", 
        database="f1db",
        user="postgres",
        password="password",
        port="5432"
    )

conn = get_connection()

st.title("F1 Data")
st.sidebar.title("Choose an operation")
sidebar = st.sidebar.radio("", [
    "Team carry", 
    "Driver Points Evolution", 
    "Driver Duel", 
    "Victories by Nationality", 
    "Insert new data", 
    "Modify data", 
    "Delete data", 
    "Yearly schedule"
])

def new_constructor(conn):
    st.markdown("Insert new constructor")
    with st.form("new_constructor"):
        name = st.text_input("Constructor name*")
        nationality = st.text_input("Nationality*")
        url = st.text_input("Wikipedia URL")
        inviato = st.form_submit_button("Add constructor")
        if inviato:
            if name and nationality:
                query = "INSERT INTO constructors (name, nationality, url) VALUES (%s, %s, %s)"
                try:
                    cur = conn.cursor()
                    cur.execute(query, (name, nationality, url))
                    conn.commit()
                    cur.close()
                    st.toast("Constructor added!")
                    st.success(f"{name} has been added to the constructors!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback() # Annulla in caso di errore
            else:
                st.warning("All * fields are mandatory!")

def delete_constructor(conn):
    st.markdown("Delete constructor")
    st.write("Insert the constructor's name to remove it from the database (this is not reversible).")
    with st.form("delete_constructor"):
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Constructor name*")
        with col2:
            search_id = st.number_input("Constructor ID (optional)", min_value=1, step=1, value=None)
        inviato = st.form_submit_button("Delete constructor", type="primary")
        if inviato:
            if search_name:
                check_query = "SELECT constructorid, name, nationality FROM constructors WHERE name = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No constructor found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple constructors found. Specify the Constructor ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    try:
                        if search_id is not None:
                            query, parameters = "DELETE FROM constructors WHERE constructorid = %s", (search_id,)
                        else:
                            query, parameters = "DELETE FROM constructors WHERE name = %s", (search_name,)
                        
                        cur = conn.cursor()
                        cur.execute(query, parameters)
                        rowcount = cur.rowcount
                        conn.commit()
                        cur.close()
                        
                        if rowcount > 0:
                            st.success(f"Constructor '{search_name}' deleted successfully!")
                            st.toast("Constructor deleted!")
                        else:
                            st.error("Constructor not deleted. Check if the ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                        conn.rollback()
            else:
                st.warning("Constructor name is mandatory!")

def alter_constructor(conn):
    st.markdown("Update Constructor Info")
    st.write("Insert the constructor's name, then fill ONLY the fields you want to modify.")
    with st.form("alter_constructor"):
        st.markdown("Which constructor do you want to modify?")
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Current constructor name*")
        with col2:
            search_id = st.number_input("Constructor ID (optional)", min_value=1, step=1, value=None)
        st.divider()
        st.markdown("Insert new values (leave blank to keep current)")
        new_name = st.text_input("New name")
        new_nationality = st.text_input("New nationality")
        new_url = st.text_input("New Wikipedia URL")
        inviato = st.form_submit_button("Update Constructor", use_container_width=True)
        if inviato:
            if search_name:
                check_query = "SELECT constructorid, name, nationality FROM constructors WHERE name = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No constructor found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple constructors found. Specify the Constructor ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    update_fields, parameters = [], []
                    if new_name: update_fields.append("name = %s"); parameters.append(new_name)
                    if new_nationality: update_fields.append("nationality = %s"); parameters.append(new_nationality)
                    if new_url: update_fields.append("url = %s"); parameters.append(new_url)
                    if not update_fields:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE constructors SET {set_clause} WHERE constructorid = %s"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE constructors SET {set_clause} WHERE name = %s"
                            parameters.append(search_name)
                        try:
                            cur = conn.cursor()
                            cur.execute(query, tuple(parameters))
                            conn.commit()
                            cur.close()
                            st.success(f"Constructor '{search_name}' updated successfully!")
                            st.toast("Constructor updated!")
                        except Exception as e:
                            st.error(f"Database error: {e}")
                            conn.rollback()
            else:
                st.warning("Constructor name is mandatory!")

def new_circuit(conn):
    st.markdown("Insert new circuit")
    with st.form("new_circuit"):
        name = st.text_input("Circuit name*")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location (city)")
            country = st.text_input("Country")
            alt = st.number_input("Altitude (m)", value=None, step=1)
        with col2:
            lat = st.number_input("Latitude", value=None, format="%.6f")
            lng = st.number_input("Longitude", value=None, format="%.6f")
        url = st.text_input("Wikipedia URL")
        inviato = st.form_submit_button("Add circuit")
        if inviato:
            if name:
                query = "INSERT INTO circuits (name, location, country, lat, lng, alt, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                try:
                    cur = conn.cursor()
                    cur.execute(query, (name, location, country, lat, lng, alt, url))
                    conn.commit()
                    cur.close()
                    st.toast("Circuit added!")
                    st.success(f"{name} has been added to the circuits!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("Circuit name is mandatory!")

def alter_circuit(conn):
    st.markdown("Update Circuit Info")
    st.write("Insert the circuit's name, then fill ONLY the fields you want to modify.")
    with st.form("alter_circuit"):
        st.markdown("Which circuit do you want to modify?")
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Current circuit name*")
        with col2:
            search_id = st.number_input("Circuit ID (optional)", min_value=1, step=1, value=None)
        st.divider()
        st.markdown("Insert new values (leave blank to keep current)")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New name")
            new_location = st.text_input("New location")
            new_country = st.text_input("New country")
            new_alt = st.number_input("New altitude (m)", value=None, step=1)
        with col2:
            new_lat = st.number_input("New latitude", value=None, format="%.6f")
            new_lng = st.number_input("New longitude", value=None, format="%.6f")
            new_url = st.text_input("New Wikipedia URL")
        inviato = st.form_submit_button("Update Circuit", use_container_width=True)
        if inviato:
            if search_name:
                check_query = "SELECT circuitid, name, location, country FROM circuits WHERE name = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No circuit found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple circuits found. Specify the Circuit ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    update_fields, parameters = [], []
                    if new_name: update_fields.append("name = %s"); parameters.append(new_name)
                    if new_location: update_fields.append("location = %s"); parameters.append(new_location)
                    if new_country: update_fields.append("country = %s"); parameters.append(new_country)
                    if new_lat is not None: update_fields.append("lat = %s"); parameters.append(new_lat)
                    if new_lng is not None: update_fields.append("lng = %s"); parameters.append(new_lng)
                    if new_alt is not None: update_fields.append("alt = %s"); parameters.append(new_alt)
                    if new_url: update_fields.append("url = %s"); parameters.append(new_url)
                    if not update_fields:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE circuits SET {set_clause} WHERE circuitid = %s"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE circuits SET {set_clause} WHERE name = %s"
                            parameters.append(search_name)
                        try:
                            cur = conn.cursor()
                            cur.execute(query, tuple(parameters))
                            conn.commit()
                            cur.close()
                            st.success(f"Circuit '{search_name}' updated successfully!")
                            st.toast("Circuit updated!")
                        except Exception as e:
                            st.error(f"Database error: {e}")
                            conn.rollback()
            else:
                st.warning("Circuit name is mandatory!")

def delete_circuit(conn):
    st.markdown("Delete circuit")
    st.write("Insert the circuit's name to remove it from the database (this is not reversible).")
    with st.form("delete_circuit"):
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Circuit name*")
        with col2:
            search_id = st.number_input("Circuit ID (optional)", min_value=1, step=1, value=None)
        inviato = st.form_submit_button("Delete circuit", type="primary")
        if inviato:
            if search_name:
                check_query = "SELECT circuitid, name, location, country FROM circuits WHERE name = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No circuit found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple circuits found. Specify the Circuit ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    try:
                        if search_id is not None:
                            query, parameters = "DELETE FROM circuits WHERE circuitid = %s", (search_id,)
                        else:
                            query, parameters = "DELETE FROM circuits WHERE name = %s", (search_name,)
                        
                        cur = conn.cursor()
                        cur.execute(query, parameters)
                        rowcount = cur.rowcount
                        conn.commit()
                        cur.close()
                        
                        if rowcount > 0:
                            st.success(f"Circuit '{search_name}' deleted successfully!")
                            st.toast("Circuit deleted!")
                        else:
                            st.error("Circuit not deleted. Check if the ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                        conn.rollback()
            else:
                st.warning("Circuit name is mandatory!")

def new_status(conn):
    st.markdown("Insert new status")
    with st.form("new_status"):
        status = st.text_input("Status label*")
        inviato = st.form_submit_button("Add status")
        if inviato:
            if status:
                query = "INSERT INTO status (status) VALUES (%s)"
                try:
                    cur = conn.cursor()
                    cur.execute(query, (status,))
                    conn.commit()
                    cur.close()
                    st.toast("Status added!")
                    st.success(f"Status '{status}' has been added!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("Status field is mandatory!")

def alter_status(conn):
    st.markdown("Update Status")
    with st.form("alter_status"):
        st.markdown("Which status do you want to modify?")
        status_df = pd.read_sql("SELECT statusid, status FROM status ORDER BY status", conn)
        status_opts = {r["status"]: r["statusid"] for _, r in status_df.iterrows()}
        current_status = st.selectbox("Current status*", list(status_opts.keys()))
        st.divider()
        new_status = st.text_input("New status label*")
        inviato = st.form_submit_button("Update Status", use_container_width=True)
        if inviato:
            if new_status:
                statusid = status_opts[current_status]
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE status SET status = %s WHERE statusid = %s", (new_status, statusid))
                    conn.commit()
                    cur.close()
                    st.success(f"Status '{current_status}' updated to '{new_status}'!")
                    st.toast("Status updated!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("New status label is mandatory!")

def delete_status(conn):
    st.markdown("Delete status")
    st.write("Select a status to remove it from the database (this is not reversible).")
    with st.form("delete_status"):
        status_df = pd.read_sql("SELECT statusid, status FROM status ORDER BY status", conn)
        status_opts = {r["status"]: r["statusid"] for _, r in status_df.iterrows()}
        selected_status = st.selectbox("Status to delete*", list(status_opts.keys()))
        inviato = st.form_submit_button("Delete status", type="primary")
        if inviato:
            try:
                statusid = status_opts[selected_status]
                cur = conn.cursor()
                cur.execute("DELETE FROM status WHERE statusid = %s", (statusid,))
                rowcount = cur.rowcount
                conn.commit()
                cur.close()
                if rowcount > 0:
                    st.success(f"Status '{selected_status}' deleted successfully!")
                    st.toast("Status deleted!")
                else:
                    st.error("Status not deleted.")
            except Exception as e:
                st.error(f"Database error: {e}")
                conn.rollback()

def new_race(conn):
    st.markdown("Insert new race")
    circuits_df = pd.read_sql("SELECT circuitid, name FROM circuits ORDER BY name", conn)
    circuit_options = {row["name"]: row["circuitid"] for _, row in circuits_df.iterrows()}

    with st.form("new_race"):
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Year*", min_value=1950, max_value=2100, step=1)
            round_n = st.number_input("Round*", min_value=1, step=1)
            name = st.text_input("Race name*")
            date = st.date_input("Race date*")
            time_race = st.text_input("Race time (HH:MM:SS)")
        with col2:
            circuit_name = st.selectbox("Circuit*", list(circuit_options.keys()))
            quali_date = st.date_input("Qualifying date")
            quali_time = st.text_input("Qualifying time (HH:MM:SS)")
            sprint_date = st.date_input("Sprint date (optional)")
            sprint_time = st.text_input("Sprint time (HH:MM:SS, optional)")
        url = st.text_input("Wikipedia URL")
        inviato = st.form_submit_button("Add race")
        if inviato:
            if name and year and round_n and date and circuit_name:
                circuitid = circuit_options[circuit_name]
                query = """INSERT INTO races (year, round, circuitid, name, date, time_race, url, quali_date, quali_time, sprint_date, sprint_time)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                try:
                    cur = conn.cursor()
                    cur.execute(query, (year, round_n, circuitid, name, str(date),
                                         time_race or None, url or None,
                                         str(quali_date), quali_time or None,
                                         str(sprint_date), sprint_time or None))
                    conn.commit()
                    cur.close()
                    st.toast("Race added!")
                    st.success(f"{name} {year} has been added!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("All * fields are mandatory!")

def alter_race(conn):
    st.markdown("Update Race Info")
    st.write("Search the race by name and year, then fill ONLY the fields you want to modify.")
    with st.form("alter_race"):
        st.markdown("Which race do you want to modify?")
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Race name*")
        with col2:
            search_year = st.number_input("Year*", min_value=1950, max_value=2100, step=1)
        with col3:
            search_id = st.number_input("Race ID (optional)", min_value=1, step=1, value=None)
        st.divider()
        st.markdown("Insert new values (leave blank to keep current)")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New name")
            new_date = st.text_input("New race date (YYYY-MM-DD)")
            new_time = st.text_input("New race time (HH:MM:SS)")
            new_round = st.number_input("New round", min_value=1, step=1, value=None)
        with col2:
            new_quali_date = st.text_input("New qualifying date (YYYY-MM-DD)")
            new_quali_time = st.text_input("New qualifying time (HH:MM:SS)")
            new_sprint_date = st.text_input("New sprint date (YYYY-MM-DD)")
            new_sprint_time = st.text_input("New sprint time (HH:MM:SS)")
        new_url = st.text_input("New Wikipedia URL")
        inviato = st.form_submit_button("Update Race", use_container_width=True)
        if inviato:
            if search_name and search_year:
                check_query = "SELECT raceid, name, year, round FROM races WHERE name = %s AND year = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_year))
                if len(df_check) == 0:
                    st.warning(f"No race found named '{search_name}' in {search_year}.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple races found. Specify the Race ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    update_fields, parameters = [], []
                    if new_name: update_fields.append("name = %s"); parameters.append(new_name)
                    if new_date: update_fields.append("date = %s"); parameters.append(new_date)
                    if new_time: update_fields.append("time_race = %s"); parameters.append(new_time)
                    if new_round is not None: update_fields.append("round = %s"); parameters.append(new_round)
                    if new_quali_date: update_fields.append("quali_date = %s"); parameters.append(new_quali_date)
                    if new_quali_time: update_fields.append("quali_time = %s"); parameters.append(new_quali_time)
                    if new_sprint_date: update_fields.append("sprint_date = %s"); parameters.append(new_sprint_date)
                    if new_sprint_time: update_fields.append("sprint_time = %s"); parameters.append(new_sprint_time)
                    if new_url: update_fields.append("url = %s"); parameters.append(new_url)
                    if not update_fields:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE races SET {set_clause} WHERE raceid = %s"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE races SET {set_clause} WHERE name = %s AND year = %s"
                            parameters.extend([search_name, search_year])
                        try:
                            cur = conn.cursor()
                            cur.execute(query, tuple(parameters))
                            conn.commit()
                            cur.close()
                            st.success(f"Race '{search_name} {search_year}' updated successfully!")
                            st.toast("Race updated!")
                        except Exception as e:
                            st.error(f"Database error: {e}")
                            conn.rollback()
            else:
                st.warning("Race name and year are mandatory!")

def delete_race(conn):
    st.markdown("Delete race")
    st.write("Insert the race's name and year to remove it from the database (this is not reversible).")
    with st.form("delete_race"):
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Race name*")
        with col2:
            search_year = st.number_input("Year*", min_value=1950, max_value=2100, step=1)
        with col3:
            search_id = st.number_input("Race ID (optional)", min_value=1, step=1, value=None)
        inviato = st.form_submit_button("Delete race", type="primary")
        if inviato:
            if search_name and search_year:
                check_query = "SELECT raceid, name, year, round FROM races WHERE name = %s AND year = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_year))
                if len(df_check) == 0:
                    st.warning(f"No race found named '{search_name}' in {search_year}.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple races found. Specify the Race ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    try:
                        if search_id is not None:
                            query, parameters = "DELETE FROM races WHERE raceid = %s", (search_id,)
                        else:
                            query, parameters = "DELETE FROM races WHERE name = %s AND year = %s", (search_name, search_year)
                        
                        cur = conn.cursor()
                        cur.execute(query, parameters)
                        rowcount = cur.rowcount
                        conn.commit()
                        cur.close()
                        if rowcount > 0:
                            st.success(f"Race '{search_name} {search_year}' deleted successfully!")
                            st.toast("Race deleted!")
                        else:
                            st.error("Race not deleted. Check if the ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                        conn.rollback()
            else:
                st.warning("Race name and year are mandatory!")

def new_result(conn):
    st.markdown("Insert new result")
    drivers_df = pd.read_sql("SELECT driverid, name || ' ' || surname AS fullname FROM drivers ORDER BY surname", conn)
    constructors_df = pd.read_sql("SELECT constructorid, name FROM constructors ORDER BY name", conn)
    races_df = pd.read_sql("SELECT raceid, year || ' - ' || name AS racename FROM races ORDER BY year DESC, round", conn)
    status_df = pd.read_sql("SELECT statusid, status FROM status ORDER BY status", conn)

    driver_opts = {r["fullname"]: r["driverid"] for _, r in drivers_df.iterrows()}
    constructor_opts = {r["name"]: r["constructorid"] for _, r in constructors_df.iterrows()}
    race_opts = {r["racename"]: r["raceid"] for _, r in races_df.iterrows()}
    status_opts = {r["status"]: r["statusid"] for _, r in status_df.iterrows()}

    with st.form("new_result"):
        col1, col2 = st.columns(2)
        with col1:
            race_name = st.selectbox("Race*", list(race_opts.keys()))
            driver_name = st.selectbox("Driver*", list(driver_opts.keys()))
            constructor_name = st.selectbox("Constructor*", list(constructor_opts.keys()))
            status_name = st.selectbox("Status*", list(status_opts.keys()))
            number = st.number_input("Car number", min_value=1, max_value=99, step=1, value=None)
        with col2:
            grid = st.number_input("Grid position", min_value=0, step=1, value=None)
            position = st.number_input("Final position", min_value=0, step=1, value=None)
            positionText = st.text_input("Position text (e.g. 1, R, D)")
            positionOrder = st.number_input("Position order*", min_value=1, step=1)
            points = st.number_input("Points", min_value=0.0, step=0.5, value=0.0)
        col3, col4 = st.columns(2)
        with col3:
            laps = st.number_input("Laps completed", min_value=0, step=1, value=None)
            milliseconds = st.number_input("Total time (ms)", min_value=0, step=1, value=None)
            fastestLap = st.number_input("Fastest lap (lap number)", min_value=0, step=1, value=None)
        with col4:
            rank = st.number_input("Fastest lap rank", min_value=0, step=1, value=None)
            fastestLapTime = st.text_input("Fastest lap time (M:SS.mmm)")
            fastestLapSpeed = st.number_input("Fastest lap speed (km/h)", min_value=0.0, step=0.1, value=None)

        inviato = st.form_submit_button("Add result")
        if inviato:
            if race_name and driver_name and constructor_name and positionOrder:
                query = """INSERT INTO results (raceid, driverid, constructorid, statusid, number, grid, position,
                           positionText, positionOrder, points, laps, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                try:
                    cur = conn.cursor()
                    cur.execute(query, (
                        race_opts[race_name], driver_opts[driver_name],
                        constructor_opts[constructor_name], status_opts[status_name],
                        number, grid, position, positionText or None, positionOrder,
                        points, laps, milliseconds, fastestLap, rank,
                        fastestLapTime or None, fastestLapSpeed
                    ))
                    conn.commit()
                    cur.close()
                    st.toast("Result added!")
                    st.success("Result has been added successfully!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("All * fields are mandatory!")

def alter_result(conn):
    st.markdown("Update Result Info")
    st.write("Search by Result ID (visible in the results table).")
    with st.form("alter_result"):
        search_id = st.number_input("Result ID*", min_value=1, step=1)
        st.divider()
        st.markdown("Insert new values (leave blank / 0 to keep current)")
        col1, col2 = st.columns(2)
        with col1:
            new_grid = st.number_input("New grid position", min_value=0, step=1, value=None)
            new_position = st.number_input("New final position", min_value=0, step=1, value=None)
            new_positionText = st.text_input("New position text (e.g. 1, R, D)")
            new_positionOrder = st.number_input("New position order", min_value=1, step=1, value=None)
            new_points = st.number_input("New points", min_value=0.0, step=0.5, value=None)
        with col2:
            new_laps = st.number_input("New laps", min_value=0, step=1, value=None)
            new_ms = st.number_input("New time (ms)", min_value=0, step=1, value=None)
            new_fastestLap = st.number_input("New fastest lap (lap nr)", min_value=0, step=1, value=None)
            new_rank = st.number_input("New fastest lap rank", min_value=0, step=1, value=None)
            new_fastestLapTime = st.text_input("New fastest lap time (M:SS.mmm)")
            new_fastestLapSpeed = st.number_input("New fastest lap speed (km/h)", min_value=0.0, step=0.1, value=None)
        inviato = st.form_submit_button("Update Result", use_container_width=True)
        if inviato:
            check_df = pd.read_sql("SELECT resultid FROM results WHERE resultid = %s", conn, params=(search_id,))
            if len(check_df) == 0:
                st.warning(f"No result found with ID {search_id}.")
            else:
                update_fields, parameters = [], []
                if new_grid is not None: update_fields.append("grid = %s"); parameters.append(new_grid)
                if new_position is not None: update_fields.append("position = %s"); parameters.append(new_position)
                if new_positionText: update_fields.append("positionText = %s"); parameters.append(new_positionText)
                if new_positionOrder is not None: update_fields.append("positionOrder = %s"); parameters.append(new_positionOrder)
                if new_points is not None: update_fields.append("points = %s"); parameters.append(new_points)
                if new_laps is not None: update_fields.append("laps = %s"); parameters.append(new_laps)
                if new_ms is not None: update_fields.append("milliseconds = %s"); parameters.append(new_ms)
                if new_fastestLap is not None: update_fields.append("fastestLap = %s"); parameters.append(new_fastestLap)
                if new_rank is not None: update_fields.append("rank = %s"); parameters.append(new_rank)
                if new_fastestLapTime: update_fields.append("fastestLapTime = %s"); parameters.append(new_fastestLapTime)
                if new_fastestLapSpeed is not None: update_fields.append("fastestLapSpeed = %s"); parameters.append(new_fastestLapSpeed)
                if not update_fields:
                    st.warning("Update at least one parameter")
                else:
                    set_clause = ", ".join(update_fields)
                    query = f"UPDATE results SET {set_clause} WHERE resultid = %s"
                    parameters.append(search_id)
                    try:
                        cur = conn.cursor()
                        cur.execute(query, tuple(parameters))
                        conn.commit()
                        cur.close()
                        st.success(f"Result ID {search_id} updated successfully!")
                        st.toast("Result updated!")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                        conn.rollback()

def delete_result(conn):
    st.markdown("Delete result")
    st.write("Insert the Result ID to remove it from the database (this is not reversible).")
    with st.form("delete_result"):
        result_id = st.number_input("Result ID*", min_value=1, step=1)
        inviato = st.form_submit_button("Delete result", type="primary")
        if inviato:
            check_df = pd.read_sql("SELECT resultid FROM results WHERE resultid = %s", conn, params=(result_id,))
            if len(check_df) == 0:
                st.warning(f"No result found with ID {result_id}.")
            else:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM results WHERE resultid = %s", (result_id,))
                    rowcount = cur.rowcount
                    conn.commit()
                    cur.close()
                    if rowcount > 0:
                        st.success(f"Result ID {result_id} deleted successfully!")
                        st.toast("Result deleted!")
                    else:
                        st.error("Result not deleted.")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()

def new_driver(conn):
    st.markdown("Insert new Driver")
    with st.form("newpilot"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name*")
            surname = st.text_input("Surname*")
            number= st.number_input("Number", min_value=1, max_value=100, step=1)
        with col2:
            code = st.text_input("Driver code (for ex LEC)")
            dob = st.date_input("Date of birth")
            nationality = st.text_input("Nationality")
        url = st.text_input("URL to his wikipedia")
        
        inviato = st.form_submit_button("Add driver")
        code = code.upper() if code != "" else None
        if inviato:
            if name and surname:
                query = "INSERT INTO drivers (name, surname, number, code, dob, nationality, url) VALUES (%s, %s ,%s, %s ,%s , %s, %s)"
                try:
                    cur = conn.cursor()
                    cur.execute(query, (name, surname, number, code, dob, nationality, url))
                    conn.commit()
                    cur.close()
                    st.toast("Driver added!")
                    st.success(f"{name} {surname} has been added to the pilots!")
                except Exception as e:
                    st.error(f"Database error: {e}")
                    conn.rollback()
            else:
                st.warning("All * fields are mandatory!")

def alter_driver(conn):
    st.markdown("Update Driver Info")
    st.write("Insert the driver's name and surname, then fill ONLY the fields you want to modify.")
    
    with st.form("alterdriver"):
        st.markdown("Who do you want to modify?")
        col_search1, col_search2, col_search3 = st.columns(3)
        with col_search1:
            search_name = st.text_input("Current Name*")
        with col_search2:
            search_surname = st.text_input("Current Surname*")
        with col_search3:
            search_id = st.number_input("Driver ID (optional)", min_value=1, step=1, value=None)
            
        st.divider() 
        st.markdown("Insert new values (leave blank to keep current)")
        
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New name")
            new_surname = st.text_input("New surname")
            new_number = st.number_input("New number", min_value=1, max_value=99, step=1, value=None)
        with col2:
            new_code = st.text_input("New pilot code", max_chars=3)
            new_nationality = st.text_input("New nationality")
            new_url = st.text_input("New wikipedia URL")
            
        inviato = st.form_submit_button("Update Driver", use_container_width=True)
        
        if inviato:
            if search_name and search_surname:
                check_query = "SELECT driverid, name, surname, dob, nationality FROM drivers WHERE name = %s AND surname = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_surname))
                    
                if len(df_check) == 0:
                        st.warning(f"No driver found named {search_name} {search_surname}.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple drivers found with this name, check the list below and specify the correct driver id in the search box")
                    st.dataframe(df_check, hide_index=True)
                else:
                    update_fields = []
                    parameters = []
                    if new_name != "": update_fields.append("name = %s"); parameters.append(new_name)
                    if new_surname != "": update_fields.append("surname = %s"); parameters.append(new_surname)
                    if new_number is not None: update_fields.append("number = %s"); parameters.append(new_number)
                    if new_code != "": update_fields.append("code = %s"); parameters.append(new_code.upper())
                    if new_nationality != "": update_fields.append("nationality = %s"); parameters.append(new_nationality)
                    if new_url != "": update_fields.append("url = %s"); parameters.append(new_url)
            
                    if len(update_fields) == 0:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE drivers SET {set_clause} WHERE driverid = %s"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE drivers SET {set_clause} WHERE name = %s AND surname = %s"
                            parameters.extend([search_name, search_surname]) 
                        
                        try:
                            cur = conn.cursor()
                            cur.execute(query, tuple(parameters))
                            conn.commit()
                            cur.close()
                            st.success(f"Driver {search_name} {search_surname} updated successfully!")
                            st.toast("Driver updated!")
                        except Exception as e:
                            st.error(f"Database error: {e}")
                            conn.rollback()
            else:
                st.warning("Driver's name and surname are mandatory to find the driver!")

def delete_driver(conn):
    st.markdown("Delete driver")
    st.write("Insert the driver's name and surname to remove them from the database (remember this is not reversible)")
    
    with st.form("deletedriver"):
        st.markdown("Who do you want to delete?")
        col_search1, col_search2, col_search3 = st.columns(3)
        with col_search1:
            search_name = st.text_input("Name*")
        with col_search2:
            search_surname = st.text_input("Surname*")
        with col_search3:
            search_id = st.number_input("Driver ID (optional)", min_value=1, step=1, value=None)
            
        inviato = st.form_submit_button("Delete driver", type="primary")
        
        if inviato:
            if search_name and search_surname:
                check_query = "SELECT driverid, name, surname, dob, nationality FROM drivers WHERE name = %s AND surname = %s"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_surname))
                    
                if len(df_check) == 0:
                    st.warning(f"No driver found named {search_name} {search_surname}.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple drivers found with this name. Check the list below and specify the correct driver ID to delete.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    if search_id is not None:
                        query = "DELETE FROM drivers WHERE driverid = %s"
                        parameters = (search_id,)
                    else:
                        query = "DELETE FROM drivers WHERE name = %s AND surname = %s"
                        parameters = (search_name, search_surname)
                    
                    try:
                        cur = conn.cursor()
                        cur.execute(query, parameters)
                        rowcount = cur.rowcount
                        conn.commit()
                        cur.close()
                        if rowcount > 0:
                            st.success(f"Driver {search_name} {search_surname} has been successfully deleted!")
                            st.toast("Driver deleted!")
                        else:
                            st.error("Error! Driver not deleted. Check if the Driver ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                        conn.rollback()
            else:
                st.warning("Driver's name and surname are mandatory to find the driver!")

def yearly_schedule(conn):
    st.subheader("View the yearly schedule with race winners")
    anno_scelto = st.number_input("Choose a season year to view (from 1950 to 2024)", min_value=1950, max_value=2024, step=1)

    query = """
        SELECT 
            ra.round AS "Round", 
            ra.name AS "Grand Prix", 
            ra.date AS "Date",
            d.name || ' ' || d.surname AS "Winner"
        FROM races ra
        LEFT JOIN results re ON ra.raceid = re.raceid AND re.positionOrder = 1
        LEFT JOIN drivers d ON re.driverid = d.driverid
        WHERE ra.year = %s 
        ORDER BY ra.round ASC
    """
        
    df = pd.read_sql(query, conn, params=(anno_scelto,))
            
    if not df.empty:
        st.success(f"Trovate {len(df)} gare per la stagione {anno_scelto}!")
        st.dataframe(df, hide_index=True) 
    else:
        st.warning(f"Nessuna gara trovata per il {anno_scelto}.")

def insertpage(conn):
    insert = st.selectbox("What do you want to insert? ",["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])
    match insert:
        case "Drivers": new_driver(conn)
        case "Circuits": new_circuit(conn)
        case "Constructors": new_constructor(conn)
        case "Races": new_race(conn)
        case "Results": new_result(conn)
        case "Status": new_status(conn)

def modifypage(conn):
    st.subheader("Which table do you want to modify?")
    insert = st.selectbox("", ["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])
    match insert:
        case "Drivers": alter_driver(conn)
        case "Circuits": alter_circuit(conn)
        case "Constructors": alter_constructor(conn)
        case "Races": alter_race(conn)
        case "Results": alter_result(conn)
        case "Status": alter_status(conn)

def deletepage(conn):
    st.subheader("Which table do you want to delete data from?")
    insert = st.selectbox("", ["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])
    match insert:
        case "Drivers": delete_driver(conn)
        case "Circuits": delete_circuit(conn)
        case "Constructors": delete_constructor(conn)
        case "Races": delete_race(conn)
        case "Results": delete_result(conn)
        case "Status": delete_status(conn)

def team_carry(conn):
    st.markdown("Team carry")
    st.write("Which driver contributed the highest percentage of points to their constructor in a said season?")

    year = st.number_input("Select Season:", min_value=1950, max_value=2024, value=2021, step=1)

    query = """
        WITH TeamStats AS (
            SELECT 
                c.constructorid, 
                SUM(re.points) AS "TotalTeamPoints"
            FROM results re
            JOIN races ra ON re.raceid = ra.raceid
            JOIN constructors c ON re.constructorid = c.constructorid
            WHERE ra.year = %s
            GROUP BY c.constructorid
        )
        SELECT 
            d.name || ' ' || d.surname AS "Driver",
            c.name AS "Constructor",
            SUM(re.points) AS "DriverPoints",
            ts."TotalTeamPoints",
            ROUND(((SUM(re.points) * 100.0) / ts."TotalTeamPoints")::numeric, 2) AS "Contribution" --numeric per fare in modo che postgres abbia il tipo di dato giusto da poter arrotondare, altrimenti non lo fa
        FROM results re
        JOIN drivers d ON re.driverid = d.driverid
        JOIN constructors c ON re.constructorid = c.constructorid
        JOIN races ra ON re.raceid = ra.raceid
        JOIN TeamStats ts ON c.constructorid = ts.constructorid  
        WHERE ra.year = %s and ts."TotalTeamPoints" > 0
        GROUP BY d.driverid, d.name, d.surname, c.name, ts."TotalTeamPoints"
        ORDER BY ts."TotalTeamPoints" DESC, "Contribution" DESC
    """

    df = pd.read_sql(query, conn, params=(year, year))

    if df.empty:
        st.warning(f"No points data available for {year}.")
        return

    top = df.loc[df["Contribution"].idxmax()]
    st.info(f"Biggest carry of {year}: {top['Driver']} scored {top['Contribution']}% of {top['Constructor']}'s points ({int(top['DriverPoints'])} / {int(top['TotalTeamPoints'])})")

    st.markdown("Points scored per driver")
    df_points = df.set_index("Driver")[["DriverPoints"]].rename(columns={"DriverPoints": "Points"})
    st.bar_chart(df_points)

    st.markdown("**Drivers who scored more than 50% of their team's total points**")
    carries = df[df["Contribution"] > 50].set_index("Driver")[["Contribution"]].rename(columns={"Contribution": "% of team points"})
    if carries.empty:
        st.write("No driver scored more than 50 perc of their team points this season.")
    else:
        st.bar_chart(carries)

    with st.expander("See full data table"):
        df_display = df.rename(columns={
            "DriverPoints": "Driver Pts",
            "TotalTeamPoints": "Team Total Pts",
            "Contribution": "Contribution (%)"
        })
        st.dataframe(df_display[["Driver", "Constructor", "Driver Pts", "Team Total Pts", "Contribution (%)"]],
                     hide_index=True, use_container_width=True)

def driver_points_evolution(conn):
    st.markdown("Driver Points Evolution")
    st.write("Track how a driver accumulated points race by race throughout a season.")

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Select Season:", min_value=1950, max_value=2024, value=2021, step=1, key="evol_year")
    with col2:
        search_name = st.text_input("Driver surname (Hamilton, Verstappen)")

    if not search_name:
        st.info("Enter a driver surname to see their points evolution.")
        return

    query = """
        SELECT
            ra.round AS "Round",
            ra.name AS "GrandPrix",
            re.points AS "RacePoints",
            SUM(re.points) OVER (
                PARTITION BY re.driverid
                ORDER BY ra.round
            ) AS "CumulativePoints"
        FROM results re
        JOIN races ra ON re.raceid = ra.raceid
        JOIN drivers d ON re.driverid = d.driverid
        WHERE ra.year = %s
          AND d.surname = %s
        ORDER BY ra.round ASC
    """

    df = pd.read_sql(query, conn, params=(year, search_name))

    if df.empty:
        st.warning(f"No data found for '{search_name}' in {year}. Check the surname spelling.")
        return

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Points", int(df["CumulativePoints"].iloc[-1]))
    col_b.metric("Races Completed", len(df))
    col_c.metric("Best Single Race", int(df["RacePoints"].max()))

    st.markdown("Cumulative points by round")
    chart_data = df.set_index("Round")[["CumulativePoints"]]
    st.line_chart(chart_data)

    st.markdown("Points per race")
    bar_data = df.set_index("Round")[["RacePoints"]]
    st.bar_chart(bar_data)

    with st.expander("See detailed table"):
        st.dataframe(df[["Round", "GrandPrix", "RacePoints", "CumulativePoints"]], hide_index=True, use_container_width=True)

def driver_duel(conn):
    st.markdown("Driver Duel")
    st.write("Compare two drivers head to head in the same season.")

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("Season:", min_value=1950, max_value=2024, value=2021, step=1, key="duel_year")
    with col2:
        driver1 = st.text_input("First driver surname", value="Hamilton")
    with col3:
        driver2 = st.text_input("Second driver surname", value="Verstappen")

    if not driver1 or not driver2:
        st.info("Enter both driver surnames to compare them.")
        return

    query_points = """
        SELECT
            ra.round AS "Round",
            ra.name AS "GrandPrix",
            d.surname AS "Driver",
            re.points AS "RacePoints",
            SUM(re.points) OVER (
                PARTITION BY re.driverid
                ORDER BY ra.round
            ) AS "CumulativePoints"
        FROM results re
        JOIN races ra ON re.raceid = ra.raceid
        JOIN drivers d ON re.driverid = d.driverid
        WHERE ra.year = %s
          AND d.surname = %s
        ORDER BY ra.round ASC
    """

    query_position = """
        WITH SeasonPoints AS (
            SELECT
                re.driverid,
                d.name || ' ' || d.surname AS "Driver",
                d.surname AS "Surname",
                SUM(re.points) AS "TotalPoints"
            FROM results re
            JOIN races ra ON re.raceid = ra.raceid
            JOIN drivers d ON re.driverid = d.driverid
            WHERE ra.year = %s
            GROUP BY re.driverid, d.name, d.surname
        )
        SELECT
            "Driver",
            "TotalPoints",
            RANK() OVER (ORDER BY "TotalPoints" DESC) AS "ChampionshipPosition"
        FROM SeasonPoints
        WHERE "Surname" = %s
    """

    df1 = pd.read_sql(query_points, conn, params=(year, driver1))
    df2 = pd.read_sql(query_points, conn, params=(year, driver2))
    pos1 = pd.read_sql(query_position, conn, params=(year, driver1))
    pos2 = pd.read_sql(query_position, conn, params=(year, driver2))

    if df1.empty:
        st.warning(f"No data for '{driver1}' in {year}.")
        return
    if df2.empty:
        st.warning(f"No data for '{driver2}' in {year}.")
        return

    name1 = df1["Driver"].iloc[0]
    name2 = df2["Driver"].iloc[0]
    p1_total = int(df1["CumulativePoints"].iloc[-1])
    p2_total = int(df2["CumulativePoints"].iloc[-1])
    champ1 = int(pos1["ChampionshipPosition"].iloc[0]) if not pos1.empty else "N/A"
    champ2 = int(pos2["ChampionshipPosition"].iloc[0]) if not pos2.empty else "N/A"

    winner = name1 if p1_total >= p2_total else name2
    st.success(f"{year} — {winner} wins the duel")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**{name1}**")
        m1, m2 = st.columns(2)
        m1.metric("Points", p1_total, delta=p1_total - p2_total)
        m2.metric("Championship Position", f"P{champ1}")
    with col_b:
        st.markdown(f"**{name2}**")
        m3, m4 = st.columns(2)
        m3.metric("Points", p2_total, delta=p2_total - p1_total)
        m4.metric("Championship Position", f"P{champ2}")

    st.divider()

    merged = pd.merge(
        df1[["Round", "CumulativePoints"]].rename(columns={"CumulativePoints": name1}),
        df2[["Round", "CumulativePoints"]].rename(columns={"CumulativePoints": name2}),
        on="Round", how="outer"
    ).set_index("Round").sort_index()

    st.markdown("Cumulative points race by race")
    st.line_chart(merged)

    race_compare = pd.merge(
        df1[["Round", "RacePoints"]].rename(columns={"RacePoints": name1}),
        df2[["Round", "RacePoints"]].rename(columns={"RacePoints": name2}),
        on="Round", how="outer"
    ).set_index("Round").sort_index()

    st.markdown("Points scored per race")
    st.bar_chart(race_compare)

    with st.expander("See detailed table"):
        st.dataframe(merged.reset_index(), hide_index=True, use_container_width=True)

def victories_by_nationality(conn):
    st.markdown("Victories by Nationality")
    st.write("Which countries have produced the most race winners in F1 history?")

    col1, col2 = st.columns(2)
    with col1:
        year_from = st.number_input("From year:", min_value=1950, max_value=2024, value=1950, step=1)
    with col2:
        year_to = st.number_input("To year:", min_value=1950, max_value=2024, value=2023, step=1)

    if year_from > year_to:
        st.warning("'From year' must be less than or equal to 'To year'.")
        return

    query = """
        SELECT
            d.nationality AS "Nationality",
            COUNT(*) AS "Victories",
            COUNT(DISTINCT d.driverid) AS "UniqueDrivers"
        FROM results re
        JOIN drivers d ON re.driverid = d.driverid
        JOIN races ra ON re.raceid = ra.raceid
        WHERE re.positionOrder = 1
          AND ra.year BETWEEN %s AND %s
        GROUP BY d.nationality
        ORDER BY "Victories" DESC
        LIMIT 20
    """

    df = pd.read_sql(query, conn, params=(year_from, year_to))

    if df.empty:
        st.warning("No data found for the selected period.")
        return

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Top Nation", df["Nationality"].iloc[0])
    col_b.metric("Their Victories", int(df["Victories"].iloc[0]))
    col_c.metric("Nations on Podium", len(df))

    st.markdown("Top 20 nations by race victories")
    chart_data = df.set_index("Nationality")[["Victories"]]
    st.bar_chart(chart_data)

    st.dataframe(df, hide_index=True, use_container_width=True)

match sidebar:
    case "Team carry":
        team_carry(conn)
    case "Driver Points Evolution":
        driver_points_evolution(conn)
    case "Driver Duel":
        driver_duel(conn)
    case "Victories by Nationality":
        victories_by_nationality(conn)
    case "Insert new data":
        insertpage(conn)
    case "Modify data":
        modifypage(conn)
    case "Delete data":
        deletepage(conn)
    case "Yearly schedule":
        yearly_schedule(conn)