from django.db import models
from projects.models import Project

# Create your models here.
class DiagramText(models.Model):
    name = models.TextField(null=True, blank=True)
    json_user_stories = models.JSONField(null=True,blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    id_project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE, db_column='id_project')
    
    class Meta:
        db_table = "diagram_text"
