# The script, written by Chany Jacobs, 
# is designed to create to all the classes in specific stereotype in selected package - Actors 
# that connect to the class in realisation with the same name.

import win32com.client
# num - order of functions

# 3
def actor_exists(repository, stereotype_name, Package_ID):
    # Construct the SQL query to find elements with the specified name and stereotype
    sql_query = f"""
        SELECT 
        e.Name
    FROM((
        t_object e 
    INNER JOIN 
        t_connector c ON e.Object_ID = c.Start_Object_ID )
    INNER JOIN 
        t_object s ON c.End_Object_ID = s.Object_ID )
    WHERE 
    e.Name = s.Name 
	AND s.Object_Type='Actor'
    AND e.Stereotype = '{stereotype_name}' 
    AND c.Connector_Type = 'Realisation' 
    AND s.Stereotype = '{stereotype_name}'
	AND e.Package_ID={Package_ID}
    """
    
    # Execute the SQL query and check if any results are returned
    result = repository.SQLQuery(sql_query)
    return result

# 2
def create_and_add_actors(repository, package, stereotype_name):
    num_of_actors=0
    if package:
        actor_exists_result = actor_exists(repository, stereotype_name, package.PackageID)
        print(actor_exists_result)
        for element in package.Elements:
            # Check if the current element's name is in the actor_exists_result
            if element.Stereotype == stereotype_name and element.Type == "Class" and element.Name not in actor_exists_result:
                # Create a new actor with the specified stereotype
                new_actor = package.Elements.AddNew(element.Name, "Actor")
                new_actor.Stereotype = stereotype_name
                new_actor.Update()

                # Connect the newly created actor to itself using realization
                connector = package.Connectors.AddNew("", "Realisation")
                connector.SupplierID = new_actor.ElementID
                connector.ClientID = element.ElementID
                connector.Update()
                num_of_actors+=1
        print(num_of_actors,"Actors created and added successfully in package:", package.Name)

        # Recursively call the function for sub-packages
        for sub_package in package.Packages:
            create_and_add_actors(repository, sub_package, stereotype_name)

# 1
def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository

    package = repository.GetTreeSelectedPackage()
    if package is not None:
        stereotype_name = input("Please enter the stereotype: ")
        if stereotype_name == "":
            stereotype_name = "Subsystem"  # Default stereotype name
        create_and_add_actors(repository, package, stereotype_name)
    else:
        print("This script requires a package to be selected.")

if __name__ == "__main__":
    main()
