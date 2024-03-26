import os
import xml.etree.ElementTree as ET
from generalFunction import *

def add_attribute_from_period_class(rep, attribute_type, table_script):
    print("innnnn")
    period_element = None
    # Construct the SQL query to retrieve the Object_ID of the period class
    squery = f"SELECT Object_ID FROM t_object WHERE Name = '{attribute_type}'"
    # Execute the SQL query and get the result
    result = select_statement(squery, rep)
    root = result.getroot()

    # Check if the Object_ID of the period class is found
    if root.findall(".//Object_ID"):
        element_id = root.findall(".//Object_ID")[0].text
        period_element = rep.GetElementByID(int(element_id))

        # Iterate through all attributes of the period class
        for current_attribute in period_element.Attributes:
            # Check if the attribute's stereotype is greater than or equal to "JPA"
            if current_attribute.Stereotype >= "JPA":
                continue
            # Check if the attribute has a tagged value named "DB2ColumnName"
            if "DB2ColumnName" in [tag.Name for tag in current_attribute.TaggedValues]:
                # Get the value of the "DB2ColumnName" tagged value
                tag_val = next((tag.Value for tag in current_attribute.TaggedValues if tag.Name == "DB2ColumnName"), None)
                attr_name = tag_val.strip() if tag_val else ""

                # Check if the attribute type does not contain "list", "map", or "charColl"
                if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                    table_script += attr_name + " "
                    print(table_script)
                    # Check if the attribute name contains "_ID"
                    if "_ID" in attr_name:
                        table_script += "INTEGER"
                        print(table_script)
                    else:
                        table_script = define_db2_type(current_attribute, table_script)

                    # Check for NULL constraints in the tagged values
                    if "NULL=TRUE" in [tag.Name for tag in current_attribute.TaggedValues]:
                        table_script += " NULL"
                        print(table_script)
                    elif "NULL=FALSE" in [tag.Name for tag in current_attribute.TaggedValues]:
                        table_script += " NOT NULL"
                        print(table_script)

                    table_script += ",\n \t \t "

    return table_script

def add_attribute_from_embed_class(rep, attribute_type, table_script):
    emb_element = None
    # Construct the SQL query to retrieve the Object_ID of the embedded class
    squery = f"SELECT Object_ID FROM t_object WHERE Name = '{attribute_type}'"
    # Execute the SQL query and get the result
    result = select_statement(squery, rep)
    root = result.getroot()

    # Check if the Object_ID of the embedded class is found
    if root.findall(".//Object_ID"):
        element_id = root.findall(".//Object_ID")[0].text
        emb_element = rep.GetElementByID(int(element_id))

        # Iterate through all attributes of the embedded class
        for current_attribute in emb_element.Attributes:
            # Check if the attribute has a tagged value named "DB2ColumnName"
            if is_tagged_value_exist(current_attribute, "DB2ColumnName"):
                # Check if the attribute's stereotype is greater than or equal to "JPA"
                if current_attribute.Stereotype >= "JPA":
                    continue
                # Check if the attribute's type contains "PeriodEntity"
                if "PeriodEntity" in current_attribute.Type:
                    table_script = add_attribute_from_period_class(rep, current_attribute.Type, table_script)
                    continue
                
                # Get the value of the "DB2ColumnName" tagged value
                tag_val = next((tag.Value for tag in current_attribute.TaggedValues if tag.Name == "DB2ColumnName"), None)
                attr_name = tag_val.strip() if tag_val else ""

                # Check if the attribute type does not contain "list", "map", or "charColl"
                if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                    table_script += attr_name + " "
                    print(table_script)
                    # Check if the attribute name contains "_ID"
                    if "_ID" in attr_name:
                        table_script += "INTEGER"
                        print(table_script)
                    else:
                        table_script = define_db2_type(current_attribute, table_script)

                    # Check for NULL constraints in the tagged values
                    if "NULL=TRUE" in [tag.Name for tag in current_attribute.TaggedValues]:
                        table_script += " NULL"
                        print(table_script)
                    elif "NULL=FALSE" in [tag.Name for tag in current_attribute.TaggedValues]:
                        table_script += " NOT NULL"
                        print(table_script)

                    table_script += ",\n \t \t "

    return table_script 

