CREATE FUNCTION add(integer, integer) RETURNS integer
  AS 'select $1 + $2;'
  LANGUAGE SQL
  IMMUTABLE
  RETURNS NULL ON NULL INPUT;

SELECT story FROM test_table
  WHERE id = %s OR story = 'Данные';

SELECT version();
