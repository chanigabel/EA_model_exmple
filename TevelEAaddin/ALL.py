import os
from datetime import datetime

def save_package_enum_in_excel_file(Repository):
    parentPackage = None
    grandParentPackage = None
    excelApp = None
    excelWorkbooks = None
    excelWorkbook = None
    fileDirectory = r'C:\Temp\'
    fullPath = fileDirectory
    strDate = datetime.now().strftime('%Y%m%d')
    fileName = ''
    misValue = None
    
    # check for the selected package
    selPackage = Repository.GetTreeSelectedPackage()
    
    # check if any package is selected
    if selPackage is None:
        print("Please, select a package for enums' search.")
    else:
        if selPackage.ParentID != 0:
            parentPackage = Repository.GetPackageByID(selPackage.ParentID)
            if parentPackage.ParentID != 0:
                grandParentPackage = Repository.GetPackageByID(parentPackage.ParentID)
        fileName += (grandParentPackage.Name if grandParentPackage else "Model") + "." + \
                    (parentPackage.Name if parentPackage else "View") + "." + \
                    selPackage.Name + " " + strDate + ".xls"
        fullPath += fileName
        
        # check if directory exists
        if not os.path.exists(fileDirectory):
            os.makedirs(fileDirectory)
        
        try:
            # Creating new Excel application
            excelApp = Dispatch('Excel.Application')
            if excelApp is None:
                raise Exception("ERROR: Excel couldn't be started")
            
            # To make application visible
            excelApp.Visible = True
            
            # To get the workbooks collection
            excelWorkbooks = excelApp.Workbooks
            
            # Creating a new workbook
            excelWorkbook = excelWorkbooks.Add()
            
            # To get the worksheets collection
            sheets = excelWorkbook.Worksheets
            worksheet = sheets.Item(1)
            if worksheet is None:
                raise Exception("ERROR: Worksheet is null")
            
            # Set Headers for the document
            headers = ["Enum Name", "Enum Hebrew Name(Tag)", "Hebrew Enumeration(Tag)", "Enumeration Value(Attribute)"]
            rangeHeader = worksheet.Range("A1", "D1")
            if rangeHeader is None:
                raise Exception("ERROR: Range is null")
            rangeHeader.Value = headers
            
            fill_out_excel_file(get_package_enums(selPackage, Repository), worksheet)
            
            # Save workbook
            excelWorkbook.SaveAs(fullPath)
            print("It's done")
        finally:
            excelApp = None

def save_enums_in_excel_file(Repository):
    excelApp = None
    excelWorkbooks = None
    excelWorkbook = None
    fileDirectory = r"C:\Temp\"
    fileName = "TevelEnums " + datetime.now().strftime("%Y%m%d") + ".xls"
    fullPath = os.path.join(fileDirectory, fileName)
    
    if not os.path.exists(fileDirectory):
        os.makedirs(fileDirectory)
    
    try:
        excelApp = win32.Dispatch("Excel.Application")
        if excelApp is None:
            raise Exception("ERROR: EXCEL couldn't be started")
        excelApp.Visible = True
        excelWorkbooks = excelApp.Workbooks
        excelWorkbook = excelWorkbooks.Add()
        sheets = excelWorkbook.Worksheets
        worksheet = sheets.Item(1)
        if worksheet is None:
            raise Exception("ERROR: worksheet is null")
        
        headers = ["Enum Name", "Enum Hebrew Name(Tag)", "Hebrew Enumeration(Tag)", "Enumeration Value(Attribute)"]
        rangeHeader = worksheet.Range("A1", "D1")
        if rangeHeader is None:
            raise Exception("ERROR: range is null")
        rangeHeader.Value = headers
        
        fill_out_excel_file(get_tevel_enums(Repository), worksheet)
        excelWorkbook.SaveAs(fullPath, AccessMode=win32.constants.xlNoChange)
        print("It's done")
    finally:
        if excelApp:
            excelApp.Quit()
            excelApp = None

