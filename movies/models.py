from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True, blank=True, default=0.0)

    class Meta:
        ordering = ['-id']

    def total_report(self):
        reports = Report.objects.filter(movie=self, state='inappropriate')
        report = []
        for r in reports:
            report.append(r.id)

        return len(report)

    def __str__(self):
        return f"{self.title}"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title}_{str(self.score)}"


class Report(models.Model):
    movie = models.ForeignKey(Movie, related_name='report', on_delete=models.CASCADE)
    state = models.CharField(max_length=255, default='unresolved')
    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title}_{self.state}"
