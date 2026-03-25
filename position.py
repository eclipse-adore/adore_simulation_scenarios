from pyproj import Transformer
import math
from typing import Any, Dict, List, Optional, Tuple, Union
import utm

class Position:
    def __init__(self, lat_long=None, utm=None, psi=0.0):
        self.psi = psi
        if lat_long is not None and utm is not None:
            raise ValueError("Cannot specify both lat_long and utm coordinates")
        elif lat_long is not None:
            self.lat, self.long = lat_long
            self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere = self._lat_long_to_utm(self.lat, self.long)
        elif utm is not None:
            if len(utm) == 4:
                self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere = utm
            else:
                raise ValueError("UTM coordinates must be (x, y, zone, hemisphere)")
            self.lat, self.long = self._utm_to_lat_long(self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere)
        else:
            raise ValueError("Must specify either lat_long or utm coordinates")

    def _lat_long_to_utm(self, lat, long):
        utm_x, utm_y, zone, hemisphere= utm.from_latlon(lat, long)
        return float(utm_x), float(utm_y), zone, hemisphere

    def _utm_to_lat_long(self, utm_x, utm_y, zone, hemisphere):
        lat, long = utm.to_latlon(utm_x, utm_y, zone, hemisphere)
        return float(lat), float(long)

    def get_utm_coordinates(self) -> Tuple[float, float, int, str, float]:
        return self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere,  self.psi 

    def get_lat_long_coordinates(self) -> Tuple[float, float, float]:
        return self.lat, self.long, self.psi


