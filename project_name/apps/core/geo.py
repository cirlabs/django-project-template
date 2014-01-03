from django.contrib.gis import geos


def get_simple_polygon(input_geom, tolerance=2, srid=4326):
    """
    Modified Ben Welsh method

    Simplifies the source polygons so they don't use so many points.

    Provide a tolerance score the indicates how sharply the
    the lines should be redrawn.

    Returns resulting simplified MultiPolygon if successful.
    """
    try:
        # Simplify the input geometry (using the start SRID)
        simple = input_geom.simplify(tolerance, True)

        if simple.srid is not srid:
            simple = simple.transform(srid, True)

        # If it's not a MultiPolygon, convert it to a MultiPolygon
        if not isinstance(simple, geos.MultiPolygon):
            simple = geos.MultiPolygon(simple)

    except:
        simple = None

    return simple
