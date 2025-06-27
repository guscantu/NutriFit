import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://127.0.0.1:5000/api/dietas_personalizadas"

class DietaPersonalizadaApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Dietas Personalizadas")
        master.geometry("750x550")
        master.resizable(False, False)

        objetivos = ['perder peso', 'ganhar massa muscular', 'manter peso']

        
        labels = [
            ("ID", 0), ("Faixa Peso ID", 1), ("Faixa Altura ID", 2),
            ("Faixa Idade ID", 3), ("Objetivo", 4),
            ("Restrição (opcional)", 5), ("Descrição", 6)
        ]
        for text, row in labels:
            tk.Label(master, text=text).grid(row=row, column=0, sticky="w", padx=10, pady=3)

        self.id_entry = tk.Entry(master, width=30)
        self.peso_entry = tk.Entry(master, width=30)
        self.altura_entry = tk.Entry(master, width=30)
        self.idade_entry = tk.Entry(master, width=30)
        self.objetivo_combo = ttk.Combobox(master, values=objetivos, width=28, state="readonly")
        self.restricao_entry = tk.Entry(master, width=30)
        self.descricao_text = tk.Text(master, width=50, height=4)

        self.id_entry.grid(row=0, column=1)
        self.peso_entry.grid(row=1, column=1)
        self.altura_entry.grid(row=2, column=1)
        self.idade_entry.grid(row=3, column=1)
        self.objetivo_combo.grid(row=4, column=1)
        self.restricao_entry.grid(row=5, column=1)
        self.descricao_text.grid(row=6, column=1, pady=3)

        
        btn_frame = tk.Frame(master)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Buscar", width=15, command=self.buscar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Listar Todos", width=15, command=self.listar_todos).pack(side="left", padx=5)

        
        self.resultado = tk.Text(master, height=12, width=90)
        self.resultado.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def get_form_data(self):
        try:
            return {
                "faixa_peso_id": int(self.peso_entry.get()),
                "faixa_altura_id": int(self.altura_entry.get()),
                "faixa_idade_id": int(self.idade_entry.get()),
                "objetivo": self.objetivo_combo.get(),
                "restricao": self.restricao_entry.get(),
                "descricao": self.descricao_text.get("1.0", tk.END).strip()
            }
        except ValueError:
            raise ValueError("IDs devem ser números inteiros.")

    def cadastrar(self):
        try:
            dados = self.get_form_data()
            if not dados["objetivo"] or not dados["descricao"]:
                raise ValueError("Objetivo e descrição são obrigatórios.")
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Dieta personalizada cadastrada com sucesso!")
                self.limpar()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar dieta."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        dieta_id = self.id_entry.get().strip()
        if not dieta_id:
            messagebox.showwarning("Aviso", "Informe o ID da dieta.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{dieta_id}")
            if response.status_code == 200:
                data = response.json()
                self.peso_entry.delete(0, tk.END)
                self.altura_entry.delete(0, tk.END)
                self.idade_entry.delete(0, tk.END)
                self.objetivo_combo.set(data.get("objetivo", ""))
                self.restricao_entry.delete(0, tk.END)
                self.descricao_text.delete("1.0", tk.END)

                self.peso_entry.insert(0, data["faixa_peso_id"])
                self.altura_entry.insert(0, data["faixa_altura_id"])
                self.idade_entry.insert(0, data["faixa_idade_id"])
                self.restricao_entry.insert(0, data.get("restricao", ""))
                self.descricao_text.insert(tk.END, data["descricao"])
            else:
                messagebox.showinfo("Info", "Dieta não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        dieta_id = self.id_entry.get().strip()
        if not dieta_id:
            messagebox.showwarning("Aviso", "Informe o ID da dieta a ser atualizada.")
            return
        try:
            dados = self.get_form_data()
            response = requests.put(f"{BASE_URL}/{dieta_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Dieta atualizada com sucesso!")
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar dieta."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        dieta_id = self.id_entry.get().strip()
        if not dieta_id:
            messagebox.showwarning("Aviso", "Informe o ID da dieta para excluir.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{dieta_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Dieta excluída com sucesso!")
                self.limpar()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao excluir dieta."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todos(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                dietas = response.json()
                self.resultado.config(state=tk.NORMAL)
                self.resultado.delete(1.0, tk.END)
                if dietas:
                    for d in dietas:
                        self.resultado.insert(tk.END,
                            f"ID: {d['id']} | Peso: {d['faixa_peso_id']} | Altura: {d['faixa_altura_id']} | Idade: {d['faixa_idade_id']}\n"
                            f"Objetivo: {d['objetivo']} | Restrição: {d.get('restricao', 'Nenhuma')}\n"
                            f"Descrição: {d['descricao']}\n{'-'*80}\n"
                        )
                else:
                    self.resultado.insert(tk.END, "Nenhuma dieta cadastrada.")
                self.resultado.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar(self):
        self.id_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.altura_entry.delete(0, tk.END)
        self.idade_entry.delete(0, tk.END)
        self.restricao_entry.delete(0, tk.END)
        self.descricao_text.delete("1.0", tk.END)
        self.objetivo_combo.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = DietaPersonalizadaApp(root)
    root.mainloop()
