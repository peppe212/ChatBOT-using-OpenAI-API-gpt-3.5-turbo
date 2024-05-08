#Author: Giuseppe Muschetta

import logging
import tkinter as tk
from tkinter import scrolledtext, font
from openai import OpenAI
import os

# Recupera la chiave API da una variabile di ambiente e inizializza il client di OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = "gpt-3.5-turbo-0125"


def chat_with_openai(prompt):
    """
    Invia una richiesta alla API di OpenAI e restituisce la risposta del modello.

    @args
        prompt (str): Il messaggio inserito dall'utente da inviare al modello.

    @returns:
        str: Il contenuto della risposta del modello, in caso di successo.
        str: Un messaggio di errore, in caso di fallimento.
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}])
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Failed to retrieve response: {e}")
        return f"An error occurred: {e}"
#end_function


def send_message(event=None):
    """
    Gestisce l'invio dei messaggi quando l'utente preme 'Invio' o clicca sul pulsante 'Send'.
    Prende l'input dall'utente, invia la richiesta al modello e visualizza la risposta.

    @args
          event: Parametro opzionale per gestire l'evento di pressione del tasto.
    """
    user_input = user_input_text.get()
    if user_input.lower() == 'quit':
        window.quit()
    else:
        response = chat_with_openai(user_input)
        chat_history.config(state='normal')
        chat_history.insert(tk.END, "Tu: " + user_input + "\n")
        chat_history.insert(tk.END, "BOT: " + response + "\n\n")
        chat_history.yview(tk.END)
        chat_history.config(state='disabled')
        user_input_text.set("")
    return


# Inizializzazione della finestra principale dell'interfaccia grafica
window = tk.Tk()
window.title("Giuseppe Muschetta's ChatBOT")
window.geometry("1280x720")
# Font personalizzato per i widget
custom_font = font.Font(family="Verdana", size=16, weight='normal')


# Configura la griglia per rendere i widget responsivi
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Configurazione del widget ScrolledText per visualizzare la cronologia della chat
chat_history = scrolledtext.ScrolledText(window,
                                         state='normal',
                                         width=150,
                                         height=40,
                                         font=custom_font)

chat_history.grid(row=0,
                  column=0,
                  columnspan=3,
                  padx=10,
                  pady=10,
                  sticky="nsew")


# Configurazione del tag per il colore del testo
chat_history.tag_configure('welcome', foreground='darkgreen')

# Inserimento del messaggio di benvenuto con il tag 'welcome'
chat_history.config(state='normal', font=custom_font)

chat_history.insert(tk.END, "Benvenuto alla chat caro essere umano!\n"
                            "Sarò il tuo assistente artificiale, ma vacci piano con me, sono solo una IA\n"
                            "Scrivimi tutto quello che vuoi e poi premi INVIO o il tasto SEND.\n\n", 'welcome')

chat_history.config(state='disabled', font=custom_font)


# Configurazione del campo di testo per l'input dell'utente
user_input_text = tk.StringVar()
user_input_entry = tk.Entry(window,
                            textvariable=user_input_text,
                            font=custom_font, width=150)

user_input_entry.grid(row=1,
                      column=0,
                      padx=10,
                      pady=10,
                      sticky="ew")

user_input_entry.bind("<Return>", send_message)


# Configurazione del pulsante di invio
send_button = tk.Button(window,
                        text="Send",
                        font=custom_font,
                        command=send_message)

send_button.grid(row=1,
                 column=2,
                 padx=10,
                 pady=10,
                 sticky="ew")


# Avvio del ciclo principale della finestra
window.mainloop()

#%%
