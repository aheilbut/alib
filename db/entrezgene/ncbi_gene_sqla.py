import sqlalchemy

from sqlalchemy import Table, Column, Integer, String, Date, BigInteger, DateTime, Boolean, MetaData, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref

from entrezgene_base import Base

class NCBIGeneInfo(Base):
    __tablename__ = 'ncbi_geneinfo'

    gene_id = Column("gene_id", Integer, primary_key=True)
    tax_id = Column("tax_id", Integer)
    symbol = Column("symbol", String)
    locustag = Column("locustag", String)
    synonyms = Column("synonyms", String)
    dbxrefs = Column("dbxrefs", String)
    chromosome = Column("chromosome", String)
    map_location = Column("map_location", String)
    description = Column("description", String)
    type_of_gene = Column("type_of_gene", String)
    nom_symbol = Column("nom_symbol", String)
    nom_fullname = Column("nom_fullname", String)
    nom_status = Column("nom_status", String)
    other_des = Column("other_des", String)
    mod_date = Column("mod_date", String)