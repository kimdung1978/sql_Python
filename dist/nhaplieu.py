import PySimpleGUI as sg
import pyodbc

# Function to retrieve data from the database
def get_table_data():
    # Establish the connection
    cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
                          SERVER=Thuan-Nguyen; \
                          Database=sql; UID=hoa; PWD=123;')
    cursor = cnx.cursor()

    # Query to fetch data
    cursor.execute('SELECT Id, Name, Gender, Department, City FROM nam')
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    cnx.close()

    # Convert data to list of lists
    data_list = [list(row) for row in data]
    return data_list

# Function to save new data to the database
def save_to_database(Id, Name, Gender, Department, City):
    # Establish the connection
    cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
                          SERVER=Thuan-Nguyen; \
                          Database=sql; UID=hoa; PWD=123;')
    cursor = cnx.cursor()

    # Insert new data
    cursor.execute('INSERT INTO nam (Id, Name, Gender, Department, City) VALUES (?, ?, ?, ?, ?)',
                   (Id, Name, Gender, Department, City))

    # Commit the transaction
    cnx.commit()

    # Close the connection
    cursor.close()
    cnx.close()

# Function to update existing data in the database
def update_database(Id, Name, Gender, Department, City):
    # Establish the connection
    cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
                          SERVER=Thuan-Nguyen; \
                          Database=sql; UID=hoa; PWD=123;')
    cursor = cnx.cursor()

    # Update existing data
    cursor.execute('UPDATE nam SET Name = ?, Gender = ?, Department = ?, City = ? WHERE Id = ?',
                   (Name, Gender, Department, City, Id))

    # Commit the transaction
    cnx.commit()

    # Close the connection
    cursor.close()
    cnx.close()

# Function to delete data from the database
def delete_from_database(Id):
    # Establish the connection
    cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
                          SERVER=Thuan-Nguyen; \
                          Database=sql; UID=hoa; PWD=123;')
    cursor = cnx.cursor()

    # Delete data
    cursor.execute('DELETE FROM nam WHERE Id = ?', (Id,))

    # Commit the transaction
    cnx.commit()

    # Close the connection
    cursor.close()
    cnx.close()

# Function to clear input fields
def clear_input_fields(window):
    window["ID"].update("")
    window["Name"].update("")
    window["City"].update("")
    window["g1"].update(True)
    window["g2"].update(False)

# Function to set up and run the main application window
def main():
    # Retrieve data and set up table headers
    table_data = get_table_data()
    table_header = ["ID", "Name", "Gender", "Department", "City"]

    sg.theme("GreenMono")

    layout = [
        [sg.Text("Enter Employee Information", background_color="Green",
                 text_color="Yellow", justification="left")],
        [sg.Text('Emp ID', size=(10, 1)), sg.Input(key="ID", size=(61, 4)),
         sg.Text('Department', size=(11, 1)),
         sg.Combo(['Hành Chính', 'Kỹ thuật kiểm tra giám sát', 'Kế hoạch tài chính', 'Truyền thông'],
                  key='Department', size=(58, 5))],
        [sg.Text("Emp Name", size=(10, 1)), sg.Input(key="Name", size=(61, 2)),
         sg.Text("City", size=(10, 1)), sg.Input(key="City", size=(60, 2))],
        [sg.Text('Gender', size=(10, 1)), sg.Radio("Male", "g", True, key="g1"),
         sg.Radio("Female", "g", key="g2")],
        [sg.Button('Save and Add New', key="SaveAddNew"), sg.Button('Update', key="Update"),
         sg.Button('Delete', key="Delete"), sg.Button('Exit', key="Exit")],
        [
            sg.Table(
                values=table_data,
                headings=table_header,
                key="Table",
                row_height=30,
                justification="center",
                expand_x=True,
                expand_y=True,
                enable_events=True,  # Enable events for row selection
                select_mode=sg.TABLE_SELECT_MODE_BROWSE  # Only one row can be selected
            )
        ],
        [sg.Text('Search by Name:'), sg.Input(key='search_input'), sg.Button('Search', key='search')]
    ]

    window = sg.Window("Employee Information", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "SaveAddNew":
            Id = values["ID"]
            Name = values["Name"]
            Department = values["Department"]
            City = values["City"]
            Gender = "Nam" if values["g1"] else "Nữ"

            # Save the new data to the database
            save_to_database(Id, Name, Gender, Department, City)

            # Update the table data
            table_data = get_table_data()
            window["Table"].update(values=table_data)

            # Clear input fields if not saving temporarily
            if event != "SaveTemp":
                clear_input_fields(window)
        elif event == "Update":
            if values["Table"]:  # Check if any row is selected
                selected_row = values["Table"][0]  # Get the index of the selected row
                selected_data = table_data[selected_row]  # Get the data of the selected row

                Id = selected_data[0]
                Name = values["Name"]
                Department = values["Department"]
                City = values["City"]
                Gender = "Nam" if values["g1"] else "Nữ"

                # Update the data in the database
                update_database(Id, Name, Gender, Department, City)

                # Update the table data
                table_data = get_table_data()
                window["Table"].update(values=table_data)
        elif event == "Delete":
            if values["Table"]:  # Check if any row is selected
                selected_row = values["Table"][0]  # Get the index of the selected row
                selected_data = table_data[selected_row]  # Get the data of the selected row

                Id = selected_data[0]

                # Delete the data from the database
                delete_from_database(Id)

                # Update the table data
                table_data = get_table_data()
                window["Table"].update(values=table_data)
        elif event == "Table":
            if values["Table"]:  # Check if any row is selected
                selected_row = values["Table"][0]  # Get the index of the selected row
                selected_data = table_data[selected_row]  # Get the data of the selected row

                # Populate the input fields with the selected data
                window["ID"].update(selected_data[0])
                window["Name"].update(selected_data[1])
                window["Department"].update(selected_data[3])
                window["City"].update(selected_data[4])
                if selected_data[2] == "Nam":
                    window["g1"].update(True)
                else:
                    window["g2"].update(True)
        elif event == 'search':
            search_term = values['search_input']
            if search_term.strip() != '':
                filtered_data = [row for row in table_data if search_term.lower() in row[1].lower()]
                window['Table'].update(values=filtered_data)
            else:
                window['Table'].update(values=table_data)

    window.close()

if __name__ == "__main__":
    main()
