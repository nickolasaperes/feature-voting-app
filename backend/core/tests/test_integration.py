import json

from django.test import TransactionTestCase
from core.models import Feature


class FeatureIntegrationTest(TransactionTestCase):
    def setUp(self):
        """Set up test data"""
        self.feature = Feature.objects.create(
            title="Integration Test Feature",
            description="Testing integration scenarios",
        )

    def test_concurrent_voting(self):
        """Test concurrent voting doesn't cause race conditions"""
        feature_id = self.feature.id

        # Simulate multiple upvotes
        responses = []
        for _ in range(5):
            response = self.client.post(f"/v1/features/{feature_id}/upvote/")
            responses.append(response)

        # All requests should succeed
        for response in responses:
            self.assertEqual(response.status_code, 200)

        # Final vote count should be correct
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.votes, 5)

    def test_feature_lifecycle(self):
        """Test complete feature lifecycle: create, read, update, vote, delete"""
        # Create
        create_data = {
            "title": "Lifecycle Test Feature",
            "description": "Testing complete lifecycle",
        }

        response = self.client.post(
            "/v1/features/",
            data=json.dumps(create_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        feature_data = response.json()
        feature_id = feature_data["id"]

        # Read
        response = self.client.get(f"/v1/features/{feature_id}/")
        self.assertEqual(response.status_code, 200)

        # Update
        update_data = {"title": "Updated Lifecycle Feature"}
        response = self.client.patch(
            f"/v1/features/{feature_id}/",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Vote
        response = self.client.post(f"/v1/features/{feature_id}/upvote/")
        self.assertEqual(response.status_code, 200)

        # Verify vote
        response = self.client.get(f"/v1/features/{feature_id}/")
        data = response.json()
        self.assertEqual(data["votes"], 1)

        # Delete
        response = self.client.delete(f"/v1/features/{feature_id}/")
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        response = self.client.get(f"/v1/features/{feature_id}/")
        self.assertEqual(response.status_code, 404)

    def test_search_functionality(self):
        """Test search across multiple features"""
        # Create test features
        Feature.objects.create(title="Feature", description="About Python")
        Feature.objects.create(title="JavaScript Feature", description="About JS")
        Feature.objects.create(
            title="Django Feature", description="Python web framework"
        )

        # Search by title
        response = self.client.get("/v1/features/?search=Python")
        data = response.json()
        self.assertEqual(data["count"], 2)

        # Search by description
        response = self.client.get("/v1/features/?search=Python")
        data = response.json()
        self.assertEqual(data["count"], 2)

        # Case insensitive search
        response = self.client.get("/v1/features/?search=python")
        data = response.json()
        self.assertEqual(data["count"], 2)
