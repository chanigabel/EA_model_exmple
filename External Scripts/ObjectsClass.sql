SELECT 
	o2.ea_guid as CLASSGUID,
	't_object' as CLASSTABLE,
	o2.Object_Type AS CLASSTYPE,
    t_diagram.Name AS Diagram_Name,
	t_object.Name AS Object_Name,
	t_object.Classifier,
	IIF(
    t_object.Object_Type IN ('Class', 'Interface'), 
    t_object.Name,
    o2.Name
	) AS Class_Name,
	IIF(
	t_object.Classifier_guid IS NOT NULL,
	t_object.Classifier_guid,
	IIF(
    t_object.Object_Type IN ('Class', 'Interface'), 
    t_object.ea_guid,
    o2.ea_guid
	)) AS Class_Guid,
	o2.Note AS Class_Description
FROM ((((
    t_diagram
INNER JOIN 
    t_diagramobjects ON t_diagram.Diagram_ID = t_diagramobjects.Diagram_ID)
INNER JOIN 
    t_object ON t_diagramobjects.Object_ID = t_object.Object_ID)
LEFT JOIN 
    t_object o2 ON t_object.Classifier = o2.Object_ID)
INNER JOIN 
    t_package  ON t_diagram.Package_ID = t_package.Package_ID)
WHERE 
    t_diagram.Package_ID =#Package#;
