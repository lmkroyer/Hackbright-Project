--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.9
-- Dumped by pg_dump version 9.5.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answers; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE answers (
    answer_id integer NOT NULL,
    doc_type_id integer NOT NULL,
    case_id integer NOT NULL,
    date_created timestamp without time zone,
    date_reviewed timestamp without time zone,
    date_submitted timestamp without time zone,
    docx character varying(64) NOT NULL
);


ALTER TABLE answers OWNER TO vagrant;

--
-- Name: answers_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE answers_answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answers_answer_id_seq OWNER TO vagrant;

--
-- Name: answers_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE answers_answer_id_seq OWNED BY answers.answer_id;


--
-- Name: caseparties; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE caseparties (
    caseparty_id integer NOT NULL,
    party_id integer NOT NULL,
    case_id integer NOT NULL,
    role_name character varying(25)
);


ALTER TABLE caseparties OWNER TO vagrant;

--
-- Name: caseparties_caseparty_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE caseparties_caseparty_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE caseparties_caseparty_id_seq OWNER TO vagrant;

--
-- Name: caseparties_caseparty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE caseparties_caseparty_id_seq OWNED BY caseparties.caseparty_id;


--
-- Name: cases; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE cases (
    case_id integer NOT NULL,
    case_no integer,
    team_lead character varying(25),
    opposing_id integer,
    claim_type_id integer,
    damages_asked character varying(15),
    state character varying(25),
    county character varying(25),
    initialized timestamp without time zone,
    settlement_amount integer,
    settled boolean NOT NULL
);


ALTER TABLE cases OWNER TO vagrant;

--
-- Name: cases_case_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE cases_case_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_id_seq OWNER TO vagrant;

--
-- Name: cases_case_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE cases_case_id_seq OWNED BY cases.case_id;


--
-- Name: caseusers; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE caseusers (
    team_id integer NOT NULL,
    user_id character varying(25) NOT NULL,
    case_id integer NOT NULL
);


ALTER TABLE caseusers OWNER TO vagrant;

--
-- Name: caseusers_team_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE caseusers_team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE caseusers_team_id_seq OWNER TO vagrant;

--
-- Name: caseusers_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE caseusers_team_id_seq OWNED BY caseusers.team_id;


