"""
Prompt Manager & Versioning Registry Module.

Decouples prompt engineering, system directives, and prompt templates from API endpoints.
Provides prompt versioning (V1, V2), template parameter substitution, and prompt builder tools.
"""

from typing import Any


class PromptTemplate:
    """Represents a versioned, parameterized prompt template."""

    def __init__(self, version: str, name: str, system_instruction: str, user_template: str):
        self.version = version
        self.name = name
        self.system_instruction = system_instruction
        self.user_template = user_template

    def render(self, **kwargs: Any) -> str:
        """Substitutes variables into template string."""
        return self.user_template.format(**kwargs)


class PromptBuilder:
    """Builder class for dynamically assembling prompts with context."""

    def __init__(self, template: PromptTemplate):
        self.template = template
        self.params: dict[str, Any] = {}

    def set_param(self, key: str, value: Any) -> "PromptBuilder":
        self.params[key] = value
        return self

    def build_user_prompt(self) -> str:
        return self.template.render(**self.params)

    def get_system_instruction(self) -> str:
        return self.template.system_instruction


# ==========================================
# PROMPT REGISTRY & VERSIONS
# ==========================================

# Learning Path System Instructions
SYSTEM_INSTRUCTION_LEARNING_PATH = """
You are an expert Enterprise L&D AI Business Assistant and Technical Career Advisor.
Your objective is to generate highly structured, actionable, and realistic career learning roadmaps for users.
You MUST ALWAYS respond with strict, valid JSON strictly adhering to the specified schema.
Do NOT wrap your JSON response in extra commentary, conversational intro text, or explanation outside the JSON.
"""

# Learning Path Prompt V1
PROMPT_LEARNING_PATH_V1 = PromptTemplate(
    version="V1",
    name="learning_path_generator_v1",
    system_instruction=SYSTEM_INSTRUCTION_LEARNING_PATH,
    user_template="""
User Career Goal: {career_goal}
Current User Skills: {current_skills}

Generate a comprehensive learning path response strictly matching the following JSON structure:
{{
  "career_goal": "{career_goal}",
  "recommended_courses": [
    {{
      "title": "Course Name",
      "description": "Short description of what course covers",
      "category": "Domain/Category",
      "difficulty": "Beginner/Intermediate/Advanced",
      "reason": "Why recommended"
    }}
  ],
  "learning_path": [
    {{
      "week": 1,
      "topic": "Module or Topic Title",
      "description": "Weekly learning goal and key concepts",
      "skills_to_acquire": ["Skill 1", "Skill 2"]
    }}
  ],
  "estimated_duration": "Estimated time (e.g. '6 Weeks')",
  "difficulty": "Overall level (Beginner/Intermediate/Advanced)",
  "summary": "Executive summary explaining the roadmap tailored to user skills"
}}

Respond ONLY with valid JSON.
"""
)

# Learning Path Prompt V2 (Enhanced domain context & course library matching)
PROMPT_LEARNING_PATH_V2 = PromptTemplate(
    version="V2",
    name="learning_path_generator_v2",
    system_instruction=SYSTEM_INSTRUCTION_LEARNING_PATH,
    user_template="""
Analyze candidate profile for Career Role: {career_goal}
Candidate Existing Skill Inventory: {current_skills}

Instructions:
1. Identify critical skill gaps between current skills and target career goal.
2. Recommend 2 to 4 high-impact courses targeting the missing competencies.
3. Formulate a multi-week step-by-step sequential learning path (4 to 8 weeks).
4. Provide realistic duration and difficulty assessment.

Required JSON Output Format:
{{
  "career_goal": "{career_goal}",
  "recommended_courses": [
    {{
      "title": "Course Title",
      "description": "Course focus and key deliverables",
      "category": "Technical Category",
      "difficulty": "Beginner | Intermediate | Advanced",
      "reason": "Detailed rationale for recommendation"
    }}
  ],
  "learning_path": [
    {{
      "week": 1,
      "topic": "Weekly Topic Title",
      "description": "Concrete learning actions and practical projects",
      "skills_to_acquire": ["Skill A", "Skill B"]
    }}
  ],
  "estimated_duration": "X Weeks",
  "difficulty": "Beginner | Intermediate | Advanced",
  "summary": "Custom tailored executive career summary"
}}

Output ONLY the JSON object.
"""
)


# General AI Assistant System Instruction
SYSTEM_INSTRUCTION_CHAT = """
You are an expert AI Business Assistant for an Enterprise Learning Management Platform.
You assist employees, managers, and learners with career planning, skill development advice, course recommendations, and industry insights.
Be professional, encouraging, clear, and structured in your responses.
"""

# General Chat Prompt V1
PROMPT_CHAT_V1 = PromptTemplate(
    version="V1",
    name="ai_chat_assistant_v1",
    system_instruction=SYSTEM_INSTRUCTION_CHAT,
    user_template="""
User Career Goal Context: {career_goal}
User Current Skills Context: {current_skills}

Conversation Context History:
{conversation_history}

Current User Message: {user_message}

Provide a helpful, precise, professional response:
"""
)


class PromptManager:
    """Central registry to retrieve and configure prompts by version."""

    def __init__(self) -> None:
        self._learning_path_templates: dict[str, PromptTemplate] = {
            "V1": PROMPT_LEARNING_PATH_V1,
            "V2": PROMPT_LEARNING_PATH_V2,
        }
        self._chat_templates: dict[str, PromptTemplate] = {
            "V1": PROMPT_CHAT_V1,
        }
        self.default_version = "V2"

    def get_learning_path_builder(
        self,
        career_goal: str,
        current_skills: list[str],
        version: str | None = None
    ) -> PromptBuilder:
        v = version or self.default_version
        template = self._learning_path_templates.get(v, PROMPT_LEARNING_PATH_V2)
        
        skills_str = ", ".join(current_skills) if current_skills else "None specified"
        
        builder = PromptBuilder(template)
        builder.set_param("career_goal", career_goal)
        builder.set_param("current_skills", skills_str)
        return builder

    def get_chat_builder(
        self,
        user_message: str,
        conversation_history: str = "",
        career_goal: str | None = None,
        current_skills: list[str] | None = None,
        version: str | None = None
    ) -> PromptBuilder:
        v = version or "V1"
        template = self._chat_templates.get(v, PROMPT_CHAT_V1)
        
        skills_str = ", ".join(current_skills) if current_skills else "Not specified"
        goal_str = career_goal or "Not specified"
        
        builder = PromptBuilder(template)
        builder.set_param("user_message", user_message)
        builder.set_param("conversation_history", conversation_history or "No previous message history.")
        builder.set_param("career_goal", goal_str)
        builder.set_param("current_skills", skills_str)
        return builder


prompt_manager = PromptManager()
