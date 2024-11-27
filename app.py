import streamlit as st
import pandas as pd
import os


# Function to load data from CSV or create new DataFrame
#If condition excute if the CSV is Already Presents
def load_data():
    if os.path.exists('main_table.csv'):
        # Load data from CSV if file exists
        main_table = pd.read_csv('main_table.csv')
        employee_list = pd.read_csv('employee_list.csv')
        project_list = pd.read_csv('project_list.csv')
    else:
        ###if the Data/CSV Not Present Intially,it will execute
        # Initialize default DataFrames if no CSV file found
        main_table = pd.DataFrame({
            'Week Day': [1, 1, 1, 2, 2],
            'Employee': ['Ram', 'Laxman', 'Ram', 'Charan', 'Laxman'],
            'Project': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
            'Time(in hours)': [50, 60, 50, 80, 40]
        })

        employee_list = pd.DataFrame({
            'Name': ['Ram', 'Laxman', 'Charan'],
            'Position': ['Manager', 'Developer', 'Analyst'],
            'Skills': ['Python, ML', 'Java, SQL', 'R, Analytics'],
            'CurrentStatus': ['Active', 'Active', 'Active']
        })

        project_list = pd.DataFrame({
            'Project': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
            'Description': ['Analysis', 'Development', 'Testing', 'Reporting', 'Design'],
            'StartDate': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01'],
            'Expected to Complete(Weeks)': [4, 6, 8, 3, 5],
            'Internal/External': ['Internal', 'External', 'Internal', 'External', 'Internal'],
            'Status': ['Active', 'Completed', 'On Hold', 'Active', 'Active']
        })

    return main_table, employee_list, project_list

#Function to save data to CSV
#This will save the tables
def save_data(main_table, employee_list, project_list):
    main_table.to_csv('main_table.csv', index=False)
    employee_list.to_csv('employee_list.csv', index=False)
    project_list.to_csv('project_list.csv', index=False)


# Load data (from CSV or default values)
main_table, employee_list, project_list = load_data()

##################################################################################################################################33
# Streamlit Appication
st.title("🏢Employee Work Tracker")

# Selectbox to choose between adding details or viewing analysis
choice = st.selectbox("Choose the action:", ["Task Tracker Table", "Add Details To Tables", "Utilization Analysis (O/P)"])

if choice == "Task Tracker Table":
    # Display the 3 tables: Main Table, Employee List, Project List
    #make the main table as ->Task Tracker Table
    st.header("Task Tracker Table")
    st.dataframe(main_table)

    st.header("Employee List")
    st.dataframe(employee_list)

    st.header("Project List")
    st.dataframe(project_list)

elif choice == "Add Details To Tables":
    # Sidebar for adding new employee, project, or work entry
    st.sidebar.header("Add New Employee")
    employee_name = st.sidebar.text_input("Enter Employee Name:")
    employee_position = st.sidebar.text_input("Enter Employee Position:")
    employee_skills = st.sidebar.text_input("Enter Employee Skills (comma separated):")
    employee_status = st.sidebar.selectbox("Select Employee Status:", ["Active", "Inactive"])

    if st.sidebar.button("Add New Employee"):
        if employee_name not in employee_list['Name'].values:
            new_employee = {
                'Name': employee_name,
                'Position': employee_position,
                'Skills': employee_skills,
                'CurrentStatus': employee_status
            }
            employee_list = pd.concat([employee_list, pd.DataFrame([new_employee])], ignore_index=True)
            save_data(main_table, employee_list, project_list)  # Save updated data to CSV
            st.sidebar.success(f"New employee '{employee_name}' added successfully!")
        else:
            st.sidebar.warning(f"Employee '{employee_name}' already exists!")

    # Sidebar for adding a new project Details
    st.sidebar.header("Add New Project")
    project_name = st.sidebar.text_input("Enter Project Name:")
    project_description = st.sidebar.text_input("Enter Project Description:")
    project_start_date = st.sidebar.date_input("Enter Start Date:", value=pd.to_datetime('2024-01-01'))
    project_exp_weeks = st.sidebar.number_input("Enter Expected Weeks:", min_value=1)
    project_status = st.sidebar.selectbox("Select Project Status:", ["Active", "Completed", "On Hold"])
    project_type = st.sidebar.selectbox("Select Project Type (Internal/External):", ["Internal", "External"])

    if st.sidebar.button("Add New Project"):
        if project_name not in project_list['Project'].values:
            new_project = {
                'Project': project_name,
                'Description': project_description,
                'StartDate': project_start_date,
                'Expected to Complete(Weeks)': project_exp_weeks,
                'Internal/External': project_type,
                'Status': project_status
            }
            project_list = pd.concat([project_list, pd.DataFrame([new_project])], ignore_index=True)
            save_data(main_table, employee_list, project_list)  # Save updated data to CSV
            st.sidebar.success(f"New project '{project_name}' added successfully!")
        else:
            st.sidebar.warning(f"Project '{project_name}' already exists!")

    # Sidebar for adding a new work entry Details
    st.sidebar.header("Add Employee Work Details")
    employee_name_work = st.sidebar.text_input("Enter Employee Name for Work Entry:")
    project_name_work = st.sidebar.text_input("Enter Project Name for Work Entry:")
    week_number = st.sidebar.number_input("Enter Week Number:", min_value=1, step=1)
    percent_time = st.sidebar.number_input("Enter % Time Allocation:", min_value=0, max_value=100, step=1)

    if st.sidebar.button("Add Work Entry"):
        if employee_name_work not in employee_list['Name'].values:
            st.sidebar.error("Employee not found in Employee List. Please add the Employee Details first.")
        elif project_name_work not in project_list['Project'].values:
            st.sidebar.error("Project not found in Project List. Please add it to the Project List first.")
        else:
            new_entry = {
                'Week Day': week_number,
                'Employee': employee_name_work,
                'Project': project_name_work,
                'Time(in hours)': percent_time
            }
            main_table = pd.concat([main_table, pd.DataFrame([new_entry])], ignore_index=True)
            save_data(main_table, employee_list, project_list)  # Save updated data to CSV
            st.sidebar.success("Work entry added successfully!")

elif choice == "Utilization Analysis (O/P)":
    # Generate Output Table using Pivot Table
    output = main_table.pivot_table(
        index='Employee',
        columns='Project',
        values='Time(in hours)'
    ).fillna(0)

 
    ####################################33
    st.header("Output Table (Utilization Analysis)")
    st.dataframe(output)

    # Option to download the Output Table as CSV
    st.download_button(
        label="Download Output Table as CSV",
        data=output.to_csv(index=False),
        file_name='output_table.csv',
        mime='text/csv'
    )
