class BrandGuidelines:
    def __init__(
        self,
        brand_name: str,
        logo: str,
        logo_rules: str,
        industry: str,
        tagline: str,
        brand_identity: str,
        website: str,
        visual_style_direction: str,
        color_palette: list[str],
        color_direction: dict[str, str],
        typography: list[str],
        typography_direction: str,
        ui_ad_social_media_direction: str,
        imagery_direction: str,
        target_audience: str,
        audience_interests: list[str],
        audience_pain_points: list[str],
        unique_value: str,
        content_pillars: tuple[tuple[str]],
        social_tone: str,
        inferred_fields: list[str] | None = None,
        field_confidence: dict[str, float] | None = None,
    ) -> None:
        self.brand_name = brand_name
        self.logo = logo
        self.logo_rules = logo_rules
        self.industry = industry
        self.tagline = tagline
        self.brand_identity = brand_identity
        self.website = website
        self.visual_style_direction = visual_style_direction
        self.color_palette = color_palette
        self.color_direction = color_direction
        self.typography = typography
        self.typography_direction = typography_direction
        self.ui_ad_social_media_direction = ui_ad_social_media_direction
        self.imagery_direction = imagery_direction
        self.target_audience = target_audience
        self.audience_interests = audience_interests
        self.audience_pain_points = audience_pain_points
        self.unique_value = unique_value
        self.content_pillars = content_pillars
        self.social_tone = social_tone
        self.inferred_fields = inferred_fields
        self.field_confidence = field_confidence

    @classmethod
    def map_to_model(cls, parsed: dict) -> "BrandGuidelines":
        return BrandGuidelines(
            brand_name=parsed["brand_name"],
            logo=parsed["logo"],
            logo_rules=parsed["logo_rules"],
            industry=parsed["industry"],
            tagline=parsed["tagline"],
            brand_identity=parsed["brand_identity"],
            website=parsed["website"],
            visual_style_direction=parsed["visual_style_direction"],
            color_palette=parsed["color_palette"],
            color_direction=parsed["color_direction"],
            typography=parsed["typography"],
            typography_direction=parsed["typography_direction"],
            ui_ad_social_media_direction=parsed["ui_ad_social_media_direction"],
            imagery_direction=parsed["imagery_direction"],
            target_audience=parsed["target_audience"],
            audience_interests=parsed["audience_interests"],
            audience_pain_points=parsed["audience_pain_points"],
            unique_value=parsed["unique_value"],
            content_pillars=parsed["content_pillars"],
            social_tone=parsed["social_tone"],
            inferred_fields=parsed.get("inferred_fields", []),
            field_confidence=parsed.get("field_confidence", {}),
        )
