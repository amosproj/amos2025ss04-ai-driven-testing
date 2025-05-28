export interface Model {
  id: string;
  name: string;
  running: boolean;
  licence: string;
  licence_link: string;
}

export interface PromptResponse {
  response_markdown: string;
  total_seconds: number;
}

const API_BASE_URL = "http://backend:8000";

export async function getModels(): Promise<Model[]> {
  const res = await fetch(`${API_BASE_URL}/models`);
  if (!res.ok) {
    throw new Error(`GET /models failed: ${res.status} ${res.statusText}`);
  }
  const data = await res.json();
  console.debug("Erhaltene Modelle:", data);
  return data;
}

export async function sendPrompt(
  model_id: string,
  prompt: string
): Promise<PromptResponse> {
  const res = await fetch(`${API_BASE_URL}/prompt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model_id, prompt }),
  });
  if (!res.ok) {
    throw new Error(`POST /prompt failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function shutdownModel(model_id: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/shutdown`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model_id }),
  });
  if (!res.ok) {
    throw new Error(`POST /shutdown failed: ${res.status} ${res.statusText}`);
  }
} 