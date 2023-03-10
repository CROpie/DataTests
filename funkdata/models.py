from django.db import models

# Create your models here.

class Language(models.Model):
    unique_language = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.unique_language}"

class FunctionType(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    unique_function_type = models.CharField(max_length=64)

    class Meta:
        unique_together = ("language", "unique_function_type")

    def __str__(self):
        return f"{self.unique_function_type}"

#Needed to add default=None or else the makemigrations/migrate would come up with errors
class FunctionName(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=None)
    function_type = models.ForeignKey(FunctionType, on_delete=models.CASCADE, default=None)
    unique_function_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        #return f"{self.language} {self.function_type} {self.method_name}"
        return f"{self.unique_function_name}"
    

    
class FunctionAll(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=None)
    function_type = models.ForeignKey(FunctionType, on_delete=models.CASCADE, default=None)
    function_name = models.ForeignKey(FunctionName, on_delete=models.CASCADE, default=None)
    syntax = models.CharField(max_length=64, unique=True)
    parameters = models.CharField(max_length=64)
    return_value =models.CharField(max_length=64)

    def __str__(self):
        return f"{self.syntax},{self.parameters},{self.return_value}"
    

    """
    # Pretty sure this isnt used anymore, delete when confirmed
class FunctionData(models.Model):
    function_name = models.ForeignKey(FunctionName, on_delete=models.CASCADE, default=None)
    syntax = models.CharField(max_length=64)
    parameters = models.CharField(max_length=64)
    return_value =models.CharField(max_length=64)

    def __str__(self):
        return f"{self.syntax}"
        """