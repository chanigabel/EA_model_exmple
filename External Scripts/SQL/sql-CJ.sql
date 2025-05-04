SELECT DISTINCT
t_object.ea_guid AS CLASSGUID,t_object.Object_ID AS CLASSTYPE,t_object.Name, 
#DB=ORACLE#
--Bar Charts
--CARs - Trace Relation From ERs
-- Changes by CJ 2024-11-20 1) Added another condition is that if CAR has more than one connection 
-- it will take the 'trace' type connection. 
-- (Does not help if there is a CAR with more than one connection that does not have a 'trace' connection.)

#DB=ORACLE#
    IIF(t_connector.Stereotype = 'trace', 'Have', 'Do not have') AS Series
FROM 
    t_object
LEFT JOIN
    t_connector ON t_connector.End_Object_ID = t_object.Object_ID
WHERE 
t_object.Package_ID =#Package#
AND t_object.Object_Type='Requirement'
AND ( t_connector.Stereotype = 'trace' or (t_connector.Stereotype IS NULL AND t_object.Object_ID NOT IN
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
WHERE count>1)))