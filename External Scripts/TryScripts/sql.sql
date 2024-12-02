req:
pie:
SELECT 
    IIF(t_connector.Connector_ID IS NOT NULL, 'Connected', 'Not Connected') AS Series
FROM 
    t_object
LEFT JOIN 
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID
WHERE 
t_object.Package_ID =214
AND t_object.Object_Type='Requirement';

model view:
SELECT 
    req.Name AS RequirementName,
    IIF(t_connector.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
	uc.Name AS UseCaseName
FROM((
    t_object AS req
LEFT JOIN 
    t_connector ON t_connector.End_Object_ID = req.Object_ID)
LEFT JOIN
	t_object AS uc ON uc.Object_ID = t_connector.Start_Object_ID)
WHERE 
    req.Package_ID = 214
	AND req.Object_Type='Requirement';

UseCase:
pie:
SELECT 
    IIF(sub.Connector_ID IS NOT NULL, 'Connected', 'Not Connected') AS Series
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = 168
    AND uc.Object_Type = "UseCase"

model view:
SELECT 
    uc.Name AS UseCaseName,
    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
    sub.RequirementName
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = 168
    AND uc.Object_Type = "UseCase"









    SELECT 
    uc.Name AS UseCaseName,
    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
    sub.RequirementName
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = #Package#
	AND uc.Object_Type = "UseCase"





    SELECT 
    uc.Name AS ElementName,
    IIF(sub.Connector_ID IS NOT NULL, 'Connected to', 'Not Connected') AS Connection,
    sub.RequirementName
FROM
    t_object AS uc
LEFT JOIN 
(
    SELECT 
        t_connector.Connector_ID,
        t_connector.Start_Object_ID,
        req.Name AS RequirementName
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = #Package#





the true:
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
    req.Package_ID = 168
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
        req.Name AS RequirementName
    FROM
        t_connector
    LEFT JOIN 
        t_object AS req ON req.Object_ID = t_connector.End_Object_ID
    WHERE 
        req.Object_Type = 'Requirement'
) AS sub ON sub.Start_Object_ID = uc.Object_ID
WHERE 
    uc.Package_ID = 168
	AND
	uc.Object_Type<>'Requirement'






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
    req.Package_ID = 215
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
    uc.Package_ID = 215
	AND
	(uc.Object_Type<>'Requirement' OR (uc.Object_Type='Requirement' AND (sub.Object_Type='Requirement')))