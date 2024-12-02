import win32com.client

# Create a connection to the EA application
ea = win32com.client.Dispatch("EA.App")
repository = ea.Repository

# Retrieve the selected elements in the EA tree
selected_elements = repository.GetTreeSelectedObject()

if selected_elements.Count > 0:
    # Loop through each selected element
    for i in range(selected_elements.Count):
        selected_element = selected_elements.GetAt(i)

        # Check if the selected element is a Chart
            # Retrieve the chart's SQL queries through its collection
        try:
            # Get the chart's collection
            charts = selected_element.ChartGroups
            for j in range(charts.Count):
                chart = charts.GetAt(j)
                sql_query = chart.SQLQuery  # Attempt to get the SQL query property
                print(f"Custom SQL query for chart '{chart.Name}': {sql_query}")

        except Exception as e:
            print(f"Error retrieving SQL query for chart '{selected_element.Name}': {e}")

      

else:
    print("Error: No elements selected.")
