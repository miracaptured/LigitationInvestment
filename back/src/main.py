from api.app import app

import uvicorn
uvicorn.run("api.app:app", host='0.0.0.0', port=8000, log_level="debug")



