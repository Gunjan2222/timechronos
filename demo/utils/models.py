from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid, enum

models = Blueprint('models', __name__)

db = SQLAlchemy()

class TimeStamp(object):
    created_date = db.Column(db.Date, default=datetime.now)
    created_time = db.Column(db.TIME, default=datetime.now)
    updated_date = db.Column(db.Date, default=datetime.now, onupdate=datetime.now)
    updated_time = db.Column(db.TIME, default=datetime.now, onupdate=datetime.now)
    created_by = db.Column(db.String, default='app')
    updated_by = db.Column(db.String, default='app')

class DimDate(db.Model):
    __tablename__ = 'dim_date'
    date_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_actual = db.Column(db.Date, nullable=False)
    epoch = db.Column(db.BigInteger, nullable=False)
    day_suffix = db.Column(db.String(4), nullable=False)
    day_name = db.Column(db.String(9), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_quarter = db.Column(db.Integer, nullable=False)
    day_of_year = db.Column(db.Integer, nullable=False)
    week_of_month = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    week_of_year_iso = db.Column(db.String(10), nullable=False)
    month_actual = db.Column(db.Integer, nullable=False)
    month_name = db.Column(db.String(9), nullable=False)
    month_name_abbreviated = db.Column(db.String(3), nullable=False)
    quarter_actual = db.Column(db.Integer, nullable=False)
    quarter_name = db.Column(db.String(9), nullable=False)
    year_actual = db.Column(db.Integer, nullable=False)
    first_day_of_week = db.Column(db.Date, nullable=False)
    last_day_of_week = db.Column(db.Date, nullable=False)
    first_day_of_month = db.Column(db.Date, nullable=False)
    last_day_of_month = db.Column(db.Date, nullable=False)
    first_day_of_quarter = db.Column(db.Date, nullable=False)
    last_day_of_quarter = db.Column(db.Date, nullable=False)
    first_day_of_year = db.Column(db.Date, nullable=False)
    last_day_of_year = db.Column(db.Date, nullable=False)
    mmyyyy = db.Column(db.String(6), nullable=False)
    mmddyyyy = db.Column(db.String(10), nullable=False)
    weekend_indr = db.Column(db.Boolean, nullable=False)

class Company(db.Model, TimeStamp):
    __tablename__ = 'company'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)

    users = db.relationship('User', backref='company', cascade="all, delete-orphan", passive_deletes=True)
    clients = db.relationship('Client', backref='company', cascade="all, delete-orphan", passive_deletes=True)

class User(db.Model, TimeStamp):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10))
    gender = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(255))
    password = db.Column(db.String)
    profile_photo_url = db.Column(db.String())
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)
    supervisor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="SET NULL"))
    approver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="SET NULL"))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)

    supervisor = db.relationship('User', remote_side=[id], backref='subordinates', foreign_keys=[supervisor_id])
    approver = db.relationship('User', remote_side=[id], backref='approvables', foreign_keys=[approver_id])
    timesheets = db.relationship('Timesheet', backref='user', cascade="all, delete-orphan", passive_deletes=True)

class Client(db.Model, TimeStamp):
    __tablename__ = 'client'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

    projects = db.relationship('Project', backref='client', cascade="all, delete-orphan", passive_deletes=True)

class Project(db.Model, TimeStamp):            
    __tablename__ = 'project'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    estimated_hours = db.Column(db.Integer)
    estimated_cost = db.Column(db.Integer)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id', ondelete="CASCADE"), nullable=False)

    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan", passive_deletes=True)

class BillableType(enum.Enum):
    BILLABLE = "Billable"
    NON_BILLABLE = "Non-Billable"
    BOTH = "Both"

class Task(db.Model, TimeStamp):
    __tablename__ = 'task'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.id', ondelete="CASCADE"), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    billable_type = db.Column(db.Enum(BillableType), default= BillableType.BILLABLE)

    taskhours = db.relationship('TaskHours', backref='task', cascade="all, delete-orphan", passive_deletes=True)

class Approval(enum.Enum): 
    PENDING = "PENDING"
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RECALLED = "RECALLED"

class Timesheet(db.Model, TimeStamp):
    __tablename__ = 'timesheet'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    approval = db.Column(db.Enum(Approval), default=Approval.DRAFT)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    taskhours = db.relationship('TaskHours', backref='timesheet', cascade="all, delete-orphan", passive_deletes=True)

class TaskHours(db.Model, TimeStamp):
    __tablename__ = 'taskhours'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    values = db.Column(db.ARRAY(db.Integer), nullable=False, default=lambda: [0] * 7)
    comments = db.Column(db.ARRAY(db.String(255)), default=lambda: [''] * 7)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.id', ondelete="CASCADE"), nullable=False)
    billable_type = db.Column(db.Enum(BillableType), default= BillableType.BILLABLE)
    timesheet_id = db.Column(UUID(as_uuid=True), db.ForeignKey('timesheet.id', ondelete="CASCADE"), nullable=False)
    
class HistoryLogger(db.Model, TimeStamp):
    __tablename__ = 'history_logger'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(UUID(as_uuid=True), nullable=False)
    operation = db.Column(db.String(50), nullable=False)
    old_data = db.Column(db.JSON) 
    new_data = db.Column(db.JSON) 
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True) 

class BlacklistToken(db.Model, TimeStamp):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    jti = db.Column(db.String(100), nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Token(db.Model, TimeStamp):
    __tablename__ = 'token'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    token_date = db.Column(db.DateTime(), nullable=False, default=datetime.now)

