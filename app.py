import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("f1.db", check_same_thread=False)


st.title("F1 Data")
#st.write("c'è da divertirsi")
st.sidebar.title("Choose an operation")
sidebar=st.sidebar.radio("", ["Search circuits", "Insert new data", "Modify data", "Delete data", "Yearly schedule"])


def new_constructor(conn):
    st.markdown("insert new data")
    with st.form("new_constructor"):
        name=st.text_input("constructor name*")
        nationality=st.text_input("nationality*")
        url=st.text_input("wikipedia URL")
        inviato = st.form_submit_button("Add constructor")
        if inviato:
            if name and nationality:
                query = "INSERT INTO constructors (name, nationality, url) VALUES (?, ?, ?)"
                with conn:
                    conn.execute(query, (name, nationality, url))
                    st.toast("Constructor added!")
                    st.success(f"{name} has been added to the constructors!")
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
                check_query = "SELECT constructorid, name, nationality FROM constructors WHERE name = ?"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No constructor found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple constructors found. Specify the Constructor ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    try:
                        if search_id is not None:
                            query, parameters = "DELETE FROM constructors WHERE constructorid = ?", (search_id,)
                        else:
                            query, parameters = "DELETE FROM constructors WHERE name = ?", (search_name,)
                        with conn:
                            result = conn.execute(query, parameters)
                            if result.rowcount > 0:
                                st.success(f"Constructor '{search_name}' deleted successfully!")
                                st.toast("Constructor deleted!")
                            else:
                                st.error("Constructor not deleted. Check if the ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
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
                check_query = "SELECT constructorid, name, nationality FROM constructors WHERE name = ?"
                df_check = pd.read_sql(check_query, conn, params=(search_name,))
                if len(df_check) == 0:
                    st.warning(f"No constructor found named '{search_name}'.")
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple constructors found. Specify the Constructor ID.")
                    st.dataframe(df_check, hide_index=True)
                else:
                    update_fields, parameters = [], []
                    if new_name: update_fields.append("name = ?"); parameters.append(new_name)
                    if new_nationality: update_fields.append("nationality = ?"); parameters.append(new_nationality)
                    if new_url: update_fields.append("url = ?"); parameters.append(new_url)
                    if not update_fields:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE constructors SET {set_clause} WHERE constructorid = ?"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE constructors SET {set_clause} WHERE name = ?"
                            parameters.append(search_name)
                        with conn:
                            conn.execute(query, tuple(parameters))
                            st.success(f"Constructor '{search_name}' updated successfully!")
                            st.toast("Constructor updated!")
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
                query = "INSERT INTO circuits (name, location, country, lat, lng, alt, url) VALUES (?, ?, ?, ?, ?, ?, ?)"
                with conn:
                    conn.execute(query, (name, location, country, lat, lng, alt, url))
                    st.toast("Circuit added!")
                    st.success(f"{name} has been added to the circuits!")
            else:
                st.warning("Circuit name is mandatory!")







def new_driver(conn):
    st.markdown("Insert new data")
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
                query = "INSERT INTO drivers (name, surname, number, code, dob, nationality, url) VALUES (?, ? ,?, ? ,? , ?, ?)"
                with conn:
                    conn.execute(query, (name, surname,number, code, dob, nationality, url))
                    st.toast("Driver added!")
                    st.success(f"{name} {surname} has been added to the pilots!")
            else:
                st.warning("all * fields are mandatory !")

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
                #looking for double names
                check_query = "SELECT driverid, name, surname, dob, nationality FROM drivers WHERE name = ? AND surname = ?"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_surname))
                    
                if len(df_check) == 0:
                        st.warning(f"No driver found named {search_name} {search_surname}.")
                        
                elif len(df_check) > 1 and search_id is None:
                    st.warning(" Multiple drivers found with this name, check the list below and specify the correct driver id in the search box")
                    st.dataframe(df_check, hide_index=True)
                
            
                else:
                    update_fields = []
                    parameters = []
                    if new_name != "":
                        update_fields.append("name = ?")
                        parameters.append(new_name)
                    if new_surname != "":
                        update_fields.append("surname = ?")
                        parameters.append(new_surname)
                    if new_number is not None:
                        update_fields.append("number = ?")
                        parameters.append(new_number)
                    if new_code != "":
                        update_fields.append("code = ?")
                        parameters.append(new_code.upper())
                    if new_nationality != "":
                        update_fields.append("nationality = ?")
                        parameters.append(new_nationality)
                    if new_url != "":
                        update_fields.append("url = ?")
                        parameters.append(new_url)
            
                    if len(update_fields) == 0:
                        st.warning("Update at least one parameter")
                    else:
                        set_clause = ", ".join(update_fields)
                        if search_id is not None:
                            query = f"UPDATE drivers SET {set_clause} WHERE driverid = ?"
                            parameters.append(search_id)
                        else:
                            query = f"UPDATE drivers SET {set_clause} WHERE name = ? AND surname = ?"
                            parameters.extend([search_name, search_surname]) #per non aggiungere una lista ma i singoli elementi di essa 
                        
                        with conn:
                            conn.execute(query, tuple(parameters))
                            st.success(f"Driver {search_name} {search_surname} updated successfully!")
                            st.toast("Driver updated!")
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
                
                check_query = "SELECT driverid, name, surname, dob, nationality FROM drivers WHERE name = ? AND surname = ?"
                df_check = pd.read_sql(check_query, conn, params=(search_name, search_surname))
                    
                if len(df_check) == 0:
                    st.warning(f"No driver found named {search_name} {search_surname}.")
                        
                elif len(df_check) > 1 and search_id is None:
                    st.warning("Multiple drivers found with this name. Check the list below and specify the correct driver ID to delete.")
                    st.dataframe(df_check, hide_index=True)
                
                else:
                    if search_id is not None:
                        query = "DELETE FROM drivers WHERE driverid = ?"
                        parameters = (search_id,)
                    else:
                        query = "DELETE FROM drivers WHERE name = ? AND surname = ?"
                        parameters = (search_name, search_surname)
                    
                    try:
                        with conn:
                            result = conn.execute(query, parameters)
                            if result.rowcount > 0:
                                st.success(f"Driver {search_name} {search_surname} has been successfully deleted!")
                                st.toast("Driver deleted!")
                            else:
                                st.error("Error! Driver not deleted. Check if the Driver ID is correct.")
                    except Exception as e:
                        st.error(f"Database error: {e}")
            else:
                st.warning("Driver's name and surname are mandatory to find the driver!")