--
-- Name: claim_types; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE claim_types (
    claim_type_id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE claim_types OWNER TO vagrant;

--
-- Name: claim_types_claim_type_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE claim_types_claim_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE claim_types_claim_type_id_seq OWNER TO vagrant;

--
-- Name: claim_types_claim_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE claim_types_claim_type_id_seq OWNED BY claim_types.claim_type_id;


--
-- Name: complaints; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE complaints (
    complaint_id integer NOT NULL,
    case_id integer NOT NULL,
    doc_type_id integer NOT NULL,
    date_received timestamp without time zone NOT NULL,
    date_processed timestamp without time zone,
    damages_asked character varying(100) NOT NULL,
    legal_basis character varying(64),
    doc character varying(64) NOT NULL,
    txt character varying(64) NOT NULL
);


ALTER TABLE complaints OWNER TO vagrant;

--
-- Name: complaints_complaint_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE complaints_complaint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE complaints_complaint_id_seq OWNER TO vagrant;

--
-- Name: complaints_complaint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE complaints_complaint_id_seq OWNED BY complaints.complaint_id;


--
-- Name: doc_types; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE doc_types (
    doc_type_id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE doc_types OWNER TO vagrant;

--
-- Name: doc_types_doc_type_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE doc_types_doc_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE doc_types_doc_type_id_seq OWNER TO vagrant;

--
-- Name: doc_types_doc_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE doc_types_doc_type_id_seq OWNED BY doc_types.doc_type_id;


--
-- Name: fclients; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE fclients (
    client_id integer NOT NULL,
    attorney character varying(25),
    fund character varying(64),
    fund_state character varying(25),
    fund_ppp character varying(64),
    gp character varying(64),
    gp_state character varying(25),
    gp_address character varying(64),
    gp_email character varying(64),
    gp_sig_party character varying(64),
    im character varying(64),
    im_state character varying(25),
    im_address character varying(64),
    im_email character varying(64),
    sig_date_lpa date,
    lpa character varying(64),
    mgmt_fee character varying(64),
    perf_fee integer,
    ppm character varying(64),
    ima character varying(64),
    "form_13F" character varying(64),
    "form_PF" character varying(64),
    sum_rep boolean,
    principals character varying(250),
    removal text,
    leverage text,
    min_commitment character varying(25),
    transfers text,
    reinvestment text
);


ALTER TABLE fclients OWNER TO vagrant;

--
-- Name: fclients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE fclients_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE fclients_client_id_seq OWNER TO vagrant;

--
-- Name: fclients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE fclients_client_id_seq OWNED BY fclients.client_id;


--
-- Name: interrogatories; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE interrogatories (
    interrogatories_id integer NOT NULL,
    doc_type_id integer NOT NULL,
    case_id integer NOT NULL,
    date_created timestamp without time zone,
    date_reviewed timestamp without time zone,
    date_submitted timestamp without time zone,
    docx character varying(64)
);


ALTER TABLE interrogatories OWNER TO vagrant;

--
-- Name: interrogatories_interrogatories_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE interrogatories_interrogatories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE interrogatories_interrogatories_id_seq OWNER TO vagrant;

--
-- Name: interrogatories_interrogatories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE interrogatories_interrogatories_id_seq OWNED BY interrogatories.interrogatories_id;


--
-- Name: opposing_counsel; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE opposing_counsel (
    opposing_id integer NOT NULL,
    fname character varying(25) NOT NULL,
    lname character varying(25) NOT NULL,
    email character varying(100),
    mailing_address character varying(100),
    firm_name character varying(64)
);


ALTER TABLE opposing_counsel OWNER TO vagrant;

--
-- Name: opposing_counsel_opposing_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE opposing_counsel_opposing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE opposing_counsel_opposing_id_seq OWNER TO vagrant;

--
-- Name: opposing_counsel_opposing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE opposing_counsel_opposing_id_seq OWNED BY opposing_counsel.opposing_id;


--
-- Name: parties; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE parties (
    party_id integer NOT NULL,
    fname character varying(25),
    lname character varying(25),
    company character varying(100),
    email character varying(100),
    residence character varying(100)
);


ALTER TABLE parties OWNER TO vagrant;

--
-- Name: parties_party_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE parties_party_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE parties_party_id_seq OWNER TO vagrant;

--
-- Name: parties_party_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE parties_party_id_seq OWNED BY parties.party_id;


--
-- Name: request_pro_docs; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE request_pro_docs (
    request_pro_docs_id integer NOT NULL,
    doc_type_id integer NOT NULL,
    case_id integer NOT NULL,
    date_created timestamp without time zone,
    date_reviewed timestamp without time zone,
    date_submitted timestamp without time zone,
    docx character varying(64)
);


ALTER TABLE request_pro_docs OWNER TO vagrant;

--
-- Name: request_pro_docs_request_pro_docs_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE request_pro_docs_request_pro_docs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE request_pro_docs_request_pro_docs_id_seq OWNER TO vagrant;

--
-- Name: request_pro_docs_request_pro_docs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE request_pro_docs_request_pro_docs_id_seq OWNED BY request_pro_docs.request_pro_docs_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE roles (
    role_name character varying(25) NOT NULL
);


ALTER TABLE roles OWNER TO vagrant;

--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id character varying(25) NOT NULL,
    fname character varying(25) NOT NULL,
    lname character varying(25) NOT NULL,
    email character varying(100) NOT NULL,
    mailing_address character varying(100) NOT NULL,
    firm_name character varying(64) NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: answer_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY answers ALTER COLUMN answer_id SET DEFAULT nextval('answers_answer_id_seq'::regclass);


--
-- Name: caseparty_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseparties ALTER COLUMN caseparty_id SET DEFAULT nextval('caseparties_caseparty_id_seq'::regclass);


--
-- Name: case_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY cases ALTER COLUMN case_id SET DEFAULT nextval('cases_case_id_seq'::regclass);


--
-- Name: team_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseusers ALTER COLUMN team_id SET DEFAULT nextval('caseusers_team_id_seq'::regclass);


--
-- Name: claim_type_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY claim_types ALTER COLUMN claim_type_id SET DEFAULT nextval('claim_types_claim_type_id_seq'::regclass);


--
-- Name: complaint_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY complaints ALTER COLUMN complaint_id SET DEFAULT nextval('complaints_complaint_id_seq'::regclass);


--
-- Name: doc_type_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY doc_types ALTER COLUMN doc_type_id SET DEFAULT nextval('doc_types_doc_type_id_seq'::regclass);


--
-- Name: client_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY fclients ALTER COLUMN client_id SET DEFAULT nextval('fclients_client_id_seq'::regclass);


--
-- Name: interrogatories_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY interrogatories ALTER COLUMN interrogatories_id SET DEFAULT nextval('interrogatories_interrogatories_id_seq'::regclass);


--
-- Name: opposing_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY opposing_counsel ALTER COLUMN opposing_id SET DEFAULT nextval('opposing_counsel_opposing_id_seq'::regclass);


--
-- Name: party_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY parties ALTER COLUMN party_id SET DEFAULT nextval('parties_party_id_seq'::regclass);


--
-- Name: request_pro_docs_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY request_pro_docs ALTER COLUMN request_pro_docs_id SET DEFAULT nextval('request_pro_docs_request_pro_docs_id_seq'::regclass);


--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY answers (answer_id, doc_type_id, case_id, date_created, date_reviewed, date_submitted, docx) FROM stdin;
1	2	3	2017-12-06 01:12:29.893879	2017-12-06 01:12:29.893879	2017-12-06 01:12:29.893879	filestorage/answer_454545.docx
2	2	5	2017-12-06 01:24:22.501994	2017-12-06 01:24:22.501994	2017-12-06 01:24:22.501994	filestorage/answer_123456.docx
3	2	7	2017-12-06 01:44:09.092588	2017-12-06 01:44:09.092588	2017-12-06 01:44:09.092588	filestorage/answer_454545.docx
\.


--
-- Name: answers_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('answers_answer_id_seq', 3, true);


--
-- Data for Name: caseparties; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY caseparties (caseparty_id, party_id, case_id, role_name) FROM stdin;
1	1	1	plaintiff
2	2	1	defendant
3	3	2	plaintiff
4	4	2	defendant
5	1	3	plaintiff
6	2	3	defendant
7	5	4	plaintiff
8	4	4	defendant
9	6	5	plaintiff
10	4	5	defendant
11	7	6	plaintiff
12	4	6	defendant
13	3	7	plaintiff
14	2	7	defendant
\.


--
-- Name: caseparties_caseparty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('caseparties_caseparty_id_seq', 14, true);


--
-- Data for Name: cases; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY cases (case_id, case_no, team_lead, opposing_id, claim_type_id, damages_asked, state, county, initialized, settlement_amount, settled) FROM stdin;
1	454545	theFunnyOne	1	1	$350,000	California For	Sonoma	2017-12-06 00:54:01.075338	\N	f
2	123456	lmkroyer	2	1	$10,000	New York	New York	2017-12-06 01:07:56.524019	\N	f
3	454545	theDancingOne	1	1	$350,000	California For	Sonoma	2017-12-06 01:11:37.856204	\N	f
4	123456	theRudeOne	2	5	$95,000	CA	San Francisco	2017-12-06 01:16:49.562094	\N	f
5	123456	theDancingOne	2	1	$10,000	California	Los Angeles	2017-12-06 01:21:54.554415	\N	f
6	123456	theRudeOne	2	1	$10,000	California	Alameda	2017-12-06 01:25:13.362849	\N	f
7	454545	theLostOne	1	1	$350,000	California For	Sonoma	2017-12-06 01:43:19.496441	\N	f
\.


--
-- Name: cases_case_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('cases_case_id_seq', 7, true);


--
-- Data for Name: caseusers; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY caseusers (team_id, user_id, case_id) FROM stdin;
1	theFunnyOne	1
2	theRudeOne	1
3	lmkroyer	1
4	lmkroyer	2
5	theRebelOne	2
6	theDrivenOne	2
7	theDancingOne	3
8	thePopularOne	3
9	theGothOne	3
10	theRudeOne	4
11	theTragicOne	4
12	theHonestOne	4
13	theDancingOne	5
14	theIntenseOne	5
15	lmkroyer	5
16	theRudeOne	6
17	lmkroyer	6
18	theTragicOne	6
19	theLostOne	7
20	theSensitiveOne	7
21	theDrivenOne	7
\.


--
-- Name: caseusers_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('caseusers_team_id_seq', 21, true);


--
-- Data for Name: claim_types; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY claim_types (claim_type_id, name) FROM stdin;
1	Personal Injury
2	Breach of Contract
3	Divorce
4	Property Dispute
5	Landlord Tenant
6	Other
\.


--
-- Name: claim_types_claim_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('claim_types_claim_type_id_seq', 1, false);


--
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY complaints (complaint_id, case_id, doc_type_id, date_received, date_processed, damages_asked, legal_basis, doc, txt) FROM stdin;
1	1	1	2017-12-06 00:54:01.075338	2017-12-06 00:56:17.298017	$350,000	Negligence	filestorage/complaint1.pdf	filestorage/complaint1.txt
2	1	1	2017-12-06 00:54:01.075338	2017-12-06 00:57:57.894494	$350,000	Negligence	filestorage/complaint1.pdf	filestorage/complaint1.txt
3	2	1	2017-12-06 01:07:56.524019	2017-12-06 01:08:30.684327	$10,000	Defamation	filestorage/complaint2.pdf	filestorage/complaint2.txt
4	2	1	2017-12-06 01:07:56.524019	2017-12-06 01:10:31.37148	$10,000	Defamation	filestorage/complaint2.pdf	filestorage/complaint2.txt
5	3	1	2017-12-06 01:11:37.856204	2017-12-06 01:12:04.719131	$350,000	Negligence	filestorage/complaint1.pdf	filestorage/complaint1.txt
6	4	1	2017-12-06 01:16:49.562094	2017-12-06 01:21:08.182049	$95,000	Libel	filestorage/complaint2.pdf	filestorage/complaint2.txt
7	5	1	2017-12-06 01:21:54.554415	2017-12-06 01:24:17.768133	$10,000	Defamation	filestorage/complaint2.pdf	filestorage/complaint2.txt
8	6	1	2017-12-06 01:25:13.362849	2017-12-06 01:29:16.875715	$10,000	Defamation	filestorage/complaint2.pdf	filestorage/complaint2.txt
9	7	1	2017-12-06 01:43:19.496441	2017-12-06 01:43:57.204292	$350,000	Negligence	filestorage/complaint1.pdf	filestorage/complaint1.txt
\.


--
-- Name: complaints_complaint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('complaints_complaint_id_seq', 9, true);


--
-- Data for Name: doc_types; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY doc_types (doc_type_id, name) FROM stdin;
1	Complaint
2	Answer
3	Interrogatories
4	Request_Pro_Docs
\.


--
-- Name: doc_types_doc_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('doc_types_doc_type_id_seq', 1, false);


--
-- Data for Name: fclients; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY fclients (client_id, attorney, fund, fund_state, fund_ppp, gp, gp_state, gp_address, gp_email, gp_sig_party, im, im_state, im_address, im_email, sig_date_lpa, lpa, mgmt_fee, perf_fee, ppm, ima, "form_13F", "form_PF", sum_rep, principals, removal, leverage, min_commitment, transfers, reinvestment) FROM stdin;
1	lmkroyer	KXTER FUND ONE LLC	Delaware	\N	\N	\N	\N	\N	\N	ther Advisors LLC	\N	\N	\N	\N	\N	1.5%, payable quarterly	\N	filestorage/ppm_sample.pdf	\N	\N	\N	t	The principals of the Manager that will be primarily responsible for the\nFund’s investment activities will be Thomas Schneider and Rickard\nAntblad (the “Principals").	The Manager may be removed for Cause upon the Vote of at least 75% in\ninterest ofthc Members.	The Fund may not incur any indebtedness other than to pay expenses or\nshortiterm borrowings to fund Members’ capital contributions on an\nexpedited basis, or in connection with a remedy provided in the Fund\nAgreement related to a Defaulting Member.	$5,000	All proposed transfers of Fund interests will be subject to the consent of the\nManager, which consent may be granted or withheld in the sole discretion\nof the Manager.	\N
2	lmkroyer	Red Cedar Onshore Fund, LP	Utah	Salt Lake City, Utah	Red Cedar Feeder Fund GP, LLC	Delaware	285 Edgar St.	rcgp@gmail.com	Jane Doe	Red Cedar Mgr LLC	Delaware	285 Edgar St.	rcim@gmail.com	2017-11-17	filestorage/LPA_Red Cedar Onshore Fund, LP.docx	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
3	lmkroyer	Red Cedar Offshore Fund, LP	Utah	Salt Lake City, Utah	Red Cedar Feeder Fund GP, LLC	Delaware	285 Edgar St.	rcgp@gmail.com	Jane Doe	Red Cedar Mgr LLC	Delaware	285 Edgar St.	rcim@gmail.com	2017-11-17	filestorage/LPA_Red Cedar Offshore Fund, LP.docx	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
4	lmkroyer	Red Cedar Master Fund, LP	Utah	Salt Lake City, Utah	Red Cedar GP, LLC	Delaware	285 Edgar St.	rcgp@gmail.com	Jane Doe	Red Cedar Mgr LLC	Delaware	285 Edgar St.	rcim@gmail.com	2017-11-18	filestorage/LPA_Red Cedar Master Fund, LP.docx	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
5	lmkroyer	Hackbright Onshore Fund, LP	California	San Francisco, CA	Hackbright Onshore GP, LLC	Delaware	683 Sutter St. San Francisco, CA	hackbright@gmail.com	Ada Lovelace	Hackbright Management, LLC	Delaware	683 Sutter St. San Francisco, CA	hackbrightim@gmail.com	2017-12-06	filestorage/LPA_Hackbright Onshore Fund, LP.docx	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Name: fclients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('fclients_client_id_seq', 5, true);


--
-- Data for Name: interrogatories; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY interrogatories (interrogatories_id, doc_type_id, case_id, date_created, date_reviewed, date_submitted, docx) FROM stdin;
\.


--
-- Name: interrogatories_interrogatories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('interrogatories_interrogatories_id_seq', 1, false);


--
-- Data for Name: opposing_counsel; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY opposing_counsel (opposing_id, fname, lname, email, mailing_address, firm_name) FROM stdin;
1	Deborah	Robertson	\N	\N	Wolters Klewer LLC
2	Timothy	Murphy	\N	\N	Bertie Botts Beans LLC
\.


--
-- Name: opposing_counsel_opposing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('opposing_counsel_opposing_id_seq', 2, true);


--
-- Data for Name: parties; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY parties (party_id, fname, lname, company, email, residence) FROM stdin;
1	Ronald	Weasley	\N	\N	\N
2	Harry	Potter	\N	\N	Sonoma Sonoma County California
3	Hermione	Granger	\N	\N	\N
4	Severus	Snape	\N	\N	New York New York
5	Draco	Malfoy	\N	\N	\N
6	Ron	Weasley	\N	\N	\N
7	Seamus	Thomas	\N	\N	\N
\.


--
-- Name: parties_party_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('parties_party_id_seq', 7, true);


--
-- Data for Name: request_pro_docs; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY request_pro_docs (request_pro_docs_id, doc_type_id, case_id, date_created, date_reviewed, date_submitted, docx) FROM stdin;
\.


--
-- Name: request_pro_docs_request_pro_docs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('request_pro_docs_request_pro_docs_id_seq', 1, false);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY roles (role_name) FROM stdin;
plaintiff
defendant
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, fname, lname, email, mailing_address, firm_name) FROM stdin;
theIntenseOne	Effy	Stonem	estonem@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theRudeOne	Tony	Stonem	tstonem@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theDancingOne	Maxxie	Oliver	moliver@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theLostOne	Cassie	Ainsworth	cainsworth@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theRebelOne	James	Cook	jcook@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theSensitiveOne	Sid	Jenkins	sjenkins@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theTragicOne	Chris	Miles	cmiles@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theFunnyOne	Naomi	Campbell	ncampbell@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theHonestOne	Franky	Fitzgerald	ffitzgerald@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
thePopularOne	Mini	McGuinness	mmcguinness@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theDrivenOne	Jal	Fazer	jfazer@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
theGothOne	Rich	Hardbeck	rhardbeck@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
thePoshOne	Grace	Blood	gblood@lglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
lmkroyer	Lindsay	Kroyer	lkroyer@leglease.com	383 Sutter St. San Francisco, CA	Wayne, Prince & Jones LLP
\.


--
-- Name: answers_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (answer_id);


--
-- Name: caseparties_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseparties
    ADD CONSTRAINT caseparties_pkey PRIMARY KEY (caseparty_id);


--
-- Name: cases_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY cases
    ADD CONSTRAINT cases_pkey PRIMARY KEY (case_id);


--
-- Name: caseusers_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseusers
    ADD CONSTRAINT caseusers_pkey PRIMARY KEY (team_id);


--
-- Name: claim_types_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY claim_types
    ADD CONSTRAINT claim_types_pkey PRIMARY KEY (claim_type_id);


--
-- Name: complaints_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (complaint_id);


--
-- Name: doc_types_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY doc_types
    ADD CONSTRAINT doc_types_pkey PRIMARY KEY (doc_type_id);


--
-- Name: fclients_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY fclients
    ADD CONSTRAINT fclients_pkey PRIMARY KEY (client_id);


--
-- Name: interrogatories_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY interrogatories
    ADD CONSTRAINT interrogatories_pkey PRIMARY KEY (interrogatories_id);


--
-- Name: opposing_counsel_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY opposing_counsel
    ADD CONSTRAINT opposing_counsel_pkey PRIMARY KEY (opposing_id);


--
-- Name: parties_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY parties
    ADD CONSTRAINT parties_pkey PRIMARY KEY (party_id);


--
-- Name: request_pro_docs_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY request_pro_docs
    ADD CONSTRAINT request_pro_docs_pkey PRIMARY KEY (request_pro_docs_id);


--
-- Name: roles_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_name);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: answers_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT answers_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: caseparties_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseparties
    ADD CONSTRAINT caseparties_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: caseparties_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseparties
    ADD CONSTRAINT caseparties_party_id_fkey FOREIGN KEY (party_id) REFERENCES parties(party_id);


--
-- Name: caseparties_role_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseparties
    ADD CONSTRAINT caseparties_role_name_fkey FOREIGN KEY (role_name) REFERENCES roles(role_name);


--
-- Name: cases_claim_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY cases
    ADD CONSTRAINT cases_claim_type_id_fkey FOREIGN KEY (claim_type_id) REFERENCES claim_types(claim_type_id);


--
-- Name: cases_opposing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY cases
    ADD CONSTRAINT cases_opposing_id_fkey FOREIGN KEY (opposing_id) REFERENCES opposing_counsel(opposing_id);


--
-- Name: cases_team_lead_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY cases
    ADD CONSTRAINT cases_team_lead_fkey FOREIGN KEY (team_lead) REFERENCES users(user_id);


--
-- Name: caseusers_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseusers
    ADD CONSTRAINT caseusers_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: caseusers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY caseusers
    ADD CONSTRAINT caseusers_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: complaints_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY complaints
    ADD CONSTRAINT complaints_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: fclients_attorney_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY fclients
    ADD CONSTRAINT fclients_attorney_fkey FOREIGN KEY (attorney) REFERENCES users(user_id);


--
-- Name: interrogatories_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY interrogatories
    ADD CONSTRAINT interrogatories_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: request_pro_docs_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY request_pro_docs
    ADD CONSTRAINT request_pro_docs_case_id_fkey FOREIGN KEY (case_id) REFERENCES cases(case_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

