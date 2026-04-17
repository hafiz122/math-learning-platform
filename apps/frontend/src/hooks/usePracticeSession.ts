import { useCallback, useEffect, useState } from "react";
import { createSession } from "../api/questionApi";

export function usePracticeSession() {
  const [sessionId, setSessionId] = useState<string>("");
  const [isCreating, setIsCreating] = useState(true);

  const startSession = useCallback(async () => {
    setIsCreating(true);
    const response = await createSession();
    setSessionId(response.session_id);
    setIsCreating(false);
  }, []);

  useEffect(() => {
    void startSession();
  }, [startSession]);

  return {
    sessionId,
    isCreating,
    startSession
  };
}
