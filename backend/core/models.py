from django.core.validators import MinLengthValidator
from django.db import models


class Feature(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)],
        help_text="Feature title (minimum 5 characters)",
    )
    description = models.TextField(help_text="Detailed feature description")
    votes = models.IntegerField(default=0, help_text="Number of votes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-votes", "-created_at"]
        indexes = [
            models.Index(fields=["-votes", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.votes} votes)"

    def upvote(self):
        """Increment vote count"""
        self.votes += 1
        self.save(update_fields=["votes"])

    def downvote(self):
        """Decrement vote count (minimum 0)"""
        self.votes = max(0, self.votes - 1)
        self.save(update_fields=["votes"])
