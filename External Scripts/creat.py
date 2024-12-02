import win32com.client

def update_tagged_value(element, tag_name, tag_value):
    """Updates the tagged value if it exists, otherwise modifies it."""
    try:
        # Access the TaggedValues collection
        tagged_values = element.TaggedValues

        # Loop through existing tagged values to find the one to update
        for tag in tagged_values:
            if tag.Name:
                tag.Notes = tag_value  # Update the value of the existing tag
                tag.Update()  # Commit the change
                break

            
    except Exception as e:
        print(f"Error updating tagged value: {e}")

def create_package(parent_package, package_name):
    """Creates a new package under the specified parent package."""
    new_package = parent_package.Packages.AddNew(package_name, "")
    new_package.Update()
    parent_package.Packages.Refresh()
    return new_package

def create_element(package, name, element_type, stereotype=None):
    """Creates a new element within the specified package."""
    element = package.Elements.AddNew(name, element_type)
    if stereotype:
        element.Stereotype = stereotype
    element.Update()
    package.Elements.Refresh()
    return element

def main():
    # Connect to EA
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
        print("EA is accessible.")
    except Exception as e:
        print("Error: Could not connect to EA:", str(e))
        return

    # Get the root model
    models = repository.Models
    if not models:
        print("No root model found.")
        return

    # Create or find the "ModelView-Chart" package in the root model
    root_model = models.GetAt(0)  # Assuming we're using the first model as root
    modelview_chart_package = None
    for package in root_model.Packages:
        if package.Name == "ModelView-Chart":
            modelview_chart_package = package
            print("Package 'ModelView-Chart' already exists.")
            break

    if not modelview_chart_package:
        modelview_chart_package = create_package(root_model, "ModelView-Chart")
        print("Created package 'ModelView-Chart'.")

    # Add elements to the package
    model_views = ["ElementsTraces", "RequiremenentTraces"]
    pie_charts = ["TraceRequirements", "TraceElements"]

    # Create Model Views and update their tagged values
    for model_view_name in model_views:
        model_view = create_element(modelview_chart_package, model_view_name, "ModelView")
        model_view_tag = """<modelview>
	<source customSQL="SELECT &#xA;    uc.Name AS ElementName,&#xA;    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,&#xA;    sub.RequirementName&#xA;FROM&#xA;    t_object AS uc&#xA;LEFT JOIN &#xA;(&#xA;    SELECT &#xA;        t_connector.Connector_ID,&#xA;        t_connector.Start_Object_ID,&#xA;        req.Name AS RequirementName&#xA;    FROM&#xA;        t_connector&#xA;    LEFT JOIN &#xA;        t_object AS req ON req.Object_ID = t_connector.End_Object_ID&#xA;    WHERE &#xA;        req.Object_Type = 'Requirement'&#xA;    ) AS sub ON sub.Start_Object_ID = uc.Object_ID&#xA;WHERE &#xA;    uc.Package_ID = #Package#"/>
</modelview>"""
        update_tagged_value(model_view, "ViewPropertise", model_view_tag)
        print(f"Created Model View '{model_view_name}' and updated tagged value.")

    # Create Pie Charts and update their tagged values
    for pie_chart_name in pie_charts:
        pie_chart = create_element(modelview_chart_package, pie_chart_name, "Chart")
        pie_chart.Stereotype = "Chart"  # Set the chart type to Pie Chart
        pie_chart.Update()
        
        chart_property = """<chart type="piechart">
	<source customSQL="SELECT &#xA;    IIF(sub.Connector_ID IS NOT NULL, &#xA;        IIF(sub.Connector_Type IS NOT NULL,&#xA;            IIF(sub.Btm_Mid_Label IS NOT NULL, sub.Btm_Mid_Label, sub.Connector_Type), &#xA;            'No Connection'), &#xA;        'Not Connected') AS Series,&#xA;    COUNT(*) AS ChartValue&#xA;FROM&#xA;    t_object AS uc&#xA;LEFT JOIN &#xA;(&#xA;    SELECT &#xA;        t_connector.Btm_Mid_Label,&#xA;        t_connector.Connector_Type,&#xA;        t_connector.Connector_ID,&#xA;        t_connector.Start_Object_ID,&#xA;        req.Name AS RequirementName&#xA;    FROM&#xA;        t_connector&#xA;    LEFT JOIN &#xA;        t_object AS req ON req.Object_ID = t_connector.End_Object_ID&#xA;    WHERE &#xA;        req.Object_Type = 'Requirement'&#xA;    ) AS sub ON sub.Start_Object_ID = uc.Object_ID&#xA;WHERE &#xA;    uc.Package_ID = #Package#&#xA;GROUP BY &#xA;    IIF(sub.Connector_ID IS NOT NULL, &#xA;        IIF(sub.Connector_Type IS NOT NULL,&#xA;            IIF(sub.Btm_Mid_Label IS NOT NULL, sub.Btm_Mid_Label, sub.Connector_Type), &#xA;            'No Connection'), &#xA;        'Not Connected')&#xA;ORDER BY &#xA;    IIF(sub.Connector_ID IS NOT NULL, &#xA;        IIF(sub.Connector_Type IS NOT NULL,&#xA;            IIF(sub.Btm_Mid_Label IS NOT NULL, sub.Btm_Mid_Label, sub.Connector_Type), &#xA;            'No Connection'), &#xA;        'Not Connected');"/>
	<appearance category="0" gradient="0" showindexinlabels="0" exploded="0" showdatalabels="1" fitinarea="0" labelPosition="0" holesize="50" displaylegend="0" rotationAngle="0" pieAngle="45"/>
</chart>"""
        update_tagged_value(pie_chart, "ChartPropertise", chart_property)
        print(f"Created Pie Chart '{pie_chart_name}' and updated tagged value.")

    print("Setup of 'ModelView-Chart' package is complete.")

if __name__ == "__main__":
    main()
