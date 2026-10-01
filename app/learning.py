from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Lesson:
    topic: str
    lesson: str
    source: str
    confidence: float
    created_at: str

class LearningMemory:
    def __init__(self):
        self.lessons: list[Lesson] = []

    def record(self, topic: str, lesson: str, source: str, confidence: float) -> Lesson:
        item = Lesson(
            topic=topic,
            lesson=lesson,
            source=source,
            confidence=max(0.0, min(confidence, 1.0)),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.lessons.append(item)
        return item

memory = LearningMemory()
