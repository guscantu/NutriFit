import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/progresso"

class ProgressoApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Progresso")
        master.geometry("750x500")
        master.resizable(False, False)

        self.create_widgets()
        self.listar_todos()

    def create_widgets(self):
        frame = tk.LabelFrame(self.master, text="Cadastro de Progresso", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        
        tk.Label(frame, text="ID:").grid(row=0, column=0, sticky="w")
        self.id_entry = tk.Entry(frame, width=10)
        self.id_entry.grid(row=0, column=1, sticky="w")

        tk.Button(frame, text="Buscar por ID", command=self.buscar).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Usuário ID:").grid(row=1, column=0, sticky="w")
        self.usuario_id_entry = tk.Entry(frame, width=30)
        self.usuario_id_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        tk.Label(frame, text="Data (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.data_entry = tk.Entry(frame, width=30)
        self.data_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        tk.Label(frame, text="Peso (kg):").grid(row=3, column=0, sticky="w")
        self.peso_entry = tk.Entry(frame, width=30)
        self.peso_entry.grid(row=3, column=1, columnspan=2, sticky="w")

        tk.Label(frame, text="IMC (opcional):").grid(row=4, column=0, sticky="w")
        self.imc_entry = tk.Entry(frame, width=30)
        self.imc_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        
        botoes = tk.Frame(self.master)
        botoes.pack(pady=10)

        tk.Button(botoes, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(botoes, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(botoes, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(botoes, text="Listar Todos", width=15, command=self.listar_todos).pack(side="left", padx=5)

        
        colunas = ("ID", "Usuário ID", "Data", "Peso", "IMC")
        self.tree = ttk.Treeview(self.master, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == "Data":
                self.tree.column(col, width=120, anchor="center")
            elif col == "IMC":
                self.tree.column(col, width=80, anchor="center")
            else:
                self.tree.column(col, width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)

    def preencher_campos(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, item[0])
            self.usuario_id_entry.delete(0, tk.END)
            self.usuario_id_entry.insert(0, item[1])
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, item[2])
            self.peso_entry.delete(0, tk.END)
            self.peso_entry.insert(0, item[3])
            self.imc_entry.delete(0, tk.END)
            self.imc_entry.insert(0, item[4] if item[4] is not None else "")

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.usuario_id_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.imc_entry.delete(0, tk.END)

    def cadastrar(self):
        try:
            peso = float(self.peso_entry.get())
            if peso <= 0:
                raise ValueError("Peso deve ser maior que 0.")

            dados = {
                "usuario_id": int(self.usuario_id_entry.get()),
                "dataprogresso": self.data_entry.get(),
                "peso": peso,
                "imc": float(self.imc_entry.get()) if self.imc_entry.get() else None
            }

            datetime.strptime(dados["dataprogresso"], "%Y-%m-%d")

            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Progresso cadastrado com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar progresso."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        progresso_id = self.id_entry.get()
        if not progresso_id:
            messagebox.showwarning("Aviso", "Informe o ID para buscar.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{progresso_id}")
            if response.status_code == 200:
                data = response.json()
                self.usuario_id_entry.delete(0, tk.END)
                self.data_entry.delete(0, tk.END)
                self.peso_entry.delete(0, tk.END)
                self.imc_entry.delete(0, tk.END)

                self.usuario_id_entry.insert(0, data["usuario_id"])
                self.data_entry.insert(0, data["dataprogresso"])
                self.peso_entry.insert(0, data["peso"])
                self.imc_entry.insert(0, data["imc"] if data["imc"] is not None else "")
            else:
                messagebox.showwarning("Atenção", "Progresso não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        progresso_id = self.id_entry.get()
        try:
            peso = float(self.peso_entry.get())
            if peso <= 0:
                raise ValueError("Peso deve ser maior que 0.")

            dados = {
                "usuario_id": int(self.usuario_id_entry.get()),
                "dataprogresso": self.data_entry.get(),
                "peso": peso,
                "imc": float(self.imc_entry.get()) if self.imc_entry.get() else None
            }

            datetime.strptime(dados["dataprogresso"], "%Y-%m-%d")

            response = requests.put(f"{BASE_URL}/{progresso_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Progresso atualizado com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar progresso."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        progresso_id = self.id_entry.get()
        if not progresso_id:
            messagebox.showwarning("Aviso", "Informe o ID para excluir.")
            return

        try:
            response = requests.delete(f"{BASE_URL}/{progresso_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Progresso excluído com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showwarning("Atenção", "Progresso não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todos(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                registros = response.json()
                self.tree.delete(*self.tree.get_children())
                for prog in registros:
                    self.tree.insert("", "end", values=(
                        prog["id"],
                        prog["usuario_id"],
                        prog["dataprogresso"],
                        prog["peso"],
                        prog["imc"] if prog["imc"] is not None else "-"
                    ))
            else:
                messagebox.showerror("Erro", "Erro ao buscar registros.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressoApp(root)
    root.mainloop()
