import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://localhost:5000/api/progresso"

class ProgressoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        
        tk.Label(form, text="ID (editar/excluir):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Usuário ID:").grid(row=1, column=0)
        self.usuario_entry = tk.Entry(form)
        self.usuario_entry.grid(row=1, column=1)

        
        tk.Label(form, text="Data (YYYY-MM-DD):").grid(row=2, column=0)
        self.data_entry = tk.Entry(form)
        self.data_entry.grid(row=2, column=1)

        
        tk.Label(form, text="Peso (kg):").grid(row=3, column=0)
        self.peso_entry = tk.Entry(form)
        self.peso_entry.grid(row=3, column=1)

        
        tk.Label(form, text="IMC (opcional):").grid(row=4, column=0)
        self.imc_entry = tk.Entry(form)
        self.imc_entry.grid(row=4, column=1)

        
        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todos", command=self.carregar).grid(row=0, column=4, padx=5)

        
        self.tree = ttk.Treeview(self, columns=("ID", "Usuário", "Data", "Peso", "IMC"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def get_data(self):
        return {
            "usuario_id": self.try_parse_int(self.usuario_entry.get()),
            "dataprogresso": self.data_entry.get(),
            "peso": self.try_parse_float(self.peso_entry.get()),
            "imc": self.try_parse_float(self.imc_entry.get())
        }

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.imc_entry.delete(0, tk.END)

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, data=self.get_data())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Progresso cadastrado!")
                self.carregar()
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
            r = requests.put(f"{BASE_URL}/{id_}", data=self.get_data())
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Progresso atualizado!")
                self.carregar()
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
                messagebox.showinfo("Sucesso", "Progresso excluído!")
                self.carregar()
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
                p = r.json()
                self.usuario_entry.delete(0, tk.END)
                self.usuario_entry.insert(0, p["usuario_id"])
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(0, p["dataprogresso"])
                self.peso_entry.delete(0, tk.END)
                self.peso_entry.insert(0, p["peso"])
                self.imc_entry.delete(0, tk.END)
                self.imc_entry.insert(0, p.get("imc", ""))
            else:
                messagebox.showerror("Erro", "Progresso não encontrado")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for p in r.json():
                    self.tree.insert("", tk.END, values=(p["id"], p["usuario_id"], p["dataprogresso"], p["peso"], p["imc"]))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            v = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, v[0])
            self.usuario_entry.delete(0, tk.END)
            self.usuario_entry.insert(0, v[1])
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, v[2])
            self.peso_entry.delete(0, tk.END)
            self.peso_entry.insert(0, v[3])
            self.imc_entry.delete(0, tk.END)
            self.imc_entry.insert(0, v[4])

    def try_parse_int(self, val):
        try:
            return int(val)
        except:
            return None

    def try_parse_float(self, val):
        try:
            return float(val)
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Progresso - NutriFit")
    ProgressoFrame(root)
    root.mainloop()
