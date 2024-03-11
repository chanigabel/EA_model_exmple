import os
import sys
import win32com.client
import xml.etree.ElementTree as ET

# Define constants
DOCUMENTATION_TYPE = 0  # RTF
def read_sql_query(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
    return sql_query

# Define the path to the SQL file
sql_file_path = os.path.join(os.path.dirname(__file__), 'query.sql')
DIAGRAM_TEMPLATE = "Model Report"
CONNECTOR_TEMPLATE="ConnectorMessages"
OBJECT_TEMPLATE="Child Elements"

def documentation_example(model_file_path,file_path_save):
    # Create a COM object for Enterprise Architect
    ea = win32com.client.Dispatch("EA.App")
    # Get the currently active EA repository
    repository = ea.Repository
    repository.OpenFile(model_file_path)
    # Show the script output window
    sql_query = read_sql_query(sql_file_path)
    
    # Execute the SQL query
    result_set = repository.SQLQuery(sql_query)

    # Parse the XML result set
    root = ET.fromstring(result_set)

    # Check if connectors are available
    rows = root.findall(".//Row")
    if not rows:
        report_info("No connectors found in the model.")
        return

    # Create a document generator object
    doc_generator = repository.CreateDocumentGenerator()
    if doc_generator.NewDocument(""):
        generation_success = False

        generation_success = doc_generator.InsertTableOfContents()
        if not generation_success:
            report_warning("Error inserting Table of Contents: " + doc_generator.GetLastError())

        # Insert page break
        doc_generator.InsertBreak(1)

        # Iterate over the rows and print Connector_ID values
        for row in rows:
            Diagram_ID = row.find("Diagram_ID").text
            Name = row.find("Name").text
            Connector_ID = row.find("Connector_ID").text
            Connector_Type = row.find("Connector_Type").text
            Message = row.find("Massege").text
            Source_Object_ID = row.find("Source_Object_ID").text
            Source_Object_Package = row.find("Source_Object_Packeg").text
            Target_Object_ID = row.find("Target_Object_ID").text
            Target_Object_Package = row.find("Target_Object_Packeg").text
            FromMethod = row.find("FromMathod").text
            # Add the extracted information to the document
            doc_generator.InsertText(
            "Diagram ID: {} Diagram Name: {} Connector ID: {} Connector Type: {} Message: {} "
            "Source Object ID: {} Source Object Package: {} Target Object ID: {} Target Object Package: {} "
            "From Method: {}".format(
            Diagram_ID, Name, Connector_ID, Connector_Type, Message,
            Source_Object_ID, Source_Object_Package, Target_Object_ID, Target_Object_Package, FromMethod
            ),0)

            # Source_Object = ea.Repository.GetElementByID(Source_Object_ID)
            # # Retrieve the Object_ID attribute from Source_Object
            # Source_Object_ID = Source_Object.Object_ID

            # # Generate documentation for the Source_Object
            # generation_success = doc_generator.DocumentElement(Source_Object_ID, 0, OBJECT_TEMPLATE)
            # if not generation_success:
            #     report_warning("Error generating Object documentation: " + doc_generator.GetLastError())


            # element={ Diagram_ID, Name, Connector_ID, Connector_Type, Message,
            # Source_Object_ID, Source_Object_Package, Target_Object_ID, Target_Object_Package, FromMethod}

             
            # generation_success = doc_generator.DocumentElement(Diagram_ID, 0,DIAGRAM_TEMPLATE)
            # if not generation_success:
            #     report_warning("Error generating Diagram documentation: " + doc_generator.GetLastError())
            # Insert page break after each connector's information
            doc_generator.InsertBreak(1)

        # Save the document
        output_file = os.path.join(os.path.dirname(__file__), file_path_save)
        save_success = doc_generator.SaveDocument(output_file, DOCUMENTATION_TYPE)
        if save_success:
            report_info("Documentation complete!")
        else:
            report_warning("Error saving file: " + doc_generator.GetLastError())
    else:
        report_fatal("Could not create new document: " + doc_generator.GetLastError())

    print("Done!")

def report_info(message):
    print("[INFO] " + message)

def report_warning(message):
    print("[WARNING] " + message)

def report_fatal(message):
    print("[FATAL] " + message)
    print(message, 0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <model_file_path>")
        sys.exit(1)
    model_file_path = sys.argv[1]
    if(len(sys.argv) == 3):
        file_path_save= sys.argv[2]
    else:
        file_path_save="DocumentationExample.rtf"
    documentation_example(model_file_path,file_path_save)
