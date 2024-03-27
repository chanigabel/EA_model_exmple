import win32com.client
import datetime
import os
from All import *

def create_ddl_script_single_file(rep, selected_element, table_script):
    table_name = ""
    flag_db2_name = False

    # Find DB2Name tagged value
    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":  # Check if the current tag is DB2Name
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        table_script = loop_by_attributes(rep, selected_element, table_script)
    else:
        print(f"Warning: Could not create file for the {selected_element.Name} class because it does not have the 'DB2Name' tagged value.")

def create_diagram_ddl_single_file(repository):
    table_script = ""
    cur_diagram = get_selected_diagram(repository)

    if cur_diagram:  # check if any diagram is selected
        # check if directory exists
        if not os.path.exists("C:\\Temp"):
            os.makedirs("C:\\Temp")

        # create file for the ddl script
        # the file name is the selected diagram name + date
        cur_date = datetime.date.today().strftime("%Y%m%d")
        file_name = fr"C:\Temp\{cur_diagram.Name} {cur_date}.sql"

        # check if file exists
        if os.path.exists(file_name):
            os.remove(file_name)

        for cur_object in cur_diagram.DiagramObjects:  # loop on all diagram objects
            table_script = ""
            sel_element = repository.GetElementByID(cur_object.ElementID)
            if sel_element.Type == "Class":  # check if the object is a class
                create_ddl_script_single_file(repository, sel_element, table_script)  # create script for all the diagram's tagged value
                table_script += "\n\n"
                with open(file_name, "a") as file:
                    file.write(table_script)  # create the file

        print("Done")

def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    create_diagram_ddl_single_file(repository)

if __name__ == "__main__":
    main()
