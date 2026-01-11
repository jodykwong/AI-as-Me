"""Soul file loader."""
from pathlib import Path
from typing import Dict, Optional


class SoulLoader:
    """Load and manage soul files."""
    
    def __init__(self, soul_dir: Path):
        self.soul_dir = soul_dir
        self.profile_file = soul_dir / "profile.md"
        self.rules_file = soul_dir / "rules.md"
        self.mission_file = soul_dir / "mission.md"
    
    def initialize(self):
        """Initialize soul directory with template files."""
        self.soul_dir.mkdir(exist_ok=True)
        
        # Create profile.md template
        if not self.profile_file.exists():
            self.profile_file.write_text("""# Personal Profile

## Background
<!-- Your professional background, education, experience -->

## Expertise
<!-- Your areas of expertise and skills -->

## Communication Style
<!-- How you prefer to communicate (formal/casual, concise/detailed, etc.) -->

## Language Preference
<!-- Preferred language(s) for communication -->

## Personality Traits
<!-- Key personality traits that should be reflected -->
""")
            self.profile_file.chmod(0o600)
        
        # Create rules.md template
        if not self.rules_file.exists():
            self.rules_file.write_text("""# Decision Rules

## Communication Rules
<!-- Rules about how to communicate -->
- Example: Always be concise and direct

## Technical Rules
<!-- Rules about technical decisions -->
- Example: Prefer Python for scripting tasks

## Work Rules
<!-- Rules about work habits and preferences -->
- Example: Focus on one task at a time

## Life Rules
<!-- Personal life rules and values -->
- Example: Prioritize health and family
""")
            self.rules_file.chmod(0o600)
        
        # Create mission.md template
        if not self.mission_file.exists():
            self.mission_file.write_text("""# Mission & Goals

## Core Mission
<!-- Your overarching mission or purpose -->

## Short-term Goals (3-6 months)
<!-- Immediate goals and objectives -->
- 

## Long-term Goals (1-3 years)
<!-- Future aspirations and targets -->
- 

## Values
<!-- Core values that guide decisions -->
- 
""")
            self.mission_file.chmod(0o600)
    
    def check_status(self) -> Dict[str, bool]:
        """Check which soul files exist.
        
        Returns:
            Dict with existence status for each file
        """
        return {
            "profile": self.profile_file.exists(),
            "rules": self.rules_file.exists(),
            "mission": self.mission_file.exists(),
        }
    
    def load_all(self) -> Optional[str]:
        """Load all soul files into a single context string.
        
        Returns:
            Combined soul context or None if files don't exist
        """
        parts = []
        
        if self.profile_file.exists():
            parts.append(f"# Profile\n{self.profile_file.read_text()}")
        
        if self.rules_file.exists():
            parts.append(f"# Rules\n{self.rules_file.read_text()}")
        
        if self.mission_file.exists():
            parts.append(f"# Mission\n{self.mission_file.read_text()}")
        
        return "\n\n".join(parts) if parts else None
