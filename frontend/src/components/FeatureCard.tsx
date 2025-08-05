import React from "react";
import { featureService } from "../services/api";
import { Feature } from "../types/Feature";

interface FeatureCardProps {
  feature: Feature;
  onVoteUpdate: (id: number, newVotes: number) => void;
  onEdit?: (feature: Feature) => void;
  onDelete?: (id: number) => void;
  showActions?: boolean;
}

const FeatureCard: React.FC<FeatureCardProps> = ({
  feature,
  onVoteUpdate,
  onEdit,
  onDelete,
  showActions = true,
}) => {
  const handleUpvote = async () => {
    try {
      const response = await featureService.upvoteFeature(feature.id);
      onVoteUpdate(feature.id, response.votes);
    } catch (error) {
      console.error("Error upvoting:", error);
    }
  };

  const handleDownvote = async () => {
    try {
      const response = await featureService.downvoteFeature(feature.id);
      onVoteUpdate(feature.id, response.votes);
    } catch (error) {
      console.error("Error downvoting:", error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this feature?")) {
      try {
        await featureService.deleteFeature(feature.id);
        onDelete?.(feature.id);
      } catch (error) {
        console.error("Error deleting:", error);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-800">{feature.title}</h3>
        <div className="flex items-center space-x-2">
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
            {feature.votes} votes
          </span>
        </div>
      </div>

      <p className="text-gray-600 mb-4">{feature.description}</p>

      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <button
            onClick={handleUpvote}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition-colors flex items-center space-x-1"
          >
            <span>👍</span>
            <span>Upvote</span>
          </button>
          <button
            onClick={handleDownvote}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors flex items-center space-x-1"
          >
            <span>👎</span>
            <span>Downvote</span>
          </button>
        </div>

        {showActions && (
          <div className="flex space-x-2">
            <button
              onClick={() => onEdit?.(feature)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              Delete
            </button>
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-500">
        Created: {new Date(feature.created_at).toLocaleDateString()}
      </div>
    </div>
  );
};

export default FeatureCard;
