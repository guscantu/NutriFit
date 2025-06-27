import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://localhost:5000/api/usuario_restricoes"

class UsuarioRestricaoApp:
    def __init__(self, master):
        self.master = master
        master.title("Associação Usuário x Restrição")
        master.geometry("650x450")
        master.resizable(False, False)

        tk.Label(master, text="ID do Usuário:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.usuario_entry = tk.Entry(master, width=20)
        self.usuario_entry.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(master, text="ID da Restrição:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.restricao_entry = tk.Entry(master, width=20)
        self.restricao_entry.grid(row=1, column=1, pady=5, sticky="w")

        btn_frame = tk.Frame(master)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Associar Restrição", command=self.associar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Remover Restrição", command=self.remover).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Listar Restrições do Usuário", command=self.listar_restricoes).pack(side="left", padx=5)

        self.resultado = tk.Text(master, height=18, width=80)
        self.resultado.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def associar(self):
        usuario_id = self.usuario_entry.get().strip()
        restricao_id = self.restricao_entry.get().strip()

        if not usuario_id or not restricao_id:
            messagebox.showwarning("Aviso", "Preencha os campos corretamente.")
            return

        try:
            payload = {"usuario_id": int(usuario_id), "restricao_id": int(restricao_id)}
            response = requests.post(BASE_URL, json=payload)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Restrição associada.")
                self.limpar_campos()
                self.listar_restricoes()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro inesperado."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover(self):
        usuario_id = self.usuario_entry.get().strip()
        restricao_id = self.restricao_entry.get().strip()

        if not usuario_id or not restricao_id:
            messagebox.showwarning("Aviso", "Preencha os campos corretamente.")
            return

        try:
            payload = {"usuario_id": int(usuario_id), "restricao_id": int(restricao_id)}
            response = requests.delete(BASE_URL, json=payload)
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Restrição removida.")
                self.limpar_campos()
                self.listar_restricoes()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro inesperado."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_restricoes(self):
        usuario_id = self.usuario_entry.get().strip()

        if not usuario_id:
            messagebox.showwarning("Aviso", "Informe o ID do usuário.")
            return

        try:
            url = f"{BASE_URL}/{int(usuario_id)}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                restricoes = data.get("restricoes", [])
                self.resultado.config(state=tk.NORMAL)
                self.resultado.delete(1.0, tk.END)

                if isinstance(restricoes, list) and restricoes:
                    self.resultado.insert(tk.END, f"Restrições do usuário {usuario_id}:\n\n")
                    for r in restricoes:
                        if isinstance(r, dict) and "id" in r and "nome" in r:
                            self.resultado.insert(tk.END, f"- ID: {r['id']} | Nome: {r['nome']}\n")
                        elif isinstance(r, int):  # fallback: apenas id
                            self.resultado.insert(tk.END, f"- ID: {r}\n")
                        else:
                            self.resultado.insert(tk.END, f"- Entrada desconhecida: {r}\n")
                else:
                    self.resultado.insert(tk.END, "Este usuário não possui restrições associadas.")
                self.resultado.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao listar restrições."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        self.usuario_entry.delete(0, tk.END)
        self.restricao_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UsuarioRestricaoApp(root)
    root.mainloop()