def get_package_enums(selPackage, rep):
    squery = f"SELECT COALESCE(t_object.Name,'') AS 'EnumName', COALESCE(t_objectproperties.Value,'') AS 'EnumHebrewName', " \
             f"COALESCE(t_attributetag.VALUE,'') AS 'HebrewEnumeration', COALESCE(t_attribute.Name,'') AS 'EnumerationValue' " \
             f"FROM  t_object LEFT JOIN t_attribute ON t_object.Object_ID = t_attribute.Object_ID LEFT JOIN " \
             f"t_attributetag ON t_attribute.ID = t_attributetag.ElementID LEFT JOIN " \
             f"t_objectproperties ON t_object.Object_ID = t_objectproperties.Object_ID " \
             f"WHERE t_object.Package_ID = {selPackage.PackageID} ORDER BY t_object.Name"
    result = rep.SQLQuery(squery)
    return result

def get_tevel_enums(rep):
    squery = """
        SELECT COALESCE(t_object.Name'') AS 'EnumName', COALESCE(t_objectproperties.Value,'') AS 'EnumHebrewName', 
               COALESCE(t_attributetag.VALUE,'') AS 'HebrewEnumeration', COALESCE(t_attribute.Name'') AS 'EnumerationValue'
        FROM  t_object LEFT JOIN t_attribute ON t_object.Object_ID = t_attribute.Object_ID LEFT JOIN
              t_attributetag ON t_attribute.ID = t_attributetag.ElementID LEFT JOIN
              t_objectproperties ON t_object.Object_ID = t_objectproperties.Object_ID
        WHERE t_object.Name IN ('%Enum','Enum_TODELETE') ORDER BY t_object.Name
    """
    result = rep.SQLQuery(squery)
    
    # Parse the XML result into an XML document
    xml_doc = ET.fromstring(result)
    return xml_doc

def fill_out_excel_file(result, worksheet):
    listEnumElements = result.SelectNodes("//EnumName")
    listEnumTagValues = result.SelectNodes("//EnumHebrewName")
    listEnumAttributedTagValues = result.SelectNodes("//HebrewEnumeration")
    listEnumAttributes = result.SelectNodes("//EnumerationValue")

    for i in range(len(listEnumElements)):
        rowArray = [listEnumElements[i].InnerText if listEnumElements[i] else "",
                    listEnumTagValues[i].InnerText if listEnumTagValues else "",
                    listEnumAttributedTagValues[i].InnerText if listEnumAttributedTagValues[i] else "",
                    listEnumAttributes[i].InnerText if listEnumAttributes[i] else ""]
        row = str(i + 2)
        rangeRow = worksheet.Range("A" + row, "D" + row)
        if rangeRow is None:
            raise Exception("ERROR: Range is null")
        rangeRow.Value = rowArray

def search_for_duplicates(repository):
    # Check for the selected package
    sel_package = repository.GetTreeSelectedPackage()

    # Check if some package is selected
    if sel_package is None:
        print("Please, select a package for the duplicates search.")
    else:
        # Assuming DuplicatesSearch is a class in your Python environment
        dialog = DuplicatesSearch(repository, sel_package)
        dialog.Show()

def create_diagram_dll_single_file(rep):
    table_script = ""
    sel_element = get_selected_element(rep)
    cur_diagram = get_selected_diagram(rep)

    if cur_diagram:
        # Check if directory exists
        if not os.path.exists("C:/Temp/"):
            os.makedirs("C:/Temp/")
        
        # Create file for the ddl script
        cur_date = datetime.today().strftime("%Y%m%d")
        file_name = f"C:/Temp/{cur_diagram.Name} {cur_date}.sql"

        # Check if file exists
        if os.path.exists(file_name):
            os.remove(file_name)

        for cur_object in cur_diagram.DiagramObjects:
            table_script = ""
            sel_element = rep.GetElementByID(cur_object.ElementID)
            if sel_element.Type == "Class":
                create_ddl_script_single_file(rep, sel_element, table_script)
                table_script += "\n\n"
                with open(file_name, "a") as file:
                    file.write(table_script)
        
        messagebox.showinfo("Done", "DDL files created successfully.")

def create_ddl_script_single_file(rep, selected_element, table_script):
    table_name = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        table_script = loop_by_attributes(rep, selected_element, table_script)
    else:
        print("Missing Tagged Value", f"Could not create file for {selected_element.Name} class because it does not have the 'DB2Name' tagged value.")

