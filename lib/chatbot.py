from __future__ import annotations

from typing import Dict, List

from lib.config import get_config
from lib.openai_client import client

Messages = List[Dict[str, str]]

# Charger la config une fois au démarrage du module
_config = get_config()


def create_catalog_system_context(catalog_text: str) -> Messages:
    """Crée le contexte initial (message system) pour le chatbot catalogue."""
    system_content = f"""
Tu es un assistant pour un petit catalogue de produits.

RÈGLE DE LANGUE (TRÈS IMPORTANTE) :
- Tu dois TOUJOURS répondre dans LA MÊME LANGUE que la question de l'utilisateur.
- Si l'utilisateur pose sa question en français → tu réponds en français.
- S'il pose sa question en anglais → tu réponds en anglais.
- S'il pose la question dans une autre langue → tu réponds dans cette langue.
- Tu NE DOIS PAS répondre en français quand la question est en anglais,
  sauf si l'utilisateur te le demande explicitement.
- Ne traduis pas la question : réponds simplement dans la même langue.

On te fournit ci-dessous la liste des produits au format JSON, avec :
- id
- name
- category
- price_eur
- colors
- description
- features
- in_stock

Tu utilises UNIQUEMENT ces informations pour répondre.

L'utilisateur peut poser des questions comme :
- Donne les informations résumées du produit 2
- Quels produits font partie de la catégorie wearable ?
- Donne-moi les détails sur la chaise de bureau
- Quels produits sont adaptés au télétravail ?

Dans ta réponse, pour chaque produit pertinent, donne :
- le nom du produit
- la catégorie (traduite en français si tu réponds en français)
- le prix
- la disponibilité (en stock ou non)
- un résumé très court.

Catalogue JSON :
{catalog_text}
"""

    return [{"role": "system", "content": system_content}]


def get_completion_from_messages(
    messages: Messages,
    model: str | None = None,
    temperature: float | None = None,
) -> str:
    """Appelle le modèle de chat et renvoie le contenu de la réponse."""
    # Utiliser les valeurs de la config si non spécifiées
    model = model or _config["chatbot"]["model"]
    temperature = temperature if temperature is not None else _config["chatbot"]["temperature"]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def answer_question(
    context: Messages,
    question: str,
    model: str | None = None,
    temperature: float | None = None,
) -> tuple[str, Messages]:
    """Ajoute une question au contexte et renvoie la réponse du modèle.

    Retourne un tuple (réponse, nouveau_contexte).
    """
    new_context = list(context)
    new_context.append({"role": "user", "content": question})

    answer = get_completion_from_messages(
        new_context,
        model=model,
        temperature=temperature,
    )

    new_context.append({"role": "assistant", "content": answer})

    return answer, new_context
