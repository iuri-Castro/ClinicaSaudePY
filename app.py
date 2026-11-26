from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

pacientes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    try:
        nome = request.form["nome"]
        idade = int(request.form["idade"])
        telefone = int(request.form["telefone"])
        sexo = request.form["sexo"]
    except ValueError:
        return "Erro: Insira valores válidos."

    if nome == "":
        return "Erro: O nome não pode ser vazio."
    if idade <= 0 or idade > 99:
        return "Erro: A idade deve ser um número positivo."
    if telefone <= 0:
        return "Erro: O telefone deve ser um número positivo."
    if sexo not in ["masculino", "feminino", "automovel", "transgenero", "nao_binario", "outro"]:
        return "Erro: Escolha um gênero."

    paciente = {
        "nome": nome,
        "idade": idade,
        "telefone": telefone,
        "sexo": sexo
    }
    pacientes.append(paciente)
    return render_template("cadastro.html")

@app.route("/pacientes")
def pagina_pacientes():
    return render_template("pacientes.html")

@app.route("/lista")
def lista():
    return jsonify(pacientes)

@app.route("/pagina-estatisticas")
def pagina_estatisticas():
    return render_template("estatistica.html")

@app.route("/estatisticas")
def estatisticas():
    total_pacientes = len(pacientes)
    if total_pacientes == 0: 
        return "Erro: Nenhum paciente cadastrado."


    media_idade = sum(p["idade"] for p in pacientes) / total_pacientes

    menor = min(idade["idade"] for idade in pacientes)
    maior = max(idade["idade"] for idade in pacientes)


    return jsonify({
        "total_pacientes": total_pacientes,
        "media_idade": media_idade,
        "menor_idade": menor,
        "maior_idade": maior
    }) 

@app.route("/buscar")
def buscar():
    if not pacientes:
        return "erro:Nenhum paciente cadastrado."
    
    nome = request.args.get("nome").lower()
    resultado = [paciente for paciente in pacientes if nome in paciente["nome"].lower()]
    return jsonify(resultado)

@app.route("/pagina-buscar", methods=["GET", "POST"])
def pagina_buscar():
    return render_template("buscar.html")
    

if __name__ == "__main__":
    app.run(debug=True)