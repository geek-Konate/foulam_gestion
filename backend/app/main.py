import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import AsyncSessionLocal
from app.scripts.seed_permissions import seed_permissions
from app.scripts.seed_superadmin import seed_superadmin

# ────────────────────────────────────────────────
# INITIALISATION FASTAPI
# ────────────────────────────────────────────────
app = FastAPI(
    title="Authentifia Backend API",
    description="API de Generation  académique",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du routeur principal avec le préfixe global /api/v1
try:
    from app.api.routers import api_router
    app.include_router(api_router, prefix="/api")
    print("✅ API Router enregistré avec succès")

except Exception as e:
    print("❌ Impossible d'enregistrer les routes")
    print(f"Erreur : {type(e).__name__}")
    print(f"Détails : {e}")

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Store ERP API. Go to /docs for the documentation."}

# ────────────────────────────────────────────────
# ENDPOINT ROOT
# ────────────────────────────────────────────────
@app.get("/")
def read_root():
    return {
        "message": "🚀  Authentia Sync Backend API",
        "status": "online",
        "docs": "/docs"
    }

# ────────────────────────────────────────────────
# INITIALISATION BASE DE DONNÉES
# ────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    print("════════════════════════════════════")
    print("🚀 Initialisation School Sync")
    print("════════════════════════════════════")

    try:
        # 1. Permissions (reçoit la session)
        async with AsyncSessionLocal() as session:
            result = await seed_permissions(session)
            print(
                f"✅ Permissions : {result['created']} créées, "
                f"{result['existing']} existantes"
            )

        # 2. Super Admin (gère sa propre session)
        await seed_superadmin()
        print("✅ Super Admin prêt")

        print("✅ Initialisation Authentifia App")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {type(e).__name__}")
        print(f"Détails : {e}")
        raise


# ────────────────────────────────────────────────
# LANCEMENT
# ────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(
        "App.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )