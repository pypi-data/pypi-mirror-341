from collections.abc import Iterable
from pydantic import BaseModel, field_validator
from typing import TYPE_CHECKING, Any, List, Optional, Union

from kraph.vars import current_ontology, current_graph
import dataclasses
import datetime
from rath.turms.utils import NotQueriedError, get_attributes_or_error


if TYPE_CHECKING:
    from kraph.api.schema import Entity, MeasurementCategory, MetricCategory, RelationCategory, EntityCategory, StructureCategory, MetricKind, Structure, Metric



def validate_reagent_category_definition(cls, value):
    from kraph.api.schema import CategoryDefinitionInput
        
    if isinstance(value, CategoryDefinitionInput):
        return value
    
    tagFilters = []
    categoryFilters = []
    
    if not isinstance(value, Iterable):
        value = [value]
        
    for i in value:
        if isinstance(i, str):
            if i.startswith("class:"):
                categoryFilters.append(i[len("class:") :])
            elif i.startswith("tag:"):
                tagFilters.append(i[len("tag:") :])
            else:
                raise ValueError(f"Unknown filter {i}")
        elif isinstance(i, EntityCategoryTrait):
            raise ValueError("Reagent role cannot have entity categories")
        elif isinstance(i, ReagentCategoryTrait):
            categoryFilters.append(i.id)
        else:
            raise ValueError(f'Unknown filter {i}. Either specify a string with ""tag:" or "class:" or a ReagentCategoryTrait')
    
    if not categoryFilters and not tagFilters:
        raise ValueError("You must specify at least one class or tag filter")
    

    return CategoryDefinitionInput(
        categoryFilters=categoryFilters,
        tagFilters=tagFilters,
    )
    
    
def validate_entitiy_category_definition(cls, value):
    from kraph.api.schema import CategoryDefinitionInput
    
    if isinstance(value, CategoryDefinitionInput):
        return value
    
    tagFilters = []
    categoryFilters = []
    
    if not isinstance(value, list) and not isinstance(value, tuple):
        value = [value]
        
    for i in value:
        if isinstance(i, str):
            if i.startswith("class:"):
                categoryFilters.append(i[len("class:") :])
            elif i.startswith("tag:"):
                tagFilters.append(i[len("tag:") :])
            else:
                raise ValueError(f"Unknown filter {i}")
        elif isinstance(i, EntityCategoryTrait):
            categoryFilters.append(i.id)
        elif isinstance(i, ReagentCategoryTrait):
            raise ValueError("Enitity role cannot have reagent categories")
        else:
            raise ValueError(f'Unknown filter {i}. Either specify a string with ""tag:" or "class:" or a EntityCategoryTrait')
    
    if not categoryFilters and not tagFilters:
        raise ValueError("You must specify at least one class or tag filter")
    

    return CategoryDefinitionInput(
        categoryFilters=categoryFilters,
        tagFilters=tagFilters,
    )


def validate_structure_category_definition(cls, value):
    from kraph.api.schema import CategoryDefinitionInput, create_structure_category
    
    if isinstance(value, CategoryDefinitionInput):
        return value
    
    tagFilters = []
    categoryFilters = []
    
    if not isinstance(value, list) and not isinstance(value, tuple):
        value = [value]
        
    for i in value:
        if isinstance(i, str):
            if i.startswith("@") and "/" in i:
                categoryFilters.append(i)
            if i.startswith("class:"):
                categoryFilters.append(i[len("class:") :])
            elif i.startswith("tag:"):
                tagFilters.append(i[len("tag:") :])
            else:
                raise ValueError(f"Unknown filter {i}")
        elif isinstance(i, EntityCategoryTrait):
            categoryFilters.append(i.id)
        elif isinstance(i, ReagentCategoryTrait):
            raise ValueError("Enitity role cannot have reagent categories")
        else:
            try:
                if issubclass(i, BaseModel):
                    from rekuest_next.structures.default import get_default_structure_registry
        
                    registry = get_default_structure_registry()
                    identifier = registry.get_identifier_for_cls(i)
                    if identifier is None:
                        raise ValueError(f"Structure category {i} not registered")
                    categoryFilters.append(identifier)
                else:
                    raise ValueError(f"Unknown filter {i}")
            except TypeError as e:
                raise e
    
    if not categoryFilters and not tagFilters:
        raise ValueError("You must specify at least one class or tag filter")
    

    return CategoryDefinitionInput(
        categoryFilters=categoryFilters,
        tagFilters=tagFilters,
    )






