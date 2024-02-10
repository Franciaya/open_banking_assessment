CREATE TABLE IF NOT EXISTS customers (
                customer_id VARCHAR(255) NOT NULL,
                transaction_date DATE NOT NULL,
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (customer_id)
);
CREATE TABLE IF NOT EXISTS transactions (
                customer_id VARCHAR(255) NOT NULL,
                transaction_id VARCHAR(255) NOT NULL,
                transaction_date DATE NOT NULL,
                source_date TIMESTAMP,
                merchant_id VARCHAR(255),
                category_id VARCHAR(255),
                amount DECIMAL NOT NULL,
                description VARCHAR(255),
                currency VARCHAR(3) NOT NULL,
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (customer_id, transaction_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE IF NOT EXISTS error_log_tab (
                customer_id VARCHAR(255),
                transaction_id VARCHAR(255),
                error_message VARCHAR(255),
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);