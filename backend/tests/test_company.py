from typing import Any

import pytest

from app.models.company import Company


def test_company_checks_datatype():
    """Raises error if value datatype is invalid"""
    with pytest.raises(TypeError, match="Invalid data type"):
        Company(
            name=1,
            logo=[],
            industry=True,
            email={},
            description=0.5,
            target_audience="test",
            unique_value="value",
            tone="test",
            personality=[],
            color_palette=[],
            main_competitors=[],
        )


def test_company_requires_data():
    """Raises value error if required data is missing"""
    with pytest.raises(ValueError, match="Missing required fields"):
        Company(
            name="",
            logo="",
            industry="",
            email="",
            description="",
            target_audience="",
            unique_value="value",
            tone="",
            personality=[],
            color_palette=[],
            main_competitors=[],
        )


@pytest.fixture
def data() -> dict[str, Any]:
    return {
        "   businessName  ": "SpaceX",
        "logo": "https://logo.com/space.png",
        "industry": "  Aerospace  ",
        "email": "elon@spacex.com",
        "description": "Making life multi-planetary",
        "targetAudience": "Humanity",
        "colorPalette": " #000000 , #FFFFFF , #B5B5B5 ",
        "uniqueValue": "Reusable rockets",
        "mainCompetitors": "",
        "personality": ["Bold", "Innovative", "Visionary"],
        "tone": "Inspirational",
    }


def test_handle_request_data(data):
    """Returns Company instance with valid data"""
    company = Company.handle_request_data(data)

    assert company.name == "SpaceX"
    assert company.industry == "Aerospace"
    assert company.color_palette == ["#000000", "#FFFFFF", "#B5B5B5"]
    assert company.main_competitors == []
    assert company.personality == ["Bold", "Innovative", "Visionary"]


def test_to_db_params(data):
    """Returns tuple with data in the correct order"""
    db_params = Company.handle_request_data(data).to_db_params()

    assert db_params[0] == "SpaceX"
    assert db_params[1] == "https://logo.com/space.png"
    assert db_params[2] == "Aerospace"
    assert db_params[3] == "elon@spacex.com"
    assert db_params[4] == "Making life multi-planetary"
    assert db_params[5] == "Humanity"
    assert db_params[6] == '["#000000", "#FFFFFF", "#B5B5B5"]'
    assert db_params[7] == "Reusable rockets"
    assert db_params[8] == "[]"
    assert db_params[9] == '["Bold", "Innovative", "Visionary"]'
    assert db_params[10] == "Inspirational"


def test_handle_request_data_with_lists():
    """Verify handle_request_data handles fields that are already lists"""
    list_data = {
        "businessName": "List Co",
        "logo": "logo.png",
        "industry": "testing",
        "email": "test@test.com",
        "description": "desc",
        "targetAudience": "devs",
        "colorPalette": ["#000", "#fff"],
        "mainCompetitors": ["Comp A", "Comp B"],
        "personality": ["Friendly"],
        "tone": "Casual",
    }

    company = Company.handle_request_data(list_data)
    assert company.color_palette == ["#000", "#fff"]
    assert company.main_competitors == ["Comp A", "Comp B"]
    assert company.personality == ["Friendly"]
