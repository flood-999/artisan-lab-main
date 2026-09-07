"""
NIRMAAN - Application Server Launcher
"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    print("=" * 60)
    print("  NIRMAAN - AI-Powered Artisan Catalog & Marketplace")
    print("  Server starting at http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
