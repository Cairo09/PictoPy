from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.routes.images import router as images_router


app = FastAPI()
app.include_router(images_router, prefix="/images")
client = TestClient(app)


class TestToggleFavourite:
    @patch("app.routes.images.db_get_image_favourite_status")
    @patch("app.routes.images.db_toggle_image_favourite_status")
    def test_toggle_favourite_existing_image_success(
        self,
        mock_toggle_image_favourite_status,
        mock_get_image_favourite_status,
    ):
        mock_toggle_image_favourite_status.return_value = True
        mock_get_image_favourite_status.return_value = True

        response = client.post(
            "/images/toggle-favourite", json={"image_id": "image-123"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "image_id": "image-123",
            "isFavourite": True,
        }

    @patch("app.routes.images.db_toggle_image_favourite_status")
    def test_toggle_favourite_unknown_image_returns_404(
        self,
        mock_toggle_image_favourite_status,
    ):
        mock_toggle_image_favourite_status.return_value = False

        response = client.post(
            "/images/toggle-favourite", json={"image_id": "unknown-image"}
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Image not found or failed to toggle"
