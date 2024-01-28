/*

INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id, transaction_id) 
DO UPDATE SET {update_columns}
WHERE EXCLUDED.audit_timestamp > {table_name}.audit_timestamp;

*/

/*
INSERT INTO transactions (customer_id, transaction_id, transaction_date, source_date, merchant_id, category_id, amount, description, currency)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (customer_id, transaction_id)
DO UPDATE SET
    transaction_date = EXCLUDED.transaction_date,
    source_date = EXCLUDED.source_date,
    merchant_id = EXCLUDED.merchant_id,
    category_id = EXCLUDED.category_id,
    amount = EXCLUDED.amount,
    description = EXCLUDED.description,
    currency = EXCLUDED.currency;

*/