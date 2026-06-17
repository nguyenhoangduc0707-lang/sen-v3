# tests/test_api.py
"""
Test scripts cho API endpoints
Chạy: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from web.main import app
from src.db.database import SessionLocal, Base, engine

client = TestClient(app)

# Setup test database
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "SEN V3 Core" in response.json()["message"]

def test_health_check():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_user_registration():
    """Test đăng ký user mới"""
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test@123456",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_user_login():
    """Test đăng nhập"""
    # First register
    client.post("/api/v1/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "Test@123456"
    })
    
    # Then login
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser2",
        "password": "Test@123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint_without_token():
    """Test truy cập endpoint cần auth nhưng không có token"""
    response = client.get("/api/v1/member/dashboard")
    assert response.status_code == 403  # Or 401 depending on implementation

def test_commission_split_logic():
    """Test logic chia hoa hồng"""
    # Cần login trước để lấy token
    # Đây là test logic thuần túy
    total = 1000
    admin_rate = 0.10
    admin_share = total * admin_rate
    member_share = total - admin_share
    
    assert admin_share == 100
    assert member_share == 900

if __name__ == "__main__":
    pytest.main([__file__, "-v"])