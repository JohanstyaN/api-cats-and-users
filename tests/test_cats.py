import pytest

def test_list_breeds(client):
    r = client.get("/breeds")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0] and "name" in data[0]

def test_search_breeds(client):
    r = client.get("/breeds/search?q=siam&attach_image=true")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    for breed in data:
        assert "id" in breed
        assert "image" in breed and "url" in breed["image"]

def test_get_breed_by_id(client):
    all_breeds = client.get("/breeds").json()
    some_id = all_breeds[0]["id"]
    r = client.get(f"/breeds/{some_id}")
    assert r.status_code == 200
    b = r.json()
    assert b["id"] == some_id

def test_get_breed_not_found(client):
    r = client.get("/breeds/doesnotexist")
    assert r.status_code == 404