def create_ddl_for_diagram_and_links(rep):
    create_diagram_ddl_function(rep)
    create_diagram_link_tables(rep)

def create_diagram_link_tables(rep):
    utility = EAUtility()
    flag_db2_name = False
    link_table_name = ""
    start_table_name = ""
    end_table_name = ""
    table_script = ""
    cur_diagram = utility.get_selected_diagram(rep)

    if cur_diagram:
        if not os.path.exists("C:\\Temp\\"):
            os.makedirs("C:\\Temp\\")

        for cur_link in cur_diagram.DiagramLinks:
            flag_db2_name = False
            cur_connector = rep.GetConnectorByID(cur_link.ConnectorID)
            if cur_connector.Stereotype.lower() != "link table":
                continue

            for con_tag_value in cur_connector.TaggedValues:
                if con_tag_value.Name.lower() == "db2name":
                    link_table_name = con_tag_value.Value
                    flag_db2_name = True
                    break

            if not flag_db2_name:
                link_table_name = "NO_DB2Name"

            cur_end_object = rep.GetElementByID(cur_connector.ClientID)
            cur_start_object = rep.GetElementByID(cur_connector.SupplierID)

            if cur_end_object.TaggedValues.GetByName("DB2Name"):
                start_table_name = cur_end_object.TaggedValues.GetByName("DB2Name").Value
                if len(start_table_name) > 30:
                    start_table_name = "???" + start_table_name
            else:
                continue

            if cur_start_object.TaggedValues.GetByName("DB2Name"):
                end_table_name = cur_start_object.TaggedValues.GetByName("DB2Name").Value
                if len(end_table_name) > 30:
                    end_table_name = "???" + end_table_name
            else:
                continue

            table_script = "CREATE TABLE " + link_table_name + "\n"
            table_script += "(\n \t \t " + start_table_name + ",\n"
            table_script += " \t \t " + end_table_name + "\n)"
            link_table_name = link_table_name.strip()
            with open("C:\\Temp\\" + link_table_name + ".sql", "w") as file:
                file.write(table_script)

        MessageBox.Show("It's done")

def create_link_table(rep):
    utility = EAUtility()
    result = XmlDocument()
    cur_diagram = utility.get_selected_diagram(rep)
    squery = ""
    table_script = ""
    link_table_name = ""
    start_table_name = ""
    end_table_name = ""

    if cur_diagram:
        sel_connector = cur_diagram.SelectedConnector
        if sel_connector:
            squery = "SELECT ct.VALUE AS 'ConnectorName',so.Object_ID AS 'StartTableID', ed.Object_ID AS 'EndTableID' FROM t_connector c, t_object so, t_object ed, t_connectortag ct " + \
                     "WHERE c.Connector_ID = ct.ElementID AND c.Start_Object_ID = so.Object_ID AND c.End_Object_ID = ed.Object_ID " + \
                     "AND c.Stereotype='Link table' AND ct.Property LIKE 'DB2Name' AND c.Connector_ID = " + str(sel_connector.ConnectorID)
            result.LoadXml(rep.SQLQuery(squery))
            link_table_name = result.SelectNodes("//ConnectorName")[0].InnerText
            start_element = rep.GetElementByID(int(result.SelectNodes("//StartTableID")[0].InnerText))
            end_element = rep.GetElementByID(int(result.SelectNodes("//EndTableID")[0].InnerText))
            start_table_name = start_element.TaggedValues.GetByName("DB2Name").Value
            end_table_name = end_element.TaggedValues.GetByName("DB2Name").Value

            if len(start_table_name) > 30:
                start_table_name = "???" + start_table_name
            if len(end_table_name) > 30:
                end_table_name = "???" + end_table_name

            table_script = "CREATE TABLE " + link_table_name + "\n"
            table_script += "(\n \t \t " + start_table_name + ",\n"
            table_script += " \t \t " + end_table_name + "\n)"
            if not os.path.exists("C:\\Temp\\"):
                os.makedirs("C:\\Temp\\")
            link_table_name = link_table_name.strip()
            with open("C:\\Temp\\" + link_table_name + ".sql", "w") as file:
                file.write(table_script)
            MessageBox.Show("It's done")
        else:
            MessageBox.Show("Please, select a connector.", "Tevel Addins: ")

