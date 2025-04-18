from io import BytesIO
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)  # ✅ Cloudinary storage
    thumbnail = CloudinaryField('thumbnail', blank=True, null=True)  # ✅ Cloudinary storage
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        """Returns Cloudinary URL of the main image."""
        if self.image:
            return self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.image:
            # Use Cloudinary to generate a thumbnail dynamically
            return cloudinary.utils.cloudinary_url(self.image.public_id, width=300, height=200, crop="fill")[0]
        return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        """Creates a thumbnail, uploads to Cloudinary, and returns the URL."""
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)

        # ✅ Upload thumbnail to Cloudinary
        response = cloudinary.uploader.upload(
            thumb_io.getvalue(),
            folder="thumbnails",
            format="jpg",
            quality="auto:low",
        )

        return response['secure_url']  # ✅ Return Cloudinary URL
