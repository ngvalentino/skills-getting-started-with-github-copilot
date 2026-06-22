from fastapi.testclient import TestClient
from src.app import app, activities
import copy

original_activities = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture(autouse=True)
def restore_activities():
    reset_activities()
    yield
    reset_activities()


@pytest.fixture
def client():
    return TestClient(app)
