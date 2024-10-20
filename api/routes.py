import datetime
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from typing import Dict, Literal
from utils import get_feature_info, predict_salary
from model import SalaryPredictor
import logging
import asyncio
import os
from health_check import HealthChecker

EducationLevel = Literal[
    "High School",
    "Bachelor's",
    "Master's",
    "PhD",
    "Associate's",
    "Some College",
    "Professional Degree",
    "Other"
]


router = APIRouter()

@router.get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}

@router.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()

        feature_info = get_feature_info()
        if data['job_title'] not in feature_info["job_titles"]:
            raise ValueError(f"Invalid job title. Must be one of: {feature_info['job_titles']}")
        
        if data['education_level'] not in feature_info["education_levels"]:
            raise ValueError(f"Invalid education level. Must be one of: {feature_info['education_levels']}")
        
        if data['gender'] not in feature_info["gender_categories"]:
            raise ValueError(f"Invalid gender. Must be one of: {feature_info['gender_categories']}")
            
        prediction = predict_salary(
            age=data['age'],
            gender=data['gender'],
            education_level=data['education_level'],
            job_title=data['job_title'],
            years_experience=data['years_experience'],
        )

        return {
            "status": "success",
            "predicted_salary": round(prediction, 2),
            "input_data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_with_timeout(cmd: list, timeout: int = 300):
    """Run command with timeout"""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )
        
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        if process:
            try:
                process.terminate()
                await asyncio.sleep(0.1)
                process.kill()
            except:
                pass
        raise

@router.get("/fetch-spark")
async def run_process() -> Dict:
    script_path = os.path.abspath("process.sh")
    output_path = "./data/data.csv"
    
    try:
        health_checker = HealthChecker()
        
        logger.info("Checking service health...")
        if not health_checker.wait_for_services():
            raise HTTPException(
                status_code=503,
                detail="Services not ready. Please try again later."
            )
        
        if not os.path.exists(script_path):
            raise HTTPException(
                status_code=500,
                detail=f"Processing script not found at {script_path}"
            )
        
        os.chmod(script_path, 0o755)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logger.info("Starting Spark processing...")
        returncode, stdout, stderr = await run_with_timeout(
            ["/bin/bash", script_path],
            timeout=300 
        )
        
        if returncode != 0:
            logger.error(f"Process failed: {stderr.decode()}")
            raise HTTPException(
                status_code=500,
                detail=f"Script failed with error: {stderr.decode()}"
            )
        
        for _ in range(30):
            if os.path.exists(output_path):
                break
            await asyncio.sleep(1)
        else:
            raise HTTPException(
                status_code=500,
                detail="Data processing completed but output file not found"
            )
        
        return {
            "status": "success",
            "message": "Data processing completed successfully",
            "output": stdout.decode()
        }
        
    except asyncio.TimeoutError:
        logger.error("Process timed out")
        raise HTTPException(
            status_code=504,
            detail="Processing timed out"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )