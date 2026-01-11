from django.http import HttpResponseForbidden

TEACHER_PREFIXES = ("/admin/", "/ucitel/")  # přidej/uber podle sebe

class TeacherLocalOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Pokud někdo leze na učitelskou část…
        if path.startswith(TEACHER_PREFIXES):
            ip = request.META.get("REMOTE_ADDR", "")

            # povolíme jen přístup z toho samého počítače (localhost)
            if ip not in ("127.0.0.1", "::1"):
                return HttpResponseForbidden("Přístup jen z počítače serveru.")

        return self.get_response(request)
