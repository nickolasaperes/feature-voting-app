import json

from django.test import Client, TestCase
from core.models import Feature


class FeatureAPITest(TestCase):
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.feature_data = {
            "title": "Test Feature",
            "description": "This is a test feature description",
        }

        # Create test features
        self.feature1 = Feature.objects.create(
            title="Feature 1", description="Description 1", votes=5
        )
        self.feature2 = Feature.objects.create(
            title="Feature 2", description="Description 2", votes=3
        )

    def test_get_feature_list(self):
        """Test GET /v1/features/ returns feature list"""
        response = self.client.get("/v1/features/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("count", data)
        self.assertIn("results", data)
        self.assertEqual(data["count"], 2)
        self.assertEqual(len(data["results"]), 2)

        # Check ordering (highest votes first)
        self.assertEqual(data["results"][0]["title"], "Feature 1")
        self.assertEqual(data["results"][0]["votes"], 5)

    def test_get_feature_list_with_search(self):
        """Test GET /v1/features/ with search parameter"""
        response = self.client.get("/v1/features/?search=Feature 1")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "Feature 1")

    def test_get_feature_detail(self):
        """Test GET /v1/features/{id}/ returns specific feature"""
        response = self.client.get(f"/v1/features/{self.feature1.id}/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["id"], self.feature1.id)
        self.assertEqual(data["title"], "Feature 1")
        self.assertEqual(data["votes"], 5)

    def test_get_feature_detail_not_found(self):
        """Test GET /v1/features/{id}/ with non-existent ID"""
        response = self.client.get("/v1/features/999/")
        self.assertEqual(response.status_code, 404)

    def test_create_feature_success(self):
        """Test POST /v1/features/ creates new feature"""
        response = self.client.post(
            "/v1/features/",
            data=json.dumps(self.feature_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()

        self.assertEqual(data["title"], "Test Feature")
        self.assertEqual(data["description"], "This is a test feature description")
        self.assertEqual(data["votes"], 0)

        # Verify feature was created in database
        self.assertTrue(Feature.objects.filter(title="Test Feature").exists())

    def test_create_feature_invalid_title_too_short(self):
        """Test POST /v1/features/ with title too short"""
        invalid_data = {"title": "Hi", "description": "Valid description"}

        response = self.client.post(
            "/v1/features/",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("title", data)

    def test_create_feature_missing_title(self):
        """Test POST /v1/features/ without title"""
        invalid_data = {"description": "Valid description"}

        response = self.client.post(
            "/v1/features/",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_feature_missing_description(self):
        """Test POST /v1/features/ without description"""
        invalid_data = {"title": "Valid Title"}

        response = self.client.post(
            "/v1/features/",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_feature_duplicate_title(self):
        """Test POST /v1/features/ with duplicate title"""
        duplicate_data = {
            "title": "Feature 1",  # Already exists
            "description": "Different description",
        }

        response = self.client.post(
            "/v1/features/",
            data=json.dumps(duplicate_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_feature_success(self):
        """Test PATCH /v1/features/{id}/ updates feature"""
        update_data = {"title": "Updated Feature Title"}

        response = self.client.patch(
            f"/v1/features/{self.feature1.id}/",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["title"], "Updated Feature Title")

        # Verify in database
        self.feature1.refresh_from_db()
        self.assertEqual(self.feature1.title, "Updated Feature Title")

    def test_update_feature_full_update(self):
        """Test PUT /v1/features/{id}/ full update"""
        update_data = {
            "title": "Completely New Title",
            "description": "Completely new description",
        }

        response = self.client.put(
            f"/v1/features/{self.feature1.id}/",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["title"], "Completely New Title")
        self.assertEqual(data["description"], "Completely new description")

    def test_delete_feature_success(self):
        """Test DELETE /v1/features/{id}/ deletes feature"""
        feature_id = self.feature1.id

        response = self.client.delete(f"/v1/features/{feature_id}/")

        self.assertEqual(response.status_code, 204)

        # Verify feature was deleted
        self.assertFalse(Feature.objects.filter(id=feature_id).exists())

    def test_upvote_feature(self):
        """Test POST /v1/features/{id}/upvote/ increases votes"""
        initial_votes = self.feature1.votes

        response = self.client.post(f"/v1/features/{self.feature1.id}/upvote/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["votes"], initial_votes + 1)
        self.assertIn("message", data)

        # Verify in database
        self.feature1.refresh_from_db()
        self.assertEqual(self.feature1.votes, initial_votes + 1)

    def test_downvote_feature(self):
        """Test POST /v1/features/{id}/downvote/ decreases votes"""
        initial_votes = self.feature1.votes

        response = self.client.post(f"/v1/features/{self.feature1.id}/downvote/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["votes"], initial_votes - 1)

        # Verify in database
        self.feature1.refresh_from_db()
        self.assertEqual(self.feature1.votes, initial_votes - 1)

    def test_downvote_feature_minimum_zero(self):
        """Test downvote doesn't go below 0"""
        # Create feature with 0 votes
        feature = Feature.objects.create(
            title="Zero Votes Feature", description="Description", votes=0
        )

        response = self.client.post(f"/v1/features/{feature.id}/downvote/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["votes"], 0)

    def test_top_voted_features(self):
        """Test GET /v1/features/top_voted/ returns top voted features"""
        response = self.client.get("/v1/features/top_voted/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        # Should be ordered by votes descending
        self.assertEqual(data[0]["votes"], 5)
        self.assertEqual(data[1]["votes"], 3)

    def test_top_voted_features_with_limit(self):
        """Test GET /v1/features/top_voted/ with limit parameter"""
        response = self.client.get("/v1/features/top_voted/?limit=1")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["votes"], 5)

    def test_recent_features(self):
        """Test GET /v1/features/recent/ returns recent features"""
        response = self.client.get("/v1/features/recent/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_invalid_json_request(self):
        """Test POST with invalid JSON"""
        response = self.client.post(
            "/v1/features/", data="invalid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