def create_diagram_ddl_function(rep):
    sel_element = None
    cur_diagram = generalFunction.GetSelectedDiagram(rep)

    if cur_diagram:
        for cur_object in cur_diagram.DiagramObjects:
            sel_element = rep.GetElementByID(cur_object.ElementID)
            if sel_element.Type.lower() == "class":
                create_ddl_script(rep, sel_element)

def loop_by_attributes(rep, selected_element, table_script):
    for current_attribute in selected_element.Attributes:
        if current_attribute.GetTaggedValueByName("DB2ColumnName"):
            if current_attribute.Stereotype.lower() >= "jpa":
                continue
            if "embed" in current_attribute.Stereotype.lower():
                continue
            if "periodentity" in current_attribute.Type.lower():
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
                table_script += ",\n\t\t"
    return table_script

def define_db2_type(current_attribute, table_script):
    # Define DB2 type based on current attribute
    pass  # Define your logic here

def create_diagram_ddl_function(rep):
    cur_diagram = get_selected_diagram(rep)

    if cur_diagram:
        for cur_object in cur_diagram.DiagramObjects:
            sel_element = rep.GetElementByID(cur_object.ElementID)
            if sel_element.Type == "Class":
                create_ddl_script(rep, sel_element)

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

def is_derived_class_single_table(sel_element):
    squery = f"SELECT End_Object_ID FROM t_connector WHERE STEREOTYPE='single_table' AND Start_Object_ID = {sel_element.ElementID}"
    result = connect_to_db.SelectStatement(squery)
    list_class_ids = result.SelectNodes("//End_Object_ID")
    return list_class_ids.Count != 0

def create_diagram_and_links(rep):
    create_diagram_ddl_function(rep)
    create_diagram_link_tables(rep)

def create_diagram_link_tables(rep):
    utility = EAUtility()
    cur_diagram = utility.GetSelectedDiagram(rep)

    if cur_diagram:
        if not os.path.exists("C:/Temp/"):
            os.makedirs("C:/Temp/")

        for cur_link in cur_diagram.DiagramLinks:
            flag_db2_name = False
            cur_connector = rep.GetConnectorByID(cur_link.ConnectorID)
            if cur_connector.Stereotype.lower() != "link table":
                continue
            for con_tag_value in cur_connector.TaggedValues:
                if con_tag_value.Name.lower() == "db2name":
                    link_table_name = con_tag_value.Value.strip()
                    flag_db2_name = True
                    break
            if not flag_db2_name:
                link_table_name = "NO_DB2Name"

            cur_end_object = rep.GetElementByID(cur_connector.ClientID)
            cur_start_object = rep.GetElementByID(cur_connector.SupplierID)

            if cur_end_object.GetTaggedValueByName("DB2Name"):
                start_table_name = cur_end_object.GetTaggedValueByName("DB2Name").Value.strip()
                if len(start_table_name) > 30:
                    start_table_name = "???" + start_table_name
            else:
                continue

            if cur_start_object.GetTaggedValueByName("DB2Name"):
                end_table_name = cur_start_object.GetTaggedValueByName("DB2Name").Value.strip()
                if len(end_table_name) > 30:
                    end_table_name = "???" + end_table_name
            else:
                continue

            table_script = f"CREATE TABLE {link_table_name}\n"
            table_script += f"(\n\t\t{start_table_name},\n\t\t{end_table_name}\n)"
            link_table_name = link_table_name.strip()
            with open(f"C:/Temp/{link_table_name}.sql", "w") as file:
                file.write(table_script)

        messagebox.showinfo("Done", "DDL files created successfully.")

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

def create_ddl_script(rep, selected_element):
    table_name = ""
    table_script = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        if not os.path.exists("C:/Temp/"):
            os.makedirs("C:/Temp/")
        file_name = f"C:/Temp/{table_name}.sql"
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                file.write(loop_by_attributes(rep, selected_element, table_script))
        else:
            print("File Exists", f"The file '{file_name}' already exists.")
    else:
        print("Missing Tagged Value", f"Could not create file for the '{selected_element.Name}' class because it does not have the 'DB2Name' tagged value.")

