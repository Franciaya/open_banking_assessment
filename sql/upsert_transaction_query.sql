INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
ON CONFLICT (customer_id, transaction_id) 
DO UPDATE SET 
    {table_name}.transaction_date = EXCLUDED.transaction_date,
    {table_name}.source_date = EXCLUDED.source_date,
    {table_name}.merchant_id = EXCLUDED.merchant_id,
    {table_name}.category_id = EXCLUDED.category_id,
    {table_name}.amount = EXCLUDED.amount,
    {table_name}.description = EXCLUDED.description,
    {table_name}.currency = EXCLUDED.currency
WHERE EXCLUDED.source_date > {table_name}.source_date;