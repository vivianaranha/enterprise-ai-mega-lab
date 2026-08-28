from pathlib import Path
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.config import settings

@dataclass
class KnowledgeChunk:
    source: str
    text: str

class KnowledgeRetriever:
    def __init__(self):
        self.chunks: list[KnowledgeChunk] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self.refresh()

    def refresh(self):
        knowledge_dir = settings.project_root / "knowledge"
        chunks = []
        for path in sorted(knowledge_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            # Knowledge files in this lab are intentionally short. Keeping each
            # file together prevents headings from being retrieved without the
            # policy or product text that gives them meaning.
            chunks.append(KnowledgeChunk(str(path.relative_to(settings.project_root)), text.strip()))
        self.chunks = chunks
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks]) if chunks else None

    def search(self, query: str, top_k: int | None = None):
        if not self.chunks or self.matrix is None:
            return []
        k = top_k or settings.top_k_retrieval
        qv = self.vectorizer.transform([query])
        scores = cosine_similarity(qv, self.matrix).flatten()
        indices = scores.argsort()[::-1][:k]
        results = []
        for idx in indices:
            if scores[idx] <= 0:
                continue
            c = self.chunks[idx]
            results.append({"source": c.source, "score": round(float(scores[idx]), 4), "excerpt": c.text[:700]})
        return results

retriever = KnowledgeRetriever()
