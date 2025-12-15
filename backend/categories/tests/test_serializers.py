import pytest  # type: ignore
from categories.serializers import CategorySerializer
#from categories.models import Category

@pytest.fixture
def valid_category_data():
    return {
        "name": "Home Appliances"
    } 

@pytest.mark.django_db
def test_category_serializer_valid_data(valid_category_data):
    serializer = CategorySerializer(data=valid_category_data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_category_serializer_empty_name():
    serializer = CategorySerializer(data={"name": ""})

    assert not serializer.is_valid()
    assert "name" in serializer.errors

@pytest.mark.django_db
def test_category_serializer_slug_is_read_only(valid_category_data):
    valid_category_data["slug"] = "manual-slug"

    serializer = CategorySerializer(data=valid_category_data)
    assert serializer.is_valid()

    category = serializer.save()
    assert category.slug == "home-appliances"