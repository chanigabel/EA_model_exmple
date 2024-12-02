SELECT DISTINCT  
	sub.ea_guid AS CLASSGUID,
    sub.Object_Type AS CLASSTYPE,
	obj1.Name, 
#DB=ORACLE#
    --Bar Charts
    --ERs - Trace Relation To CARs
	-- Changed by CJ 2024-11-20
#DB=ORACLE#
       IIF(sub.Connector_ID IS NOT NULL, 'Have', 'Do not have') AS Series
FROM
    t_object AS obj1
LEFT JOIN 
(
    SELECT 
        t_connector.Start_Object_ID,
        t_connector.Connector_ID,
        obj2.ea_guid,
        obj2.Object_Type,
        t_connector.Btm_Mid_Label,
        obj2.Name
    FROM
        t_connector
    LEFT JOIN 
        t_object AS obj2 ON obj2.Object_ID = t_connector.End_Object_ID
    WHERE 
        obj2.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = obj1.Object_ID
WHERE 
    obj1.Package_ID = #Package#;



SELECT DISTINCT
    sub.ea_guid AS CLASSGUID,
    sub.Object_Type AS CLASSTYPE,
    obj1.Name AS Name,
    sub.Btm_Mid_Label AS connLabel,
    sub.Name AS Name2,
    sub.Object_Type AS Type2
	#DB=ORACLE#
	-- Model View for ERs
	-- Changed by CJ 2024-11-20
	#DB=ORACLE#
FROM
    t_object AS obj1
LEFT JOIN 
(
    SELECT 
        t_connector.Start_Object_ID,
        obj2.ea_guid,
        obj2.Object_Type,
        t_connector.Btm_Mid_Label,
        obj2.Name
    FROM
        t_connector
    LEFT JOIN 
        t_object AS obj2 ON obj2.Object_ID = t_connector.End_Object_ID
    WHERE 
        obj2.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = obj1.Object_ID
WHERE 
    obj1.Package_ID = #Package#;