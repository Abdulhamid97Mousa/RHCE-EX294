SELECT version();

SELECT story FROM test_table
  WHERE id = %s OR story = 'Данные';
