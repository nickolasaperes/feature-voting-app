import axios from "axios";
import {
    CreateFeatureRequest,
    Feature,
    FeatureListResponse,
    UpdateFeatureRequest
} from "../types/Feature";

const API_VERSION = "v1";
const API_BASE_URL = `http://localhost:8000/${API_VERSION}`;

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const featureService = {
  getFeatures: (search?: string, page?: number): Promise<FeatureListResponse> =>
    api
      .get("/features/", {
        params: { search, page },
      })
      .then((res) => res.data),

  getFeature: (id: number): Promise<Feature> =>
    api.get(`/features/${id}/`).then((res) => res.data),

  createFeature: (data: CreateFeatureRequest): Promise<Feature> =>
    api.post("/features/", data).then((res) => res.data),

  updateFeature: (id: number, data: UpdateFeatureRequest): Promise<Feature> =>
    api.patch(`/features/${id}/`, data).then((res) => res.data),

  deleteFeature: (id: number): Promise<void> => api.delete(`/features/${id}/`),

  upvoteFeature: (id: number) =>
    api.post(`/features/${id}/upvote/`).then((res) => res.data),

  downvoteFeature: (id: number) =>
    api.post(`/features/${id}/downvote/`).then((res) => res.data),

  getTopVoted: (limit?: number): Promise<Feature[]> =>
    api
      .get("/features/top_voted/", { params: { limit } })
      .then((res) => res.data),

  getRecent: (limit?: number): Promise<Feature[]> =>
    api.get("/features/recent/", { params: { limit } }).then((res) => res.data),
};
