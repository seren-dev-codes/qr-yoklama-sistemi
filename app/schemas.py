from pydantic import BaseModel
from typing import List

class YoklamaGuncelle(BaseModel):
    ogrenci_id: int
    durum: bool

    class Config:
        from_attributes = True


class YoklamaKaydetIstek(BaseModel):
    sinif_kodu: str
    liste: List[YoklamaGuncelle]