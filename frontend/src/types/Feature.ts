export interface Feature {
  id: number;
  title: string;
  description: string;
  votes: number;
  created_at: string;
  updated_at: string;
}

export interface CreateFeatureRequest {
  title: string;
  description: string;
}

export interface UpdateFeatureRequest {
  title?: string;
  description?: string;
}

export interface FeatureListResponse {
  count: number;
  next: boolean;
  previous: boolean;
  results: Feature[];
}
