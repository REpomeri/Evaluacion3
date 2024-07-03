from django.db import models

class Document(models.Model):
    descripcion = models.CharField(max_length=255, default="Sin descripción")  
    document = models.FileField(upload_to='documents/')
    upload_at = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    
class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    articulos = models.TextField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Compra {self.id}'