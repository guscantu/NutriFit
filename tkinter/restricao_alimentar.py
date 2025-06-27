import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://127.0.0.1:5000/api/restricoes"

class RestricaoApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Restrições Alimentares")
        master.geometry("600x400")
        master.resizable(False, False)

        self.criar_widgets()
        self.listar_todos()

    def criar_widgets(self):
        frame = tk.LabelFrame(self.master, text="Cadastro de Restrição", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        
        tk.Label(frame, text="ID:").grid(row=0, column=0, sticky="w")
        self.id_entry = tk.Entry(frame, width=10)
        self.id_entry.grid(row=0, column=1, sticky="w")

        tk.Button(frame, text="Buscar por ID", command=self.buscar).grid(row=0, column=2, padx=5)

        
        tk.Label(frame, text="Nome da Restrição:").grid(row=1, column=0, sticky="w")
        self.nome_entry = tk.Entry(frame, width=40)
        self.nome_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        
        botoes = tk.Frame(self.master)
        botoes.pack(pady=10)

        tk.Button(botoes, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(botoes, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(botoes, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(botoes, text="Listar Todos", width=15, command=self.listar_todos).pack(side="left", padx=5)

        
        self.tree = ttk.Treeview(self.master, columns=("ID", "Nome"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome da Restrição")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=400)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)

    def preencher_campos(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, item[0])
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, item[1])

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)

    def cadastrar(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome da restrição é obrigatório.")
            return

        dados = {"nome": nome}
        try:
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Restrição cadastrada com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar restrição."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        restricao_id = self.id_entry.get()
        if not restricao_id:
            messagebox.showwarning("Aviso", "Informe o ID para buscar.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{restricao_id}")
            if response.status_code == 200:
                data = response.json()
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, data["nome"])
            else:
                messagebox.showwarning("Atenção", "Restrição não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        restricao_id = self.id_entry.get()
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome da restrição é obrigatório para atualização.")
            return

        dados = {"nome": nome}
        try:
            response = requests.put(f"{BASE_URL}/{restricao_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Restrição atualizada com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar restrição."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        restricao_id = self.id_entry.get()
        if not restricao_id:
            messagebox.showwarning("Aviso", "Informe o ID para excluir.")
            return

        try:
            response = requests.delete(f"{BASE_URL}/{restricao_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Restrição excluída com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showwarning("Atenção", "Restrição não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todos(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                restricoes = response.json()
                self.tree.delete(*self.tree.get_children())
                for r in restricoes:
                    self.tree.insert("", "end", values=(r["id"], r["nome"]))
            else:
                messagebox.showerror("Erro", "Erro ao buscar restrições.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = RestricaoApp(root)
    root.mainloop()
