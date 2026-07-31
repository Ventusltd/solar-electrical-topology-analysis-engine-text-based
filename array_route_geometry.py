"""Geometry algorithms used by the Build 025 routing authority."""

from __future__ import annotations

from dataclasses import asdict
import math
from typing import Iterable, Mapping, Sequence

from geometry_authority import ModulePlacement, Point2D, TableGeometryReceipt
from array_topology import StringTopology, WiringStrategy
from array_route_types import (
    EPSILON,
    ConductorRoute,
    ConductorScope,
    InstallationMethod,
    LocalPoint2D,
    ModuleTerminalLayout,
    RouteClass,
    RoutePolarity,
    RouteSegment,
    RoutingConfig,
    canonical_float,
    hash_payload,
    method_flags,
    same_point,
)


def local_to_world(
    local: LocalPoint2D,
    geometry: TableGeometryReceipt,
) -> Point2D:
    theta = math.radians(geometry.rotation_deg)
    cosine = math.cos(theta)
    sine = math.sin(theta)
    return Point2D(
        canonical_float(
            geometry.origin.x_m + local.u_m * cosine - local.v_m * sine
        ),
        canonical_float(
            geometry.origin.y_m + local.u_m * sine + local.v_m * cosine
        ),
    )


def world_to_local(
    point: Point2D,
    geometry: TableGeometryReceipt,
) -> LocalPoint2D:
    theta = math.radians(geometry.rotation_deg)
    cosine = math.cos(theta)
    sine = math.sin(theta)
    dx = point.x_m - geometry.origin.x_m
    dy = point.y_m - geometry.origin.y_m
    return LocalPoint2D(
        canonical_float(dx * cosine + dy * sine),
        canonical_float(-dx * sine + dy * cosine),
    )


def _module_offset_point(
    placement: ModulePlacement,
    offset_u_m: float,
    offset_v_m: float,
) -> Point2D:
    theta = math.radians(placement.rotation_deg)
    cosine = math.cos(theta)
    sine = math.sin(theta)
    return Point2D(
        canonical_float(
            placement.centre.x_m + offset_u_m * cosine - offset_v_m * sine
        ),
        canonical_float(
            placement.centre.y_m + offset_u_m * sine + offset_v_m * cosine
        ),
    )


def terminal_points(
    geometry: TableGeometryReceipt,
    layout: ModuleTerminalLayout,
) -> dict[str, tuple[Point2D, Point2D]]:
    result: dict[str, tuple[Point2D, Point2D]] = {}
    for placement in geometry.placements:
        half_width = placement.width_m / 2.0
        half_height = placement.height_m / 2.0
        offsets = (
            (
                "negative",
                layout.negative_offset_u_m,
                layout.negative_offset_v_m,
            ),
            (
                "positive",
                layout.positive_offset_u_m,
                layout.positive_offset_v_m,
            ),
        )
        for label, offset_u, offset_v in offsets:
            if (
                abs(offset_u) > half_width + EPSILON
                or abs(offset_v) > half_height + EPSILON
            ):
                raise ValueError(
                    f"{label} terminal offset lies outside module "
                    f"{placement.module_id!r}"
                )
        result[placement.module_id] = (
            _module_offset_point(
                placement,
                layout.negative_offset_u_m,
                layout.negative_offset_v_m,
            ),
            _module_offset_point(
                placement,
                layout.positive_offset_u_m,
                layout.positive_offset_v_m,
            ),
        )
    return result


def deduplicate_vertices(
    vertices: Iterable[Point2D],
) -> tuple[Point2D, ...]:
    result: list[Point2D] = []
    for point in vertices:
        if not result or not same_point(result[-1], point):
            result.append(point)
    if len(result) < 2:
        raise ValueError(
            "a conductor route requires at least two distinct vertices"
        )
    return tuple(result)


def _route_class(
    index: int,
    count: int,
    home_run: bool,
    from_input: bool,
) -> RouteClass:
    if not home_run:
        return RouteClass.MODULE_INTERCONNECT
    if from_input:
        if index == 0:
            return RouteClass.INPUT_TAIL
        if index == count - 1:
            return RouteClass.STRING_EXIT
        if index == 1:
            return RouteClass.INVERTER_ENTRY
        return RouteClass.COLLECTION_RUN
    if index == 0:
        return RouteClass.STRING_EXIT
    if index == count - 1:
        return RouteClass.INPUT_TAIL
    if index == count - 2:
        return RouteClass.INVERTER_ENTRY
    return RouteClass.COLLECTION_RUN


