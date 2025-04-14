import random
from datetime import datetime
import psycopg2
import faker

fake_data = faker.Faker()

DATABASE_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "user": "admin",
    "password": "postgres",
    "database": "financial_db"
}

TABLE_NAME = "transactions"

def generate_transaction():
    return {
        "transactionId": fake_data.uuid4(),
        "username": fake_data.user_name(),
        "timestamp": datetime.now(),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(["USD", "GBP"]),
        "city": fake_data.city(),
        "country": fake_data.country(),
        "merchantName": fake_data.company(),
        "paymentMethod": random.choice(["credit_card", "debit_card", "online_transfer"]),
        "ipAddress": fake_data.ipv4(),
        "voucherCode": random.choice(["DISCOUNT10", "DISCOUNT15", "DISCOUNT20"]),
        "affiliateId": fake_data.uuid4()
    }

def create_table(cursor, table_name):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            transactionId UUID PRIMARY KEY,
            username VARCHAR(255),
            timestamp TIMESTAMP,
            amount DECIMAL,
            currency VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            merchantName VARCHAR(255),
            paymentMethod VARCHAR(255),
            ipAddress INET,
            voucherCode VARCHAR(255),
            affiliateId UUID
        )
    """)

def insert_data(cursor, table_name, data):
    cursor.execute(f"""
        INSERT INTO {table_name} (transactionId, username, timestamp, amount, currency, city, country, merchantName, paymentMethod, ipAddress, voucherCode, affiliateId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [data["transactionId"], data["username"], data["timestamp"], data["amount"], data["currency"], data["city"], data["country"],
        data["merchantName"], data["paymentMethod"], data["ipAddress"], data["voucherCode"], data["affiliateId"]]
    )

if __name__ == "__main__":
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()

    create_table(cur, TABLE_NAME)

    transaction = generate_transaction()
    print(transaction)

    insert_data(cur, TABLE_NAME, transaction)

    conn.commit()
    cur.close()
    conn.close()