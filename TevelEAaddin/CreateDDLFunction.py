def get_single_table_relation_class(rep, single_element, table_script):
    for current_attribute in single_element.Attributes:
        if current_attribute.GetTaggedValueByName("DB2ColumnName"):
            if current_attribute.Stereotype.lower() >= "jpa":
                continue
            if "embed" in current_attribute.Stereotype.lower():
                add_attribute_from_embed_class(rep, current_attribute.Type, table_script)
                continue
            if "periodentity" in current_attribute.Type.lower():
                add_attribute_from_period_class(rep, current_attribute.Type, table_script)
                continue
            attr_name = current_attribute.GetTaggedValueByName("DB2ColumnName").Value.strip()
            if "list" not in current_attribute.Type.lower() and "map" not in current_attribute.Type.lower() and "charcoll" not in current_attribute.Type.lower():
                table_script += f"{attr_name} "
                if "_id" in attr_name.lower():
                    table_script += "INTEGER"
                else:
                    define_db2_type(current_attribute, table_script)
                if current_attribute.GetTaggedValueByName("NULL=TRUE"):
                    table_script += " NULL"
                elif current_attribute.GetTaggedValueByName("NULL=FALSE"):
                    table_script += " NOT NULL"
                table_script += ",\n"

def check_class_parents(selected_element, rep, table_script):
    squery = f"SELECT End_Object_ID FROM t_connector WHERE t_connector.Connector_Type='Generalization' AND Connector_ID NOT IN (SELECT Connector_ID FROM t_connector WHERE Stereotype like 'join%') AND Start_Object_ID = {selected_element.ElementID}"
    result = connect_to_db.select_statement(squery)
    list_class_ids = result.SelectNodes("//End_Object_ID")
    if list_class_ids is not None:
        for class_id in list_class_ids:
            parent_class_id = class_id.SelectSingleNode("//End_Object_ID").InnerText
            parent_element = rep.GetElementByID(int(parent_class_id))
            get_single_table_relation_class(rep, parent_element, table_script)
            return check_class_parents(parent_element, rep, table_script)
    return None

def find_base_entity_for_join_table(selected_element, rep, squery, table_script):
    result = rep.SQLQuery(squery + str(selected_element.ElementID))
    list_class_ids = result.SelectNodes("//End_Object_ID")
    
    if list_class_ids is not None and list_class_ids.Count != 0:
        for class_id in list_class_ids:
            table_script += "ID INTEGER NOT NULL," + "\n \t \t "
    else:
        return

def add_attribute_from_embed_class(rep, attribute_type, table_script):
    squery = "SELECT Object_ID FROM t_object WHERE Name = '" + attribute_type + "'"
    result = connect_to_db.SelectStatement(squery)

    if result.SelectNodes("//Object_ID") is not None:
        element_id = result.SelectNodes("//Object_ID")[0].InnerText
        emb_element = rep.GetElementByID(int(element_id))
        
        for current_attribute in emb_element.Attributes:
            if general_function.IsTaggedValueExist(current_attribute, "DB2ColumnName"):
                if current_attribute.Stereotype >= "JPA":
                    continue
                if "PeriodEntity" in current_attribute.Type:
                    add_attribute_from_period_class(rep, current_attribute.Type, table_script)
                    continue
                tag_val = current_attribute.TaggedValues.GetByName("DB2ColumnName")
                attr_name = general_function.TrimStrings(tag_val.Value)
                
                if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                    table_script += attr_name + " "
                    
                    if "_ID" in attr_name:
                        table_script += "INTEGER"
                    else:
                        general_function.DefineDB2Type(current_attribute, table_script)
                    
                    if general_function.IsTaggedValueExist(current_attribute, "NULL=TRUE"):
                        table_script += " NULL"
                    elif general_function.IsTaggedValueExist(current_attribute, "NULL=FALSE"):
                        table_script += " NOT NULL"
                    
                    table_script += "," + "\n \t \t "

