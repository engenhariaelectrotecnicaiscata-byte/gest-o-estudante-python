import tkinter as tk
from tkinter import messagebox, simpledialog

ARQUIVO = "estudantes.txt"

# ================== DADOS ==================

def ler_dados():
    dados = []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            for linha in f:
                dados.append(linha.strip())
    except FileNotFoundError:
        open(ARQUIVO, "w", encoding="utf-8").close()
    return dados


def guardar_lista(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for d in dados:
            f.write(d + "\n")


def id_existe(novo_id):
    for linha in ler_dados():
        if linha.split(";")[0] == novo_id:
            return True
    return False


def formatar_linha(linha):
    id_, nome, curso, ano = linha.split(";")
    return f"{id_:<5} | {nome:<20} | {curso:<20} | {ano:<4}"


# ================== LISTA DE ESTUDANTES ==================

def atualizar_lista():
    listbox_estudantes.delete(0, tk.END)
    for d in ler_dados():
        listbox_estudantes.insert(tk.END, formatar_linha(d))
        listbox_estudantes.insert(tk.END, "-" * 60)


def janela_estudantes():
    global listbox_estudantes

    janela_lista = tk.Toplevel(janela)
    janela_lista.title("Estudantes Cadastrados")
    janela_lista.geometry("400x300")

    tk.Label(
        janela_lista,
        text="ID    | Nome                 | Curso                | Ano",
        font=("century", 10, "bold")
    ).pack()

    listbox_estudantes = tk.Listbox(
        janela_lista,
        font=("century", 10),
        width=60
    )
    listbox_estudantes.pack(fill="both", expand=True)

    atualizar_lista()


# ================== CONTROLO DE TELAS ==================

def limpar_tela():
    for widget in frame_principal.winfo_children():
        widget.destroy()


def voltar_menu():
    limpar_tela()
    menu_inicial()


# ================== MENU ==================

def menu_inicial():
    tk.Label(
        frame_principal,
        text="Sistema de Gestão de Estudantes",
        font=("century", 25, "bold")
    ).pack(pady=20)

    tk.Button(frame_principal, text="➕ Cadastrar", width=25, command=tela_cadastrar, font=('Times New Roman',15)).pack(pady=5)
    tk.Button(frame_principal, text="✏️ Editar", width=25, command=tela_editar, font=('Times New Roman',15)).pack(pady=5)
    tk.Button(frame_principal, text="🗑️ Eliminar", width=25, command=tela_eliminar, font=('Times New Roman',15)).pack(pady=5)
    tk.Button(frame_principal, text="🔍 Pesquisar", width=25, command=tela_pesquisar, font=('Times New Roman',15)).pack(pady=5)
    tk.Button(frame_principal, text="❌ Sair", width=25, command=sair, font=('Times New Roman',15)).pack(pady=5)


# ================== CADASTRAR ==================

def tela_cadastrar():
    limpar_tela()

    tk.Label(frame_principal, text="Cadastrar Estudante",
             font=("century", 25, "bold")).pack(pady=10)

    entry_id = tk.Entry(frame_principal)
    entry_nome = tk.Entry(frame_principal)
    entry_curso = tk.Entry(frame_principal)
    entry_ano = tk.Entry(frame_principal)

    for txt, ent in [("ID", entry_id), ("Nome", entry_nome),
                     ("Curso", entry_curso), ("Ano", entry_ano)]:
        tk.Label(frame_principal, text=txt).pack()
        ent.pack()

    def guardar():
        if not entry_id.get() or not entry_nome.get() or not entry_curso.get() or not entry_ano.get():
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        if id_existe(entry_id.get()):
            messagebox.showerror("Erro", "ID já cadastrado!")
            return

        dados = ler_dados()
        dados.append(f"{entry_id.get()};{entry_nome.get()};{entry_curso.get()};{entry_ano.get()}")
        guardar_lista(dados)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Estudante cadastrado!")
        voltar_menu()

    tk.Button(frame_principal, text="💾 Guardar", command=guardar, font=('Times New Roman',15)).pack(pady=5)
    tk.Button(frame_principal, text="🔙 Voltar", command=voltar_menu, font=('Times New Roman',15)).pack()


# ================== EDITAR (ALTERADO) ==================

def tela_editar():
    dados = ler_dados()

    id_procurado = simpledialog.askstring("Editar", "Digite o ID do estudante:")
    if not id_procurado:
        return

    for i, linha in enumerate(dados):
        if linha.split(";")[0] == id_procurado:
            editar_form(i, linha.split(";"))
            return

    messagebox.showerror("Erro", "ID não encontrado!")


def editar_form(indice, registro):
    limpar_tela()

    tk.Label(frame_principal, text="Editar Estudante",
             font=("Segoe UI", 12, "bold")).pack(pady=10)

    entry_id = tk.Entry(frame_principal)
    entry_nome = tk.Entry(frame_principal)
    entry_curso = tk.Entry(frame_principal)
    entry_ano = tk.Entry(frame_principal)

    entry_id.insert(0, registro[0])
    entry_nome.insert(0, registro[1])
    entry_curso.insert(0, registro[2])
    entry_ano.insert(0, registro[3])

    entry_id.config(state="disabled")
    entry_nome.config(state="disabled")

    for txt, ent in [("ID", entry_id), ("Nome", entry_nome),
                     ("Curso", entry_curso), ("Ano", entry_ano)]:
        tk.Label(frame_principal, text=txt).pack()
        ent.pack()

    def guardar():
        dados = ler_dados()
        dados[indice] = f"{registro[0]};{registro[1]};{entry_curso.get()};{entry_ano.get()}"
        guardar_lista(dados)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Dados atualizados!")
        voltar_menu()

    tk.Button(frame_principal, text="💾 Guardar", command=guardar).pack(pady=5)
    tk.Button(frame_principal, text="🔙 Voltar", command=voltar_menu).pack()


# ================== ELIMINAR ==================

def tela_eliminar():
    dados = ler_dados()

    janela_sel = tk.Toplevel(janela)
    janela_sel.title("Eliminar Estudante")
    janela_sel.geometry("400x300")

    listbox = tk.Listbox(janela_sel)
    listbox.pack(fill="both", expand=True)

    for d in dados:
        listbox.insert(tk.END, formatar_linha(d))

    def eliminar():
        try:
            i = listbox.curselection()[0]
        except:
            messagebox.showwarning("Erro", "Selecione um estudante!")
            return

        if messagebox.askyesno("Confirmar", "Deseja eliminar este estudante?"):
            dados.pop(i)
            guardar_lista(dados)
            atualizar_lista()
            janela_sel.destroy()
            messagebox.showinfo("Sucesso", "Estudante eliminado!")

    tk.Button(janela_sel, text="🗑️ Eliminar", command=eliminar).pack(pady=5)


# ================== PESQUISAR ==================

def tela_pesquisar():
    limpar_tela()

    tk.Label(frame_principal, text="Pesquisar Estudante",
             font=("Segoe UI", 12, "bold")).pack(pady=10)

    entry = tk.Entry(frame_principal)
    entry.pack()

    listbox = tk.Listbox(frame_principal, font=("Courier New", 9))
    listbox.pack(fill="both", expand=True, pady=10)

    def pesquisar():
        listbox.delete(0, tk.END)
        termo = entry.get().lower()
        for d in ler_dados():
            if termo in d.lower():
                listbox.insert(tk.END, formatar_linha(d))

    tk.Button(frame_principal, text="🔍 Pesquisar", command=pesquisar).pack()
    tk.Button(frame_principal, text="🔙 Voltar", command=voltar_menu).pack(pady=5)


# ================== SAIR ==================

def sair():
    if messagebox.askyesno("Sair", "Deseja sair do sistema?"):
        janela.destroy()


# ================== JANELA PRINCIPAL ==================

janela = tk.Tk()
janela.title("Gestão de Estudantes")
janela.geometry("500x400")

frame_principal = tk.Frame(janela)
frame_principal.pack(fill="both", expand=True)

menu_inicial()
janela_estudantes()

janela.mainloop()
