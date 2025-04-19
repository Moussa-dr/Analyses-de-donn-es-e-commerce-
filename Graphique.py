import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des fichiers CSV
sales = pd.read_csv("sales_data.csv")
products = pd.read_csv("products.csv")
customers = pd.read_csv("customers.csv")

# Fusion des trois fichiers
df = sales.merge(products, on="product_id").merge(customers, on="customer_id")

# Calcul du chiffre d'affaires
df["CA"] = df["quantity"] * df["unit_price"]

# Extraire le mois
df["mois"] = pd.to_datetime(df["date"]).dt.to_period("M")

ca_produit = df.groupby("product_name")["CA"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=ca_produit.values, y=ca_produit.index, palette="crest")
plt.title("Chiffre d'affaires par produit")
plt.xlabel("CA total (FCFA)")
plt.ylabel("Produit")
plt.tight_layout()


volume_mois = df.groupby("mois")["quantity"].sum()

plt.figure(figsize=(10, 5))
volume_mois.plot(marker="o", color="darkorange")
plt.title("Volume de vente par mois")
plt.xlabel("Mois")
plt.ylabel("Quantité vendue")
plt.grid(True)
plt.tight_layout()
plt.show()

ventes_pays = df.groupby("country")["CA"].sum()

plt.figure(figsize=(6, 6))
ventes_pays.plot(kind="pie", autopct="%1.1f%%", startangle=140, colors=sns.color_palette("Set2"))
plt.title("Répartition du chiffre d'affaires par pays")
plt.ylabel("")
plt.tight_layout()
plt.show()