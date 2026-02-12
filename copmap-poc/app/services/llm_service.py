from typing import List, Dict, Any
import httpx
from ..config import settings


class LlmService:
    async def generate_patrol_summary(
        self,
        patrol: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        notes: str | None,
        rag_context: List[str],
    ) -> Dict[str, Any]:
        if settings.LLM_MODE.lower() == "groq" and settings.GROQ_API_KEY.strip():
            text = await self._groq_summary(patrol, alerts, notes, rag_context)
            return {"text": text, "generated_with": "groq"}

        # Fallback: deterministic template (still PoC-useful and always runnable)
        risk = self._risk_score(alerts)
        lines = []
        lines.append("Executive Summary: Patrol completed; key alerts reviewed and logged.")
        if notes:
            lines.append(f"Officer Notes: {notes}")
        if alerts:
            lines.append("Key Alerts:")
            for a in alerts[:8]:
                lines.append(f"- {a['priority']} {a['type']} ({a['status']}) @ ({a['lat']:.4f},{a['lon']:.4f})")
        else:
            lines.append("Key Alerts: None recorded.")
        if rag_context:
            lines.append("SOP Context Used (RAG):")
            lines.append(f"- Retrieved {len(rag_context)} relevant SOP/log snippets.")
        lines.append("Recommendations: Increase monitoring at repeated hotspots; validate high-priority alerts quickly.")
        return {"text": "\n".join(lines), "generated_with": "template"}

    def _risk_score(self, alerts: List[Dict[str, Any]]) -> float:
        weights = {"P1": 1.0, "P2": 0.7, "P3": 0.4, "P4": 0.2}
        score = 0.0
        for a in alerts:
            score += weights.get(a.get("priority", "P4"), 0.2)
        return min(1.0, score / 5.0)

    async def _groq_summary(self, patrol, alerts, notes, rag_context) -> str:
        prompt = (
            "You are an assistant for police operations.\n"
            "Generate a concise end-of-shift patrol summary for the station commander.\n\n"
            f"Patrol:\n{patrol}\n\n"
            f"Alerts:\n{alerts}\n\n"
            f"Officer Notes:\n{notes}\n\n"
            f"Retrieved SOP/History context:\n{rag_context}\n\n"
            "Return:\n1) Executive Summary (2-3 sentences)\n"
            "2) Key Incidents (bullets)\n3) Recommendations\n4) Risk Indicators\n"
        )

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You write operationally useful, non-hyped police summaries."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]


llm_service = LlmService()
