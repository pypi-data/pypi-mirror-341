
import datetime
import uuid

from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.decorator.entity import Entity


@Entity(
    table_name="estoque.unidades",
    pk_field="unidade",
    default_order_fields=["codigo"],
)
class UnidadeEntity(EntityBase):
    unidade: uuid.UUID = None
    tenant: int = None
    codigo: str = None
    decimais: int = None
    descricao: str = None
    id_grupo: uuid.UUID = None
    lastupdate: datetime.datetime = None
    created_at: datetime.datetime = None
    created_by: dict = None
    updated_at: datetime.datetime = None
    updated_by: dict = None
    id_conjunto: uuid.UUID = None
