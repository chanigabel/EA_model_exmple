SELECT 
    req.Name AS RequirementName,
    IIF(t_connector.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
	uc.Name AS TracesFrom
FROM((
    t_object AS req
LEFT JOIN 
    t_connector ON t_connector.End_Object_ID = req.Object_ID)
LEFT JOIN
	t_object AS uc ON uc.Object_ID = t_connector.Start_Object_ID)
WHERE 
    req.Package_ID = #Package#
	AND req.Object_Type='Requirement';










    SELECT 
    elem.Name AS ElementName,
    IIF(req.Connector_ID IS NOT NULL AND (req.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 'Connected to', 'Not Connected') AS Connection,
	IIF(req.Connector_ID IS NOT NULL AND (req.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), req.RequirementName, '') AS RequirementName
FROM
    t_object AS elem
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName,
		req.Object_Type
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
) AS req ON req.Start_Object_ID = elem.Object_ID
WHERE  
    elem.Package_ID = 168










    SELECT DISTINCT 
    elem.Name AS ElementName,
    IIF(outConn.Connector_ID IS NOT NULL AND 
       (targetElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
       'Connected to ', 
       IIF(inConn.Connector_ID IS NOT NULL AND 
          (sourceElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
          'Connected from ', 
          'Not Connected')) AS Connection,
    IIF(outConn.Connector_ID IS NOT NULL AND 
       (targetElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
       targetElem.Name, 
       IIF(inConn.Connector_ID IS NOT NULL AND 
          (sourceElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
          sourceElem.Name, 
          '')) AS TargetElementName
FROM((((
    t_object AS elem
LEFT JOIN 
    t_connector AS outConn ON outConn.Start_Object_ID = elem.Object_ID)
LEFT JOIN 
    t_object AS targetElem ON targetElem.Object_ID = outConn.End_Object_ID)
LEFT JOIN 
    t_connector AS inConn ON inConn.End_Object_ID = elem.Object_ID)
LEFT JOIN 
    t_object AS sourceElem ON sourceElem.Object_ID = inConn.Start_Object_ID)
WHERE 
    elem.Package_ID = 168;












    ALLLLLLLL3
    SELECT 
    req.Name AS ElementName,
    IIF(t_connector.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
	uc.Name AS Traces
FROM((
    t_object AS req
LEFT JOIN 
    t_connector ON t_connector.End_Object_ID = req.Object_ID)
LEFT JOIN
	t_object AS uc ON uc.Object_ID = t_connector.Start_Object_ID)
WHERE 
    req.Package_ID = 214
	AND req.Object_Type='Requirement'
UNION
SELECT 
    uc.Name AS ElementName,
    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
    sub.RequirementName AS Traces
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName,
		req.Object_Type
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = 214
	AND
	uc.Object_Type<>'Requirement'
UNION
SELECT 
	uc.name AS ElementName,
    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected')  AS Connection,
	sub.RequirementName AS Traces
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName,
		req.Object_Type
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = 214
AND 
    uc.Object_Type = 'Requirement'













SELECT DISTINCT elem.Name AS ElementName,
    IIF(outConn.Connector_ID IS NOT NULL AND 
       (targetElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
       'Connected to ', 
       IIF(inConn.Connector_ID IS NOT NULL AND 
          (sourceElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
          'Connected from ', 
          'Not Connected')) AS Connection,
    IIF(outConn.Connector_ID IS NOT NULL AND 
       (targetElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
       targetElem.Name, 
       IIF(inConn.Connector_ID IS NOT NULL AND 
          (sourceElem.Object_Type = 'Requirement' OR elem.Object_Type = 'Requirement'), 
          sourceElem.Name, 
          '')) AS TargetElementName
FROM((((
    t_object AS elem
LEFT JOIN 
    t_connector AS outConn ON outConn.Start_Object_ID = elem.Object_ID)
LEFT JOIN 
    t_object AS targetElem ON targetElem.Object_ID = outConn.End_Object_ID)
LEFT JOIN 
    t_connector AS inConn ON inConn.End_Object_ID = elem.Object_ID)
LEFT JOIN 
    t_object AS sourceElem ON sourceElem.Object_ID = inConn.Start_Object_ID)
WHERE 
    elem.Package_ID = 168
