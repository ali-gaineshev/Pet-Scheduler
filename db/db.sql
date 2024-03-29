toc.dat                                                                                             0000600 0004000 0002000 00000032534 14553407552 0014460 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP           /                 |            pet_scheduler_db %   14.10 (Ubuntu 14.10-0ubuntu0.22.04.1) %   14.10 (Ubuntu 14.10-0ubuntu0.22.04.1) 0    I           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         J           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         K           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         L           1262    16385    pet_scheduler_db    DATABASE     e   CREATE DATABASE pet_scheduler_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_CA.UTF-8';
     DROP DATABASE pet_scheduler_db;
                postgres    false         M           0    0    DATABASE pet_scheduler_db    ACL     d   GRANT ALL ON DATABASE pet_scheduler_db TO ali;
GRANT ALL ON DATABASE pet_scheduler_db TO ali_admin;
                   postgres    false    3404         �            1255    16498    clean_for_test()    FUNCTION     V  CREATE FUNCTION public.clean_for_test() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM familymembers WHERE family_id <> 1;
  DELETE FROM FAMILYTASKS;
  delete from familymembers where person_id <> 1;
   DELETE FROM tasks;
    DELETE FROM families WHERE family_id <> 1;
     DELETE FROM persons WHERE person_id <> 1;
