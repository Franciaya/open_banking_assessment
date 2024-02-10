INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id, transaction_id) 
DO UPDATE SET 
    transaction_date = EXCLUDED.transaction_date,
    source_date = EXCLUDED.source_date,
    merchant_id = EXCLUDED.merchant_id,
    category_id = EXCLUDED.category_id,
    amount = EXCLUDED.amount,
    description = EXCLUDED.description,
    currency = EXCLUDED.currency
WHERE EXCLUDED.source_date > {table_name}.source_date;