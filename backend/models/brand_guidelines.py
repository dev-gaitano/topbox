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
        self.__inferred_fields: list[str] = []
        self.__field_confidence: dict[str, float] = {}
