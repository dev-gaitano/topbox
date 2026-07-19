import os

# Set dummy OpenAI API key before any imports of modules that initialize ChatOpenAI
os.environ.setdefault("OPENAI_API_KEY", "dummy-key-for-tests")

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from utils import extract_text, parse_brand_data

FIXTURE_PDF = Path(__file__).parent / "fixtures" / "sample_brand.pdf"

VALID_JSON_DICT = {
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
    "content_pillars": [["Pillar 1", "Pillar 2"], ["Pillar 3"]],
    "social_tone": "Humorous",
}


@pytest.fixture
def extracted_text():
    return extract_text(FIXTURE_PDF)


@pytest.fixture
def mock_llm():
    with patch("utils.parse_brand_data.llm") as mock_model:
        yield mock_model


@pytest.fixture
def mock_llm_success(mock_llm):
    mock_response = MagicMock()
    mock_response.content = json.dumps(VALID_JSON_DICT)
    mock_llm.invoke.return_value = mock_response
    return mock_llm


@pytest.fixture
def mock_llm_fails_then_succeeds(mock_llm):
    mock_response_bad1 = MagicMock()
    mock_response_bad1.content = "Malformed JSON 1"

    mock_response_bad2 = MagicMock()
    mock_response_bad2.content = "Malformed JSON 2"

    mock_response_good = MagicMock()
    mock_response_good.content = json.dumps(VALID_JSON_DICT)

    mock_llm.invoke.side_effect = [
        mock_response_bad1,
        mock_response_bad2,
        mock_response_good,
    ]
    return mock_llm


@pytest.fixture
def mock_llm_malformed(mock_llm):
    mock_response_bad1 = MagicMock()
    mock_response_bad1.content = "Malformed JSON 1"

    mock_response_bad2 = MagicMock()
    mock_response_bad2.content = "Malformed JSON 2"

    mock_response_bad3 = MagicMock()
    mock_response_bad3.content = "Malformed JSON 3"

    mock_llm.invoke.side_effect = [
        mock_response_bad1,
        mock_response_bad2,
        mock_response_bad3,
    ]
    return mock_llm


# 1. Valid text in, correct dict out
def test_valid_text_in_correct_dict_out(extracted_text, mock_llm_success):
    result = parse_brand_data(extracted_text)

    assert result is not None
    assert isinstance(result, dict)

    expected_keys = [
        "brand_name",
        "logo",
        "logo_rules",
        "industry",
        "tagline",
        "brand_identity",
        "website",
        "visual_style_direction",
        "color_palette",
        "color_direction",
        "typography",
        "typography_direction",
        "ui_ad_social_media_direction",
        "imagery_direction",
        "target_audience",
        "audience_interests",
        "audience_pain_points",
        "unique_value",
        "content_pillars",
        "social_tone",
    ]

    for key in expected_keys:
        assert key in result

    assert isinstance(result["color_palette"], list)
    assert isinstance(result["color_direction"], dict)


# 2. Malformed JSON triggers exactly one retry
def test_malformed_json_triggers_exactly_one_retry(mock_llm_fails_then_succeeds):
    result = parse_brand_data("dummy text")
    assert result is not None
    assert isinstance(result, dict)
    assert mock_llm_fails_then_succeeds.invoke.call_count == 2


# 3. Two consecutive bad responses returns None
def test_three_consecutive_bad_responses_returns_none(mock_llm_malformed):
    result = parse_brand_data("dummy text")
    assert result is None
    assert mock_llm_malformed.invoke.call_count == 3


# 4. Empty string short-circuits before calling the LLM
def test_empty_string_short_circuits_before_calling_llm(mock_llm):
    result = parse_brand_data("")
    assert result is None
    mock_llm.invoke.assert_not_called()


# 5. Types are correct on list and dict fields
def test_types_are_correct_on_list_and_dict_fields(mock_llm_success):
    result = parse_brand_data("dummy text")
    assert result is not None

    fields_to_check = [
        ("color_palette", lambda x: isinstance(x, list)),
        ("color_direction", lambda x: isinstance(x, dict)),
        ("audience_interests", lambda x: isinstance(x, list)),
        ("audience_pain_points", lambda x: isinstance(x, list)),
        (
            "content_pillars",
            lambda x: isinstance(x, (list, tuple))
            and all(isinstance(i, (list, tuple)) for i in x),
        ),
    ]

    for field_name, check_fn in fields_to_check:
        assert check_fn(result[field_name]), f"{field_name} type check failed"
