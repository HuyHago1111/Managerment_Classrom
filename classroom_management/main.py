import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from classroom_management.database import engine, Base
from classroom_management.seed import seed_database
from classroom_management.routers import auth_router, admin_router, teacher_router, student_router

# Create DB Tables & Seed Data
Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print(f"Seed info: {e}")

def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title="Hệ Thống Quản Lý Lớp Học - Enterprise Python",
        description="Dự án Python 3 tầng Quản lý lớp học phân quyền Giáo viên, Sinh viên, Admin",
        version="1.0.0"
    )

    # Register API Routers
    app.include_router(auth_router.router)
    app.include_router(admin_router.router)
    app.include_router(teacher_router.router)
    app.include_router(student_router.router)

    # Mount Static Directory
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    def read_root():
        """Render single page dashboard interface."""
        index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)

    return app

app = create_app()
