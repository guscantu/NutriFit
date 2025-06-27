import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://localhost:5000/api/usuario_restricoes"

class UsuarioRestricaoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        form = tk.Frame(self)
        form.pack(pady=10, padx=20, fill="x")

        
        tk.Label(form, text="Usuário ID:").grid(row=0, column=0)
        self.usuario_entry = tk.Entry(form)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(form, text="Restrição ID:").grid(row=1, column=0)
        self.restricao_entry = tk.Entry(form)
        self.restricao_entry.grid(row=1, column=1)

        
        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Associar", command=self.associar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Remover", command=self.remover).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Ver Restrições do Usuário", command=self.buscar).grid(row=0, column=2, padx=5)

        
        self.tree = ttk.Treeview(self, columns=("ID da Restrição", "Nome"), show="headings")
        self.tree.heading("ID da Restrição", text="ID da Restrição")
        self.tree.heading("Nome", text="Nome")
        self.tree.column("ID da Restrição", anchor="center")
        self.tree.column("Nome", anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def associar(self):
        try:
            dados = {
                "usuario_id": int(self.usuario_entry.get()),
                "restricao_id": int(self.restricao_entry.get())
            }
            r = requests.post(BASE_URL, json=dados)
            if r.status_code == 201:
                messagebox.showinfo("Sucesso", "Restricão associada ao usuário!")
                self.buscar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro na requisição"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover(self):
        try:
            usuario_id = int(self.usuario_entry.get())
            restricao_id = int(self.restricao_entry.get())
            r = requests.delete(f"{BASE_URL}/{usuario_id}/{restricao_id}")
            if r.status_code == 204:
                messagebox.showinfo("Sucesso", "Associação removida!")
                self.buscar()
            else:
                messagebox.showerror("Erro", r.json().get("message", "Erro ao remover"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        try:
            usuario_id = int(self.usuario_entry.get())
            r = requests.get(f"{BASE_URL}/{usuario_id}")
            if r.status_code == 200:
                dados = r.json()
                self.tree.delete(*self.tree.get_children())
                for r in dados.get("restricoes", []):
                    self.tree.insert("", tk.END, values=(r["id"], r["nome"]))
            else:
                messagebox.showerror("Erro", "Usuário não encontrado")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Usuário x Restrição - NutriFit")
    UsuarioRestricaoFrame(root)
    root.mainloop()