def assert_is_reagent_or_id(value):
    from kraph.api.schema import Reagent

    if isinstance(value, str):
        return value
    elif getattr(value, "typename", None) == "Reagent":
        return getattr(value, "id")
    else:
        raise ValueError(
            f"Value {value} is not a string or a Reagent. You need to specify a single value for {value} (pass quantity as node mapping instead)"
        )
        
def assert_is_entity_or_id(value):
    from kraph.api.schema import Entity

    if isinstance(value, str):
        return value
    elif getattr(value, "typename", None) == "Entity":
        return getattr(value, "id")
    else:
        raise ValueError(
            f"Value {value} is not a string or a Entity. You need to specify a single value for {value} (pass quantity as node mapping instead)"
        )









@dataclasses.dataclass
class MetricWithValue:
    metric_category: "MetricCategory"
    value: float
    
    def __ror__(self, other):
        from rekuest_next.structures.default import get_default_structure_registry
        from kraph.api.schema import create_structure, create_metric
    
        if isinstance(other, BaseModel):
            registry = get_default_structure_registry()
            structure_string = registry.get_identifier_for_cls(type(other))
            id = get_attributes_or_error(other, "id")
            return create_metric(structure=create_structure(f"{structure_string}:{id}", self.metric_category.graph.id), category=self.metric_category, value=self.value)
        
        if isinstance(other, StructureTrait):
            assert other.graph.id == self.metric_category.graph.id, "Structure and metric must be in the same graph"
            return create_metric(structure=other, category=self.metric_category, value=self.value)
            
        raise NotImplementedError("You can only merge a measurement with a structure")



@dataclasses.dataclass
class MeasurementWithStructureAndValidity:
    measurement_category: "MeasurementCategory"
    structure: "Structure"
    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None
    
    def __or__(self, other):
        from rekuest_next.structures.default import get_default_structure_registry
        from kraph.api.schema import create_structure, create_metric, create_measurement
        
        if isinstance(other, EntityTrait):
            id = get_attributes_or_error(other, "id")
            
            return create_measurement(
                self.measurement_category,
                self.structure.id,
                id,
                valid_from=self.valid_from,
                valid_to=self.valid_to, 
            )
    
        if isinstance(other, BaseModel):
            raise NotImplementedError("You can only merge a measurement with a structure")
            
        
            
        raise NotImplementedError("You can only merge a measurement with a structure")




@dataclasses.dataclass
class MeasurementWithValidity:
    measurement_category: "MeasurementCategory"
    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None
    
    def __ror__(self, other):
        from rekuest_next.structures.default import get_default_structure_registry
        from kraph.api.schema import create_structure, create_metric
        
        if isinstance(other, StructureTrait):
            return MeasurementWithStructureAndValidity(structure=other, valid_from=self.valid_from, valid_to=self.valid_to)       
    
        if isinstance(other, BaseModel):
            from rekuest_next.structures.default import get_default_structure_registry
            registry = get_default_structure_registry()
            structure_string = registry.get_identifier_for_cls(type(other))
            id = get_attributes_or_error(other, "id")
            
            return MeasurementWithStructureAndValidity(measurement_category=self.measurement_category, structure=create_structure(f"{structure_string}:{id}", self.measurement_category.graph.id), valid_from=self.valid_from, valid_to=self.valid_to)
        
            
        
            
        raise NotImplementedError("You can only merge a measurement with a structure")





