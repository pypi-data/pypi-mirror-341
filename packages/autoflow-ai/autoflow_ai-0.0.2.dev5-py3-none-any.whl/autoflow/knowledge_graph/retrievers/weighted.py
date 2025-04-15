from collections import defaultdict
from typing import List, Set, Tuple, Optional

from autoflow.knowledge_graph.types import (
    RetrievedKnowledgeGraph,
    RetrievedRelationship,
)
from autoflow.models.embedding_models import EmbeddingModel
from autoflow.storage.graph_store import GraphStore
from autoflow.knowledge_graph.retrievers.base import KGRetriever
from autoflow.storage.graph_store.types import (
    Entity,
    EntityDegree,
    EntityFilters,
    Relationship,
    EntityType,
    RelationshipFilters,
)
from autoflow.storage.types import QueryBundle


# The configuration for the weight coefficient
# format: ((min_weight, max_weight), coefficient)
DEFAULT_WEIGHT_COEFFICIENTS = [
    ((0, 100), 0.01),
    ((100, 1000), 0.001),
    ((1000, 10000), 0.0001),
    ((10000, float("inf")), 0.00001),
]

# The configuration for the range search
# format: ((min_distance, max_distance), search_ratio)
# The sum of search ratio should be 1 except some case we want to search as many as possible relationships.
# In this case, we set the search ratio to 1, and the other search ratio sum should be 1
DEFAULT_RANGE_SEARCH_CONFIG = [
    ((0.0, 0.25), 1),
    ((0.25, 0.35), 0.7),
    ((0.35, 0.45), 0.2),
    ((0.45, 0.55), 0.1),
]

DEFAULT_DEGREE_COEFFICIENT = 0.001


