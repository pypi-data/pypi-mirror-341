from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResultTableNode")


@_attrs_define
class ResultTableNode:
    """This can be either a folder or a table

    Attributes:
        kind (Union[None, Unset, str]): What type of node is this. Either Table or Folder.
        help_ (Union[None, Unset, str]): A link to the help documentation for this node, if it exists
        name (Union[None, Unset, str]): The name of this node, this is used for referencing in other HTTP queries
        display_name (Union[None, Unset, str]): The display name of this node, e.g. this will make something like
            "CorrelationGroup9" into "Correlation Group 9"
        is_in_use (Union[None, Unset, bool]): Whether or not this result table was output by the model calculation.
        children (Union[None, Unset, list['ResultTableNode']]): If Kind equals Folder then the children contains a list
            of tables and subfolders that logically sit inside this folder.
    """

    kind: Union[None, Unset, str] = UNSET
    help_: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    display_name: Union[None, Unset, str] = UNSET
    is_in_use: Union[None, Unset, bool] = UNSET
    children: Union[None, Unset, list["ResultTableNode"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: Union[None, Unset, str]
        if isinstance(self.kind, Unset):
            kind = UNSET
        else:
            kind = self.kind

        help_: Union[None, Unset, str]
        if isinstance(self.help_, Unset):
            help_ = UNSET
        else:
            help_ = self.help_

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        display_name: Union[None, Unset, str]
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        is_in_use: Union[None, Unset, bool]
        if isinstance(self.is_in_use, Unset):
            is_in_use = UNSET
        else:
            is_in_use = self.is_in_use

        children: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.children, Unset):
            children = UNSET
        elif isinstance(self.children, list):
            children = []
            for children_type_0_item_data in self.children:
                children_type_0_item = children_type_0_item_data.to_dict()
                children.append(children_type_0_item)

        else:
            children = self.children

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if help_ is not UNSET:
            field_dict["help"] = help_
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if is_in_use is not UNSET:
            field_dict["isInUse"] = is_in_use
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_kind(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        kind = _parse_kind(d.pop("kind", UNSET))

        def _parse_help_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        help_ = _parse_help_(d.pop("help", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_display_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_name = _parse_display_name(d.pop("displayName", UNSET))

        def _parse_is_in_use(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_in_use = _parse_is_in_use(d.pop("isInUse", UNSET))

        def _parse_children(data: object) -> Union[None, Unset, list["ResultTableNode"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                children_type_0 = []
                _children_type_0 = data
                for children_type_0_item_data in _children_type_0:
                    children_type_0_item = ResultTableNode.from_dict(children_type_0_item_data)

                    children_type_0.append(children_type_0_item)

                return children_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ResultTableNode"]], data)

        children = _parse_children(d.pop("children", UNSET))

        result_table_node = cls(
            kind=kind,
            help_=help_,
            name=name,
            display_name=display_name,
            is_in_use=is_in_use,
            children=children,
        )

        return result_table_node
