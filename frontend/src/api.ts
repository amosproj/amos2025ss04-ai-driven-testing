export interface Model {
  id: string;
  name: string;
  running: boolean;
  licence: string;
  licence_link: string;
}

export interface Module {
  id: string;
  name: string;
  filename: string;
  applies_before: boolean;
  applies_after: boolean;
  description: string;
  dependencies: Array<String>;
}

export interface PromptResponse {
  response_markdown: string;
  total_seconds: number;
  modules_used: string[];
}

export interface response {
  response_markdown: string;
  total_seconds: number;
  modules_used: string[];
  output: {
    code: string | null;
    syntax_valid: boolean | null;
    ccc_complexity: number | null;
    mcc_complexity: number | null;
    lm_eval: unknown | null;
  };
  timing: {
    loading_time: number;
    generation_time: number;
  };
  prompt_data: {
    token_count: number | null;
    token_count_estimated: number | null;
    ccc_complexity: number | null;
    mcc_complexity: number | null;
    rag_sources: unknown | null;
  };
}

const API_BASE_URL = "http://localhost:8000";

export async function getModels(): Promise<Model[]> {
  const res = await fetch(`${API_BASE_URL}/models`);
  if (!res.ok) {
    throw new Error(`GET /models failed: ${res.status} ${res.statusText}`);
  }
  const data = await res.json();
  console.debug("Erhaltene Modelle:", data);
  return data;
}

export async function getModules(): Promise<Module[]> {
  const res = await fetch(`${API_BASE_URL}/modules`);
  if (!res.ok) {
    throw new Error(`GET /modules failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function sendPrompt(
  model: Model,
  user_message: string,
  source_code: string,
  modules: string[] = []
): Promise<PromptResponse> {
  const body = {
    model: {
      id: model.id,
      name: model.name,
    },
    input: {
      user_message,
      source_code,
      system_message:
        "You are a helpful assistant. Provide your answer always in Markdown.\nFormat code blocks appropriately, and do not include text outside valid Markdown.",
      options: {
        temperature: 0.7,
        num_ctx: 4096,
        seed: 42,
        top_p: 0.95,
      },
    },
    modules: modules,
  };

  const res = await fetch(`${API_BASE_URL}/prompt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(`POST /prompt failed: ${res.status} - ${error}`);
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