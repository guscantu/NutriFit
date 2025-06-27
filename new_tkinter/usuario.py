import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/usuarios"

class UsuarioFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.carregar_usuarios()

    def create_widgets(self):
        
        self.nome_var = tk.StringVar()
        self.idade_var = tk.StringVar()
        self.peso_var = tk.StringVar()
        self.altura_var = tk.StringVar()
        self.objetivo_var = tk.StringVar()
        self.restricoes_var = tk.StringVar()
        self.id_usuario_var = tk.StringVar()

        
        form_frame = tk.LabelFrame(self, text="Cadastro de Usuário", padx=10, pady=10)
        form_frame.pack(pady=10, fill="x")

        tk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.id_usuario_var).grid(row=0, column=1)

        tk.Label(form_frame, text="Nome:").grid(row=1, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.nome_var).grid(row=1, column=1)

        tk.Label(form_frame, text="Idade:").grid(row=2, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.idade_var).grid(row=2, column=1)

        tk.Label(form_frame, text="Peso (kg):").grid(row=3, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.peso_var).grid(row=3, column=1)

        tk.Label(form_frame, text="Altura (m):").grid(row=4, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.altura_var).grid(row=4, column=1)

        tk.Label(form_frame, text="Objetivo:").grid(row=5, column=0, sticky="e")
        objetivo_cb = ttk.Combobox(form_frame, textvariable=self.objetivo_var, values=[
            "perder peso", "ganhar massa muscular", "manter peso"
        ], state="readonly")
        objetivo_cb.grid(row=5, column=1)
        objetivo_cb.set("perder peso")

        tk.Label(form_frame, text="Restrições:").grid(row=6, column=0, sticky="ne")
        self.restricoes_entry = tk.Text(form_frame, height=3, width=40)
        self.restricoes_entry.grid(row=6, column=1)

        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self.atualizar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Buscar por ID", command=self.buscar).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Recarregar Todos", command=self.carregar_usuarios).grid(row=0, column=4, padx=5)

        
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Idade", "Peso", "Altura", "Objetivo", "Restrições"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def pegar_restricoes(self):
        return self.restricoes_entry.get("1.0", tk.END).strip()

    def setar_restricoes(self, texto):
        self.restricoes_entry.delete("1.0", tk.END)
        self.restricoes_entry.insert(tk.END, texto)

    def limpar_campos(self):
        self.nome_var.set("")
        self.idade_var.set("")
        self.peso_var.set("")
        self.altura_var.set("")
        self.objetivo_var.set("perder peso")
        self.restricoes_entry.delete("1.0", tk.END)
        self.id_usuario_var.set("")

    def cadastrar(self):
        dados = self.pegar_dados_formulario()
        try:
            resp = requests.post(BASE_URL, data=dados)
            if resp.status_code == 201:
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", resp.json().get("message", "Erro ao cadastrar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        id = self.id_usuario_var.get()
        if not id:
            return messagebox.showwarning("Aviso", "Informe o ID para atualizar.")
        dados = self.pegar_dados_formulario()
        try:
            resp = requests.put(f"{BASE_URL}/{id}", data=dados)
            if resp.status_code == 200:
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", resp.json().get("message", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        id = self.id_usuario_var.get()
        if not id:
            return messagebox.showwarning("Aviso", "Informe o ID para excluir.")
        try:
            resp = requests.delete(f"{BASE_URL}/{id}")
            if resp.status_code == 204:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        id = self.id_usuario_var.get()
        if not id:
            return messagebox.showwarning("Aviso", "Informe o ID para buscar.")
        try:
            resp = requests.get(f"{BASE_URL}/{id}")
            if resp.status_code == 200:
                u = resp.json()
                self.nome_var.set(u["nome"])
                self.idade_var.set(u["idade"])
                self.peso_var.set(u["peso"])
                self.altura_var.set(u["altura"])
                self.objetivo_var.set(u["objetivo"])
                self.setar_restricoes(u["restricoes"] or "")
            else:
                messagebox.showwarning("Aviso", "Usuário não encontrado")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_usuarios(self):
        try:
            resp = requests.get(BASE_URL)
            if resp.status_code == 200:
                usuarios = resp.json()
                self.tree.delete(*self.tree.get_children())
                for u in usuarios:
                    self.tree.insert("", tk.END, values=(
                        u["id"], u["nome"], u["idade"], u["peso"], u["altura"], u["objetivo"], u["restricoes"]
                    ))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_usuario_var.set(values[0])
            self.nome_var.set(values[1])
            self.idade_var.set(values[2])
            self.peso_var.set(values[3])
            self.altura_var.set(values[4])
            self.objetivo_var.set(values[5])
            self.setar_restricoes(values[6])

    def pegar_dados_formulario(self):
        return {
            "nome": self.nome_var.get(),
            "idade": self.idade_var.get(),
            "peso": self.peso_var.get(),
            "altura": self.altura_var.get(),
            "objetivo": self.objetivo_var.get(),
            "restricoes": self.pegar_restricoes()
        }