def build_route(
    *,
    route_id: str,
    string_id: str,
    polarity: RoutePolarity,
    conductor_scope: ConductorScope,
    from_node_id: str,
    to_node_id: str,
    vertices: Sequence[Point2D],
    installation_method: InstallationMethod,
    support_path_id: str,
    home_run: bool,
) -> ConductorRoute:
    clean = deduplicate_vertices(vertices)
    buried, screened, armoured, metallic, bonded_screen = method_flags(
        installation_method
    )
    segment_count = len(clean) - 1
    segments: list[RouteSegment] = []
    for index, (start, end) in enumerate(zip(clean, clean[1:])):
        length = canonical_float(
            math.dist((start.x_m, start.y_m), (end.x_m, end.y_m))
        )
        segments.append(
            RouteSegment(
                segment_id=f"{route_id}:SEG-{index + 1:03d}",
                string_id=string_id,
                polarity=polarity,
                start=start,
                end=end,
                route_class=_route_class(
                    index,
                    segment_count,
                    home_run,
                    polarity is RoutePolarity.POSITIVE,
                ),
                installation_method=installation_method,
                buried=buried,
                screened=screened,
                armoured=armoured,
                earthed_metallic_containment=metallic,
                bonded_screen=bonded_screen,
                support_path_id=support_path_id,
                geometric_length_m=length,
                from_node_id=(
                    from_node_id
                    if index == 0
                    else f"{route_id}:WP-{index:03d}"
                ),
                to_node_id=(
                    to_node_id
                    if index == segment_count - 1
                    else f"{route_id}:WP-{index + 1:03d}"
                ),
                conductor_scope=conductor_scope,
            )
        )
    total = canonical_float(
        math.fsum(item.geometric_length_m for item in segments)
    )
    basis = {
        "route_id": route_id,
        "string_id": string_id,
        "polarity": str(polarity),
        "conductor_scope": str(conductor_scope),
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "vertices": [asdict(point) for point in clean],
        "segments": [asdict(item) for item in segments],
    }
    return ConductorRoute(
        route_id=route_id,
        string_id=string_id,
        polarity=polarity,
        conductor_scope=conductor_scope,
        from_node_id=from_node_id,
        to_node_id=to_node_id,
        vertices=clean,
        segments=tuple(segments),
        geometric_length_m=total,
        route_hash=hash_payload(basis),
    )


def _interconnect_vertices(
    start: Point2D,
    end: Point2D,
    geometry: TableGeometryReceipt,
    lane_offset_m: float,
    lane_sign: int,
) -> tuple[Point2D, ...]:
    start_local = world_to_local(start, geometry)
    end_local = world_to_local(end, geometry)
    if lane_sign == 0 or lane_offset_m == 0:
        return deduplicate_vertices((start, end))
    lane_v = canonical_float(
        (start_local.v_m + end_local.v_m) / 2.0
        + lane_sign * lane_offset_m
    )
    return deduplicate_vertices(
        (
            start,
            local_to_world(
                LocalPoint2D(start_local.u_m, lane_v),
                geometry,
            ),
            local_to_world(
                LocalPoint2D(end_local.u_m, lane_v),
                geometry,
            ),
            end,
        )
    )


def build_interconnect_routes(
    topology: StringTopology,
    geometry: TableGeometryReceipt,
    terminals: Mapping[str, tuple[Point2D, Point2D]],
    config: RoutingConfig,
) -> tuple[ConductorRoute, ...]:
    physical_index = {
        module_id: index
        for index, module_id in enumerate(topology.physical_module_ids)
    }
    routes: list[ConductorRoute] = []
    pairs = zip(
        topology.electrical_module_ids,
        topology.electrical_module_ids[1:],
    )
    for ordinal, (left_module, right_module) in enumerate(
        pairs,
        start=1,
    ):
        delta = physical_index[right_module] - physical_index[left_module]
        lane_sign = 0
        if topology.strategy is WiringStrategy.LEAPFROG:
            lane_sign = 1 if delta >= 0 else -1
        route_id = f"{topology.string_id}:INTERCONNECT-{ordinal:03d}"
        routes.append(
            build_route(
                route_id=route_id,
                string_id=topology.string_id,
                polarity=RoutePolarity.SERIES,
                conductor_scope=ConductorScope.FACTORY_FITTED,
                from_node_id=f"{left_module}:P",
                to_node_id=f"{right_module}:N",
                vertices=_interconnect_vertices(
                    terminals[left_module][1],
                    terminals[right_module][0],
                    geometry,
                    config.interconnect_lane_offset_m,
                    lane_sign,
                ),
                installation_method=(
                    config.interconnect_installation_method
                ),
                support_path_id=(
                    f"{topology.string_id}:MODULE-BACKPLANE"
                ),
                home_run=False,
            )
        )
    return tuple(routes)


