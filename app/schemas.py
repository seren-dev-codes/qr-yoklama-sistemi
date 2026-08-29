from pydantic import BaseModel

class YoklamaGuncelle(BaseModel):
    ogrenci_id: int
    durum: bool

    class Config:
        from_attributes = True