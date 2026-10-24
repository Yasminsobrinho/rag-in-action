
import os
import chainlit as cl

from dotenv import load_dotenv
from google import genai

# Carrega as variáveis de ambiente
load_dotenv()

# Instruções do assistente
SYSTEM_PROMPT = """
Você é um assistente técnico direto, preciso e útil.
Responda sempre em português do Brasil.
Explique assuntos técnicos de maneira simples.
Não invente informações.
Quando não souber algo, diga que não sabe.
"""

# Configuração do Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY não encontrada no arquivo .env"
    )

client = genai.Client(api_key=api_key)

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# Mensagem inicial
@cl.on_chat_start
async def start():
    await cl.Message(
        content="Olá! Sou seu assistente de IA. Como posso ajudar?"
    ).send()


# Processamento das mensagens
@cl.on_message
async def on_message(message: cl.Message):
    try:
        prompt = f"""
{SYSTEM_PROMPT}

Mensagem do usuário:
{message.content}
"""

        response = await cl.make_async(
            client.models.generate_content
        )(
            model=MODEL,
            contents=prompt,
        )

        await cl.Message(
            content=response.text or "Não recebi uma resposta em texto."
        ).send()

    except Exception as e:
        print(f"\nERRO AO GERAR RESPOSTA: {e}\n")

        await cl.Message(
            content="Ocorreu um erro. Consulte o terminal do VS Code."
        ).send()
