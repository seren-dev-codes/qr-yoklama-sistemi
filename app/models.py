from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Sinif(Base):
    __tablename__ = "siniflar"
    id = Column(Integer, primary_key=True, index=True)
    kod = Column(String, unique=True, index=True)

    ogrenciler = relationship("Ogrenci", back_populates="sinif")


class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    id = Column(Integer, primary_key=True, index=True)
    okul_no = Column(String, unique=True, index=True)
    ad_soyad = Column(String)
    veli_tel = Column(String, nullable=True)
    sinif_id = Column(Integer, ForeignKey("siniflar.id"))

    sinif = relationship("Sinif", back_populates="ogrenciler")
    yoklamalar = relationship("Yoklama", back_populates="ogrenci")


class Yoklama(Base):
    __tablename__ = "yoklamalar"
    id = Column(Integer, primary_key=True, index=True)
    ogrenci_id = Column(Integer, ForeignKey("ogrenciler.id"))
    tarih = Column(DateTime, default=utcnow)
    durum = Column(Boolean, default=False)

    ogrenci = relationship("Ogrenci", back_populates="yoklamalar")