class WeightedGraphRetriever(KGRetriever):
    def __init__(
        self,
        kg_store: GraphStore,
        embedding_model: EmbeddingModel,
        with_degree: bool = False,
        alpha: float = 1,
        weight_coefficients: List[Tuple[float, float]] = None,
        search_range_config: List[Tuple[Tuple[float, float], float]] = None,
        degree_coefficient: float = DEFAULT_DEGREE_COEFFICIENT,
        fetch_synopsis_entities_num: int = 2,
        max_neighbors: int = 10,
    ):
        super().__init__(kg_store)
        self._embedding_model = embedding_model
        self.with_degree = with_degree
        self.alpha = alpha
        self.weight_coefficients = weight_coefficients or DEFAULT_WEIGHT_COEFFICIENTS
        self.search_range_config = search_range_config or DEFAULT_RANGE_SEARCH_CONFIG
        self.degree_coefficient = degree_coefficient
        self.fetch_synopsis_entities_num = fetch_synopsis_entities_num
        self.max_neighbors = max_neighbors

    def retrieve(
        self,
        query: str,
        depth: int = 2,
        metadata_filters: Optional[dict] = None,
    ) -> RetrievedKnowledgeGraph:
        query_embedding = self._embedding_model.get_query_embedding(query)

        visited_relationships = set()
        visited_entities = set()

        new_relationships = self._weighted_search_relationships(
            query_embedding=query_embedding,
            visited_relationships=visited_relationships,
            visited_entities=visited_entities,
            metadata_filters=metadata_filters,
        )

        if len(new_relationships) == 0:
            return RetrievedKnowledgeGraph(
                entities=[],
                relationships=[],
            )

        for rel, score in new_relationships:
            visited_relationships.add(
                RetrievedRelationship(
                    **rel.model_dump(),
                    similarity_score=score,
                    score=score,
                )
            )
            visited_entities.add(rel.source_entity)
            visited_entities.add(rel.target_entity)

        for _ in range(depth - 1):
            actual_number = 0
            progress = 0
            for search_config in DEFAULT_RANGE_SEARCH_CONFIG:
                search_ratio = search_config[1]
                search_distance_range = search_config[0]
                remaining_number = self.max_neighbors - actual_number
                # calculate the expected number based search progress
                # It's an accumulative search, so the expected number should be the difference between the expected number and the actual number
                expected_number = (
                    int((search_ratio + progress) * self.max_neighbors - actual_number)
                    if progress * self.max_neighbors > actual_number
                    else int(search_ratio * self.max_neighbors)
                )
                if expected_number > remaining_number:
                    expected_number = remaining_number
                if remaining_number <= 0:
                    break

                new_relationships = self._weighted_search_relationships(
                    query_embedding=query_embedding,
                    visited_relationships=visited_relationships,
                    visited_entities=visited_entities,
                    search_distance_range=search_distance_range,
                    top_k=expected_number,
                    metadata_filters=metadata_filters,
                )

                for rel, score in new_relationships:
                    visited_relationships.add(
                        RetrievedRelationship(
                            **rel.model_dump(),
                            similarity_score=score,
                            score=score,
                        )
                    )
                    visited_entities.add(rel.source_entity)
                    visited_entities.add(rel.target_entity)

                actual_number += len(new_relationships)
                # search_ratio == 1 won't count the progress
                if search_ratio != 1:
                    progress += search_ratio

        # Fetch related synopsis entities.
        synopsis_entities = self._kg_store.search_entities(
            query=QueryBundle(query_embedding=query_embedding),
            top_k=self.fetch_synopsis_entities_num,
            filters=EntityFilters(
                entity_type=EntityType.synopsis,
            ),
        )
        if len(synopsis_entities) > 0:
            visited_entities.update(synopsis_entities)

        # Rerank final relationships.
        return_relationships = list(visited_relationships)
        return_relationships.sort(key=lambda x: x.score, reverse=True)
        self._fill_entity(return_relationships)

        return_entities = [
            Entity(**e.model_dump())
            for e in visited_entities
        ]

        return RetrievedKnowledgeGraph(
            entities=return_entities,
            relationships=return_relationships,
        )

    def _fill_entity(self, relationships: List[RetrievedRelationship]):
        # FIXME: pytidb should return the relationship field: target_entity, source_entity.
        entity_ids = [item.target_entity_id for item in relationships]
        entity_ids.extend([item.source_entity_id for item in relationships])
        entities = self._kg_store.list_entities(
            filters=EntityFilters(entity_id=entity_ids)
        )
        entity_map = {entity.id: entity for entity in entities}
        for rel in relationships:
            rel.target_entity = Entity(**entity_map[rel.target_entity_id].model_dump())
            rel.source_entity = Entity(**entity_map[rel.source_entity_id].model_dump())

    def _weighted_search_relationships(
        self,
        query_embedding: List[float],
        visited_relationships: Set[RetrievedRelationship],
        visited_entities: Set[Entity],
        search_distance_range: Tuple[float, float] = (0, 1),
        top_k: int = 10,
        metadata_filters: Optional[dict] = None,
    ) -> List[RetrievedRelationship]:
        visited_entity_ids = [e.id for e in visited_entities]
        visited_relationship_ids = [r.id for r in visited_relationships]
        relationships_with_score = self._kg_store.search_relationships(
            query=QueryBundle(query_embedding=query_embedding),
            filters=RelationshipFilters(
                source_entity_id=visited_entity_ids,
                exclude_relationship_ids=visited_relationship_ids,
                metadata=metadata_filters,
            ),
            distance_range=search_distance_range,
            top_k=top_k,
        )

        return self._rank_relationships(
            relationships_with_score=relationships_with_score,
            top_k=top_k,
        )

    def _rank_relationships(
        self,
        relationships_with_score: List[Tuple[Relationship, float]],
        top_k: int = 10,
    ) -> List[Tuple[Relationship, float]]:
        """
        Rerank the relationship based on distance and weight
        """
        # TODO: the degree can br pre-calc and stored in the database in advanced.
        if self.with_degree:
            entity_ids = set()
            for r, _ in relationships_with_score:
                entity_ids.add(r.source_entity_id)
                entity_ids.add(r.target_entity_id)
            entity_degrees = self._kg_store.bulk_calc_entities_degrees(entity_ids)
        else:
            entity_degrees = defaultdict(EntityDegree)

        reranked_relationships = []
        for r, similarity_score in relationships_with_score:
            embedding_distance = 1 - similarity_score
            source_in_degree = entity_degrees[r.source_entity_id].in_degree
            target_out_degree = entity_degrees[r.target_entity_id].out_degree
            final_score = self._calc_relationship_weighted_score(
                embedding_distance,
                r.weight,
                source_in_degree,
                target_out_degree,
            )
            reranked_relationships.append((r, final_score))

        # Rerank relationships based on the calculated score.
        reranked_relationships.sort(key=lambda x: x[1], reverse=True)
        return reranked_relationships[:top_k]

    def _calc_relationship_weighted_score(
        self,
        embedding_distance: float,
        weight: int = 0,
        in_degree: int = 0,
        out_degree: int = 0,
    ) -> float:
        weighted_score = self._calc_weight_score(weight)
        degree_score = 0
        if self.with_degree:
            degree_score = self._calc_degree_score(in_degree, out_degree)
        return self.alpha * (1 / embedding_distance) + weighted_score + degree_score

    def _calc_weight_score(self, weight: float) -> float:
        weight_score = 0.0
        remaining_weight = weight

        for weight_range, coefficient in self.weight_coefficients:
            if remaining_weight <= 0:
                break
            lower_bound, upper_bound = weight_range
            applicable_weight = min(upper_bound - lower_bound, remaining_weight)
            weight_score += applicable_weight * coefficient
            remaining_weight -= applicable_weight

        return weight_score

    def _calc_degree_score(self, in_degree: int, out_degree: int) -> float:
        return (in_degree - out_degree) * self.degree_coefficient
