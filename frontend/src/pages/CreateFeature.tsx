import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import FeatureForm from "../components/FeatureForm";
import { featureService } from "../services/api";
import { CreateFeatureRequest } from "../types/Feature";

const CreateFeature: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (data: CreateFeatureRequest) => {
    setIsLoading(true);
    try {
      await featureService.createFeature(data);
      navigate("/");
    } catch (error) {
      console.error("Error creating feature:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <FeatureForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default CreateFeature;