@dataclasses.dataclass
class IntermediateRelation:
    left: "Entity"
    category: "RelationCategoryTrait"

    def __or__(self, other):
        from kraph.api.schema import create_relation, EntityCategoryDefinition, Entity

        if isinstance(other, Entity):
            source: EntityCategoryDefinition = get_attributes_or_error(self.category, "source_definition")
            target: EntityCategoryDefinition = get_attributes_or_error(self.category, "target_definition")
            
            if source.category_filters:
                assert self.left.category.id in source.category_filters, f"Source {self.left.category} not in {source.category_filters}"
            if source.tag_filters:
                assert self.left.category.id in source.tag_filters, f"Source {self.left.category.id} not in {source.tag_filters}"
                
            if target.category_filters:
                assert other.category.id in target.category_filters, f"Target {other.category.id} not in {target.category_filters}"
                
            if target.tag_filters:
                assert other.category.id in target.tag_filters, f"Target {other.category.id} not in {target.tag_filters}"
            
            return create_relation(source=self.left, target=other, category=self.category)
        
        
        raise NotImplementedError("You can only merge a relation with an entity")


@dataclasses.dataclass
class RelationWithValidity:
    relation: "RelationCategoryTrait"
    value: float
    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None


@dataclasses.dataclass
class IntermediateDescription:
    left: "StructureTrait"
    metric_with_value: "MetricWithValue"

    def __or__(self, other) -> "Metric":
        from kraph.api.schema import create_metric, create_structure

        if isinstance(other, StructureTrait):
            return create_metric(
                self.left,
                self.metric_with_value.metric_category,
                self.metric_with_value.value,
            )
            
        if isinstance(other, BaseModel):
            from rekuest_next.structures.default import get_default_structure_registry
            registry = get_default_structure_registry()
            structure_string = registry.get_identifier_for_cls(type(other))
            id = get_attributes_or_error(other, "id")
            
            structure = create_structure(f"{structure_string}:{id}", self.metric_with_value.metric_category.graph.id)
            return create_metric(structure, self.metric_with_value.metric_category, self.metric_with_value.value)
                
            

        raise NotImplementedError


@dataclasses.dataclass
class IntermediateRelationWithValidity:
    left: "EntityTrait"
    relation_with_validity: RelationWithValidity

    def __or__(self, other):
        from kraph.api.schema import create_relation

        if isinstance(other, EntityTrait):
            return create_relation(
                self.left,
                other,
                self.relation_with_validity.relation,
                valid_from=self.relation_with_validity.valid_from,
                valid_to=self.relation_with_validity.valid_to,
            )

        raise NotImplementedError


class EntityTrait(BaseModel):
    def __or__(self, other):
        if other is None:
            return self

        if isinstance(other, StructureTrait):
            raise NotImplementedError(
                "Cannot merge structures directly, use a relation or measurement inbetween"
            )

        if isinstance(other, EntityTrait):
            raise NotImplementedError(
                "Cannot merge structure and entities directly, use a relation or measurement inbetween"
            )

        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError(
                "When merging a structure and a measurement, please instatiante the measurement with a value first"
            )

        if isinstance(other, RelationCategoryTrait):
            return IntermediateRelation(self, other)


class StructureTrait(BaseModel):
    def __or__(self, other):
        if other is None:
            return self

        if isinstance(other, StructureTrait):
            raise NotImplementedError(
                "Cannot merge structures directly, use a relation or measurement inbetween"
            )

        if isinstance(other, EntityTrait):
            raise NotImplementedError(
                "Cannot merge structure and entities directly, use a relation or measurement inbetween"
            )

        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError(
                "When merging a structure and a measurement, please instatiante the measurement with a value first"
            )

        if isinstance(other, RelationCategoryTrait):
            return

        raise NotImplementedError
    
    
class MetricTrait(BaseModel):
    def __or__(self, other):
        raise NotImplementedError("You cannot merge metrics directly, use a relation or measurement inbetween")

        raise NotImplementedError
    
    

class RelationCategoryTrait(BaseModel):

    def __str__(self):
        return get_attributes_or_error(self, "age_name")
    
    def __or__(self, other):
        raise NotImplementedError

    def __call__(self, valid_from=None, valid_to=None):
        return RelationWithValidity(kind=self, valid_from=valid_from, valid_to=valid_to)


