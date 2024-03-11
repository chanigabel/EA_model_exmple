SELECT 
	t_object_end.ea_guid AS CLASSGUID, 
	't_object' AS CLASSTABLE, 
	t_object_end.Object_Type AS CLASSTYPE, 
	t_DiagramObjects.Diagram_ID, 
	t_Diagram.Name, 
	t_connector.Connector_ID, 
	t_connector.Connector_Type, 
	t_connector.Name
	AS Massege, 
	t_connector.Start_Object_ID AS Source_Object_ID, 
	t_object.Package_ID AS Source_Object_Packeg, 
	t_connector.End_Object_ID AS Target_Object_ID, 
	t_object_end.Package_ID AS Target_Object_Packeg, 
	IIF(
    t_object_end.Object_Type IN ('Class', 'Interface'), 
    t_object_end.Object_ID,
    t_object_end.Classifier
	) AS Source_Object_Classifier, 
	IIf(t_object_end.Object_Type In ('Class','Interface'),
	t_object_end.ea_guid,o2.ea_guid) 
	AS Guid_Classifier,
	IIF(t_connector.Connector_ID IN(
				SELECT 
					t_connector.Connector_ID
				FROM((((((((
					t_object
				INNER JOIN
					t_DiagramObjects ON t_object.Object_ID = t_DiagramObjects.Object_ID)
				INNER JOIN
					t_connector ON t_DiagramObjects.Diagram_ID = t_connector.DiagramID)
				INNER JOIN
					t_object AS t_object_end ON t_connector.End_Object_ID = t_object_end.Object_ID)
				LEFT JOIN 
					t_stereotypes ON t_object_end.stereotype = t_stereotypes.stereotype)
				LEFT JOIN 
					t_object o2 ON t_object_end.Classifier = o2.Object_ID)
				LEFT JOIN
					t_Diagram ON t_DiagramObjects.Diagram_ID = t_Diagram.Diagram_ID)
				LEFT JOIN 
					t_operation ON o2.Object_ID = t_operation.Object_ID)
				LEFT JOIN 
					t_operation AS o3 ON t_object_end.Object_ID = o3.Object_ID)
				WHERE 
					t_connector.Name IS NOT NULL AND
					(t_DiagramObjects.Object_ID = t_connector.Start_Object_ID 
					OR t_connector.Start_Object_ID = t_connector.End_Object_ID)
					AND (t_object_end.Object_Type NOT IN ('Class','Interface') OR (t_object_end.Object_Type IN ('Class','Interface') AND o3.Scope='Public'))
				GROUP BY
					t_object_end.ea_guid,
					t_object_end.Object_Type,
					t_DiagramObjects.Diagram_ID,
					t_Diagram.Name,
					t_connector.Connector_ID,
					t_connector.Connector_Type,
					t_connector.Name,
					t_operation.Name,
					t_connector.Start_Object_ID,
					t_object.Package_ID,
					t_connector.End_Object_ID,
					t_object.Classifier,
					t_connector.End_Object_ID,
					t_object_end.Package_ID,
					t_object_end.Classifier,
					IIF(
					t_object_end.Object_Type IN ('Class', 'Interface'), 
					t_object_end.ea_guid,
					o2.ea_guid
					),
					IIF(
					t_object_end.Object_Type IN ('Class', 'Interface'), 
					o3.Name,
					t_operation.Name 
					)	
					HAVING IIF(
					INSTR(1, t_connector.Name, '(') = 0,
					t_connector.Name,
					LEFT(t_connector.Name, INSTR(1, t_connector.Name, '(')- 1)
					) = IIF(
					t_object_end.Object_Type IN ('Class', 'Interface'), 
					o3.Name,
					t_operation.Name 
					)
				),1,0) AS FromMathod
FROM((((((
    t_object
INNER JOIN
    t_DiagramObjects ON t_object.Object_ID = t_DiagramObjects.Object_ID)
INNER JOIN
    t_connector ON t_DiagramObjects.Diagram_ID = t_connector.DiagramID)
INNER JOIN
    t_object AS t_object_end ON t_connector.End_Object_ID = t_object_end.Object_ID)
LEFT JOIN 
	t_stereotypes ON t_object_end.stereotype = t_stereotypes.stereotype)
LEFT JOIN 
    t_object o2 ON t_object_end.Classifier = o2.Object_ID)
LEFT JOIN
    t_Diagram ON t_DiagramObjects.Diagram_ID = t_Diagram.Diagram_ID)
WHERE 
	(t_DiagramObjects.Object_ID = t_connector.Start_Object_ID 
    OR t_connector.Start_Object_ID = t_connector.End_Object_ID)
GROUP BY
    t_object_end.ea_guid,
    t_object_end.Object_Type,
    t_DiagramObjects.Diagram_ID,
	t_Diagram.Name,
    t_connector.Connector_ID,
    t_connector.Connector_Type,
	t_connector.Name,
    t_connector.Start_Object_ID,
    t_object.Package_ID,
    t_connector.End_Object_ID,
    t_object.Classifier,
    t_connector.End_Object_ID,
    t_object_end.Package_ID,
	IIF(
    t_object_end.Object_Type IN ('Class', 'Interface'), 
    t_object_end.Object_ID,
    t_object_end.Classifier
	),
	IIF(
    t_object_end.Object_Type IN ('Class', 'Interface'), 
    t_object_end.ea_guid,
    o2.ea_guid
	)
ORDER BY t_connector.Connector_ID ASC
