import win32com.client
import xml.etree.ElementTree as ET

# Create a COM object for Enterprise Architect
ea = win32com.client.Dispatch("EA.App")

# Get the currently active EA repository
repository = ea.Repository

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
