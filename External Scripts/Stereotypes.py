# The script, written by Chany Jacobs, 
# is designed to create to all the classes in specific stereotype in selected package - Actors 
# that connect to the class in realisation with the same name.

import win32com.client
# num - order of functions

# 3
def actor_exists(repository, stereotype_name):
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
	e.Object_Type='Actor'
    AND s.Stereotype = '{stereotype_name}' 
    AND (c.Connector_Type = 'Realisation' OR c.Connector_Type ="Generalization")
    """
    
    # Execute the SQL query and check if any results are returned
    result = repository.SQLQuery(sql_query)
    return result

# 2
def create_and_add_actors(repository, package, stereotype_name):
    num_of_actors=0
    if package:
        actor_exists_result = actor_exists(repository, stereotype_name)
        for element in package.Elements:
            # Check if the current element's name is in the actor_exists_result
            if element.Stereotype == stereotype_name and element.Type == "Class" and element.Name not in actor_exists_result:
                # Create a new actor with the specified stereotype
                new_actor = package.Elements.AddNew(element.Name, "Actor")
                new_actor.Update()

                # Connect the newly created actor to itself using realization
                connector = package.Connectors.AddNew("", "Realisation")
                connector.SupplierID = element.ElementID
                connector.ClientID = new_actor.ElementID
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
        stereotype_name = input(f"Please enter the stereotype: ")
        #need to do option to cancelled
        create_and_add_actors(repository, package, stereotype_name)
    else:
        print("This script requires a package to be selected.")

if __name__ == "__main__":
    main()