class MeasurementCategoryTrait(BaseModel):
    
    
    def __ror__(self, other):
        from kraph.api.schema import create_measurement

        if isinstance(other, StructureTrait):
            raise ValueError(f"You cannot merge a measurement category with a structure directly, you need to first give it a validity range by Calling the class YOUR_MEASUREMENT(valid_from=..., valid_to=...)")

        if isinstance(other, BaseModel):
            from rekuest_next.structures.default import get_default_structure_registry
            raise ValueError(f"You cannot merge a measurement category with a structure directly, you need to first give it a validity range by Calling the class YOUR_MEASUREMENT(valid_from=..., valid_to=...)")

        raise NotImplementedError(
            "Measurement categories cannot be merged directly, use a relation or measurement inbetween"
        )
    
    
    def __call__(self, valid_from=None, valid_to=None):
        from kraph.api.schema import MetricKind


        return MeasurementWithValidity(
            measurement_category=self,valid_from=valid_from, valid_to=valid_to
        )


class ReagentCategoryTrait(BaseModel):
    
    
    def __call__(self, *args, external_id=None, **kwargs):
        from kraph.api.schema import create_reagent

        """Creates an entity with a name


        """
        id = get_attributes_or_error(self, "id")
        return create_reagent(id, *args, external_id=external_id, **kwargs)



class StructureCategoryTrait(BaseModel):

     

    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use a entitiy instead")

    def create_structure(self, identifier) -> "Entity":
        from kraph.api.schema import create_structure

        """Creates an entity with a name


        """
        graph = current_graph.get()
        return create_structure(identifier, graph)

    def __call__(self, *args, **kwds):
        return self.create_structure(*args, **kwds)



class EntityCategoryTrait(BaseModel):
    """Allows for the creation of a generic categoryss"""

    
    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use an entitiy instead E.g. by calling the category")


    def __call__(self, *args, **kwargs):
        from kraph.api.schema import create_entity

        """Creates an entity with a name


        """
        id = get_attributes_or_error(self, "id")
        return create_entity(id, *args, **kwargs)
    
    
class NaturalEventCategoryTrait(BaseModel):
    """Allows for the creation of a generic category"""

    
    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use an entitiy instead E.g. by calling the category")


    def __call__(self, *args, external_id=None, **kwargs):
        from kraph.api.schema import record_natural_event

        """Creates an entity with a name


        """
        id = get_attributes_or_error(self, "id")
        return record_natural_event(id, *args, **kwargs)
    
    
