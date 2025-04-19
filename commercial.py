##############################
####  ANALYSE COMMERCIAL #######
##############################

##########importation###########
import pandas as pd

##############################

#######chargement de données#####
pd.set_option('display.max_row', 500)
#1-donnees sur les client
df_client = pd.read_csv('customers.csv')

#2-donnees sur les produts vendus
df_prod = pd.read_csv('products.csv')

#3-information sur la vente
df_vent = pd.read_csv('sales_data.csv', parse_dates=['date'])
##############################

###########fusion des donnee#####
#fusion de df_prod et df_vent
df_aff = pd.merge(df_prod, df_vent, on='product_id')

#fusion df_aff et df_client
df = pd.merge(df_client, df_aff, on='customer_id')
##############################


#######exploration de donnee#######
print('----------------exploration des donnees-----------------')
print('dimensions : ', df.shape)
print('valeur manquante :\n', df.isnull().sum())
print('doublons : ', df.duplicated().sum())
print('types de donnee : \n', df.dtypes)
##############################

#######creation de colonne utile#####
#creation de la colonne mois
df['mois'] = df['date'].dt.to_period('M')
#creation d'une colonne benefice
df['benefice'] = df.unit_price - df.cost_price

#colonne ca
df['CA'] = df.quantity * df.unit_price
##############################


#########analyse des vents########

#le CA par pays, produit et par mois
CA = df.groupby('product_name').CA.sum().sort_values().rename('CA')

#benefie par produit
benefice = df.groupby('product_name').benefice.sum().sort_values().rename('benefice')

#rendement des produit
rendement = (benefice/CA).rename('rendement')

#resultat 
df_resul = pd.concat([CA, benefice, rendement], axis=1)

print('-----------------------analyse des ventes-------------------')
print(df_resul)
##############################


#########analyse des client########
#nombres d'achat pour chaque client
nbrs_achat = df.name.value_counts().rename('nbres_achat')

#quantite achete par client
quantt = df.groupby('name').quantity.sum().sort_values(ascending=False).rename('quantité')

#revenu genere par les client vip et non vip
rev = df.groupby('is_vip').unit_price.sum()

#resultat
df_resul1 = pd.concat([nbrs_achat, quantt], axis=1)

print('----------------------analyse sur les client---------------')
print('les client les plus fidels : \n', df_resul1[:4])
print('les client qui genere le plus de revenu: \n', rev)
##############################

##########analyse temporaire######
#volume de vent par period
vent_period = df.groupby('mois').quantity.sum().rename('volume_vent')

#volume de vent par saison et par zone
vent_zone = df.groupby(['mois', 'country']).quantity.sum()

print('--------------------------analyse temporaire----------------------')
print('volume de vent par moi : \n'  ,vent_zone)
##############################

#############bloc note##########
"""
-Chiffre d'affaire le plus haut: le CA le plus eleves est celui de l'eau minerale
-benefice le plus eleves : thon en boite
-rendement plus eleves : chaucolat noir
-les client les plus fidels:client1, 16, 21, il sont vip
-les client qui genere le plus de revenu : client_vip
-mois ou il y a des pic : 6 et 12 eme mois
-le senegal perfome le plus durant toute l'annee
"""
##############################
