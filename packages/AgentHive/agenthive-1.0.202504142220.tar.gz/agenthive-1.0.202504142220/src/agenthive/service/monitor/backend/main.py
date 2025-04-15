"""
Monitor Server.

This version of the Monitor service focuses on:
1. Providing a Web interface
2. Retrieving information from the database
3. Interacting with the Coordinator API
"""
import os
import logging
import asyncio
import json
import time
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Query, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from agenthive.db.adapters.base import BaseDBAdapter
from agenthive.db.adapters.sqlalchemy import SQLAlchemyAdapter  # Use the concrete adapter
from agenthive.version import __version__

try:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
except ValueError:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.warning(f"Invalid log level '{os.environ.get("LOG_LEVEL", "INFO").upper()}', defaulting to INFO")
else:
    logger = logging.getLogger(__name__)

# Templates directory (HTML templates)
templates = Jinja2Templates(directory="src/agenthive/service/monitor/backend/templates")

# Global database adapter
db_adapter = None
worker_timeout = 120

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler.
    Handles application startup and shutdown events.
    """
    global db_adapter, worker_timeout

    worker_timeout = int(os.environ.get("WORKER_TIMEOUT", "120"))
    
    # Code executed at startup
    # Get database connection string
    db_url = os.environ.get("DATABASE_URL")
    
    # If a database URL is provided, initialize the database connection
    if db_url:
        try:
            # Create adapter using heartbeat db_adapters
            db_adapter = SQLAlchemyAdapter(db_url)
            await db_adapter.connect()
            logger.debug(f"Database connection initialized: {db_url}")
        except Exception as e:
            logger.error(f"Database connection initialization failed: {e}")
            db_adapter = None
    else:
        logger.warning("No database URL provided. Monitor will not be able to display data from the database")
    
    logger.info("Monitor server started")
    
    # Pause here, wait for the application to execute
    yield
    
    # Code executed at shutdown
    if db_adapter:
        await db_adapter.close()
        logger.debug("Database connection closed")
    
    logger.info("Monitor server stopped")

app = FastAPI(
    title="AgentHive Monitor",
    description="Monitoring interface for the AgentHive distributed system",
    version=__version__,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
app.mount("/static", StaticFiles(directory="src/agenthive/service/monitor/frontend/dist/static"), name="static")

# Get coordinator URL
def get_coordinator_url():
    return os.environ.get("COORDINATOR_URL", "http://localhost:8000")

# Dependency for database adapter
async def get_db_adapter():
    if db_adapter is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    return db_adapter

# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "database_connected": db_adapter is not None}

@app.get("/")
async def index(request: Request):
    """Serve the main dashboard page"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "AgentHive Monitor"}
    )

@app.get("/api/dashboard")
async def get_dashboard_data(db = Depends(get_db_adapter)):
    """
    Get consolidated dashboard data including system status, worker stats, task stats,
    and resource usage - all in a single API call.
    
    This reduces multiple API calls to a single request for the main dashboard view.
    """
    coordinator_url = get_coordinator_url()
    
    try:
        # Prepare the comprehensive response
        dashboard_data = {
            "timestamp": time.time(),
            "system": {
                "status": "unknown",
                "uptime": "unknown",
                "uptime_seconds": 0
            },
            "workers": {
                "total": 0,
                "active": 0,
                "idle": 0,
                "busy": 0
            },
            "tasks": {
                "total": 0,
                "pending": 0,
                "assigned": 0,
                "completed": 0,
                "failed": 0,
                "throughput": 0
            },
            "resources": {
                "cpu": 0,
                "memory": 0,
                "disk": 0
            }
        }

        # Try to get data from coordinator
        async with httpx.AsyncClient() as client:
            try:
                # First try the overview endpoint
                overview_response = await client.get(f"{coordinator_url}/api/metrics/overview", timeout=2.0)
                if overview_response.status_code == 200:
                    overview_data = overview_response.json()
                    
                    # Extract data from overview
                    if "coordinator" in overview_data:
                        dashboard_data["system"]["status"] = "active"
                        if "start_time" in overview_data["coordinator"]:
                            uptime_seconds = time.time() - overview_data["coordinator"]["start_time"]
                            dashboard_data["system"]["uptime_seconds"] = uptime_seconds
                            dashboard_data["system"]["uptime"] = format_uptime(uptime_seconds)
                        
                        if "throughput" in overview_data["coordinator"]:
                            dashboard_data["tasks"]["throughput"] = overview_data["coordinator"]["throughput"]
                            
                        if "supported_task_types" in overview_data["coordinator"]:
                            dashboard_data["system"]["supported_task_types"] = overview_data["coordinator"]["supported_task_types"]
                    
                    if "workers" in overview_data:
                        workers_data = overview_data["workers"]
                        for key in ["active", "idle", "busy", "details"]:
                            if key in workers_data:
                                dashboard_data["workers"][key] = workers_data[key]
                        dashboard_data["workers"]["total"] = sum(
                            [workers_data.get(key, 0) for key in ["active", "idle", "busy"]]
                        )
                    
                    if "tasks" in overview_data:
                        tasks_data = overview_data["tasks"]
                        for key in ["pending", "assigned", "completed", "failed", "total", "details",]:
                            if key in tasks_data:
                                dashboard_data["tasks"][key] = tasks_data[key]
                    
                    if "resource_usage" in overview_data:
                        resource_data = overview_data["resource_usage"]
                        if "cpu" in resource_data and "percent" in resource_data["cpu"]:
                            dashboard_data["resources"]["cpu"] = resource_data["cpu"]["percent"]
                        if "memory" in resource_data and "percent" in resource_data["memory"]:
                            dashboard_data["resources"]["memory"] = resource_data["memory"]["percent"]
                        if "disk" in resource_data and "percent" in resource_data["disk"]:
                            dashboard_data["resources"]["disk"] = resource_data["disk"]["percent"]

            except (httpx.RequestError, asyncio.TimeoutError):
                logger.warning("Could not connect to coordinator for overview data")
            
            # If we still need worker data
            if dashboard_data["workers"]["total"] == 0:
                try:
                    workers_response = await client.get(f"{coordinator_url}/api/workers", timeout=2.0)
                    if workers_response.status_code == 200:
                        workers_data = workers_response.json()
                        dashboard_data["workers"]["total"] = len(workers_data.get("workers", []))
                        
                        # Count workers by status
                        statuses = [w.get("status", "unknown") for w in workers_data.get("workers", [])]
                        dashboard_data["workers"]["idle"] = statuses.count("idle")
                        dashboard_data["workers"]["busy"] = statuses.count("busy")
                        dashboard_data["workers"]["active"] = dashboard_data["workers"]["total"]
                except (httpx.RequestError, asyncio.TimeoutError):
                    logger.warning("Could not connect to coordinator for workers data")
        
        # If we couldn't get data from coordinator, try the database if available
        if db and dashboard_data["workers"]["total"] == 0:
            try:
                workers = await db.get_active_workers()
                dashboard_data["workers"]["total"] = len(workers)
                
                # Count workers by status
                statuses = [w.get("status", "unknown") for w in workers]
                dashboard_data["workers"]["idle"] = statuses.count("idle")
                dashboard_data["workers"]["busy"] = statuses.count("busy")
                dashboard_data["workers"]["active"] = dashboard_data["workers"]["total"]
            except Exception as e:
                logger.error(f"Error getting workers from database: {e}")
        
        # Add local resource metrics if we couldn't get from coordinator
        if dashboard_data["resources"]["cpu"] == 0:
            try:
                from agenthive.utils.health import get_system_metrics
                metrics = get_system_metrics()
                dashboard_data["resources"]["cpu"] = metrics.get("cpu", {}).get("percent", 0)
                dashboard_data["resources"]["memory"] = metrics.get("memory", {}).get("percent", 0)
                dashboard_data["resources"]["disk"] = metrics.get("disk", {}).get("percent", 0)
            except Exception as e:
                logger.error(f"Error getting local system metrics: {e}")
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return {
            "timestamp": time.time(),
            "error": str(e),
            "system": {"status": "error"},
            "workers": {"total": 0},
            "tasks": {"total": 0},
            "resources": {}
        }

