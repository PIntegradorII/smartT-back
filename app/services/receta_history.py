from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def get_receta_plan_history(db: Session, user_id: int):
    sql = text("""
            SELECT id, user_id, transcript, recipe, created_at 
            FROM recetas_historico 
            WHERE user_id = :user_id;
    """)

    result = db.execute(sql, {"user_id": user_id})

    return [dict(row._mapping) for row in result]  # Convertimos a lista de diccionarios