END;
$$;
 '   DROP FUNCTION public.clean_for_test();
       public          ali    false         N           0    0    FUNCTION clean_for_test()    ACL     <   GRANT ALL ON FUNCTION public.clean_for_test() TO ali_admin;
          public          ali    false    217         �            1259    16410    families    TABLE     ]   CREATE TABLE public.families (
    head_member_id integer,
    family_id integer NOT NULL
);
    DROP TABLE public.families;
       public         heap    admin    false         O           0    0    TABLE families    ACL     I   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.families TO ali_admin;
          public          admin    false    211         �            1259    16472    families_new_family_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_new_family_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.families_new_family_id_seq;
       public          admin    false    211         P           0    0    families_new_family_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.families_new_family_id_seq OWNED BY public.families.family_id;
          public          admin    false    213         Q           0    0 #   SEQUENCE families_new_family_id_seq    ACL     O   GRANT SELECT,USAGE ON SEQUENCE public.families_new_family_id_seq TO ali_admin;
          public          admin    false    213         �            1259    16420    familymembers    TABLE     f   CREATE TABLE public.familymembers (
    family_id integer NOT NULL,
    person_id integer NOT NULL
);
 !   DROP TABLE public.familymembers;
       public         heap    admin    false         R           0    0    TABLE familymembers    ACL     N   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.familymembers TO ali_admin;
          public          admin    false    212         �            1259    16528    familytasks    TABLE     �   CREATE TABLE public.familytasks (
    family_id integer NOT NULL,
    task_id integer NOT NULL,
    person_id integer,
    completed boolean DEFAULT false
);
    DROP TABLE public.familytasks;
       public         heap    ali    false         S           0    0    TABLE familytasks    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.familytasks TO ali_admin;
          public          ali    false    216         �            1259    16387    persons    TABLE     �   CREATE TABLE public.persons (
    person_id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL
);
    DROP TABLE public.persons;
       public         heap    admin    false         T           0    0    TABLE persons    ACL     H   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.persons TO ali_admin;
          public          admin    false    210         �            1259    16386    persons_person_id_seq    SEQUENCE     �   CREATE SEQUENCE public.persons_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.persons_person_id_seq;
       public          admin    false    210         U           0    0    persons_person_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;
          public          admin    false    209         V           0    0    SEQUENCE persons_person_id_seq    ACL     J   GRANT SELECT,USAGE ON SEQUENCE public.persons_person_id_seq TO ali_admin;
          public          admin    false    209         �            1259    16515    tasks    TABLE     ;  CREATE TABLE public.tasks (
    task_id integer NOT NULL,
    name text NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    CONSTRAINT tasks_check CHECK ((end_time > start_time)),
    CONSTRAINT tasks_start_time_check CHECK (((start_time >= '00:00:00'::time without time zone) AND (start_time < '24:00:00'::time without time zone))),
    CONSTRAINT tasks_start_time_check1 CHECK (((start_time >= '00:00:00'::time without time zone) AND (start_time < '24:00:00'::time without time zone)))
);
    DROP TABLE public.tasks;
       public         heap    ali    false         W           0    0    TABLE tasks    ACL     F   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tasks TO ali_admin;
          public          ali    false    215         �            1259    16514    tasks_task_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.tasks_task_id_seq;
       public          ali    false    215         X           0    0    tasks_task_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks.task_id;
          public          ali    false    214         Y           0    0    SEQUENCE tasks_task_id_seq    ACL     F   GRANT SELECT,USAGE ON SEQUENCE public.tasks_task_id_seq TO ali_admin;
          public          ali    false    214         �           2604    16485    families family_id    DEFAULT     |   ALTER TABLE ONLY public.families ALTER COLUMN family_id SET DEFAULT nextval('public.families_new_family_id_seq'::regclass);
 A   ALTER TABLE public.families ALTER COLUMN family_id DROP DEFAULT;
       public          admin    false    213    211         �           2604    16390    persons person_id    DEFAULT     v   ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);
 @   ALTER TABLE public.persons ALTER COLUMN person_id DROP DEFAULT;
       public          admin    false    209    210    210         �           2604    16518    tasks task_id    DEFAULT     n   ALTER TABLE ONLY public.tasks ALTER COLUMN task_id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);
 <   ALTER TABLE public.tasks ALTER COLUMN task_id DROP DEFAULT;
       public          ali    false    215    214    215         A          0    16410    families 
   TABLE DATA           =   COPY public.families (head_member_id, family_id) FROM stdin;
    public          admin    false    211       3393.dat B          0    16420    familymembers 
   TABLE DATA           =   COPY public.familymembers (family_id, person_id) FROM stdin;
    public          admin    false    212       3394.dat F          0    16528    familytasks 
   TABLE DATA           O   COPY public.familytasks (family_id, task_id, person_id, completed) FROM stdin;
    public          ali    false    216       3398.dat @          0    16387    persons 
   TABLE DATA           C   COPY public.persons (person_id, name, email, password) FROM stdin;
    public          admin    false    210       3392.dat E          0    16515    tasks 
   TABLE DATA           J   COPY public.tasks (task_id, name, date, start_time, end_time) FROM stdin;
    public          ali    false    215       3397.dat Z           0    0    families_new_family_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.families_new_family_id_seq', 35, true);
          public          admin    false    213         [           0    0    persons_person_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.persons_person_id_seq', 136, true);
          public          admin    false    209         \           0    0    tasks_task_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.tasks_task_id_seq', 133, true);
          public          ali    false    214         �           2606    16487    families families_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (family_id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            admin    false    211         �           2606    16424     familymembers familymembers_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_pkey PRIMARY KEY (family_id, person_id);
 J   ALTER TABLE ONLY public.familymembers DROP CONSTRAINT familymembers_pkey;
       public            admin    false    212    212         �           2606    16533    familytasks familytasks_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_pkey PRIMARY KEY (family_id, task_id);
 F   ALTER TABLE ONLY public.familytasks DROP CONSTRAINT familytasks_pkey;
       public            ali    false    216    216         �           2606    16456    persons primary_key_email 
   CONSTRAINT     Z   ALTER TABLE ONLY public.persons
    ADD CONSTRAINT primary_key_email PRIMARY KEY (email);
 C   ALTER TABLE ONLY public.persons DROP CONSTRAINT primary_key_email;
       public            admin    false    210         �           2606    16522    tasks tasks_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);
 :   ALTER TABLE ONLY public.tasks DROP CONSTRAINT tasks_pkey;
       public            ali    false    215         �           2606    16454    persons unique_person_id 
   CONSTRAINT     X   ALTER TABLE ONLY public.persons
    ADD CONSTRAINT unique_person_id UNIQUE (person_id);
 B   ALTER TABLE ONLY public.persons DROP CONSTRAINT unique_person_id;
       public            admin    false    210         �           2606    16488 %   families families_head_member_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_head_member_id_fkey FOREIGN KEY (head_member_id) REFERENCES public.persons(person_id);
 O   ALTER TABLE ONLY public.families DROP CONSTRAINT families_head_member_id_fkey;
       public          admin    false    3238    210    211         �           2606    16493 *   familymembers familymembers_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(family_id);
 T   ALTER TABLE ONLY public.familymembers DROP CONSTRAINT familymembers_family_id_fkey;
       public          admin    false    3240    211    212         �           2606    16467 *   familymembers familymembers_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(person_id);
 T   ALTER TABLE ONLY public.familymembers DROP CONSTRAINT familymembers_person_id_fkey;
       public          admin    false    210    3238    212         �           2606    16534 &   familytasks familytasks_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(family_id);
 P   ALTER TABLE ONLY public.familytasks DROP CONSTRAINT familytasks_family_id_fkey;
       public          ali    false    211    3240    216         �           2606    16539 $   familytasks familytasks_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(task_id);
 N   ALTER TABLE ONLY public.familytasks DROP CONSTRAINT familytasks_task_id_fkey;
       public          ali    false    3244    216    215                                                                                                                                                                            3393.dat                                                                                            0000600 0004000 0002000 00000000011 14553407552 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       3394.dat                                                                                            0000600 0004000 0002000 00000000017 14553407552 0014264 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1
1	136
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 3398.dat                                                                                            0000600 0004000 0002000 00000000111 14553407552 0014263 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	129	136	t
1	128	136	t
1	131	136	f
1	132	1	f
1	130	1	t
1	133	136	f
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                       3392.dat                                                                                            0000600 0004000 0002000 00000000112 14553407552 0014256 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	Test Person	admin	admin123
136	Test Person 2	test@example.com	test
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                      3397.dat                                                                                            0000600 0004000 0002000 00000000555 14553407552 0014276 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        128	Walk Yumi	2024-01-17	00:00:00	10:10:11
129	Walk Yumid sadsadasdasdasd	2024-01-17	11:11:11	22:22:22
130	Walk Yumi, walk YYYYYYYYYYYUMASDA	2024-01-17	12:11:11	22:22:22
131	Walk Yumi aSDsadas 	2024-01-17	01:11:11	22:22:22
132	Walk Yumi asdasdasdasdas 	2024-01-17	17:11:11	23:22:22
133	Walk Yumi asdasdasdasdas asdsdasdsadasdsadas	2024-01-17	17:11:11	23:29:22
\.


                                                                                                                                                   restore.sql                                                                                         0000600 0004000 0002000 00000024304 14553407552 0015401 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE pet_scheduler_db;
--
-- Name: pet_scheduler_db; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE pet_scheduler_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_CA.UTF-8';


\connect pet_scheduler_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: clean_for_test(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.clean_for_test() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM familymembers WHERE family_id <> 1;
  DELETE FROM FAMILYTASKS;
  delete from familymembers where person_id <> 1;
   DELETE FROM tasks;
    DELETE FROM families WHERE family_id <> 1;
     DELETE FROM persons WHERE person_id <> 1;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: families; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.families (
    head_member_id integer,
    family_id integer NOT NULL
);


--
-- Name: families_new_family_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.families_new_family_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: families_new_family_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.families_new_family_id_seq OWNED BY public.families.family_id;


--
-- Name: familymembers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.familymembers (
    family_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: familytasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.familytasks (
    family_id integer NOT NULL,
    task_id integer NOT NULL,
    person_id integer,
    completed boolean DEFAULT false
);


--
-- Name: persons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.persons (
    person_id integer NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL
);


--
-- Name: persons_person_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.persons_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: persons_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tasks (
    task_id integer NOT NULL,
    name text NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    CONSTRAINT tasks_check CHECK ((end_time > start_time)),
    CONSTRAINT tasks_start_time_check CHECK (((start_time >= '00:00:00'::time without time zone) AND (start_time < '24:00:00'::time without time zone))),
    CONSTRAINT tasks_start_time_check1 CHECK (((start_time >= '00:00:00'::time without time zone) AND (start_time < '24:00:00'::time without time zone)))
);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tasks_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks.task_id;


--
-- Name: families family_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.families ALTER COLUMN family_id SET DEFAULT nextval('public.families_new_family_id_seq'::regclass);


--
-- Name: persons person_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);


--
-- Name: tasks task_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks ALTER COLUMN task_id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);


--
-- Data for Name: families; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.families (head_member_id, family_id) FROM stdin;
\.
COPY public.families (head_member_id, family_id) FROM '$$PATH$$/3393.dat';

--
-- Data for Name: familymembers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.familymembers (family_id, person_id) FROM stdin;
\.
COPY public.familymembers (family_id, person_id) FROM '$$PATH$$/3394.dat';

--
-- Data for Name: familytasks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.familytasks (family_id, task_id, person_id, completed) FROM stdin;
\.
COPY public.familytasks (family_id, task_id, person_id, completed) FROM '$$PATH$$/3398.dat';

--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.persons (person_id, name, email, password) FROM stdin;
\.
COPY public.persons (person_id, name, email, password) FROM '$$PATH$$/3392.dat';

--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tasks (task_id, name, date, start_time, end_time) FROM stdin;
\.
COPY public.tasks (task_id, name, date, start_time, end_time) FROM '$$PATH$$/3397.dat';

--
-- Name: families_new_family_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.families_new_family_id_seq', 35, true);


--
-- Name: persons_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.persons_person_id_seq', 136, true);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 133, true);


--
-- Name: families families_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (family_id);


--
-- Name: familymembers familymembers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_pkey PRIMARY KEY (family_id, person_id);


--
-- Name: familytasks familytasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_pkey PRIMARY KEY (family_id, task_id);


--
-- Name: persons primary_key_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT primary_key_email PRIMARY KEY (email);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);


