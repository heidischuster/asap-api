from typing import Generator

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app import schemas
from app.core.config import settings