def module_row_v(
    module_ids: Sequence[str],
    placement_by_id: Mapping[str, ModulePlacement],
    geometry: TableGeometryReceipt,
) -> float:
    values = [
        world_to_local(
            placement_by_id[module_id].centre,
            geometry,
        ).v_m
        for module_id in module_ids
    ]
    return canonical_float(math.fsum(values) / len(values))


def entry_u(
    collection_u: float,
    inverter_u: float,
    offset: float,
) -> float:
    difference = inverter_u - collection_u
    if abs(difference) <= 2 * offset or offset == 0:
        return canonical_float(collection_u + difference / 2.0)
    return canonical_float(
        inverter_u - math.copysign(offset, difference)
    )


def home_route_vertices(
    *,
    free_point: Point2D,
    input_point: Point2D,
    exit_lane_v: float,
    trunk_lane_v: float,
    collection_u: float,
    entry_u_m: float,
    geometry: TableGeometryReceipt,
    from_input: bool,
) -> tuple[Point2D, ...]:
    free_local = world_to_local(free_point, geometry)
    input_local = world_to_local(input_point, geometry)
    free_to_input = (
        free_point,
        local_to_world(
            LocalPoint2D(free_local.u_m, exit_lane_v),
            geometry,
        ),
        local_to_world(
            LocalPoint2D(collection_u, exit_lane_v),
            geometry,
        ),
        local_to_world(
            LocalPoint2D(collection_u, trunk_lane_v),
            geometry,
        ),
        local_to_world(
            LocalPoint2D(entry_u_m, trunk_lane_v),
            geometry,
        ),
        local_to_world(
            LocalPoint2D(entry_u_m, input_local.v_m),
            geometry,
        ),
        input_point,
    )
    return deduplicate_vertices(
        tuple(reversed(free_to_input))
        if from_input
        else free_to_input
    )


def _point_to_segment_distance(
    point: Point2D,
    start: Point2D,
    end: Point2D,
) -> float:
    dx = end.x_m - start.x_m
    dy = end.y_m - start.y_m
    length_squared = dx * dx + dy * dy
    if length_squared <= EPSILON:
        return math.dist(
            (point.x_m, point.y_m),
            (start.x_m, start.y_m),
        )
    fraction = (
        (point.x_m - start.x_m) * dx
        + (point.y_m - start.y_m) * dy
    ) / length_squared
    fraction = min(1.0, max(0.0, fraction))
    projection = Point2D(
        start.x_m + fraction * dx,
        start.y_m + fraction * dy,
    )
    return math.dist(
        (point.x_m, point.y_m),
        (projection.x_m, projection.y_m),
    )


def _point_to_route_distance(
    point: Point2D,
    route: ConductorRoute,
) -> float:
    return min(
        _point_to_segment_distance(
            point,
            item.start,
            item.end,
        )
        for item in route.segments
    )


def pole_separation_metrics(
    positive: ConductorRoute,
    negative: ConductorRoute,
) -> tuple[float, float, float]:
    endpoint_distances = [
        _point_to_route_distance(point, negative)
        for point in positive.vertices
    ] + [
        _point_to_route_distance(point, positive)
        for point in negative.vertices
    ]
    weighted_sum = 0.0
    weight = 0.0
    for source, target in (
        (positive, negative),
        (negative, positive),
    ):
        for segment in source.segments:
            midpoint = Point2D(
                canonical_float(
                    (segment.start.x_m + segment.end.x_m) / 2.0
                ),
                canonical_float(
                    (segment.start.y_m + segment.end.y_m) / 2.0
                ),
            )
            weighted_sum += (
                segment.geometric_length_m
                * _point_to_route_distance(midpoint, target)
            )
            weight += segment.geometric_length_m
    maximum = max(endpoint_distances) if endpoint_distances else 0.0
    mean = weighted_sum / weight if weight else 0.0
    return (
        canonical_float(maximum),
        canonical_float(mean),
        canonical_float(weight),
    )


