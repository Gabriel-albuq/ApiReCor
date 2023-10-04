from django.db import models

class ApplyModel(models.Model):
    imagem_input = models.ImageField(upload_to='input')
    datahora = models.IntegerField(null=True, blank=True, editable=False)
    detect_class = models.CharField(max_length=50, null=True, blank=True, editable=False)
    conf_class = models.CharField(max_length=10, null=True, blank=True, editable=False)
    principal_cor = models.CharField(max_length=50, null=True, blank=True, editable=False)
    principal_cor_conf = models.DecimalField(null=True, blank=True, editable=False, decimal_places=2, max_digits=6)
    conf_claro = models.DecimalField(null=True, blank=True, editable=False, decimal_places=2, max_digits=6)
    conf_escuro = models.DecimalField(null=True, blank=True, editable=False, decimal_places=2, max_digits=6)
    conf_padrao = models.DecimalField(null=True, blank=True, editable=False, decimal_places=2, max_digits=6)
    imagem_output = models.ImageField(null=True, blank=True, editable=False, upload_to='output')

    def __str__(self):
        return f'DataHora: {self.datahora}, Classe: {self.detect_class}, Conf_Classe: {self.conf_class}, Classificacao: {self.principal_cor}, Conf_Classificacao: {self.principal_cor_conf}'