@app.get("/api/worker/summary")
async def get_worker_summary(
    worker_id: Optional[str] = Query(None, description="Query worker status"),
):
    output = { "status": False, "error": None, "worker_id": worker_id, "data": {} }
    try:
        coordinator_url = get_coordinator_url()
        url = f"{coordinator_url}/api/workers/status"
        params = {}
        
        if worker_id:
            params["worker_ids"] = worker_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                full_data = response.json()
            
                return full_data
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except httpx.RequestError as e:
        logger.error(f"Error connecting to coordinator: {e}")
        output["error"] = f"Error connecting to coordinator: {e}"
    
    except Exception as e:
        logger.error(f"Error getting worker summary: {e}")
        output["error"] = f"Error getting worker summary: {e}"

    return output

@app.get("/api/task/summary")
async def get_task_summary(
    task_id: Optional[str] = Query(None, description="Query task_id status"),
):
    output = { "status": False, "error": None, "task_id": task_id, "data": {} }
    try:
        coordinator_url = get_coordinator_url()
        url = f"{coordinator_url}/api/tasks/status"
        params = {}
        
        if task_id:
            params["task_ids"] = task_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                full_data = response.json()
                return full_data
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except httpx.RequestError as e:
        logger.error(f"Error connecting to coordinator: {e}")
        output["error"] = f"Error connecting to coordinator: {e}"
    
    except Exception as e:
        logger.error(f"Error getting worker summary: {e}")
        output["error"] = f"Error getting worker summary: {e}"

    return output

@app.post("/api/tasks/quick-create")
async def quick_create_task(
    task_type: str = Body(..., embed=True),
    priority: int = Body(0, embed=True),
    data: Dict[str, Any] = Body({}, embed=True)
):
    """
    Simplified task creation endpoint that combines all parameters in a single call
    rather than as separate query parameters.
    """
    coordinator_url = get_coordinator_url()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{coordinator_url}/api/tasks/submit",
                json={
                    "task_type": task_type,
                    "priority": priority,
                    "data": data
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except httpx.RequestError as e:
        logger.error(f"Error connecting to coordinator: {e}")
        raise HTTPException(status_code=503, detail="Could not connect to coordinator")
    
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
def format_uptime(seconds: float) -> str:
    """Format uptime in seconds to a human-readable string."""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{int(days)}d")
    if hours > 0 or days > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{int(minutes)}m")
    parts.append(f"{int(seconds)}s")
    
    return " ".join(parts)

# Routes for handling static files and root page
@app.get("/{path:path}")
async def serve_static_files(path: str):
    """Serve static files or return the main page for SPA routing"""
    # Check static files directory
    static_file_path = f"src/agenthive/service/monitor/frontend/dist/{path}"
    if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
        return FileResponse(static_file_path)
    
    # Return main page (SPA routing)
    return FileResponse("src/agenthive/service/monitor/frontend/dist/static/index.html")

# Run server (if this module is executed directly)
if __name__ == "__main__":
    import uvicorn
    
    # Get host and port
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    
    # Run server
    uvicorn.run(app, host=host, port=port)
