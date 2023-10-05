--- 001_source_MySQL_GPT_query.sql
--- source MySQL for GPT query  
--- QUERY :: In MySQL, write the code in order to create a table named users with the following fields : FirstName, LastName, email, address, country. The user id must be a key and incremental.



--- Sure, here's the code to create a MySQL table named "users" with the specified fields:


CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  FirstName VARCHAR(50),
  LastName VARCHAR(50),
  email VARCHAR(100),
  address VARCHAR(200),
  country VARCHAR(50)
);


--- This code creates a table with six columns: "id" (the primary key), "FirstName", "LastName", "email", "address", and "country". The "id" column is defined as an auto-incrementing integer, which means that it will automatically generate a new, unique value for each new row that is inserted into the table.

