from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from models import Product, User, CartItem
from database import create_db_and_tables, engine
from auth import verify_password, create_access_token, hash_password

app = FastAPI()

# Configuration CORS pour permettre toutes les origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les headers
)

# Création de la base de données et des tables + insertion de produits de test
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    insert_sample_products()

def insert_sample_products():
    with Session(engine) as session:
        if not session.exec(select(Product)).first():  # Pour éviter les doublons
            session.add_all([
                User(email="admin@test.com", username="admin", password=hash_password("admin")),
                Product(name="Chaussures", price=59.99, description="Chaussures de sport confortables"),
                Product(name="T-shirt", price=19.99, description="T-shirt 100% coton"),
                Product(name="Casquette", price=14.99, description="Casquette stylée pour l'été"),
                Product(name="Jean", price=49.99, description="Jean classique en denim"),
                Product(name="Sneakers", price=79.99, description="Sneakers tendance et confortables"),
                Product(name="Pull", price=39.99, description="Pull chaud pour l'hiver"),
                Product(name="Sac à dos", price=29.99, description="Sac à dos pratique pour tous les jours"),
                Product(name="Montre", price=129.99, description="Montre élégante et précise"),
                Product(name="Écharpe", price=24.99, description="Écharpe douce et chaude"),
                Product(name="Gants", price=19.99, description="Gants confortables pour l'hiver"),
                Product(name="Ceinture", price=34.99, description="Ceinture en cuir de qualité"),
            ])
            session.commit()

@app.get("/")
def read_root():
    return {"message": "Welcome to my E-commerce demo"}

#Retourne la liste des produits de la base de données
@app.get("/products", response_model=List[Product])
def get_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

#Retourne un produit à partir de l'id
@app.get("/products/{product_id}", response_model=Product)
def get_product_detail(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produit non trouvé")
        return product

#Ajouter un nouveau produit dans la base de données
@app.post("/products", response_model=Product)
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

#Recuperer le panier
@app.get("/cart", response_model=List[CartItem])
def get_cart(user_id: int):
    with Session(engine) as session:
        cart = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
    return cart

#Ajouter des produits dans le panier
@app.post("/cart/add", response_model=CartItem)
def add_to_cart(user_id: int = Body(...), product_id: int = Body(...), quantity: int = Body(...)):
    with Session(engine) as session:
        # Vérifier si l'item existe déjà pour cet utilisateur et ce produit
        cart_item = session.exec(
            select(CartItem).where(
                (CartItem.user_id == user_id) & (CartItem.product_id == product_id)
            )
        ).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(cart_item)
        session.commit()
        session.refresh(cart_item)
        return cart_item

@app.post("/auth/login")
def login(email: str = Body(...), password: str = Body(...)):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"email": user.email, "user_id": user.id})
        return {"token": token, "user": {"id": user.id, "email": user.email, "username": user.username}}

@app.post("/auth/register")
def register(email: str = Body(...), username: str = Body(...), password: str = Body(...)):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already taken")
        user = User(email=email, username=username, password=hash_password(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"user_id": user.id, "user": {"id": user.id, "email": user.email, "username": user.username}}
    