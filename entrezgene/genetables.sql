CREATE TABLE geneinfo (
  tax_id INTEGER,
  gene_id INTEGER,
  symbol TEXT,
  locustag TEXT, 
  synonyms TEXT,
  dbxrefs TEXT,
  chromosome TEXT,
  map_location TEXT,
  description TEXT,
  type_of_gene TEXT,
  nom_symbol TEXT,
  nom_fullname TEXT,
  nom_status TEXT,
  other_des TEXT,
  mod_date TEXT
)

CREATE TABLE gene2acc (
  tax_id INTEGER,
  gene_id INTEGER,
  status TEXT,
  rna_acc TEXT, 
  rna_gi BIGINT,
  protein_acc TEXT,
  protein_gi BIGINT,
  genomic_acc TEXT, 
  genomic_gi BIGINT,
  genomic_start BIGINT, 
  genomic_end BIGINT, 
  orientation char(1),
  assembly TEXT
)

create index genesymbol_i on geneinfo(symbol);
create index geneid_id on geneinfo(gene_id);

