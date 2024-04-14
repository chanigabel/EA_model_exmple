import os
import datetime
import xml.etree.ElementTree as ET
from tkinter import messagebox
import win32com.client

def save_enums_in_excel_file(repository):
    file_directory = "C:\\Temp\\"
    file_name = f"TevelEnums {datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
    full_path = os.path.join(file_directory, file_name)

    try:
        workbook = create_excel_workbook()
        worksheet = workbook.active
        worksheet.title = "Tevel Enums"

        headers = ["Enum Name", "Enum Hebrew Name (Tag)", "Hebrew Enumeration (Tag)", "Enumeration Value (Attribute)"]
        worksheet.append(headers)

        tevel_enums = get_tevel_enums(repository)
        fill_out_excel_file(tevel_enums, worksheet)

        workbook.save(full_path)
        messagebox.showinfo("Success", f"Excel file saved successfully at:\n{full_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def create_excel_workbook():
    # Simulate workbook creation without using external libraries
    # Here you can define your own logic to create a workbook
    pass

def fill_out_excel_file(tevel_enums, worksheet):
    for enum in tevel_enums:
        worksheet.append(enum)

def get_tevel_enums(repository):
    query = """
        SELECT 
            t_object.Name AS 'EnumName', 
            t_objectproperties.Value AS 'EnumHebrewName', 
            t_attributetag.VALUE AS 'HebrewEnumeration', 
            t_attribute.Name AS 'EnumerationValue'
        FROM(((
            t_object 
            LEFT JOIN t_attribute ON t_object.Object_ID = t_attribute.Object_ID)
            LEFT JOIN t_attributetag ON t_attribute.ID = t_attributetag.ElementID) 
            LEFT JOIN t_objectproperties ON t_object.Object_ID = t_objectproperties.Object_ID) 
        WHERE 
            t_object.Name LIKE '%Enum' 
        ORDER BY 
            t_object.Name
    """
    result = repository.SQLQuery(query)
    tevel_enums = []

    if result:
        root = ET.fromstring(result)
        for element in root.findall('.//Row'):
            enum_name = element.find('EnumName').text.strip() if element.find('EnumName') is not None else ''
            enum_hebrew_name = element.find('EnumHebrewName').text.strip() if element.find('EnumHebrewName') is not None else ''
            hebrew_enumeration = element.find('HebrewEnumeration').text.strip() if element.find('HebrewEnumeration') is not None else ''
            enumeration_value = element.find('EnumerationValue').text.strip() if element.find('EnumerationValue') is not None else ''
            tevel_enums.append([enum_name, enum_hebrew_name, hebrew_enumeration, enumeration_value])

    return tevel_enums

def main():
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
        save_enums_in_excel_file(repository)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
