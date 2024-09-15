#MATHIAS ALFREDO BAMBAREN MEDINA 71335785
#PARA CORRER EL PROTOTIPO DEBES llamar con la consola de python
#esto ejecutara el servidor web que recibira las solicitudes http para fastapi
#python -m uvicorn main:app --reload 

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)

app = FastAPI()

#en system le dicen a la IA QUE COSA ES osea como se comporta y así
#en user se le dice cómo el usuario le preguntara
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
]

#Este es mi endpoint inicial recibe solicitudes get y muestra una ventana de mensajes
@app.get("/", response_class=HTMLResponse)
async def formulario():
    return """
    <html>
        <head>
            <title>Chatbot Prototipo con OpenAI</title>
        </head>
        <body>
            <h2>Chatbot de Plagas</h2>
            <form action="/procesar" method="post">
                <label for="mensaje">Mensaje:</label><br>
                <input type="text" id="mensaje" name="mensaje"><br><br>
                <input type="submit" value="Enviar">
            </form>
            <h3>Historial de mensajes:</h3>
            <ul>
                {}
            </ul>
        </body>
    </html>
    """.format("".join(f"<li>{m['role']}: {m['content']}</li>" for m in messages))


#el form de arriba se define como metodo post y lo manda al endpoint procesar
#esto se manda como objeto con nombre mensaje a este endpoint
@app.post("/procesar", response_class=HTMLResponse)
async def procesar(mensaje: str = Form(...)):
    #se agrega al historial
    messages.append({"role": "user", "content": mensaje})

    #aqui ocurre la magia, se manda a openai para generar respuesta que luego se guarda en competion
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    #esa rpta se castea para que se guarde en esa nueva variable la rpta en texto
    assistant_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})

    #historial de mdjs
    return """
    <html>
        <head>
            <title>Chatbot con OpenAI</title>
        </head>
        <body>
            <h2>Respuesta del Bot:</h2>
            <p>{}</p><br>
            <a href="/">Enviar otro mensaje</a>
            <h3>Historial de mensajes:</h3>
            <ul>
                {}
            </ul>
        </body>
    </html>
    """.format(assistant_response, "".join(f"<li>{m['role']}: {m['content']}</li>" for m in messages))
