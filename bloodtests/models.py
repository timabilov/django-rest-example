from django.db import models


def format_open_ideal_range(lower, upper):
    return f"value {'>' if lower else '<'}= {lower or upper}"


class Test(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    lower = models.FloatField(null=True)
    upper = models.FloatField(null=True)

    @property
    def ideal_range(self):
        if self.lower and self.upper:
            formatted = f'{self.lower} <= value <= {self.upper}'
        else:
            formatted = format_open_ideal_range(self.lower, self.upper)
        return formatted

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save(force_insert, force_update, using, update_fields)

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