def _parallel_overlap(
    first: RouteSegment,
    second: RouteSegment,
    maximum_separation: float,
) -> float:
    first_dx = first.end.x_m - first.start.x_m
    first_dy = first.end.y_m - first.start.y_m
    second_dx = second.end.x_m - second.start.x_m
    second_dy = second.end.y_m - second.start.y_m
    first_length = math.hypot(first_dx, first_dy)
    second_length = math.hypot(second_dx, second_dy)
    if first_length <= EPSILON or second_length <= EPSILON:
        return 0.0
    cross = abs(first_dx * second_dy - first_dy * second_dx)
    if cross > 1e-8 * first_length * second_length:
        return 0.0
    unit_x = first_dx / first_length
    unit_y = first_dy / first_length
    separation = abs(
        (second.start.x_m - first.start.x_m) * unit_y
        - (second.start.y_m - first.start.y_m) * unit_x
    )
    if separation > maximum_separation + EPSILON:
        return 0.0
    second_a = (
        (second.start.x_m - first.start.x_m) * unit_x
        + (second.start.y_m - first.start.y_m) * unit_y
    )
    second_b = (
        (second.end.x_m - first.start.x_m) * unit_x
        + (second.end.y_m - first.start.y_m) * unit_y
    )
    lower, upper = sorted((second_a, second_b))
    return max(
        0.0,
        min(first_length, upper) - max(0.0, lower),
    )


def parallel_run_distance(
    positive: ConductorRoute,
    negative: ConductorRoute,
    maximum_separation: float,
) -> float:
    total = 0.0
    for positive_segment in positive.segments:
        total += max(
            (
                _parallel_overlap(
                    positive_segment,
                    negative_segment,
                    maximum_separation,
                )
                for negative_segment in negative.segments
            ),
            default=0.0,
        )
    return canonical_float(total)


def _orientation(
    a: Point2D,
    b: Point2D,
    c: Point2D,
) -> float:
    return (b.x_m - a.x_m) * (c.y_m - a.y_m) - (
        b.y_m - a.y_m
    ) * (c.x_m - a.x_m)


def _proper_intersection(
    a: Point2D,
    b: Point2D,
    c: Point2D,
    d: Point2D,
) -> bool:
    if any(
        same_point(first, second)
        for first in (a, b)
        for second in (c, d)
    ):
        return False
    first = _orientation(a, b, c)
    second = _orientation(a, b, d)
    third = _orientation(c, d, a)
    fourth = _orientation(c, d, b)
    return (
        first * second < -EPSILON
        and third * fourth < -EPSILON
    )


def _intersection_point(
    a: Point2D,
    b: Point2D,
    c: Point2D,
    d: Point2D,
) -> Point2D | None:
    x1, y1, x2, y2 = a.x_m, a.y_m, b.x_m, b.y_m
    x3, y3, x4, y4 = c.x_m, c.y_m, d.x_m, d.y_m
    denominator = (
        (x1 - x2) * (y3 - y4)
        - (y1 - y2) * (x3 - x4)
    )
    if abs(denominator) <= EPSILON:
        return None
    determinant_first = x1 * y2 - y1 * x2
    determinant_second = x3 * y4 - y3 * x4
    px = (
        determinant_first * (x3 - x4)
        - (x1 - x2) * determinant_second
    ) / denominator
    py = (
        determinant_first * (y3 - y4)
        - (y1 - y2) * determinant_second
    ) / denominator
    on_both = (
        min(x1, x2) - EPSILON <= px <= max(x1, x2) + EPSILON
        and min(y1, y2) - EPSILON <= py <= max(y1, y2) + EPSILON
        and min(x3, x4) - EPSILON <= px <= max(x3, x4) + EPSILON
        and min(y3, y4) - EPSILON <= py <= max(y3, y4) + EPSILON
    )
    return (
        Point2D(canonical_float(px), canonical_float(py))
        if on_both
        else None
    )


def count_route_crossings(
    routes: Sequence[ConductorRoute],
) -> int:
    tagged = [
        (route.route_id, segment)
        for route in routes
        for segment in route.segments
    ]
    count = 0
    for index, (first_route_id, first) in enumerate(tagged):
        for second_route_id, second in tagged[index + 1 :]:
            if (
                first_route_id != second_route_id
                and _proper_intersection(
                    first.start,
                    first.end,
                    second.start,
                    second.end,
                )
            ):
                count += 1
    return count


def signed_polygon_area(
    vertices: Sequence[Point2D],
) -> float:
    if len(vertices) < 4 or not same_point(
        vertices[0],
        vertices[-1],
    ):
        raise ValueError(
            "loop area requires an explicitly closed polyline"
        )
    return 0.5 * math.fsum(
        first.x_m * second.y_m - second.x_m * first.y_m
        for first, second in zip(vertices, vertices[1:])
    )


