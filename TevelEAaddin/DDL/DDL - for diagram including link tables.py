import win32com.client
from All import *

import os

def create_diagram_link_tables(repository):
    
    flag_db2name = False
    link_table_name = ""
    start_table_name = ""
    end_table_name = ""
    table_script = ""
    cur_diagram = get_selected_diagram(repository)

    if cur_diagram is not None:
        if not os.path.exists("C:\\Temp"):
            os.makedirs("C:\\Temp")

        for cur_link in cur_diagram.DiagramLinks:
            flag_db2name = False
            cur_connector = repository.GetConnectorByID(cur_link.ConnectorID)
            if cur_connector.Stereotype.lower() != "link table":
                continue

            for con_tag_value in cur_connector.TaggedValues:
                if con_tag_value.Name.lower() == "db2name":
                    link_table_name = con_tag_value.Value
                    flag_db2name = True
                    break

            if not flag_db2name:
                link_table_name = "NO_DB2Name"

            cur_end_object = repository.GetElementByID(cur_connector.ClientID)
            cur_start_object = repository.GetElementByID(cur_connector.SupplierID)

            if cur_end_object.TaggedValues.GetByName("DB2Name") is not None:
                start_table_name = cur_end_object.TaggedValues.GetByName("DB2Name").Value
                if len(start_table_name) > 30:
                    start_table_name = "???" + start_table_name
            else:
                continue

            if cur_start_object.TaggedValues.GetByName("DB2Name") is not None:
                end_table_name = cur_start_object.TaggedValues.GetByName("DB2Name").Value
                if len(end_table_name) > 30:
                    end_table_name = "???" + end_table_name
            else:
                continue

            table_script = "CREATE TABLE " + link_table_name + "\n"
            table_script += "(\n \t \t " + start_table_name + ",\n"
            table_script += " \t \t " + end_table_name + "\n)"
            link_table_name = link_table_name.strip()
            with open("C:\\Temp\\" + link_table_name + ".sql", "w") as f:
                f.write(table_script)

def create_ddl_for_diagram_and_links(repository):
    create_diagram_ddl_function(repository)  # create DDL for the selected diagram
    create_diagram_link_tables(repository)   # create link tables for selected diagram

def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    create_ddl_for_diagram_and_links(repository)

if __name__ == "__main__":
    main()
