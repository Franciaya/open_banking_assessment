INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id, transaction_id) 
DO UPDATE SET {update_columns}
WHERE EXCLUDED.audit_timestamp > {table_name}.audit_timestamp;