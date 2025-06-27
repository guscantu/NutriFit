import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://127.0.0.1:5000/api/refeicoes_personalizadas"

class RefeicaoPersonalizadaApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Refeições Personalizadas")
        master.geometry("800x600")
        master.resizable(False, False)

        tipos_refeicao = ['café da manhã', 'almoço', 'lanche', 'jantar']

        
        tk.Label(master, text="ID").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(master, text="ID Dieta Personalizada").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(master, text="Tipo").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Label(master, text="Alimentos").grid(row=3, column=0, sticky="nw", padx=10, pady=5)

        
        self.id_entry = tk.Entry(master, width=30)
        self.dieta_id_entry = tk.Entry(master, width=30)

        self.tipo_var = tk.StringVar(master)
        self.tipo_var.set(tipos_refeicao[0])
        self.tipo_menu = ttk.Combobox(master, textvariable=self.tipo_var, values=tipos_refeicao, width=28, state="readonly")

        self.alimentos_text = tk.Text(master, height=6, width=60)

        self.id_entry.grid(row=0, column=1, pady=5)
        self.dieta_id_entry.grid(row=1, column=1, pady=5)
        self.tipo_menu.grid(row=2, column=1, pady=5, sticky="w")
        self.alimentos_text.grid(row=3, column=1, padx=5, pady=5)

        
        btn_frame = tk.Frame(master)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Buscar", width=15, command=self.buscar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Listar Todas", width=15, command=self.listar_todas).pack(side="left", padx=5)

        
        self.resultado = tk.Text(master, height=12, width=95)
        self.resultado.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def get_text(self, widget):
        return widget.get("1.0", tk.END).strip()

    def cadastrar(self):
        try:
            dados = {
                "dieta_personalizada_id": int(self.dieta_id_entry.get()),
                "tipo": self.tipo_var.get(),
                "alimentos": self.get_text(self.alimentos_text)
            }
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Refeição cadastrada com sucesso!")
                self.limpar_campos()
                self.listar_todas()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        refeicao_id = self.id_entry.get()
        if not refeicao_id:
            messagebox.showwarning("Aviso", "Informe o ID.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{refeicao_id}")
            if response.status_code == 200:
                data = response.json()
                self.dieta_id_entry.delete(0, tk.END)
                self.alimentos_text.delete("1.0", tk.END)
                self.dieta_id_entry.insert(0, data["dieta_personalizada_id"])
                self.tipo_var.set(data["tipo"])
                self.alimentos_text.insert("1.0", data["alimentos"])
            else:
                messagebox.showwarning("Atenção", "Refeição não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        refeicao_id = self.id_entry.get()
        if not refeicao_id:
            messagebox.showwarning("Aviso", "Informe o ID.")
            return
        try:
            dados = {
                "dieta_personalizada_id": int(self.dieta_id_entry.get()),
                "tipo": self.tipo_var.get(),
                "alimentos": self.get_text(self.alimentos_text)
            }
            response = requests.put(f"{BASE_URL}/{refeicao_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Refeição atualizada com sucesso!")
                self.listar_todas()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        refeicao_id = self.id_entry.get()
        if not refeicao_id:
            messagebox.showwarning("Aviso", "Informe o ID para excluir.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{refeicao_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Refeição excluída!")
                self.limpar_campos()
                self.listar_todas()
            else:
                messagebox.showerror("Erro", "Erro ao excluir.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_todas(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                dados = response.json()
                self.resultado.config(state=tk.NORMAL)
                self.resultado.delete(1.0, tk.END)
                if dados:
                    for r in dados:
                        self.resultado.insert(
                            tk.END,
                            f"ID: {r['id']} | Dieta: {r['dieta_personalizada_id']} | Tipo: {r['tipo']}\n"
                            f"Alimentos: {r['alimentos']}\n{'-'*80}\n"
                        )
                else:
                    self.resultado.insert(tk.END, "Nenhuma refeição cadastrada.")
                self.resultado.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao listar."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.dieta_id_entry.delete(0, tk.END)
        self.alimentos_text.delete("1.0", tk.END)
        self.tipo_var.set("café da manhã")

if __name__ == "__main__":
    root = tk.Tk()
    app = RefeicaoPersonalizadaApp(root)
    root.mainloop()
