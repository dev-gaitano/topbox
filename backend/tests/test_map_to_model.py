import pytest

from models.brand_guidelines import BrandGuidelines

VALID_PARSED = {
    "brand_name": "Acme",
    "logo": "logo.png",
    "logo_rules": "Don't stretch it.",
    "industry": "Anvil Manufacturing",
    "tagline": "Quality anvils since 1920",
    "brand_identity": "Industrial, reliable, classic",
    "website": "https://acme.com",
    "visual_style_direction": "Clean lines, industrial colors",
    "color_palette": ["#ff0000", "#00ff00", "#0000ff"],
    "color_direction": {"primary": "red", "secondary": "green"},
    "typography": ["Helvetica", "Arial"],
    "typography_direction": "Clean sans-serif typography",
    "ui_ad_social_media_direction": "Bold layouts",
    "imagery_direction": "Product photos",
    "target_audience": "Coyotes",
    "audience_interests": ["Road runners", "Catching road runners"],
    "audience_pain_points": ["Gravity", "Explosions"],
    "unique_value": "Indestructible anvils",
    "content_pillars": (("Pillar 1", "desc 1"), ("Pillar 2", "desc 2")),
    "social_tone": "Humorous",
    "inferred_fields": ["logo", "website"],
    "field_confidence": {"brand_name": 0.99, "logo": 0.75},
}


def test_returns_brand_guidelines_instance():
    result = BrandGuidelines.map_to_model(VALID_PARSED)
    assert isinstance(result, BrandGuidelines)


def test_all_fields_map_correctly():
    result = BrandGuidelines.map_to_model(VALID_PARSED)
    assert result.brand_name == "Acme"
    assert result.logo == "logo.png"
    assert result.logo_rules == "Don't stretch it."
    assert result.industry == "Anvil Manufacturing"
    assert result.tagline == "Quality anvils since 1920"
    assert result.brand_identity == "Industrial, reliable, classic"
    assert result.website == "https://acme.com"
    assert result.visual_style_direction == "Clean lines, industrial colors"
    assert result.color_palette == ["#ff0000", "#00ff00", "#0000ff"]
    assert result.color_direction == {"primary": "red", "secondary": "green"}
    assert result.typography == ["Helvetica", "Arial"]
    assert result.typography_direction == "Clean sans-serif typography"
    assert result.ui_ad_social_media_direction == "Bold layouts"
    assert result.imagery_direction == "Product photos"
    assert result.target_audience == "Coyotes"
    assert result.audience_interests == ["Road runners", "Catching road runners"]
    assert result.audience_pain_points == ["Gravity", "Explosions"]
    assert result.unique_value == "Indestructible anvils"
    assert result.content_pillars == (("Pillar 1", "desc 1"), ("Pillar 2", "desc 2"))
    assert result.social_tone == "Humorous"
    assert result.inferred_fields == ["logo", "website"]
    assert result.field_confidence == {"brand_name": 0.99, "logo": 0.75}


def test_inferred_fields_defaults_to_empty_list_when_absent():
    parsed = VALID_PARSED.copy()
    del parsed["inferred_fields"]
    result = BrandGuidelines.map_to_model(parsed)
    assert result.inferred_fields == []


def test_field_confidence_defaults_to_empty_dict_when_absent():
    parsed = VALID_PARSED.copy()
    del parsed["field_confidence"]
    result = BrandGuidelines.map_to_model(parsed)
    assert result.field_confidence == {}


def test_raises_on_missing_required_field():
    incomplete = VALID_PARSED.copy()
    del incomplete["brand_name"]
    with pytest.raises(KeyError):
        BrandGuidelines.map_to_model(incomplete)


def test_raises_on_none_input():
    with pytest.raises((TypeError, AttributeError)):
        BrandGuidelines.map_to_model(None)