def yearly_schedule(conn):
    st.subheader("View the yearly schedule with race winners")

    anno_scelto = st.number_input("Choose a season year to view (from 1950 to 2024)", min_value=1950, max_value=2024, step=1)

    query = """
        SELECT 
            ra.round AS 'Round', 
            ra.name AS 'Grand Prix', 
            ra.date AS 'Date',
            d.name || ' ' || d.surname AS 'Winner'
        FROM races ra
        LEFT JOIN results re ON ra.raceid = re.raceid AND re.positionOrder = 1
        LEFT JOIN drivers d ON re.driverid = d.driverid
        WHERE ra.year = ? 
        ORDER BY ra.round ASC
    """
        
    df = pd.read_sql(query, conn, params=(anno_scelto,))
            
    if not df.empty:
        st.success(f"Trovate {len(df)} gare per la stagione {anno_scelto}!")
        st.dataframe(df, hide_index=True) 
    else:
        st.warning(f"Nessuna gara trovata per il {anno_scelto}.")

def insertpage(conn):
    insert=st.selectbox("What do you want to insert? ",["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])

    match insert:
        case "Drivers":
            new_driver(conn)
        case "Circuits":
            print("")
        case "Constructors":
            print("")

        case "Races":
            print("")

        case "Results":
            print("")
        
        case "Status":
            print("")

def modifypage(conn):
    st.subheader("Which table do you want to modify?")
    insert=st.selectbox("", ["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])
    match insert:
        case "Drivers":
            alter_driver(conn)
        case "Circuits":
            print("")

        case "Constructors":
            print("")

        case "Races":
            print("")

        case "Results":
            print("")
        
        case "Status":
            print("")

def deletepage(conn):
    st.subheader("Which table do you want to delete data from?")
    insert=st.selectbox("", ["Drivers", "Circuits", "Constructors", "Races", "Results", "Status"])
    match insert:
        case "Drivers":
            delete_driver(conn)
        case "Circuits":
            print("")

        case "Constructors":
            print("")

        case "Races":
            print("")

        case "Results":
            print("")
        
        case "Status":
            print("")

match sidebar:
    case "Search circuits":
        print("ciao")
    case "Insert new data":
        insertpage(conn)
    case "Modify data":
        modifypage(conn)
    case "Delete data":
        deletepage(conn)
    case "Yearly schedule":
        yearly_schedule(conn)