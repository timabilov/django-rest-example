from django.db import models


# for better code readibility and to not confuse with tech tests etc.
# we can change model name to mark it as "Medical test".
class Test(models.Model):
    # Generally to be future-proof it is good idea to use 'unique' instead of primary_key
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    lower = models.FloatField(null=True)
    upper = models.FloatField(null=True)

    @property
    def ideal_range(self):
        """Ideal acceptable range for particular test"""
        low = self.lower
        up = self.upper

        if low and up:
            formatted = f'{low} <= value <= {up}'
        else:
            formatted = f"value {'>' if low else '<'}= {low or up}"
        return formatted

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f'{self.code} {self.name} {self.unit} [{self.lower or "∞"} : {self.upper or "∞"}]'

    class Meta:
        # If we really need, we can avoid two nulls entering the database regardless of serializers, save etc.
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(lower__isnull=False) | models.Q(upper__isnull=False))
                ),
                name='at_least_one_boundary',
            )
        ]
