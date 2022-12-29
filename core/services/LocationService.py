from core.models import Location


class LocationService:

    def get_locations(self, city_code, location_type=Location.TYPE.STOP):
        locations = Location.objects.filter(city__code=city_code, type=location_type)
        return locations

    def gcd(self, lat1, long1, lat2, long2):
        return 0

    def get_nearest_location(self, city_code, lat, long):
        locations = Location.objects.filter(city__code=city_code)
        # gcd formula to find nearest location
        nearest_location = None
        for location in locations:
            gcd = self.gcd(lat, long, location.lat, location.long)
            if gcd < nearest_location:
                nearest_location = location
        return nearest_location