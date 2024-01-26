CREATE TABLE IF NOT EXISTS error_log_tab (
                customer_id VARCHAR(255),
                transaction_id VARCHAR(255),
                error_message VARCHAR(255),
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);