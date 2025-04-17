import uuid
from functools import partial

from ..types_app import Any, TypeFieldsDict, TypeFieldsListNone, TypeModel

__all__ = [
    "Data",
]


class Data:
    """
    Attributes:
        model: TypeModel - Model class
        create_data: dict[str, Any] - all not-nullable (required) fields with valid values
        update_data: dict[str, Any] = {} - arbitrary fields with valid values
        default_data: dict[str, Any] = {} - all default fields (besides `id`) with default values
        pk_fields: list[str] = [] - all primary key fields (besides `id`)
        unique_fields: list[str] = [] - all unique fields (besides `id`)
        indexed_fields: list[str] = [] - all indexed fields
        nullable_fields: list[str] = [] - all nullable fields
    """

    @staticmethod
    def get_val_or_sub(value: Any | None, substitution: Any):
        # used here and in base_test_model.py
        return value or substitution

    def add_id(self, *, as_uuid: bool = True, **data) -> dict[str, Any]:
        # used here and in base_test_crud.py
        return {"id": self.item_uuid if as_uuid else str(self.item_uuid), **data}

    def __init__(
        self,
        *,
        model: TypeModel,
        create_data: TypeFieldsDict,
        update_data: TypeFieldsDict | None = None,
        default_data: TypeFieldsDict | None = None,
        pk_fields: TypeFieldsListNone = None,
        unique_fields: TypeFieldsListNone = None,
        indexed_fields: TypeFieldsListNone = None,
        nullable_fields: TypeFieldsListNone = None,
    ) -> None:
        # Manually set data =================================================
        self.model = model
        self.create_data = create_data
        self.update_data = self.get_val_or_sub(update_data, create_data)
        self.default_data = self.get_val_or_sub(default_data, {})
        self.pk_fields = self.get_val_or_sub(pk_fields, []) + ["id"]
        self.unique_fields = self.get_val_or_sub(unique_fields, [])
        self.indexed_fields = self.get_val_or_sub(indexed_fields, [])
        self.nullable_fields = self.get_val_or_sub(nullable_fields, [])
        self.item_uuid = uuid.uuid4()
        # Calculated data ======================================================
        _expected_create = {
            **{}.fromkeys(self.nullable_fields),
            **self.default_data,
            **self.create_data,
        }
        _expected_update = {
            **_expected_create,
            **self.update_data,
        }

        # Model
        self.dump_initial = {
            # **{c.name: None for c in self.model.__table__.c},
            **{}.fromkeys(c.name for c in self.model.__table__.c),
            **self.create_data,
        }

        # CRUD - create_data and update_data will be manipulated with add_id in the base_test_crud.py
        self.get_test_obj = lambda *args, **kwargs: self.model(
            **self.add_id(**self.create_data)
        )
        self.expected_create = self.add_id(**_expected_create)  # type: ignore [arg-type]
        self.expected_update = self.add_id(**_expected_update)  # type: ignore [arg-type]

        # API/Bot
        jsonify = partial(self.add_id, as_uuid=False)
        self.create_data_json = jsonify(**self.create_data)
        self.update_data_json = jsonify(**self.update_data)
        self.expected_response_json_create = jsonify(**_expected_create)
        self.expected_response_json_update = jsonify(**_expected_update)
