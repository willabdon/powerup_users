from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    external_id = models.CharField(max_length=36, null=False, blank=False, unique=True)
    created_date = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    username = None

    def verify_external_id_exists(external_id):
        return User.objects.filter(external_id=external_id).exists()

    def _generate_external_id(self):
        from users.utils import generate_external_id

        if self.external_id == "":
            external_id = generate_external_id()
            while User.verify_external_id_exists(external_id) is True:
                external_id = generate_external_id()
            self.external_id = external_id

    def save(self, **kargs) -> None:
        self._generate_external_id()
        self.updated_at = timezone.now()
        return super().save(**kargs)
