import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000/api/substituicoes_alimento"

class SubstituicaoAlimentoApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Substituições de Alimentos")
        master.geometry("750x500")

        
        tk.Label(master, text="ID").grid(row=0, column=0, sticky="w", padx=10, pady=3)
        tk.Label(master, text="Restrição ID").grid(row=1, column=0, sticky="w", padx=10, pady=3)
        tk.Label(master, text="Alimento Original").grid(row=2, column=0, sticky="w", padx=10, pady=3)
        tk.Label(master, text="Alimento Substituto").grid(row=3, column=0, sticky="w", padx=10, pady=3)

        
        self.id_entry = tk.Entry(master, width=40)
        self.restricao_id_entry = tk.Entry(master, width=40)
        self.alimento_original_entry = tk.Entry(master, width=40)
        self.alimento_substituto_entry = tk.Entry(master, width=40)

        self.id_entry.grid(row=0, column=1, pady=3)
        self.restricao_id_entry.grid(row=1, column=1, pady=3)
        self.alimento_original_entry.grid(row=2, column=1, pady=3)
        self.alimento_substituto_entry.grid(row=3, column=1, pady=3)

        
        btn_frame = tk.Frame(master)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Buscar", width=15, command=self.buscar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Listar Todas", width=15, command=self.listar_todas).pack(side="left", padx=5)

        
        self.resultado = tk.Text(master, height=10, width=90)
        self.resultado.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def cadastrar(self):
        try:
            dados = {
                "restricao_id": int(self.restricao_id_entry.get()),
                "alimento_original": self.alimento_original_entry.get().strip(),
                "alimento_substituto": self.alimento_substituto_entry.get().strip()
            }
            response = requests.post(BASE_URL, json=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Substituição cadastrada com sucesso!")
                self.limpar_campos()
                self.listar_todas()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        substituicao_id = self.id_entry.get()
        if not substituicao_id:
            messagebox.showwarning("Aviso", "Informe o ID.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{substituicao_id}")
            if response.status_code == 200:
                data = response.json()
                self.restricao_id_entry.delete(0, tk.END)
                self.alimento_original_entry.delete(0, tk.END)
                self.alimento_substituto_entry.delete(0, tk.END)

                self.restricao_id_entry.insert(0, data["restricao_id"])
                self.alimento_original_entry.insert(0, data["alimento_original"])
                self.alimento_substituto_entry.insert(0, data["alimento_substituto"])
            else:
                messagebox.showwarning("Atenção", "Substituição não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        substituicao_id = self.id_entry.get()
        if not substituicao_id:
            messagebox.showwarning("Aviso", "Informe o ID.")
            return
        try:
            dados = {
                "restricao_id": int(self.restricao_id_entry.get()),
                "alimento_original": self.alimento_original_entry.get().strip(),
                "alimento_substituto": self.alimento_substituto_entry.get().strip()
            }
            response = requests.put(f"{BASE_URL}/{substituicao_id}", json=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Substituição atualizada com sucesso!")
                self.listar_todas()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        substituicao_id = self.id_entry.get()
        if not substituicao_id:
            messagebox.showwarning("Aviso", "Informe o ID.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{substituicao_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Substituição excluída!")
                self.limpar_campos()
                self.listar_todas()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao excluir."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todas(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                substituicoes = response.json()
                self.resultado.config(state=tk.NORMAL)
                self.resultado.delete(1.0, tk.END)
                if substituicoes:
                    for s in substituicoes:
                        self.resultado.insert(
                            tk.END,
                            f"ID: {s['id']} | Restrição ID: {s['restricao_id']}\n"
                            f"Original: {s['alimento_original']} → Substituto: {s['alimento_substituto']}\n"
                            + "-"*70 + "\n"
                        )
                else:
                    self.resultado.insert(tk.END, "Nenhuma substituição cadastrada.")
                self.resultado.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Erro", "Erro ao listar substituições.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.restricao_id_entry.delete(0, tk.END)
        self.alimento_original_entry.delete(0, tk.END)
        self.alimento_substituto_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SubstituicaoAlimentoApp(root)
    root.mainloop()
