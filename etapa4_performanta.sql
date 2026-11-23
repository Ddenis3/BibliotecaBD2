-- =====================================================
-- ETAPA 4 - PERFORMANTA
-- Sistem de Gestionare a unei Biblioteci
-- =====================================================


-- =====================================================
-- 1. CREAREA TABELEI PENTRU TESTAREA PERFORMANTEI
-- =====================================================

DROP TABLE IF EXISTS imprumuturi_perf_test;

CREATE TABLE imprumuturi_perf_test (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cititor_id INTEGER NOT NULL,
    exemplar_id INTEGER NOT NULL,
    data_imprumut DATE NOT NULL,
    data_scadenta DATE NOT NULL,
    status VARCHAR(30) NOT NULL
);


-- =====================================================
-- 2. GENERAREA A 100.000 DE INREGISTRARI
-- =====================================================

INSERT INTO imprumuturi_perf_test (
    cititor_id,
    exemplar_id,
    data_imprumut,
    data_scadenta,
    status
)
SELECT
    (gs % 1000) + 1,
    (gs % 5000) + 1,
    DATE '2020-01-01' + (gs % 2000),
    DATE '2020-01-15' + (gs % 2000),
    CASE
        WHEN gs % 3 = 0 THEN 'returnat'
        WHEN gs % 3 = 1 THEN 'activ'
        ELSE 'intarziat'
    END
FROM generate_series(1, 100000) AS gs;

ANALYZE imprumuturi_perf_test;


-- =====================================================
-- 3. VERIFICAREA NUMARULUI DE INREGISTRARI
-- =====================================================

SELECT COUNT(*) AS total_inregistrari
FROM imprumuturi_perf_test;


-- =====================================================
-- 4. TESTUL 1 - FARA INDEX
-- CAUTAREA IMPRUMUTURILOR DUPA CITITOR
-- =====================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    id,
    cititor_id,
    exemplar_id,
    data_imprumut,
    data_scadenta,
    status
FROM imprumuturi_perf_test
WHERE cititor_id = 500
ORDER BY data_imprumut DESC;


-- =====================================================
-- 5. CREAREA PRIMULUI INDEX COMPUS
-- =====================================================

CREATE INDEX idx_perf_imprumuturi_cititor_data
ON imprumuturi_perf_test (
    cititor_id,
    data_imprumut DESC
);

ANALYZE imprumuturi_perf_test;


-- =====================================================
-- 6. TESTUL 1 - CU INDEX
-- =====================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    id,
    cititor_id,
    exemplar_id,
    data_imprumut,
    data_scadenta,
    status
FROM imprumuturi_perf_test
WHERE cititor_id = 500
ORDER BY data_imprumut DESC;


-- =====================================================
-- 7. TESTUL 2 - FARA INDEX SPECIFIC
-- IMPRUMUTURI ACTIVE DUPA DATA SCADENTEI
-- =====================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    id,
    cititor_id,
    exemplar_id,
    data_imprumut,
    data_scadenta,
    status
FROM imprumuturi_perf_test
WHERE status = 'activ'
  AND data_scadenta BETWEEN
      DATE '2024-01-01'
      AND DATE '2024-01-31'
ORDER BY data_scadenta DESC
LIMIT 30;


-- =====================================================
-- 8. CREAREA INDEXULUI PARTIAL
-- =====================================================

CREATE INDEX idx_perf_imprumuturi_active_scadenta
ON imprumuturi_perf_test (
    data_scadenta DESC
)
WHERE status = 'activ';

ANALYZE imprumuturi_perf_test;


-- =====================================================
-- 9. TESTUL 2 - CU INDEX
-- =====================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    id,
    cititor_id,
    exemplar_id,
    data_imprumut,
    data_scadenta,
    status
FROM imprumuturi_perf_test
WHERE status = 'activ'
  AND data_scadenta BETWEEN
      DATE '2024-01-01'
      AND DATE '2024-01-31'
ORDER BY data_scadenta DESC
LIMIT 30;


-- =====================================================
-- 10. VERIFICAREA INDECSILOR CREATI
-- =====================================================

SELECT
    tablename AS tabel,
    indexname AS nume_index,
    indexdef AS definitie
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'imprumuturi_perf_test'
ORDER BY indexname;


-- =====================================================
-- 11. VERIFICAREA FINALA
-- =====================================================

SELECT
    COUNT(*) AS total_inregistrari,
    COUNT(DISTINCT cititor_id) AS total_cititori,
    COUNT(*) FILTER (
        WHERE status = 'activ'
    ) AS imprumuturi_active
FROM imprumuturi_perf_test;