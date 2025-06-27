from src.controllers.usuario import UsuarioList, UsuarioItem
from src.controllers.dica import DicaList, DicaItem
from src.controllers.produto import ProdutoList, ProdutoItem
from src.controllers.progresso import ProgressoList, ProgressoItem
from src.controllers.restricao_alimentar import RestricaoList, RestricaoItem
from src.controllers.usuario_restricao import UsuarioRestricaoList, UsuarioRestricaoGet,UsuarioRestricaoDelete
from src.controllers.faixa_peso import FaixaPesoList, FaixaPesoItem
from src.controllers.faixa_altura import FaixaAlturaList, FaixaAlturaItem
from src.controllers.faixa_idade import FaixaIdadeList, FaixaIdadeItem
from src.controllers.dieta_personalizada import DietaPersonalizadaList, DietaPersonalizadaItem
from src.controllers.refeicao_personalizada import RefeicaoPersonalizadaList, RefeicaoPersonalizadaItem
from src.controllers.substituicao_alimentar import SubstituicaoAlimentoList, SubstituicaoAlimentoItem

def initialize_endpoints(api):
    # Usuario
    api.add_resource(UsuarioList, "/usuarios")
    api.add_resource(UsuarioItem, "/usuarios/<int:usuario_id>")

    # Dica
    api.add_resource(DicaList, "/dicas")
    api.add_resource(DicaItem, "/dicas/<int:dica_id>")

    # Produto
    api.add_resource(ProdutoList, "/produtos")
    api.add_resource(ProdutoItem, "/produtos/<int:produto_id>")

    # Progresso
    api.add_resource(ProgressoList, "/progresso")
    api.add_resource(ProgressoItem, "/progresso/<int:progresso_id>")

    # Restricao Alimentar
    api.add_resource(RestricaoList, "/restricoes")
    api.add_resource(RestricaoItem, "/restricoes/<int:restricao_id>")

    # Usuario_Restricao
    api.add_resource(UsuarioRestricaoGet, "/usuario_restricoes/<int:usuario_id>")
    api.add_resource(UsuarioRestricaoDelete, "/usuario_restricoes/<int:usuario_id>/<int:restricao_id>")
    api.add_resource(UsuarioRestricaoList, "/usuario_restricoes")


    # Faixa Peso
    api.add_resource(FaixaPesoList, "/faixas_peso")
    api.add_resource(FaixaPesoItem, "/faixas_peso/<int:faixa_peso_id>")

    # Faixa Altura
    api.add_resource(FaixaAlturaList, "/faixas_altura")
    api.add_resource(FaixaAlturaItem, "/faixas_altura/<int:faixa_altura_id>")

    # Faixa Idade
    api.add_resource(FaixaIdadeList, "/faixas_idade")
    api.add_resource(FaixaIdadeItem, "/faixas_idade/<int:faixa_idade_id>")

    # Dieta Personalizada
    api.add_resource(DietaPersonalizadaList, "/dietas_personalizadas")
    api.add_resource(DietaPersonalizadaItem, "/dietas_personalizadas/<int:dieta_personalizada_id>")

    # Refeicao Personalizada
    api.add_resource(RefeicaoPersonalizadaList, "/refeicoes_personalizadas")
    api.add_resource(RefeicaoPersonalizadaItem, "/refeicoes_personalizadas/<int:refeicao_personalizada_id>")

    # Substituicao Alimento
    api.add_resource(SubstituicaoAlimentoList, "/substituicoes_alimento")
    api.add_resource(SubstituicaoAlimentoItem, "/substituicoes_alimento/<int:substituicao_id>")
