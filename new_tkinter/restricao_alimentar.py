import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://localhost:5000/api/restricoes"

class RestricaoAlimentarFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_restricoes()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        tk.Label(form, text="ID (edição/exclusão):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Nome da Restrição:").grid(row=1, column=0)
        self.nome_entry = tk.Entry(form, width=40)
        self.nome_entry.grid(row=1, column=1)

        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todos", command=self.carregar_restricoes).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)

    def get_dados_form(self):
        return {"nome": self.nome_entry.get().strip()}

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, json=self.get_dados_form())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Restrição cadastrada!")
                self.carregar_restricoes()
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
            r = requests.put(f"{BASE_URL}/{id_}", json=self.get_dados_form())
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Restrição atualizada!")
                self.carregar_restricoes()
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
                messagebox.showinfo("Sucesso", "Restrição excluída!")
                self.carregar_restricoes()
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
                restricao = r.json()
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, restricao["nome"])
            else:
                messagebox.showerror("Erro", "Restrição não encontrada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_restricoes(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for restricao in r.json():
                    self.tree.insert("", tk.END, values=(restricao["id"], restricao["nome"]))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Restrição Alimentar - NutriFit")
    RestricaoAlimentarFrame(root)
    root.mainloop()


