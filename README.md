# E-commerce API - FastAPI Backend

Ce projet est une API REST pour un site e-commerce développée avec FastAPI et SQLite.

## 🚀 Installation et démarrage

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration des variables d'environnement (.env)

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```env
SECRET_KEY=change-me-very-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///database.db
```

- **SECRET_KEY** : Clé secrète pour le JWT (changez-la en production)
- **ALGORITHM** : Algorithme utilisé pour le JWT
- **ACCESS_TOKEN_EXPIRE_MINUTES** : Durée de validité du token (en minutes)
- **DATABASE_URL** : URL de connexion à la base de données SQLite

### Démarrage du serveur

```bash
# Démarrer le serveur de développement
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur sera accessible à l'adresse : `http://127.0.0.1:8000`

## 🛣️ Routes disponibles

### 1. Route racine
- **GET** `/`
- **Description** : Page d'accueil de l'API
- **Réponse** : Message de bienvenue

### 2. Gestion des produits

#### Liste des produits
- **GET** `/products`
- **Description** : Récupère la liste de tous les produits
- **Réponse** : Liste des produits avec id, nom, prix, description

#### Détail d'un produit
- **GET** `/products/{product_id}`
- **Description** : Récupère les détails d'un produit spécifique
- **Paramètres** : `product_id` (int) - ID du produit
- **Réponse** : Détails du produit ou erreur 404 si non trouvé

#### Ajouter un produit
- **POST** `/products`
- **Description** : Ajoute un nouveau produit à la base de données
- **Body** :
```json
{
  "name": "Nom du produit",
  "price": 29.99,
  "description": "Description du produit"
}
```

### 3. Authentification

#### Inscription
- **POST** `/auth/register`
- **Description** : Crée un nouveau compte utilisateur
- **Body** :
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```
- **Réponse** : Détails de l'utilisateur créé

#### Connexion
- **POST** `/auth/login`
- **Description** : Authentifie un utilisateur
- **Body** :
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- **Réponse** : Token JWT et informations utilisateur

### 4. Gestion du panier

#### Récupérer le panier
- **GET** `/cart`
- **Description** : Récupère le panier d'un utilisateur
- **Paramètres** : `user_id` (int) - ID de l'utilisateur
- **Réponse** : Liste des items dans le panier

#### Ajouter au panier
- **POST** `/cart/add`
- **Description** : Ajoute un produit au panier
- **Body** :
```json
{
  "user_id": 1,
  "product_id": 2,
  "quantity": 3
}
```
- **Réponse** : Item ajouté au panier

## 🗄️ Structure de la base de données

### Tables

#### Products
- `id` (int, primary key)
- `name` (string)
- `price` (float)
- `description` (string)

#### Users
- `id` (int, primary key)
- `email` (string, unique)
- `username` (string)
- `password` (string, hashé)

#### CartItems
- `id` (int, primary key)
- `user_id` (int, foreign key)
- `product_id` (int, foreign key)
- `quantity` (int)

## 🔧 Configuration

### Base de données
- **Type** : SQLite
- **Fichier** : `database.db` (créé automatiquement)
- **ORM** : SQLModel

### Sécurité
- **Hash des mots de passe** : SHA-256
- **JWT** : Pour l'authentification
- **CORS** : Configuré pour permettre toutes les origines

## 👤 Utilisateur admin par défaut

> **La base de données contient un utilisateur par défaut :**
> - **Email :** admin@test.com
> - **Mot de passe :** admin

## 📝 Exemples d'utilisation

### Créer un compte
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### Se connecter
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Récupérer les produits
```bash
curl -X GET "http://127.0.0.1:8000/products"
```

### Ajouter au panier
```bash
curl -X POST "http://127.0.0.1:8000/cart/add" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 2,
    "quantity": 1
  }'
```

## 🚨 Notes importantes

1. **Base de données** : La base SQLite est créée automatiquement au premier démarrage
2. **Données de test** : Des produits et un utilisateur admin sont créés automatiquement
3. **CORS** : Configuré pour le développement (permet toutes les origines)
4. **Sécurité** : En production, changez la clé secrète JWT et utilisez bcrypt pour le hash des mots de passe

## 🔄 Prochaines étapes

- [ ] Implémenter la vérification JWT pour sécuriser les routes
- [ ] Ajouter la gestion des commandes
- [ ] Implémenter la gestion des catégories de produits
- [ ] Ajouter la validation des données
- [ ] Implémenter la pagination pour les listes 