def loop_by_attributes(rep, selected_element, table_script):
    table_script += "(\n"
    for current_attribute in selected_element.Attributes:
        if current_attribute.GetTaggedValueByName("DB2ColumnName"):
            if current_attribute.Stereotype.lower() >= "jpa":
                continue
            if "embed" in current_attribute.Stereotype.lower():
                continue
            if "periodentity" in current_attribute.Type.lower():
                continue
            attr_name = current_attribute.GetTaggedValueByName("DB2ColumnName").Value.strip()
            if "list" not in current_attribute.Type.lower() and "map" not in current_attribute.Type.lower() and "charcoll" not in current_attribute.Type.lower():
                table_script += f"\t{attr_name} "
                if "_id" in attr_name.lower():
                    table_script += "INTEGER"
                else:
                    define_db2_type(current_attribute, table_script)
                if current_attribute.GetTaggedValueByName("NULL=TRUE"):
                    table_script += " NULL"
                elif current_attribute.GetTaggedValueByName("NULL=FALSE"):
                    table_script += " NOT NULL"
                table_script += ",\n"
    table_script += ")"
    return table_script

def check_foreign_keys(selected_element, rep, table_script):
    create_target_class_foreign_key(selected_element, rep, table_script)
    create_source_class_foreign_key(selected_element, rep, table_script)

def create_ddl_from_class(rep):
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

def create_ddl_script(rep, selected_element):
    table_name = ""
    table_script = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        if not os.path.exists("C:/Temp/"):
            os.makedirs("C:/Temp/")
        file_name = f"C:/Temp/{table_name}.sql"
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                file.write(loop_by_attributes(rep, selected_element, table_script))
        else:
            print("File Exists", f"The file '{file_name}' already exists.")
    else:
        print("Missing Tagged Value", f"Could not create file for the '{selected_element.Name}' class because it does not have the 'DB2Name' tagged value.")

def loop_by_attributes(rep, selected_element, table_script):
    table_script += "(\n"
    for current_attribute in selected_element.Attributes:
        if current_attribute.GetTaggedValueByName("DB2ColumnName"):
            if current_attribute.Stereotype.lower() >= "jpa":
                continue
            if "embed" in current_attribute.Stereotype.lower():
                continue
            if "periodentity" in current_attribute.Type.lower():
                continue
            attr_name = current_attribute.GetTaggedValueByName("DB2ColumnName").Value.strip()
            if "list" not in current_attribute.Type.lower() and "map" not in current_attribute.Type.lower() and "charcoll" not in current_attribute.Type.lower():
                table_script += f"\t{attr_name} "
                if "_id" in attr_name.lower():
                    table_script += "INTEGER"
                else:
                    define_db2_type(current_attribute, table_script)
                if current_attribute.GetTaggedValueByName("NULL=TRUE"):
                    table_script += " NULL"
                elif current_attribute.GetTaggedValueByName("NULL=FALSE"):
                    table_script += " NOT NULL"
                table_script += ",\n"
    table_script += ")"
    return table_script

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

def create_ddl_script(rep, selected_element):
    table_name = ""
    table_script = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script

def check_class_relations(selected_element, rep, table_script):
    squery = f"SELECT Start_Object_ID FROM t_connector WHERE STEREOTYPE='single_table' AND End_Object_ID = {selected_element.ElementID}"
    result = connect_to_db.select_statement(squery)
    list_class_ids = result.SelectNodes("//Start_Object_ID")
    if list_class_ids is not None:
        for class_id in list_class_ids:
            single_table_class_name = class_id.SelectSingleNode("//Start_Object_ID").InnerText
            get_single_table_relation_class(rep, rep.GetElementByID(int(single_table_class_name)), table_script)

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

