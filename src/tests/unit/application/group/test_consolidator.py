from deps_api_gateway.application.group.consolidator import GroupsConsolidator

SPLITTER_WITHOUT_DOC_TYPE = {
    "id": "splitter-id-1",
    "groupId": "group-id-1",
    "documentTypeId": None,
    "name": "Splitter 1",
    "description": "Description 1",
}

SPLITTER_WITH_DOC_TYPE = {
    "id": "splitter-id-2",
    "groupId": "group-id-2",
    "documentTypeId": "doc-type-id-1",
    "name": "Splitter 2",
    "description": "Description 2",
}

GROUP_1 = {"id": "group-id-1", "name": "Group 1", "documentTypeIds": [], "createdAt": "2024-01-01T00:00:00"}
GROUP_2 = {"id": "group-id-2", "name": "Group 2", "documentTypeIds": [], "createdAt": "2024-01-01T00:00:00"}
GROUP_99 = {"id": "group-id-99", "name": "Group 99", "documentTypeIds": [], "createdAt": "2024-01-01T00:00:00"}


def test_consolidate_groups__matching_splitter__splitter_added_to_group(
    ok_proxy_response__maker,
) -> None:
    groups_response = ok_proxy_response__maker({"meta": {"total": 1}, "result": [GROUP_1]})
    splittings_response = ok_proxy_response__maker({"splitters": [SPLITTER_WITHOUT_DOC_TYPE], "total": 1})

    result = GroupsConsolidator.consolidate_groups(
        groups_response=groups_response,
        splittings_response=splittings_response,
    )

    assert result.json()["result"][0]["splitter"] == SPLITTER_WITHOUT_DOC_TYPE  # type: ignore


def test_consolidate_groups__splitter_has_document_type_id__splitter_not_matched(
    ok_proxy_response__maker,
) -> None:
    groups_response = ok_proxy_response__maker({"meta": {"total": 1}, "result": [GROUP_2]})
    splittings_response = ok_proxy_response__maker({"splitters": [SPLITTER_WITH_DOC_TYPE], "total": 1})

    result = GroupsConsolidator.consolidate_groups(
        groups_response=groups_response,
        splittings_response=splittings_response,
    )

    assert result.json()["result"][0]["splitter"] is None  # type: ignore


def test_consolidate_groups__no_splitter_for_group__splitter_is_null(
    ok_proxy_response__maker,
) -> None:
    groups_response = ok_proxy_response__maker({"meta": {"total": 1}, "result": [GROUP_99]})
    splittings_response = ok_proxy_response__maker({"splitters": [SPLITTER_WITHOUT_DOC_TYPE], "total": 1})

    result = GroupsConsolidator.consolidate_groups(
        groups_response=groups_response,
        splittings_response=splittings_response,
    )

    assert result.json()["result"][0]["splitter"] is None  # type: ignore


def test_consolidate_groups__groups_not_ok__returns_groups_response(
    not_ok_proxy_response__maker,
    ok_proxy_response__maker,
) -> None:
    groups_response = not_ok_proxy_response__maker(status_code=500, data={"error": "internal"})
    splittings_response = ok_proxy_response__maker({"splitters": [], "total": 0})

    result = GroupsConsolidator.consolidate_groups(
        groups_response=groups_response,
        splittings_response=splittings_response,
    )

    assert result is groups_response


def test_consolidate_groups__splittings_not_ok__returns_splittings_response(
    ok_proxy_response__maker,
    not_ok_proxy_response__maker,
) -> None:
    groups_response = ok_proxy_response__maker({"meta": {"total": 1}, "result": [GROUP_1]})
    splittings_response = not_ok_proxy_response__maker(status_code=503, data={"error": "unavailable"})

    result = GroupsConsolidator.consolidate_groups(
        groups_response=groups_response,
        splittings_response=splittings_response,
    )

    assert result is splittings_response
