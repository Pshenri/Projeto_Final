import tkinter as tk
from tkinter import messagebox
from logs.logger import log_evento

def abrir_painel(usuario_logado):
    def autorizar():
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Campos obrigatórios", "Preencha o nome e CPF do visitante.")
            return

        log_evento(f"ACCESS_GRANTED | Visitante: {nome} | CPF: {cpf} | Autorizado por: {usuario_logado}")
        messagebox.showinfo("Acesso Liberado", f"Acesso liberado para {nome}. Porta aberta.")
        painel.destroy()

    def negar():
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        log_evento(f"ACCESS_DENIED | Visitante: {nome or 'Desconhecido'} | CPF: {cpf or 'Desconhecido'} | Negado por: {usuario_logado}")
        messagebox.showwarning("Acesso Negado", "Acesso negado ao visitante.")
        painel.destroy()

    painel = tk.Tk()
    painel.title("Painel de Autorização de Visitantes")
    painel.geometry("400x250")
    painel.resizable(False, False)

    tk.Label(painel, text=f"Usuário logado: {usuario_logado}", font=("Arial", 10)).pack(pady=5)
    tk.Label(painel, text="Autorização de Visitante", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(painel, text="Nome do Visitante:").pack()
    entry_nome = tk.Entry(painel, width=40)
    entry_nome.pack(pady=5)

    tk.Label(painel, text="CPF do Visitante:").pack()
    entry_cpf = tk.Entry(painel, width=40)
    entry_cpf.pack(pady=5)

    tk.Button(painel, text="Autorizar e Abrir Porta", bg="green", fg="white",
              font=("Arial", 10), command=autorizar, width=25).pack(pady=10)

    tk.Button(painel, text="Negar Acesso", bg="red", fg="white",
              font=("Arial", 10), command=negar, width=25).pack()

    painel.mainloop()