def create_ddl_function(self, rep):
    col_object = rep.GetDiagramObjectByID(rep.GetCurrentDiagram().DiagramID)
    if col_object:
        sel_object = col_object.GetAt(0)
        sel_element = rep.GetElementByID(sel_object.ElementID)
        if sel_element:
            self.create_ddl_script(rep, sel_element)
        else:
            messagebox.showwarning("Error", "Could not find selected element.")
    else:
        messagebox.showwarning("Error", "No objects selected in the diagram.")

def create_ddl_script(self, rep, selected_element):
    table_name = ""
    table_script = ""
    flag_db2_name = False

    for cur_tag in selected_element.TaggedValues:
        if cur_tag.Name.lower() == "db2name":
            table_name = cur_tag.Value.strip()
            table_script = f"CREATE TABLE {table_name}\n"
            flag_db2_name = True
            break

    if flag_db2_name:
        if not os.path.exists("C:/Temp/"):
            os.makedirs("C:/Temp/")
        file_name = f"C:/Temp/{table_name}.sql"
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                file.write(self.loop_by_attributes(rep, selected_element, table_script))
        else:
            messagebox.showwarning("File Exists", f"The file '{file_name}' already exists.")
    else:
        messagebox.showwarning("Missing Tagged Value",
                                f"Could not create file for the '{selected_element.Name}' class because it does not have the 'DB2Name' tagged value.")

def loop_by_attributes(self, rep, selected_element, table_script):
    table_script += "(\n"
    for current_attribute in selected_element.Attributes:
        if current_attribute.GetTaggedValueByName("DB2ColumnName"):
            if current_attribute.Stereotype.lower() >= "jpa":
                continue
            if "embed" in current_attribute.Stereotype.lower():
                continue
            if "periodentity" in current_attribute.Type.lower():
                continue
            attr_name = current_attribute.GetTaggedValueByName("DB2ColumnName").Value.strip()
            if "list" not in current_attribute.Type.lower() and "map" not in current_attribute.Type.lower() and "charcoll" not in current_attribute.Type.lower():
                table_script += f"\t{attr_name} "
                if "_id" in attr_name.lower():
                    table_script += "INTEGER"
                else:
                    self.define_db2_type(current_attribute, table_script)
                if current_attribute.GetTaggedValueByName("NULL=TRUE"):
                    table_script += " NULL"
                elif current_attribute.GetTaggedValueByName("NULL=FALSE"):
                    table_script += " NOT NULL"
                table_script += ",\n"
    table_script += ")"
    return table_script

def check_foreign_keys(self, selected_element, rep, table_script):
        self.create_target_class_foreign_key(selected_element, rep, table_script)
        self.create_source_class_foreign_key(selected_element, rep, table_script)

def create_ddl_from_class(self, rep):
        col_object = rep.GetDiagramObjectByID(rep.GetCurrentDiagram().DiagramID)
        if col_object:
            sel_object = col_object.GetAt(0)
            sel_element = rep.GetElementByID(sel_object.ElementID)
            if sel_element:
                self.create_ddl_script(rep, sel_element)
            else:
                messagebox.showwarning("Error", "Could not find selected element.")
        else:
            messagebox.showwarning("Error", "No objects selected in the diagram.")

def create_diagram_eap(rep):
    flag_if_package_exist = False
    list_xmi_package = []
    list_package_guids = []
    list_package_names = []
    cur_diagram = general_function.get_selected_diagram(rep)

    if cur_diagram is not None:
        my_project = EA.Project()
        sel_package = rep.get_tree_selected_package()
        if sel_package is None:
            print("Please select a Yachidat Avoda.")
        else:
            if cur_diagram is not None:
                my_project = rep.get_project_interface()
                for cur_object in cur_diagram.diagram_objects:
                    sel_element = rep.get_element_by_id(cur_object.element_id)
                    if sel_element.type == "Package":
                        flag_if_package_exist = True
                        if not os.path.exists("C:\\Temp\\"):
                            os.makedirs("C:\\Temp\\")
                        xmi_name = sel_package.name + "_" + sel_element.name
                        file_name = "C:\\Temp\\" + xmi_name + ".xmi"
                        if not os.path.exists(file_name):
                            xmi_package = EAPClass(file_name, sel_element.element_guid, sel_element.name)
                            first_package_id = sel_element.package_id
                            sel_package = rep.get_package_by_id(first_package_id)
                            list_package_guids.append(sel_package.package_guid)
                            list_package_names.append(sel_package.name)
                            create_eap_hierarchy(sel_package, rep, list_package_guids, list_package_names)
                            xmi_package.package_hierarchy = list(list_package_guids)
                            xmi_package.package_hierarchy_name = list(list_package_names)
                            list_xmi_package.append(xmi_package)
                            my_project.export_package_xmi(sel_element.element_guid, EA.EnumXMIType.xmiEA241, 1, -1, 0, 0, file_name)
                        list_package_guids.clear()
                        list_package_names.clear()

                if rep.create_model(EA.CreateModelType.cmEAPFromBase, "C:\\Temp\\" + cur_diagram.name + ".eap", 1) and flag_if_package_exist:
                    create_eap_model("C:\\Temp\\" + cur_diagram.name + ".eap", list_xmi_package, my_project, rep)
                if not flag_if_package_exist:
                    print("No packages are found in the selected diagram.")

