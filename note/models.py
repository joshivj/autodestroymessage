from django.db import models

# Create your models here.

class SecureNotes(models.Model):
    """
    Model to handle table containing notes and hashkey and readtime
        """
    key = models.CharField(max_length=100, null=True,
                                         blank=True,
                                         verbose_name="HashKey")

    notes = models.TextField(verbose_name="Note Detail",null=True,blank=True)

    read_date = models.DateTimeField(auto_now=True,null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    is_active = models.BooleanField(default=True)

    reader_ipaddress = models.TextField(verbose_name="Readers IP address",null=True,blank=True)

    def __unicode__(self):
        return unicode(self.id)