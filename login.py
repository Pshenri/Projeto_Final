import tkinter as tk
from tkinter import messagebox
from logs.logger import log_evento
from painel.autorizacao import abrir_painel

usuarios = {
    "admin": "admin123",
    "joao": "senha123",
    "maria": "123456",
}

def iniciar_login():
    def autenticar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario in usuarios and usuarios[usuario] == senha:
            log_evento(f"LOGIN_SUCESSO | Usuário: {usuario}")
            messagebox.showinfo("Login", f"Bem-vindo, {usuario}!")
            janela.destroy()
            abrir_painel(usuario)
        else:
            log_evento(f"LOGIN_FALHA | Tentativa com usuário: {usuario}")
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def sair():
        log_evento("SISTEMA_ENCERRADO pelo usuário")
        janela.destroy()

    log_evento("SISTEMA_INICIADO - Tela de login carregada")

    janela = tk.Tk()
    janela.title("Tela de Login")
    janela.geometry("300x180")
    janela.resizable(False, False)

    tk.Label(janela, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(janela)
    entry_usuario.pack()

    tk.Label(janela, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Button(janela, text="Login", width=10, command=autenticar).pack(pady=10)
    tk.Button(janela, text="Sair", width=10, command=sair).pack()

    janela.mainloop()
