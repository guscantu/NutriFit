import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import requests

BASE_URL = "http://127.0.0.1:5000/api/produtos"

class ProdutoApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciar Produtos")
        master.geometry("750x600")
        master.resizable(False, False)

        self.create_widgets()
        self.carregar_produtos()

    def create_widgets(self):
        frame = tk.LabelFrame(self.master, text="Cadastro de Produto", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        
        tk.Label(frame, text="ID:").grid(row=0, column=0, sticky="w")
        self.id_entry = tk.Entry(frame, width=10)
        self.id_entry.grid(row=0, column=1, sticky="w")

        tk.Button(frame, text="Buscar por ID", command=self.buscar).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Nome:").grid(row=1, column=0, sticky="w")
        self.nome_entry = tk.Entry(frame, width=50)
        self.nome_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        tk.Label(frame, text="Descrição:").grid(row=2, column=0, sticky="nw")
        self.desc_text = scrolledtext.ScrolledText(frame, width=60, height=4, wrap=tk.WORD)
        self.desc_text.grid(row=2, column=1, columnspan=2, sticky="w")

        tk.Label(frame, text="Preço:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.preco_entry = tk.Entry(frame, width=20)
        self.preco_entry.grid(row=3, column=1, sticky="w", pady=(10, 0))

        tk.Label(frame, text="Link de Compra:").grid(row=4, column=0, sticky="w")
        self.link_entry = tk.Entry(frame, width=50)
        self.link_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        
        botoes = tk.Frame(self.master)
        botoes.pack(pady=10)

        tk.Button(botoes, text="Cadastrar", width=15, command=self.cadastrar).pack(side="left", padx=5)
        tk.Button(botoes, text="Atualizar", width=15, command=self.atualizar).pack(side="left", padx=5)
        tk.Button(botoes, text="Excluir", width=15, command=self.excluir).pack(side="left", padx=5)
        tk.Button(botoes, text="Listar Todos", width=15, command=self.carregar_produtos).pack(side="left", padx=5)

        
        colunas = ("ID", "Nome", "Preço", "Link")
        self.tree = ttk.Treeview(self.master, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == "Nome":
                self.tree.column(col, width=200)
            elif col == "Link":
                self.tree.column(col, width=250)
            else:
                self.tree.column(col, width=80, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)

    def preencher_campos(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, item[0])
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, item[1])
            self.preco_entry.delete(0, tk.END)
            self.preco_entry.insert(0, item[2])
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert(0, item[3])

    def limpar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.preco_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)

    def cadastrar(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "O nome do produto é obrigatório.")
            return

        dados = {
            "nome": nome,
            "descricao": self.desc_text.get("1.0", tk.END).strip(),
            "preco": float(self.preco_entry.get()) if self.preco_entry.get() else None,
            "link_compra": self.link_entry.get().strip() or None
        }

        try:
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self.limpar_campos()
                self.carregar_produtos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao cadastrar produto."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar(self):
        produto_id = self.id_entry.get()
        if not produto_id:
            messagebox.showwarning("Aviso", "Informe o ID do produto.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{produto_id}")
            if response.status_code == 200:
                data = response.json()
                self.nome_entry.delete(0, tk.END)
                self.desc_text.delete("1.0", tk.END)
                self.preco_entry.delete(0, tk.END)
                self.link_entry.delete(0, tk.END)

                self.nome_entry.insert(0, data["nome"])
                self.desc_text.insert(tk.END, data["descricao"] or "")
                self.preco_entry.insert(0, data["preco"] if data["preco"] is not None else "")
                self.link_entry.insert(0, data["link_compra"] or "")
            else:
                messagebox.showwarning("Atenção", "Produto não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar(self):
        produto_id = self.id_entry.get()
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "O nome do produto é obrigatório.")
            return

        dados = {
            "nome": nome,
            "descricao": self.desc_text.get("1.0", tk.END).strip(),
            "preco": float(self.preco_entry.get()) if self.preco_entry.get() else None,
            "link_compra": self.link_entry.get().strip() or None
        }

        try:
            response = requests.put(f"{BASE_URL}/{produto_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                self.limpar_campos()
                self.carregar_produtos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro ao atualizar produto."))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir(self):
        produto_id = self.id_entry.get()
        if not produto_id:
            messagebox.showwarning("Aviso", "Informe o ID do produto para excluir.")
            return

        try:
            response = requests.delete(f"{BASE_URL}/{produto_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.limpar_campos()
                self.carregar_produtos()
            else:
                messagebox.showwarning("Atenção", "Produto não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_produtos(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                produtos = response.json()
                self.tree.delete(*self.tree.get_children())
                for p in produtos:
                    self.tree.insert("", "end", values=(p["id"], p["nome"], p["preco"], p["link_compra"] or ""))
            else:
                messagebox.showerror("Erro", "Erro ao carregar produtos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProdutoApp(root)
    root.mainloop()
