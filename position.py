# ********************************************************************************
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
# ********************************************************************************

from pyproj import Transformer
import math
from typing import Any, Dict, List, Optional, Tuple, Union
import utm

class Position:
    _DEFAULT_UTM_ZONE = 32
    _DEFAULT_UTM_HEMISPHERE = "U"

    def __init__(self, lat_long=None, utm=None, xy=None, psi=0.0):
        self.psi = psi
        specified = sum(v is not None for v in [lat_long, utm, xy])
        if specified > 1:
            raise ValueError("Cannot specify more than one of lat_long, utm, or xy coordinates")
        elif lat_long is not None:
            self.lat, self.long = lat_long
            self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere = self._lat_long_to_utm(self.lat, self.long)
        elif utm is not None:
            if len(utm) == 4:
                self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere = utm
            else:
                raise ValueError("UTM coordinates must be (x, y, zone, hemisphere)")
            self.lat, self.long = self._utm_to_lat_long(self.utm_x, self.utm_y, self.utm_zone, self.utm_hemisphere)
        elif xy is not None:
            if len(xy) == 2:
                self.utm_x, self.utm_y = float(xy[0]), float(xy[1])
            else:
                raise ValueError("XY coordinates must be (x, y)")
            self.utm_zone = None
            self.utm_hemisphere = None
            self.lat = None
            self.long = None
        else:
            raise ValueError("Must specify one of lat_long, utm, or xy coordinates")

    def _lat_long_to_utm(self, lat, long):
        utm_x, utm_y, zone, hemisphere = utm.from_latlon(lat, long)
        return float(utm_x), float(utm_y), zone, hemisphere

    def _utm_to_lat_long(self, utm_x, utm_y, zone, hemisphere):
        lat, long = utm.to_latlon(utm_x, utm_y, zone, hemisphere)
        return float(lat), float(long)

    def is_raw_xy(self) -> bool:
        return self.utm_zone is None

    def get_utm_coordinates(self) -> Tuple[float, float, int, str, float]:
        zone = self.utm_zone if self.utm_zone is not None else self._DEFAULT_UTM_ZONE
        hemisphere = self.utm_hemisphere if self.utm_hemisphere is not None else self._DEFAULT_UTM_HEMISPHERE
        return self.utm_x, self.utm_y, zone, hemisphere, self.psi

    def get_lat_long_coordinates(self) -> Tuple[float, float, float]:
        if self.is_raw_xy():
            raise ValueError("Cannot convert raw XY position to lat/long without UTM zone")
        return self.lat, self.long, self.psi
