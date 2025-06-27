import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/dicas"

class DicaFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_dicas()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        tk.Label(form, text="ID (edição/exclusão):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Objetivo:").grid(row=1, column=0)
        self.objetivo_var = tk.StringVar()
        self.objetivo_combo = ttk.Combobox(form, textvariable=self.objetivo_var, state="readonly", values=["perder peso", "ganhar massa muscular", "manter peso"])
        self.objetivo_combo.grid(row=1, column=1)
        self.objetivo_combo.current(0)

        tk.Label(form, text="Texto da Dica:").grid(row=2, column=0)
        self.texto_text = tk.Text(form, height=3, width=40)
        self.texto_text.grid(row=2, column=1)

        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todos", command=self.carregar_dicas).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Objetivo", "Texto"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.texto_text.delete("1.0", tk.END)
        self.objetivo_combo.current(0)

    def get_dados_form(self):
        return {
            "objetivo": self.objetivo_var.get(),
            "texto": self.texto_text.get("1.0", tk.END).strip()
        }

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, data=self.get_dados_form())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Dica cadastrada!")
                self.carregar_dicas()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao cadastrar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def editar(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("Atenção", "ID inválido")
            return
        try:
            r = requests.put(f"{BASE_URL}/{id_}", data=self.get_dados_form())
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Dica atualizada!")
                self.carregar_dicas()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("Atenção", "ID inválido")
            return
        try:
            r = requests.delete(f"{BASE_URL}/{id_}")
            if r.status_code == 204:
                messagebox.showinfo("Sucesso", "Dica excluída!")
                self.carregar_dicas()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao excluir"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_por_id(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("Atenção", "ID inválido")
            return
        try:
            r = requests.get(f"{BASE_URL}/{id_}")
            if r.status_code == 200:
                dica = r.json()
                self.texto_text.delete("1.0", tk.END)
                self.texto_text.insert(tk.END, dica["texto"] or "")
                self.objetivo_var.set(dica["objetivo"] or "perder peso")
            else:
                messagebox.showerror("Erro", "Dica não encontrada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dicas(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for d in r.json():
                    self.tree.insert("", tk.END, values=(d["id"], d["objetivo"], d["texto"]))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.objetivo_var.set(values[1])
            self.texto_text.delete("1.0", tk.END)
            self.texto_text.insert(tk.END, values[2])



def show_dica(self):
    self.clear_content()
    tk.Label(self.content_frame, text="Dicas 💡", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
    from new_tkinter.dica import DicaFrame
    DicaFrame(self.content_frame)
