from django.db import models

# Create your models here.

class Language(models.Model):
    unique_language = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.unique_language}"

class FunctionType(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    unique_function_type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.unique_function_type}"

#Needed to add default=None or else the makemigrations/migrate would come up with errors
class FunctionInfo(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=None)
    function_type = models.ForeignKey(FunctionType, on_delete=models.CASCADE, default=None)
    method_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.method_name}"