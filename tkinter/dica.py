import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://localhost:5000/api/dicas"

class DicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Dicas")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        
        self.id_dica_var = tk.IntVar()
        self.objetivo_var = tk.StringVar(value="perder peso")

        self.create_widgets()
        self.carregar_dicas()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self.root, text="Dados da Dica", padx=10, pady=10)
        frame_form.pack(padx=10, pady=10, fill="x")

        
        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        id_entry = tk.Entry(frame_form, textvariable=self.id_dica_var, width=10)
        id_entry.grid(row=0, column=1, sticky="w")

        tk.Button(frame_form, text="Buscar por ID", command=self.buscar_dica).grid(row=0, column=2, padx=5)

        
        tk.Label(frame_form, text="Objetivo:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        objetivos = ["perder peso", "ganhar massa muscular", "manter peso"]
        objetivo_menu = ttk.OptionMenu(frame_form, self.objetivo_var, objetivos[0], *objetivos)
        objetivo_menu.grid(row=1, column=1, sticky="w", pady=(10, 0))

        
        tk.Label(frame_form, text="Texto:").grid(row=2, column=0, sticky="nw", pady=(10, 0))
        text_frame = tk.Frame(frame_form)
        text_frame.grid(row=2, column=1, columnspan=2, pady=(10, 0), sticky="ew")

        self.texto_text = tk.Text(text_frame, height=5, width=60, wrap="word")
        self.texto_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.texto_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.texto_text.config(yscrollcommand=scrollbar.set)

        
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Cadastrar", width=15, command=self.cadastrar_dica).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar", width=15, command=self.editar_dica).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", width=15, command=self.excluir_dica).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Recarregar", width=15, command=self.carregar_dicas).pack(side="left", padx=5)

        
        columns = ("ID", "Objetivo", "Texto")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100 if col != "Texto" else 400)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def limpar_campos(self):
        self.id_dica_var.set(0)
        self.objetivo_var.set("perder peso")
        self.texto_text.delete("1.0", tk.END)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.id_dica_var.set(values[0])
            self.objetivo_var.set(values[1])
            self.texto_text.delete("1.0", tk.END)
            self.texto_text.insert(tk.END, values[2])

    def buscar_dica(self):
        dica_id = self.id_dica_var.get()
        if dica_id == 0:
            messagebox.showwarning("Aviso", "Informe um ID válido.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{dica_id}")
            if response.status_code == 200:
                dica = response.json()
                self.objetivo_var.set(dica["objetivo"])
                self.texto_text.delete("1.0", tk.END)
                self.texto_text.insert(tk.END, dica["texto"])
            else:
                messagebox.showerror("Erro", f"Dica ID {dica_id} não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na requisição: {e}")

    def cadastrar_dica(self):
        objetivo = self.objetivo_var.get()
        texto = self.texto_text.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "O texto da dica não pode ser vazio.")
            return
        dados = {"objetivo": objetivo, "texto": texto}
        try:
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Dica cadastrada com sucesso!")
                self.carregar_dicas()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro desconhecido"))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na requisição: {e}")

    def editar_dica(self):
        dica_id = self.id_dica_var.get()
        if dica_id == 0:
            messagebox.showwarning("Aviso", "Informe o ID da dica para editar.")
            return
        texto = self.texto_text.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "O texto da dica não pode ser vazio.")
            return
        dados = {"objetivo": self.objetivo_var.get(), "texto": texto}
        try:
            response = requests.put(f"{BASE_URL}/{dica_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Dica atualizada com sucesso!")
                self.carregar_dicas()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro desconhecido"))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na requisição: {e}")

    def excluir_dica(self):
        dica_id = self.id_dica_var.get()
        if dica_id == 0:
            messagebox.showwarning("Aviso", "Informe o ID da dica para excluir.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{dica_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Dica excluída com sucesso!")
                self.carregar_dicas()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a dica.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na requisição: {e}")

    def carregar_dicas(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                dicas = response.json()
                self.tree.delete(*self.tree.get_children())
                for d in dicas:
                    texto_resumo = d["texto"][:70] + ("..." if len(d["texto"]) > 70 else "")
                    self.tree.insert("", "end", values=(d["id"], d["objetivo"], texto_resumo))
            else:
                messagebox.showerror("Erro", "Erro ao buscar dicas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na requisição: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DicaApp(root)
    root.mainloop()