--
-- Name: persons unique_person_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT unique_person_id UNIQUE (person_id);


--
-- Name: families families_head_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_head_member_id_fkey FOREIGN KEY (head_member_id) REFERENCES public.persons(person_id);


--
-- Name: familymembers familymembers_family_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(family_id);


--
-- Name: familymembers familymembers_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familymembers
    ADD CONSTRAINT familymembers_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(person_id);


--
-- Name: familytasks familytasks_family_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(family_id);


--
-- Name: familytasks familytasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.familytasks
    ADD CONSTRAINT familytasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(task_id);


--
-- Name: DATABASE pet_scheduler_db; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON DATABASE pet_scheduler_db TO ali;
GRANT ALL ON DATABASE pet_scheduler_db TO ali_admin;


--
-- Name: FUNCTION clean_for_test(); Type: ACL; Schema: public; Owner: -
--

GRANT ALL ON FUNCTION public.clean_for_test() TO ali_admin;


--
-- Name: TABLE families; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.families TO ali_admin;


--
-- Name: SEQUENCE families_new_family_id_seq; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,USAGE ON SEQUENCE public.families_new_family_id_seq TO ali_admin;


--
-- Name: TABLE familymembers; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.familymembers TO ali_admin;


--
-- Name: TABLE familytasks; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.familytasks TO ali_admin;


--
-- Name: TABLE persons; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.persons TO ali_admin;


--
-- Name: SEQUENCE persons_person_id_seq; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,USAGE ON SEQUENCE public.persons_person_id_seq TO ali_admin;


--
-- Name: TABLE tasks; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tasks TO ali_admin;


--
-- Name: SEQUENCE tasks_task_id_seq; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,USAGE ON SEQUENCE public.tasks_task_id_seq TO ali_admin;


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            