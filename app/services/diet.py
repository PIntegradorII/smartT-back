import json
import os
import re
from dotenv import load_dotenv
from together import Together
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from app.db.database import Session, get_db
from app.models.user import User
from app.services.watson import speech_to_text
from app.models.diet import DietPlan



load_dotenv()

# Inicializar cliente con la API Key de Together
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)

def get_diet_plan(objectives):
    """Genera un plan alimenticio diario en formato JSON basado en los objetivos dados."""
    
    # Definir el prompt con formato detallado
    prompt = f"""
    Eres un nutricionista experto en alimentación saludable. Tu tarea es generar un plan alimenticio completo y balanceado para todo el día basado en los objetivos del usuario.

    ### **Objetivos del usuario:**  
    {objectives}

    ### **Instrucciones:**  
    1. El plan debe ser saludable, balanceado y adaptado a los objetivos del usuario.  
    2. Debe incluir 3 comidas principales (desayuno, almuerzo, cena) y 2 snacks.  
    3. Cada comida debe especificar los componentes nutricionales principales (proteínas, carbohidratos, grasas saludables, vegetales/frutas).  
    4. El plan debe contener los siguientes elementos en **formato JSON**, respetando esta estructura:

    ```json
    {{
      "plan_alimenticio": {{
        "desayuno": {{
          "descripcion": "Descripción detallada del desayuno",
          "componentes": [
            "Proteína: tipo y cantidad",
            "Carbohidratos: tipo y cantidad",
            "Frutas/Vegetales: tipo y cantidad",
            "Líquidos: tipo y cantidad"
          ]
        }},
        "snack_manana": {{
          "descripcion": "Descripción del snack de media mañana",
          "componentes": [
            "Componente 1",
            "Componente 2"
          ]
        }},
        "almuerzo": {{
          "descripcion": "Descripción detallada del almuerzo",
          "componentes": [
            "Proteína: tipo y cantidad",
            "Carbohidratos: tipo y cantidad",
            "Vegetales: tipo y cantidad",
            "Grasas saludables: tipo y cantidad"
          ]
        }},
        "snack_tarde": {{
          "descripcion": "Descripción del snack de media tarde",
          "componentes": [
            "Componente 1",
            "Componente 2"
          ]
        }},
        "cena": {{
          "descripcion": "Descripción detallada de la cena",
          "componentes": [
            "Proteína: tipo y cantidad",
            "Carbohidratos: tipo y cantidad (opcional)",
            "Vegetales: tipo y cantidad",
            "Grasas saludables: tipo y cantidad"
          ]
        }}
      }},
      "recomendaciones_generales": [
        "Recomendación 1",
        "Recomendación 2"
      ]
    }}
    ```

    4. **Devuelve únicamente el JSON sin explicaciones adicionales.**  
    5. Adapta las cantidades y tipos de alimentos según los objetivos del usuario (ej: pérdida de peso, ganancia muscular, mantenimiento).  
    6. **No agregues comentarios ni explicaciones. Solo devuelve el JSON puro.**  
    """
    
    # Llamar al modelo de IA
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[{"role": "user", "content": prompt}]
    )
    raw_response = response.choices[0].message.content

    # Extraer solo la parte que parece ser JSON
    match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))  # Convertir a JSON solo la parte válida
        except json.JSONDecodeError:
            return {"error": "El JSON generado no es válido"}
    
    return {"error": "No se pudo extraer un JSON válido"}



def save_or_update_recipe(user_id: int, transcript: str, recipe: dict) -> dict:
    """
    Guarda o actualiza la receta del usuario. Si el usuario ya tiene una receta,
    la anterior se mueve al historial.
    """
    db: Session = SessionLocal()

    # Aseguramos que 'recipe' sea una cadena JSON válida con caracteres no escapados
    dieta_json = json.dumps(recipe, ensure_ascii=False)


    # Guardar la nueva receta
    new_diet = DietPlan(
        user_id=user_id,
        transcript=transcript,
        plan=dieta_json,  # Almacenamos la receta como string JSON
    )
    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)

    return {
        "message": "Dieta guardada o actualizada correctamente.",
        "dieta": dieta_json  # Se devuelve la receta en su formato JSON
    }

