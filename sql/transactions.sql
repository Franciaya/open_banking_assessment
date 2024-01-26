CREATE TABLE IF NOT EXISTS transactions (
                customer_id VARCHAR(255),
                transaction_id VARCHAR(255),
                transaction_date DATE,
                source_date TIMESTAMP,
                merchant_id VARCHAR(255),
                category_id VARCHAR(255),
                amount DECIMAL,
                description VARCHAR(255),
                currency VARCHAR(3),
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (customer_id, transaction_id)
);