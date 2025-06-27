import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://localhost:5000/api/usuarios"

class UsuarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Usuários")
        self.root.geometry("850x600")

        self.nome_var = tk.StringVar()
        self.idade_var = tk.StringVar()
        self.peso_var = tk.StringVar()
        self.altura_var = tk.StringVar()
        self.objetivo_var = tk.StringVar()
        self.id_usuario_var = tk.StringVar()

        self.create_widgets()
        self.carregar_usuarios()

    def create_widgets(self):
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.id_usuario_var, width=10).grid(row=0, column=1, sticky="w")

        tk.Button(form_frame, text="Buscar por ID", command=self.buscar_por_id).grid(row=0, column=2, padx=10)

        tk.Label(form_frame, text="Nome:").grid(row=1, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.nome_var, width=40).grid(row=1, column=1, columnspan=2, sticky="w")

        tk.Label(form_frame, text="Idade:").grid(row=2, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.idade_var, width=10).grid(row=2, column=1, sticky="w")

        tk.Label(form_frame, text="Peso (kg):").grid(row=3, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.peso_var, width=10).grid(row=3, column=1, sticky="w")

        tk.Label(form_frame, text="Altura (m):").grid(row=4, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.altura_var, width=10).grid(row=4, column=1, sticky="w")

        tk.Label(form_frame, text="Objetivo:").grid(row=5, column=0, sticky="e")
        objetivos = ["perder peso", "ganhar massa muscular", "manter peso"]
        objetivo_menu = ttk.Combobox(form_frame, textvariable=self.objetivo_var, values=objetivos, state="readonly", width=37)
        objetivo_menu.grid(row=5, column=1, columnspan=2, sticky="w")
        objetivo_menu.current(0)

        tk.Label(form_frame, text="Restrições:").grid(row=6, column=0, sticky="ne")
        self.restricoes_text = tk.Text(form_frame, width=40, height=4)
        self.restricoes_text.grid(row=6, column=1, columnspan=2, sticky="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cadastrar", command=self.cadastrar_usuario, width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Editar", command=self.editar_usuario, width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Excluir", command=self.excluir_usuario, width=15).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Recarregar", command=self.carregar_usuarios, width=15).grid(row=0, column=3, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Idade", "Peso", "Altura", "Objetivo", "Restrições"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def pegar_restricoes(self):
        return self.restricoes_text.get("1.0", tk.END).strip()

    def setar_restricoes(self, texto):
        self.restricoes_text.delete("1.0", tk.END)
        self.restricoes_text.insert(tk.END, texto)

    def limpar_campos(self):
        self.id_usuario_var.set("")
        self.nome_var.set("")
        self.idade_var.set("")
        self.peso_var.set("")
        self.altura_var.set("")
        self.objetivo_var.set("perder peso")
        self.restricoes_text.delete("1.0", tk.END)

    def cadastrar_usuario(self):
        dados = {
            "nome": self.nome_var.get(),
            "idade": self.try_parse_int(self.idade_var.get()),
            "peso": self.try_parse_float(self.peso_var.get()),
            "altura": self.try_parse_float(self.altura_var.get()),
            "objetivo": self.objetivo_var.get(),
            "restricoes": self.pegar_restricoes()
        }
        try:
            response = requests.post(BASE_URL, data=dados)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro desconhecido"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def editar_usuario(self):
        usuario_id = self.id_usuario_var.get()
        if not usuario_id:
            messagebox.showwarning("Atenção", "Informe o ID do usuário.")
            return
        dados = {
            "nome": self.nome_var.get(),
            "idade": self.try_parse_int(self.idade_var.get()),
            "peso": self.try_parse_float(self.peso_var.get()),
            "altura": self.try_parse_float(self.altura_var.get()),
            "objetivo": self.objetivo_var.get(),
            "restricoes": self.pegar_restricoes()
        }
        try:
            response = requests.put(f"{BASE_URL}/{usuario_id}", data=dados)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", response.json().get("message", "Erro desconhecido"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir_usuario(self):
        usuario_id = self.id_usuario_var.get()
        if not usuario_id:
            messagebox.showwarning("Atenção", "Informe o ID do usuário.")
            return
        try:
            response = requests.delete(f"{BASE_URL}/{usuario_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.carregar_usuarios()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Erro ao excluir.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_usuarios(self):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                self.tree.delete(*self.tree.get_children())
                for u in response.json():
                    self.tree.insert("", "end", values=(u["id"], u["nome"], u["idade"], u["peso"], u["altura"], u["objetivo"], u["restricoes"]))
            else:
                messagebox.showerror("Erro", "Erro ao buscar usuários.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_por_id(self):
        usuario_id = self.id_usuario_var.get()
        if not usuario_id:
            messagebox.showwarning("Atenção", "Informe um ID para buscar.")
            return
        try:
            response = requests.get(f"{BASE_URL}/{usuario_id}")
            if response.status_code == 200:
                u = response.json()
                self.nome_var.set(u["nome"])
                self.idade_var.set(u["idade"])
                self.peso_var.set(u["peso"])
                self.altura_var.set(u["altura"])
                self.objetivo_var.set(u["objetivo"])
                self.setar_restricoes(u["restricoes"])
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.id_usuario_var.set(values[0])
            self.nome_var.set(values[1])
            self.idade_var.set(values[2])
            self.peso_var.set(values[3])
            self.altura_var.set(values[4])
            self.objetivo_var.set(values[5])
            self.setar_restricoes(values[6])

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
    app = UsuarioApp(root)
    root.mainloop()