def get_single_table_relation_class(rep, single_element, table_script):
    # Iterate through all attributes of the single element
    for current_attribute in single_element.Attributes:
        # Check if the current attribute has a tagged value named "DB2ColumnName"
        if is_tagged_value_exist(current_attribute, "DB2ColumnName"):
            # Check if the attribute's stereotype is greater than or equal to "JPA"
            if current_attribute.Stereotype >= "JPA":
                continue
            # Check if the attribute's stereotype contains "embed"
            if "embed" in current_attribute.Stereotype:
                print(current_attribute.Stereotype, "hhhhhhhhh")
                # Get the attribute type and add it to the table script
                table_script = add_attribute_from_embed_class(rep, current_attribute.Type, table_script)
                continue
            # Check if the attribute's type contains "PeriodEntity"
            if "PeriodEntity" in current_attribute.Type:
                table_script = add_attribute_from_period_class(rep, current_attribute.Type, table_script)
                continue
            
            # Get the value of the "DB2ColumnName" tagged value
            tag_val = next((tag.Value for tag in current_attribute.TaggedValues if tag.Name == "DB2ColumnName"), None)
            attr_name = tag_val.strip() if tag_val else ""
            
            # Check if the attribute type does not contain "list", "map", or "charColl"
            if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                table_script += attr_name + " "
                print(table_script)
                # Check if the attribute name contains "_ID"
                if "_ID" in attr_name:
                    table_script += "INTEGER"
                    print(table_script)
                else:
                    table_script = define_db2_type(current_attribute, table_script)
                
                # Check for NULL constraints in the tagged values
                if "NULL=TRUE" in [tag.Name for tag in current_attribute.TaggedValues]:
                    table_script += " NULL"
                    print(table_script)
                elif "NULL=FALSE" in [tag.Name for tag in current_attribute.TaggedValues]:
                    table_script += " NOT NULL"
                    print(table_script)

                table_script += ",\n \t \t "
    return table_script

def select_statement(squery, repository):
    # Execute the SQL query using the repository's SQLQuery method
    result = ET.ElementTree(ET.fromstring(repository.SQLQuery(squery)))
    return result

def check_class_parents(selected_element, repository, table_script):
    # Construct the SQL query to select parent objects
    squery = ("SELECT End_Object_ID FROM t_connector WHERE t_connector.Connector_Type='Generalization' " +
              "AND Connector_ID NOT IN (SELECT Connector_ID FROM t_connector " +
              "WHERE Stereotype like 'join%') AND Start_Object_ID = " + str(selected_element.ElementID))
    
    # Execute the query to get the results
    result = select_statement(squery, repository)
    root = result.getroot()
    list_class_ids = root.findall(".//End_Object_ID")

    # Check if any parent class IDs are found
    if list_class_ids:
        # Iterate over each parent class ID
        for class_id in list_class_ids:
            # Get the parent class ID
            parent_class_id = class_id.text
            # Get the parent element using the repository
            parent_element = repository.GetElementByID(int(parent_class_id))
            print("parent_element", parent_element.Name)
            # Call the function to handle single table relation class for the parent element
            table_script = get_single_table_relation_class(repository, parent_element, table_script)
            # Recursively call the function for checking parent elements
            return check_class_parents(parent_element, repository, table_script)
    
    return table_script

def find_base_entity_for_join_table(selected_element, rep, squery, table_script):
    # Append the selected element's ID to the SQL query
    squery = squery + str(selected_element.ElementID)
    # Execute the query to get the results
    result = select_statement(squery, rep)
    root = result.getroot()
    list_class_ids = root.findall(".//End_Object_ID")

    # Check if any class IDs are found
    if list_class_ids:
        # If class IDs are found, iterate over each one
        for class_id in list_class_ids:
            # Add an ID column to the table script
            table_script += "ID INTEGER NOT NULL," + "\n \t \t "
    else:
        return table_script
    
    return table_script

def check_class_relations(selected_element, rep, table_script):
    # Construct the SQL query to retrieve information about class relations
    squery = ("SELECT Start_Object_ID FROM t_connector WHERE STEREOTYPE='single_table' " +
              "AND End_Object_ID = " + str(selected_element.ElementID))
    
    # Execute the query to get the results
    result = select_statement(squery, rep)
    root = result.getroot()
    list_class_ids = root.findall(".//Start_Object_ID")
    
    ind = 0
    # Check if there are any class relations found
    if list_class_ids:
        # Iterate over each class ID found in the results
        for class_id in list_class_ids:
            single_table_class_name = class_id.text
            # Assuming `get_single_table_relation_class` is defined elsewhere
            # Get information about single table relation class and update the table script
            table_script = get_single_table_relation_class(rep, rep.GetElementByID(int(single_table_class_name)), table_script)
            ind += 1
    return table_script

