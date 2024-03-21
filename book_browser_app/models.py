from django.db import models


# Create your models here.


class MyBaseModel(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created date'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated date'
    )

    class Meta:
        abstract = True
        ordering = ('pk',)

    def __str__(self):
        raise NotImplementedError('Implement __str__ method')


class ValidatedUrl(MyBaseModel):
    url = models.URLField()
    url_text = models.TextField(verbose_name="Url text", )

    class Meta:
        ordering = ('pk',)
        verbose_name = "ValidatedUrl"
        verbose_name_plural = "ValidatedUrls"

    def __str__(self):
        return self.url


class Author(MyBaseModel):
    url = models.ForeignKey(ValidatedUrl,
                            related_name='authors',
                            on_delete=models.PROTECT,
                            verbose_name="Url",
                            )
    name = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Name",
                            )

    @property
    def active_posts(self):
        return self.books.filter(is_active=True).values(
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
        )

    @property
    def disabled_posts(self):
        return self.books.filter(is_active=False).values(
            'id',
            'title',
            'description',
            'created_date',
            'updated_date',
        )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class BookRow(MyBaseModel):
    author = models.ForeignKey(Author,
                               related_name='books',
                               on_delete=models.PROTECT,
                               verbose_name="Author",
                               )
    name = models.CharField(max_length=250,
                            blank=False,
                            null=False,
                            verbose_name="Title",
                            )
    rating_avg = models.FloatField(blank=False,
                                   null=False,
                                   verbose_name="RatingAvg",
                                   )
    raters = models.CharField(max_length=250,
                              blank=False,
                              null=False,
                              verbose_name="Raters",
                              )
    published_year = models.CharField(max_length=4,
                                      blank=False,
                                      null=False,
                                      verbose_name="PublishedYear", )
    editions = models.CharField(max_length=250,
                                blank=False,
                                null=False,
                                verbose_name="Editions", )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f'{self.name}({self.author.name})'
