from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    owner_team = Column(String(100))
    risk_score = Column(Float, default=0.0)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    versions = relationship("ModelVersion", back_populates="parent_model")

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    version_tag = Column(String(50), nullable=False) # e.g. 1.2.0
    artifact_uri = Column(String(500)) # ADLS/S3 Link
    metrics = Column(JSON) # {"accuracy": 0.95, "latency_ms": 12}
    status = Column(String(50), default="experimental") # experimental, approved, deployed, retired
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    parent_model = relationship("Model", back_populates="versions")

class PromptTemplate(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50))
    content = Column(Text, nullable=False)
    parameters = Column(JSON) # Variables like {{user_input}}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ApprovalAudit(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True)
    target_type = Column(String(50)) # model_version or prompt
    target_id = Column(Integer)
    approved_by = Column(String(255))
    environment = Column(String(50)) # prod, staging
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MultiTenantQuota(Base):
    __tablename__ = "quotas"
    id = Column(Integer, primary_key=True)
    tenant_name = Column(String(100), unique=True)
    max_models = Column(Integer, default=50)
    current_models = Column(Integer, default=0)
    storage_limit_gb = Column(Integer, default=500)
