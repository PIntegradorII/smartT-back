import json
import os
import re
from dotenv import load_dotenv
from together import Together
from app.db.database import SessionLocal
from app.models.receta import Receta, RecetaHistorico
from sqlalchemy.orm import Session



load_dotenv()

# Inicializar cliente con la API Key de Together
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)

def get_recipe_from_ingredients(ingredients_text):
    """Genera una receta en formato JSON basado en los ingredientes dados."""
    
    # Definir el prompt con formato detallado
    prompt = f"""
    Eres un chef experto en comida saludable. Tu tarea es generar recetas saludables basadas en los ingredientes proporcionados por el usuario.

    ### **Ingredientes del usuario:**  
    {ingredients_text}

    ### **Instrucciones:**  
    1. La receta debe ser saludable y balanceada.  
    2. Solo usa los ingredientes proporcionados. No agregues otros.  
    3. La receta debe contener los siguientes elementos en **formato JSON**, respetando esta estructura:

    ```json
    {{
      "nombre": "Nombre de la receta",
      "ingredientes": [
        {{"nombre": "Ingrediente 1", "cantidad": "Cantidad y unidad"}},
        {{"nombre": "Ingrediente 2", "cantidad": "Cantidad y unidad"}}
      ],
      "preparacion": [
        "Paso 1 de la preparación",
        "Paso 2 de la preparación",
        "Paso 3 de la preparación"
      ]
    }}
    ```

    4. **Devuelve únicamente el JSON sin explicaciones adicionales.**  
    5. No incluyas ingredientes que el usuario no mencionó.  
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
    recipe_json = json.dumps(recipe, ensure_ascii=False)

    # Verificar si ya existe una receta para el usuario
    existing_recipe = db.query(Receta).filter(Receta.user_id == user_id).first()

    if existing_recipe:
        # Mover la receta anterior al historial
        receta_historico = RecetaHistorico(
            user_id=user_id,
            transcript=transcript,
            recipe=recipe_json,  # Almacenamos la receta como string JSON
        )
        db.add(receta_historico)
        db.delete(existing_recipe)

    # Guardar la nueva receta
    new_recipe = Receta(
        user_id=user_id,
        transcript=transcript,
        recipe=recipe_json,  # Almacenamos la receta como string JSON
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return {
        "message": "Receta guardada o actualizada correctamente.",
        "recipe": recipe_json  # Se devuelve la receta en su formato JSON
    }
    