--- 003_source_MySQL_GPT_sqllite_create_countries_table.sql.sql
--- source sqllite for GPT query  
--- QUERY :: In SQLite, write the code to create a table named countries with the following fields: name, tld, email, cca2, capital, callingCode. The user id must be a key and incremental.

--- Here's the SQLite code to create a table named "countries" with the specified fields:



CREATE TABLE countries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  tld TEXT,
  email TEXT,
  cca2 TEXT,
  capital TEXT,
  callingCode TEXT
);


---  In this code, the "id" field is defined as the primary key with the "INTEGER" data type, and it is set to auto-increment using the "AUTOINCREMENT" keyword. The remaining fields are defined with their respective data types of "TEXT".