def _winding_number(
    point: Point2D,
    vertices: Sequence[Point2D],
) -> int:
    winding = 0
    for first, second in zip(vertices, vertices[1:]):
        if first.y_m <= point.y_m:
            if (
                second.y_m > point.y_m
                and _orientation(first, second, point) > 0
            ):
                winding += 1
        elif (
            second.y_m <= point.y_m
            and _orientation(first, second, point) < 0
        ):
            winding -= 1
    return winding


def absolute_winding_area(
    vertices: Sequence[Point2D],
) -> float:
    """Integrate absolute winding number, preserving self-crossing loop lobes."""

    if len(vertices) < 4 or not same_point(
        vertices[0],
        vertices[-1],
    ):
        raise ValueError(
            "absolute loop area requires an explicitly closed polyline"
        )
    edges = tuple(zip(vertices, vertices[1:]))
    x_events = {point.x_m for point in vertices}
    for index, (a, b) in enumerate(edges):
        for second_index, (c, d) in enumerate(
            edges[index + 1 :],
            start=index + 1,
        ):
            if second_index in {index, index + 1}:
                continue
            if index == 0 and second_index == len(edges) - 1:
                continue
            intersection = _intersection_point(a, b, c, d)
            if intersection is not None:
                x_events.add(intersection.x_m)
    area = 0.0
    ordered_x = sorted(x_events)
    for left, right in zip(ordered_x, ordered_x[1:]):
        width = right - left
        if width <= EPSILON:
            continue
        x_mid = (left + right) / 2.0
        y_intersections: list[float] = []
        for first, second in edges:
            dx = second.x_m - first.x_m
            if abs(dx) <= EPSILON:
                continue
            if (
                min(first.x_m, second.x_m)
                < x_mid
                < max(first.x_m, second.x_m)
            ):
                fraction = (x_mid - first.x_m) / dx
                y_intersections.append(
                    first.y_m
                    + fraction * (second.y_m - first.y_m)
                )
        ordered_y: list[float] = []
        for value in sorted(y_intersections):
            if not ordered_y or not math.isclose(
                value,
                ordered_y[-1],
                abs_tol=1e-9,
            ):
                ordered_y.append(value)
        for lower, upper in zip(ordered_y, ordered_y[1:]):
            if upper - lower <= EPSILON:
                continue
            probe = Point2D(
                x_mid,
                (lower + upper) / 2.0,
            )
            winding = _winding_number(probe, vertices)
            if winding:
                area += (
                    width * (upper - lower) * abs(winding)
                )
    return area


def circuit_loop_vertices(
    topology: StringTopology,
    positive_route: ConductorRoute,
    negative_route: ConductorRoute,
    interconnect_routes: Sequence[ConductorRoute],
    terminals: Mapping[str, tuple[Point2D, Point2D]],
) -> tuple[Point2D, ...]:
    loop = list(positive_route.vertices)
    route_by_pair = {
        pair: route
        for pair, route in zip(
            zip(
                topology.electrical_module_ids,
                topology.electrical_module_ids[1:],
            ),
            interconnect_routes,
        )
    }
    electrical = topology.electrical_module_ids
    last_negative, last_positive = terminals[electrical[-1]]
    if not same_point(loop[-1], last_positive):
        raise ValueError(
            "positive home route does not terminate at "
            "the positive free end"
        )
    loop.append(last_negative)
    for index in range(len(electrical) - 2, -1, -1):
        current = electrical[index]
        following = electrical[index + 1]
        route = route_by_pair[(current, following)]
        for point in reversed(route.vertices):
            if not same_point(loop[-1], point):
                loop.append(point)
        current_negative, current_positive = terminals[current]
        if not same_point(loop[-1], current_positive):
            raise ValueError(
                "interconnect geometry does not match "
                "topology terminal coordinates"
            )
        loop.append(current_negative)
    if not same_point(loop[-1], negative_route.vertices[0]):
        raise ValueError(
            "negative home route does not start at "
            "the negative free end"
        )
    for point in negative_route.vertices[1:]:
        if not same_point(loop[-1], point):
            loop.append(point)
    if not same_point(loop[-1], loop[0]):
        loop.append(loop[0])
    return tuple(loop)


def bend_count(route: ConductorRoute) -> int:
    count = 0
    for first, second in zip(
        route.segments,
        route.segments[1:],
    ):
        first_dx = first.end.x_m - first.start.x_m
        first_dy = first.end.y_m - first.start.y_m
        second_dx = second.end.x_m - second.start.x_m
        second_dy = second.end.y_m - second.start.y_m
        if abs(
            first_dx * second_dy - first_dy * second_dx
        ) > 1e-9:
            count += 1
    return count
