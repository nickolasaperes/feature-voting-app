import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Feature } from "../types/Feature";
import { featureService } from "../services/api";
import FeatureCard from "../components/FeatureCard";
import SearchBar from "../components/SearchBar";

const FeatureList: React.FC = () => {
  const [features, setFeatures] = useState<Feature[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const loadFeatures = async () => {
    try {
      setLoading(true);
      const response = await featureService.getFeatures(searchQuery);
      setFeatures(response.results);
    } catch (error) {
      console.error("Error loading features:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeatures();
  }, [searchQuery]);

  const handleVoteUpdate = (id: number, newVotes: number) => {
    setFeatures((prev) =>
      prev.map((feature) =>
        feature.id === id ? { ...feature, votes: newVotes } : feature,
      ),
    );
  };

  const handleEdit = (feature: Feature) => {
    navigate(`/features/${feature.id}/edit`);
  };

  const handleDelete = (id: number) => {
    setFeatures((prev) => prev.filter((feature) => feature.id !== id));
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl">Loading features...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">
            Feature Voting System
          </h1>
          <Link
            to="/features/new"
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-md transition-colors"
          >
            Create Feature
          </Link>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleSearch} />
        </div>

        {features.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600 mb-4">
              {searchQuery
                ? "No features found matching your search."
                : "No features yet."}
            </p>
            <Link
              to="/features/new"
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-md transition-colors"
            >
              Create the First Feature
            </Link>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <FeatureCard
                key={feature.id}
                feature={feature}
                onVoteUpdate={handleVoteUpdate}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FeatureList;
