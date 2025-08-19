

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO postgres;

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;


CREATE TABLE public.items (
    item_id integer NOT NULL,
    item_name character varying(50) NOT NULL,
    price integer NOT NULL
);


ALTER TABLE public.items OWNER TO postgres;


CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.items_item_id_seq OWNER TO postgres;


ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;

ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);



ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);



COPY public.customers (customer_id, first_name, last_name) FROM stdin;
1	Greg	Jones
2	Sandra	Jones
3	Scott	Scott
4	Trevor	Green
5	Melanie	Johnson
\.



COPY public.items (item_id, item_name, price) FROM stdin;
1	Petit bureau	100
2	Grand bureau	300
3	Ventilateur	80
\.



SELECT pg_catalog.setval('public.customers_customer_id_seq', 5, true);



SELECT pg_catalog.setval('public.items_item_id_seq', 3, true);



ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);



ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);