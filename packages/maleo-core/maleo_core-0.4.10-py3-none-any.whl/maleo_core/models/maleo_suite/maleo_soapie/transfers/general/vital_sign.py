from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIEVitalSignGeneralTransfers:
    class Base(BaseModel):
        systole:Optional[int] = Field(None, gt=0, description="Systole")
        diastole:Optional[int] = Field(None, gt=0, description="Diastole")
        temperature:Optional[float] = Field(None, gt=0, description="Temperature")
        respiration_rate:Optional[int] = Field(None, gt=0, description="Respiration Rate")
        heart_rate:Optional[int] = Field(None, gt=0, description="Heart Rate")
        oxygen_saturation:Optional[int] = Field(None, gt=0, description="Oxygen Saturation")
        abdominal_circumference:Optional[float] = Field(None, gt=0, description="Abdominal circumference")
        waist_circumference:Optional[float] = Field(None, gt=0, description="Waist circumference")
        height:Optional[float] = Field(None, gt=0, description="Height")
        weight:Optional[float] = Field(None, gt=0, description="Weight")
        body_mass_index:Optional[float] = Field(None, gt=0, description="Body Mass Index (BMI)")
        organ_examination_detail:Optional[str] = Field(None, description="Organ examination detail")