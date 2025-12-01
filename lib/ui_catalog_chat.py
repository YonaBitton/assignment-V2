from __future__ import annotations

from typing import Dict, List

import panel as pn

# from lib.chatbot import answer_question
import lib.chatbot as chatbot

Messages = List[Dict[str, str]]


def build_catalog_chat_dashboard(initial_context: Messages) -> pn.Column:
    """Construit le dashboard Panel pour le chatbot catalogue.

    Parameters
    ----------
    initial_context :
        ...

    Returns:
        pn.Column: Le layout Panel prêt à être affiché dans un notebook (ou via .servable()).
    """
    pn.extension()

    context: Messages = list(initial_context)

    conversation = pn.Column()

    inp = pn.widgets.TextInput(
        value="",
        placeholder="Pose ta question sur les produits…",
        width=600,
    )
    button_conversation = pn.widgets.Button(
        name="Chat!",
        button_type="primary",
    )

    def on_chat_click(_event: object) -> None:
        """Callback déclenché quand on clique sur le bouton Chat!."""
        nonlocal context

        question = inp.value.strip()
        if not question:
            return

        inp.value = ""

        # Affiche la question
        conversation.append(pn.Row("User:", pn.pane.Markdown(question, width=600)))

        try:
            # answer, context = answer_question(context, question)
            answer, context = chatbot.answer_question(context, question)

        except Exception as exc:  # type: ignore[assignment]
            answer = f"⚠️ Erreur lors de l'appel au modèle : `{exc}`"

        # Affiche la réponse de l'assistant
        conversation.append(
            pn.Row(
                "Assistant:",
                pn.pane.Markdown(
                    answer,
                    width=600,
                    styles={
                        "background-color": "#222222",
                        "color": "white",
                        "padding": "10px",
                        "border-radius": "4px",
                    },
                ),
            )
        )

    button_conversation.on_click(on_chat_click)

    dashboard = pn.Column(
        "## Assistant catalogue produits",
        pn.pane.Markdown(
            "Pose tes questions en français ou en anglais, par exemple :  \n"
            "- *Quels produits y a-t-il dans la catégorie wearable ?*  \n"
            "- *Peux-tu me résumer les informations concernant la chaise de bureau ?*  \n"
            "- *Quels produits sont adaptés au télétravail ?*  \n"
        ),
        pn.Row(inp, button_conversation),
        pn.Spacer(height=10),
        conversation,
    )

    return dashboard
