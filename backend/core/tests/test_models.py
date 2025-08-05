from django.core.exceptions import ValidationError
from django.test import TestCase
from core.models import Feature


class FeatureModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.feature_data = {
            "title": "Test Feature",
            "description": "This is a test feature description",
        }

    def test_feature_creation(self):
        """Test creating a feature with valid data"""
        feature = Feature.objects.create(**self.feature_data)

        self.assertEqual(feature.title, "Test Feature")
        self.assertEqual(feature.description, "This is a test feature description")
        self.assertEqual(feature.votes, 0)
        self.assertIsNotNone(feature.created_at)
        self.assertIsNotNone(feature.updated_at)

    def test_feature_str_representation(self):
        """Test string representation of feature"""
        feature = Feature.objects.create(**self.feature_data)
        expected_str = f"{feature.title} ({feature.votes} votes)"
        self.assertEqual(str(feature), expected_str)

    def test_feature_ordering(self):
        """Test that features are ordered by votes desc, then created_at desc"""
        feature1 = Feature.objects.create(title="Feature 1", description="Desc 1")
        feature2 = Feature.objects.create(title="Feature 2", description="Desc 2")
        feature3 = Feature.objects.create(title="Feature 3", description="Desc 3")

        # Give feature2 more votes
        feature2.votes = 5
        feature2.save()

        # Give feature3 some votes
        feature3.votes = 3
        feature3.save()

        features = list(Feature.objects.all())
        self.assertEqual(features[0], feature2)  # Highest votes first
        self.assertEqual(features[1], feature3)  # Second highest votes
        self.assertEqual(features[2], feature1)  # Lowest votes last

    def test_upvote_method(self):
        """Test upvote method increases votes by 1"""
        feature = Feature.objects.create(**self.feature_data)
        initial_votes = feature.votes

        feature.upvote()
        feature.refresh_from_db()

        self.assertEqual(feature.votes, initial_votes + 1)

    def test_downvote_method(self):
        """Test downvote method decreases votes by 1"""
        feature = Feature.objects.create(**self.feature_data)
        feature.votes = 5
        feature.save()

        feature.downvote()
        feature.refresh_from_db()

        self.assertEqual(feature.votes, 4)

    def test_downvote_minimum_zero(self):
        """Test downvote doesn't go below 0"""
        feature = Feature.objects.create(**self.feature_data)
        # votes is already 0

        feature.downvote()
        feature.refresh_from_db()

        self.assertEqual(feature.votes, 0)

    def test_title_min_length_validation(self):
        """Test title minimum length validation"""
        with self.assertRaises(ValidationError):
            feature = Feature(title="Hi", description="Valid description")
            feature.full_clean()

    def test_title_max_length(self):
        """Test title maximum length"""
        long_title = "x" * 201  # Exceeds 200 char limit
        with self.assertRaises(ValidationError):
            feature = Feature(title=long_title, description="Valid description")
            feature.full_clean()

    def test_description_required(self):
        """Test description is required"""
        with self.assertRaises(ValidationError):
            feature = Feature(title="Valid Title", description="")
            feature.full_clean()
