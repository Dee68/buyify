from django.db import models # type: ignore
from django.utils.text import slugify # type: ignore

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_breadcrumbs(self):
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.append({
                "id": current.id,
                "name": current.name,
                "slug": current.slug,
            })
            current = current.parent
        return list(reversed(breadcrumbs))

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        return self.products.count()
