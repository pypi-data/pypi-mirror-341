from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks_geo.blocks:ReadGeoPoints', 'Spatialize a data frame'),
        Info('sier2_blocks_geo.blocks:GeoPoints', 'Geoviews Points chart'),
        Info('sier2_blocks_geo.blocks:GeoPointsSelect', 'Geoviews Points chart that passes on selections'),
    ]

def dags() -> list[Info]:
    return [
        Info('sier2_blocks_geo.dags:geo_points', 'Load and plot a dataframe as geo points'),
    ]