def create_source_class_foreign_key(selected_element, rep, table_script):
    # Construct the SQL query to retrieve information about foreign keys
    squery = (
        "SELECT SourceCard, DestCard, t_objectproperties.Value AS 'EndTableTagVal' FROM  t_connector, t_object, t_objectproperties "
        "WHERE t_object.Object_ID = t_connector.End_Object_ID and t_object.Object_ID = t_objectproperties.Object_ID "
        "AND t_objectproperties.Property like 'DB2Name' AND SourceCard is not null AND DestCard IS NOT NULL AND Start_Object_ID = "
        + str(selected_element.ElementID)
    )
    # Execute the query to get the results
    result = select_statement(squery, rep)
    root = result
    # Extract necessary information from the query results
    list_object_names = root.findall(".//EndTableTagVal")
    list_source_multiplicity = root.findall(".//SourceCard")
    list_target_multiplicity = root.findall(".//DestCard")

    index = 0
    # Iterate over each foreign key entry
    for cur_multiplicity in list_source_multiplicity:
        multiplicity_source_type = cur_multiplicity.find(".//SourceCard").text
        multiplicity_target_type = list_target_multiplicity[index].text
        # Check if the multiplicity target type meets the condition for a foreign key
        if check_multiplicity_type(multiplicity_target_type) >= "1":
            # Check if the selected element has a DB2Name tagged value
            if selected_element.TaggedValues.GetByName("DB2Name"):
                # Construct the foreign key name based on DB2Name and object names
                tag_val = selected_element.TaggedValues.GetByName("DB2Name").Value
                table_script += f"FK_{tag_val[:4]}_{list_object_names[index].text[:4]},\n \t \t "
                print(table_script)
        index += 1
    return table_script

def create_target_class_foreign_key(selected_element, rep, table_script):
    # Construct the SQL query to retrieve information about foreign keys
    squery = (
        "SELECT SourceCard, DestCard, t_objectproperties.Value AS 'StartTableTagVal' FROM  t_connector, t_object, t_objectproperties "
        "WHERE t_object.Object_ID = t_connector.Start_Object_ID AND t_object.Object_ID = t_objectproperties.Object_ID "
        "AND t_objectproperties.Property like 'DB2Name' AND SourceCard is not null AND t_connector.DestIsNavigable=0 "
        "AND DestCard IS NOT NULL AND End_Object_ID = "
        + str(selected_element.ElementID)
    )
    # Execute the query to get the results
    result = select_statement(squery, rep)
    root = result
    # Extract necessary information from the query results
    list_object_names = root.findall(".//StartTableTagVal")
    list_source_multiplicity = root.findall(".//SourceCard")
    list_target_multiplicity = root.findall(".//DestCard")

    index = 0
    # Iterate over each foreign key entry
    for cur_multiplicity in list_source_multiplicity:
        multiplicity_source_type = cur_multiplicity.find(".//SourceCard").text
        multiplicity_target_type = list_target_multiplicity[index].text
        # Check if the multiplicity source type meets the condition for a foreign key
        if check_multiplicity_type(multiplicity_source_type) >= "1":
            # Check if the selected element has a DB2Name tagged value
            if selected_element.TaggedValues.GetByName("DB2Name"):
                # Construct the foreign key name based on DB2Name and object names
                tag_val = selected_element.TaggedValues.GetByName("DB2Name").Value
                table_script += f"FK_{tag_val[:4]}_{list_object_names[index].text[:4]},\n \t \t "
                print(table_script)
        index += 1
    return table_script

def check_foreign_keys(selected_element, repository, table_script):
    # Add foreign keys from target classes
    table_script = create_target_class_foreign_key(selected_element, repository, table_script)
    # Add foreign keys from source classes
    table_script = create_source_class_foreign_key(selected_element, repository, table_script)
    # Return the updated table script with foreign keys
    return table_script

