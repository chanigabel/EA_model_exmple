import win32com.client

# Function to execute a SQL query and return the results
def execute_query(repository, query):
    return repository.SQLQuery(query)

# Function to create a pie chart element with specified properties
def create_pie_chart(repository, package, sql_query):
    # Create a new diagram for the pie chart
    pie_chart_diagram = package.Diagrams.AddNew("ConnectRequirements", "PieChart")  
    pie_chart_diagram.Update()  # Save the diagram
    
    # Create the diagram object
    diagram_object = pie_chart_diagram.DiagramObjects.AddNew("Pie Chart", "PieChart")
    
    # Set the properties for the pie chart
    diagram_object.SQLQuery = sql_query  # Set the SQL query for the chart
    diagram_object.Type = "Pie"  # Set the type of chart to Pie
    diagram_object.GroupBy = "General"  # Set the grouping option
    diagram_object.Series = "X"  # Set the series name
    diagram_object.Color = "Auto"  # Set color option (adjust as needed)
    
    diagram_object.Update()  # Save the diagram object
    return diagram_object

# Function to create a model view element with specified properties
def create_model_view(repository, package, sql_query):
    # Create a new diagram for the model view
    model_view_diagram = package.Diagrams.AddNew("Model View", "ModelView")
    model_view_diagram.Update()  # Save the diagram
    
    # Create the diagram object
    diagram_object = model_view_diagram.DiagramObjects.AddNew("Model View", "ModelView")
    
    # Set the properties for the model view
    diagram_object.SQLQuery = sql_query  # Set the SQL query for the model view
    
    diagram_object.Update()  # Save the diagram object
    return diagram_object

# Main script execution
def main():
    repository = win32com.client.Dispatch("EA.App").Repository
    selected_package = repository.GetTreeSelectedPackage()  # Get the currently selected package
    
    # SQL Queries
    pie_chart_query = """
    SELECT 
        IIF(t_connector.Connector_ID IS NOT NULL, 'Connected', 'Not Connected') AS Series
    FROM 
        t_object
    LEFT JOIN 
        t_connector ON t_connector.End_Object_ID = t_object.Object_ID
    WHERE 
        t_object.Package_ID = 214
        AND t_object.Object_Type='Requirement';
    """

    model_view_query = """
    SELECT 
        req.Name AS RequirementName,
        IIF(t_connector.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
        uc.Name AS UseCaseName
    FROM 
        t_object AS req
    LEFT JOIN 
        t_connector ON t_connector.End_Object_ID = req.Object_ID
    LEFT JOIN
        t_object AS uc ON uc.Object_ID = t_connector.Start_Object_ID
    WHERE 
        req.Package_ID = 214
        AND req.Object_Type='Requirement';
    """

    # Create pie chart and model view
    pie_chart = create_pie_chart(repository, selected_package, pie_chart_query)
    model_view = create_model_view(repository, selected_package, model_view_query)

    print("Pie chart and model view created successfully.")

if __name__ == "__main__":
    main()
