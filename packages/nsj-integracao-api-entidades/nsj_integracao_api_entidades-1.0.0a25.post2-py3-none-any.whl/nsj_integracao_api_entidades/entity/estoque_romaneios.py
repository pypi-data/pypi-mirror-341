
import datetime
import uuid

from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.decorator.entity import Entity


@Entity(
    table_name="estoque.romaneios",
    pk_field="romaneio",
    default_order_fields=["numero"],
)
class RomaneioEntity(EntityBase):
    romaneio: uuid.UUID = None
    tenant: int = None
    id_rota: uuid.UUID = None
    id_veiculo: uuid.UUID = None
    id_motorista: uuid.UUID = None
    id_empresa: uuid.UUID = None
    id_usuario_criacao: uuid.UUID = None
    numero: str = None
    situacao: int = None
    data_envio: datetime.datetime = None
    data_entrega: datetime.datetime = None
    data_retorno: datetime.datetime = None
    observacao: str = None
    peso_bruto: float = None
    peso_liquido: float = None
    volumes: float = None
    valor: float = None
    id_entregador: uuid.UUID = None
    geo_localizacao_checkin: dict = None
    geo_localizacao_checkout: dict = None
    checkin: datetime.datetime = None
    checkout: datetime.datetime = None
    data_criacao: datetime.datetime = None
    lastupdate: datetime.datetime = None
    km_estimada: float = None
    duracao_estimada: str = None
    custo_hora_motorista: float = None
    custo_hora_ajudantes: float = None
    custo_hora_entregadores: float = None
    custo_combustivel: float = None
    custo_combustivel_estimado: float = None
    custo_equipe_estimado: float = None
    custo_extra: float = None
    veiculo_km_inicial: float = None
    veiculo_km_final: float = None
    origem: int = None
    horario_inicio: datetime.time = None
    horario_partida: datetime.time = None
    horario_chegada: datetime.time = None
    intervalos: dict = None
    localdeestoque: uuid.UUID = None
    endereco_tipologradouro: str = None
    endereco_logradouro: str = None
    endereco_numero: str = None
    endereco_complemento: str = None
    endereco_cep: str = None
    endereco_bairro: str = None
    endereco_referencia: str = None
    endereco_ibge: str = None
    endereco_cidade: str = None
    endereco_uf: str = None
    ordem_entregas_alterada_por: dict = None