class ProtocolEventCategoryTrait(BaseModel):
    """Allows for the creation of a generic category"""

    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use an entitiy instead E.g. by calling the category")


    def __call__(self, external_id=None, **kwargs):
        from kraph.api.schema import record_protocol_event, EntityRoleDefinition, ReagentRoleDefinition, NodeMapping, VariableMappingInput, VariableDefinition, Reagent

        """Creates an entity with a name


        """
        reagent_source_roles: list[ReagentRoleDefinition] = get_attributes_or_error(self, "source_reagent_roles")
        reagent_target_roles: list[ReagentRoleDefinition]  = get_attributes_or_error(self, "target_reagent_roles")
        
        entity_source_roles: list[EntityRoleDefinition]  = get_attributes_or_error(self, "source_entity_roles")
        entity_target_roles: list[EntityRoleDefinition]  = get_attributes_or_error(self, "target_entity_roles")
        
        variable_definitions: list[VariableDefinition] = get_attributes_or_error(self, "variable_definitions")
        
        
        entity_sources: list[NodeMapping] = kwargs.get("entity_sources", [])
        entity_targets: list[NodeMapping] = kwargs.get("entity_targets", [])
        reagent_sources: list[NodeMapping] = kwargs.get("reagent_sources", [])
        reagent_targets: list[NodeMapping] = kwargs.get("reagent_targets", [])
        variable_mappings: list[VariableMappingInput] = kwargs.get("variable_mappings", [])
        
        validated_entity_sources = []
        validated_entity_targets = []
        validated_reagent_sources = []
        validated_reagent_targets = []
        validated_variable_mappings = []
        
        
        for i in reagent_source_roles:
            if i.role not in [x.key for x in reagent_sources]:
                if i.needs_quantity:
                    raise ValueError(f"Reagent source role {i.role} requires a quantity. You need to specify a quanitnity in a node mapping for {i.role}")
                
                elif i.role in kwargs:
                    passed_value = kwargs.pop(i.role)
                    assert_is_reagent_or_id(passed_value)
                    validated_reagent_sources.append(NodeMapping(key=i.role, node=passed_value))
                
                else:
                    if i.optional:
                        continue
                    raise ValueError(f"Reagent source role {i.role} not found in source or keyword arguments")
        
            else:
                passed_values = [x.key for x in reagent_sources]
                assert len(passed_values) == 1, f"Reagent source role {i.role} found multiple times in source. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                assert isinstance(passed_values, NodeMapping), f"Reagent source role {i.role} is not a node mapping. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                validated_reagent_sources.append(passed_values[0])
        
        for i in entity_source_roles:
            if i.role not in [x.key for x in entity_sources]:
                if i.role in kwargs:
                    passed_value =  kwargs.pop(i.role)
                    if isinstance(passed_value, list) or isinstance(passed_value, tuple):
                        assert i.allow_multiple, f"Entity source role {i.role} does not allow multiple values. You need to specify a single value for {i.role}"
                        
                        for passed_v in passed_value:
                           assert_is_entity_or_id(passed_v)
                           validated_entity_sources.append(NodeMapping(key=i.role, node=passed_v))
                    else:
                        assert_is_entity_or_id(passed_value)
                        validated_entity_sources.append(NodeMapping(key=i.role, node=passed_value))
                else:
                    if i.optional:
                        continue
                    else:
                        raise ValueError(f"Reagent source role {i.role} not found in source or keyword arguments")
        
            else:
                passed_values = [x.key for x in reagent_sources]
                if len(passed_values) > 1 and not i.allow_multiple:
                    raise ValueError(f"Reagent source role {i.role} found multiple times in source. You need to specify a single value for {i.role}")
                
                for i in passed_values:
                    assert isinstance(i, NodeMapping), f"Reagent source role {i.role} is not a node mapping. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                    validated_entity_sources.append(i)
                
                
                
        for i in reagent_target_roles:
            if i.role not in [x.key for x in reagent_targets]:
                if i.needs_quantity:
                    raise ValueError(f"Reagent target role {i.role} requires a quantity. You need to specify a quanitnity in a node mapping for {i.role}")
                
                elif i.role in kwargs:
                    passed_value =  kwargs.pop(i.role)
                    assert_is_reagent_or_id(passed_value)
                    validated_reagent_targets.append(NodeMapping(key=i.role, node=passed_value))
                
                else:
                    if i.optional:
                        continue
                    raise ValueError(f"Reagent target role {i.role} not found in source or keyword arguments")
        
            else:
                passed_values = [x.key for x in reagent_targets]
                assert len(passed_values) == 1, f"Reagent target role {i.role} found multiple times in source. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                assert isinstance(passed_values, NodeMapping), f"Reagent target role {i.role} is not a node mapping. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                validated_reagent_targets.append(passed_values[0])
                
                
        for i in entity_target_roles:
            if i.role not in [x.key for x in entity_targets]:
                if i.role in kwargs:
                    passed_value = kwargs.pop(i.role)
                    if isinstance(passed_value, list) or isinstance(passed_value, tuple):
                        assert i.allow_multiple, f"Entity target role {i.role} does not allow multiple values. You need to specify a single value for {i.role}"
                        
                        for passed_v in passed_value:
                            assert_is_entity_or_id(passed_v)
                            validated_entity_targets.append(NodeMapping(key=i.role, node=passed_v))
                    else:
                        assert_is_entity_or_id(passed_value)
                        validated_entity_targets.append(NodeMapping(key=i.role, node=passed_value))
                else:
                    if i.optional:
                        continue
                    else:
                        raise ValueError(f"Reagent target role {i.role} not found in source or keyword arguments")
        
            else:
                passed_values = [x.key for x in entity_targets]
                if len(passed_values) > 1 and not i.allow_multiple:
                    raise ValueError(f"Entity target role {i.role} found multiple times in source. You need to specify a single value for {i.role}")
                
                for i in passed_values:
                    assert isinstance(i, NodeMapping), f"Entity target role {i.role} is not a node mapping. You need to specify a single value for {i.role} (pass quantity as node mapping instead)"
                    validated_entity_targets.append(i)
                
                
        for i in variable_definitions:
            if i.param not in [x.key for x in variable_mappings]:
                if i.param in kwargs:
                    passed_value = kwargs.pop(i.param)
                    validated_variable_mappings.append(VariableMappingInput(key=i.param, value=passed_value))
                else:
                    if i.optional:
                        continue
                    else:
                        raise ValueError(f"Variable mapping {i.param} not found in source or keyword arguments")
        
            else:
                passed_values = [x.key for x in variable_mappings]
                assert len(passed_values) == 1, f"Variable mapping {i.param} found multiple times in source. You need to specify a single value for {i.param} (pass quantity as node mapping instead)"
                assert isinstance(passed_values, VariableMappingInput), f"Variable mapping {i.param} is not a node mapping. You need to specify a single value for {i.param} (pass quantity as node mapping instead)"
                validated_variable_mappings.append(passed_values[0])
                
                
        return record_protocol_event(
            category=self,
            external_id=external_id,
            entity_sources=validated_entity_sources,
            entity_targets=validated_entity_targets,
            reagent_sources=validated_reagent_sources,
            reagent_targets=validated_reagent_targets,
            **kwargs,
        )
        
        


