import photonforge as pf
import numpy

import typing


def _cpw_info(port_spec):
    path_profiles = port_spec.path_profiles
    if isinstance(path_profiles, dict):
        path_profiles = list(path_profiles.values())

    ground_profile = None
    central_profile = None
    for profile in path_profiles:
        if profile[1] == 0:
            central_profile = profile
        elif profile[1] > 0:
            ground_profile = profile

    if (
        central_profile is None
        or ground_profile is None
        or central_profile[2] != ground_profile[2]
        or not port_spec.symmetric()
        or len(path_profiles) != 3
    ):
        raise RuntimeError(
            "Port specification does not correspond to an expected CPW transmission line."
        )

    central_width = central_profile[0]
    ground_width, ground_offset, layer = ground_profile
    gap = ground_offset - 0.5 * (ground_width + central_width)

    return central_width, gap, ground_width, ground_offset, layer


_sides = ["N", "NORTH", "W", "WEST", "E", "EAST", "S", "SOUTH"]


def place_edge_couplers(
    chip_frame: pf.Component,
    coupler: pf.Component = None,
    slab_removal_width: float = 20.0,
    straight_length: float = 10.0,
    side_spec: typing.Literal[_sides] = "N",
    offset: float = 60.0,
    number: int = 1,
    pitch: float = 127.0,
):
    """Place an array of edge couplers on a chip frame

    Args:
        chip_frame: Chip frame component.
        coupler: Edge coupler component. If not set, the default
          ``double_linear_inverse_taper`` is used.
        slab_removal_width: Width of the region where the slab is removed
          close to the coupler (for fabrication in positive tone).
        straight_length: Uniform waveguide segment extending beyond the chip
          frame, relaxing the chip singulation tolerances.
        side_spec: Specification of the chip edge for coupler placement.
        offset: Distance between the chip edge and the first edge coupler.
        number: Number of edge couplers to place.
        pitch: Distance between adjacent edge couplers.

    Returns:
        List of references.
    """
    if slab_removal_width < 0:
        raise ValueError("'slab_removal_width' cannot be negative.")

    if straight_length < 0:
        raise ValueError("'straight_length' cannot be negative.")

    if side_spec.upper() not in _sides:
        raise ValueError("'side_spec' must be one of " + ", ".join(f"'{s}'" for s in _sides))
    side_spec = side_spec[0].upper()

    if coupler is None:
        from .component import double_linear_inverse_taper

        coupler = double_linear_inverse_taper()

    ports = sorted(coupler.ports.items())
    port = ports[0][1]

    frame = pf.envelope(chip_frame.get_structures((6, 1), 0), use_box=True)
    inner = pf.envelope(chip_frame.get_structures((6, 0), 0), use_box=True)

    if side_spec in "NS":
        if frame.x_min + offset <= inner.x_min:
            raise ValueError(
                "'First coupler outside safe zone: please increase 'offset' above "
                f"{inner.x_min - frame.x_min}."
            )
        if frame.x_min + offset + (number - 1) * pitch >= inner.x_max:
            raise ValueError(
                "'Last coupler outside safe zone: please decrease 'offset', 'number', or 'pitch'."
            )

    if side_spec in "EW":
        if frame.y_max - offset >= inner.y_max:
            raise ValueError(
                "'First coupler outside safe zone: please increase 'offset' above "
                f"{frame.y_max - inner.y_max}."
            )
        if frame.y_max - offset - (number - 1) * pitch <= inner.y_min:
            raise ValueError(
                "'Last coupler outside safe zone: please decrease 'offset', 'number', or 'pitch'."
            )

    if side_spec == "N":
        origin = numpy.array((frame.x_min + offset, frame.y_max - 0.5 * straight_length))
        spacing = numpy.array((pitch, 0))
        rotation = -90
    elif side_spec == "S":
        origin = numpy.array((frame.x_min + offset, frame.y_min + 0.5 * straight_length))
        spacing = numpy.array((pitch, 0))
        rotation = 90
    elif side_spec == "W":
        origin = numpy.array((frame.x_min + 0.5 * straight_length, frame.y_max - offset))
        spacing = numpy.array((0, -pitch))
        rotation = 0
    elif side_spec == "E":
        origin = numpy.array((frame.x_max - 0.5 * straight_length, frame.y_max - offset))
        spacing = numpy.array((0, -pitch))
        rotation = 180

    full_coupler = pf.Component(f"COUPLER_{side_spec}", technology=coupler.technology)

    ref = pf.Reference(coupler, -port.center)
    full_coupler.add(ref)
    full_coupler.add_port(ref[ports[0][0]], ports[0][0])
    full_coupler.add_port(ref[ports[1][0]], ports[1][0])
    for name, model in coupler.models.items():
        if isinstance(model, pf.Tidy3DModel):
            full_coupler.add_model(model, name)

    if straight_length > 0:
        extension = pf.parametric.straight(
            port_spec=port.spec,
            length=straight_length,
            technology=coupler.technology,
        )
        ref = full_coupler.add_reference(extension).connect("P1", ref[ports[0][0]])
        # Substitute port
        full_coupler.add_port(ref["P0"], ports[0][0])

    if slab_removal_width > 0:
        coupler_length = abs(ports[0][1].center[0] - ports[1][1].center[0])
        full_coupler.add(
            (3, 1),
            pf.Rectangle(
                (-straight_length, -0.5 * slab_removal_width),
                (coupler_length, 0.5 * slab_removal_width),
            ),
        )

    return [
        pf.Reference(full_coupler, origin + n * spacing, rotation=rotation) for n in range(number)
    ]
