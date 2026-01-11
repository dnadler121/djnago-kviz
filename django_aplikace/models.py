
from django.db import models

class VysledekKvizu(models.Model):
    jmeno = models.CharField(max_length=60)
    skore = models.IntegerField()
    max_skore = models.IntegerField()
    # uložíme detail odpovědí jako text (jednoduché a stačí na učňák)
    detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jmeno}: {self.skore}/{self.max_skore}"

