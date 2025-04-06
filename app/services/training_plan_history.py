from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def get_training_plan_history(db: Session, user_id: int):
    sql = text("""
            SELECT 
            id, 
            user_id, 
            lunes, 
            martes, 
            miercoles, 
            jueves, 
            viernes, 
            created_at, 
            updated_at AS fecha_estado, 
            1 AS estado,
            (SELECT pd.objetivo FROM physical_data pd WHERE pd.user_id = training_plans.user_id) AS objetivo
        FROM training_plans
        WHERE user_id = :user_id
        UNION ALL
        SELECT 
            id, 
            user_id, 
            lunes, 
            martes, 
            miercoles, 
            jueves, 
            viernes, 
            created_at, 
            archived_at AS fecha_estado, 
            estado, 
            (SELECT pd.objetivo FROM physical_data pd WHERE pd.user_id = training_plans_history.user_id) AS objetivo
        FROM training_plans_history  
        WHERE user_id = :user_id;
    """)

    result = db.execute(sql, {"user_id": user_id})

    return [dict(row._mapping) for row in result]  # Convertimos a lista de diccionarios
