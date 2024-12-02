# import win32com.client

# # התחברות ל-Enterprise Architect
# ea = win32com.client.Dispatch("EA.App")
# repository = ea.Repository

# # יצירת פאקג' חדשה
# package_name = "TestPackage"
# parent_package = repository.GetTreeSelectedPackage()  # בחר את הפאקג' הנוכחית
# new_package = parent_package.Packages.AddNew(package_name, "")
# new_package.Update()

# # יצירת ריקוויירמנט
# requirement_name = "TestRequirement"
# requirement = new_package.Elements.AddNew(requirement_name, "Requirement")
# requirement.Update()

# # הוספת 10 אלמנטים עם קשרים לריקוויירמנט
# for i in range(10):
#     element_name = f"TestElement_{i+1}"
#     element = new_package.Elements.AddNew(element_name, "Class")  # או סוג אחר לפי הצורך
#     element.Update()

#     # יצירת קשר (Dependency) עם הריקוויירמנט
#     connector = new_package.Connectors.AddNew("", "Dependency")
#     connector.SupplierID = element.ElementID
#     connector.ClientID = requirement.ElementID
#     connector.Update()

# # עדכון הפאקג' כדי לשמור את השינויים
# new_package.Update()

# # הודעה לסיום
# print(f"Created package '{package_name}' with 10 elements and a requirement.")



# SELECT 
#     t_object.Package_ID AS Series, 
#     t_package.Name AS GroupName, 
#     COUNT(t_object.Object_ID) AS ChartValue
# FROM 
#     t_object
# INNER JOIN 
#     t_package ON t_object.Package_ID = t_package.Package_ID
# WHERE 
#     t_package.Name IN ('Sequence Diagrams')
# GROUP BY 
#     t_object.Package_ID, t_package.Name;