def add_attribute_from_period_class(rep, attribute_type, table_script):
    squery = "SELECT Object_ID FROM t_object WHERE Name = '" + attribute_type + "'"
    result = connect_to_db.SelectStatement(squery)
    element_id = result.SelectNodes("//Object_ID")[0].InnerText

    period_element = rep.GetElementByID(int(element_id))
    for current_attribute in period_element.Attributes:
        if current_attribute.Stereotype >= "JPA":
            continue
        if general_function.IsTaggedValueExist(current_attribute, "DB2ColumnName"):
            tag_val = current_attribute.TaggedValues.GetByName("DB2ColumnName")
            attr_name = general_function.TrimStrings(tag_val.Value)
            
            if "list" not in current_attribute.Type and "map" not in current_attribute.Type and "charColl" not in current_attribute.Type:
                table_script += attr_name + " "
                
                if "_ID" in attr_name:
                    table_script += "INTEGER"
                else:
                    general_function.DefineDB2Type(current_attribute, table_script)
                
                if general_function.IsTaggedValueExist(current_attribute, "NULL=TRUE"):
                    table_script += " NULL"
                elif general_function.IsTaggedValueExist(current_attribute, "NULL=FALSE"):
                    table_script += " NOT NULL"
                
                table_script += "," + "\n \t \t "

def loop_by_attributes(rep, selected_element, table_script):
    squery = "SELECT End_Object_ID FROM t_connector WHERE t_connector.Connector_Type='Generalization' " + \
             "AND Connector_ID IN (SELECT Connector_ID FROM t_connector " + \
             "WHERE Stereotype like 'join%') AND Start_Object_ID = "
    table_script += "(\n \t \t "
    
    # add fields from base entities
    check_class_parents(selected_element, rep, table_script)
    find_base_entity_for_join_table(selected_element, rep, squery, table_script)
    
    for current_attribute in selected_element.Attributes:
        if general_function.is_tagged_value_exist(current_attribute, "DB2ColumnName"):
            if current_attribute.Stereotype >= "JPA":
                continue
            if "embed" in current_attribute.Stereotype:
                # get attribute type
                add_attribute_from_embed_class(rep, current_attribute.Type, table_script)
                continue
            if "PeriodEntity" in current_attribute.Type:
                add_attribute_from_period_class(rep, current_attribute.Type, table_script)
                continue

            tag_val = current_attribute.TaggedValues.GetByName("DB2ColumnName")
            attr_name = general_function.trim_strings(tag_val.Value)

            if "list" not in current_attribute.Type and \
               "map" not in current_attribute.Type and \
               "charColl" not in current_attribute.Type:
                table_script += attr_name + " "
                # Check if the attribute is key with extension _ID
                if "_ID" in attr_name:
                    table_script += "INTEGER"
                else:
                    general_function.define_db2_type(current_attribute, table_script)

                if general_function.is_tagged_value_exist(current_attribute, "NULL=TRUE"):
                    table_script += " NULL"
                elif general_function.is_tagged_value_exist(current_attribute, "NULL=FALSE"):
                    table_script += " NOT NULL"

                table_script += ",\n \t \t "

    check_class_relations(selected_element, rep, table_script)
    check_foreign_keys(selected_element, rep, table_script)

    # Remove last comma from the script
    # Find last comma
    ind = table_script.rfind(',')
    if ind > 0:
        table_script = table_script[:ind]
    table_script += "\n)"
    return table_script

def create_ddl_script(rep, selected_element):
    table_name = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        loop_by_attributes(rep, selected_element, table_script)
    else:
        print("Missing Tagged Value", f"Could not create file for {selected_element.Name} class because it does not have the 'DB2Name' tagged value.")

def create_ddl_function(rep):
    col_object = rep.GetDiagramObjectByID(rep.GetCurrentDiagram().DiagramID)
    if col_object:
        sel_object = col_object.GetAt(0)
        sel_element = rep.GetElementByID(sel_object.ElementID)
        if sel_element:
            create_ddl_script(rep, sel_element)
        else:
            print("Error", "Could not find selected element.")
    else:
        print("Error", "No objects selected in the diagram.")
