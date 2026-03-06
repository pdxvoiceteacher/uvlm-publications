#!/usr/bin/env python3
"""Validate atlas timeline structure and consistency."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

EVENT_TYPE_ORDER = {"node-appear": 0, "edge-appear": 1}


class TimelineValidationError(Exception):
    """Raised for malformed timeline inputs that cannot be validated further."""


def parse_iso_date(value: Any, field_name: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string in YYYY-MM-DD format")
    if "T" in value:
        raise ValueError(f"{field_name} must be date-only (YYYY-MM-DD), not datetime")
    try:
        return dt.date.fromisoformat(value)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"{field_name} is not a valid ISO date (YYYY-MM-DD): {value}") from exc


def load_timeline(path: Path) -> tuple[dict[str, Any], list[str]]:
    duplicate_key_errors: list[str] = []

    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                duplicate_key_errors.append(f"Duplicate key found in JSON object: {key}")
            result[key] = value
        return result

    try:
        timeline = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)
    except json.JSONDecodeError as exc:
        raise TimelineValidationError(f"Malformed JSON: {exc}") from exc

    if not isinstance(timeline, dict):
        raise TimelineValidationError("Top-level timeline payload must be a JSON object")

    return timeline, duplicate_key_errors


def parse_edge_id(edge_id: str) -> tuple[str, str, str]:
    if not isinstance(edge_id, str) or not edge_id:
        raise ValueError("Edge ID must be a non-empty string")
    if "->" not in edge_id:
        raise ValueError(f"Edge ID missing '->': {edge_id}")

    source, remainder = edge_id.split("->", 1)
    if ":" not in remainder:
        raise ValueError(f"Edge ID missing final ':' type separator: {edge_id}")

    target, edge_type = remainder.rsplit(":", 1)
    if not source:
        raise ValueError(f"Edge ID has empty source: {edge_id}")
    if not target:
        raise ValueError(f"Edge ID has empty target: {edge_id}")
    if not edge_type:
        raise ValueError(f"Edge ID has empty type: {edge_id}")
    return source, target, edge_type


def validate_top_level_shape(timeline: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "timeRange": dict,
        "nodes": dict,
        "edges": dict,
        "events": list,
    }

    for key, expected_type in required.items():
        if key not in timeline:
            errors.append(f"Missing top-level key: {key}")
            continue
        value = timeline[key]
        if value is None:
            errors.append(f"Top-level key cannot be null: {key}")
            continue
        if not isinstance(value, expected_type):
            errors.append(
                f"Top-level key '{key}' must be of type {expected_type.__name__}, got {type(value).__name__}"
            )

    return errors


def validate_time_range(time_range: dict[str, Any]) -> tuple[list[str], dt.date | None, dt.date | None]:
    errors: list[str] = []
    for key in ("start", "end"):
        if key not in time_range:
            errors.append(f"timeRange missing required key: {key}")

    if errors:
        return errors, None, None

    try:
        start = parse_iso_date(time_range["start"], "timeRange.start")
    except ValueError as exc:
        errors.append(str(exc))
        start = None

    try:
        end = parse_iso_date(time_range["end"], "timeRange.end")
    except ValueError as exc:
        errors.append(str(exc))
        end = None

    if start and end and start > end:
        errors.append("timeRange.start must be <= timeRange.end")

    return errors, start, end


def validate_nodes(nodes: dict[str, Any], start: dt.date, end: dt.date) -> tuple[list[str], dict[str, dt.date]]:
    errors: list[str] = []
    parsed_dates: dict[str, dt.date] = {}

    if not nodes:
        errors.append("nodes must not be empty")
        return errors, parsed_dates

    for node_id, meta in nodes.items():
        if not isinstance(node_id, str) or not node_id:
            errors.append("Node ID must be a non-empty string")
            continue
        if not isinstance(meta, dict):
            errors.append(f"Node value must be an object for id: {node_id}")
            continue
        if "appearanceDate" not in meta:
            errors.append(f"Node missing appearanceDate: {node_id}")
            continue

        try:
            appearance_date = parse_iso_date(meta["appearanceDate"], f"nodes[{node_id}].appearanceDate")
            parsed_dates[node_id] = appearance_date
            if appearance_date < start or appearance_date > end:
                errors.append(
                    f"Node appearanceDate out of timeRange for {node_id}: {appearance_date.isoformat()}"
                )
        except ValueError as exc:
            errors.append(str(exc))

    return errors, parsed_dates


def validate_edges(
    edges: dict[str, Any],
    node_dates: dict[str, dt.date],
    start: dt.date,
    end: dt.date,
) -> tuple[list[str], list[str], dict[str, dt.date]]:
    errors: list[str] = []
    warnings: list[str] = []
    edge_dates: dict[str, dt.date] = {}

    if not edges:
        warnings.append("edges map is empty")
        return errors, warnings, edge_dates

    for edge_id, meta in edges.items():
        if not isinstance(edge_id, str) or not edge_id:
            errors.append("Edge ID must be a non-empty string")
            continue
        if not isinstance(meta, dict):
            errors.append(f"Edge value must be an object for id: {edge_id}")
            continue
        if "appearanceDate" not in meta:
            errors.append(f"Edge missing appearanceDate: {edge_id}")
            continue

        try:
            source, target, _etype = parse_edge_id(edge_id)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        try:
            appearance_date = parse_iso_date(meta["appearanceDate"], f"edges[{edge_id}].appearanceDate")
            edge_dates[edge_id] = appearance_date
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if appearance_date < start or appearance_date > end:
            errors.append(
                f"Edge appearanceDate out of timeRange for {edge_id}: {appearance_date.isoformat()}"
            )

        if source not in node_dates:
            errors.append(f"Edge source node does not exist in nodes map: {edge_id} -> {source}")
        if target not in node_dates:
            errors.append(f"Edge target node does not exist in nodes map: {edge_id} -> {target}")

        if source in node_dates and appearance_date < node_dates[source]:
            errors.append(
                f"Edge appears before source node: {edge_id} ({appearance_date.isoformat()} < {node_dates[source].isoformat()})"
            )
        if target in node_dates and appearance_date < node_dates[target]:
            errors.append(
                f"Edge appears before target node: {edge_id} ({appearance_date.isoformat()} < {node_dates[target].isoformat()})"
            )

    return errors, warnings, edge_dates


def validate_events(
    events: list[Any],
    node_dates: dict[str, dt.date],
    edge_dates: dict[str, dt.date],
) -> tuple[list[str], list[dt.date], set[str], list[tuple[dt.date, int, str, int]]]:
    errors: list[str] = []
    all_event_dates: list[dt.date] = []
    seen_triplets: set[tuple[str, str, str]] = set()
    publication_nodes_seen: set[str] = set()
    normalized_order: list[tuple[dt.date, int, str, int]] = []

    if not events:
        errors.append("events must not be empty")
        return errors, all_event_dates, publication_nodes_seen, normalized_order

    for idx, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"Event at index {idx} must be an object")
            continue

        missing_keys = [k for k in ("date", "type", "id") if k not in event]
        if missing_keys:
            errors.append(f"Event at index {idx} missing required key(s): {', '.join(missing_keys)}")
            continue

        event_id = event["id"]
        event_type = event["type"]
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"Event id must be a non-empty string at index {idx}")
            continue
        if not isinstance(event_type, str) or event_type not in EVENT_TYPE_ORDER:
            errors.append(
                f"Event type must be one of {', '.join(EVENT_TYPE_ORDER)} at index {idx}: {event_type}"
            )
            continue

        try:
            event_date = parse_iso_date(event["date"], f"events[{idx}].date")
            all_event_dates.append(event_date)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        triplet = (event["date"], event_type, event_id)
        if triplet in seen_triplets:
            errors.append(
                f"Duplicate event triplet detected at index {idx}: (date={triplet[0]}, type={triplet[1]}, id={triplet[2]})"
            )
        seen_triplets.add(triplet)

        if event_type == "node-appear":
            if event_id not in node_dates:
                errors.append(f"Event references unknown node id at index {idx}: {event_id}")
            else:
                if event_date != node_dates[event_id]:
                    errors.append(
                        "Node event date mismatch at index "
                        f"{idx}: {event_id} event={event_date.isoformat()} expected={node_dates[event_id].isoformat()}"
                    )
                if event_id.startswith("publication:"):
                    publication_nodes_seen.add(event_id)
        elif event_type == "edge-appear":
            if event_id not in edge_dates:
                errors.append(f"Event references unknown edge id at index {idx}: {event_id}")
            else:
                if event_date != edge_dates[event_id]:
                    errors.append(
                        "Edge event date mismatch at index "
                        f"{idx}: {event_id} event={event_date.isoformat()} expected={edge_dates[event_id].isoformat()}"
                    )

        normalized_order.append((event_date, EVENT_TYPE_ORDER[event_type], event_id, idx))

    return errors, all_event_dates, publication_nodes_seen, normalized_order


def validate_event_order(normalized_order: list[tuple[dt.date, int, str, int]]) -> list[str]:
    errors: list[str] = []
    last_key: tuple[dt.date, int, str] | None = None

    for event_date, type_order, event_id, idx in normalized_order:
        key = (event_date, type_order, event_id)
        if last_key and key < last_key:
            errors.append(
                f"Events are not sorted at index {idx}; expected ordering by (date, type, id) with node-appear before edge-appear"
            )
            break
        last_key = key

    return errors


def validate_time_range_coverage(
    start: dt.date,
    end: dt.date,
    node_dates: dict[str, dt.date],
    edge_dates: dict[str, dt.date],
    event_dates: list[dt.date],
) -> list[str]:
    errors: list[str] = []
    all_dates = [*node_dates.values(), *edge_dates.values(), *event_dates]

    if not all_dates:
        errors.append("No timeline dates found to validate timeRange coverage")
        return errors

    expected_start = min(all_dates)
    expected_end = max(all_dates)

    if start != expected_start:
        errors.append(
            f"timeRange.start does not match minimum timeline date ({start.isoformat()} != {expected_start.isoformat()})"
        )
    if end != expected_end:
        errors.append(
            f"timeRange.end does not match maximum timeline date ({end.isoformat()} != {expected_end.isoformat()})"
        )

    return errors


def validate_timeline(path: Path, strict: bool = False) -> tuple[list[str], list[str], dict[str, Any] | None]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        timeline, duplicate_key_errors = load_timeline(path)
    except TimelineValidationError as exc:
        return [str(exc)], warnings, None

    errors.extend(duplicate_key_errors)

    shape_errors = validate_top_level_shape(timeline)
    errors.extend(shape_errors)
    if shape_errors:
        return errors, warnings, timeline

    tr_errors, start, end = validate_time_range(timeline["timeRange"])
    errors.extend(tr_errors)
    if start is None or end is None:
        return errors, warnings, timeline

    node_errors, node_dates = validate_nodes(timeline["nodes"], start, end)
    errors.extend(node_errors)

    edge_errors, edge_warnings, edge_dates = validate_edges(timeline["edges"], node_dates, start, end)
    errors.extend(edge_errors)
    warnings.extend(edge_warnings)

    event_errors, event_dates, publication_nodes, normalized_order = validate_events(
        timeline["events"], node_dates, edge_dates
    )
    errors.extend(event_errors)

    errors.extend(validate_event_order(normalized_order))
    errors.extend(validate_time_range_coverage(start, end, node_dates, edge_dates, event_dates))

    unique_dates = set([*node_dates.values(), *edge_dates.values(), *event_dates])
    if len(unique_dates) <= 1:
        warnings.append("Timeline contains only one unique date")
    if len(publication_nodes) <= 1:
        warnings.append("Timeline includes only one publication node event")

    if strict and warnings:
        errors.extend([f"[strict] {w}" for w in warnings])

    return errors, warnings, timeline


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", nargs="?", type=Path, help="Path to atlas_timeline.json")
    parser.add_argument("--timeline", dest="timeline_opt", type=Path, help="Path to atlas_timeline.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    timeline_path = args.timeline_opt or args.timeline
    if timeline_path is None:
        parser.error("timeline path is required (positional or --timeline)")

    errors, warnings, timeline = validate_timeline(timeline_path, strict=args.strict)

    if errors:
        print(f"{timeline_path.name} is invalid")
        for msg in errors:
            print(f"ERROR: {msg}")
        return 1

    print(f"{timeline_path.name} is valid")
    if timeline is not None:
        print(f"nodes: {len(timeline['nodes'])}")
        print(f"edges: {len(timeline['edges'])}")
        print(f"events: {len(timeline['events'])}")
        print(
            "timeRange: "
            f"{timeline['timeRange']['start']} -> {timeline['timeRange']['end']}"
        )
    for msg in warnings:
        print(f"WARNING: {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
