import json
from typing import Any


class Company:
    def __init__(
        self,
        name: str,
        logo: str,
        industry: str,
        email: str,
        description: str,
        target_audience: str,
        unique_value: str,
        tone: str,
        personality: list,
        color_palette: list,
        main_competitors: list,
    ) -> None:
        # Define expected types per field
        fields: dict[str, tuple] = {
            "name": (name, str),
            "logo": (logo, str),
            "industry": (industry, str),
            "email": (email, str),
            "description": (description, str),
            "target_audience": (target_audience, str),
            "unique_value": (unique_value, str),
            "tone": (tone, str),
            "personality": (personality, list),
            "color_palette": (color_palette, list),
            "main_competitors": (main_competitors, list),
        }

        for value, expected_type in fields.values():
            if not isinstance(value, expected_type):
                raise TypeError("Invalid data type")

        if not all([name, logo, industry, email, description, target_audience, tone]):
            raise ValueError("Missing required fields")

        self.name = name
        self.logo = logo
        self.industry = industry
        self.email = email
        self.description = description
        self.target_audience = target_audience
        self.unique_value = unique_value
        self.tone = tone
        self.personality = personality
        self.color_palette = color_palette
        self.main_competitors = main_competitors

    @classmethod
    def handle_request_data(cls, request_data: dict[str, Any]) -> "Company":
        data = {k.strip(): v for k, v in request_data.items()}

        def clean(key: str) -> str:
            return (data.get(key) or "").strip()

        def split_csv(key: str) -> list[str]:
            value = data.get(key)
            if isinstance(value, list):
                return [str(v).strip() for v in value if str(v).strip()]

            raw = clean(key)
            return [v.strip() for v in raw.split(",") if v.strip()] if raw else []

        return cls(
            name=clean("businessName"),
            logo=clean("logo"),
            industry=clean("industry"),
            email=clean("email"),
            description=clean("description"),
            target_audience=clean("targetAudience"),
            color_palette=split_csv("colorPalette"),
            unique_value=clean("uniqueValue"),
            main_competitors=split_csv("mainCompetitors"),
            personality=split_csv("personality"),
            tone=clean("tone"),
        )

    def to_db_params(self) -> tuple:
        return (
            self.name,
            self.logo,
            self.industry,
            self.email,
            self.description,
            self.target_audience,
            json.dumps(self.color_palette),
            self.unique_value,
            json.dumps(self.main_competitors),
            json.dumps(self.personality),
            self.tone,
        )
