from core.models import Route, RouteDetail


class RouteService:

    def get_routes(self, city_code):
        routes = RouteDetail.objects.filter(city__code=city_code)
        return routes