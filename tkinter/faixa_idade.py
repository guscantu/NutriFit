import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000/api/faixas_idade"

class FaixaIdadeApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Faixas de Idade")
        master.geometry("650x500")

        
        tk.Label(master, text="ID").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(master, text="Faixa Mínima (anos)").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(master, text="Faixa Máxima (anos)").grid(row=2, column=0, sticky="w", padx=10, pady=5)

        
        self.id_entry = tk.Entry(master, width=30)
        self.faixa_min_entry = tk.Entry(master, width=30)
        self.faixa_max_entry = tk.Entry(master, width=30)

        self.id_entry.grid(row=0, column=1)
        self.faixa_min_entry.grid(row=1, column=1)
        self.faixa_max_entry.grid(row=2, column=1)

        
        btn_frame = tk.Frame(master)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Buscar por ID", width=15, command=self.buscar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Listar Todos", width=15, command=self.listar_todos).pack(side="left", padx=5)

        
        self.resultado = tk.Text(master, height=12, width=75)
        self.resultado.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def cadastrar(self):
        try:
            faixa_min = int(self.faixa_min_entry.get())
            faixa_max = int(self.faixa_max_entry.get())
            if faixa_min >= faixa_max:
                raise ValueError("A idade mínima deve ser menor que a máxima.")

            dados = {"faixa_min": faixa_min, "faixa_max": faixa_max}
            response = requests.post(BASE_URL, json=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Faixa de idade cadastrada com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar faixa de idade."))
        except ValueError as e:
            messagebox.showwarning("Entrada inválida", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        faixa_id = self.id_entry.get().strip()
        if not faixa_id:
            messagebox.showwarning("Aviso", "Informe o ID da faixa de idade.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{faixa_id}")
            if response.status_code == 200:
                data = response.json()
                self.faixa_min_entry.delete(0, tk.END)
                self.faixa_max_entry.delete(0, tk.END)
                self.faixa_min_entry.insert(0, data.get("faixa_min", ""))
                self.faixa_max_entry.insert(0, data.get("faixa_max", ""))
            else:
                messagebox.showwarning("Atenção", "Faixa de idade não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        faixa_id = self.id_entry.get()
        try:
            faixa_min = int(self.faixa_min_entry.get())
            faixa_max = int(self.faixa_max_entry.get())
            if faixa_min >= faixa_max:
                raise ValueError("A idade mínima deve ser menor que a máxima.")

            dados = {"faixa_min": faixa_min, "faixa_max": faixa_max}
            response = requests.put(f"{BASE_URL}/{faixa_id}", json=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Faixa de idade atualizada com sucesso!")
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar faixa de idade."))
        except ValueError as e:
            messagebox.showwarning("Entrada inválida", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        faixa_id = self.id_entry.get().strip()
        if not faixa_id:
            messagebox.showwarning("Aviso", "Informe o ID da faixa de idade para excluir.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{faixa_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Faixa de idade excluída com sucesso!")
                self.limpar_campos()
                self.listar_todos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao excluir faixa de idade."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todos(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                dados = response.json()
                self.resultado.config(state=tk.NORMAL)
                self.resultado.delete(1.0, tk.END)
                if dados:
                    self.resultado.insert(tk.END, "Faixas de idade cadastradas:\n\n")
                    for item in dados:
                        self.resultado.insert(
                            tk.END,
                            f"ID: {item['id']} | Mín: {item['faixa_min']} anos | Máx: {item['faixa_max']} anos\n"
                        )
                else:
                    self.resultado.insert(tk.END, "Nenhuma faixa de idade cadastrada.")
                self.resultado.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao listar faixas."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.faixa_min_entry.delete(0, tk.END)
        self.faixa_max_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaixaIdadeApp(root)
    root.mainloop()
