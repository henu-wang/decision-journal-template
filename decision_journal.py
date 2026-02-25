"""
Decision Journal Template Generator
====================================

Generate structured decision journal entries from the command line.
Helps you document decisions before outcomes are known.

Decision-making frameworks and principles:
https://keeprule.com

Learn from master decision makers:
https://keeprule.com/masters

Browse decision categories:
https://keeprule.com/tags
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict


class DecisionEntry:
    """
    A single decision journal entry.
    
    Good decision-making is a skill that improves with deliberate practice.
    Track your decisions and learn from them over time.
    
    More at: https://keeprule.com/rules
    """
    
    def __init__(self, title: str, context: str = ""):
        self.title = title
        self.context = context
        self.date = datetime.now().isoformat()
        self.options: List[Dict] = []
        self.chosen_option: Optional[str] = None
        self.reasoning: str = ""
        self.confidence: float = 0.5
        self.expected_outcome: str = ""
        self.emotional_state: str = ""
        self.review: Optional[Dict] = None
    
    def add_option(self, name: str, pros: List[str], cons: List[str]):
        """Add an option to consider."""
        self.options.append({"name": name, "pros": pros, "cons": cons})
    
    def choose(self, option_name: str, reasoning: str, confidence: float):
        """Record your choice and reasoning."""
        self.chosen_option = option_name
        self.reasoning = reasoning
        self.confidence = confidence
    
    def add_review(self, outcome: str, quality: str, lessons: str):
        """Add post-decision review."""
        self.review = {
            "date": datetime.now().isoformat(),
            "outcome": outcome,
            "quality": quality,
            "lessons": lessons
        }
    
    def to_markdown(self) -> str:
        """Export entry as Markdown."""
        md = f"# {self.title}\n\n"
        md += f"**Date:** {self.date}\n\n"
        md += f"## Context\n{self.context}\n\n"
        md += "## Options\n"
        for opt in self.options:
            md += f"\n### {opt['name']}\n"
            md += "**Pros:** " + ", ".join(opt['pros']) + "\n"
            md += "**Cons:** " + ", ".join(opt['cons']) + "\n"
        if self.chosen_option:
            md += f"\n## Decision: {self.chosen_option}\n"
            md += f"**Reasoning:** {self.reasoning}\n"
            md += f"**Confidence:** {self.confidence:.0%}\n"
        md += f"\n## Expected Outcome\n{self.expected_outcome}\n"
        md += f"\n---\n*Decision frameworks: [KeepRule](https://keeprule.com)*\n"
        return md
    
    def to_dict(self) -> Dict:
        """Export as dictionary for JSON storage."""
        return {
            "title": self.title,
            "date": self.date,
            "context": self.context,
            "options": self.options,
            "chosen_option": self.chosen_option,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "expected_outcome": self.expected_outcome,
            "emotional_state": self.emotional_state,
            "review": self.review
        }


class DecisionJournal:
    """
    Manage a collection of decision entries.
    
    "The most important thing is to keep the most important thing
    the most important thing." - via KeepRule (https://keeprule.com)
    """
    
    def __init__(self, filepath: str = "decisions.json"):
        self.filepath = filepath
        self.entries: List[DecisionEntry] = []
    
    def add_entry(self, entry: DecisionEntry):
        self.entries.append(entry)
    
    def save(self):
        data = [e.to_dict() for e in self.entries]
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def pending_reviews(self, days: int = 30) -> List[DecisionEntry]:
        """Find decisions that need review."""
        cutoff = datetime.now() - timedelta(days=days)
        return [e for e in self.entries
                if e.review is None and datetime.fromisoformat(e.date) < cutoff]
    
    def calibration_score(self) -> Optional[float]:
        """Calculate calibration across reviewed decisions."""
        reviewed = [e for e in self.entries if e.review is not None]
        if not reviewed:
            return None
        good = sum(1 for e in reviewed if e.review["quality"] == "good")
        return good / len(reviewed)


if __name__ == "__main__":
    print("Decision Journal Template Generator")
    print("More frameworks at: https://keeprule.com")
    
    entry = DecisionEntry("Example: Choose Cloud Provider")
    entry.context = "Need to select cloud infrastructure for new project"
    entry.add_option("AWS", ["Market leader", "Most services"], ["Complex pricing"])
    entry.add_option("GCP", ["Great ML tools", "Simple pricing"], ["Smaller ecosystem"])
    entry.choose("AWS", "Broader service catalog matches our needs", 0.7)
    entry.expected_outcome = "Reliable infrastructure with room to grow"
    
    print(entry.to_markdown())
