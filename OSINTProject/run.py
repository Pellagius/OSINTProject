if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.backend.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=False,
        reload_dirs=["src/"]
    )