from django.db import models


class Spinset(models.Model):
    SPINSET_RENDERING = 0
    SPINSET_DONE = 1

    status = models.IntegerField("status", default=SPINSET_RENDERING)
    path = models.CharField("path", max_length=200)

    def __str__(self):
        return self.path


class Asset(models.Model):
    title = models.CharField("Title", max_length=100)
    className = models.CharField("className", max_length=100)

    structure = models.TextField("Content")

    allowedOnGround = models.BooleanField("allowedOnGround", default=False)
    allowedInAir = models.BooleanField("allowedInAir", default=False)

    defaultAngle = models.IntegerField("defaultAngle", default=0)

    spinset = models.ForeignKey(Spinset, on_delete=models.SET_NULL, null=True, related_name="spinset")

    def __str__(self):
        return f"{self.pk} {self.className}"


class Relation(models.Model):
    first = models.ForeignKey(Asset, on_delete=models.CASCADE, null=False, related_name="first")
    second = models.ForeignKey(Asset, on_delete=models.CASCADE, null=False, related_name="second")

    angle = models.IntegerField("Аngle")

    direction = models.CharField("Dimension", max_length=100)

    def __str__(self):
        return f"{self.first.className}<{self.first.pk}> - {self.direction}< {self.angle}°> - {self.second.className}<{self.second.pk}>"
