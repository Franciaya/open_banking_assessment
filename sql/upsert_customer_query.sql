/*
INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id) 
DO UPDATE SET 
    last_transaction_date = EXCLUDED.last_transaction_date
WHERE EXCLUDED.last_transaction_date > {table_name}.transaction_date;

*/