INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id) 
DO UPDATE SET 
    transaction_date = EXCLUDED.transaction_date
WHERE EXCLUDED.transaction_date > {table_name}.transaction_date;