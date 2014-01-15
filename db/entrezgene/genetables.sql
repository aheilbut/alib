CREATE TABLE ncbi_geneinfo (
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

CREATE TABLE ncbi_gene2acc (
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

CREATE TABLE generif_intx (
 tax_id_a INTEGER,
 gene_id_a INTEGER,
 pmid text
 tax_id_b INTEGER,
 gene_id_b INTEGER
)

INSERT INTO generif_intx
SELECT a.tax_id, a.gene_id, a.pmid, b.tax_id, b.gene_id
 FROM generifs a INNER JOIN generifs b ON 
 a.pmid = b.pmid AND a.gene_id != b.gene_id 


INSERT INTO intx_count
select iA.symbol, iB.symbol, COUNT(DISTINCT pmid) from generif_intx
 INNER JOIN geneinfo iA ON tax_id_a = iA.tax_id AND gene_id_a = iA.gene_id
 INNER JOIN geneinfo iB ON tax_id_b = iB.tax_id AND gene_id_b = iB.gene_id
 GROUP BY iA.symbol, iB.symbol

\copy ncbi_geneinfo from '/Users/heilbut/alib_data/gene_info.humanmouse.withHeader.tab' WITH DELIMITER '  ' CSV HEADER