class MetricCategoryTrait(BaseModel):
    """Allows for the creation of a generic category"""

    def __or__(self, other):
        raise NotImplementedError("You cannot relate structure categories directly. Use an entitiy instead E.g. by calling the category")


    def __call__(self, value, target=None):
        from kraph.api.schema import create_metric

        """Creates an entity with a name


        """
        try:
            kind = get_attributes_or_error(self, "category.metric_kind")
        except NotQueriedError:
            kind = None
            
        if kind:
            if kind == MetricKind.FLOAT:
                assert isinstance(value, float), "Value must be a float"
            elif kind == MetricKind.INT:
                assert isinstance(value, int), "Value must be an int"
            elif kind == MetricKind.STRING:
                assert isinstance(value, str), "Value must be a string"
            elif kind == MetricKind.BOOLEAN:
                assert isinstance(value, bool), "Value must be a bool"
            else:
                raise NotImplementedError(f"Kind {kind} not implemented")
            
            
        if target is not None:
            assert isinstance(target, StructureTrait), "Target must be an structure"
            assert target.graph.id == self.graph.id, "Target and metric must be in the same graph"
            return create_metric(
                target,
                category=self,
                value=value,
            )

        return MetricWithValue(
            metric_category=self, value=value,
        )





class ExpressionTrait(BaseModel):
    def __or__(self, other):
        raise NotImplementedError

    def __str__(self):
        return getattr(self, "label", super().__str__())


class EntityTrait(BaseModel):
    
    
    def __or__(self, other):
        if isinstance(other, RelationWithValidity):
            return IntermediateRelationWithValidity(left=self, relation_with_validity=other)
        if isinstance(other, EntityTrait):
            raise NotImplementedError("Cannot merge entities directly, use a relation or measurement inbetween")
        if isinstance(other, StructureTrait):
            raise NotImplementedError("Cannot merge entities and structures directly, use a relation or measurement inbetween")
        if isinstance(other, RelationCategoryTrait):
            return IntermediateRelation(self, other)
        if isinstance(other, MeasurementCategoryTrait):
            raise NotImplementedError("When merging a entity and a measurement, please instatiante the measurement with a value first")

    def set(self, metric: "LinkedExpressionTrait", value: float, **kwargs):
        from kraph.api.schema import create_entity_metric, ExpressionKind

        assert isinstance(
            metric, LinkedExpressionTrait
        ), "Metric must be a LinkedExpressionTrait"
        (
            get_attributes_or_error(metric, "kind") == ExpressionKind.METRIC,
            "Expression must be a METRIC",
        )

        return create_entity_metric(entity=self, metric=metric, value=value, **kwargs)

    def subject_to(self, **kwargs):
        from kraph.api.schema import (
            create_protocol_step,
            ProtocolStepInput,
            ExpressionKind,
        )

        return create_protocol_step(input=ProtocolStepInput(entity=self, **kwargs))



class OntologyTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_ontology.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_ontology.reset(self._token)


class GraphTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_graph.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_graph.reset(self._token)
        
        
    def create_entity_category(
        self,
        label: str,
        description: str = None,
        **kwargs,
    ) -> "EntityCategory":
        from kraph.api.schema import create_entity_category

        return create_entity_category(
            graph=self, label=label, description=description, **kwargs
        )
        
    def create_structure_category(
        self,
        identifier: str,
        description: str = None,
        **kwargs,
    ) -> "StructureCategory":
        from kraph.api.schema import create_structure_category

        return create_structure_category(
            graph=self, identifier=identifier, description=description, **kwargs
        )
        
    def create_measurement_category(
        self,
        label: str,
        description: str = None,
        **kwargs,
    ) -> "MeasurementCategory":
        from kraph.api.schema import create_measurement_category

        return create_measurement_category(
            graph=self, label=label, description=description, **kwargs
        )
        
    def create_relation_category(
        self,
        label: str,
        description: str = None,
        **kwargs,
    ) -> "RelationCategory":
        from kraph.api.schema import create_relation_category, CategoryDefinitionInput
        
        return create_relation_category(
            graph=self, label=label, description=description, **kwargs,
        )
        
    def create_metric_category(
        self,
        label: str,
        kind: "MetricKind" = None,
        description: str = None,
        **kwargs,
    ) -> "MetricCategory":
        from kraph.api.schema import create_metric_category

        return create_metric_category(
            graph=self, label=label, description=description, kind=kind, **kwargs
        )


class HasPresignedDownloadAccessor(BaseModel):
    _dataset: Any = None

    def download(self, file_name: str = None) -> "str":
        from kraph.io import download_file

        url, key = get_attributes_or_error(self, "presigned_url", "key")
        return download_file(url, file_name=file_name or key)



class EntityRoleDefinitionInputTrait(BaseModel):
    
    
    
    @field_validator("category_definition", mode="before", check_fields=False)
    def validate_category_definition(cls, value):
        return validate_entitiy_category_definition(cls, value)
    
    

class ReagentRoleDefinitionInputTrait(BaseModel):
    
    
    
    @field_validator("category_definition", mode="before", check_fields=False)
    def validate_category_definition(cls, value):
        return validate_reagent_category_definition(cls, value)
    
    
    
class RelationCategoryInputTrait(BaseModel):
    
    
    @field_validator("source_definition", mode="before", check_fields=False)
    def validate_source_definition(cls, value):
        return validate_entitiy_category_definition(cls, value)
    
    
     
    @field_validator("target_definition", mode="before", check_fields=False)
    def validate_target_definition(cls, value):
        return validate_entitiy_category_definition(cls, value)
    
    
class MeasurementCategoryInputTrait(BaseModel):
    
    
    @field_validator("structure_definition", mode="before", check_fields=False)
    def validate_source_definition(cls, value):
        return validate_structure_category_definition(cls, value)
    
    
     
    @field_validator("entity_definition", mode="before", check_fields=False)
    def validate_target_definition(cls, value):
        return validate_entitiy_category_definition(cls, value)
    
class MetricCategoryInputTrait(BaseModel):
    
    
    @field_validator("structure_definition", mode="before", check_fields=False)
    def validate_source_definition(cls, value):
        return validate_structure_category_definition(cls, value)
    
    
     