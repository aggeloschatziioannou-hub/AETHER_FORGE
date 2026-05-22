import { useEffect, useState, useRef } from "react";
import { getDatabase, ref, onValue, set, onDisconnect, ServerValue } from "firebase/database";

interface CursorPosition {
  x: number;
  y: number;
}

interface PresenceMetrics {
  cursor: CursorPosition;
  viewportOffset: CursorPosition;
  lastActive: number;
}

export const useRealtimePresence = (
  canvasId: string,
  userId: string,
  isAuthenticated: boolean
) => {
  const [presenceList, setPresenceList] = useState<Record<string, PresenceMetrics>>({});
  const lastUpdateRef = useRef<number>(0);
  const throttleWindowMs = 100; // Strict FinOps cost barrier block

  useEffect(() => {
    if (!isAuthenticated || !canvasId || !userId) return;

    const db = getDatabase();
    const presenceRef = ref(db, `presence/${canvasId}`);
    const userPresenceRef = ref(db, `presence/${canvasId}/${userId}`);

    // 1. Establish On-Disconnect Lifecycle Purge Routine (Prevents Zombie States)
    const sessionCleanup = onDisconnect(userPresenceRef);
    sessionCleanup.remove().catch((err) => {
      console.error("Critical: Failed to register onDisconnect purge hook.", err);
    });

    // 2. Open Real-Time Listening Web-Socket Pipeline
    const unsubscribePresence = onValue(presenceRef, (snapshot) => {
      if (snapshot.exists()) {
        setPresenceList(snapshot.val() as Record<string, PresenceMetrics>);
      } else {
        setPresenceList({});
      }
    });

    // Clean up connections when component unmounts or context mutates
    return () => {
      unsubscribePresence();
    };
  }, [canvasId, userId, isAuthenticated]);

  // 3. Throttled Egress Broadcast Channel (Pointer Event Receiver)
  const updatePresenceTelemetry = (cursorX: number, cursorY: number, panX: number, panY: number) => {
    if (!isAuthenticated || !canvasId || !userId) return;

    const now = Date.now();
    if (now - lastUpdateRef.current < throttleWindowMs) return; // Drop redundant network ticks
    lastUpdateRef.current = now;

    const db = getDatabase();
    const userPresenceRef = ref(db, `presence/${canvasId}/${userId}`);

    // Commit state changes to Realtime Database using our strict layout variables
    set(userPresenceRef, {
      cursor: { x: cursorX, y: cursorY },
      viewportOffset: { x: panX, y: panY },
      lastActive: ServerValue.TIMESTAMP, // Sync with server-side time primitives
    }).catch((err) => {
      console.error("Infrastructure Write Refused: Security alignment mismatch.", err);
    });
  };

  return {
    presenceList,
    updatePresenceTelemetry,
  };
};