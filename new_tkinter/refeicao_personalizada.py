import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/refeicoes_personalizadas"

class RefeicaoPersonalizadaFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_refeicoes()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        tk.Label(form, text="ID (edição/exclusão):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="ID Dieta Personalizada:").grid(row=1, column=0)
        self.dieta_id_entry = tk.Entry(form)
        self.dieta_id_entry.grid(row=1, column=1)

        tk.Label(form, text="Tipo:").grid(row=2, column=0)
        self.tipo_var = tk.StringVar()
        tipos = ["café da manhã", "almoço", "lanche", "jantar"]
        self.tipo_menu = ttk.Combobox(form, textvariable=self.tipo_var, values=tipos, state="readonly")
        self.tipo_menu.grid(row=2, column=1)
        self.tipo_menu.current(0)

        tk.Label(form, text="Alimentos:").grid(row=3, column=0)
        self.alimentos_text = tk.Text(form, height=4, width=30)
        self.alimentos_text.grid(row=3, column=1)

        
        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Listar Todas", command=self.carregar_refeicoes).grid(row=0, column=4, padx=5)

        
        self.tree = ttk.Treeview(self, columns=("ID", "Dieta", "Tipo", "Alimentos"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def get_form_data(self):
        return {
            "dieta_personalizada_id": self.try_parse_int(self.dieta_id_entry.get()),
            "tipo": self.tipo_var.get(),
            "alimentos": self.alimentos_text.get("1.0", tk.END).strip()
        }

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.dieta_id_entry.delete(0, tk.END)
        self.alimentos_text.delete("1.0", tk.END)
        self.tipo_menu.current(0)

    def cadastrar(self):
        try:
            r = requests.post(BASE_URL, data=self.get_form_data())
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Refeição cadastrada!")
                self.carregar_refeicoes()
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
            r = requests.put(f"{BASE_URL}/{id_}", data=self.get_form_data())
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", "Refeição atualizada!")
                self.carregar_refeicoes()
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
                messagebox.showinfo("Sucesso", "Refeição excluída!")
                self.carregar_refeicoes()
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
                d = r.json()
                self.dieta_id_entry.delete(0, tk.END)
                self.dieta_id_entry.insert(0, d["dieta_personalizada_id"])
                self.tipo_var.set(d["tipo"])
                self.alimentos_text.delete("1.0", tk.END)
                self.alimentos_text.insert(tk.END, d["alimentos"])
            else:
                messagebox.showerror("Erro", "Refeição não encontrada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_refeicoes(self):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for d in r.json():
                    self.tree.insert("", tk.END, values=(d["id"], d["dieta_personalizada_id"], d["tipo"], d["alimentos"]))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.dieta_id_entry.delete(0, tk.END)
            self.dieta_id_entry.insert(0, values[1])
            self.tipo_var.set(values[2])
            self.alimentos_text.delete("1.0", tk.END)
            self.alimentos_text.insert(tk.END, values[3])

    def try_parse_int(self, val):
        try:
            return int(val)
        except:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Refeição Personalizada - NutriFit")
    RefeicaoPersonalizadaFrame(root)
    root.mainloop()
