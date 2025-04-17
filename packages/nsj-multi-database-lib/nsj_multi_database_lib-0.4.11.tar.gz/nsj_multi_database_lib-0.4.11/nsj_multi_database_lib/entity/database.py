import datetime
from nsj_rest_lib.decorator.entity import Entity
import uuid
from nsj_rest_lib.entity.entity_base import EntityBase


@Entity(
    table_name="multibanco.database",
    pk_field="id",
    default_order_fields=["id"],
)
class DatabaseEntity(EntityBase):
    id: uuid.UUID = None
    host: str = None
    porta: int = None
    nome: str = None
    homologacao: bool = None
    user: str = None
    password: str = None
    criado_em: datetime.datetime = None
    criado_por: str = None
    atualizado_em: datetime.datetime = None
    atualizado_por: str = None
    apagado_em: datetime.datetime = None
    apagado_por: str = None
    tenant: str = None
