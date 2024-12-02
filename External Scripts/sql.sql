--Bar Charts

--CARs - Trace Relation From ERs
SELECT 
    IIF(t_connector.Stereotype = "trace", 'Have', 'Do not have') AS Series
FROM 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement'
AND ( t_connector.Stereotype = "trace" or (t_connector.Stereotype IS NULL AND t_object.Object_ID NOT IN
(SELECT Object_ID
FROM
(SELECT 
		COUNT(t_object.Object_ID) AS count,t_object.Object_ID
FROM 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement'
GROUP BY t_object.Object_ID)
WHERE count>1)));

--CARs - Trace Relation From ERs - GroupBy Relation Type
SELECT 
    IIF(t_connector.Stereotype = "trace", 'Have', 'Do not have') AS Series,
	t_connector.Btm_Mid_Label AS GroupName
FROM(( 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID)
LEFT JOIN
    t_object AS o2 ON  o2.Object_ID = t_connector.Start_Object_ID)
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement';

--CARs - Trace Relation From ERs - GroupBy Element
SELECT 
    IIF(t_connector.Stereotype = "trace", 'Have', 'Do not have') AS Series,
	o2.Object_Type AS GroupName
FROM(( 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID)
LEFT JOIN
    t_object AS o2 ON  o2.Object_ID = t_connector.Start_Object_ID)
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement';

--Model View

--CARs That Have A Trace Relation To Them
SELECT o2.ea_guid as CLASSGUID, t_object.Name AS CAR_Name, 
    t_connector.Btm_Mid_Label AS RelationType, o2.Name AS ER_Name
FROM ((
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID)
LEFT JOIN
    t_object o2 ON o2.Object_ID = t_connector.Start_Object_ID)
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement'
AND t_connector.Stereotype = "trace";

--CARS That Have A Other Relation To Them
SELECT  o2.ea_guid as CLASSGUID,t_object.Name AS CAR_Name, 
    t_connector.Btm_Mid_Label AS RelationType, o2.Name AS ER_Name
FROM ((
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID)
LEFT JOIN
    t_object o2 ON o2.Object_ID = t_connector.Start_Object_ID)
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement'
AND(t_connector.Connector_ID IS NOT NULL AND t_connector.Stereotype IS NULL);

--CARs That Do Not Have A Trace Relation To Them
SELECT 
	 t_object.ea_guid as CLASSGUID,t_object.Name
FROM
	t_object
WHERE
	t_object.Package_ID =#Package#
AND 
	t_object.Object_Type='Requirement'
AND
	t_object.Object_ID NOT IN
(SELECT 
    t_object.Object_ID
FROM 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID
WHERE 
	t_object.Package_ID =#Package#
AND 
	t_connector.Stereotype = "trace");