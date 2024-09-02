import sys
import logging
from datetime import datetime
import asyncio

async def verify_aiohttp(aiohttp):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com') as response:
            return response.status

def verify_libraries():
    logging.info("Verifying installed libraries...")

    libraries = [
        ("NumPy", "numpy", lambda numpy: numpy.array([1, 2, 3, 4, 5])),
        ("Pandas", "pandas", lambda pandas: pandas.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})),
        ("Requests", "requests", lambda requests: requests.get("https://api.github.com").status_code),
        ("PyYAML", "yaml", lambda yaml: yaml.safe_load("key: value")),
        ("Celery", "celery", lambda celery: celery.__version__),
        ("Redis", "redis", lambda redis: redis.Redis()),
        ("SQLAlchemy", "sqlalchemy", lambda sqlalchemy: sqlalchemy.create_engine("sqlite:///:memory:")),
        ("FastAPI", "fastapi", lambda fastapi: fastapi.FastAPI()),
        ("Uvicorn", "uvicorn", lambda uvicorn: uvicorn.__version__),
        ("Pydantic", "pydantic", lambda pydantic: pydantic.BaseModel),
        ("AIOHTTP", "aiohttp", lambda aiohttp: asyncio.get_event_loop().run_until_complete(verify_aiohttp(aiohttp)))
    ]

    for lib_name, lib_import, lib_test in libraries:
        try:
            module = __import__(lib_import)
            lib_test(module)
            logging.info(f"{lib_name}: Successfully imported and tested.")
        except ImportError as e:
            logging.error(f"{lib_name} import failed: {e}")
        except Exception as e:
            logging.error(f"{lib_name} verification failed: {e}")

    logging.info("Library verification complete.")

if __name__ == "__main__":
    # Set up logging
    log_filename = 'library_verification.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')

    logging.info(f"Starting library verification at {datetime.now()}")
    
    verify_libraries()
    
    logging.info(f"Finished library verification at {datetime.now()}")

    print(f"Verification complete. Check {log_filename} for details.")