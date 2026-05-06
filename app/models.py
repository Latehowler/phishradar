"""
Database models for Phishing Detection System
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = "users"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(120), nullable=False)
    email             = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash     = db.Column(db.String(256), nullable=False)
    role              = db.Column(db.String(20), nullable=False, default="user")      # admin | moderator | user
    status            = db.Column(db.String(20), nullable=False, default="active")   # active | inactive | suspended
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    # ── password helpers ──────────────────────────────────────────────────────
    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    # ── convenience properties ──────────────────────────────────────────────────────
    @property
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == "admin"

    @property
    def is_active_user(self) -> bool:
        """Check if user is active"""
        return self.status == "active"

    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "role":       self.role,
            "status":     self.status,
            "created_at": self.created_at.strftime("%b %d, %Y") if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"


class PhishingReport(db.Model):
    """Model for user-submitted phishing reports"""
    __tablename__ = "phishing_reports"

    id                = db.Column(db.Integer, primary_key=True)
    url               = db.Column(db.String(2048), nullable=False)
    email             = db.Column(db.String(254), nullable=True, index=True)
    name              = db.Column(db.String(120), nullable=True)
    threat_type       = db.Column(db.String(50), nullable=False)
    severity          = db.Column(db.String(20), nullable=False)
    details           = db.Column(db.Text, nullable=True)
    flags             = db.Column(db.Text, nullable=True)  # JSON array
    status            = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True
    )  # pending | reviewed | confirmed | false_positive
    created_at        = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reviewed_by       = db.Column(db.String(254), nullable=True)
    reviewed_at       = db.Column(db.DateTime, nullable=True)

    # ── methods ────────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        """Convert report to dictionary"""
        return {
            "id":          self.id,
            "url":         self.url,
            "email":       self.email,
            "name":        self.name,
            "threat_type": self.threat_type,
            "severity":    self.severity,
            "details":     self.details,
            "flags":       json.loads(self.flags) if self.flags else [],
            "status":      self.status,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
        }

    def __repr__(self) -> str:
        return f"<PhishingReport {self.url} ({self.status})>"
