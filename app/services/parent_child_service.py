from app.models.models import ParentChildContextModel, ParentChildRetrievalResultModel, RetrievalResultModel

from app.services.chunking_service import get_parent_chunk


def expand_to_parent(
    result: RetrievalResultModel,
    chunks
) -> ParentChildRetrievalResultModel:

    child = result.chunk
    parent = get_parent_chunk(child, chunks)

    return ParentChildRetrievalResultModel(
        child=child,
        parent=parent,
        score=result.score
    )


def expand_results(results: list[RetrievalResultModel], chunks):

    expanded_results = []

    for result in results:
        expanded = expand_to_parent(
            result,
            chunks
        )

        expanded_results.append(expanded)

    return expanded_results


def deduplicate_parents(expanded_results):

    unique_parents = {}

    for result in expanded_results:

        if result.parent is None:
            continue

        parent_id = result.parent.chunk_id

        if parent_id not in unique_parents:
            unique_parents[parent_id] = result

    return list(unique_parents.values())


def group_by_parent(expanded_results: list[ParentChildRetrievalResultModel]):
    grouped = {}

    for result in expanded_results:

        if result.parent is None:
            continue

        parent_id = result.parent.chunk_id

        if parent_id not in grouped:
            grouped[parent_id] = {
                "parent": result.parent,
                "children": [],
                "score": result.score
            }

        grouped[parent_id]["children"].append(result.child)

        if result.score > grouped[parent_id]["score"]:
            grouped[parent_id]["score"] = result.score

    return [
        ParentChildContextModel(**data)
        for data in grouped.values()
    ]