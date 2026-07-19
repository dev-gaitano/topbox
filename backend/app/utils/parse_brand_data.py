import json
import logging
from typing import Any, Optional
from agents import model as llm

logger = logging.getLogger(__name__)


def parse_brand_data(text: str) -> Optional[dict[str, Any]]:
    if not text or not text.strip():
        return None

    prompt = f"""You are a brand analysis expert. Analyze the following extracted text from a brand guidelines document and extract the brand data.
You MUST output a valid JSON object. Do not wrap the JSON in markdown code blocks or any other formatting, just return raw JSON.

The JSON object must have exactly the following 20 keys with the specified types:
- brand_name: string
- logo: string
- logo_rules: string
- industry: string
- tagline: string
- brand_identity: string
- website: string
- visual_style_direction: string
- color_palette: list of strings (hex colors)
- color_direction: dictionary of key-value string pairs
- typography: list of strings (font names)
- typography_direction: string
- ui_ad_social_media_direction: string
- imagery_direction: string
- target_audience: string
- audience_interests: list of strings
- audience_pain_points: list of strings
- unique_value: string
- content_pillars: list of lists of strings (representing pillars/categories)
- social_tone: string
- inferred_fields: list of strings - field names you inferred because they were not explicitly stated in the document
- field_confidence: dictionary of field name to confidence score (0.0 to 1.0) for every field you extracted or inferred

Text to analyze:
{text}
"""

    for attempt in range(3):
        content_cleaned = None

        try:
            response = llm.invoke(prompt)
            content = (
                response.content if hasattr(response, "content") else str(response)
            )

            if not isinstance(content, str):
                content = str(content)

            content_cleaned = content.strip()

            # Remove markdown code fences
            if content_cleaned.startswith("```"):
                lines = content_cleaned.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content_cleaned = "\n".join(lines).strip()

            data = json.loads(content_cleaned)

            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")

            # Define expected types per field
            required_fields: dict[str, type] = {
                "brand_name": str,
                "logo": str,
                "logo_rules": str,
                "industry": str,
                "tagline": str,
                "brand_identity": str,
                "website": str,
                "visual_style_direction": str,
                "color_palette": list,
                "color_direction": dict,
                "typography": list,
                "typography_direction": str,
                "ui_ad_social_media_direction": str,
                "imagery_direction": str,
                "target_audience": str,
                "audience_interests": list,
                "audience_pain_points": list,
                "unique_value": str,
                "content_pillars": list,
                "social_tone": str,
                "inferred_fields": list,
                "field_confidence": dict,
            }

            for key in required_fields.keys():
                if key not in data:
                    raise ValueError(f"Missing key: {key}")

            for key, expected_type in required_fields.items():
                if not isinstance(data[key], expected_type):
                    raise TypeError(f"Invalid data type for {key}")

            data["content_pillars"] = tuple(
                tuple(pillar) for pillar in data["content_pillars"]
            )

            data["field_confidence"] = {
                key: float(value) for key, value in data["field_confidence"].items()
            }

            return data
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            logger.warning(f"Attempt {attempt + 1} failed parsing brand data: {e}")
            if attempt == 2:
                logger.warning(f"Final failure. Raw response: {content_cleaned!r}")
                return None
        except Exception as e:
            logger.error(f"Unexpected error calling LLM: {e}")
            raise
    return None
