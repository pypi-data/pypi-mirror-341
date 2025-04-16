
import datetime
import uuid

from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.decorator.entity import Entity


@Entity(
    table_name="servicos.ordensservicos",
    pk_field="ordemservico",
    default_order_fields=["ordemservico"],
)
class OrdensservicoEntity(EntityBase):
    ordemservico: uuid.UUID = None
    tenant: int = None
    data_criacao: datetime.datetime = None
    hora_criacao: datetime.time = None
    chamadotecnico_id: uuid.UUID = None
    situacao: int = None
    referenciaexterna: str = None
    tipoordemservico_id: uuid.UUID = None
    ordemservicoretorno_id: uuid.UUID = None
    origem: int = None
    estabelecimento_id: uuid.UUID = None
    cliente_id: uuid.UUID = None
    objetoservico_id: uuid.UUID = None
    enderecocliente_id: uuid.UUID = None
    valor_total: float = None
    xml_docengine: str = None
    contrato_id: uuid.UUID = None
    tipo_manutencao: uuid.UUID = None
    situacao_maquina_chamado: int = None
    sintoma: str = None
    situacao_maquina_chegada: int = None
    causa: str = None
    situacao_maquina_saida: int = None
    intervencao: str = None
    observacao: str = None
    horimetro: float = None
    numero: int = None
    usuario_id: uuid.UUID = None
    assinado_por: str = None
    orcamento_gerado: bool = None
    numero_orcamento: int = None
    responsavel_orcamento: str = None
    pedido_garantia: str = None
    lastupdate: datetime.datetime = None
    tabeladepreco_id: uuid.UUID = None
    operacaoordemservico_codigo: str = None
    operacaoordemservico_id: uuid.UUID = None
    ordemservicovinculada: uuid.UUID = None
    pessoamunicipio: uuid.UUID = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    responsavel_web: str = None
    projeto: uuid.UUID = None
    rascunho: bool = None
    created_by: dict = None
    updated_by: dict = None
    grupoempresarial: uuid.UUID = None
    serie: str = None
    centrodecusto: uuid.UUID = None
    observacaointerna: str = None
    responsavel: uuid.UUID = None
    motivofinalizacao: str = None
    tipologradouro: str = None
    pais: str = None
    ibge: str = None
    logradouro: str = None
    numeroendereco: str = None
    complemento: str = None
    cep: str = None
    bairro: str = None
    uf: str = None
    cidade: str = None
    latitude: float = None
    longitude: float = None
    cidadeestrangeira: str = None
    urlassinatura: str = None
    idserie: uuid.UUID = None
    numeronegocio: str = None
    transportepublico: bool = None
    situacaoagendamento: int = None
    dataconfirmacaoagendamento: datetime.datetime = None
    nometecnicoconfirmacao: str = None
    atc_id: uuid.UUID = None
    recurso: uuid.UUID = None
    tiporecurso: int = None
    tipoagendamento: int = None
    enderecoorigem: uuid.UUID = None
    lote: int = None
    situacaoanteriorimpedido: int = None
    cancelamentoautomatico: bool = None
    situacaoanteriorrps: int = None
