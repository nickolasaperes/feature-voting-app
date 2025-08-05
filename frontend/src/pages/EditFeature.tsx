import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FeatureForm from "../components/FeatureForm";
import { featureService } from "../services/api";
import { CreateFeatureRequest, Feature } from "../types/Feature";

const EditFeature: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [feature, setFeature] = useState<Feature | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      loadFeature(parseInt(id));
    }
  }, [id]);

  const loadFeature = async (featureId: number) => {
    try {
      const feature = await featureService.getFeature(featureId);
      setFeature(feature);
    } catch (error) {
      console.error("Error loading feature:", error);
      navigate("/");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: CreateFeatureRequest) => {
    if (!feature) return;

    setIsLoading(true);
    try {
      await featureService.updateFeature(feature.id, data);
      navigate("/");
    } catch (error) {
      console.error("Error updating feature:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    navigate("/");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl">Loading feature...</div>
      </div>
    );
  }

  if (!feature) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl">Feature not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <FeatureForm
            feature={feature}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default EditFeature;