def loop_by_attributes(repository, selected_element, table_script):
    # Construct the SQL query to find base entities
    squery = (
        "SELECT End_Object_ID FROM t_connector WHERE t_connector.Connector_Type='Generalization' " +
        "AND Connector_ID IN (SELECT Connector_ID FROM t_connector " +
        "WHERE Stereotype like 'join%') AND Start_Object_ID = "
    )
    # Add indentation for the table script
    table_script += "(\n\t\t"  
    
    # Add fields from base entities
    table_script = check_class_parents(selected_element, repository, table_script)
    table_script = find_base_entity_for_join_table(selected_element, repository, squery, table_script)
    
    # Loop through attributes of the selected element
    for current_attribute in selected_element.Attributes:
        # Check if the current attribute has a DB2ColumnName tagged value
        if "DB2ColumnName" in [tag.Name for tag in current_attribute.TaggedValues]:
            # Check if the attribute stereotype is greater than or equal to "JPA"
            if current_attribute.Stereotype >= "JPA":
                continue
            # Check if the attribute is an embedded attribute
            if "embed" in current_attribute.Stereotype:
                table_script = add_attribute_from_embed_class(repository, current_attribute.Type, table_script)
                continue
            # Check if the attribute type is a PeriodEntity
            if "PeriodEntity" in current_attribute.Type:
                table_script = add_attribute_from_period_class(repository, current_attribute.Type, table_script)
                continue
            
            # Get the attribute name from the DB2ColumnName tagged value
            attr_name = next((tag.Value for tag in current_attribute.TaggedValues if tag.Name == "DB2ColumnName"), None)
            attr_name = attr_name.strip() if attr_name else ""
            
            # Check if the attribute type does not contain list, map, or charColl
            if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                table_script += attr_name + " "
                print(table_script)
                # Check if the attribute name contains "_ID"
                if "_ID" in attr_name:
                    table_script += "INTEGER"
                    print(table_script)
                else:
                    table_script = define_db2_type(current_attribute, table_script)
                
                # Check if the attribute allows NULL values
                if "NULL=TRUE" in [tag.Name for tag in current_attribute.TaggedValues]:
                    table_script += " NULL"
                    print(table_script)
                elif "NULL=FALSE" in [tag.Name for tag in current_attribute.TaggedValues]:
                    table_script += " NOT NULL"
                    print(table_script)

                # Add a comma and newline for the next attribute
                table_script += ",\n\t\t"
                print(table_script)

    # Check class relations and foreign keys
    table_script = check_class_relations(selected_element, repository, table_script)
    table_script = check_foreign_keys(selected_element, repository, table_script)
    
    # Remove the last comma from the script and add a closing bracket
    table_script = table_script.rstrip(",") + "\n)"
    print(table_script)
    return table_script

def create_ddl_script(repository, selected_element):
    table_script=""
    table_name = ""
    flag_db2name = False

    # find DB2Name tagged value
    for tagged_value in selected_element.TaggedValues:
        # Loop through all tagged values of the selected element
        if tagged_value.Name.lower() == "db2name": # Check if the tagged value is DB2Name
            table_name = tagged_value.Value.strip()# Get the table name
            table_script += f"CREATE TABLE {table_name}\n"
            flag_db2name = True
            break # Exit the loop once DB2Name tagged value is found

    if flag_db2name:  # If the element has a DB2Name tagged value
        directory = "C:\\Temp\\"
        if not os.path.exists(directory):  # Check if directory exists
            os.makedirs(directory)  # Create directory if it doesn't exist

        file_name = f"{directory}{table_name}.sql"  # Construct file name
        if not os.path.exists(file_name):  # Check if file doesn't exist
            # Write the create table script to the DDL file
            with open(file_name, "w") as file:
                file.write(loop_by_attributes(repository, selected_element, table_script))
        else:
            # Show a warning if the file already exists
            print("The file name already exists.", f"File Exists {table_name}")

    else:
        # Show a warning if the element doesn't have a DB2Name tagged value
        print(f"Could not create file for the {selected_element.Name} class because it does not have the 'DB2Name' tagged value.")

def create_diagram_ddl_function(repository):
    # Get the current selected diagram
    cur_diagram = get_selected_diagram(repository)
    
    # If there's a selected diagram
    if cur_diagram:
        # Iterate through each object in the diagram
        for cur_object in cur_diagram.DiagramObjects:
            sel_element = repository.GetElementByID(cur_object.ElementID)
            # If the element type is a class
            if sel_element.Type == "Class":
                # Create DDL script for the selected element
                create_ddl_script(repository, sel_element)
