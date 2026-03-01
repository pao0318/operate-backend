# Operate DB - Database Schema and Data

This document contains the DDL (Data Definition Language) statements and INSERT statements for all tables in the `operate_db` PostgreSQL database.

**Database:** `operate_db`  
**Generated:** March 1, 2026  
**Total Tables:** 15

---

## Table of Contents

1. [alembic_version](#1-alembic_version)
2. [available_services](#2-available_services)
3. [cases](#3-cases)
4. [covenant_status](#4-covenant_status)
5. [datasimulator_benefits](#5-datasimulator_benefits)
6. [detailed_findings_operational](#6-detailed_findings_operational)
7. [detailed_findings_y14](#7-detailed_findings_y14)
8. [documents](#8-documents)
9. [extracted_key_metrics](#9-extracted_key_metrics)
10. [fr_y14_schedule_template_data_points](#10-fr_y14_schedule_template_data_points)
11. [fr_y14_schedule_template_data_point_details](#11-fr_y14_schedule_template_data_point_details)
12. [q3_highlights](#12-q3_highlights)
13. [quarter_by_quarter_financial_drivers](#13-quarter_by_quarter_financial_drivers)
14. [quarterly_dscr](#14-quarterly_dscr)
15. [shipment_details](#15-shipment_details)

---

## 1. alembic_version

### DDL

```sql
CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
```

### INSERT Statements

```sql
INSERT INTO public.alembic_version VALUES ('001');
```

---

## 2. available_services

### DDL

```sql
CREATE TABLE public.available_services (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(1000),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE SEQUENCE public.available_services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.available_services_id_seq OWNED BY public.available_services.id;

ALTER TABLE ONLY public.available_services ALTER COLUMN id SET DEFAULT nextval('public.available_services_id_seq'::regclass);

ALTER TABLE ONLY public.available_services
    ADD CONSTRAINT available_services_pkey PRIMARY KEY (id);
```

### INSERT Statements

```sql
INSERT INTO public.available_services VALUES (1, 'Loan Agreement', 'Manage and track loan agreements, terms, and conditions', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (2, 'Covenant Register', 'Monitor and manage loan covenants and compliance requirements', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (3, 'FR Y-14 Reporting', 'Federal Reserve Y-14 regulatory reporting and submissions', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (4, 'Financials & ESG Reports', 'Financial statements and Environmental, Social, and Governance reports', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (5, 'KYC/AML file', 'Know Your Customer and Anti-Money Laundering documentation and verification', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (6, 'Risk Dashboard', 'Comprehensive risk monitoring and analytics dashboard', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (7, 'Client Communication', 'Client communication portal and messaging system', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');
INSERT INTO public.available_services VALUES (8, 'Blockchain ledger', 'Distributed ledger technology for transaction tracking and verification', '2026-03-01 11:46:53.296349+05:30', '2026-03-01 11:46:53.296349+05:30');

-- Reset sequence
SELECT pg_catalog.setval('public.available_services_id_seq', 8, true);
```

---

## 3. cases

### DDL

```sql
CREATE TABLE public.cases (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(1000),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    case_no character varying(255) DEFAULT ''::character varying NOT NULL,
    applied_by character varying(255)
);

CREATE SEQUENCE public.cases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.cases_id_seq OWNED BY public.cases.id;

ALTER TABLE ONLY public.cases ALTER COLUMN id SET DEFAULT nextval('public.cases_id_seq'::regclass);

ALTER TABLE ONLY public.cases
    ADD CONSTRAINT cases_pkey PRIMARY KEY (id);
```

### INSERT Statements

```sql
INSERT INTO public.cases VALUES (1, 'Vertex Logistics Corp - $18M Working Capital Facility', 'Working capital facility for Vertex Logistics Corp with $18 million credit line', '2026-03-01 11:48:05.993756+05:30', '2026-03-01 11:48:05.993756+05:30', '', NULL);

-- Reset sequence
SELECT pg_catalog.setval('public.cases_id_seq', 1, true);
```

---

## 4. covenant_status

### DDL

```sql
CREATE TABLE public.covenant_status (
    case_id integer NOT NULL,
    name character varying(255),
    label character varying(255),
    value character varying(500),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL,
    indicator character varying,
    status character varying
);

CREATE SEQUENCE public.covenant_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.covenant_status_id_seq OWNED BY public.covenant_status.id;

ALTER TABLE ONLY public.covenant_status ALTER COLUMN id SET DEFAULT nextval('public.covenant_status_id_seq'::regclass);

ALTER TABLE ONLY public.covenant_status
    ADD CONSTRAINT covenant_status_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.covenant_status
    ADD CONSTRAINT covenant_status_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.covenant_status VALUES (1, 'DSCR', 'DSCR', '1.10(Below 1.25 Covenant)', '2026-03-01 12:47:03.956015+05:30', '2026-03-01 12:47:03.956015+05:30', 6, 'Alert', 'alert');
INSERT INTO public.covenant_status VALUES (1, 'Debt/Equity', 'Debt/Equity', '3.2x(Above 3.0 Threshold)', '2026-03-01 12:47:03.956015+05:30', '2026-03-01 12:47:03.956015+05:30', 7, 'Warning', 'warning');
INSERT INTO public.covenant_status VALUES (1, 'Current Ratio', 'Current Ratio', '12.3(Unusually high vs. 1.5–2.0 industry norm)', '2026-03-01 12:47:03.956015+05:30', '2026-03-01 12:47:03.956015+05:30', 8, 'Alert', 'alert');

-- Reset sequence
SELECT pg_catalog.setval('public.covenant_status_id_seq', 8, true);
```

---

## 5. datasimulator_benefits

### DDL

```sql
CREATE TABLE public.datasimulator_benefits (
    case_id integer NOT NULL,
    data jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

ALTER TABLE ONLY public.datasimulator_benefits
    ADD CONSTRAINT datasimulator_benefits_pkey PRIMARY KEY (case_id);

ALTER TABLE ONLY public.datasimulator_benefits
    ADD CONSTRAINT datasimulator_benefits_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.datasimulator_benefits VALUES (1, '{"speed": {"now": {"label": "Now (with AI)", "value": "30 Minutes"}, "title": "Before/After Impact Timeline", "earlier": {"label": "Earlier (Without AI Integration)", "value": "3 Days"}}, "accuracy": {"title": "Accuracy (OCR/NLP Error Reduction Metrics)", "metrics": [{"items": ["Global Logistics Provider secured 65% faster Covenant Checks.", "XYZ Company secured 35% faster Covenant Checks."], "title": "Faster Covenant Checks"}, {"items": ["Global Logistics Provider, reduced 40% error in processing.", "XYZ Company, reduced 40% error in processing."], "title": "Fewer Errors"}]}, "offerings": ["AI-Powered Document Processing", "Real-time Covenant Monitoring", "Automated Compliance Checks"], "compliance": {"title": "Compliance", "missedBreaches": [{"type": "Covenant Breach", "label": "DEBT RATIO EXCEEDED"}, {"type": "Reporting Deadline", "label": "MISSED BY 3 DAYS"}, {"type": "Document Verification", "label": "INCOMPLETE"}], "proactiveAlerts": [{"company": "XYZ Holdings (Offshore)", "category": "Transport Incident", "description": "Temporal Routing Path Rerouted through unknown server node (Hong Kong)"}, {"category": "Biometrics Mold Data", "description": "Mismatch - Integrity violated"}]}}', '2026-03-01 14:10:34.682189+05:30', '2026-03-01 14:10:34.682189+05:30');
```

---

## 6. detailed_findings_operational

### DDL

```sql
CREATE TABLE public.detailed_findings_operational (
    id integer NOT NULL,
    data jsonb,
    case_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE SEQUENCE public.detailed_findings_operational_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.detailed_findings_operational_id_seq OWNED BY public.detailed_findings_operational.id;

ALTER TABLE ONLY public.detailed_findings_operational ALTER COLUMN id SET DEFAULT nextval('public.detailed_findings_operational_id_seq'::regclass);

ALTER TABLE ONLY public.detailed_findings_operational
    ADD CONSTRAINT detailed_findings_operational_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.detailed_findings_operational
    ADD CONSTRAINT detailed_findings_operational_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.detailed_findings_operational VALUES (1, '{"warningMessage": "Operational metrics require attention for performance optimization", "detailedFindings": [{"docName": "On-Time Delivery (OTIF) Impact", "usedFor": "Analyze root cause: late pickups, route inefficiency, or carrier performance", "description": "Tracking OTIF dropped to 91%, missing covenant threshold"}, {"docName": "Promised vs Delivered Variance", "usedFor": "Standardize lead time estimates and improve forecasting accuracy", "description": "Delivery lead times vary ±60% (2-10 days), impacting cash flow"}, {"docName": "Cost Per Mile / Unit Cost Pressure", "usedFor": "Identify cost drivers: fuel, labor, maintenance, or route optimization gaps", "description": "Analyze cost per mile vs 8.5 p/mi, understand if cost pressure exists"}, {"docName": "Capacity Utilization Decline", "usedFor": "Review load planning and asset allocation to improve utilization rates", "description": "Flagging utilization at 78%, impacting fixed cost absorption"}, {"docName": "OTIF Gap/Time to Fulfil", "usedFor": "Monitor performance trends and identify improvement opportunities", "description": "Tracking OTIF at 91% (Above 90%)"}]}', 1, '2026-03-01 14:07:27.450088+05:30', '2026-03-01 14:07:27.450088+05:30');

-- Reset sequence
SELECT pg_catalog.setval('public.detailed_findings_operational_id_seq', 1, true);
```

---

## 7. detailed_findings_y14

### DDL

```sql
CREATE TABLE public.detailed_findings_y14 (
    case_id integer NOT NULL,
    data jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

ALTER TABLE ONLY public.detailed_findings_y14
    ADD CONSTRAINT detailed_findings_y14_pkey PRIMARY KEY (case_id);

ALTER TABLE ONLY public.detailed_findings_y14
    ADD CONSTRAINT detailed_findings_y14_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.detailed_findings_y14 VALUES (1, '{"warningMessage": "Some documents require attention for Y-14 compliance", "detailedFindings": [{"docName": "Finance_Operations_Q2.xlsx", "usedFor": "DSCR calculation (EBITDA ÷ Debt Service)", "description": "Cash Flow Statement (Operating Activities)"}, {"docName": "Loan_Agreement.pdf", "usedFor": "Covenant threshold: DSCR ≥ 1.25", "description": "Financial Covenant Schedule"}, {"docName": "Covenant_Compliance_Certificate_Q2.pdf", "usedFor": "Y-14Q Schedule H.1 - Covenant Status", "description": "Borrower attestation & covenant reporting"}, {"docName": "Borrower_Financials_Q2_Reviewed.pdf", "usedFor": "Covenant threshold: DSCR ≥ 1.25", "description": "Financial Covenant Schedule"}]}', '2026-03-01 13:21:05.755084+05:30', '2026-03-01 13:21:51.465695+05:30');
```

---

## 8. documents

### DDL

```sql
CREATE TABLE public.documents (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    url character varying(500),
    description character varying(1000),
    type character varying(100),
    filename character varying(255),
    case_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);

CREATE INDEX ix_documents_case_id ON public.documents USING btree (case_id);

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.documents VALUES (1, 'Loan Agreement', NULL, 'Primary loan agreement document outlining terms and conditions', 'pdf', 'Loan_Agreement.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (2, 'Financial Statement', NULL, 'Company financial statements and performance metrics', 'pdf', 'Financial_Statement.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (3, 'Covenant Summary', NULL, 'Summary of loan covenants and compliance tracking', 'xlsx', 'Covenant_Summary.xlsx', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (4, 'ESG Report 02', NULL, 'Environmental, Social, and Governance report', 'pdf', 'ESG_Report_02.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (5, 'FR Y-14 Analysis', NULL, 'Federal Reserve Y-14 regulatory analysis and reporting', 'pdf', 'FR_Y_14_Analysis.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (6, 'Risk Assessment', NULL, 'Comprehensive risk assessment document', 'docx', 'Risk_Assessment.docx', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (7, 'Balance Sheet', NULL, 'Company balance sheet and financial position', 'xlsx', 'Balance_Sheet.xlsx', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (8, 'Quarterly Report', NULL, 'Quarterly financial and operational report', 'pdf', 'Quarterly_Report.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (9, 'Compliance Certificate', NULL, 'Compliance certification and regulatory documentation', 'pdf', 'Compliance_Certificate.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (10, 'Market Analysis', NULL, 'Market analysis and industry trends presentation', 'pptx', 'Market_Analysis.pptx', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (11, 'Credit Approval', NULL, 'Credit approval documentation and decision rationale', 'pdf', 'Credit_Approval.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');
INSERT INTO public.documents VALUES (12, 'Facility Agreement', NULL, 'Facility agreement terms and conditions', 'pdf', 'Facility_Agreement.pdf', 1, '2026-03-01 11:55:09.378113+05:30', '2026-03-01 11:55:09.378113+05:30');

-- Reset sequence
SELECT pg_catalog.setval('public.documents_id_seq', 12, true);
```

---

## 9. extracted_key_metrics

### DDL

```sql
CREATE TABLE public.extracted_key_metrics (
    case_id integer NOT NULL,
    name character varying(255),
    description character varying(1000),
    data jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);

CREATE SEQUENCE public.extracted_key_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.extracted_key_metrics_id_seq OWNED BY public.extracted_key_metrics.id;

ALTER TABLE ONLY public.extracted_key_metrics ALTER COLUMN id SET DEFAULT nextval('public.extracted_key_metrics_id_seq'::regclass);

ALTER TABLE ONLY public.extracted_key_metrics
    ADD CONSTRAINT extracted_key_metrics_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.extracted_key_metrics
    ADD CONSTRAINT extracted_key_metrics_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.extracted_key_metrics VALUES (1, 'Revenue', 'Key financial metrics including Revenue, EBITDA, Debt, Equity, and Interest Expense', '[{"name": "Revenue", "infoLines": ["Revenue growth supports minimum turnover covenant, reducing risk of operating underperformance.", "Stable YoY increase indicates low likelihood of cash-flow stress, supporting DSCR maintenance."], "dataPoints": {"Apr": 12, "Feb": 10.8, "Jan": 10.2, "Mar": 11.5, "May": 12.5}}, {"name": "EBITDA", "infoLines": ["Rising EBITDA strengthens Debt/EBITDA covenant compliance, improving borrower creditworthiness.", "Sustained profitability trend reduces risk of breach on interest coverage or leverage covenants."], "dataPoints": {"Apr": 1.1, "Feb": 1, "Jan": 0.9, "Mar": 1.05, "May": 1.2}}, {"name": "Debt", "infoLines": ["Current leverage remains within allowable Debt/EBITDA thresholds, though trending upward.", "Monitoring required to avoid breaching maximum leverage or total indebtedness covenants."], "dataPoints": {"Apr": 3.7, "Feb": 3.4, "Jan": 3.2, "Mar": 3.5, "May": 3.8}}, {"name": "Equity", "infoLines": ["Stable equity position supports Net Worth / Equity Maintenance covenants.", "Equity cushion reduces risk of LTV covenant deterioration during adverse market cycles."], "dataPoints": {"Apr": 1.15, "Feb": 1.05, "Jan": 1, "Mar": 1.1, "May": 1.2}}, {"name": "Interest Expense", "infoLines": ["Rising interest expense may pressure Interest Coverage covenants if EBITDA slows.", "Higher servicing costs could impact DSCR compliance, requiring ongoing monitoring."], "dataPoints": {"Apr": 205, "Feb": 190, "Jan": 180, "Mar": 195, "May": 210}}]', '2026-03-01 12:28:58.55607+05:30', '2026-03-01 20:24:22.845838+05:30', 6);
INSERT INTO public.extracted_key_metrics VALUES (1, 'EBITDA', 'Rising EBITDA strengthens Debt/EBITDA covenant compliance, improving borrower creditworthiness.', '{"Apr": 1.1, "Feb": 1, "Jan": 0.9, "Mar": 1.05, "May": 1.2}', '2026-03-01 12:28:58.55607+05:30', '2026-03-01 12:28:58.55607+05:30', 7);
INSERT INTO public.extracted_key_metrics VALUES (1, 'Debt', 'Current leverage remains within allowable Debt/EBITDA thresholds, though trending upward.', '{"Apr": 3.7, "Feb": 3.4, "Jan": 3.2, "Mar": 3.5, "May": 3.8}', '2026-03-01 12:28:58.55607+05:30', '2026-03-01 12:28:58.55607+05:30', 8);
INSERT INTO public.extracted_key_metrics VALUES (1, 'Equity', 'Stable equity position supports Net Worth / Equity Maintenance covenants.', '{"Apr": 1.15, "Feb": 1.05, "Jan": 1, "Mar": 1.1, "May": 1.2}', '2026-03-01 12:28:58.55607+05:30', '2026-03-01 12:28:58.55607+05:30', 9);
INSERT INTO public.extracted_key_metrics VALUES (1, 'Interest Expense', 'Rising interest expense may pressure Interest Coverage covenants if EBITDA slows.', '{"Apr": 205, "Feb": 190, "Jan": 180, "Mar": 195, "May": 210}', '2026-03-01 12:28:58.55607+05:30', '2026-03-01 12:28:58.55607+05:30', 10);

-- Reset sequence
SELECT pg_catalog.setval('public.extracted_key_metrics_id_seq', 10, true);
```

---

## 10. fr_y14_schedule_template_data_points

### DDL

```sql
CREATE TABLE public.fr_y14_schedule_template_data_points (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    label character varying(255),
    case_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE SEQUENCE public.fr_y14_schedule_template_data_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.fr_y14_schedule_template_data_points_id_seq OWNED BY public.fr_y14_schedule_template_data_points.id;

ALTER TABLE ONLY public.fr_y14_schedule_template_data_points ALTER COLUMN id SET DEFAULT nextval('public.fr_y14_schedule_template_data_points_id_seq'::regclass);

ALTER TABLE ONLY public.fr_y14_schedule_template_data_points
    ADD CONSTRAINT fr_y14_schedule_template_data_points_pkey PRIMARY KEY (id);

CREATE INDEX ix_fr_y14_schedule_template_data_points_case_id ON public.fr_y14_schedule_template_data_points USING btree (case_id);

ALTER TABLE ONLY public.fr_y14_schedule_template_data_points
    ADD CONSTRAINT fr_y14_schedule_template_data_points_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (1, 'Borrower / Obligor Information', 'Borrower / Obligor Information', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (2, 'Loan Characteristics', 'Loan Characteristics', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (3, 'Collateral Information', 'Collateral Information', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (4, 'Covenant Information (Extracted)', 'Covenant Information (Extracted)', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (5, 'Credit Quality & Risk Metrics', 'Credit Quality & Risk Metrics', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (6, 'Performance & Payment Info', 'Performance & Payment Info', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (7, 'Accounting & Reporting Attributes', 'Accounting & Reporting Attributes', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');
INSERT INTO public.fr_y14_schedule_template_data_points VALUES (8, 'Regulatory Schedule Mapping (Meta Fields)', 'Regulatory Schedule Mapping (Meta Fields)', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30');

-- Reset sequence
SELECT pg_catalog.setval('public.fr_y14_schedule_template_data_points_id_seq', 8, true);
```

---

## 11. fr_y14_schedule_template_data_point_details

### DDL

```sql
CREATE TABLE public.fr_y14_schedule_template_data_point_details (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    label character varying(255),
    value character varying(500),
    template_data_point_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    additional_data jsonb
);

CREATE SEQUENCE public.fr_y14_schedule_template_data_point_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.fr_y14_schedule_template_data_point_details_id_seq OWNED BY public.fr_y14_schedule_template_data_point_details.id;

ALTER TABLE ONLY public.fr_y14_schedule_template_data_point_details ALTER COLUMN id SET DEFAULT nextval('public.fr_y14_schedule_template_data_point_details_id_seq'::regclass);

ALTER TABLE ONLY public.fr_y14_schedule_template_data_point_details
    ADD CONSTRAINT fr_y14_schedule_template_data_point_details_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.fr_y14_schedule_template_data_point_details
    ADD CONSTRAINT fr_y14_schedule_template_data_point_template_data_point_id_fkey FOREIGN KEY (template_data_point_id) REFERENCES public.fr_y14_schedule_template_data_points(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (1, 'Obligor name', 'Obligor name', 'Vertex Logistics Corp.', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (2, 'Obligor ID', 'Obligor ID', '00492-WHSL', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (3, 'Country', 'Country', 'United States', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (4, 'Industry/NAICS code', 'Industry/NAICS code', '488510 - Freight Transportation Arrangement', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (5, 'Obligor type', 'Obligor type', 'Corporate', 1, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (6, 'Loan Type', 'Loan Type', 'Working Capital Revolver', 2, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (7, 'Origination Date', 'Origination Date', '15-Jan-21', 2, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (8, 'Maturity Date', 'Maturity Date', '15-Jan-26', 2, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (9, 'Original Commitment', 'Original Commitment', '$1,80,00,000', 2, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (10, 'Current Outstanding Balance', 'Current Outstanding Balance', '$1,42,00,000', 2, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (11, 'Collateral Type', 'Collateral Type', 'Accounts Receivable + Inventory', 3, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (12, 'Collateral Code', 'Collateral Code', '24', 3, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (13, 'Collateral Value', 'Collateral Value', '$2,10,00,000', 3, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (14, 'LTV (Calculated)', 'LTV (Calculated)', '64%', 3, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (15, 'Lien Position', 'Lien Position', '1st Lien', 3, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (16, 'DSCR', 'DSCR', NULL, 4, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', '{"status": "At Risk", "current": "0.75", "covenant": "DSCR", "threshold": "≥ 1.20"}');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (17, 'LTV', 'LTV', NULL, 4, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', '{"status": "Compliant", "current": "64%", "covenant": "LTV", "threshold": "≤ 70%"}');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (18, 'Leverage Ratio', 'Leverage Ratio', NULL, 4, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', '{"status": "Compliant", "current": "3.20x", "covenant": "Leverage Ratio", "threshold": "≤ 3.50x"}');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (19, 'Internal Risk Rating', 'Internal Risk Rating', '6 (Moderate Risk)', 5, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (20, 'Prob. of Default (PD)', 'Prob. of Default (PD)', '1.90%', 5, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (21, 'Loss Given Default (LGD)', 'Loss Given Default (LGD)', '38%', 5, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (22, 'Exposure at Default (EAD)', 'Exposure at Default (EAD)', '$1,80,00,000', 5, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (23, 'Accrued Interest', 'Accrued Interest', '$72,400', 5, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (24, 'Days Past Due', 'Days Past Due', '0', 6, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (25, 'Past Due Indicator', 'Past Due Indicator', 'No', 6, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (26, 'Last Payment Date', 'Last Payment Date', '12-Sep-25', 6, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (27, 'Next Payment Date', 'Next Payment Date', '12-Oct-25', 6, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (28, 'Payment Status', 'Payment Status', 'Current', 6, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (29, 'Accounting Standard', 'Accounting Standard', 'GAAP', 7, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (30, 'Accrual Status', 'Accrual Status', 'Performing', 7, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (31, 'Impairment Status', 'Impairment Status', 'Not Impaired', 7, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (32, 'Charge-Off Amount', 'Charge-Off Amount', '$0', 7, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (33, 'Restructured Indicator', 'Restructured Indicator', 'No', 7, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (34, 'DSCR (Reported)', 'DSCR (Reported)', '0.75', 8, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (35, 'DSCR (Trend YoY)', 'DSCR (Trend YoY)', '5%', 8, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (36, 'LTV (Reported)', 'LTV (Reported)', '64%', 8, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (37, 'EBITDA (TTM)', 'EBITDA (TTM)', '$1.2B', 8, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');
INSERT INTO public.fr_y14_schedule_template_data_point_details VALUES (38, 'Revenue (TTM)', 'Revenue (TTM)', '$12.5B', 8, '2026-03-01 13:10:41.731395+05:30', '2026-03-01 13:10:41.731395+05:30', 'null');

-- Reset sequence
SELECT pg_catalog.setval('public.fr_y14_schedule_template_data_point_details_id_seq', 38, true);
```

---

## 12. q3_highlights

### DDL

```sql
CREATE TABLE public.q3_highlights (
    case_id integer NOT NULL,
    name character varying(255),
    description character varying(1000),
    datalines character varying[],
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);

CREATE SEQUENCE public.q3_highlights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.q3_highlights_id_seq OWNED BY public.q3_highlights.id;

ALTER TABLE ONLY public.q3_highlights ALTER COLUMN id SET DEFAULT nextval('public.q3_highlights_id_seq'::regclass);

ALTER TABLE ONLY public.q3_highlights
    ADD CONSTRAINT q3_highlights_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.q3_highlights
    ADD CONSTRAINT q3_highlights_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.q3_highlights VALUES (1, 'DSCR Improvement', 'DSCR increased from 1.10 in Q2 → 1.15 in Q3, driven by higher operating cash flow.', '{"DSCR increased from 1.10 in Q2 → 1.15 in Q3","Driven by higher operating cash flow"}', '2026-03-01 12:56:22.569069+05:30', '2026-03-01 12:56:22.569069+05:30', 1);
INSERT INTO public.q3_highlights VALUES (1, 'Cash Flow Growth', 'Operating cash flow rose to $22K, marking a +22% increase quarter-over-quarter.', '{"Operating cash flow rose to $22K","Marking a +22% increase quarter-over-quarter"}', '2026-03-01 12:56:22.569069+05:30', '2026-03-01 12:56:22.569069+05:30', 2);
INSERT INTO public.q3_highlights VALUES (1, 'Interest Costs Stabilized', 'Interest expense increased only slightly ($4.0K → $4.5K), slowing the negative pressure on coverage.', '{"Interest expense increased only slightly ($4.0K → $4.5K)","Slowing the negative pressure on coverage"}', '2026-03-01 12:56:22.569069+05:30', '2026-03-01 12:56:22.569069+05:30', 3);
INSERT INTO public.q3_highlights VALUES (1, 'Delayed Shipments Reduced', 'Shipment delays dropped from 5 to 3, contributing to stronger cash collections.', '{"Shipment delays dropped from 5 to 3","Contributing to stronger cash collections"}', '2026-03-01 12:56:22.569069+05:30', '2026-03-01 12:56:22.569069+05:30', 4);
INSERT INTO public.q3_highlights VALUES (1, 'Operating Revenue Rebounded', 'Revenue improved following improved fulfillment performance (Promised vs Delivered variance reduced by 8%).', '{"Revenue improved following improved fulfillment performance","Promised vs Delivered variance reduced by 8%"}', '2026-03-01 12:56:22.569069+05:30', '2026-03-01 12:56:22.569069+05:30', 5);

-- Reset sequence
SELECT pg_catalog.setval('public.q3_highlights_id_seq', 5, true);
```

---

## 13. quarter_by_quarter_financial_drivers

### DDL

```sql
CREATE TABLE public.quarter_by_quarter_financial_drivers (
    case_id integer NOT NULL,
    data jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

ALTER TABLE ONLY public.quarter_by_quarter_financial_drivers
    ADD CONSTRAINT quarter_by_quarter_financial_drivers_pkey PRIMARY KEY (case_id);

ALTER TABLE ONLY public.quarter_by_quarter_financial_drivers
    ADD CONSTRAINT quarter_by_quarter_financial_drivers_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.quarter_by_quarter_financial_drivers VALUES (1, '[{"debt": 15000, "quarter": "Q1", "cashFlow": 15000, "interest": 15000}, {"debt": 16800, "quarter": "Q2", "cashFlow": 18000, "interest": 17500}, {"debt": 21000, "quarter": "Q3", "cashFlow": 25500, "interest": 23000}, {"debt": 27000, "quarter": "Q4", "cashFlow": 36000, "interest": 31000}]', '2026-03-01 21:18:08.782906+05:30', '2026-03-01 21:18:08.782906+05:30');
```

---

## 14. quarterly_dscr

### DDL

```sql
CREATE TABLE public.quarterly_dscr (
    case_id integer NOT NULL,
    data jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

ALTER TABLE ONLY public.quarterly_dscr
    ADD CONSTRAINT quarterly_dscr_pkey PRIMARY KEY (case_id);

ALTER TABLE ONLY public.quarterly_dscr
    ADD CONSTRAINT quarterly_dscr_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.quarterly_dscr VALUES (1, '[{"dscr": 1.8, "period": "FY 24-25 (Jan - Mar)", "quarter": "Q1", "threshold": 1.1}, {"dscr": 2.4, "period": "FY 24-25 (Apr - Jun)", "quarter": "Q2", "threshold": 1.1}, {"dscr": 2.0, "period": "FY 24-25 (Jul - Sep)", "quarter": "Q3", "threshold": 1.1}, {"dscr": 1.9, "period": "FY 24-25 (Oct - Dec)", "quarter": "Q4", "threshold": 1.1}]', '2026-03-01 12:49:35.399614+05:30', '2026-03-01 12:49:35.399614+05:30');
```

---

## 15. shipment_details

### DDL

```sql
CREATE TABLE public.shipment_details (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    promised_delivery_date date,
    actual_delivery_date date,
    case_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    status character varying(50)
);

CREATE SEQUENCE public.shipment_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.shipment_details_id_seq OWNED BY public.shipment_details.id;

ALTER TABLE ONLY public.shipment_details ALTER COLUMN id SET DEFAULT nextval('public.shipment_details_id_seq'::regclass);

ALTER TABLE ONLY public.shipment_details
    ADD CONSTRAINT shipment_details_pkey PRIMARY KEY (id);

CREATE INDEX ix_shipment_details_case_id ON public.shipment_details USING btree (case_id);

ALTER TABLE ONLY public.shipment_details
    ADD CONSTRAINT shipment_details_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.cases(id) ON DELETE CASCADE;
```

### INSERT Statements

```sql
INSERT INTO public.shipment_details VALUES (1, 'Shipment 1', '2025-08-12', '2025-08-10', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'Early');
INSERT INTO public.shipment_details VALUES (2, 'Shipment 2', '2025-06-02', '2025-06-01', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'On-Time');
INSERT INTO public.shipment_details VALUES (3, 'Shipment 3', '2025-05-01', '2025-05-10', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'Delayed');
INSERT INTO public.shipment_details VALUES (4, 'Shipment 4', '2025-04-12', '2025-04-12', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'On-Time');
INSERT INTO public.shipment_details VALUES (5, 'Shipment 5', '2025-03-25', '2025-03-25', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'On-Time');
INSERT INTO public.shipment_details VALUES (6, 'Shipment 6', '2025-02-14', '2025-02-18', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'Delayed');
INSERT INTO public.shipment_details VALUES (7, 'Shipment 7', '2025-02-02', '2025-02-02', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'On-Time');
INSERT INTO public.shipment_details VALUES (8, 'Shipment 9', '2025-01-26', '2025-01-26', 1, '2026-03-01 14:01:23.93667+05:30', '2026-03-01 14:01:23.93667+05:30', 'On-Time');

-- Reset sequence
SELECT pg_catalog.setval('public.shipment_details_id_seq', 8, true);
```

---

## Database Relationships Summary

| Child Table | Foreign Key | Parent Table | On Delete |
|-------------|-------------|--------------|-----------|
| covenant_status | case_id | cases | CASCADE |
| datasimulator_benefits | case_id | cases | CASCADE |
| detailed_findings_operational | case_id | cases | CASCADE |
| detailed_findings_y14 | case_id | cases | CASCADE |
| documents | case_id | cases | CASCADE |
| extracted_key_metrics | case_id | cases | CASCADE |
| fr_y14_schedule_template_data_points | case_id | cases | CASCADE |
| fr_y14_schedule_template_data_point_details | template_data_point_id | fr_y14_schedule_template_data_points | CASCADE |
| q3_highlights | case_id | cases | CASCADE |
| quarter_by_quarter_financial_drivers | case_id | cases | CASCADE |
| quarterly_dscr | case_id | cases | CASCADE |
| shipment_details | case_id | cases | CASCADE |

---

## Indexes

| Table | Index Name | Column(s) |
|-------|------------|-----------|
| documents | ix_documents_case_id | case_id |
| fr_y14_schedule_template_data_points | ix_fr_y14_schedule_template_data_points_case_id | case_id |
| shipment_details | ix_shipment_details_case_id | case_id |
