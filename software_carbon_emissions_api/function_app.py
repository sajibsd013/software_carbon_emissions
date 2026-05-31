import azure.functions as func
from app.main import app 

azure_app = func.AsgiFunctionApp(
    app=app, 
    http_auth_level=func.AuthLevel.ANONYMOUS,
    route_prefix=""
)
