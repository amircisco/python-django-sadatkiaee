from django.db import models
from account.models import User


class DocumentArchive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="document_archives", verbose_name="نام بیمه گذار")
    file = models.FileField(upload_to="document_archive/%Y/%m/%d", verbose_name="فایل")
    doctype = models.ForeignKey("DocType", on_delete=models.DO_NOTHING ,verbose_name="نوع بایگانی")

    def __str__(self):
        return self.user + " " + self.doctype

    class Meta:
        verbose_name = "بایگانی"
        verbose_name_plural = "بایگانی ها"


class DocType(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع بایگانی"
        verbose_name_plural = "انواع بایگانی"