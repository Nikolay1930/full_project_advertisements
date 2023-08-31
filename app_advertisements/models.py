from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


User = get_user_model()


class Advertisement(models.Model):
    title = models.CharField(max_length=128, verbose_name='заголовок')
    description = models.TextField('Описание')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    auction = models.BooleanField('торг', help_text='Отметьте, если уместен торг')
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    image = models.ImageField('изображение', upload_to='advertisements/')

    def __str__(self):
        return f'Advertisement(id={self.id}, title={self.title}, price={self.price})'

    @admin.display(description='Дата создания')
    def created_date(self):
        from django.utils import timezone
        if self.create_at.date() == timezone.now().date():
            created_time = self.create_at.time().strftime('%H:%M:%S')
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created_time
            )
        return self.create_at.strftime('%d.%m.%y')

    @admin.display(description='фото')
    def get_html_image(self):
        if self.image:
            return format_html(
                '<img src="{url}" style="max-width: 80px; max-height: 80px;">', url=self.image.url
            )

    class Meta:
        db_table = 'advertisement'

    def get_absolute_url(self):
        return reverse('adv-detail', kwargs={'pk': self.pk})
