import pandas as pd
customers = pd.read_csv("/olist_customers_dataset.csv")
orders = pd.read_csv("/olist_orders_dataset.csv")
order_items = pd.read_csv("/olist_order_items_dataset.csv")
payments = pd.read_csv("/olist_order_payments_dataset.csv")
products = pd.read_csv("/olist_products_dataset.csv")
reviews = pd.read_csv("/olist_order_reviews_dataset.csv")
sellers = pd.read_csv("/olist_sellers_dataset.csv")
geolocation = pd.read_csv("/olist_geolocation_dataset.csv")

print(customers.head())
print(customers.shape)

print(orders.head())      
print(orders.shape)     

print(order_items.head())
print(order_items.shape)

print(payments.head())
print(payments.shape)

print(products.head())
print(products.shape)

print(reviews.head())
print(reviews.shape)

print(sellers.head())
print(sellers.shape)

print(geolocation.head())
print(geolocation.shape)

datasets = {
    "Customers": customers,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Products": products,
    "Reviews": reviews,
    "Sellers": sellers,
    "Geolocation": geolocation
}

for name, df in datasets.items():
    print(f"\n{name}")
    print("-" * 30)
    print("Missing Values:")
    print(df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())
    print("\nData Types:")
    print(df.dtypes)
