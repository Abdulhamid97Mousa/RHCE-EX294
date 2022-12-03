SELECT version();

SELECT story FROM test_table
  WHERE id = %(item)s OR story = 'Данные';
