-- 6. Bar Chart: ERs and Relations to CARs

-- ERs that have or do not have a trace relation to CARs, grouped by type of element
SELECT
    IIF(t_connector.Stereotype = 'trace', 'Have Trace', 'Do Not Have Trace') AS Series,
    o2.Object_Type AS Element_Type,
    COUNT(DISTINCT o2.Object_ID) AS Count
FROM
    t_object AS CARs
LEFT JOIN
    t_connector ON CARs.Object_ID = t_connector.End_Object_ID
LEFT JOIN
    t_object AS o2 ON o2.Object_ID = t_connector.Start_Object_ID
WHERE
    CARs.Package_ID = #Package#
    AND CARs.Object_Type = 'Requirement' -- CAR perspective
    AND (o2.Object_Type IN ('UseCase', 'Requirement', 'Activity', 'Action')
         OR (o2.Stereotype = 'Capability' AND o2.Object_Type = 'Operation')) -- ER/AdER types
GROUP BY
    IIF(t_connector.Stereotype = 'trace', 'Have Trace', 'Do Not Have Trace'),
    o2.Object_Type;

-- 7. ModelView: ERs with Trace Relation to CARs
SELECT DISTINCT
    o2.Package_ID AS ER_Package,
    o2.ParentID AS ER_Parent,
    o2.Name AS ER_Name,
    o2.Object_Type AS ER_Type,
    o2.Alias AS ER_Alias
FROM
    t_object AS CARs
LEFT JOIN
    t_connector ON CARs.Object_ID = t_connector.End_Object_ID
LEFT JOIN
    t_object AS o2 ON o2.Object_ID = t_connector.Start_Object_ID
WHERE
    CARs.Package_ID = #Package#
    AND CARs.Object_Type = 'Requirement' -- CAR perspective
    AND t_connector.Stereotype = 'trace'
    AND (o2.Object_Type IN ('UseCase', 'Requirement', 'Activity', 'Action')
         OR (o2.Stereotype = 'Capability' AND o2.Object_Type = 'Operation'));

-- 8. ModelView: ERs without Trace Relation to CARs
SELECT DISTINCT
    o2.Package_ID AS ER_Package,
    o2.ParentID AS ER_Parent,
    o2.Name AS ER_Name,
    o2.Object_Type AS ER_Type,
    o2.Alias AS ER_Alias
FROM
    t_object AS CARs
LEFT JOIN
    t_connector ON CARs.Object_ID = t_connector.End_Object_ID
LEFT JOIN
    t_object AS o2 ON o2.Object_ID = t_connector.Start_Object_ID
WHERE
    CARs.Package_ID = #Package#
    AND CARs.Object_Type = 'Requirement' -- CAR perspective
    AND (t_connector.Connector_ID IS NULL OR t_connector.Stereotype <> 'trace')
    AND (o2.Object_Type IN ('UseCase', 'Requirement', 'Activity', 'Action')
         OR (o2.Stereotype = 'Capability' AND o2.Object_Type = 'Operation'));

-- 9. ModelView: ERs with Non-Trace Relations to CARs
SELECT DISTINCT
    o2.Package_ID AS ER_Package,
    o2.ParentID AS ER_Parent,
    o2.Name AS ER_Name,
    o2.Object_Type AS ER_Type,
    o2.Alias AS ER_Alias,
    t_connector.Stereotype AS Relation_Type
FROM
    t_object AS CARs
LEFT JOIN
    t_connector ON CARs.Object_ID = t_connector.End_Object_ID
LEFT JOIN
    t_object AS o2 ON o2.Object_ID = t_connector.Start_Object_ID
WHERE
    CARs.Package_ID = #Package#
    AND CARs.Object_Type = 'Requirement' -- CAR perspective
    AND t_connector.Stereotype <> 'trace'
    AND (o2.Object_Type IN ('UseCase', 'Requirement', 'Activity', 'Action')
         OR (o2.Stereotype = 'Capability' AND o2.Object_Type = 'Operation'));

-- Notes:
-- - Replace #Package# with the actual Package ID for the specific ERs and AdERs package.
-- - The grouping in the bar chart query supports distinguishing by ER types and AdER types.
-- - Lists for ModelView include Package, Parent, ER Name, ER Type, Alias, and Relation Type where applicable.
-- - To adapt these queries for a specific package dynamically, consider embedding them in a script with user input or configuration settings.