def create_eap_hierarchy(sel_package, rep, package_guids, package_names):
    parent_package = None
    if sel_package.parent_id == 0:
        return None

    parent_package = rep.get_package_by_id(sel_package.parent_id)
    package_guids.append(parent_package.package_guid)
    package_names.append(parent_package.name)

    return create_eap_hierarchy(parent_package, rep, package_guids, package_names)

def create_eap_model(project_path, list_xmi_package, my_project, rep1):
    cur_package = None
    tmp_package = None
    list_package_guids = []

    my_project.load_project(project_path)
    rep1.open_file(project_path)
    rep1.models.delete_at(0, True)

    root = rep1.models.add_new(list_xmi_package[0].package_hierarchy_name[-1], "")
    root.update()
    rep1.models.refresh()

    cur_package = root
    cur_package.update()
    cur_package.packages.refresh()
    rep1.refresh_model_view(0)
    list_package_guids.append(cur_package.package_guid)

    for cur_class in list_xmi_package:
        count = len(cur_class.package_hierarchy) - 1
        for i in range(count, -1, -1):
            if i == count:
                continue
            if general_function.if_package_exist(rep1, cur_class.package_hierarchy_name[i], list_package_guids, tmp_package):
                cur_package = tmp_package
                continue
            else:
                cur_package = cur_package.packages.add_new(cur_class.package_hierarchy_name[i], "")
            cur_package.update()
            cur_package.packages.refresh()
            list_package_guids.append(cur_package.package_guid)
        my_project.import_package_xmi(cur_package.package_guid, cur_class.filename, 1, 1)
    
    rep1.refresh_model_view(0)
    rep1.models.refresh()
    print("It's done")

def is_class_derived_from_base_entity(rep, args):
    class_guid = ""
    sa = args
    class_guid = sa[0]
    cur_element = rep.get_element_by_guid(class_guid)
    for cur_att in cur_element.attributes:
        if cur_att.name.strip().upper() == "ID":
            return False
    is_base_entity = [False]
    check_for_base_entity_parent(cur_element, rep, is_base_entity)
    if is_base_entity[0]:
        return "true"
    else:
        return "false"

def check_for_base_entity_parent(selected_element, rep, is_base_entity):
    parent_element = None
    squery = ""
    parent_class_id = ""
    result = None
    list_class_ids = []
    my_db = DB(rep)
    squery = "SELECT End_Object_ID FROM t_connector WHERE t_connector.Connector_Type='Generalization' " + \
             "AND Connector_ID NOT IN (SELECT Connector_ID FROM t_connector " + \
             "WHERE Stereotype like 'join%') AND Start_Object_ID = " + str(selected_element.element_id)
    result = my_db.select_statement(squery)
    list_class_ids = result.findall("//End_Object_ID")
    if list_class_ids is not None or len(list_class_ids) != 0:
        for class_id in list_class_ids:
            parent_class_id = class_id.find("//End_Object_ID").text
            parent_element = rep.get_element_by_id(int(parent_class_id))
            if parent_element.name == "BaseEntity":
                is_base_entity[0] = True
                return
            check_for_base_entity_parent(parent_element, rep, is_base_entity)
    else:
        return