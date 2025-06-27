import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from new_tkinter.usuario import UsuarioFrame
from new_tkinter.dieta_personalizada import DietaPersonalizadaFrame
from new_tkinter.usuario_restricao import UsuarioRestricaoFrame
from new_tkinter.produto import ProdutoFrame
from new_tkinter.dica import DicaFrame
from new_tkinter.refeicao_personalizada import RefeicaoPersonalizadaFrame
from new_tkinter.progresso import ProgressoFrame
from new_tkinter.restricao_alimentar import RestricaoAlimentarFrame
from new_tkinter.substituicao_alimento import SubstituicaoAlimentoFrame

class NutriFitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriFit - Seu Nutricionista Virtual 🥦")
        self.root.geometry("1000x600")

        
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        
        self.menu_frame = tk.Frame(self.main_frame, width=220, bg="#e0f7fa")
        self.menu_frame.pack(side="left", fill="y")

       
        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.create_menu()
        self.show_home()

    def create_menu(self):
        title = tk.Label(self.menu_frame, text="NutriFit 🍏", bg="#e0f7fa", fg="#00695c",
                         font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        buttons = [
            ("🏠 Início", self.show_home),
            ("👤 Usuários", self.show_usuario),
            ("📊 Progresso", self.show_progresso),
            ("🔒 Restrições", self.show_restricao),
            ("💡 Dicas", self.show_dica),
            ("🛒 Produtos", self.show_produto),
            ("📋 Dietas Personalizadas", self.show_dieta_personalizada),
            ("🍽️ Refeições Personalizadas", self.show_refeicao_personalizada),
            ("🔁 Substituições", self.show_substituicao),
            ("🔗 Usuário x Restrição", self.show_usuario_restricao),
        ]

        for text, command in buttons:
            btn = tk.Button(self.menu_frame, text=text, font=("Helvetica", 12), width=22,
                            bg="#b2dfdb", relief="flat", command=command)
            btn.pack(pady=4)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Bem-vindo ao NutriFit! 🍽️\nSeu nutricionista digital.",
                 font=("Helvetica", 20, "bold"), bg="white", fg="#00796b").pack(pady=50)

        tk.Label(self.content_frame, text="Use o menu à esquerda para navegar entre os módulos.",
                 font=("Helvetica", 14), bg="white").pack()

    
    def show_usuario(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Usuários 👤", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        UsuarioFrame(self.content_frame)        

    def show_progresso(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Progresso 📈", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        ProgressoFrame(self.content_frame)

    def show_restricao(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Restrições Alimentares 🚫", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        RestricaoAlimentarFrame(self.content_frame)

    def show_dica(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Dicas 💡", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        DicaFrame(self.content_frame)

    def show_produto(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Produtos 🛒", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        ProdutoFrame(self.content_frame)

    def show_dieta_personalizada(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Dietas Personalizadas 🥗", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        DietaPersonalizadaFrame(self.content_frame)
        
    def show_refeicao_personalizada(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Refeições Personalizadas 🍽️", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        RefeicaoPersonalizadaFrame(self.content_frame)

    def show_substituicao(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Substituições Alimentares 🍽️", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        SubstituicaoAlimentoFrame(self.content_frame)

    def show_usuario_restricao(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Usuário x Restrição ❗", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
        UsuarioRestricaoFrame(self.content_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = NutriFitApp(root)
    root.mainloop()