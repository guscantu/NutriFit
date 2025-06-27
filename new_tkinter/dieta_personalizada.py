import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/dietas_personalizadas"

class DietaPersonalizadaFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_dietas()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        tk.Label(form, text="ID (para editar/excluir):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Faixa Peso ID:").grid(row=1, column=0)
        self.faixa_peso_entry = tk.Entry(form)
        self.faixa_peso_entry.grid(row=1, column=1)

        tk.Label(form, text="Faixa Altura ID:").grid(row=2, column=0)
        self.faixa_altura_entry = tk.Entry(form)
        self.faixa_altura_entry.grid(row=2, column=1)

        tk.Label(form, text="Faixa Idade ID:").grid(row=3, column=0)
        self.faixa_idade_entry = tk.Entry(form)
        self.faixa_idade_entry.grid(row=3, column=1)

        tk.Label(form, text="Objetivo:").grid(row=4, column=0)
        self.objetivo_var = tk.StringVar()
        objetivo_combo = ttk.Combobox(form, textvariable=self.objetivo_var, state="readonly")
        objetivo_combo['values'] = ["perder peso", "ganhar massa muscular", "manter peso"]
        objetivo_combo.grid(row=4, column=1)
        objetivo_combo.current(0)

        tk.Label(form, text="Descrição:").grid(row=5, column=0)
        self.descricao_text = tk.Text(form, height=4, width=40)
        self.descricao_text.grid(row=5, column=1)

        tk.Label(form, text="Restrição (opcional):").grid(row=6, column=0)
        self.restricao_text = tk.Text(form, height=2, width=40)
        self.restricao_text.grid(row=6, column=1)

        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todos", command=self.carregar_dietas).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "PesoID", "AlturaID", "IdadeID", "Objetivo", "Descrição", "Restrição"), show="headings")
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.faixa_peso_entry.delete(0, tk.END)
        self.faixa_altura_entry.delete(0, tk.END)
        self.faixa_idade_entry.delete(0, tk.END)
        self.objetivo_var.set("perder peso")
        self.descricao_text.delete("1.0", tk.END)
        self.restricao_text.delete("1.0", tk.END)

    def get_dados_form(self):
        return {
            "faixa_peso_id": self.try_parse_int(self.faixa_peso_entry.get()),
            "faixa_altura_id": self.try_parse_int(self.faixa_altura_entry.get()),
            "faixa_idade_id": self.try_parse_int(self.faixa_idade_entry.get()),
            "objetivo": self.objetivo_var.get(),
            "descricao": self.descricao_text.get("1.0", tk.END).strip(),
            "restricao": self.restricao_text.get("1.0", tk.END).strip()
        }

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, data=self.get_dados_form())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Dieta personalizada cadastrada!")
                self.carregar_dietas()
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
                messagebox.showinfo("Sucesso", "Dieta atualizada!")
                self.carregar_dietas()
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
                messagebox.showinfo("Sucesso", "Dieta excluída!")
                self.carregar_dietas()
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
                dieta = r.json()
                self.faixa_peso_entry.delete(0, tk.END)
                self.faixa_peso_entry.insert(0, dieta["faixa_peso_id"])
                self.faixa_altura_entry.delete(0, tk.END)
                self.faixa_altura_entry.insert(0, dieta["faixa_altura_id"])
                self.faixa_idade_entry.delete(0, tk.END)
                self.faixa_idade_entry.insert(0, dieta["faixa_idade_id"])
                self.objetivo_var.set(dieta["objetivo"])
                self.descricao_text.delete("1.0", tk.END)
                self.descricao_text.insert(tk.END, dieta["descricao"])
                self.restricao_text.delete("1.0", tk.END)
                self.restricao_text.insert(tk.END, dieta["restricao"] or "")
            else:
                messagebox.showerror("Erro", "Dieta não encontrada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dietas(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for d in r.json():
                    self.tree.insert("", tk.END, values=(
                        d["id"], d["faixa_peso_id"], d["faixa_altura_id"], d["faixa_idade_id"],
                        d["objetivo"], d["descricao"], d.get("restricao", "")
                    ))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.faixa_peso_entry.delete(0, tk.END)
            self.faixa_peso_entry.insert(0, values[1])
            self.faixa_altura_entry.delete(0, tk.END)
            self.faixa_altura_entry.insert(0, values[2])
            self.faixa_idade_entry.delete(0, tk.END)
            self.faixa_idade_entry.insert(0, values[3])
            self.objetivo_var.set(values[4])
            self.descricao_text.delete("1.0", tk.END)
            self.descricao_text.insert(tk.END, values[5])
            self.restricao_text.delete("1.0", tk.END)
            self.restricao_text.insert(tk.END, values[6])

    def try_parse_int(self, value):
        try:
            return int(value)
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dieta Personalizada - NutriFit")
    DietaPersonalizadaFrame(root)
    root.mainloop()
