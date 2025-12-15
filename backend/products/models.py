from django.db import models # type: ignore
from django.utils.text import slugify # type: ignore
from categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(
        "products.Product",
        related_name="variants",
        on_delete=models.CASCADE,
    )
    sku = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.sku})"
    

class VariantAttribute(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class VariantAttributeValue(models.Model):
    attribute = models.ForeignKey(
        VariantAttribute,
        related_name="values",
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=50)

    class Meta:
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class VariantValueAssignment(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        related_name="attribute_values",
        on_delete=models.CASCADE,
    )
    attribute_value = models.ForeignKey(
        VariantAttributeValue,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("variant", "attribute_value")

