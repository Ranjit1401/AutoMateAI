const API = process.env.NEXT_PUBLIC_API_URL!;

export interface ExecutionStep {
  agent: string;
  status: string;
  message: string;
}

export interface ChatResponse {
  session_id: string;
  response: string;
  execution: ExecutionStep[];
}

export async function sendMessage(
  message: string
): Promise<ChatResponse> {
  const response = await fetch(`${API}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: "admin123",
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to contact backend");
  }

  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${API}/health`);

  if (!response.ok) {
    throw new Error("Backend Offline");
  }

  return response.json();
}