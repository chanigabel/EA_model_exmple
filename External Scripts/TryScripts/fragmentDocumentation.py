import os
import sys
import win32com.client

# Define constants
ACTOR_TEMPLATE = "Model Report"
USECASE_TEMPLATE = "Use Case Details"
CONNECTOR_TEMPLAT="Connectors"
DOCUMENTATION_TYPE = 0  # RTF
OUTPUT_FILE = "C:\\Users\\ch058\\OneDrive\\שולחן העבודה\\DocumentationExample.rtf"

def documentation():
    # Create a COM object for Enterprise Architect
    ea = win32com.client.Dispatch("EA.App")
    
    # Show the script output window
    ea.Repository.EnsureOutputVisible("Script")

    # Get the currently selected package in the Project Browser
    current_package = ea.Repository.GetTreeSelectedPackage()
    
    if current_package:
        # Create a document generator object
        doc_generator = ea.Repository.CreateDocumentGenerator()
        
        # Create a new document
        if doc_generator.NewDocument(""):
            generation_success = False
            
            # Insert table of contents
            doc_generator.InsertText("Table of Contents", 0)
            generation_success = doc_generator.InsertTableOfContents()
            if not generation_success:
                report_warning("Error inserting Table of Contents: " + doc_generator.GetLastError())
            
            # Insert page break
            doc_generator.InsertBreak(1)
            
            # Iterate over all actors under the currently selected package
            package_elements = current_package.Elements
            for i in range(package_elements.Count):
                # Get the current element
                current_element = package_elements.GetAt(i)
                
                # if current_element.Type != None:
                #     # Generate documentation
                #     report_info("Generating documentation for: " + current_element.Name)
                #     generation_success = doc_generator.DocumentElement(current_element.ElementID, 0, ACTOR_TEMPLATE)
                #     if not generation_success:
                #         report_warning("Error generating Class documentation: " + doc_generator.GetLastError())
                    
                # Generate documentation for all Use Cases connected to the current actor
                element_connectors = current_element.Connectors
                for j in range(element_connectors.Count):
                    # Get the current connector and the element that it connects to
                    current_connector = element_connectors.GetAt(j)
                    connected_element = ea.Repository.GetElementByID(current_connector.SupplierID)
                    
                    if connected_element.Type == "Sequence":
                        # Generate Use Case documentation
                        report_info("Generating documentation for connected Sequence: " + connected_element.Name)
                        generation_success = doc_generator.DocumentElement(connected_element.ElementID, 1, CONNECTOR_TEMPLAT)
                        if not generation_success:
                            report_warning("Error generating Sequence documentation: " + doc_generator.GetLastError())
            else:
                report_info("Skipping element " + current_element.Name + " - not an Sequence")
        
            # Save the document
            save_success = doc_generator.SaveDocument(OUTPUT_FILE, DOCUMENTATION_TYPE)
            if save_success:
                report_info("Documentation complete!")
            else:
                report_warning("Error saving file: " + doc_generator.GetLastError())
        else:
            report_fatal("Could not create new document: " + doc_generator.GetLastError())
    else:
        report_fatal("This script requires a package to be selected in the Project Browser.\n" +
                     "Please select a package in the Project Browser and try again.")
    
    report_info("Done!")

def report_info(message):
    print("[INFO] " + message)

def report_warning(message):
    print("[WARNING] " + message)

def report_fatal(message):
    print("[FATAL] " + message)
    print(message)

documentation()
