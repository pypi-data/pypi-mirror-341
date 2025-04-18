# !/usr/bin/python
# -*- coding: utf-8 -*-
from model.base_model import BaseModel
from abc import abstractmethod
from datetime import datetime

class ScheduleModel(BaseModel):
    """
    @NotNull=active,frequency,start_at,start_hour
    @Timestamp=start_at,next_execution
    """
    id = None
    active = None
    frequency = None
    month_days = None
    next_execution = None
    start_at = None
    start_hour = None
    week_days = None
    year_days = None
    job_id = None
    schemas = None
    action_type = None
    repeat_every = None
    place = None
    
    @property
    def serialize(self):
        return {
           'id': self.id,
           'active': self.active,
           'frequency': self.frequency,
           'month_days': self.month_days,
           'next_execution': self.next_execution,
           'start_at': self.start_at,
           'start_hour': self.start_hour,
           'week_days': self.week_days,
           'year_days': self.year_days,
           'job_id': self.job_id,
           'schemas': self.schemas,
           'action_type': self.action_type,
           'repeat_every': self.repeat_every,
           'place': self.place
        }
    
    # @property
    def to_string(self):
        frequency_map = {0: "Diario", 1: "Semanal", 2: "Mensal"}
        type_map = {0: "Backup", 1: "Atualiza DEV"}
        freq = frequency_map.get(self.frequency, "Valor inválido")
        type = type_map.get(self.action_type, "Valor inválido")
        date_str = self.start_at.strftime("%d-%m-%Y")
        active = "True" if self.active == 1 else "False"
        # return f" {self.id} |   {active}    |   {freq} |   {str(self.start_at).split()[0]}  |   {self.start_hour}"
        return f" {self.id:<5} | {active:<8} | {freq:<12} | {type:<12} | {self.start_hour:<5} | {self.schemas:<12} "
    # return f" {self.id:<5} | {active:<8} | {freq:<12} | {str(self.start_at).split()[0]:<12} | {self.start_hour:<14} "
    