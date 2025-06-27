import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/substituicoes_alimento"

class SubstituicaoAlimentoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_substituicoes()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        tk.Label(form, text="ID (editar/excluir):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Restrição ID:").grid(row=1, column=0)
        self.restricao_id_entry = tk.Entry(form)
        self.restricao_id_entry.grid(row=1, column=1)

        tk.Label(form, text="Alimento original:").grid(row=2, column=0)
        self.original_entry = tk.Entry(form, width=40)
        self.original_entry.grid(row=2, column=1)

        tk.Label(form, text="Substituto:").grid(row=3, column=0)
        self.substituto_entry = tk.Entry(form, width=40)
        self.substituto_entry.grid(row=3, column=1)

        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todos", command=self.carregar_substituicoes).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Restrição ID", "Original", "Substituto"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.restricao_id_entry.delete(0, tk.END)
        self.original_entry.delete(0, tk.END)
        self.substituto_entry.delete(0, tk.END)

    def get_dados_form(self):
        return {
            "restricao_id": self.try_parse_int(self.restricao_id_entry.get()),
            "alimento_original": self.original_entry.get(),
            "alimento_substituto": self.substituto_entry.get()
        }

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, json=self.get_dados_form())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Substituição cadastrada!")
                self.carregar_substituicoes()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao cadastrar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def editar(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("ID inválido", "Informe um ID válido para editar.")
            return
        try:
            r = requests.put(f"{BASE_URL}/{id_}", json=self.get_dados_form())
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Substituição atualizada!")
                self.carregar_substituicoes()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao atualizar"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("ID inválido", "Informe um ID válido para excluir.")
            return
        try:
            r = requests.delete(f"{BASE_URL}/{id_}")
            if r.status_code == 204:
                messagebox.showinfo("Sucesso", "Substituição excluída!")
                self.carregar_substituicoes()
                self.limpar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao excluir"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_por_id(self):
        id_ = self.id_entry.get()
        if not id_.isdigit():
            messagebox.showwarning("ID inválido", "Informe um ID válido.")
            return
        try:
            r = requests.get(f"{BASE_URL}/{id_}")
            if r.status_code == 200:
                sub = r.json()
                self.restricao_id_entry.delete(0, tk.END)
                self.restricao_id_entry.insert(0, sub["restricao_id"])
                self.original_entry.delete(0, tk.END)
                self.original_entry.insert(0, sub["alimento_original"])
                self.substituto_entry.delete(0, tk.END)
                self.substituto_entry.insert(0, sub["alimento_substituto"])
            else:
                messagebox.showerror("Erro", "Substituição não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_substituicoes(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for s in r.json():
                    self.tree.insert("", tk.END, values=(s["id"], s["restricao_id"], s["alimento_original"], s["alimento_substituto"]))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.restricao_id_entry.delete(0, tk.END)
            self.restricao_id_entry.insert(0, values[1])
            self.original_entry.delete(0, tk.END)
            self.original_entry.insert(0, values[2])
            self.substituto_entry.delete(0, tk.END)
            self.substituto_entry.insert(0, values[3])

    def try_parse_int(self, value):
        try:
            return int(value)
        except:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Substituição Alimentar")
    SubstituicaoAlimentoFrame(root)
    root.mainloop()
