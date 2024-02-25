import win32com.client
import xml.etree.ElementTree as ET
import sys

# Create a COM object for Enterprise Architect
ea = win32com.client.Dispatch("EA.App")

def main(project_path):
    # Get the repository of the specified EA project
    repository = ea.Repository
    repository.OpenFile(project_path)
    
    # Define your SQL query
    sql_query = "SELECT * FROM t_connector"
    
    # Execute the SQL query
    result_set = repository.SQLQuery(sql_query)
    
        # Parse the XML result set
    root = ET.fromstring(result_set)

    # Iterate over the rows and print Connector_ID values
    for row in root.findall(".//Row"):
        connector_id = row.find("Connector_ID").text
        print("Connector_ID:", connector_id)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <EA_project_path>")
    else:
        project_path = sys.argv[1]
        main(project_path)
