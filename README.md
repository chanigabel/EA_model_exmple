06/02
At first, I searched for all the existing tables, but I couldn't find any documentation detailing the tables. 
only  a few important tables. Then, I started making queries to retrieve different tables, 
attempting to understand how the data is structured and what information is contained in the queries. 
Finally, I began creating queries with joins to retrieve Connectors along with the objects belonging to them
07/02
I encountered a problem: how to create a search in the diagram and browser within a table of connectors with joins to additional tables. 
I spent some time on it, but didn't succeed. For now, it's defined in the search as the starting object. 
Then, I attempted to create a query that would retrieve the objects of the connector along with their packages, which took some time. 
Finally, I sorted out the GitHub permissions and uploaded the queries in the form of SQL files, The second file contains all the SQL queries saved. 
I tried to describe the purpose of each query.
FID - Find in Diagram
S/E - Start - End
08/02
I created various queries to configure display options. An SQL file named '08-02' has been uploaded containing these queries. The diagram query works partially; however, in the object query, the diagram is also displayed. Additionally, in the class query, there are objects without a class, meaning that some objects cannot be associated with a specific class in the project.
12/02
I modified the queries so that there wouldn't be subqueries. I added a search according to a specific diagram. 
I tried to understand exactly how the data is stored in the tables - where the operations and properties are. 
I didn't understand exactly how to bring them without creating duplicates in the number of objects. 
(The queries are in an XML file (is it correct?) -  in the name "11-2 12-2" and arranged there according to date, 
I hope it's clear, if not - I'd be happy to know).
In general - I registered for the forum and received an email that the administration needs to check if I can join and I will receive a notification about it - I haven't received it yet.
I couldn't run queries with comments as we discussed - #DB=ORACLE# and I didn't want to get stuck on that.
13/2
As far as I understood, I was supposed to progress in a query that would bring me all the objects existing in each diagram that do not belong to the package of the diagram and to find their class. I attached the tables t_diagram, t_diagramobjects, t_object, t_package.  the table t_object join twice, once as an object and once as its class. The query brought what was needed, but I noticed there are too few results. I modified the SQL so that even records without a class will be obtained, and it turned out that there are indeed objects that do not belong to any class - some that I never created through a class, and some that simply do not belong, like actors. This led me to the conclusion that I probably missed something... maybe I didn't understand exactly what is needed, or where - which objects, which classes. I thought maybe I need to bring the operations and attributes, and I made queries like that - with permutations. But as far as I checked in the diagrams, I do get them even when they are not in the original package. So I tried to think maybe it's about objects that don't exist in my model, but even in a sample project, it didn't give different results.