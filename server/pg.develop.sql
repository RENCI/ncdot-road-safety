--
-- PostgreSQL database dump
--

-- Dumped from database version 11.9 (Debian 11.9-1.pgdg90+1)
-- Dumped by pg_dump version 11.11 (Debian 11.11-0+deb10u1)

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

ALTER TABLE ONLY public.rs_core_userprofile DROP CONSTRAINT rs_core_userprofile_user_id_8af177c7_fk_auth_user_id;
ALTER TABLE ONLY public.rs_core_userimageannotation DROP CONSTRAINT rs_core_userimageannotation_user_id_b4b6ae62_fk_auth_user_id;
ALTER TABLE ONLY public.rs_core_userimageannotation_flags DROP CONSTRAINT rs_core_userimageann_userimageannotation__f202c898_fk_rs_core_u;
ALTER TABLE ONLY public.rs_core_userimageannotation DROP CONSTRAINT rs_core_userimageann_image_id_5dd6b7a5_fk_rs_core_r;
ALTER TABLE ONLY public.rs_core_userimageannotation_flags DROP CONSTRAINT rs_core_userimageann_annotationflag_id_cfa140bd_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_userimageannotation DROP CONSTRAINT rs_core_userimageann_annotation_id_1a04caa8_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_userannotationsummary DROP CONSTRAINT rs_core_userannotationsummary_user_id_9562dbb4_fk_auth_user_id;
ALTER TABLE ONLY public.rs_core_userannotationsummary DROP CONSTRAINT rs_core_userannotati_annotation_id_ef492547_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_holdouttestinfo DROP CONSTRAINT rs_core_holdouttesti_image_id_edfe1e99_fk_rs_core_r;
ALTER TABLE ONLY public.rs_core_holdouttestinfo DROP CONSTRAINT rs_core_holdouttesti_annotation_id_5bc95c56_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_annotationset_flags DROP CONSTRAINT rs_core_annotationse_annotationset_id_e11e56d2_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_annotationset_flags DROP CONSTRAINT rs_core_annotationse_annotationflag_id_a59b281a_fk_rs_core_a;
ALTER TABLE ONLY public.rs_core_aiimageannotation DROP CONSTRAINT rs_core_aiimageannot_image_id_efbb458d_fk_rs_core_r;
ALTER TABLE ONLY public.rs_core_aiimageannotation DROP CONSTRAINT rs_core_aiimageannot_annotation_id_5dd15dc7_fk_rs_core_a;
ALTER TABLE ONLY public.django_redirect DROP CONSTRAINT django_redirect_site_id_c3e37341_fk_django_site_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX public.rs_core_userprofile_email_aba8c941_like;
DROP INDEX public.rs_core_userimageannotation_user_id_b4b6ae62;
DROP INDEX public.rs_core_userimageannotation_image_id_5dd6b7a5_like;
DROP INDEX public.rs_core_userimageannotation_image_id_5dd6b7a5;
DROP INDEX public.rs_core_userimageannotation_flags_annotationflag_id_cfa140bd;
DROP INDEX public.rs_core_userimageannotation_annotation_id_1a04caa8_like;
DROP INDEX public.rs_core_userimageannotation_annotation_id_1a04caa8;
DROP INDEX public.rs_core_userimageannotatio_userimageannotation_id_f202c898;
DROP INDEX public.rs_core_userimageannotat_annotationflag_id_cfa140bd_like;
DROP INDEX public.rs_core_userannotationsummary_user_id_9562dbb4;
DROP INDEX public.rs_core_userannotationsummary_presence_1e2c4a87;
DROP INDEX public.rs_core_userannotationsummary_annotation_id_ef492547_like;
DROP INDEX public.rs_core_userannotationsummary_annotation_id_ef492547;
DROP INDEX public.rs_core_use_user_id_629c3d_idx;
DROP INDEX public.rs_core_use_image_i_b448f4_idx;
DROP INDEX public.rs_core_routeimage_route_id_ad5a35c3_like;
DROP INDEX public.rs_core_routeimage_route_id_ad5a35c3;
DROP INDEX public.rs_core_routeimage_location_id;
DROP INDEX public.rs_core_routeimage_image_base_name_a7b8781b_like;
DROP INDEX public.rs_core_holdouttestinfo_round_number_e7397902;
DROP INDEX public.rs_core_holdouttestinfo_presence_3719c49a;
DROP INDEX public.rs_core_holdouttestinfo_in_balance_set_b6fca210;
DROP INDEX public.rs_core_holdouttestinfo_image_id_edfe1e99_like;
DROP INDEX public.rs_core_holdouttestinfo_image_id_edfe1e99;
DROP INDEX public.rs_core_holdouttestinfo_annotation_id_5bc95c56_like;
DROP INDEX public.rs_core_holdouttestinfo_annotation_id_5bc95c56;
DROP INDEX public.rs_core_annotationset_name_281c6acf_like;
DROP INDEX public.rs_core_annotationset_flags_annotationset_id_e11e56d2_like;
DROP INDEX public.rs_core_annotationset_flags_annotationset_id_e11e56d2;
DROP INDEX public.rs_core_annotationset_flags_annotationflag_id_a59b281a_like;
DROP INDEX public.rs_core_annotationset_flags_annotationflag_id_a59b281a;
DROP INDEX public.rs_core_annotationflag_title_795975fb_like;
DROP INDEX public.rs_core_aiimageannotation_image_id_efbb458d_like;
DROP INDEX public.rs_core_aiimageannotation_image_id_efbb458d;
DROP INDEX public.rs_core_aiimageannotation_annotation_id_5dd15dc7_like;
DROP INDEX public.rs_core_aiimageannotation_annotation_id_5dd15dc7;
DROP INDEX public.rs_core_aii_uncerta_217593_idx;
DROP INDEX public.rs_core_aii_image_i_d04ca4_idx;
DROP INDEX public.rs_core_aii_annotat_a4271a_idx;
DROP INDEX public.django_site_domain_a2e37b91_like;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_redirect_site_id_c3e37341;
DROP INDEX public.django_redirect_old_path_c6cc94d3_like;
DROP INDEX public.django_redirect_old_path_c6cc94d3;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.auth_user_username_6821ab7c_like;
DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX public.auth_user_groups_group_id_97559544;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
ALTER TABLE ONLY public.rs_core_userprofile DROP CONSTRAINT rs_core_userprofile_user_id_key;
ALTER TABLE ONLY public.rs_core_userprofile DROP CONSTRAINT rs_core_userprofile_pkey;
ALTER TABLE ONLY public.rs_core_userprofile DROP CONSTRAINT rs_core_userprofile_email_key;
ALTER TABLE ONLY public.rs_core_userimageannotation DROP CONSTRAINT rs_core_userimageannotation_pkey;
ALTER TABLE ONLY public.rs_core_userimageannotation_flags DROP CONSTRAINT rs_core_userimageannotation_flags_pkey;
ALTER TABLE ONLY public.rs_core_userimageannotation_flags DROP CONSTRAINT rs_core_userimageannotat_userimageannotation_id_a_6d10d5a8_uniq;
ALTER TABLE ONLY public.rs_core_userimageannotation DROP CONSTRAINT rs_core_userimageannotat_user_id_image_id_annotat_bc441fbd_uniq;
ALTER TABLE ONLY public.rs_core_userannotationsummary DROP CONSTRAINT rs_core_userannotationsummary_pkey;
ALTER TABLE ONLY public.rs_core_routeimage DROP CONSTRAINT rs_core_routeimage_pkey;
ALTER TABLE ONLY public.rs_core_holdouttestinfo DROP CONSTRAINT rs_core_holdouttestinfo_pkey;
ALTER TABLE ONLY public.rs_core_annotationset DROP CONSTRAINT rs_core_annotationset_pkey;
ALTER TABLE ONLY public.rs_core_annotationset_flags DROP CONSTRAINT rs_core_annotationset_flags_pkey;
ALTER TABLE ONLY public.rs_core_annotationset_flags DROP CONSTRAINT rs_core_annotationset_fl_annotationset_id_annotat_8f0e7f92_uniq;
ALTER TABLE ONLY public.rs_core_annotationflag DROP CONSTRAINT rs_core_annotationflag_pkey;
ALTER TABLE ONLY public.rs_core_aiimageannotation DROP CONSTRAINT rs_core_aiimageannotation_pkey;
ALTER TABLE ONLY public.rs_core_aiimageannotation DROP CONSTRAINT rs_core_aiimageannotation_image_id_annotation_id_de79cd29_uniq;
ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_domain_a2e37b91_uniq;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_redirect DROP CONSTRAINT django_redirect_site_id_old_path_ac5dd16b_uniq;
ALTER TABLE ONLY public.django_redirect DROP CONSTRAINT django_redirect_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE public.rs_core_userprofile ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_userimageannotation_flags ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_userimageannotation ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_userannotationsummary ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_holdouttestinfo ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_annotationset_flags ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rs_core_aiimageannotation ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_redirect ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.rs_core_userprofile_id_seq;
DROP TABLE public.rs_core_userprofile;
DROP SEQUENCE public.rs_core_userimageannotation_id_seq;
DROP SEQUENCE public.rs_core_userimageannotation_flags_id_seq;
DROP TABLE public.rs_core_userimageannotation_flags;
DROP TABLE public.rs_core_userimageannotation;
DROP SEQUENCE public.rs_core_userannotationsummary_id_seq;
DROP TABLE public.rs_core_userannotationsummary;
DROP TABLE public.rs_core_routeimage;
DROP SEQUENCE public.rs_core_holdouttestinfo_id_seq;
DROP TABLE public.rs_core_holdouttestinfo;
DROP SEQUENCE public.rs_core_annotationset_flags_id_seq;
DROP TABLE public.rs_core_annotationset_flags;
DROP TABLE public.rs_core_annotationset;
DROP TABLE public.rs_core_annotationflag;
DROP SEQUENCE public.rs_core_aiimageannotation_id_seq;
DROP TABLE public.rs_core_aiimageannotation;
DROP SEQUENCE public.django_site_id_seq;
DROP TABLE public.django_site;
DROP TABLE public.django_session;
DROP SEQUENCE public.django_redirect_id_seq;
DROP TABLE public.django_redirect;
DROP SEQUENCE public.django_migrations_id_seq;
DROP TABLE public.django_migrations;
DROP SEQUENCE public.django_content_type_id_seq;
DROP TABLE public.django_content_type;
DROP SEQUENCE public.django_admin_log_id_seq;
DROP TABLE public.django_admin_log;
DROP SEQUENCE public.auth_user_user_permissions_id_seq;
DROP TABLE public.auth_user_user_permissions;
DROP SEQUENCE public.auth_user_id_seq;
DROP SEQUENCE public.auth_user_groups_id_seq;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP SEQUENCE public.auth_permission_id_seq;
DROP TABLE public.auth_permission;
DROP SEQUENCE public.auth_group_permissions_id_seq;
DROP TABLE public.auth_group_permissions;
DROP SEQUENCE public.auth_group_id_seq;
DROP TABLE public.auth_group;
DROP EXTENSION postgis_topology;
DROP EXTENSION postgis_tiger_geocoder;
DROP EXTENSION postgis;
DROP EXTENSION fuzzystrmatch;
DROP SCHEMA topology;
DROP SCHEMA tiger_data;
DROP SCHEMA tiger;
--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_redirect; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_redirect (
    id integer NOT NULL,
    site_id integer NOT NULL,
    old_path character varying(200) NOT NULL,
    new_path character varying(200) NOT NULL
);


ALTER TABLE public.django_redirect OWNER TO postgres;

--
-- Name: django_redirect_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_redirect_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_redirect_id_seq OWNER TO postgres;

--
-- Name: django_redirect_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_redirect_id_seq OWNED BY public.django_redirect.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: rs_core_aiimageannotation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_aiimageannotation (
    id integer NOT NULL,
    presence boolean,
    certainty double precision NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    annotation_id character varying(100) NOT NULL,
    image_id character varying(15) NOT NULL,
    uncertainty_measure integer,
    uncertainty_group integer
);


ALTER TABLE public.rs_core_aiimageannotation OWNER TO postgres;

--
-- Name: rs_core_aiimageannotation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_aiimageannotation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_aiimageannotation_id_seq OWNER TO postgres;

--
-- Name: rs_core_aiimageannotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_aiimageannotation_id_seq OWNED BY public.rs_core_aiimageannotation.id;


--
-- Name: rs_core_annotationflag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_annotationflag (
    title character varying(200) NOT NULL
);


ALTER TABLE public.rs_core_annotationflag OWNER TO postgres;

--
-- Name: rs_core_annotationset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_annotationset (
    name character varying(100) NOT NULL,
    type character varying(10) NOT NULL
);


ALTER TABLE public.rs_core_annotationset OWNER TO postgres;

--
-- Name: rs_core_annotationset_flags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_annotationset_flags (
    id integer NOT NULL,
    annotationset_id character varying(100) NOT NULL,
    annotationflag_id character varying(200) NOT NULL
);


ALTER TABLE public.rs_core_annotationset_flags OWNER TO postgres;

--
-- Name: rs_core_annotationset_flags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_annotationset_flags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_annotationset_flags_id_seq OWNER TO postgres;

--
-- Name: rs_core_annotationset_flags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_annotationset_flags_id_seq OWNED BY public.rs_core_annotationset_flags.id;


--
-- Name: rs_core_holdouttestinfo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_holdouttestinfo (
    id integer NOT NULL,
    round_number smallint NOT NULL,
    presence boolean NOT NULL,
    in_balance_set boolean NOT NULL,
    certainty double precision NOT NULL,
    left_certainty double precision NOT NULL,
    front_certainty double precision NOT NULL,
    right_certainty double precision NOT NULL,
    category character varying(10) NOT NULL,
    annotation_id character varying(100) NOT NULL,
    image_id character varying(15) NOT NULL,
    CONSTRAINT rs_core_holdouttestinfo_round_number_check CHECK ((round_number >= 0))
);


ALTER TABLE public.rs_core_holdouttestinfo OWNER TO postgres;

--
-- Name: rs_core_holdouttestinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_holdouttestinfo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_holdouttestinfo_id_seq OWNER TO postgres;

--
-- Name: rs_core_holdouttestinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_holdouttestinfo_id_seq OWNED BY public.rs_core_holdouttestinfo.id;


--
-- Name: rs_core_routeimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_routeimage (
    route_id character varying(20) NOT NULL,
    image_base_name character varying(15) NOT NULL,
    location public.geometry(Point,4326) NOT NULL,
    mile_post double precision,
    image_path character varying(100) NOT NULL,
    aspect_ratio double precision,
    route_index integer NOT NULL
);


ALTER TABLE public.rs_core_routeimage OWNER TO postgres;

--
-- Name: rs_core_userannotationsummary; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_userannotationsummary (
    id integer NOT NULL,
    round_number smallint NOT NULL,
    total integer NOT NULL,
    annotation_id character varying(100) NOT NULL,
    user_id integer NOT NULL,
    presence boolean NOT NULL,
    CONSTRAINT rs_core_userannotationsummary_round_number_check CHECK ((round_number >= 0))
);


ALTER TABLE public.rs_core_userannotationsummary OWNER TO postgres;

--
-- Name: rs_core_userannotationsummary_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_userannotationsummary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_userannotationsummary_id_seq OWNER TO postgres;

--
-- Name: rs_core_userannotationsummary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_userannotationsummary_id_seq OWNED BY public.rs_core_userannotationsummary.id;


--
-- Name: rs_core_userimageannotation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_userimageannotation (
    id integer NOT NULL,
    presence boolean,
    "timestamp" timestamp with time zone NOT NULL,
    comment character varying(1000),
    annotation_id character varying(100) NOT NULL,
    image_id character varying(15) NOT NULL,
    user_id integer NOT NULL,
    front_view character varying(10) NOT NULL,
    left_view character varying(10) NOT NULL,
    right_view character varying(10) NOT NULL
);


ALTER TABLE public.rs_core_userimageannotation OWNER TO postgres;

--
-- Name: rs_core_userimageannotation_flags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_userimageannotation_flags (
    id integer NOT NULL,
    userimageannotation_id integer NOT NULL,
    annotationflag_id character varying(200) NOT NULL
);


ALTER TABLE public.rs_core_userimageannotation_flags OWNER TO postgres;

--
-- Name: rs_core_userimageannotation_flags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_userimageannotation_flags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_userimageannotation_flags_id_seq OWNER TO postgres;

--
-- Name: rs_core_userimageannotation_flags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_userimageannotation_flags_id_seq OWNED BY public.rs_core_userimageannotation_flags.id;


--
-- Name: rs_core_userimageannotation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_userimageannotation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_userimageannotation_id_seq OWNER TO postgres;

--
-- Name: rs_core_userimageannotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_userimageannotation_id_seq OWNED BY public.rs_core_userimageannotation.id;


--
-- Name: rs_core_userprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_userprofile (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    organization character varying(100) NOT NULL,
    years_of_service integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT rs_core_userprofile_years_of_service_check CHECK ((years_of_service >= 0))
);


ALTER TABLE public.rs_core_userprofile OWNER TO postgres;

--
-- Name: rs_core_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rs_core_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rs_core_userprofile_id_seq OWNER TO postgres;

--
-- Name: rs_core_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rs_core_userprofile_id_seq OWNED BY public.rs_core_userprofile.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_redirect id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_redirect ALTER COLUMN id SET DEFAULT nextval('public.django_redirect_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: rs_core_aiimageannotation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_aiimageannotation ALTER COLUMN id SET DEFAULT nextval('public.rs_core_aiimageannotation_id_seq'::regclass);


--
-- Name: rs_core_annotationset_flags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset_flags ALTER COLUMN id SET DEFAULT nextval('public.rs_core_annotationset_flags_id_seq'::regclass);


--
-- Name: rs_core_holdouttestinfo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_holdouttestinfo ALTER COLUMN id SET DEFAULT nextval('public.rs_core_holdouttestinfo_id_seq'::regclass);


--
-- Name: rs_core_userannotationsummary id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userannotationsummary ALTER COLUMN id SET DEFAULT nextval('public.rs_core_userannotationsummary_id_seq'::regclass);


--
-- Name: rs_core_userimageannotation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation ALTER COLUMN id SET DEFAULT nextval('public.rs_core_userimageannotation_id_seq'::regclass);


--
-- Name: rs_core_userimageannotation_flags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation_flags ALTER COLUMN id SET DEFAULT nextval('public.rs_core_userimageannotation_flags_id_seq'::regclass);


--
-- Name: rs_core_userprofile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userprofile ALTER COLUMN id SET DEFAULT nextval('public.rs_core_userprofile_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add content type	1	add_contenttype
2	Can change content type	1	change_contenttype
3	Can delete content type	1	delete_contenttype
4	Can view content type	1	view_contenttype
5	Can add redirect	2	add_redirect
6	Can change redirect	2	change_redirect
7	Can delete redirect	2	delete_redirect
8	Can view redirect	2	view_redirect
9	Can add session	3	add_session
10	Can change session	3	change_session
11	Can delete session	3	delete_session
12	Can view session	3	view_session
13	Can add site	4	add_site
14	Can change site	4	change_site
15	Can delete site	4	delete_site
16	Can view site	4	view_site
17	Can add user profile	5	add_userprofile
18	Can change user profile	5	change_userprofile
19	Can delete user profile	5	delete_userprofile
20	Can view user profile	5	view_userprofile
21	Can add annotation set	6	add_annotationset
22	Can change annotation set	6	change_annotationset
23	Can delete annotation set	6	delete_annotationset
24	Can view annotation set	6	view_annotationset
25	Can add route image	7	add_routeimage
26	Can change route image	7	change_routeimage
27	Can delete route image	7	delete_routeimage
28	Can view route image	7	view_routeimage
29	Can add image annotation	8	add_imageannotation
30	Can change image annotation	8	change_imageannotation
31	Can delete image annotation	8	delete_imageannotation
32	Can view image annotation	8	view_imageannotation
33	Can add log entry	9	add_logentry
34	Can change log entry	9	change_logentry
35	Can delete log entry	9	delete_logentry
36	Can view log entry	9	view_logentry
37	Can add permission	10	add_permission
38	Can change permission	10	change_permission
39	Can delete permission	10	delete_permission
40	Can view permission	10	view_permission
41	Can add group	11	add_group
42	Can change group	11	change_group
43	Can delete group	11	delete_group
44	Can view group	11	view_group
45	Can add user	12	add_user
46	Can change user	12	change_user
47	Can delete user	12	delete_user
48	Can view user	12	view_user
49	Can add ai image annotation	13	add_aiimageannotation
50	Can change ai image annotation	13	change_aiimageannotation
51	Can delete ai image annotation	13	delete_aiimageannotation
52	Can view ai image annotation	13	view_aiimageannotation
53	Can add user image annotation	14	add_userimageannotation
54	Can change user image annotation	14	change_userimageannotation
55	Can delete user image annotation	14	delete_userimageannotation
56	Can view user image annotation	14	view_userimageannotation
57	Can add annotation flag	15	add_annotationflag
58	Can change annotation flag	15	change_annotationflag
59	Can delete annotation flag	15	delete_annotationflag
60	Can view annotation flag	15	view_annotationflag
61	Can add user annotation summary	16	add_userannotationsummary
62	Can change user annotation summary	16	change_userannotationsummary
63	Can delete user annotation summary	16	delete_userannotationsummary
64	Can view user annotation summary	16	view_userannotationsummary
65	Can add holdout test info	17	add_holdouttestinfo
66	Can change holdout test info	17	change_holdouttestinfo
67	Can delete holdout test info	17	delete_holdouttestinfo
68	Can view holdout test info	17	view_holdouttestinfo
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$VxU2TdJOvJ2N$PH/qimirElGmCGYgR4gzOp8jEH+JmakdRSGBHKmoLOM=	2021-06-02 19:34:34.092341+00	t	admin			hongyi@renci.org	t	t	2020-10-18 19:38:21.120339+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2020-10-18 19:39:03.860204+00	guardrail	AnnotationSet object (guardrail)	1	[{"added": {}}]	6	1
2	2020-10-18 19:39:46.814964+00	1	dotdsidev.renci.org	2	[{"changed": {"fields": ["Domain name", "Display name"]}}]	4	1
3	2020-10-18 19:39:57.740125+00	2	dotdsi.renci.org	1	[{"added": {}}]	4	1
4	2020-10-20 02:55:17.823155+00	guardrail	AnnotationSet object (guardrail)	2	[{"changed": {"fields": ["Type"]}}]	6	1
5	2020-10-24 17:09:56.313068+00	2	hongyi	2	[{"changed": {"fields": ["Active"]}}]	12	1
6	2020-10-26 21:07:19.249651+00	2	hongyi	3		12	1
7	2020-11-02 21:23:17.379354+00	3	hongyi	2	[{"changed": {"fields": ["Active"]}}]	12	1
8	2020-11-03 17:32:33.65261+00	4	borland	2	[{"changed": {"fields": ["Active"]}}]	12	1
9	2020-11-16 21:59:40.649641+00	4	borland	3		12	1
10	2020-11-17 01:19:47.359856+00	5	borland	2	[{"changed": {"fields": ["Active"]}}]	12	1
11	2020-11-17 01:57:17.142986+00	6	test	2	[{"changed": {"fields": ["Active"]}}]	12	1
12	2020-12-04 16:05:39.952498+00	5	borland	3		12	1
13	2020-12-04 16:05:40.004858+00	3	hongyi	3		12	1
14	2020-12-04 16:05:40.013197+00	6	test	3		12	1
15	2020-12-05 23:18:58.35819+00	7	hongyi	3		12	1
16	2021-01-30 20:32:53.089313+00	9	hongyi	3		12	1
17	2021-02-05 02:39:12.496948+00	10	hongyi	3		12	1
18	2021-02-11 23:03:21.653337+00	Fence	AnnotationFlag object (Fence)	1	[{"added": {}}]	15	1
19	2021-02-11 23:03:42.350911+00	Obstructed	AnnotationFlag object (Obstructed)	1	[{"added": {}}]	15	1
20	2021-02-11 23:03:57.006306+00	Edge of image	AnnotationFlag object (Edge of image)	1	[{"added": {}}]	15	1
21	2021-02-11 23:04:00.881967+00	guardrail	AnnotationSet object (guardrail)	2	[{"changed": {"fields": ["Flags"]}}]	6	1
22	2021-02-18 19:20:22.946587+00	Atypical	AnnotationFlag object (Atypical)	1	[{"added": {}}]	15	1
23	2021-02-18 19:20:26.29828+00	guardrail	AnnotationSet object (guardrail)	2	[{"changed": {"fields": ["Flags"]}}]	6	1
24	2021-02-18 19:21:25.71108+00	12	hongyi	3		12	1
25	2021-05-18 17:19:51.31494+00	pole	AnnotationSet object (pole)	1	[{"added": {}}]	6	1
26	2021-06-02 19:35:08.120981+00	2	dotdsi.renci.org	3		4	1
27	2021-06-02 19:35:15.922336+00	1	dotdsidev.renci.org	3		4	1
28	2021-06-02 19:35:34.892382+00	3	localhost:8000	1	[{"added": {}}]	4	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	contenttypes	contenttype
2	redirects	redirect
3	sessions	session
4	sites	site
5	rs_core	userprofile
6	rs_core	annotationset
7	rs_core	routeimage
8	rs_core	imageannotation
9	admin	logentry
10	auth	permission
11	auth	group
12	auth	user
13	rs_core	aiimageannotation
14	rs_core	userimageannotation
15	rs_core	annotationflag
16	rs_core	userannotationsummary
17	rs_core	holdouttestinfo
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	sites	0001_initial	2020-10-18 19:36:06.446303+00
2	sites	0002_alter_domain_unique	2020-10-18 19:36:06.455367+00
3	contenttypes	0001_initial	2020-10-18 19:36:27.911243+00
4	auth	0001_initial	2020-10-18 19:36:27.949219+00
5	admin	0001_initial	2020-10-18 19:36:27.993762+00
6	admin	0002_logentry_remove_auto_add	2020-10-18 19:36:28.010352+00
7	admin	0003_logentry_add_action_flag_choices	2020-10-18 19:36:28.020078+00
8	contenttypes	0002_remove_content_type_name	2020-10-18 19:36:28.042837+00
9	auth	0002_alter_permission_name_max_length	2020-10-18 19:36:28.053496+00
10	auth	0003_alter_user_email_max_length	2020-10-18 19:36:28.068074+00
11	auth	0004_alter_user_username_opts	2020-10-18 19:36:28.081043+00
12	auth	0005_alter_user_last_login_null	2020-10-18 19:36:28.094875+00
13	auth	0006_require_contenttypes_0002	2020-10-18 19:36:28.097412+00
14	auth	0007_alter_validators_add_error_messages	2020-10-18 19:36:28.108193+00
15	auth	0008_alter_user_username_max_length	2020-10-18 19:36:28.122665+00
16	auth	0009_alter_user_last_name_max_length	2020-10-18 19:36:28.133916+00
17	auth	0010_alter_group_name_max_length	2020-10-18 19:36:28.14668+00
18	auth	0011_update_proxy_permissions	2020-10-18 19:36:28.159943+00
19	auth	0012_alter_user_first_name_max_length	2020-10-18 19:36:28.171435+00
20	redirects	0001_initial	2020-10-18 19:36:28.179646+00
21	rs_core	0001_initial	2020-10-18 19:36:28.20492+00
22	rs_core	0002_annotationset_imageannotation_routeimage	2020-10-18 19:36:28.265805+00
23	sessions	0001_initial	2020-10-18 19:36:28.287813+00
24	rs_core	0003_auto_20201020_0217	2020-10-20 02:54:11.58419+00
25	rs_core	0004_userimageannotation_presence_views	2020-11-13 21:10:15.980006+00
26	rs_core	0005_routeimage_mile_post	2020-12-03 02:31:12.526544+00
27	rs_core	0006_auto_20201204_2020	2020-12-04 20:20:31.816796+00
28	rs_core	0007_routeimage_image_path	2021-01-07 22:11:06.738148+00
29	rs_core	0008_auto_20210127_0328	2021-01-27 03:29:06.19136+00
30	rs_core	0009_auto_20210128_1803	2021-01-28 18:04:30.577185+00
32	rs_core	0010_auto_20210204_1913	2021-02-04 19:13:54.641404+00
33	rs_core	0011_auto_20210204_2053	2021-02-04 20:53:30.456046+00
34	rs_core	0012_auto_20210204_2131	2021-02-04 21:31:22.812551+00
35	rs_core	0013_auto_20210211_2301	2021-02-11 23:01:13.865824+00
39	rs_core	0014_auto_20210217_1740	2021-02-17 17:41:12.199569+00
40	rs_core	0015_userannotationsummary	2021-04-27 20:46:05.763585+00
41	rs_core	0016_auto_20210414_2348	2021-04-27 20:46:05.952944+00
42	rs_core	0017_routeimage_aspect_ratio	2021-04-27 20:46:06.007921+00
44	rs_core	0018_holdouttestinfo	2021-05-25 20:32:38.446207+00
45	rs_core	0019_auto_20210621_2010	2021-06-21 20:10:35.908775+00
46	rs_core	0020_routeimage_route_index	2021-07-07 14:26:29.185768+00
\.


--
-- Data for Name: django_redirect; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_redirect (id, site_id, old_path, new_path) FROM stdin;
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
u9eviulplrs7p0bc1hhwwwa92dks3r40	.eJxVjMEOwiAQRP-FsyGwUIoevfsNZLe7SNXQpLQn47_bJj3ocea9mbdKuC4lrU3mNLK6KFCn345weErdAT-w3ic9THWZR9K7og_a9G1ieV0P9--gYCvbOjiKZ-59FxDQZtkSMMXsDPsYLfZoxGEGxwLZCIL1kSAYyzmThU59vup8OCE:1kWN3Q:7ErJMDvxyb0jI_hokylv5F8giuYriNTQX2jZquNuX9E	2020-11-07 17:10:08.209292+00
enhb8ychjpctt0b2lp231m2w86t4qfcu	.eJxVjMEOwiAQRP-FsyGwUIoevfsNZLe7SNXQpLQn47_bJj3ocea9mbdKuC4lrU3mNLK6KFCn345weErdAT-w3ic9THWZR9K7og_a9G1ieV0P9--gYCvbOjiKZ-59FxDQZtkSMMXsDPsYLfZoxGEGxwLZCIL1kSAYyzmThU59vup8OCE:1kWopZ:AcOPp70xiLujsSroE9jscqbSsswPwMtg66FAUX2_fG0	2020-11-08 22:49:41.069433+00
wmykzghkuckc38bcdxmiv9bdzk60zrd8	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kYJhw:O35v-UKzt4Rhm1Y0KYUVag2U-42bHKVnrATQ6CLD6Lg	2020-11-13 02:00:00.999298+00
fix3j2c3tufutl3q8ptj3atcjdfwflwr	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kYUqC:_mmRVEjJZ9v9CL5-1dx37kMXhbTDifPGlzY0OpZisok	2020-11-13 13:53:16.992727+00
8sy7ivnfettixmwysgztkl3bsxu7b6s3	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kYawl:BAEAqDahyycYokOVSQYBmvkCDeKws9ETT5ICE2vJOzY	2020-11-13 20:24:27.579048+00
9e7rtok92wkyvetikoimpl7feoq69wgv	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kYbr4:B4PDtdnphoKpWJ3mRIPIt-zSbzBYdH3M4OK0tm8yzag	2020-11-13 21:22:38.847587+00
h71ewyly6vujaxmmpgorie49i25ak1cd	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kYw9q:YJy63BDzfvPV9KoPXY_NuWfPBZ50_mmC8nAPxcScMpM	2020-11-14 19:03:22.644+00
zbv3gl05u3dyorg8oknubovt8w7pm8hg	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kZJFu:GAnTy_HtVr9xRb-A3ujnDMt3iILRfQsPCX0uQOn_2O4	2020-11-15 19:43:10.713729+00
0tomoc3njd8w5yyjpz342xblbx5ibar3	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kZLBP:-9ELgzOeiUxrcSyi_Ol880IYKw8M4kkDnW5fXvGAhkI	2020-11-15 21:46:39.122169+00
yjcil0je0ibgfo6v8h8mle72liv6hgi5	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1kZeGs:x_gHjEggfs9w5bRDUBCEV6_hHpa-zpnSXcKG1es-9H0	2020-11-16 18:09:34.711401+00
c1431o0sjk90l095bolervl2f7gul62b	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kZhIf:6ocQlvmdtzOe0Y-MeD-m5qTzcg6HYRLkQHHkVVUe3PQ	2020-11-16 21:23:37.22345+00
44fpebtyjxu87x9qfkcs53gvldsxlft1	.eJxVjEEOwiAQRe_C2hAoHQGX7nsGMjAzUjVtUtqV8e7apAvd_vfef6mE21rT1nhJI6mL6tXpd8tYHjztgO443WZd5mldxqx3RR-06WEmfl4P9--gYqvf2oMxDooNnDu0NhYMYKPtQSIgC2TnhXoiETBOvEQbHEMkBoOxk7N6fwDXOTfm:1ka0aO:FT68owrWTDxRXouvSfgeCU-_qcE1NGR98BYXVitRi40	2020-11-17 17:59:12.436855+00
xazchfd64vux21k2mcq4pbshiewa6j8b	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kaIoN:rlkdjDLQI3fJkWo8uwiWln7ZV4gL9SuqxC0NcfOUoF0	2020-11-18 13:26:51.940677+00
m4rpcyw7djlzx1m2j40ln0bioow1v0js	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kcXFn:h1NWmQBfDhHUb-U3BC3H8RsQqXlhS5f38tnpUL3oeIQ	2020-11-24 17:16:23.449639+00
18lcqdkwujnjclsm5jb1c7gjk9pel29g	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kdgOF:jUAMcsf2J8sx_MNpGPeEnrBR1DrQ_67RHTXD7xEYMAw	2020-11-27 21:13:51.593034+00
n7s1rhjo5yprr5s2fpdl1ovlic24o98r	.eJxVjEEOwiAQRe_C2hCwDiMu3fcMZGAYqRpISrsy3l2bdKHb_977LxVoXUpYe57DxOqiQB1-t0jpkesG-E711nRqdZmnqDdF77TrsXF-Xnf376BQL986Eh3FnI34NKQEwojiHQqTBWeQvXhrrAXvDMSM4DPjQDa6DGk42ajeH_ouOA8:1kephs:lI0g7XogpVmeKchNjVEShZBl5-plCmUbijaslnuKxPM	2020-12-01 01:22:52.183601+00
1jgyijeybyijn8r4syg2jv1orhmf772w	.eJxVjEEOwiAQRe_C2hCwDiMu3fcMZGAYqRpISrsy3l2bdKHb_977LxVoXUpYe57DxOqiQB1-t0jpkesG-E711nRqdZmnqDdF77TrsXF-Xnf376BQL986Eh3FnI34NKQEwojiHQqTBWeQvXhrrAXvDMSM4DPjQDa6DGk42ajeH_ouOA8:1kf29k:uzgII_1XWf8mKia5UsGCwmIaME17tuWxW-bc90z1ZpI	2020-12-01 14:40:28.681492+00
cayrdwzwmnt3gybf03jr44xilg07ibo4	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kg7fR:mZqJL5hRFgSOHwGcvneyq3C5EhocYwIa80g8wEkJDWg	2020-12-04 14:45:41.885647+00
ef9fwe9phm6w24dau3t6feh98sh5j43b	.eJxVjEEOwiAQRe_C2hCwDiMu3fcMZGAYqRpISrsy3l2bdKHb_977LxVoXUpYe57DxOqiQB1-t0jpkesG-E711nRqdZmnqDdF77TrsXF-Xnf376BQL986Eh3FnI34NKQEwojiHQqTBWeQvXhrrAXvDMSM4DPjQDa6DGk42ajeH_ouOA8:1khE4m:BTihfMRpNMNO1o0DqqBIBG_rujrOH0-ww5nuMVrM0rI	2020-12-07 15:48:24.561099+00
qja7y4y16zxbwa7g02m83859khb0upkt	.eJxVjEEOwiAQRe_C2hCwDiMu3fcMZGAYqRpISrsy3l2bdKHb_977LxVoXUpYe57DxOqiQB1-t0jpkesG-E711nRqdZmnqDdF77TrsXF-Xnf376BQL986Eh3FnI34NKQEwojiHQqTBWeQvXhrrAXvDMSM4DPjQDa6DGk42ajeH_ouOA8:1khbRC:etEN-saiZxBT-7hR-2qF0LroZ1LEREJ6_lYrJo7xffA	2020-12-08 16:45:06.773256+00
saxhug2m3wcnvfuoy8gmhsg020yypvdd	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1kheYL:cxWiHoX2_aUMKxWGVltd3YHUBQEDS3A3RLVb0zqMf5A	2020-12-08 20:04:41.865751+00
2igwt2ot8k1gckb76grqev3un5fzrnyx	.eJxVjEEOwiAQRe_C2hCgMh1duvcMZGAGqRpISrsy3l2bdKHb_977LxVoXUpYu8xhYnVWVh1-t0jpIXUDfKd6azq1usxT1Juid9r1tbE8L7v7d1Col28NwhZHyM6JN2ydWM_oPbE7DpwYB0AyHm02ESPAGJMAmyGffOYsGdT7A9yCOEA:1khelv:89VBV4QtbiuEniItdcxLUzg2ZaGrYiJKN5crcobhnqg	2020-12-08 20:18:43.653031+00
ii7ibx718ivrjfo0h3m8rjb396l1h7c4	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1khkHj:SigFqorfUYNxaFYowomgq-RtX0x6oltvOwcSxiAFYlc	2020-12-09 02:11:55.537857+00
rbqw0wchhdjc8fdllznd7tjidc3soari	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1khvsG:-42lVLGzFm7Lr8DKplZtrINXJ8iL1geYSmEzUGBxWZE	2020-12-09 14:34:24.971843+00
wb1rb8tcoajlspdufylaj9ymxh1u4q5m	.eJxVjDsOwjAQBe_iGlnxJwZT0nMG6613jQMokeKkQtwdIqWA9s3Me6mEdalpbTKngdVZOXX43Qj5IeMG-I7xNuk8jcs8kN4UvdOmrxPL87K7fwcVrX5ruEzMrsSC3IvP0pEP8K4YE3ASS8RiXQS67Izx3B8RApis7X3oItT7AyEgOM4:1khwK7:2dfI-xuuvPcdmqSProUAgtdL6OVX7OqbU2YwntTjtKs	2020-12-09 15:03:11.844433+00
tmkmm7kbkymito413djbtiaxvikl1ldi	.eJxVjEEOgjAQRe_StWlaBhjq0r1nIJ3OjKCmTSisjHdXEha6_e-9_zJj3NZp3Kos48zmbMCcfjeK6SF5B3yP-VZsKnldZrK7Yg9a7bWwPC-H-3cwxTp9ayTFNrTgmROKc4ka57QX15BHCcFzUEzSgWqng1dA6AdMgXsg8R2Z9wfqVDgX:1kjpeq:3tmCoxq-HZWvoZ_3sRNMpUFNj46Z_T98jM974kc2HQ8	2020-12-14 20:20:24.45783+00
184lhgaw03jiydtyo6fzbpevrejrk3s1	.eJxVjDkOwjAUBe_iGlnENl4o6TmD9TfjAEqkOKkQdwdLKaB8b0bzUhm2teatyZJHVmcV1OH3Q6CHTB3wHabbrGme1mVE3RW906avM8vzsrt_gQqt9qwDHIgECZNPUFzhSIBSwKZjJPInY6y3gSx7NsN3ijGeI6bopGBQ7w8eXjjR:1klE1s:zocm3tgKuYdp3oj7noj4AmbJSfFlR8AR7d_4eFbuInA	2020-12-18 16:33:56.731257+00
l4pchqy8miivko10621e4kz9eqnupvon	.eJxVjDkOwjAUBe_iGlnENl4o6TmD9TfjAEqkOKkQdwdLKaB8b0bzUhm2teatyZJHVmcV1OH3Q6CHTB3wHabbrGme1mVE3RW906avM8vzsrt_gQqt9qwDHIgECZNPUFzhSIBSwKZjJPInY6y3gSx7NsN3ijGeI6bopGBQ7w8eXjjR:1klEGW:tqExp0U5NVk4-rGEpz2-OmmmFWiJ7FM_ehNbcINmj8w	2020-12-18 16:49:04.767621+00
4klim8kk7zt0xxptqlzqmkh9vadvw1rq	.eJxVjDkOwjAUBe_iGlnENl4o6TmD9TfjAEqkOKkQdwdLKaB8b0bzUhm2teatyZJHVmcV1OH3Q6CHTB3wHabbrGme1mVE3RW906avM8vzsrt_gQqt9qwDHIgECZNPUFzhSIBSwKZjJPInY6y3gSx7NsN3ijGeI6bopGBQ7w8eXjjR:1klHfz:fPUzeeE6PqgnL05LXyTH8y4tGwsCAFT66uBxlgzTmjo	2020-12-18 20:27:35.990212+00
aevv9nhwpzqewct8sqw0lus9l2s8xrff	.eJxVjDkOwjAUBe_iGlnENl4o6TmD9TfjAEqkOKkQdwdLKaB8b0bzUhm2teatyZJHVmcV1OH3Q6CHTB3wHabbrGme1mVE3RW906avM8vzsrt_gQqt9qwDHIgECZNPUFzhSIBSwKZjJPInY6y3gSx7NsN3ijGeI6bopGBQ7w8eXjjR:1klMlh:MHDZbGx-Nt1m9tq62TUHyQWf509Zq_RxEBJBuSRd53Y	2020-12-19 01:53:49.286278+00
ievr0nfwo6cjt58icck1dtm7ivop3m62	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1klgpC:og09bk4Q8d4dop5PSBPbLpSrlkGO0927CBQghhKX5BM	2020-12-19 23:18:46.986897+00
wwwisjclw5hue4vg33kmiomjpa1x7fp2	.eJxVjDsOwjAQBe_iGllrE_8o6XMGa9drcADZUpxUiLuTSCmgfTPz3iLiupS49jzHicVFeHH63QjTM9cd8APrvcnU6jJPJHdFHrTLsXF-XQ_376BgL1ttHbEO2QcT3A2TQWSTyaqBs3boPQUF4HizrAXwnpOxis4DMTgNqMTnC_Q_N9k:1kxdVg:_fm67NWl0Q98QErBqR-00Xpf_WKpq-H5ZzWddngKj30	2021-01-21 22:12:00.321218+00
voi1mf0ms9qs5g8uj8ctjt51mbxay9qo	.eJxVjDsOwjAQBe_iGllrE_8o6XMGa9drcADZUpxUiLuTSCmgfTPz3iLiupS49jzHicVFeHH63QjTM9cd8APrvcnU6jJPJHdFHrTLsXF-XQ_376BgL1ttHbEO2QcT3A2TQWSTyaqBs3boPQUF4HizrAXwnpOxis4DMTgNqMTnC_Q_N9k:1l0sH8:3YXy2OwKBOodzAtw1fMcHEDwmTpoEP-3MYeeMMlDK_4	2021-01-30 20:34:22.702371+00
qc8tfo7idyaxaubm0vhq1kqc27riapny	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1l484e:W1jS01VV-NiuPNR0zHfmBKBCbXblmO42cyxLfTXoA4o	2021-02-08 20:02:56.293348+00
u0oj3i63xajdgvv6y3temovgw2h2sfb0	.eJxVjDkOwjAUBe_iGll4i_0p6XMG6y8WDiBHipMKcXeIlALaNzPvpTJua81bL0ueRF0UqNPvRsiP0nYgd2y3WfPc1mUivSv6oF2Ps5Tn9XD_Dir2-q05Gi5OBMl5pOSAXQgi3hsjxIDRJAvAUKy14exD8oELUjTeDi4MoN4f9ww3eQ:1l4bgr:Kex8keebqnCOhFojkJw5Dch2JnQ74wm9QkuH9qFAWhw	2021-02-10 03:40:21.074718+00
oyawtbugh4gwnlug8pmsfetwvr4xz2no	.eJxVjDkOwjAUBe_iGll4i_0p6XMG6y8WDiBHipMKcXeIlALaNzPvpTJua81bL0ueRF0UqNPvRsiP0nYgd2y3WfPc1mUivSv6oF2Ps5Tn9XD_Dir2-q05Gi5OBMl5pOSAXQgi3hsjxIDRJAvAUKy14exD8oELUjTeDi4MoN4f9ww3eQ:1l4mUK:V29mFkp-5Ap5uWL2wKiyzuRpghh3z3tHweKqXNPHaZk	2021-02-10 15:12:08.200375+00
cy5lr680gb9018a2pimm0ut6wv1a4q22	.eJxVjDkOwjAUBe_iGll4i_0p6XMG6y8WDiBHipMKcXeIlALaNzPvpTJua81bL0ueRF0UqNPvRsiP0nYgd2y3WfPc1mUivSv6oF2Ps5Tn9XD_Dir2-q05Gi5OBMl5pOSAXQgi3hsjxIDRJAvAUKy14exD8oELUjTeDi4MoN4f9ww3eQ:1l5w0P:uxYd38p7iB74kZ9XEdo0SoarthkpwhWZn2xnxPT7gRs	2021-02-13 19:34:01.728992+00
2blntajvzn3aewv6prnceudnbw14tp8z	.eJxVjDkOwjAUBe_iGll4i_0p6XMG6y8WDiBHipMKcXeIlALaNzPvpTJua81bL0ueRF0UqNPvRsiP0nYgd2y3WfPc1mUivSv6oF2Ps5Tn9XD_Dir2-q05Gi5OBMl5pOSAXQgi3hsjxIDRJAvAUKy14exD8oELUjTeDi4MoN4f9ww3eQ:1l5w7G:VKNGbL39uDz72lASxzkUrxjfPVnPMeEQQYO1huLgT7E	2021-02-13 19:41:06.970608+00
kkpxwmxfthjq67tqtiystkc1g2n2csd0	.eJxVjDkOwjAUBe_iGll4i_0p6XMG6y8WDiBHipMKcXeIlALaNzPvpTJua81bL0ueRF0UqNPvRsiP0nYgd2y3WfPc1mUivSv6oF2Ps5Tn9XD_Dir2-q05Gi5OBMl5pOSAXQgi3hsjxIDRJAvAUKy14exD8oELUjTeDi4MoN4f9ww3eQ:1l5wOg:RxLgeaJy-ymBDbcw0rTM6-WOG61TEUEcCxPWI_q07U8	2021-02-13 19:59:06.109381+00
fjyp8cqihwa7mpu709zrp3bavt94s52o	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1l5wv9:ytL_vmIGAPCeKbRbj-bI_TF9JqZtRPj0xeBeDHfAyQo	2021-02-13 20:32:39.50621+00
7o1t4i6qknxovoak8hr4vnrabjc93lh8	.eJxVjM0OwiAQhN-FsyGA_Ox69O4zkAW2UjU0Ke3J-O62SQ96m8z3zbxFpHWpce08x7GIi9BKnH7LRPnJbSflQe0-yTy1ZR6T3BV50C5vU-HX9XD_Dir1uq29xbNVztktOF0Mg0YswJSzDWDYG0BNg9fKUAgDkCZUCKBUguQZxOcLy_020Q:1l77iC:MB-EpkCsa0ngG35EVY1agmu4sZrPFPuxzOK4Rh6dH7o	2021-02-17 02:16:08.755788+00
dyyol7gbe3s4fh2q1ctoeg6lst9eq1xb	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1l7r1M:xrViW0Gvcj_qmB-fMNCri1EcJ1002FslfcipxyBJefI	2021-02-19 02:38:56.598658+00
m51cxluwmgm7o3xqnw5xrjk90tgqahoy	.eJxVjMEOwiAQRP-FsyFlgVA8evcbyC4sUjWQlPbU-O-2SQ96nHlvZhMB16WEtfMcpiSuQilx-S0J44vrQdIT66PJ2OoyTyQPRZ60y3tL_L6d7t9BwV72tXNEWo_WMpFxHjElyC7bPHrjMinwQ_aRkcwANlIG0NEw6z2CMkqLzxccgzgr:1lAL20:0p1c_-Z2tUTiKwTIcSV_oWk71TuVTyvthnQsgSAJNes	2021-02-25 23:05:52.514853+00
s50tqow9pfbfxg70p8qzno94ml9e63tk	.eJxVjMEOwiAQRP-FsyFlgVA8evcbyC4sUjWQlPbU-O-2SQ96nHlvZhMB16WEtfMcpiSuQilx-S0J44vrQdIT66PJ2OoyTyQPRZ60y3tL_L6d7t9BwV72tXNEWo_WMpFxHjElyC7bPHrjMinwQ_aRkcwANlIG0NEw6z2CMkqLzxccgzgr:1lAZqV:O2AumnR8EzO8wtsMsbCJzRjQEe-euSZLQriU2sW3dJI	2021-02-26 14:54:59.322243+00
sl7i57fpaj2lgefz6fdtz5unmjp0b0sp	.eJxVjMEOwiAQRP-FsyFlgVA8evcbyC4sUjWQlPbU-O-2SQ96nHlvZhMB16WEtfMcpiSuQilx-S0J44vrQdIT66PJ2OoyTyQPRZ60y3tL_L6d7t9BwV72tXNEWo_WMpFxHjElyC7bPHrjMinwQ_aRkcwANlIG0NEw6z2CMkqLzxccgzgr:1lBhwA:HE-AQJzgewkKZtawiTAfAMlLJdTVJ_BRE1JQxYmXHE8	2021-03-01 17:45:30.014361+00
ju4w1cxji3lxttc0nw3xuxa6vr0opyhb	.eJxVjMsOwiAQRf-FtSF0eIlL934DmWGoVA0kpV0Z_92QdKHbe865bxFx30rce17jwuIiJhCn35EwPXMdhB9Y702mVrd1ITkUedAub43z63q4fwcFexm108CendVgHDNni55sNkgGZgXehHNwagZMxMrR5DVrRYnIW2YKKD5fD4s4tg:1lCVRK:RqBG_0mIssT3OhzSy2LpzReOlN3Jl1Nn8L7Ui9TrCmc	2021-03-03 22:36:58.605791+00
khco8lq4xnw16l2hd929cn9bcs6rf01u	.eJxVjMsOwiAQRf-FtSF0eIlL934DmWGoVA0kpV0Z_92QdKHbe865bxFx30rce17jwuIiJhCn35EwPXMdhB9Y702mVrd1ITkUedAub43z63q4fwcFexm108CendVgHDNni55sNkgGZgXehHNwagZMxMrR5DVrRYnIW2YKKD5fD4s4tg:1lCkgg:zgpKLaJFSEzBUsrEVx5-Yh6obpnUJQbu3e8dxQgNUVw	2021-03-04 14:53:50.930063+00
9xdtww4nwhop2anbp6jij7ki3p9ftmnd	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1lCorR:WuPB7VeaayxchG6-Kne9cw1AS2SuhlzrwUuRjOW-n2E	2021-03-04 19:21:13.209609+00
fr9ncs35wr6l081pe3f23pn4fm0aua4n	.eJxVjDsOwjAQRO_iGllee7OxKek5g-XPggPIluKkQtydREoBzRTz3sxb-LAuxa-dZz9lcRZgxOm3jCE9ue4kP0K9N5laXeYpyl2RB-3y2jK_Lof7d1BCL9s62jyAs-oGiA5NJHCRLSkdgJRJI1qlgLfUA3MiQEdmBEyknEbiJD5fzR82Uw:1lbXHn:e6lCrhyXbOq9BPNzU37vFnDIx08ceRpRyJfkmW4fAMA	2021-05-11 23:38:35.856228+00
9yg1bgy8kkae0s5ymi4r1e491vfifdlt	.eJxVjDsOwjAQRO_iGllee7OxKek5g-XPggPIluKkQtydREoBzRTz3sxb-LAuxa-dZz9lcRZgxOm3jCE9ue4kP0K9N5laXeYpyl2RB-3y2jK_Lof7d1BCL9s62jyAs-oGiA5NJHCRLSkdgJRJI1qlgLfUA3MiQEdmBEyknEbiJD5fzR82Uw:1lbplt:X9EqU1XFuV3LxLMqy-gfm1dLLBzD8Pwf9nBleBz0sKQ	2021-05-12 19:22:53.560659+00
eqyx53o35vz1dgjenchdbqama9qygr22	.eJxVjEEOwiAQRe_C2hAHOkBduvcMZAZGqRpISrsy3l2bdKHb_977LxVpXUpcu8xxyuqkANXhd2RKD6kbyXeqt6ZTq8s8sd4UvdOuLy3L87y7fweFevnWAdJowbg8MIswOgabjBkgeDhalyn4cQwuIwBiIiCLjCxXFmfNYLx6fwDwPDdr:1ldgEB:B_14Mi9yTHzvfKg0LvE7wR0TeA1RBKI0YaJYfoSrODY	2021-05-17 21:35:43.434673+00
27kdq1aakctsav7rmx1njc13cxsrvimf	.eJxVjEEOwiAQRe_C2hAHOkBduvcMZAZGqRpISrsy3l2bdKHb_977LxVpXUpcu8xxyuqkANXhd2RKD6kbyXeqt6ZTq8s8sd4UvdOuLy3L87y7fweFevnWAdJowbg8MIswOgabjBkgeDhalyn4cQwuIwBiIiCLjCxXFmfNYLx6fwDwPDdr:1ldxiH:FIF8y7mkoXtCsHh4RLem7kOkmTfJC35p2WjPF96zJLY	2021-05-18 16:15:57.768354+00
gkaagg8o1tl2d3llgyonmswk0eciaasm	.eJxVjEEOwiAQRe_C2hAHOkBduvcMZAZGqRpISrsy3l2bdKHb_977LxVpXUpcu8xxyuqkANXhd2RKD6kbyXeqt6ZTq8s8sd4UvdOuLy3L87y7fweFevnWAdJowbg8MIswOgabjBkgeDhalyn4cQwuIwBiIiCLjCxXFmfNYLx6fwDwPDdr:1lj3O9:4asWWEiOCVdZVJbEG54Hc_VZU8p09VGfaa7xVB7d8Jc	2021-06-01 17:20:13.225256+00
joex3zt5bjln2lx4g4xpdbzj0hxojf6b	.eJxVjEEOwiAQRe_C2hAHOkBduvcMZAZGqRpISrsy3l2bdKHb_977LxVpXUpcu8xxyuqkANXhd2RKD6kbyXeqt6ZTq8s8sd4UvdOuLy3L87y7fweFevnWAdJowbg8MIswOgabjBkgeDhalyn4cQwuIwBiIiCLjCxXFmfNYLx6fwDwPDdr:1lj3tt:9Linw2vcDeFM4JjFslxP-dEwYmRIl3mlU9lS8xKmCDA	2021-06-01 17:53:01.608811+00
jgzv608702ejfgdkw1rtx9hjhll4edcr	.eJxVjMsOwiAQRf-FtSGAPAaX7vsNZHiMVA0kpV0Z_12bdKHbe865LxZwW2vYRlnCnNmFSctOv2PE9ChtJ_mO7dZ56m1d5sh3hR908Knn8rwe7t9BxVG_NUbSLqkCHqxB5XQGRQjekBDFC0nCk5LGU7LxDJApRZOIwDpCqb1i7w8RGzhc:1lj5Mc:0lBKMLykBXCrPMCBWbeV9x14_Su-3kgq1Nw8lK11Y9k	2021-06-01 19:26:46.514843+00
br57jp3awvmaqrx2bhlhjeirp5dtozj7	.eJxVjMsOwiAQRf-FtSGAPAaX7vsNZHiMVA0kpV0Z_12bdKHbe865LxZwW2vYRlnCnNmFSctOv2PE9ChtJ_mO7dZ56m1d5sh3hR908Knn8rwe7t9BxVG_NUbSLqkCHqxB5XQGRQjekBDFC0nCk5LGU7LxDJApRZOIwDpCqb1i7w8RGzhc:1lj6d3:i_UvvSMPD5pzZzKIyTI8LiPAgfiYMP4oDVe1IV0Jp2E	2021-06-01 20:47:49.506418+00
e912rkfb3dzhvm5qgijre9m8gnpwg47x	.eJxVjMsOwiAQRf-FtSGAPAaX7vsNZHiMVA0kpV0Z_12bdKHbe865LxZwW2vYRlnCnNmFSctOv2PE9ChtJ_mO7dZ56m1d5sh3hR908Knn8rwe7t9BxVG_NUbSLqkCHqxB5XQGRQjekBDFC0nCk5LGU7LxDJApRZOIwDpCqb1i7w8RGzhc:1llHub:orWPDMFWnrIYLKlzO4QSQW4wzQ7wiTV5BlV0PYg16XM	2021-06-07 21:14:57.284248+00
eq0680ial4ye5ucvop6x735x33irro3f	.eJxVjMsOwiAQRf-FtSGAPAaX7vsNZHiMVA0kpV0Z_12bdKHbe865LxZwW2vYRlnCnNmFSctOv2PE9ChtJ_mO7dZ56m1d5sh3hR908Knn8rwe7t9BxVG_NUbSLqkCHqxB5XQGRQjekBDFC0nCk5LGU7LxDJApRZOIwDpCqb1i7w8RGzhc:1llZDx:jPGDU6l52oPh0eakwvElt_n2ku4iJLQ51FN6BTewbuQ	2021-06-08 15:44:05.157182+00
pm3t9o9ec8fnlamiuq39ipfxvq9n3t6s	.eJxVjMsOwiAQRf-FtSFQXqNL935Dw8yAVA0kpV0Z_92QdKHbe865bzHHfSvz3tM6LywuQgdx-h0x0jPVQfgR671JanVbF5RDkQft8tY4va6H-3dQYi-jTgY8TVp5ZAOQswZGrdXZUciY_ORUZgdKUTY2RgZNhmwAqxx6h1l8vg7VODI:1lmcUO:IGzYj6bT_G_QUEzj5yUJKzONWfpOGCP5cO-FErJyG6U	2021-06-11 13:25:24.372263+00
0jmlv2dqjlvap4n3rjvmw0tltkwc0cvz	.eJxVjMsOwiAQRf-FtSFQXqNL935Dw8yAVA0kpV0Z_92QdKHbe865bzHHfSvz3tM6LywuQgdx-h0x0jPVQfgR671JanVbF5RDkQft8tY4va6H-3dQYi-jTgY8TVp5ZAOQswZGrdXZUciY_ORUZgdKUTY2RgZNhmwAqxx6h1l8vg7VODI:1lo7tA:22e82ifUiKgG2nsYn1Y450fT7kfZ42NZuLAlBzhYHzE	2021-06-15 17:09:12.890699+00
7bd6pcvti0u57mwkvxr476ftt4ndj03z	.eJxVjMsOwiAQRf-FtSE8Bgou3fsNZIaHVA0kpV0Z_12bdKHbe865LxZwW2vYRl7CnNiZScdOvyNhfOS2k3THdus89rYuM_Fd4Qcd_NpTfl4O9--g4qjfGjASYCmWgMBkkTxIJQxKq4wDtB5AmyKzo6loENIobxWhzqU4G3Fi7w8HSDfT:1lovHz:Q1VselPUOQRW0mZ-Qvwk9VVYM-MulfeOizZXeDgQ7sw	2021-06-17 21:54:07.396996+00
6c1fw3o5vcy8rgrbinrhjtlijpy0f6g8	.eJxVjMsOwiAQRf-FtSE8Bgou3fsNZIaHVA0kpV0Z_12bdKHbe865LxZwW2vYRl7CnNiZScdOvyNhfOS2k3THdus89rYuM_Fd4Qcd_NpTfl4O9--g4qjfGjASYCmWgMBkkTxIJQxKq4wDtB5AmyKzo6loENIobxWhzqU4G3Fi7w8HSDfT:1lpEQ0:dV_tb9JBMV7atB92B6fqD-Qkr8YzyepTTrZHC9tWH8E	2021-06-18 18:19:40.338839+00
aoelhf98kvlcucets2mukbb6a8jde87l	.eJxVjDsOwjAQBe_iGln4b1PScwZr17vBAeRIcVIh7k4ipYD2zcx7iwzrUvPaec4jiYtQSZx-R4Ty5LYTekC7T7JMbZlHlLsiD9rlbSJ-XQ_376BCr1sdKSgekFVyHrWOntF6Swls8UBoolbOGE1Rl4DesRl8NAkCpbiBsxGfLwxWN40:1lrAUx:Qkh8TqErhOfnX3UHZ4fCdEe56E6dIL8LSsujSJBNSZk	2021-06-24 02:32:47.667879+00
gio2dfrzp63k65h1tkfag85s6rbbteyt	.eJxVjDsOwjAQBe_iGln4b1PScwZr17vBAeRIcVIh7k4ipYD2zcx7iwzrUvPaec4jiYtQSZx-R4Ty5LYTekC7T7JMbZlHlLsiD9rlbSJ-XQ_376BCr1sdKSgekFVyHrWOntF6Swls8UBoolbOGE1Rl4DesRl8NAkCpbiBsxGfLwxWN40:1lstt3:mVxAmk2rUlf6a55h-F30rIeur8VC85Ul4DKCpwIDlFo	2021-06-28 21:12:49.753751+00
1a88e85ac4z3n7uzp7ow2a7g2jyxgpj3	.eJxVjEEOwiAQRe_C2hCGAgMu3XsGwsBUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIstBKn35FSfnDbSbmndptlntu6TCR3RR60y-tc-Hk53L-Dmnr91qogWANmBF901iaMiOxhICZCxSq4hFl5zg6cNyZoQhvQDVASerBavD_pBjbx:1lz0tg:DcruyZsXn_xsxNGiAp3JI5Nuedvwdtd9tyidWLHJJS8	2021-07-15 17:54:44.068001+00
o2uyvf7ztn4ur32l9msgmnrks4w18llv	.eJxVjEEOwiAQRe_C2hCGAgMu3XsGwsBUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIstBKn35FSfnDbSbmndptlntu6TCR3RR60y-tc-Hk53L-Dmnr91qogWANmBF901iaMiOxhICZCxSq4hFl5zg6cNyZoQhvQDVASerBavD_pBjbx:1m0rIP:8D1cHJSR8qlJSnowgLbCwrzzXy6K0NdFlQPEu3A9G60	2021-07-20 20:03:53.698953+00
s58q0xc2ado2ejasgfhjyy6passvwxne	.eJxVjEEOwiAQRe_C2hCGAgMu3XsGwsBUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIstBKn35FSfnDbSbmndptlntu6TCR3RR60y-tc-Hk53L-Dmnr91qogWANmBF901iaMiOxhICZCxSq4hFl5zg6cNyZoQhvQDVASerBavD_pBjbx:1m0sCC:fCgESmAYDZ5xapKf2otfCctSnjM-3Hap2HODX0rG1gc	2021-07-20 21:01:32.215349+00
yi4x3fgd776hcyo15uvd1xi1i4t2wg6h	.eJxVjEEOwiAQRe_C2hCGAgMu3XsGwsBUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIstBKn35FSfnDbSbmndptlntu6TCR3RR60y-tc-Hk53L-Dmnr91qogWANmBF901iaMiOxhICZCxSq4hFl5zg6cNyZoQhvQDVASerBavD_pBjbx:1m0sz6:kRuV-EbWNapxHwUgx66PEmeemRlqCV83VjTxEYWeBdk	2021-07-20 21:52:04.387079+00
y05as9jarfve83ofd20np89pu2wcpzkw	.eJxVjEEOwiAQRe_C2hCGAgMu3XsGwsBUqoYmpV0Z765NutDtf-_9l4hpW2vcOi9xKuIstBKn35FSfnDbSbmndptlntu6TCR3RR60y-tc-Hk53L-Dmnr91qogWANmBF901iaMiOxhICZCxSq4hFl5zg6cNyZoQhvQDVASerBavD_pBjbx:1m0t5M:SUOMxrypyHFwXNCUtqwZBHovPXTLppzYvDKKzf0QBB8	2021-07-20 21:58:32.366474+00
znjctslsiywn45s85fm5sypvwrfyc9kx	.eJxVjMsOwiAQRf-FtSFDgU7Hpft-AxkYlKqBpI-V8d-1SRe6veec-1KBt7WEbclzmESdVWfU6XeMnB657kTuXG9Np1bXeYp6V_RBFz02yc_L4f4dFF7Kt_YeuyQOMvTW0pU8I9rIDp1HMWgSuExAlgYDIMTYI5ChQSJam1Kv3h_STjaX:1m17AH:2nZ4vY46RbjrjKeeLgObaT-P63qI5TDIKmpSBiusJr8	2021-07-21 13:00:33.0938+00
3e8m2qo3nv42yr5yyqrohp2skjtw8ohk	.eJxVjMsOwiAQRf-FtSFDgU7Hpft-AxkYlKqBpI-V8d-1SRe6veec-1KBt7WEbclzmESdVWfU6XeMnB657kTuXG9Np1bXeYp6V_RBFz02yc_L4f4dFF7Kt_YeuyQOMvTW0pU8I9rIDp1HMWgSuExAlgYDIMTYI5ChQSJam1Kv3h_STjaX:1m18uH:CXbZBdlufH0fpb6z78cnx9sdH6sdLzxME9WFrY698nk	2021-07-21 14:52:09.300747+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	localhost:8000	localhost:8000
\.


--
-- Data for Name: rs_core_aiimageannotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_aiimageannotation (id, presence, certainty, "timestamp", annotation_id, image_id, uncertainty_measure, uncertainty_group) FROM stdin;
12576603	f	0	2021-01-17 16:24:11.48358+00	guardrail	15901324811	4	0
12576602	f	0	2021-01-17 16:24:11.466578+00	guardrail	15901333701	0	0
12576501	f	0.0100000000000000002	2021-01-17 16:24:07.825958+00	guardrail	16100345009	13	0
12576500	f	0.0100000000000000002	2021-01-17 16:24:07.809711+00	guardrail	16100350429	0	0
12576564	f	0	2021-01-17 16:24:10.280222+00	guardrail	16300221524	0	1
12576563	f	0	2021-01-17 16:24:10.26296+00	guardrail	16300222214	0	1
12576597	f	0	2021-01-17 16:24:11.383237+00	guardrail	22000433201	0	1
12576594	f	0.0100000000000000002	2021-01-17 16:24:11.274284+00	guardrail	22000175809	1	0
12576507	f	0.0100000000000000002	2021-01-17 16:24:08.202626+00	guardrail	30001011809	50	0
12576618	f	0.0200000000000000004	2021-01-17 16:24:11.857857+00	guardrail	30400531116	0	1
12576592	f	0.119999999999999996	2021-01-17 16:24:11.241797+00	guardrail	36001265813	8	0
12576514	f	0.0800000000000000017	2021-01-17 16:24:08.553411+00	guardrail	35801340023	49	0
12576513	f	0	2021-01-17 16:24:08.49309+00	guardrail	35801471221	0	5
12576515	f	0	2021-01-17 16:24:08.628195+00	guardrail	35701420526	0	5
12576517	f	0	2021-01-17 16:24:08.669198+00	guardrail	35701451127	0	5
12576524	f	0.0200000000000000004	2021-01-17 16:24:09.08646+00	guardrail	34400403205	0	4
12576585	f	0.0500000000000000028	2021-01-17 16:24:11.015907+00	guardrail	34801052114	0	5
12576526	f	0.0100000000000000002	2021-01-17 16:24:09.11984+00	guardrail	34400303125	0	4
12576528	f	0	2021-01-17 16:24:09.194095+00	guardrail	34400595700	34	0
12576520	f	0	2021-01-17 16:24:08.8536+00	guardrail	34400370205	0	4
12576529	f	0.0100000000000000002	2021-01-17 16:24:09.210941+00	guardrail	34400391623	0	4
12576584	f	0	2021-01-17 16:24:10.998879+00	guardrail	34800560920	0	5
12576527	f	0	2021-01-17 16:24:09.136392+00	guardrail	34400592320	0	5
12576608	f	0.0100000000000000002	2021-01-17 16:24:11.607876+00	guardrail	32400271918	14	0
12576518	f	0	2021-01-17 16:24:08.694697+00	guardrail	35700040920	0	5
12576519	f	0	2021-01-17 16:24:08.719591+00	guardrail	35700310103	0	5
12576538	f	0.0299999999999999989	2021-01-17 16:24:09.595028+00	guardrail	35501325128	31	0
12576536	f	0	2021-01-17 16:24:09.561643+00	guardrail	35501091329	0	5
12576541	f	0.0100000000000000002	2021-01-17 16:24:09.645187+00	guardrail	35501154425	0	5
12576534	f	0.0200000000000000004	2021-01-17 16:24:09.453749+00	guardrail	35501541503	0	5
12576577	f	0	2021-01-17 16:24:10.689732+00	guardrail	30500414711	0	2
12576549	t	1	2021-01-17 16:24:09.829217+00	guardrail	29901341804	0	1
12576508	f	0.0299999999999999989	2021-01-17 16:24:08.218746+00	guardrail	30000081915	0	1
12576545	f	0	2021-01-17 16:24:09.712683+00	guardrail	29901194629	0	1
12576546	f	0	2021-01-17 16:24:09.779488+00	guardrail	29901322813	0	1
12576511	f	0	2021-01-17 16:24:08.401896+00	guardrail	30000385923	0	1
12576525	f	0.0100000000000000002	2021-01-17 16:24:09.102737+00	guardrail	34400300325	0	4
12576522	f	0	2021-01-17 16:24:09.020335+00	guardrail	34400230020	0	4
12576552	f	0.200000000000000011	2021-01-17 16:24:09.921127+00	guardrail	34201521024	0	4
12576590	f	0	2021-01-17 16:24:11.174652+00	guardrail	34100221828	0	4
12576504	f	0	2021-01-17 16:24:07.968471+00	guardrail	16401215429	0	1
12576505	f	0	2021-01-17 16:24:07.984238+00	guardrail	16400161125	0	1
12576559	f	0	2021-01-17 16:24:10.196002+00	guardrail	16301184725	0	1
12576560	f	0.0299999999999999989	2021-01-17 16:24:10.212789+00	guardrail	16301022617	35	0
12576562	f	0.0200000000000000004	2021-01-17 16:24:10.24693+00	guardrail	16300504528	0	1
12576540	f	0	2021-01-17 16:24:09.627977+00	guardrail	35501070209	0	5
12576548	f	0.320000000000000007	2021-01-17 16:24:09.811699+00	guardrail	29901113229	0	1
12576547	f	0.130000000000000004	2021-01-17 16:24:09.796117+00	guardrail	29901051509	0	1
12576571	t	1	2021-01-17 16:24:10.496527+00	guardrail	29701443127	0	1
12576572	f	0.0800000000000000017	2021-01-17 16:24:10.521526+00	guardrail	29701261012	0	1
12576675	f	0.0400000000000000008	2021-01-17 16:24:13.661728+00	guardrail	30600235410	0	2
12576581	t	1	2021-01-17 16:24:10.949674+00	guardrail	31101314311	0	2
12576576	t	1	2021-01-17 16:24:10.664457+00	guardrail	30500483409	0	2
12576574	t	1	2021-01-17 16:24:10.571478+00	guardrail	30502041402	0	2
12576573	f	0.609999999999999987	2021-01-17 16:24:10.546187+00	guardrail	30501412415	0	2
12576587	f	0.0599999999999999978	2021-01-17 16:24:11.090174+00	guardrail	34100155616	0	4
12576607	f	0	2021-01-17 16:24:11.591993+00	guardrail	32400230908	0	3
12576532	f	0.0200000000000000004	2021-01-17 16:24:09.353379+00	guardrail	31200424207	0	2
12576550	f	0.0899999999999999967	2021-01-17 16:24:09.846172+00	guardrail	35401573022	4	0
12576583	f	0.0100000000000000002	2021-01-17 16:24:10.981654+00	guardrail	34801083120	0	5
12576566	f	0	2021-01-17 16:24:10.313116+00	guardrail	34901293001	0	5
12576588	f	0	2021-01-17 16:24:11.107545+00	guardrail	34100282611	35	0
12576556	f	0	2021-01-17 16:24:10.112232+00	guardrail	34200012201	0	4
12576591	f	0	2021-01-17 16:24:11.19029+00	guardrail	34101115407	0	4
12576553	f	0	2021-01-17 16:24:09.995592+00	guardrail	34200034707	6	0
12576569	f	0.429999999999999993	2021-01-17 16:24:10.447258+00	guardrail	29700553621	0	1
12576619	f	0	2021-01-17 16:24:11.875195+00	guardrail	29601422623	0	1
12576595	f	0.0100000000000000002	2021-01-17 16:24:11.291201+00	guardrail	22001512810	0	1
12576596	t	1	2021-01-17 16:24:11.307364+00	guardrail	22001132920	0	1
12576561	f	0.0100000000000000002	2021-01-17 16:24:10.230214+00	guardrail	16301023018	0	1
12576598	f	0	2021-01-17 16:24:11.398758+00	guardrail	22000431902	0	1
12576557	f	0.0100000000000000002	2021-01-17 16:24:10.129692+00	guardrail	33301120926	0	3
12576610	f	0.0100000000000000002	2021-01-17 16:24:11.642432+00	guardrail	32400325018	0	3
12576578	f	0	2021-01-17 16:24:10.714252+00	guardrail	33000215519	0	3
12576606	f	0.0100000000000000002	2021-01-17 16:24:11.574846+00	guardrail	32400355028	0	3
12576542	f	0	2021-01-17 16:24:09.662419+00	guardrail	30200062407	0	1
12576512	f	0	2021-01-17 16:24:08.47814+00	guardrail	35801404307	0	5
12576622	f	0	2021-01-17 16:24:11.925014+00	guardrail	29601521527	0	1
12576589	f	0.0100000000000000002	2021-01-17 16:24:11.157931+00	guardrail	34100321517	0	4
12576521	f	0.0100000000000000002	2021-01-17 16:24:08.910893+00	guardrail	34401091323	0	5
12576533	f	0.0899999999999999967	2021-01-17 16:24:09.369345+00	guardrail	35501425510	0	5
12576611	f	0	2021-01-17 16:24:11.657931+00	guardrail	32400313308	0	3
12576570	t	0.910000000000000031	2021-01-17 16:24:10.471244+00	guardrail	29700553101	0	1
12576575	f	0.0299999999999999989	2021-01-17 16:24:10.596479+00	guardrail	30500211224	0	2
12578223	t	0.680000000000000049	2021-05-18 17:52:22.141729+00	pole	32301091708	0	0
12576554	f	0	2021-01-17 16:24:10.012988+00	guardrail	34201070010	0	4
12576568	f	0.0400000000000000008	2021-01-17 16:24:10.388705+00	guardrail	29701315222	0	1
12576539	f	0.0100000000000000002	2021-01-17 16:24:09.612365+00	guardrail	35500575109	0	5
12576617	f	0.0100000000000000002	2021-01-17 16:24:11.842203+00	guardrail	30401232201	0	2
12576612	f	0.0200000000000000004	2021-01-17 16:24:11.675529+00	guardrail	30401244412	10	0
12576582	f	0.390000000000000013	2021-01-17 16:24:10.965531+00	guardrail	31101034815	0	2
12576502	f	0	2021-01-17 16:24:07.885578+00	guardrail	16101050612	0	1
12576558	f	0	2021-01-17 16:24:10.180577+00	guardrail	16301245502	8	0
12576565	t	1	2021-01-17 16:24:10.296137+00	guardrail	16302025413	0	1
12576717	f	0	2021-01-17 16:24:14.728783+00	guardrail	16501045000	0	1
12576720	f	0.0100000000000000002	2021-01-17 16:24:14.778834+00	guardrail	16501060119	0	1
12576670	f	0.0899999999999999967	2021-01-17 16:24:13.536098+00	guardrail	33901183127	0	4
12576632	f	0	2021-01-17 16:24:12.157894+00	guardrail	35101051713	0	5
12576662	t	1	2021-01-17 16:24:13.32751+00	guardrail	35600275009	2	0
12576626	f	0.280000000000000027	2021-01-17 16:24:11.991896+00	guardrail	35101534826	43	0
12576633	f	0.0200000000000000004	2021-01-17 16:24:12.209771+00	guardrail	35100530209	0	5
12576628	t	1	2021-01-17 16:24:12.04256+00	guardrail	35101182013	0	5
12576649	f	0	2021-01-17 16:24:12.810746+00	guardrail	32500283502	2	0
12576644	f	0.0200000000000000004	2021-01-17 16:24:12.585807+00	guardrail	32500192704	0	3
12576634	f	0.0100000000000000002	2021-01-17 16:24:12.234932+00	guardrail	31901543714	0	3
12576636	f	0.0100000000000000002	2021-01-17 16:24:12.285066+00	guardrail	31901122921	0	2
12576635	f	0.0299999999999999989	2021-01-17 16:24:12.259949+00	guardrail	31901522512	0	3
12576642	f	0.320000000000000007	2021-01-17 16:24:12.485012+00	guardrail	30901523718	0	2
12576688	t	1	2021-01-17 16:24:13.969237+00	guardrail	31401385708	0	2
12576685	f	0	2021-01-17 16:24:13.919389+00	guardrail	31400173203	0	2
12576650	f	0	2021-01-17 16:24:12.835582+00	guardrail	32600594617	0	3
12576648	f	0.0299999999999999989	2021-01-17 16:24:12.727294+00	guardrail	32501102524	0	3
12576691	f	0.0800000000000000017	2021-01-17 16:24:14.019683+00	guardrail	32700031900	0	3
12576689	f	0	2021-01-17 16:24:13.986768+00	guardrail	32700170321	0	3
12576651	f	0	2021-01-17 16:24:12.860233+00	guardrail	30301141508	0	1
12576677	t	0.969999999999999973	2021-01-17 16:24:13.693836+00	guardrail	30600283129	7	0
12576656	f	0	2021-01-17 16:24:12.985684+00	guardrail	42400515327	6	0
12578224	t	1	2021-05-18 17:52:22.170334+00	pole	32301110819	1	0
12576659	f	0	2021-01-17 16:24:13.277898+00	guardrail	42400450315	0	5
12576664	f	0	2021-01-17 16:24:13.394324+00	guardrail	35601582220	0	5
12576668	f	0	2021-01-17 16:24:13.502972+00	guardrail	35601575210	0	5
12576661	f	0	2021-01-17 16:24:13.3107+00	guardrail	35601190424	0	5
12576663	f	0	2021-01-17 16:24:13.343321+00	guardrail	35601070529	0	5
12576709	f	0	2021-01-17 16:24:14.513201+00	guardrail	35900171209	0	5
12576787	f	0	2021-01-17 16:24:16.500412+00	guardrail	34300021410	0	4
12576742	f	0.0100000000000000002	2021-01-17 16:24:15.2807+00	guardrail	34000045310	0	4
12576716	f	0	2021-01-17 16:24:14.713099+00	guardrail	30800471224	0	2
12576714	f	0	2021-01-17 16:24:14.678663+00	guardrail	30801392614	0	2
12576676	f	0.0200000000000000004	2021-01-17 16:24:13.678184+00	guardrail	30601263712	0	2
12576674	t	1	2021-01-17 16:24:13.602775+00	guardrail	30601400828	0	2
12576673	t	1	2021-01-17 16:24:13.586299+00	guardrail	30601400420	0	2
12576698	f	0.0200000000000000004	2021-01-17 16:24:14.136404+00	guardrail	31801174924	18	0
12576695	f	0	2021-01-17 16:24:14.086742+00	guardrail	31600423514	0	2
12576498	f	0.0100000000000000002	2021-01-17 16:24:07.513698+00	guardrail	33400080617	0	3
12576703	f	0.0200000000000000004	2021-01-17 16:24:14.312596+00	guardrail	33500181408	0	3
12576687	f	0.0400000000000000008	2021-01-17 16:24:13.953872+00	guardrail	31401495227	6	0
12576682	f	0.110000000000000001	2021-01-17 16:24:13.869011+00	guardrail	31501391922	1	0
12576692	f	0.0100000000000000002	2021-01-17 16:24:14.036966+00	guardrail	32700281324	24	0
12576684	t	1	2021-01-17 16:24:13.903611+00	guardrail	32801545104	0	3
12576690	f	0.0500000000000000028	2021-01-17 16:24:14.003497+00	guardrail	32700170921	0	3
12576638	t	1	2021-01-17 16:24:12.375248+00	guardrail	31900161110	0	2
12576623	f	0	2021-01-17 16:24:11.94209+00	guardrail	29601072011	0	1
12576639	f	0.0200000000000000004	2021-01-17 16:24:12.434743+00	guardrail	31900261724	0	2
12576509	f	0	2021-01-17 16:24:08.285636+00	guardrail	30000272325	0	1
12576708	f	0.0100000000000000002	2021-01-17 16:24:14.488018+00	guardrail	33501464919	0	4
12576704	t	1	2021-01-17 16:24:14.37985+00	guardrail	33501402825	0	3
12576706	f	0	2021-01-17 16:24:14.429605+00	guardrail	33501452019	0	4
12576702	f	0.0100000000000000002	2021-01-17 16:24:14.287537+00	guardrail	33501434012	0	3
12576725	t	1	2021-01-17 16:24:14.863439+00	guardrail	33700545517	0	4
12576671	t	1	2021-01-17 16:24:13.552824+00	guardrail	33901182607	0	4
12576658	f	0	2021-01-17 16:24:13.136335+00	guardrail	42400135928	0	5
12576657	f	0	2021-01-17 16:24:13.01097+00	guardrail	42400405229	0	5
12576643	f	0.0100000000000000002	2021-01-17 16:24:12.500754+00	guardrail	30901293205	0	2
12576705	f	0	2021-01-17 16:24:14.404631+00	guardrail	33500481628	0	3
12576701	f	0	2021-01-17 16:24:14.262317+00	guardrail	29800012904	0	1
12576653	f	0.0100000000000000002	2021-01-17 16:24:12.910718+00	guardrail	30301130918	0	1
12576710	f	0.0100000000000000002	2021-01-17 16:24:14.537807+00	guardrail	35902013028	0	5
12576627	f	0	2021-01-17 16:24:12.017401+00	guardrail	35100180614	0	5
12576666	f	0	2021-01-17 16:24:13.468442+00	guardrail	35600544319	0	5
12576605	f	0.0200000000000000004	2021-01-17 16:24:11.557485+00	guardrail	30100424824	0	1
12576631	f	0	2021-01-17 16:24:12.100605+00	guardrail	35100165617	0	5
12576544	f	0	2021-01-17 16:24:09.695917+00	guardrail	29901432208	0	1
12576537	f	0.0100000000000000002	2021-01-17 16:24:09.577904+00	guardrail	35501085529	0	5
12576660	f	0.0100000000000000002	2021-01-17 16:24:13.294881+00	guardrail	42400220307	0	5
12576683	t	1	2021-01-17 16:24:13.886681+00	guardrail	32801431112	0	3
12576699	f	0	2021-01-17 16:24:14.212969+00	guardrail	31801210104	0	2
12576652	f	0	2021-01-17 16:24:12.885519+00	guardrail	30300400825	0	1
12576678	f	0	2021-01-17 16:24:13.711116+00	guardrail	30600402403	0	2
12576681	f	0	2021-01-17 16:24:13.853496+00	guardrail	31500235705	0	2
12576654	f	0.0100000000000000002	2021-01-17 16:24:12.935399+00	guardrail	42401304003	0	5
12576640	f	0	2021-01-17 16:24:12.450305+00	guardrail	30901224514	0	2
12576646	f	0	2021-01-17 16:24:12.634919+00	guardrail	32501014522	0	3
12576667	f	0.160000000000000003	2021-01-17 16:24:13.486035+00	guardrail	35600501306	0	5
12576680	t	1	2021-01-17 16:24:13.79526+00	guardrail	31501442614	0	2
12576614	f	0.0100000000000000002	2021-01-17 16:24:11.792715+00	guardrail	30400214412	0	1
12576523	f	0.0100000000000000002	2021-01-17 16:24:09.069747+00	guardrail	34400070221	0	4
12576655	f	0.0100000000000000002	2021-01-17 16:24:12.960684+00	guardrail	42400183706	41	0
12576711	f	0	2021-01-17 16:24:14.613344+00	guardrail	30801333508	0	2
12576641	f	0.0100000000000000002	2021-01-17 16:24:12.467916+00	guardrail	30900553212	4	0
12576647	f	0	2021-01-17 16:24:12.660457+00	guardrail	32500201714	0	3
12576624	f	0	2021-01-17 16:24:11.959001+00	guardrail	33800281503	0	4
12576551	f	0.0100000000000000002	2021-01-17 16:24:09.862268+00	guardrail	34201040410	0	4
12576600	f	0	2021-01-17 16:24:11.43335+00	guardrail	15901225329	0	0
12576506	f	0	2021-01-17 16:24:08.052087+00	guardrail	16401575226	0	1
12576719	f	0	2021-01-17 16:24:14.763253+00	guardrail	16500135607	0	1
12576718	f	0	2021-01-17 16:24:14.746041+00	guardrail	16501580619	20	0
12576620	f	0.130000000000000004	2021-01-17 16:24:11.892257+00	guardrail	29601544005	0	1
12576724	f	0	2021-01-17 16:24:14.846467+00	guardrail	33701165814	0	4
12576741	t	1	2021-01-17 16:24:15.26351+00	guardrail	34000051510	0	4
12576726	f	0	2021-01-17 16:24:14.878993+00	guardrail	33700591706	0	4
12576727	f	0	2021-01-17 16:24:14.896487+00	guardrail	33700365512	0	4
12576723	t	1	2021-01-17 16:24:14.828921+00	guardrail	33700352823	0	4
12576700	t	1	2021-01-17 16:24:14.237865+00	guardrail	31800150015	0	2
12578225	f	0.220000000000000001	2021-05-18 17:52:22.178097+00	pole	29901051509	2	0
12576586	f	0	2021-01-17 16:24:11.07405+00	guardrail	34100205218	0	4
12576555	f	0	2021-01-17 16:24:10.096623+00	guardrail	34201362524	1	0
12576739	f	0.179999999999999993	2021-01-17 16:24:15.230344+00	guardrail	34000182102	39	0
12576743	f	0	2021-01-17 16:24:15.29621+00	guardrail	34000104729	0	4
12576740	t	0.800000000000000044	2021-01-17 16:24:15.24627+00	guardrail	34001370803	0	4
12576747	f	0.530000000000000027	2021-01-17 16:24:15.36375+00	guardrail	31001261018	0	2
12576744	f	0.0299999999999999989	2021-01-17 16:24:15.313636+00	guardrail	31001305524	0	2
12576748	f	0	2021-01-17 16:24:15.380751+00	guardrail	31001364518	0	2
12576686	f	0.0299999999999999989	2021-01-17 16:24:13.936855+00	guardrail	31401474309	0	2
12576732	t	1	2021-01-17 16:24:14.987991+00	guardrail	31300315228	0	2
12576762	f	0.0100000000000000002	2021-01-17 16:24:15.990056+00	guardrail	32301485709	0	3
12576765	f	0	2021-01-17 16:24:16.09004+00	guardrail	32301231123	0	3
12576770	f	0	2021-01-17 16:24:16.172516+00	guardrail	32300491609	0	3
12576645	f	0.0200000000000000004	2021-01-17 16:24:12.610214+00	guardrail	32500195615	0	3
12576609	f	0	2021-01-17 16:24:11.625164+00	guardrail	32400265718	0	3
12576767	f	0	2021-01-17 16:24:16.123205+00	guardrail	32300431021	0	3
12576760	f	0.140000000000000013	2021-01-17 16:24:15.923648+00	guardrail	32301204606	0	3
12576750	f	0.0500000000000000028	2021-01-17 16:24:15.456286+00	guardrail	32301242313	0	3
12576753	f	0	2021-01-17 16:24:15.589847+00	guardrail	32300441828	0	3
12576756	f	0.0100000000000000002	2021-01-17 16:24:15.689281+00	guardrail	32301354704	0	3
12576771	f	0	2021-01-17 16:24:16.190985+00	guardrail	32300473808	0	3
12576752	f	0.0100000000000000002	2021-01-17 16:24:15.498317+00	guardrail	32301174026	0	3
12576755	f	0.0100000000000000002	2021-01-17 16:24:15.671976+00	guardrail	32301141114	25	0
12576758	f	0	2021-01-17 16:24:15.815019+00	guardrail	32301100319	0	3
12576593	f	0.0100000000000000002	2021-01-17 16:24:11.257202+00	guardrail	36002001114	0	5
12576535	f	0.100000000000000006	2021-01-17 16:24:09.545605+00	guardrail	35501095409	1	0
12576712	t	1	2021-01-17 16:24:14.637423+00	guardrail	30800051125	0	2
12576715	f	0.0599999999999999978	2021-01-17 16:24:14.696851+00	guardrail	30800335719	0	2
12576780	f	0	2021-01-17 16:24:16.358368+00	guardrail	30700411425	0	2
12576779	f	0.100000000000000006	2021-01-17 16:24:16.341466+00	guardrail	30701365814	0	2
12576777	f	0	2021-01-17 16:24:16.308237+00	guardrail	30700573221	1	0
12576774	f	0	2021-01-17 16:24:16.258419+00	guardrail	35200154201	0	5
12576791	f	0	2021-01-17 16:24:16.650737+00	guardrail	34300541317	0	4
12576797	f	0	2021-01-17 16:24:16.759298+00	guardrail	34301153803	4	0
12576795	t	1	2021-01-17 16:24:16.724912+00	guardrail	34301065629	0	4
12576784	f	0	2021-01-17 16:24:16.425335+00	guardrail	34301095009	3	0
12576630	f	0	2021-01-17 16:24:12.07508+00	guardrail	35100560222	0	5
12576796	t	1	2021-01-17 16:24:16.74224+00	guardrail	34301151912	0	4
12576672	f	0.140000000000000013	2021-01-17 16:24:13.56856+00	guardrail	30600250212	0	2
12576773	f	0.0100000000000000002	2021-01-17 16:24:16.233573+00	guardrail	35201071529	0	5
12576730	f	0	2021-01-17 16:24:14.955193+00	guardrail	33600004504	0	4
12576778	f	0.599999999999999978	2021-01-17 16:24:16.323923+00	guardrail	30700322607	0	2
12576734	f	0.0200000000000000004	2021-01-17 16:24:15.030283+00	guardrail	42501082612	0	5
12576735	f	0	2021-01-17 16:24:15.055098+00	guardrail	42500034620	9	0
12576781	f	0	2021-01-17 16:24:16.3741+00	guardrail	30700384125	0	2
12576713	f	0.0100000000000000002	2021-01-17 16:24:14.662571+00	guardrail	30800570802	0	2
12576637	f	0	2021-01-17 16:24:12.359428+00	guardrail	31900403905	1	0
12576751	f	0	2021-01-17 16:24:15.481568+00	guardrail	32300171012	0	3
12576729	f	0.0400000000000000008	2021-01-17 16:24:14.937868+00	guardrail	33600375407	0	4
12576746	t	1	2021-01-17 16:24:15.346312+00	guardrail	31001021901	0	2
12576731	f	0.440000000000000002	2021-01-17 16:24:14.970917+00	guardrail	33600384827	0	4
12576721	t	1	2021-01-17 16:24:14.796327+00	guardrail	33700375929	0	4
12576738	f	0	2021-01-17 16:24:15.214043+00	guardrail	34000191222	0	4
12576769	f	0.0100000000000000002	2021-01-17 16:24:16.156712+00	guardrail	32300293221	6	0
12576782	f	0.209999999999999992	2021-01-17 16:24:16.39143+00	guardrail	34301535911	0	4
12576793	f	0	2021-01-17 16:24:16.692233+00	guardrail	34301451503	1	0
12576759	f	0	2021-01-17 16:24:15.830552+00	guardrail	32301163729	0	3
12576613	f	0	2021-01-17 16:24:11.725439+00	guardrail	30401182916	0	1
12576733	t	1	2021-01-17 16:24:15.00575+00	guardrail	42500252129	0	5
12576764	f	0	2021-01-17 16:24:16.073201+00	guardrail	32300323606	0	3
12576789	f	0.0100000000000000002	2021-01-17 16:24:16.609386+00	guardrail	34301374813	26	0
12576788	f	0	2021-01-17 16:24:16.525462+00	guardrail	34301145802	0	4
12576775	f	0	2021-01-17 16:24:16.273921+00	guardrail	30701245813	0	2
12576757	f	0	2021-01-17 16:24:15.756624+00	guardrail	32300032314	0	3
12576616	f	0.0200000000000000004	2021-01-17 16:24:11.824988+00	guardrail	30401205318	0	2
12576790	f	0	2021-01-17 16:24:16.625069+00	guardrail	34300400925	0	4
12576792	f	0	2021-01-17 16:24:16.67556+00	guardrail	34301453523	28	0
12576665	f	0.0299999999999999989	2021-01-17 16:24:13.452855+00	guardrail	35600284809	0	5
12576679	t	1	2021-01-17 16:24:13.728136+00	guardrail	30600045513	0	2
12576776	f	0	2021-01-17 16:24:16.291245+00	guardrail	30702000618	0	2
12576749	f	0.0100000000000000002	2021-01-17 16:24:15.397425+00	guardrail	31001363418	0	2
12576763	f	0	2021-01-17 16:24:16.057075+00	guardrail	32300263521	28	0
12576768	f	0	2021-01-17 16:24:16.139341+00	guardrail	32301114108	0	3
12576766	f	0	2021-01-17 16:24:16.105814+00	guardrail	32301233503	0	3
12576694	f	0.0400000000000000008	2021-01-17 16:24:14.069681+00	guardrail	32700330528	0	3
12576693	f	0.0200000000000000004	2021-01-17 16:24:14.053517+00	guardrail	32700385108	0	3
12576580	f	0	2021-01-17 16:24:10.924941+00	guardrail	33000081420	0	3
12576579	f	0	2021-01-17 16:24:10.857645+00	guardrail	33000085111	0	3
12576707	f	0	2021-01-17 16:24:14.454254+00	guardrail	33501365412	0	3
12576728	f	0	2021-01-17 16:24:14.921806+00	guardrail	33700223417	0	4
12576786	f	0.739999999999999991	2021-01-17 16:24:16.475009+00	guardrail	34301182805	0	4
12576794	f	0.0100000000000000002	2021-01-17 16:24:16.708875+00	guardrail	34301294525	0	4
12576530	f	0	2021-01-17 16:24:09.269781+00	guardrail	34400394006	0	4
12576531	f	0.0400000000000000008	2021-01-17 16:24:09.285996+00	guardrail	34401231412	0	5
12576629	t	1	2021-01-17 16:24:12.059114+00	guardrail	35101145524	0	5
12576516	f	0	2021-01-17 16:24:08.643211+00	guardrail	35700034310	0	5
12576736	t	1	2021-01-17 16:24:15.080523+00	guardrail	42501474203	0	5
12578226	t	1	2021-05-18 17:52:22.184921+00	pole	32301113829	3	0
12576599	f	0	2021-01-17 16:24:11.4161+00	guardrail	15901240029	0	0
12576503	f	0	2021-01-17 16:24:07.900363+00	guardrail	16100362400	0	1
12576621	f	0	2021-01-17 16:24:11.908624+00	guardrail	29601084513	0	1
12576567	t	1	2021-01-17 16:24:10.330452+00	guardrail	29701532424	0	1
12576510	f	0	2021-01-17 16:24:08.386159+00	guardrail	30001205208	0	1
12576543	t	1	2021-01-17 16:24:09.678123+00	guardrail	30200201401	0	1
12576615	f	0.0100000000000000002	2021-01-17 16:24:11.807716+00	guardrail	30400480726	0	1
12576745	f	0.0100000000000000002	2021-01-17 16:24:15.330898+00	guardrail	31000211513	0	2
12576862	f	0	2021-05-03 21:23:35.886725+00	guardrail	32301090008	6	0
12576808	f	0	2021-05-03 21:23:34.986908+00	guardrail	32301090028	32	0
12576809	f	0	2021-05-03 21:23:35.004029+00	guardrail	32301090228	0	0
12576807	f	0	2021-05-03 21:23:34.969535+00	guardrail	32301090318	48	0
12576810	f	0.0100000000000000002	2021-05-03 21:23:35.019606+00	guardrail	32301090329	12	0
12576864	f	0.0200000000000000004	2021-05-03 21:23:35.919321+00	guardrail	32301090409	3	0
12576811	f	0.100000000000000006	2021-05-03 21:23:35.03702+00	guardrail	32301090428	33	0
12576812	f	0	2021-05-03 21:23:35.054058+00	guardrail	32301090518	42	0
12576804	f	0	2021-05-03 21:23:34.919397+00	guardrail	32301090619	12	0
12576860	f	0	2021-05-03 21:23:35.853996+00	guardrail	32301090629	46	0
12576802	f	0	2021-05-03 21:23:34.886762+00	guardrail	32301090728	13	0
12576813	f	0	2021-05-03 21:23:35.069724+00	guardrail	32301090808	27	0
12576851	f	0	2021-05-03 21:23:35.704086+00	guardrail	32301090819	22	0
12576814	f	0	2021-05-03 21:23:35.087056+00	guardrail	32301090829	47	0
12576815	f	0	2021-05-03 21:23:35.103969+00	guardrail	32301090908	42	0
12576816	f	0	2021-05-03 21:23:35.120573+00	guardrail	32301091218	25	0
12576817	f	0	2021-05-03 21:23:35.136631+00	guardrail	32301091318	4	0
12576818	f	0	2021-05-03 21:23:35.15389+00	guardrail	32301091418	17	0
12576819	f	0	2021-05-03 21:23:35.170884+00	guardrail	32301091608	8	0
12576820	f	0	2021-05-03 21:23:35.186547+00	guardrail	32301091618	22	0
12576821	f	0	2021-05-03 21:23:35.203708+00	guardrail	32301091708	0	0
12576822	f	0	2021-05-03 21:23:35.220891+00	guardrail	32301091729	16	0
12576823	f	0	2021-05-03 21:23:35.236582+00	guardrail	32301091909	12	0
12576824	f	0	2021-05-03 21:23:35.253828+00	guardrail	32301091918	36	0
12576825	f	0	2021-05-03 21:23:35.270637+00	guardrail	32301092018	28	0
12576826	f	0	2021-05-03 21:23:35.287421+00	guardrail	32301092109	19	0
12576855	f	0	2021-05-03 21:23:35.770312+00	guardrail	32301092218	27	0
12576827	f	0	2021-05-03 21:23:35.303247+00	guardrail	32301092309	33	0
12576828	f	0.0100000000000000002	2021-05-03 21:23:35.320615+00	guardrail	32301092318	24	0
12576805	f	0.0100000000000000002	2021-05-03 21:23:34.936824+00	guardrail	32301092509	22	0
12576829	f	0	2021-05-03 21:23:35.337297+00	guardrail	32301092518	32	0
12576830	f	0.0100000000000000002	2021-05-03 21:23:35.353273+00	guardrail	32301092528	20	0
12576831	f	0.0100000000000000002	2021-05-03 21:23:35.370454+00	guardrail	32301092619	26	0
12576859	f	0.0899999999999999967	2021-05-03 21:23:35.836805+00	guardrail	32301092628	39	0
12576832	f	0.170000000000000012	2021-05-03 21:23:35.387853+00	guardrail	32301092718	33	0
12576861	f	0.0400000000000000008	2021-05-03 21:23:35.869399+00	guardrail	32301092809	48	0
12576858	f	0.0200000000000000004	2021-05-03 21:23:35.819661+00	guardrail	32301092828	18	0
12576847	f	0.0100000000000000002	2021-05-03 21:23:35.637979+00	guardrail	32301092908	45	0
12576848	f	0	2021-05-03 21:23:35.65368+00	guardrail	32301092929	8	0
12576801	f	0.0100000000000000002	2021-05-03 21:23:34.869364+00	guardrail	32301093009	2	0
12576833	f	0.0700000000000000067	2021-05-03 21:23:35.403497+00	guardrail	32301093229	16	0
12576799	f	0.0200000000000000004	2021-05-03 21:23:34.83766+00	guardrail	32301093309	49	0
12576834	f	0.0299999999999999989	2021-05-03 21:23:35.421072+00	guardrail	32301093318	29	0
12576835	t	1	2021-05-03 21:23:35.437886+00	guardrail	32301093518	39	0
12576854	t	1	2021-05-03 21:23:35.754658+00	guardrail	32301093708	9	0
12576845	t	1	2021-05-03 21:23:35.603392+00	guardrail	32301093818	39	0
12576853	t	1	2021-05-03 21:23:35.737938+00	guardrail	32301094118	49	0
12576836	t	1	2021-05-03 21:23:35.453708+00	guardrail	32301094129	23	0
12576798	t	1	2021-05-03 21:23:34.735931+00	guardrail	32301094308	14	0
12576844	t	1	2021-05-03 21:23:35.587816+00	guardrail	32301094329	11	0
12576837	t	1	2021-05-03 21:23:35.470829+00	guardrail	32301094508	3	0
12576838	t	1	2021-05-03 21:23:35.487519+00	guardrail	32301094519	34	0
12576839	t	1	2021-05-03 21:23:35.503498+00	guardrail	32301094609	48	0
12576800	t	1	2021-05-03 21:23:34.853357+00	guardrail	32301094709	43	0
12576850	t	1	2021-05-03 21:23:35.688087+00	guardrail	32301094718	40	0
12576849	t	1	2021-05-03 21:23:35.670753+00	guardrail	32301094729	12	0
12576840	t	1	2021-05-03 21:23:35.520927+00	guardrail	32301094818	42	0
12576803	t	1	2021-05-03 21:23:34.903821+00	guardrail	32301095008	19	0
12576846	t	1	2021-05-03 21:23:35.620892+00	guardrail	32301095029	24	0
12576857	t	1	2021-05-03 21:23:35.804231+00	guardrail	32301095108	48	0
12576841	f	0	2021-05-03 21:23:35.537896+00	guardrail	32301095608	10	0
12576806	f	0	2021-05-03 21:23:34.953755+00	guardrail	32301095708	40	0
12576842	f	0	2021-05-03 21:23:35.553453+00	guardrail	32301095718	39	0
12576843	f	0	2021-05-03 21:23:35.571062+00	guardrail	32301095728	47	0
12576852	f	0.0299999999999999989	2021-05-03 21:23:35.720412+00	guardrail	32301095918	11	0
12576761	f	0	2021-01-17 16:24:15.938625+00	guardrail	32301201706	0	3
12576754	t	0.949999999999999956	2021-01-17 16:24:15.655984+00	guardrail	32301503324	0	3
12576499	t	1	2021-01-17 16:24:07.743568+00	guardrail	33401471905	0	3
12576722	f	0	2021-01-17 16:24:14.813334+00	guardrail	33701302323	0	4
12576625	f	0	2021-01-17 16:24:11.974616+00	guardrail	33800504204	0	4
12576669	f	0	2021-01-17 16:24:13.518758+00	guardrail	33901500703	0	4
12576785	t	0.839999999999999969	2021-01-17 16:24:16.450587+00	guardrail	34301333500	0	4
12576772	f	0	2021-01-17 16:24:16.208322+00	guardrail	35200250623	0	5
12576737	f	0	2021-01-17 16:24:15.147578+00	guardrail	42501115001	0	5
12576954	f	0.160000000000000003	2021-05-03 21:23:37.420868+00	guardrail	32301084429	17	0
12576968	f	0.479999999999999982	2021-05-03 21:23:37.655279+00	guardrail	32301084508	12	0
12576969	f	0.140000000000000013	2021-05-03 21:23:37.671748+00	guardrail	32301084528	19	0
12576970	f	0.0800000000000000017	2021-05-03 21:23:37.687755+00	guardrail	32301084619	49	0
12576955	f	0.0200000000000000004	2021-05-03 21:23:37.438335+00	guardrail	32301084628	11	0
12576956	f	0	2021-05-03 21:23:37.455308+00	guardrail	32301084808	13	0
12576971	f	0	2021-05-03 21:23:37.704365+00	guardrail	32301084818	3	0
12576957	f	0	2021-05-03 21:23:37.471213+00	guardrail	32301084908	32	0
12576951	f	0	2021-05-03 21:23:37.370717+00	guardrail	32301084918	43	0
12576966	f	0.0299999999999999989	2021-05-03 21:23:37.622028+00	guardrail	32301085018	33	0
12576958	f	0	2021-05-03 21:23:37.488584+00	guardrail	32301085208	18	0
12576964	f	0	2021-05-03 21:23:37.587675+00	guardrail	32301085228	8	0
12576959	f	0	2021-05-03 21:23:37.505052+00	guardrail	32301085318	8	0
12576952	f	0	2021-05-03 21:23:37.388235+00	guardrail	32301085418	0	0
12576961	f	0	2021-05-03 21:23:37.537579+00	guardrail	32301085518	37	0
12576962	f	0	2021-05-03 21:23:37.555107+00	guardrail	32301085609	11	0
12576965	f	0	2021-05-03 21:23:37.605149+00	guardrail	32301085719	11	0
12576963	f	0	2021-05-03 21:23:37.572116+00	guardrail	32301085809	10	0
12576921	f	0	2021-05-03 21:23:36.870662+00	guardrail	32301090108	16	0
12576922	f	0	2021-05-03 21:23:36.887837+00	guardrail	32301090118	20	0
12576923	f	0	2021-05-03 21:23:36.905014+00	guardrail	32301090128	45	0
12576924	f	0	2021-05-03 21:23:36.920606+00	guardrail	32301090208	34	0
12576926	f	0.0200000000000000004	2021-05-03 21:23:36.955132+00	guardrail	32301090418	6	0
12576927	f	0	2021-05-03 21:23:36.970765+00	guardrail	32301090608	30	0
12576928	f	0	2021-05-03 21:23:36.988077+00	guardrail	32301090708	35	0
12576866	f	0	2021-05-03 21:23:35.953879+00	guardrail	32301090919	3	0
12576867	f	0	2021-05-03 21:23:35.969252+00	guardrail	32301090928	0	0
12576868	f	0	2021-05-03 21:23:35.986717+00	guardrail	32301091008	20	0
12576929	f	0	2021-05-03 21:23:37.005316+00	guardrail	32301091018	2	0
12576930	f	0	2021-05-03 21:23:37.020806+00	guardrail	32301091029	24	0
12576931	f	0	2021-05-03 21:23:37.038169+00	guardrail	32301091118	18	0
12576919	f	0	2021-05-03 21:23:36.837916+00	guardrail	32301091128	47	0
12576870	f	0	2021-05-03 21:23:36.019406+00	guardrail	32301091308	38	0
12576871	f	0	2021-05-03 21:23:36.036623+00	guardrail	32301091409	29	0
12576872	f	0	2021-05-03 21:23:36.053824+00	guardrail	32301091509	36	0
12576873	f	0	2021-05-03 21:23:36.069314+00	guardrail	32301091519	16	0
12576874	f	0	2021-05-03 21:23:36.086715+00	guardrail	32301091718	11	0
12576875	f	0.0400000000000000008	2021-05-03 21:23:36.104018+00	guardrail	32301091809	43	0
12576933	f	0	2021-05-03 21:23:37.070848+00	guardrail	32301091829	7	0
12576877	f	0	2021-05-03 21:23:36.13669+00	guardrail	32301092009	47	0
12576878	f	0	2021-05-03 21:23:36.153943+00	guardrail	32301092028	25	0
12576934	f	0	2021-05-03 21:23:37.088167+00	guardrail	32301092128	18	0
12576935	f	0	2021-05-03 21:23:37.10533+00	guardrail	32301092208	43	0
12576936	f	0	2021-05-03 21:23:37.120979+00	guardrail	32301092408	8	0
12576937	f	0	2021-05-03 21:23:37.138429+00	guardrail	32301092418	36	0
12576938	f	0.0100000000000000002	2021-05-03 21:23:37.155145+00	guardrail	32301092428	40	0
12576940	f	0.119999999999999996	2021-05-03 21:23:37.188221+00	guardrail	32301092709	4	0
12576916	f	0.0400000000000000008	2021-05-03 21:23:36.788495+00	guardrail	32301092729	3	0
12576879	f	0.0599999999999999978	2021-05-03 21:23:36.169438+00	guardrail	32301092819	2	0
12576880	f	0	2021-05-03 21:23:36.186774+00	guardrail	32301092919	44	0
12576881	f	0.0100000000000000002	2021-05-03 21:23:36.203842+00	guardrail	32301093018	30	0
12576882	f	0.220000000000000001	2021-05-03 21:23:36.22039+00	guardrail	32301093108	25	0
12576915	f	0.0299999999999999989	2021-05-03 21:23:36.770532+00	guardrail	32301093119	11	0
12576941	f	0.110000000000000001	2021-05-03 21:23:37.205313+00	guardrail	32301093128	1	0
12576884	f	0.0899999999999999967	2021-05-03 21:23:36.253582+00	guardrail	32301093219	48	0
12576885	t	0.979999999999999982	2021-05-03 21:23:36.270598+00	guardrail	32301093328	5	0
12576886	t	0.959999999999999964	2021-05-03 21:23:36.287906+00	guardrail	32301093409	34	0
12576887	t	1	2021-05-03 21:23:36.303336+00	guardrail	32301093428	45	0
12576942	t	1	2021-05-03 21:23:37.220759+00	guardrail	32301093508	5	0
12576943	t	1	2021-05-03 21:23:37.238285+00	guardrail	32301093529	9	0
12576950	t	1	2021-05-03 21:23:37.355403+00	guardrail	32301093608	31	0
12576910	t	1	2021-05-03 21:23:36.687848+00	guardrail	32301093628	12	0
12576948	t	1	2021-05-03 21:23:37.320879+00	guardrail	32301093729	46	0
12576947	t	1	2021-05-03 21:23:37.305398+00	guardrail	32301093909	11	0
12576888	t	1	2021-05-03 21:23:36.320626+00	guardrail	32301093929	10	0
12576889	t	1	2021-05-03 21:23:36.338161+00	guardrail	32301094019	38	0
12576944	t	1	2021-05-03 21:23:37.255359+00	guardrail	32301094028	1	0
12576917	t	1	2021-05-03 21:23:36.804949+00	guardrail	32301094208	17	0
12576913	t	1	2021-05-03 21:23:36.737674+00	guardrail	32301094219	0	0
12576909	t	1	2021-05-03 21:23:36.670217+00	guardrail	32301094228	25	0
12576912	t	1	2021-05-03 21:23:36.72047+00	guardrail	32301094318	48	0
12576949	t	1	2021-05-03 21:23:37.3383+00	guardrail	32301094429	32	0
12576891	t	1	2021-05-03 21:23:36.37053+00	guardrail	32301094618	9	0
12576892	t	1	2021-05-03 21:23:36.387745+00	guardrail	32301094629	29	0
12576914	t	1	2021-05-03 21:23:36.754907+00	guardrail	32301094808	13	0
12576893	t	1	2021-05-03 21:23:36.403464+00	guardrail	32301094829	34	0
12576894	t	1	2021-05-03 21:23:36.420785+00	guardrail	32301094909	22	0
12576895	t	1	2021-05-03 21:23:36.438088+00	guardrail	32301094918	15	0
12576896	t	1	2021-05-03 21:23:36.453363+00	guardrail	32301095118	6	0
12576898	f	0	2021-05-03 21:23:36.488224+00	guardrail	32301095208	14	0
12576899	f	0	2021-05-03 21:23:36.503478+00	guardrail	32301095229	49	0
12576945	f	0.0100000000000000002	2021-05-03 21:23:37.270906+00	guardrail	32301095309	35	0
12576900	f	0	2021-05-03 21:23:36.521076+00	guardrail	32301095409	33	0
12576901	f	0	2021-05-03 21:23:36.53801+00	guardrail	32301095418	18	0
12576902	f	0	2021-05-03 21:23:36.553501+00	guardrail	32301095429	9	0
12576920	f	0	2021-05-03 21:23:36.854959+00	guardrail	32301095508	39	0
12576903	f	0.0100000000000000002	2021-05-03 21:23:36.570601+00	guardrail	32301095518	34	0
12576905	f	0	2021-05-03 21:23:36.604676+00	guardrail	32301095629	7	0
12576906	f	0	2021-05-03 21:23:36.620432+00	guardrail	32301095809	14	0
12576907	f	0	2021-05-03 21:23:36.637929+00	guardrail	32301095819	3	0
12576908	f	0	2021-05-03 21:23:36.654651+00	guardrail	32301095928	43	0
12576988	f	0.0100000000000000002	2021-05-03 21:23:37.988253+00	guardrail	32301084608	32	0
12576973	f	0.0200000000000000004	2021-05-03 21:23:37.737721+00	guardrail	32301085009	0	0
12576974	f	0.0100000000000000002	2021-05-03 21:23:37.754472+00	guardrail	32301085028	1	0
12576975	f	0.239999999999999991	2021-05-03 21:23:37.772421+00	guardrail	32301085109	17	0
12576977	f	0	2021-05-03 21:23:37.805285+00	guardrail	32301085218	25	0
12576978	f	0	2021-05-03 21:23:37.821041+00	guardrail	32301085308	46	0
12576989	f	0	2021-05-03 21:23:38.005173+00	guardrail	32301085408	45	0
12576979	f	0.0100000000000000002	2021-05-03 21:23:37.838347+00	guardrail	32301085428	7	0
12576980	f	0	2021-05-03 21:23:37.855516+00	guardrail	32301085618	30	0
12576981	f	0	2021-05-03 21:23:37.871035+00	guardrail	32301085628	25	0
12576982	f	0	2021-05-03 21:23:37.888405+00	guardrail	32301085709	23	0
12576984	f	0	2021-05-03 21:23:37.921095+00	guardrail	32301085828	11	0
12576985	f	0	2021-05-03 21:23:37.938418+00	guardrail	32301085908	18	0
12576986	f	0	2021-05-03 21:23:37.956169+00	guardrail	32301085918	4	0
12576987	f	0	2021-05-03 21:23:37.971648+00	guardrail	32301085928	30	0
12577026	f	0	2021-05-03 21:23:38.65619+00	guardrail	32301100219	33	0
12577027	f	0	2021-05-03 21:23:38.673599+00	guardrail	32301100229	3	0
12577014	f	0	2021-05-03 21:23:38.422825+00	guardrail	32301100308	12	0
12577028	f	0	2021-05-03 21:23:38.698109+00	guardrail	32301100328	43	0
12577024	f	0	2021-05-03 21:23:38.590034+00	guardrail	32301100409	37	0
12577075	f	0	2021-05-03 21:23:39.523778+00	guardrail	32301100428	40	0
12577029	f	0	2021-05-03 21:23:38.715155+00	guardrail	32301100509	9	0
12577015	f	0	2021-05-03 21:23:38.439912+00	guardrail	32301100518	12	0
12577030	f	0	2021-05-03 21:23:38.732264+00	guardrail	32301100528	2	0
12577031	f	0	2021-05-03 21:23:38.747809+00	guardrail	32301100629	38	0
12576993	f	0.0100000000000000002	2021-05-03 21:23:38.072331+00	guardrail	32301100709	37	0
12576995	f	0	2021-05-03 21:23:38.105166+00	guardrail	32301100729	22	0
12576996	f	0	2021-05-03 21:23:38.122489+00	guardrail	32301100829	24	0
12576998	f	0	2021-05-03 21:23:38.155311+00	guardrail	32301101019	26	0
12577033	f	0	2021-05-03 21:23:38.782487+00	guardrail	32301101128	28	0
12576999	f	0	2021-05-03 21:23:38.172467+00	guardrail	32301101209	29	0
12577034	f	0.0100000000000000002	2021-05-03 21:23:38.798043+00	guardrail	32301101229	12	0
12577035	f	0	2021-05-03 21:23:38.815241+00	guardrail	32301101308	0	0
12577000	f	0	2021-05-03 21:23:38.189216+00	guardrail	32301101329	30	0
12577036	f	0	2021-05-03 21:23:38.831155+00	guardrail	32301101408	37	0
12577037	f	0	2021-05-03 21:23:38.84855+00	guardrail	32301101528	20	0
12577001	f	0	2021-05-03 21:23:38.20705+00	guardrail	32301101618	5	0
12577038	f	0	2021-05-03 21:23:38.86513+00	guardrail	32301101728	37	0
12577040	f	0.0700000000000000067	2021-05-03 21:23:38.897796+00	guardrail	32301101829	2	0
12577002	f	0	2021-05-03 21:23:38.222548+00	guardrail	32301102029	15	0
12577022	f	0	2021-05-03 21:23:38.557248+00	guardrail	32301102109	6	0
12577041	f	0	2021-05-03 21:23:38.915062+00	guardrail	32301102118	14	0
12577042	f	0	2021-05-03 21:23:38.932248+00	guardrail	32301102208	15	0
12576991	f	0	2021-05-03 21:23:38.037775+00	guardrail	32301102309	48	0
12577043	f	0.0200000000000000004	2021-05-03 21:23:38.947763+00	guardrail	32301102318	19	0
12577044	f	0	2021-05-03 21:23:38.965398+00	guardrail	32301102329	36	0
12576992	f	0	2021-05-03 21:23:38.055102+00	guardrail	32301102408	38	0
12577045	f	0	2021-05-03 21:23:38.982575+00	guardrail	32301102419	12	0
12577010	f	0	2021-05-03 21:23:38.357117+00	guardrail	32301102508	8	0
12577009	f	0	2021-05-03 21:23:38.339931+00	guardrail	32301102519	42	0
12577047	f	0.0100000000000000002	2021-05-03 21:23:39.031995+00	guardrail	32301102628	15	0
12577020	f	0	2021-05-03 21:23:38.522732+00	guardrail	32301102708	5	0
12577048	f	0	2021-05-03 21:23:39.047938+00	guardrail	32301102809	11	0
12577049	f	0	2021-05-03 21:23:39.065286+00	guardrail	32301102828	44	0
12577003	f	0	2021-05-03 21:23:38.239897+00	guardrail	32301102919	18	0
12576994	f	0	2021-05-03 21:23:38.088076+00	guardrail	32301103008	30	0
12577050	f	0	2021-05-03 21:23:39.082328+00	guardrail	32301103108	21	0
12577005	f	0	2021-05-03 21:23:38.272633+00	guardrail	32301103318	12	0
12577051	f	0.0100000000000000002	2021-05-03 21:23:39.097992+00	guardrail	32301103409	24	0
12577052	f	0.0100000000000000002	2021-05-03 21:23:39.115592+00	guardrail	32301103418	29	0
12577054	f	0	2021-05-03 21:23:39.148781+00	guardrail	32301103518	37	0
12577013	f	0	2021-05-03 21:23:38.40702+00	guardrail	32301103529	13	0
12577077	f	0	2021-05-03 21:23:39.556724+00	guardrail	32301103808	48	0
12577017	f	0	2021-05-03 21:23:38.472811+00	guardrail	32301103919	2	0
12577055	f	0	2021-05-03 21:23:39.165832+00	guardrail	32301104009	31	0
12577056	f	0	2021-05-03 21:23:39.18133+00	guardrail	32301104018	49	0
12577057	f	0	2021-05-03 21:23:39.207229+00	guardrail	32301104108	24	0
12577058	f	0	2021-05-03 21:23:39.223091+00	guardrail	32301104129	37	0
12577078	f	0	2021-05-03 21:23:39.574096+00	guardrail	32301104208	26	0
12577019	f	0	2021-05-03 21:23:38.506918+00	guardrail	32301104318	2	0
12577006	f	0	2021-05-03 21:23:38.289963+00	guardrail	32301104509	40	0
12577007	f	0	2021-05-03 21:23:38.306833+00	guardrail	32301104518	21	0
12577059	f	0	2021-05-03 21:23:39.240197+00	guardrail	32301104609	4	0
12577076	f	0.0200000000000000004	2021-05-03 21:23:39.540923+00	guardrail	32301104809	37	0
12577061	f	0	2021-05-03 21:23:39.273001+00	guardrail	32301104829	33	0
12577062	f	0	2021-05-03 21:23:39.2902+00	guardrail	32301104908	8	0
12577023	f	0	2021-05-03 21:23:38.572813+00	guardrail	32301104918	36	0
12577063	f	0	2021-05-03 21:23:39.307362+00	guardrail	32301104928	24	0
12577064	f	0	2021-05-03 21:23:39.322958+00	guardrail	32301105008	26	0
12577065	f	0	2021-05-03 21:23:39.340334+00	guardrail	32301105018	40	0
12577008	f	0	2021-05-03 21:23:38.322687+00	guardrail	32301105028	44	0
12577066	f	0	2021-05-03 21:23:39.357527+00	guardrail	32301105108	8	0
12577068	f	0	2021-05-03 21:23:39.390389+00	guardrail	32301105229	17	0
12577012	f	0	2021-05-03 21:23:38.3897+00	guardrail	32301105408	48	0
12577069	f	0	2021-05-03 21:23:39.424091+00	guardrail	32301105418	33	0
12577070	f	0	2021-05-03 21:23:39.440583+00	guardrail	32301105428	35	0
12577016	f	0	2021-05-03 21:23:38.457186+00	guardrail	32301105609	32	0
12577071	f	0	2021-05-03 21:23:39.456665+00	guardrail	32301105618	36	0
12577072	f	0	2021-05-03 21:23:39.473816+00	guardrail	32301105628	28	0
12577073	f	0.0100000000000000002	2021-05-03 21:23:39.491392+00	guardrail	32301105729	22	0
12577021	f	0.0100000000000000002	2021-05-03 21:23:38.539986+00	guardrail	32301105819	37	0
12577087	f	0	2021-05-03 21:23:39.740941+00	guardrail	32301100109	4	0
12577088	f	0	2021-05-03 21:23:39.75652+00	guardrail	32301100118	6	0
12577089	f	0	2021-05-03 21:23:39.773778+00	guardrail	32301100609	0	0
12577091	f	0.0200000000000000004	2021-05-03 21:23:39.806428+00	guardrail	32301100808	18	0
12577092	f	0	2021-05-03 21:23:39.823833+00	guardrail	32301101008	1	0
12577093	f	0	2021-05-03 21:23:39.840875+00	guardrail	32301101029	19	0
12577086	f	0.0100000000000000002	2021-05-03 21:23:39.723745+00	guardrail	32301101108	20	0
12577094	f	0.0100000000000000002	2021-05-03 21:23:39.856366+00	guardrail	32301101119	26	0
12577095	f	0	2021-05-03 21:23:39.874249+00	guardrail	32301101219	49	0
12577080	f	0	2021-05-03 21:23:39.624733+00	guardrail	32301101319	2	0
12577096	f	0	2021-05-03 21:23:39.889887+00	guardrail	32301101429	15	0
12577098	f	0.0100000000000000002	2021-05-03 21:23:39.924243+00	guardrail	32301101519	4	0
12577099	f	0	2021-05-03 21:23:39.939941+00	guardrail	32301101629	34	0
12577100	f	0	2021-05-03 21:23:39.957144+00	guardrail	32301101708	16	0
12577101	f	0	2021-05-03 21:23:39.974712+00	guardrail	32301101809	2	0
12577102	f	0	2021-05-03 21:23:39.990048+00	guardrail	32301101928	30	0
12577103	f	0	2021-05-03 21:23:40.007544+00	guardrail	32301102018	15	0
12577084	f	0	2021-05-03 21:23:39.690822+00	guardrail	32301102219	3	0
12577105	f	0	2021-05-03 21:23:40.04059+00	guardrail	32301102228	17	0
12577106	f	0	2021-05-03 21:23:40.057808+00	guardrail	32301102528	36	0
12577107	f	0	2021-05-03 21:23:40.07331+00	guardrail	32301102619	2	0
12577108	f	0	2021-05-03 21:23:40.090723+00	guardrail	32301102718	4	0
12577081	f	0	2021-05-03 21:23:39.640256+00	guardrail	32301102728	40	0
12577082	f	0	2021-05-03 21:23:39.656479+00	guardrail	32301102818	32	0
12577085	f	0	2021-05-03 21:23:39.706461+00	guardrail	32301103018	39	0
12577109	f	0	2021-05-03 21:23:40.10785+00	guardrail	32301103028	45	0
12577110	f	0.0100000000000000002	2021-05-03 21:23:40.123542+00	guardrail	32301103119	11	0
12577112	f	0	2021-05-03 21:23:40.158137+00	guardrail	32301103208	8	0
12577113	f	0.0100000000000000002	2021-05-03 21:23:40.173423+00	guardrail	32301103229	26	0
12577114	f	0.0100000000000000002	2021-05-03 21:23:40.190728+00	guardrail	32301103308	4	0
12577115	f	0	2021-05-03 21:23:40.208058+00	guardrail	32301103329	8	0
12577116	f	0.0100000000000000002	2021-05-03 21:23:40.223445+00	guardrail	32301103618	46	0
12577117	f	0	2021-05-03 21:23:40.240794+00	guardrail	32301103628	6	0
12577119	f	0	2021-05-03 21:23:40.274688+00	guardrail	32301103829	5	0
12577120	f	0.0100000000000000002	2021-05-03 21:23:40.290251+00	guardrail	32301103909	35	0
12577121	f	0	2021-05-03 21:23:40.307566+00	guardrail	32301103928	20	0
12577122	f	0	2021-05-03 21:23:40.32457+00	guardrail	32301104028	42	0
12577123	f	0	2021-05-03 21:23:40.340075+00	guardrail	32301104118	23	0
12577124	f	0	2021-05-03 21:23:40.357501+00	guardrail	32301104219	13	0
12577126	f	0	2021-05-03 21:23:40.390193+00	guardrail	32301104328	11	0
12577127	f	0	2021-05-03 21:23:40.407477+00	guardrail	32301104418	22	0
12577142	f	0	2021-05-03 21:23:40.658196+00	guardrail	32301104429	37	0
12577128	f	0	2021-05-03 21:23:40.4246+00	guardrail	32301104529	24	0
12577129	f	0	2021-05-03 21:23:40.440336+00	guardrail	32301104618	47	0
12577143	f	0	2021-05-03 21:23:40.673591+00	guardrail	32301104718	49	0
12577130	f	0.0100000000000000002	2021-05-03 21:23:40.45788+00	guardrail	32301104818	15	0
12577131	f	0	2021-05-03 21:23:40.474695+00	guardrail	32301105118	49	0
12577133	f	0	2021-05-03 21:23:40.508039+00	guardrail	32301105318	23	0
12577134	f	0	2021-05-03 21:23:40.523705+00	guardrail	32301105329	49	0
12577135	f	0.0100000000000000002	2021-05-03 21:23:40.541443+00	guardrail	32301105519	34	0
12577136	f	0	2021-05-03 21:23:40.558057+00	guardrail	32301105708	11	0
12577137	f	0	2021-05-03 21:23:40.573562+00	guardrail	32301105719	6	0
12577138	f	0.0100000000000000002	2021-05-03 21:23:40.590919+00	guardrail	32301105809	17	0
12577140	f	0	2021-05-03 21:23:40.623858+00	guardrail	32301105918	1	0
12577141	f	0	2021-05-03 21:23:40.641054+00	guardrail	32301105929	36	0
12577185	f	0	2021-05-03 21:23:41.432267+00	guardrail	32301112009	40	0
12577179	f	0	2021-05-03 21:23:41.332537+00	guardrail	32301113428	26	0
12577183	f	0	2021-05-03 21:23:41.399999+00	guardrail	32301113629	30	0
12577180	f	0.0100000000000000002	2021-05-03 21:23:41.349629+00	guardrail	32301114308	29	0
12577182	f	0	2021-05-03 21:23:41.382493+00	guardrail	32301114328	27	0
12577184	f	0.450000000000000011	2021-05-03 21:23:41.416863+00	guardrail	32301115209	49	0
12577145	f	0	2021-05-03 21:23:40.708082+00	guardrail	32301120008	47	0
12577150	f	0	2021-05-03 21:23:40.791005+00	guardrail	32301120018	18	0
12577151	f	0	2021-05-03 21:23:40.808086+00	guardrail	32301120028	4	0
12577152	f	0.0100000000000000002	2021-05-03 21:23:40.823693+00	guardrail	32301120108	25	0
12577154	f	0	2021-05-03 21:23:40.858199+00	guardrail	32301120128	30	0
12577155	f	0.0200000000000000004	2021-05-03 21:23:40.873681+00	guardrail	32301120218	18	0
12577144	f	0.0100000000000000002	2021-05-03 21:23:40.691012+00	guardrail	32301120228	19	0
12577156	f	0.0100000000000000002	2021-05-03 21:23:40.890979+00	guardrail	32301120309	30	0
12577147	f	0.0100000000000000002	2021-05-03 21:23:40.741088+00	guardrail	32301120319	5	0
12577157	f	0.0299999999999999989	2021-05-03 21:23:40.908152+00	guardrail	32301120328	30	0
12577158	f	0.23000000000000001	2021-05-03 21:23:40.923655+00	guardrail	32301120418	9	0
12577159	f	0.0500000000000000028	2021-05-03 21:23:40.941058+00	guardrail	32301120428	19	0
12577161	f	0.140000000000000013	2021-05-03 21:23:40.973736+00	guardrail	32301120528	0	0
12577177	f	0.0200000000000000004	2021-05-03 21:23:41.299709+00	guardrail	32301120608	1	0
12577162	f	0.0200000000000000004	2021-05-03 21:23:40.991255+00	guardrail	32301120619	23	0
12577178	f	0.0299999999999999989	2021-05-03 21:23:41.316799+00	guardrail	32301120628	31	0
12577149	f	0.0100000000000000002	2021-05-03 21:23:40.773657+00	guardrail	32301120708	5	0
12577163	f	0.0299999999999999989	2021-05-03 21:23:41.008366+00	guardrail	32301120718	0	0
12577164	f	0.190000000000000002	2021-05-03 21:23:41.023813+00	guardrail	32301120809	33	0
12577165	f	0.739999999999999991	2021-05-03 21:23:41.04153+00	guardrail	32301120818	24	0
12577166	t	0.810000000000000053	2021-05-03 21:23:41.058174+00	guardrail	32301120829	32	0
12577176	t	0.969999999999999973	2021-05-03 21:23:41.282664+00	guardrail	32301120908	2	0
12577148	f	0.479999999999999982	2021-05-03 21:23:40.758133+00	guardrail	32301120918	8	0
12577168	f	0.23000000000000001	2021-05-03 21:23:41.090663+00	guardrail	32301121019	42	0
12577169	f	0.419999999999999984	2021-05-03 21:23:41.166705+00	guardrail	32301121028	15	0
12577170	t	0.869999999999999996	2021-05-03 21:23:41.182947+00	guardrail	32301121108	15	0
12577171	t	1	2021-05-03 21:23:41.199254+00	guardrail	32301121118	44	0
12577172	t	0.939999999999999947	2021-05-03 21:23:41.216744+00	guardrail	32301121208	10	0
12577173	t	1	2021-05-03 21:23:41.232272+00	guardrail	32301121218	7	0
12577175	f	0	2021-05-03 21:23:41.26672+00	guardrail	32301121308	23	0
12577247	f	0	2021-05-03 21:23:42.516203+00	guardrail	32301110019	41	0
12577248	f	0	2021-05-03 21:23:42.533766+00	guardrail	32301110109	37	0
12577187	f	0	2021-05-03 21:23:41.466875+00	guardrail	32301110119	18	0
12577188	f	0	2021-05-03 21:23:41.482364+00	guardrail	32301110129	47	0
12577249	f	0.0100000000000000002	2021-05-03 21:23:42.550767+00	guardrail	32301110209	40	0
12577250	f	0	2021-05-03 21:23:42.566456+00	guardrail	32301110219	18	0
12577244	f	0	2021-05-03 21:23:42.466958+00	guardrail	32301110228	30	0
12577251	f	0	2021-05-03 21:23:42.583884+00	guardrail	32301110308	1	0
12577252	f	0	2021-05-03 21:23:42.600892+00	guardrail	32301110318	14	0
12577189	f	0	2021-05-03 21:23:41.499979+00	guardrail	32301110329	43	0
12577254	f	0	2021-05-03 21:23:42.633643+00	guardrail	32301110419	1	0
12577255	f	0	2021-05-03 21:23:42.650657+00	guardrail	32301110609	33	0
12577191	f	0	2021-05-03 21:23:41.532348+00	guardrail	32301110619	21	0
12577256	f	0	2021-05-03 21:23:42.666342+00	guardrail	32301110629	35	0
12577192	f	0	2021-05-03 21:23:41.549714+00	guardrail	32301110709	40	0
12577257	f	0	2021-05-03 21:23:42.683751+00	guardrail	32301110809	35	0
12577258	f	0	2021-05-03 21:23:42.700661+00	guardrail	32301110829	18	0
12577259	f	0	2021-05-03 21:23:42.716312+00	guardrail	32301110909	3	0
12577193	f	0	2021-05-03 21:23:41.56668+00	guardrail	32301110919	40	0
12577194	f	0	2021-05-03 21:23:41.582495+00	guardrail	32301110929	36	0
12577261	f	0	2021-05-03 21:23:42.750737+00	guardrail	32301111029	5	0
12577195	f	0	2021-05-03 21:23:41.599547+00	guardrail	32301111119	36	0
12577196	f	0	2021-05-03 21:23:41.616598+00	guardrail	32301111129	19	0
12577198	f	0	2021-05-03 21:23:41.648987+00	guardrail	32301111228	0	0
12577262	f	0.0200000000000000004	2021-05-03 21:23:42.766089+00	guardrail	32301111318	39	0
12577263	f	0.0100000000000000002	2021-05-03 21:23:42.783445+00	guardrail	32301111328	36	0
12577199	f	0.0299999999999999989	2021-05-03 21:23:41.666502+00	guardrail	32301111419	6	0
12577264	f	0.0100000000000000002	2021-05-03 21:23:42.800385+00	guardrail	32301111428	26	0
12577265	f	0.0100000000000000002	2021-05-03 21:23:42.816719+00	guardrail	32301111508	12	0
12577266	f	0	2021-05-03 21:23:42.833566+00	guardrail	32301111529	21	0
12577200	f	0	2021-05-03 21:23:41.691899+00	guardrail	32301111619	40	0
12577201	f	0	2021-05-03 21:23:41.707503+00	guardrail	32301111629	2	0
12577202	f	0	2021-05-03 21:23:41.72491+00	guardrail	32301111709	32	0
12577203	f	0	2021-05-03 21:23:41.741955+00	guardrail	32301111719	6	0
12577205	f	0	2021-05-03 21:23:41.775497+00	guardrail	32301111828	5	0
12577268	f	0	2021-05-03 21:23:42.866158+00	guardrail	32301111918	38	0
12577206	f	0	2021-05-03 21:23:41.790834+00	guardrail	32301111928	29	0
12577269	f	0	2021-05-03 21:23:42.883777+00	guardrail	32301112018	45	0
12577270	f	0	2021-05-03 21:23:42.900971+00	guardrail	32301112129	4	0
12577207	f	0	2021-05-03 21:23:41.807892+00	guardrail	32301112219	9	0
12577243	f	0	2021-05-03 21:23:42.450978+00	guardrail	32301112229	19	0
12577208	f	0	2021-05-03 21:23:41.825048+00	guardrail	32301112309	3	0
12577209	f	0	2021-05-03 21:23:41.840768+00	guardrail	32301112319	38	0
12577271	f	0	2021-05-03 21:23:42.916653+00	guardrail	32301112329	3	0
12577210	f	0.0599999999999999978	2021-05-03 21:23:41.858117+00	guardrail	32301112429	49	0
12577272	f	0.0100000000000000002	2021-05-03 21:23:42.933999+00	guardrail	32301112509	30	0
12577273	f	0	2021-05-03 21:23:42.951044+00	guardrail	32301112519	1	0
12577212	f	0.0299999999999999989	2021-05-03 21:23:41.909261+00	guardrail	32301112619	37	0
12577245	f	0	2021-05-03 21:23:42.483736+00	guardrail	32301112629	22	0
12577213	f	0	2021-05-03 21:23:41.924559+00	guardrail	32301112709	33	0
12577275	f	0	2021-05-03 21:23:42.984061+00	guardrail	32301112719	30	0
12577276	f	0	2021-05-03 21:23:43.000786+00	guardrail	32301112728	10	0
12577277	f	0	2021-05-03 21:23:43.016515+00	guardrail	32301112808	3	0
12577214	f	0	2021-05-03 21:23:41.942102+00	guardrail	32301112829	31	0
12577215	f	0	2021-05-03 21:23:41.957525+00	guardrail	32301112909	5	0
12577278	f	0	2021-05-03 21:23:43.034828+00	guardrail	32301112918	45	0
12577216	f	0.0100000000000000002	2021-05-03 21:23:41.974882+00	guardrail	32301113019	4	0
12577279	f	0.0100000000000000002	2021-05-03 21:23:43.051732+00	guardrail	32301113108	40	0
12577280	f	0	2021-05-03 21:23:43.07645+00	guardrail	32301113209	6	0
12577217	f	0	2021-05-03 21:23:41.992032+00	guardrail	32301113218	29	0
12577219	f	0	2021-05-03 21:23:42.024983+00	guardrail	32301113418	16	0
12577220	f	0	2021-05-03 21:23:42.042335+00	guardrail	32301113508	9	0
12577282	f	0	2021-05-03 21:23:43.108574+00	guardrail	32301113518	12	0
12577283	f	0	2021-05-03 21:23:43.125601+00	guardrail	32301113529	40	0
12577221	f	0	2021-05-03 21:23:42.057848+00	guardrail	32301113609	6	0
12577284	f	0	2021-05-03 21:23:43.14291+00	guardrail	32301113719	37	0
12577285	f	0.0100000000000000002	2021-05-03 21:23:43.158735+00	guardrail	32301113729	5	0
12577286	f	0.0100000000000000002	2021-05-03 21:23:43.175935+00	guardrail	32301113809	19	0
12577287	f	0	2021-05-03 21:23:43.192407+00	guardrail	32301113819	29	0
12577222	f	0.0299999999999999989	2021-05-03 21:23:42.075117+00	guardrail	32301113909	4	0
12577223	f	0	2021-05-03 21:23:42.100519+00	guardrail	32301113929	38	0
12577289	f	0	2021-05-03 21:23:43.226023+00	guardrail	32301114028	10	0
12577290	f	0.0100000000000000002	2021-05-03 21:23:43.243015+00	guardrail	32301114228	16	0
12577224	f	0	2021-05-03 21:23:42.124828+00	guardrail	32301114318	29	0
12577291	f	0	2021-05-03 21:23:43.258628+00	guardrail	32301114418	26	0
12577226	f	0	2021-05-03 21:23:42.157726+00	guardrail	32301114509	15	0
12577292	f	0	2021-05-03 21:23:43.276048+00	guardrail	32301114519	15	0
12577227	f	0	2021-05-03 21:23:42.175+00	guardrail	32301114609	41	0
12577242	f	0	2021-05-03 21:23:42.432762+00	guardrail	32301114629	19	0
12577228	f	0	2021-05-03 21:23:42.192127+00	guardrail	32301114709	4	0
12577229	f	0.0100000000000000002	2021-05-03 21:23:42.207652+00	guardrail	32301114819	34	0
12577230	f	0	2021-05-03 21:23:42.225013+00	guardrail	32301115009	44	0
12577231	f	0.0200000000000000004	2021-05-03 21:23:42.242065+00	guardrail	32301115018	9	0
12577233	f	0	2021-05-03 21:23:42.274911+00	guardrail	32301115318	15	0
12577234	f	0	2021-05-03 21:23:42.300612+00	guardrail	32301115518	46	0
12577235	f	0.0100000000000000002	2021-05-03 21:23:42.316884+00	guardrail	32301115529	6	0
12577236	f	0	2021-05-03 21:23:42.332864+00	guardrail	32301115618	31	0
12577237	f	0	2021-05-03 21:23:42.35021+00	guardrail	32301115628	38	0
12577241	f	0	2021-05-03 21:23:42.41744+00	guardrail	32301115729	35	0
12577238	f	0	2021-05-03 21:23:42.367068+00	guardrail	32301115809	35	0
12577240	f	0	2021-05-03 21:23:42.399835+00	guardrail	32301115928	47	0
12577373	f	0.0899999999999999967	2021-05-03 21:23:44.636032+00	guardrail	32301084519	11	0
12577338	f	0.0100000000000000002	2021-05-03 21:23:44.042888+00	guardrail	32301084718	40	0
12577337	f	0	2021-05-03 21:23:44.025556+00	guardrail	32301085118	10	0
12577375	f	0	2021-05-03 21:23:44.676344+00	guardrail	32301085508	25	0
12577376	f	0.0800000000000000017	2021-05-03 21:23:44.69312+00	guardrail	32301085818	1	0
12577377	f	0	2021-05-03 21:23:44.710098+00	guardrail	32301090309	36	0
12577378	f	0.0100000000000000002	2021-05-03 21:23:44.725551+00	guardrail	32301090508	9	0
12577379	f	0	2021-05-03 21:23:44.743054+00	guardrail	32301090529	43	0
12577329	f	0	2021-05-03 21:23:43.893012+00	guardrail	32301091109	27	0
12577380	f	0.0100000000000000002	2021-05-03 21:23:44.760113+00	guardrail	32301091328	2	0
12577365	f	0	2021-05-03 21:23:44.492476+00	guardrail	32301091429	29	0
12577366	f	0	2021-05-03 21:23:44.509851+00	guardrail	32301091628	29	0
12577328	f	0	2021-05-03 21:23:43.876163+00	guardrail	32301091818	10	0
12577382	f	0	2021-05-03 21:23:44.792906+00	guardrail	32301092119	24	0
12577383	f	0.0700000000000000067	2021-05-03 21:23:44.810266+00	guardrail	32301092229	20	0
12577330	f	0	2021-05-03 21:23:43.909857+00	guardrail	32301092328	45	0
12577384	f	0.0700000000000000067	2021-05-03 21:23:44.825607+00	guardrail	32301093028	44	0
12577331	t	0.859999999999999987	2021-05-03 21:23:43.925724+00	guardrail	32301093419	27	0
12577333	t	1	2021-05-03 21:23:43.960016+00	guardrail	32301093718	34	0
12577334	t	1	2021-05-03 21:23:43.975638+00	guardrail	32301093809	13	0
12577385	t	1	2021-05-03 21:23:44.842982+00	guardrail	32301093918	38	0
12577386	t	1	2021-05-03 21:23:44.860372+00	guardrail	32301094009	22	0
12577336	t	1	2021-05-03 21:23:44.009933+00	guardrail	32301094409	46	0
12577387	t	1	2021-05-03 21:23:44.875969+00	guardrail	32301094529	11	0
12577390	t	1	2021-05-03 21:23:44.925894+00	guardrail	32301094929	39	0
12577335	t	1	2021-05-03 21:23:43.993003+00	guardrail	32301095019	28	0
12577359	f	0.0100000000000000002	2021-05-03 21:23:44.392451+00	guardrail	32301095318	0	0
12577369	f	0	2021-05-03 21:23:44.568754+00	guardrail	32301095618	39	0
12577389	f	0	2021-05-03 21:23:44.910799+00	guardrail	32301095908	36	0
12577364	f	0	2021-05-03 21:23:44.476498+00	guardrail	32301100009	18	0
12577358	f	0	2021-05-03 21:23:44.376859+00	guardrail	32301100019	29	0
12577363	f	0	2021-05-03 21:23:44.460045+00	guardrail	32301100029	3	0
12577391	f	0	2021-05-03 21:23:44.94321+00	guardrail	32301100128	5	0
12577392	f	0	2021-05-03 21:23:44.960169+00	guardrail	32301100818	33	0
12577393	f	0.0400000000000000008	2021-05-03 21:23:44.976129+00	guardrail	32301100908	43	0
12577340	f	0.0200000000000000004	2021-05-03 21:23:44.076262+00	guardrail	32301100929	10	0
12577368	f	0	2021-05-03 21:23:44.544343+00	guardrail	32301101418	36	0
12577394	f	0	2021-05-03 21:23:44.993369+00	guardrail	32301101718	25	0
12577341	f	0.0200000000000000004	2021-05-03 21:23:44.092386+00	guardrail	32301101908	0	0
12577396	f	0	2021-05-03 21:23:45.025858+00	guardrail	32301102009	4	0
12577342	f	0	2021-05-03 21:23:44.109707+00	guardrail	32301102429	29	0
12577397	f	0	2021-05-03 21:23:45.043356+00	guardrail	32301102908	4	0
12577398	f	0.0200000000000000004	2021-05-03 21:23:45.060094+00	guardrail	32301102929	17	0
12577343	f	0.0299999999999999989	2021-05-03 21:23:44.126733+00	guardrail	32301103428	44	0
12577344	f	0	2021-05-03 21:23:44.142607+00	guardrail	32301103608	2	0
12577345	f	0	2021-05-03 21:23:44.159792+00	guardrail	32301103709	28	0
12577399	f	0	2021-05-03 21:23:45.076167+00	guardrail	32301103718	11	0
12577372	f	0	2021-05-03 21:23:44.618045+00	guardrail	32301103728	12	0
12577347	f	0	2021-05-03 21:23:44.192622+00	guardrail	32301105529	18	0
12577309	f	0.0100000000000000002	2021-05-03 21:23:43.558519+00	guardrail	32301110009	31	0
12577310	f	0	2021-05-03 21:23:43.576171+00	guardrail	32301110029	15	0
12577350	f	0	2021-05-03 21:23:44.242472+00	guardrail	32301110519	44	0
12577371	f	0	2021-05-03 21:23:44.600969+00	guardrail	32301110729	21	0
12577312	f	0	2021-05-03 21:23:43.609079+00	guardrail	32301111009	2	0
12577313	f	0	2021-05-03 21:23:43.626526+00	guardrail	32301111218	28	0
12577314	f	0	2021-05-03 21:23:43.641975+00	guardrail	32301111729	15	0
12577351	f	0	2021-05-03 21:23:44.259554+00	guardrail	32301111808	3	0
12577352	f	0	2021-05-03 21:23:44.276778+00	guardrail	32301111909	26	0
12577315	f	0	2021-05-03 21:23:43.659404+00	guardrail	32301112119	5	0
12577307	f	0	2021-05-03 21:23:43.526017+00	guardrail	32301112209	48	0
12577354	f	0	2021-05-03 21:23:44.309823+00	guardrail	32301112419	23	0
12577355	f	0	2021-05-03 21:23:44.326573+00	guardrail	32301112818	9	0
12577316	f	0	2021-05-03 21:23:43.676226+00	guardrail	32301113008	45	0
12577317	f	0	2021-05-03 21:23:43.693082+00	guardrail	32301113029	34	0
12577356	f	0	2021-05-03 21:23:44.342608+00	guardrail	32301113318	29	0
12577308	f	0	2021-05-03 21:23:43.54302+00	guardrail	32301113328	16	0
12577319	f	0	2021-05-03 21:23:43.726151+00	guardrail	32301113619	21	0
12577361	f	0	2021-05-03 21:23:44.426731+00	guardrail	32301113709	17	0
12577320	f	0	2021-05-03 21:23:43.74299+00	guardrail	32301113829	14	0
12577321	f	0	2021-05-03 21:23:43.759041+00	guardrail	32301114118	18	0
12577322	f	0	2021-05-03 21:23:43.776253+00	guardrail	32301114408	3	0
12577294	f	0	2021-05-03 21:23:43.309345+00	guardrail	32301114719	13	0
12577362	f	0	2021-05-03 21:23:44.442487+00	guardrail	32301114729	28	0
12577295	f	0	2021-05-03 21:23:43.325858+00	guardrail	32301114809	45	0
12577296	f	0	2021-05-03 21:23:43.343039+00	guardrail	32301114829	17	0
12577323	f	0.0100000000000000002	2021-05-03 21:23:43.793094+00	guardrail	32301114928	36	0
12577298	f	0.0100000000000000002	2021-05-03 21:23:43.375879+00	guardrail	32301115028	37	0
12577299	f	0.0299999999999999989	2021-05-03 21:23:43.393006+00	guardrail	32301115118	12	0
12577324	f	0.0899999999999999967	2021-05-03 21:23:43.808707+00	guardrail	32301115128	15	0
12577300	f	0.0299999999999999989	2021-05-03 21:23:43.408512+00	guardrail	32301115229	0	0
12577301	f	0	2021-05-03 21:23:43.425784+00	guardrail	32301115309	15	0
12577370	f	0	2021-05-03 21:23:44.584202+00	guardrail	32301115409	22	0
12577302	f	0	2021-05-03 21:23:43.443359+00	guardrail	32301115419	12	0
12577357	f	0	2021-05-03 21:23:44.360021+00	guardrail	32301115428	5	0
12577303	f	0	2021-05-03 21:23:43.458743+00	guardrail	32301115509	35	0
12577326	f	0	2021-05-03 21:23:43.843478+00	guardrail	32301115609	18	0
12577305	f	0	2021-05-03 21:23:43.493057+00	guardrail	32301115719	15	0
12577306	f	0	2021-05-03 21:23:43.508636+00	guardrail	32301115828	48	0
12577327	f	0	2021-05-03 21:23:43.858947+00	guardrail	32301115918	18	0
12577348	f	0.390000000000000013	2021-05-03 21:23:44.209851+00	guardrail	32301120508	28	0
12577349	f	0.369999999999999996	2021-05-03 21:23:44.226604+00	guardrail	32301121009	20	0
12576967	f	0.100000000000000006	2021-05-03 21:23:37.63783+00	guardrail	32301084418	38	0
12576953	f	0.270000000000000018	2021-05-03 21:23:37.405362+00	guardrail	32301084709	45	0
12577339	f	0	2021-05-03 21:23:44.059871+00	guardrail	32301084728	20	0
12576972	f	0.130000000000000004	2021-05-03 21:23:37.72105+00	guardrail	32301084929	5	0
12576976	f	0	2021-05-03 21:23:37.788917+00	guardrail	32301085128	1	0
12576960	f	0.0599999999999999978	2021-05-03 21:23:37.521853+00	guardrail	32301085329	27	0
12576990	f	0	2021-05-03 21:23:38.022605+00	guardrail	32301085528	42	0
12576983	f	0	2021-05-03 21:23:37.905532+00	guardrail	32301085729	2	0
12576863	f	0	2021-05-03 21:23:35.903882+00	guardrail	32301090018	36	0
12576925	f	0.260000000000000009	2021-05-03 21:23:36.937948+00	guardrail	32301090218	45	0
12576865	f	0	2021-05-03 21:23:35.936656+00	guardrail	32301090718	14	0
12576869	f	0.0100000000000000002	2021-05-03 21:23:36.003847+00	guardrail	32301091208	44	0
12576932	f	0	2021-05-03 21:23:37.055382+00	guardrail	32301091228	19	0
12576876	f	0	2021-05-03 21:23:36.119355+00	guardrail	32301091928	5	0
12576939	f	0.0100000000000000002	2021-05-03 21:23:37.170882+00	guardrail	32301092608	28	0
12576883	f	0.340000000000000024	2021-05-03 21:23:36.236197+00	guardrail	32301093208	25	0
12576918	t	1	2021-05-03 21:23:36.820446+00	guardrail	32301093618	25	0
12576946	t	1	2021-05-03 21:23:37.288485+00	guardrail	32301093829	34	0
12576890	t	1	2021-05-03 21:23:36.353149+00	guardrail	32301094109	46	0
12576911	t	1	2021-05-03 21:23:36.704816+00	guardrail	32301094418	33	0
12576897	t	0.959999999999999964	2021-05-03 21:23:36.470464+00	guardrail	32301095128	14	0
12576856	f	0	2021-05-03 21:23:35.787559+00	guardrail	32301095219	23	0
12576904	f	0	2021-05-03 21:23:36.587769+00	guardrail	32301095529	23	0
12577332	f	0	2021-05-03 21:23:43.943068+00	guardrail	32301095828	43	0
12577025	f	0	2021-05-03 21:23:38.640733+00	guardrail	32301100208	24	0
12577018	f	0	2021-05-03 21:23:38.490083+00	guardrail	32301100418	42	0
12577090	f	0	2021-05-03 21:23:39.790892+00	guardrail	32301100619	42	0
12576997	f	0.0100000000000000002	2021-05-03 21:23:38.138129+00	guardrail	32301100919	40	0
12577097	f	0	2021-05-03 21:23:39.907323+00	guardrail	32301101509	11	0
12577083	f	0	2021-05-03 21:23:39.6737+00	guardrail	32301101608	44	0
12577039	f	0	2021-05-03 21:23:38.882365+00	guardrail	32301101818	30	0
12577104	f	0	2021-05-03 21:23:40.023315+00	guardrail	32301102128	35	0
12577046	f	0	2021-05-03 21:23:39.016246+00	guardrail	32301102608	13	0
12577111	f	0	2021-05-03 21:23:40.14085+00	guardrail	32301103129	0	0
12577004	f	0.0100000000000000002	2021-05-03 21:23:38.257025+00	guardrail	32301103219	27	0
12577053	f	0	2021-05-03 21:23:39.131477+00	guardrail	32301103509	29	0
12577118	f	0	2021-05-03 21:23:40.257468+00	guardrail	32301103819	21	0
12577125	f	0	2021-05-03 21:23:40.374937+00	guardrail	32301104308	49	0
12577401	f	0	2021-05-03 21:23:45.110271+00	guardrail	32301104409	0	0
12577346	f	0	2021-05-03 21:23:44.176635+00	guardrail	32301104628	33	0
12577079	f	0	2021-05-03 21:23:39.591047+00	guardrail	32301104709	46	0
12577060	f	0	2021-05-03 21:23:39.257249+00	guardrail	32301104728	44	0
12577402	f	0	2021-05-03 21:23:45.125817+00	guardrail	32301105128	4	0
12577067	f	0	2021-05-03 21:23:39.373177+00	guardrail	32301105208	21	0
12577132	f	0	2021-05-03 21:23:40.49058+00	guardrail	32301105219	28	0
12577011	f	0	2021-05-03 21:23:38.374202+00	guardrail	32301105308	46	0
12577403	f	0	2021-05-03 21:23:45.14362+00	guardrail	32301105508	19	0
12577074	f	0	2021-05-03 21:23:39.506639+00	guardrail	32301105908	25	0
12577253	f	0	2021-05-03 21:23:42.616458+00	guardrail	32301110409	38	0
12577405	f	0	2021-05-03 21:23:45.176261+00	guardrail	32301110509	31	0
12577190	f	0	2021-05-03 21:23:41.51683+00	guardrail	32301110529	4	0
12577311	f	0	2021-05-03 21:23:43.591838+00	guardrail	32301110719	2	0
12577260	f	0	2021-05-03 21:23:42.733551+00	guardrail	32301111019	12	0
12577406	f	0	2021-05-03 21:23:45.193573+00	guardrail	32301111109	47	0
12577197	f	0	2021-05-03 21:23:41.633446+00	guardrail	32301111209	1	0
12577407	f	0.0100000000000000002	2021-05-03 21:23:45.210399+00	guardrail	32301111308	12	0
12577408	f	0.0200000000000000004	2021-05-03 21:23:45.225939+00	guardrail	32301111409	42	0
12577246	f	0	2021-05-03 21:23:42.500476+00	guardrail	32301111518	38	0
12577267	f	0	2021-05-03 21:23:42.850779+00	guardrail	32301111609	35	0
12577204	f	0	2021-05-03 21:23:41.757987+00	guardrail	32301111818	29	0
12577409	f	0	2021-05-03 21:23:45.24339+00	guardrail	32301112028	11	0
12577353	f	0	2021-05-03 21:23:44.2923+00	guardrail	32301112108	11	0
12577410	f	0	2021-05-03 21:23:45.260445+00	guardrail	32301112409	33	0
12577274	f	0	2021-05-03 21:23:42.966777+00	guardrail	32301112529	17	0
12577211	f	0.0100000000000000002	2021-05-03 21:23:41.875151+00	guardrail	32301112609	45	0
12577412	f	0	2021-05-03 21:23:45.295899+00	guardrail	32301113118	44	0
12577318	f	0	2021-05-03 21:23:43.7087+00	guardrail	32301113129	12	0
12577218	f	0	2021-05-03 21:23:42.007575+00	guardrail	32301113308	33	0
12577281	f	0	2021-05-03 21:23:43.092502+00	guardrail	32301113408	21	0
12577414	f	0	2021-05-03 21:23:45.33463+00	guardrail	32301113919	23	0
12577288	f	0	2021-05-03 21:23:43.208391+00	guardrail	32301114008	6	0
12577415	f	0	2021-05-03 21:23:45.352416+00	guardrail	32301114128	49	0
12577186	f	0.0100000000000000002	2021-05-03 21:23:41.449601+00	guardrail	32301114208	37	0
12577416	f	0	2021-05-03 21:23:45.367764+00	guardrail	32301114218	44	0
12577225	f	0	2021-05-03 21:23:42.142027+00	guardrail	32301114429	30	0
12577293	f	0	2021-05-03 21:23:43.291844+00	guardrail	32301114529	3	0
12577181	f	0	2021-05-03 21:23:41.36682+00	guardrail	32301114619	35	0
12577297	f	0	2021-05-03 21:23:43.358607+00	guardrail	32301114908	23	0
12577417	f	0	2021-05-03 21:23:45.384937+00	guardrail	32301114918	18	0
12577232	f	0.640000000000000013	2021-05-03 21:23:42.257564+00	guardrail	32301115219	41	0
12577325	f	0.0100000000000000002	2021-05-03 21:23:43.82603+00	guardrail	32301115328	6	0
12577304	f	0	2021-05-03 21:23:43.47599+00	guardrail	32301115709	41	0
12577239	f	0.0100000000000000002	2021-05-03 21:23:42.382723+00	guardrail	32301115818	30	0
12577419	f	0	2021-05-03 21:23:45.417599+00	guardrail	32301115909	20	0
12577153	f	0.0200000000000000004	2021-05-03 21:23:40.841001+00	guardrail	32301120119	35	0
12577420	f	0	2021-05-03 21:23:45.435198+00	guardrail	32301120209	24	0
12577146	f	0.0400000000000000008	2021-05-03 21:23:40.723837+00	guardrail	32301120409	0	0
12577421	f	0.0299999999999999989	2021-05-03 21:23:45.452118+00	guardrail	32301120728	34	0
12577167	f	0.739999999999999991	2021-05-03 21:23:41.073798+00	guardrail	32301120928	46	0
12577422	t	0.979999999999999982	2021-05-03 21:23:45.467827+00	guardrail	32301121128	12	0
12577174	t	1	2021-05-03 21:23:41.249716+00	guardrail	32301121228	5	0
12577381	f	0	2021-05-03 21:23:44.775753+00	guardrail	32301091528	40	0
12577388	f	0	2021-05-03 21:23:44.893614+00	guardrail	32301095328	37	0
12577395	f	0	2021-05-03 21:23:45.01029+00	guardrail	32301101919	36	0
12577400	f	0	2021-05-03 21:23:45.093505+00	guardrail	32301104229	1	0
12577404	f	0	2021-05-03 21:23:45.160674+00	guardrail	32301110429	32	0
12577360	f	0	2021-05-03 21:23:44.409946+00	guardrail	32301110819	11	0
12577411	f	0.0100000000000000002	2021-05-03 21:23:45.275941+00	guardrail	32301112928	2	0
12577367	f	0	2021-05-03 21:23:44.526853+00	guardrail	32301114018	7	0
12577418	f	0.0500000000000000028	2021-05-03 21:23:45.402048+00	guardrail	32301115109	35	0
12578283	t	1	2021-05-18 17:52:22.760564+00	pole	15901225329	60	0
12578295	f	0.530000000000000027	2021-05-18 17:52:22.859996+00	pole	16100345009	72	0
12578293	t	1	2021-05-18 17:52:22.843941+00	pole	16500135607	70	0
12578274	t	1	2021-05-18 17:52:22.685544+00	pole	22000431902	51	0
12578227	f	0.0200000000000000004	2021-05-18 17:52:22.193927+00	pole	29601544005	4	0
12578240	t	0.890000000000000013	2021-05-18 17:52:22.302514+00	pole	30001011809	17	0
12578312	t	0.969999999999999973	2021-05-18 17:52:23.001937+00	pole	30200201401	89	0
12578233	t	1	2021-05-18 17:52:22.244331+00	pole	30500211224	10	0
12578287	t	0.979999999999999982	2021-05-18 17:52:22.793905+00	pole	30500414711	64	0
12578269	f	0.510000000000000009	2021-05-18 17:52:22.643839+00	pole	30500483409	46	0
12578310	t	1	2021-05-18 17:52:22.985071+00	pole	30600250212	87	0
12578298	f	0.110000000000000001	2021-05-18 17:52:22.885102+00	pole	31001305524	75	0
12578292	t	0.969999999999999973	2021-05-18 17:52:22.835609+00	pole	31001363418	69	0
12578237	t	0.939999999999999947	2021-05-18 17:52:22.27757+00	pole	31300315228	14	0
12578273	f	0.200000000000000011	2021-05-18 17:52:22.677192+00	pole	31900161110	50	0
12578229	f	0.239999999999999991	2021-05-18 17:52:22.21057+00	pole	32300323606	6	0
12578282	f	0.400000000000000022	2021-05-18 17:52:22.752253+00	pole	32300473808	59	0
12578268	t	0.989999999999999991	2021-05-18 17:52:22.635473+00	pole	32301085109	45	0
12578302	t	0.930000000000000049	2021-05-18 17:52:22.918417+00	pole	32301085118	79	0
12578286	t	0.989999999999999991	2021-05-18 17:52:22.785591+00	pole	32301085128	63	0
12578289	t	0.989999999999999991	2021-05-18 17:52:22.810621+00	pole	32301085428	66	0
12578258	t	1	2021-05-18 17:52:22.553088+00	pole	32301090128	35	0
12578244	t	0.949999999999999956	2021-05-18 17:52:22.335479+00	pole	32301090228	21	0
12578266	t	0.979999999999999982	2021-05-18 17:52:22.618829+00	pole	32301090518	43	0
12578236	t	0.900000000000000022	2021-05-18 17:52:22.269248+00	pole	32301091029	13	0
12578272	f	0.5	2021-05-18 17:52:22.668854+00	pole	32301091118	49	0
12578254	t	0.989999999999999991	2021-05-18 17:52:22.519317+00	pole	32301091318	31	0
12578309	t	1	2021-05-18 17:52:22.976748+00	pole	32301091429	86	0
12578252	t	0.92000000000000004	2021-05-18 17:52:22.50273+00	pole	32301091628	29	0
12578300	t	0.989999999999999991	2021-05-18 17:52:22.901854+00	pole	32301092109	77	0
12578235	t	1	2021-05-18 17:52:22.260217+00	pole	32301092218	12	0
12578265	t	1	2021-05-18 17:52:22.61048+00	pole	32301092418	42	0
12578249	t	1	2021-05-18 17:52:22.478563+00	pole	32301092809	26	0
12578246	f	0.340000000000000024	2021-05-18 17:52:22.437509+00	pole	32301092929	23	0
12578297	f	0.330000000000000016	2021-05-18 17:52:22.876489+00	pole	32301093918	74	0
12578247	t	0.930000000000000049	2021-05-18 17:52:22.454221+00	pole	32301094329	24	0
12578239	t	0.910000000000000031	2021-05-18 17:52:22.294179+00	pole	32301095819	16	0
12578311	t	0.939999999999999947	2021-05-18 17:52:22.993411+00	pole	32301100609	88	0
12578304	t	0.989999999999999991	2021-05-18 17:52:22.935145+00	pole	32301101008	81	0
12578278	t	0.939999999999999947	2021-05-18 17:52:22.718856+00	pole	32301101128	55	0
12578256	f	0.589999999999999969	2021-05-18 17:52:22.536564+00	pole	32301101408	33	0
12578308	f	0.57999999999999996	2021-05-18 17:52:22.968287+00	pole	32301102309	85	0
12578250	f	0.220000000000000001	2021-05-18 17:52:22.485672+00	pole	32301102419	27	0
12578267	f	0.340000000000000024	2021-05-18 17:52:22.627159+00	pole	32301102508	44	0
12578264	f	0.390000000000000013	2021-05-18 17:52:22.602665+00	pole	32301102728	41	0
12578231	t	1	2021-05-18 17:52:22.227625+00	pole	32301103418	8	0
12578232	t	1	2021-05-18 17:52:22.235483+00	pole	32301103728	9	0
12578241	t	0.729999999999999982	2021-05-18 17:52:22.310681+00	pole	32301103819	18	0
12578253	t	0.979999999999999982	2021-05-18 17:52:22.511178+00	pole	32301104118	30	0
12578296	t	0.839999999999999969	2021-05-18 17:52:22.868319+00	pole	32301104809	73	0
12578281	t	0.849999999999999978	2021-05-18 17:52:22.743902+00	pole	32301104918	58	0
12578270	t	0.989999999999999991	2021-05-18 17:52:22.65215+00	pole	32301105318	47	0
12578288	t	0.979999999999999982	2021-05-18 17:52:22.802232+00	pole	32301105729	65	0
12578299	t	1	2021-05-18 17:52:22.893261+00	pole	32301110419	76	0
12578284	t	1	2021-05-18 17:52:22.768881+00	pole	32301110719	61	0
12578263	t	1	2021-05-18 17:52:22.594284+00	pole	32301110909	40	0
12578280	f	0.640000000000000013	2021-05-18 17:52:22.735581+00	pole	32301111019	57	0
12578305	t	1	2021-05-18 17:52:22.943396+00	pole	32301111928	82	0
12578291	t	0.959999999999999964	2021-05-18 17:52:22.827283+00	pole	32301112309	68	0
12578276	t	0.930000000000000049	2021-05-18 17:52:22.702236+00	pole	32301112909	53	0
12578261	t	1	2021-05-18 17:52:22.578033+00	pole	32301113318	38	0
12578290	t	0.979999999999999982	2021-05-18 17:52:22.818963+00	pole	32301114308	67	0
12578306	t	1	2021-05-18 17:52:22.951785+00	pole	32301114709	83	0
12578243	t	1	2021-05-18 17:52:22.327481+00	pole	32301115409	20	0
12578257	t	1	2021-05-18 17:52:22.544014+00	pole	32301120028	34	0
12578245	t	1	2021-05-18 17:52:22.418676+00	pole	32301120508	22	0
12578275	t	0.989999999999999991	2021-05-18 17:52:22.693831+00	pole	32301120718	52	0
12578301	t	1	2021-05-18 17:52:22.909882+00	pole	32301120829	78	0
12578279	t	1	2021-05-18 17:52:22.727203+00	pole	32301120908	56	0
12578228	t	1	2021-05-18 17:52:22.202355+00	pole	33401471905	5	0
12578242	t	1	2021-05-18 17:52:22.319563+00	pole	33500481628	19	0
12578238	t	0.979999999999999982	2021-05-18 17:52:22.2853+00	pole	34000182102	15	0
12578303	t	0.989999999999999991	2021-05-18 17:52:22.926726+00	pole	34100282611	80	0
12578271	t	1	2021-05-18 17:52:22.660526+00	pole	34201521024	48	0
12578255	t	0.979999999999999982	2021-05-18 17:52:22.528179+00	pole	35100165617	32	0
12578260	f	0.550000000000000044	2021-05-18 17:52:22.56912+00	pole	35100530209	37	0
12578248	t	1	2021-05-18 17:52:22.470704+00	pole	35200250623	25	0
12578277	t	0.989999999999999991	2021-05-18 17:52:22.710532+00	pole	35902013028	54	0
12578230	f	0.280000000000000027	2021-05-18 17:52:22.218858+00	pole	42400183706	7	0
12578307	t	1	2021-05-18 17:52:22.959911+00	pole	42400450315	84	0
12578259	f	0.110000000000000001	2021-05-18 17:52:22.561581+00	pole	42401304003	36	0
12578285	f	0.469999999999999973	2021-05-18 17:52:22.777218+00	pole	42501474203	62	0
12578384	t	0.969999999999999973	2021-05-18 17:52:23.835386+00	pole	29700553621	161	0
12578385	t	1	2021-05-18 17:52:23.843778+00	pole	29701443127	162	0
12578383	t	0.989999999999999991	2021-05-18 17:52:23.827161+00	pole	30700322607	160	0
12578409	t	1	2021-05-18 17:52:24.043978+00	pole	30700411425	186	0
12578374	t	1	2021-05-18 17:52:23.751901+00	pole	30700573221	151	0
12578368	t	0.989999999999999991	2021-05-18 17:52:23.702248+00	pole	31001261018	145	0
12578359	t	1	2021-05-18 17:52:23.393507+00	pole	32300431021	136	0
12578324	t	1	2021-05-18 17:52:23.101727+00	pole	32301084429	101	0
12578405	t	0.979999999999999982	2021-05-18 17:52:24.010539+00	pole	32301084608	182	0
12578342	t	1	2021-05-18 17:52:23.251613+00	pole	32301085218	119	0
12578367	t	1	2021-05-18 17:52:23.693778+00	pole	32301090028	144	0
12578343	t	1	2021-05-18 17:52:23.259955+00	pole	32301090108	120	0
12578389	t	0.949999999999999956	2021-05-18 17:52:23.877123+00	pole	32301090608	166	0
12578398	f	0.419999999999999984	2021-05-18 17:52:23.952357+00	pole	32301090829	175	0
12578318	f	0.380000000000000004	2021-05-18 17:52:23.051586+00	pole	32301091208	95	0
12578316	t	1	2021-05-18 17:52:23.035296+00	pole	32301091328	93	0
12578341	t	1	2021-05-18 17:52:23.24338+00	pole	32301091809	118	0
12578328	t	1	2021-05-18 17:52:23.135108+00	pole	32301091818	105	0
12578400	t	0.939999999999999947	2021-05-18 17:52:23.968794+00	pole	32301091918	177	0
12578380	t	0.930000000000000049	2021-05-18 17:52:23.802128+00	pole	32301092128	157	0
12578338	t	1	2021-05-18 17:52:23.218417+00	pole	32301092328	115	0
12578329	t	0.930000000000000049	2021-05-18 17:52:23.14354+00	pole	32301092518	106	0
12578397	t	0.989999999999999991	2021-05-18 17:52:23.943851+00	pole	32301092709	174	0
12578371	t	0.989999999999999991	2021-05-18 17:52:23.727125+00	pole	32301092718	148	0
12578393	f	0.0500000000000000028	2021-05-18 17:52:23.910451+00	pole	32301093508	170	0
12578339	f	0.190000000000000002	2021-05-18 17:52:23.226769+00	pole	32301093909	116	0
12578315	f	0.25	2021-05-18 17:52:23.026845+00	pole	32301093929	92	0
12578345	t	0.939999999999999947	2021-05-18 17:52:23.276706+00	pole	32301094429	122	0
12578370	t	1	2021-05-18 17:52:23.718696+00	pole	32301094529	147	0
12578320	t	0.979999999999999982	2021-05-18 17:52:23.068577+00	pole	32301094818	97	0
12578348	t	0.989999999999999991	2021-05-18 17:52:23.301781+00	pole	32301095008	125	0
12578358	t	1	2021-05-18 17:52:23.38521+00	pole	32301095108	135	0
12578336	t	0.989999999999999991	2021-05-18 17:52:23.201872+00	pole	32301095118	113	0
12578372	t	1	2021-05-18 17:52:23.73541+00	pole	32301095318	149	0
12578335	t	1	2021-05-18 17:52:23.193352+00	pole	32301095508	112	0
12578332	t	1	2021-05-18 17:52:23.168382+00	pole	32301095518	109	0
12578388	t	0.739999999999999991	2021-05-18 17:52:23.868781+00	pole	32301100219	165	0
12578363	t	0.699999999999999956	2021-05-18 17:52:23.426872+00	pole	32301100308	140	0
12578323	t	0.810000000000000053	2021-05-18 17:52:23.093309+00	pole	32301100409	100	0
12578362	t	0.979999999999999982	2021-05-18 17:52:23.41856+00	pole	32301100808	139	0
12578346	t	0.989999999999999991	2021-05-18 17:52:23.285008+00	pole	32301100919	123	0
12578401	f	0.540000000000000036	2021-05-18 17:52:23.977192+00	pole	32301101509	178	0
12578354	t	0.92000000000000004	2021-05-18 17:52:23.351898+00	pole	32301101629	131	0
12578322	t	0.969999999999999973	2021-05-18 17:52:23.085027+00	pole	32301101708	99	0
12578347	t	0.979999999999999982	2021-05-18 17:52:23.293591+00	pole	32301101829	124	0
12578377	t	0.680000000000000049	2021-05-18 17:52:23.777022+00	pole	32301102208	154	0
12578407	f	0.179999999999999993	2021-05-18 17:52:24.027399+00	pole	32301102429	184	0
12578395	f	0.520000000000000018	2021-05-18 17:52:23.927189+00	pole	32301102708	172	0
12578352	t	0.989999999999999991	2021-05-18 17:52:23.335154+00	pole	32301103129	129	0
12578364	t	1	2021-05-18 17:52:23.435032+00	pole	32301103618	141	0
12578361	t	1	2021-05-18 17:52:23.410067+00	pole	32301104219	138	0
12578344	t	0.989999999999999991	2021-05-18 17:52:23.26845+00	pole	32301105908	121	0
12578326	t	0.979999999999999982	2021-05-18 17:52:23.118555+00	pole	32301105929	103	0
12578406	t	1	2021-05-18 17:52:24.018956+00	pole	32301110308	183	0
12578321	t	1	2021-05-18 17:52:23.076687+00	pole	32301110519	98	0
12578392	t	1	2021-05-18 17:52:23.902439+00	pole	32301111009	169	0
12578340	t	1	2021-05-18 17:52:23.235064+00	pole	32301111409	117	0
12578386	t	1	2021-05-18 17:52:23.852165+00	pole	32301112009	163	0
12578327	t	0.930000000000000049	2021-05-18 17:52:23.126789+00	pole	32301112829	104	0
12578379	t	1	2021-05-18 17:52:23.793696+00	pole	32301113118	156	0
12578369	t	1	2021-05-18 17:52:23.710413+00	pole	32301113919	146	0
12578350	t	1	2021-05-18 17:52:23.318337+00	pole	32301114208	127	0
12578381	t	1	2021-05-18 17:52:23.810409+00	pole	32301114918	158	0
12578313	t	1	2021-05-18 17:52:23.009918+00	pole	32301115028	90	0
12578333	t	1	2021-05-18 17:52:23.17664+00	pole	32301115109	110	0
12578399	t	1	2021-05-18 17:52:23.960549+00	pole	32301115818	176	0
12578314	t	1	2021-05-18 17:52:23.018508+00	pole	32301120309	91	0
12578337	t	1	2021-05-18 17:52:23.209902+00	pole	32301120728	114	0
12578396	t	0.989999999999999991	2021-05-18 17:52:23.935618+00	pole	32301120809	173	0
12578387	t	1	2021-05-18 17:52:23.860504+00	pole	32301121009	164	0
12578376	t	1	2021-05-18 17:52:23.768547+00	pole	32301121019	153	0
12578319	t	1	2021-05-18 17:52:23.059932+00	pole	32400230908	96	0
12578394	t	1	2021-05-18 17:52:23.918708+00	pole	33000215519	171	0
12578375	t	1	2021-05-18 17:52:23.760279+00	pole	33400080617	152	0
12578373	t	1	2021-05-18 17:52:23.743738+00	pole	33700223417	150	0
12578378	t	0.890000000000000013	2021-05-18 17:52:23.785547+00	pole	34000045310	155	0
12578334	t	0.930000000000000049	2021-05-18 17:52:23.185018+00	pole	34100221828	111	0
12578357	t	0.989999999999999991	2021-05-18 17:52:23.376788+00	pole	34100321517	134	0
12578391	t	1	2021-05-18 17:52:23.893731+00	pole	34101115407	168	0
12578356	t	0.82999999999999996	2021-05-18 17:52:23.368552+00	pole	34301153803	133	0
12578353	t	0.780000000000000027	2021-05-18 17:52:23.343696+00	pole	34301182805	130	0
12578360	t	0.910000000000000031	2021-05-18 17:52:23.401986+00	pole	34301535911	137	0
12578403	t	1	2021-05-18 17:52:23.993941+00	pole	34400070221	180	0
12578349	t	1	2021-05-18 17:52:23.310161+00	pole	34401231412	126	0
12578408	t	0.959999999999999964	2021-05-18 17:52:24.035648+00	pole	35100180614	185	0
12578330	t	0.979999999999999982	2021-05-18 17:52:23.151609+00	pole	35600275009	107	0
12578366	t	1	2021-05-18 17:52:23.685347+00	pole	35601070529	143	0
12578402	f	0.409999999999999976	2021-05-18 17:52:23.98551+00	pole	35701420526	179	0
12578331	f	0.469999999999999973	2021-05-18 17:52:23.159958+00	pole	35801404307	108	0
12578351	t	0.989999999999999991	2021-05-18 17:52:23.326845+00	pole	35900171209	128	0
12578325	f	0.140000000000000013	2021-05-18 17:52:23.110044+00	pole	42500034620	102	0
12578426	t	1	2021-05-18 17:52:24.185683+00	pole	16300222214	203	0
12578427	f	0.23000000000000001	2021-05-18 17:52:24.193909+00	pole	16301245502	204	0
12578415	t	1	2021-05-18 17:52:24.09379+00	pole	16400161125	192	0
12578492	t	0.989999999999999991	2021-05-18 17:52:24.736995+00	pole	22001132920	269	0
12578453	t	1	2021-05-18 17:52:24.412047+00	pole	30001205208	230	0
12578489	t	0.979999999999999982	2021-05-18 17:52:24.712169+00	pole	31000211513	266	0
12578465	t	1	2021-05-18 17:52:24.512186+00	pole	31901522512	242	0
12578464	t	1	2021-05-18 17:52:24.503722+00	pole	32301084918	241	0
12578485	t	0.939999999999999947	2021-05-18 17:52:24.678859+00	pole	32301085018	262	0
12578472	t	0.989999999999999991	2021-05-18 17:52:24.569937+00	pole	32301085329	249	0
12578476	t	0.989999999999999991	2021-05-18 17:52:24.603905+00	pole	32301085618	253	0
12578503	t	0.780000000000000027	2021-05-18 17:52:24.829059+00	pole	32301085908	280	0
12578471	t	0.989999999999999991	2021-05-18 17:52:24.562173+00	pole	32301090018	248	0
12578474	t	0.979999999999999982	2021-05-18 17:52:24.587233+00	pole	32301090118	251	0
12578467	t	1	2021-05-18 17:52:24.528982+00	pole	32301090208	244	0
12578498	t	0.949999999999999956	2021-05-18 17:52:24.786984+00	pole	32301090318	275	0
12578473	t	0.979999999999999982	2021-05-18 17:52:24.57885+00	pole	32301090418	250	0
12578424	t	0.75	2021-05-18 17:52:24.168785+00	pole	32301090619	201	0
12578445	f	0.650000000000000022	2021-05-18 17:52:24.343894+00	pole	32301090629	222	0
12578468	f	0.429999999999999993	2021-05-18 17:52:24.537129+00	pole	32301090718	245	0
12578502	f	0.28999999999999998	2021-05-18 17:52:24.820159+00	pole	32301090919	279	0
12578463	t	0.739999999999999991	2021-05-18 17:52:24.494879+00	pole	32301091008	240	0
12578419	t	1	2021-05-18 17:52:24.12721+00	pole	32301091608	196	0
12578435	t	0.959999999999999964	2021-05-18 17:52:24.260371+00	pole	32301092028	212	0
12578412	t	1	2021-05-18 17:52:24.068853+00	pole	32301092229	189	0
12578429	t	0.75	2021-05-18 17:52:24.210477+00	pole	32301092509	206	0
12578425	t	0.729999999999999982	2021-05-18 17:52:24.177252+00	pole	32301092528	202	0
12578486	t	0.979999999999999982	2021-05-18 17:52:24.687073+00	pole	32301092919	263	0
12578436	f	0.220000000000000001	2021-05-18 17:52:24.268887+00	pole	32301093119	213	0
12578433	f	0.23000000000000001	2021-05-18 17:52:24.243912+00	pole	32301093409	210	0
12578495	f	0.280000000000000027	2021-05-18 17:52:24.762+00	pole	32301093618	272	0
12578470	f	0.359999999999999987	2021-05-18 17:52:24.553724+00	pole	32301093718	247	0
12578478	f	0.469999999999999973	2021-05-18 17:52:24.620082+00	pole	32301093809	255	0
12578500	f	0.239999999999999991	2021-05-18 17:52:24.803556+00	pole	32301094009	277	0
12578449	f	0.650000000000000022	2021-05-18 17:52:24.378351+00	pole	32301094228	226	0
12578444	t	0.959999999999999964	2021-05-18 17:52:24.335589+00	pole	32301094709	221	0
12578418	t	0.959999999999999964	2021-05-18 17:52:24.118996+00	pole	32301094729	195	0
12578452	t	0.959999999999999964	2021-05-18 17:52:24.403651+00	pole	32301094808	229	0
12578497	t	1	2021-05-18 17:52:24.779066+00	pole	32301095429	274	0
12578420	t	0.930000000000000049	2021-05-18 17:52:24.135473+00	pole	32301095809	197	0
12578480	t	0.92000000000000004	2021-05-18 17:52:24.63736+00	pole	32301100509	257	0
12578469	t	0.900000000000000022	2021-05-18 17:52:24.544837+00	pole	32301100709	246	0
12578506	t	0.949999999999999956	2021-05-18 17:52:24.85353+00	pole	32301100729	283	0
12578456	t	0.959999999999999964	2021-05-18 17:52:24.437085+00	pole	32301100929	233	0
12578484	f	0.429999999999999993	2021-05-18 17:52:24.670102+00	pole	32301101229	261	0
12578496	t	0.770000000000000018	2021-05-18 17:52:24.769867+00	pole	32301102828	273	0
12578422	t	0.910000000000000031	2021-05-18 17:52:24.15209+00	pole	32301102908	199	0
12578411	t	1	2021-05-18 17:52:24.060632+00	pole	32301103018	188	0
12578442	t	0.890000000000000013	2021-05-18 17:52:24.31876+00	pole	32301104009	219	0
12578501	f	0.489999999999999991	2021-05-18 17:52:24.812056+00	pole	32301104108	278	0
12578477	t	1	2021-05-18 17:52:24.612177+00	pole	32301104318	254	0
12578459	t	1	2021-05-18 17:52:24.462099+00	pole	32301104409	236	0
12578443	t	0.699999999999999956	2021-05-18 17:52:24.327368+00	pole	32301105128	220	0
12578455	t	0.880000000000000004	2021-05-18 17:52:24.428613+00	pole	32301105219	232	0
12578437	t	0.989999999999999991	2021-05-18 17:52:24.277208+00	pole	32301105329	214	0
12578482	t	1	2021-05-18 17:52:24.653808+00	pole	32301105408	259	0
12578450	t	0.930000000000000049	2021-05-18 17:52:24.386886+00	pole	32301110119	227	0
12578454	t	1	2021-05-18 17:52:24.419946+00	pole	32301110209	231	0
12578410	t	1	2021-05-18 17:52:24.052115+00	pole	32301110529	187	0
12578458	t	1	2021-05-18 17:52:24.453749+00	pole	32301111508	235	0
12578483	t	1	2021-05-18 17:52:24.662232+00	pole	32301112028	260	0
12578439	t	1	2021-05-18 17:52:24.293806+00	pole	32301112209	216	0
12578446	f	0.239999999999999991	2021-05-18 17:52:24.352157+00	pole	32301112429	223	0
12578421	f	0.110000000000000001	2021-05-18 17:52:24.143823+00	pole	32301112619	198	0
12578447	t	1	2021-05-18 17:52:24.361852+00	pole	32301113418	224	0
12578430	t	1	2021-05-18 17:52:24.218734+00	pole	32301113629	207	0
12578448	t	0.989999999999999991	2021-05-18 17:52:24.369827+00	pole	32301113819	225	0
12578487	t	1	2021-05-18 17:52:24.694829+00	pole	32301114418	264	0
12578494	t	1	2021-05-18 17:52:24.753661+00	pole	32301114729	271	0
12578488	t	1	2021-05-18 17:52:24.703778+00	pole	32301114908	265	0
12578414	t	1	2021-05-18 17:52:24.0857+00	pole	32301115118	191	0
12578451	t	1	2021-05-18 17:52:24.394659+00	pole	32301115219	228	0
12578461	t	1	2021-05-18 17:52:24.478592+00	pole	32301115529	238	0
12578481	t	1	2021-05-18 17:52:24.645029+00	pole	32301120209	258	0
12578413	t	1	2021-05-18 17:52:24.07743+00	pole	32301120218	190	0
12578504	t	1	2021-05-18 17:52:24.837283+00	pole	32301120708	281	0
12578490	f	0.0700000000000000067	2021-05-18 17:52:24.720096+00	pole	32301121108	267	0
12578491	t	0.979999999999999982	2021-05-18 17:52:24.728724+00	pole	32301204606	268	0
12578441	t	0.770000000000000018	2021-05-18 17:52:24.310523+00	pole	32301354704	218	0
12578416	f	0.179999999999999993	2021-05-18 17:52:24.102247+00	pole	32400355028	193	0
12578499	t	0.989999999999999991	2021-05-18 17:52:24.794811+00	pole	32501102524	276	0
12578462	t	1	2021-05-18 17:52:24.487229+00	pole	32700170321	239	0
12578479	t	1	2021-05-18 17:52:24.628881+00	pole	32700170921	256	0
12578438	f	0.100000000000000006	2021-05-18 17:52:24.285457+00	pole	33600384827	215	0
12578466	t	0.979999999999999982	2021-05-18 17:52:24.52026+00	pole	33700591706	243	0
12578440	f	0.0200000000000000004	2021-05-18 17:52:24.302113+00	pole	34000104729	217	0
12578431	t	0.959999999999999964	2021-05-18 17:52:24.227154+00	pole	34301333500	208	0
12578460	f	0.569999999999999951	2021-05-18 17:52:24.469795+00	pole	34400300325	237	0
12578417	t	0.979999999999999982	2021-05-18 17:52:24.110463+00	pole	34400370205	194	0
12578475	t	0.959999999999999964	2021-05-18 17:52:24.595009+00	pole	35801471221	252	0
12578423	t	0.989999999999999991	2021-05-18 17:52:24.160375+00	pole	36002001114	200	0
12578581	t	0.92000000000000004	2021-05-18 17:52:25.48775+00	pole	16100350429	358	0
12578570	t	1	2021-05-18 17:52:25.395961+00	pole	16300221524	347	0
12578528	t	1	2021-05-18 17:52:25.045451+00	pole	16300504528	305	0
12578553	f	0.630000000000000004	2021-05-18 17:52:25.253551+00	pole	16301022617	330	0
12578517	t	1	2021-05-18 17:52:24.945029+00	pole	16501060119	294	0
12578582	f	0.5	2021-05-18 17:52:25.495969+00	pole	29601072011	359	0
12578580	f	0.609999999999999987	2021-05-18 17:52:25.479418+00	pole	29701532424	357	0
12578575	t	0.880000000000000004	2021-05-18 17:52:25.437529+00	pole	29901322813	352	0
12578566	f	0.0299999999999999989	2021-05-18 17:52:25.362318+00	pole	29901432208	343	0
12578527	t	0.989999999999999991	2021-05-18 17:52:25.036504+00	pole	30300400825	304	0
12578520	f	0.380000000000000004	2021-05-18 17:52:24.970492+00	pole	30502041402	297	0
12578552	t	1	2021-05-18 17:52:25.245587+00	pole	30800051125	329	0
12578544	f	0.239999999999999991	2021-05-18 17:52:25.178743+00	pole	30801333508	321	0
12578540	t	0.900000000000000022	2021-05-18 17:52:25.145849+00	pole	31101314311	317	0
12578549	t	1	2021-05-18 17:52:25.220737+00	pole	31400173203	326	0
12578567	t	1	2021-05-18 17:52:25.370787+00	pole	32301085609	344	0
12578511	t	1	2021-05-18 17:52:24.895031+00	pole	32301085628	288	0
12578571	t	1	2021-05-18 17:52:25.403663+00	pole	32301085719	348	0
12578564	t	1	2021-05-18 17:52:25.345771+00	pole	32301085809	341	0
12578543	f	0.209999999999999992	2021-05-18 17:52:25.170274+00	pole	32301085828	320	0
12578509	t	0.969999999999999973	2021-05-18 17:52:24.878828+00	pole	32301090329	286	0
12578594	f	0.560000000000000053	2021-05-18 17:52:25.595555+00	pole	32301090708	371	0
12578531	t	0.910000000000000031	2021-05-18 17:52:25.070443+00	pole	32301092018	308	0
12578512	t	1	2021-05-18 17:52:24.903769+00	pole	32301092619	289	0
12578578	t	1	2021-05-18 17:52:25.462267+00	pole	32301092628	355	0
12578558	t	1	2021-05-18 17:52:25.295753+00	pole	32301092828	335	0
12578599	t	0.849999999999999978	2021-05-18 17:52:25.637678+00	pole	32301093028	376	0
12578556	f	0.309999999999999998	2021-05-18 17:52:25.278673+00	pole	32301093829	333	0
12578524	t	0.709999999999999964	2021-05-18 17:52:25.01178+00	pole	32301094118	301	0
12578565	f	0.640000000000000013	2021-05-18 17:52:25.353697+00	pole	32301094129	342	0
12578523	f	0.440000000000000002	2021-05-18 17:52:25.00357+00	pole	32301094308	300	0
12578547	t	0.930000000000000049	2021-05-18 17:52:25.203348+00	pole	32301094629	324	0
12578513	t	0.959999999999999964	2021-05-18 17:52:24.912214+00	pole	32301094718	290	0
12578551	t	0.989999999999999991	2021-05-18 17:52:25.236932+00	pole	32301095718	328	0
12578583	t	0.869999999999999996	2021-05-18 17:52:25.504852+00	pole	32301095918	360	0
12578516	t	0.719999999999999973	2021-05-18 17:52:24.937379+00	pole	32301100029	293	0
12578573	t	0.969999999999999973	2021-05-18 17:52:25.420732+00	pole	32301100109	350	0
12578554	t	0.709999999999999964	2021-05-18 17:52:25.26244+00	pole	32301100118	331	0
12578591	t	0.67000000000000004	2021-05-18 17:52:25.570488+00	pole	32301100208	368	0
12578542	t	0.849999999999999978	2021-05-18 17:52:25.161863+00	pole	32301100528	319	0
12578559	t	0.969999999999999973	2021-05-18 17:52:25.30402+00	pole	32301100719	336	0
12578574	t	0.989999999999999991	2021-05-18 17:52:25.428834+00	pole	32301101029	351	0
12578532	t	0.959999999999999964	2021-05-18 17:52:25.078912+00	pole	32301101108	309	0
12578563	t	1	2021-05-18 17:52:25.337324+00	pole	32301101219	340	0
12578603	t	0.680000000000000049	2021-05-18 17:52:25.67062+00	pole	32301101608	380	0
12578595	t	1	2021-05-18 17:52:25.604396+00	pole	32301101818	372	0
12578539	f	0.0899999999999999967	2021-05-18 17:52:25.137567+00	pole	32301102018	316	0
12578585	f	0.140000000000000013	2021-05-18 17:52:25.520251+00	pole	32301102408	362	0
12578569	t	0.880000000000000004	2021-05-18 17:52:25.388105+00	pole	32301102818	346	0
12578525	t	1	2021-05-18 17:52:25.019795+00	pole	32301103219	302	0
12578598	t	1	2021-05-18 17:52:25.629387+00	pole	32301103229	375	0
12578596	t	1	2021-05-18 17:52:25.612732+00	pole	32301103428	373	0
12578568	t	1	2021-05-18 17:52:25.378751+00	pole	32301103709	345	0
12578572	t	0.979999999999999982	2021-05-18 17:52:25.412559+00	pole	32301104328	349	0
12578541	t	0.949999999999999956	2021-05-18 17:52:25.153129+00	pole	32301104418	318	0
12578592	t	0.819999999999999951	2021-05-18 17:52:25.579231+00	pole	32301104429	369	0
12578589	f	0.640000000000000013	2021-05-18 17:52:25.554459+00	pole	32301105018	366	0
12578529	t	0.930000000000000049	2021-05-18 17:52:25.053849+00	pole	32301105208	306	0
12578560	t	1	2021-05-18 17:52:25.312526+00	pole	32301105609	337	0
12578577	t	0.989999999999999991	2021-05-18 17:52:25.453594+00	pole	32301105819	354	0
12578534	t	0.969999999999999973	2021-05-18 17:52:25.094895+00	pole	32301110228	311	0
12578514	t	1	2021-05-18 17:52:24.920184+00	pole	32301110729	291	0
12578507	t	1	2021-05-18 17:52:24.862087+00	pole	32301110829	284	0
12578562	t	1	2021-05-18 17:52:25.32859+00	pole	32301111719	339	0
12578588	f	0.140000000000000013	2021-05-18 17:52:25.54549+00	pole	32301112609	365	0
12578593	t	1	2021-05-18 17:52:25.587722+00	pole	32301114529	370	0
12578538	t	1	2021-05-18 17:52:25.128639+00	pole	32301114829	315	0
12578600	t	1	2021-05-18 17:52:25.645632+00	pole	32301115709	377	0
12578508	t	1	2021-05-18 17:52:24.870093+00	pole	32301120119	285	0
12578576	t	1	2021-05-18 17:52:25.445763+00	pole	32301120328	353	0
12578550	t	0.989999999999999991	2021-05-18 17:52:25.228387+00	pole	32301120918	327	0
12578548	f	0.0700000000000000067	2021-05-18 17:52:25.212224+00	pole	32301121218	325	0
12578546	t	1	2021-05-18 17:52:25.195802+00	pole	32301163729	323	0
12578579	t	0.959999999999999964	2021-05-18 17:52:25.470597+00	pole	32400313308	356	0
12578536	f	0.640000000000000013	2021-05-18 17:52:25.112195+00	pole	32500283502	313	0
12578526	t	0.900000000000000022	2021-05-18 17:52:25.028265+00	pole	32700031900	303	0
12578533	f	0.119999999999999996	2021-05-18 17:52:25.086769+00	pole	32700281324	310	0
12578530	t	1	2021-05-18 17:52:25.061996+00	pole	32700330528	307	0
12578601	f	0.650000000000000022	2021-05-18 17:52:25.654357+00	pole	33500181408	378	0
12578521	t	0.989999999999999991	2021-05-18 17:52:24.980401+00	pole	33600004504	298	0
12578587	t	0.979999999999999982	2021-05-18 17:52:25.53747+00	pole	33700375929	364	0
12578555	t	1	2021-05-18 17:52:25.270622+00	pole	33800281503	332	0
12578561	t	0.959999999999999964	2021-05-18 17:52:25.320849+00	pole	34201070010	338	0
12578602	f	0.619999999999999996	2021-05-18 17:52:25.662506+00	pole	34301451503	379	0
12578537	t	0.949999999999999956	2021-05-18 17:52:25.120224+00	pole	34400391623	314	0
12578522	f	0.0100000000000000002	2021-05-18 17:52:24.995058+00	pole	34800560920	299	0
12578590	t	1	2021-05-18 17:52:25.56285+00	pole	35201071529	367	0
12578557	f	0.650000000000000022	2021-05-18 17:52:25.286798+00	pole	35501095409	334	0
12578535	t	0.989999999999999991	2021-05-18 17:52:25.103896+00	pole	35601190424	312	0
12578510	t	0.719999999999999973	2021-05-18 17:52:24.887161+00	pole	42400515327	287	0
12578545	t	0.739999999999999991	2021-05-18 17:52:25.18721+00	pole	42500252129	322	0
12576696	f	0	2021-01-17 16:24:14.103377+00	guardrail	15800251221	0	0
12576697	f	0	2021-01-17 16:24:14.120569+00	guardrail	15801484909	0	0
12576601	t	0.869999999999999996	2021-01-17 16:24:11.448899+00	guardrail	15901091226	0	0
12576604	f	0.0299999999999999989	2021-01-17 16:24:11.542201+00	guardrail	15901110815	0	0
12577374	f	0.0599999999999999978	2021-05-03 21:23:44.660101+00	guardrail	32301084828	6	0
12577032	f	0	2021-05-03 21:23:38.76521+00	guardrail	32301100719	28	0
12577139	f	0.0500000000000000028	2021-05-03 21:23:40.608161+00	guardrail	32301105828	9	0
12577413	f	0	2021-05-03 21:23:45.319346+00	guardrail	32301113228	28	0
12577160	f	0.309999999999999998	2021-05-03 21:23:40.958334+00	guardrail	32301120518	41	0
12576783	f	0	2021-01-17 16:24:16.408409+00	guardrail	34301424707	20	0
12578597	f	0.0800000000000000017	2021-05-18 17:52:25.620633+00	pole	15800251221	374	0
12578623	t	1	2021-07-06 20:14:38.829022+00	pole	15801484909	\N	\N
12578624	f	0.0200000000000000004	2021-07-06 20:14:38.887541+00	pole	15901091226	\N	\N
12578625	t	0.989999999999999991	2021-07-06 20:14:38.903934+00	pole	15901110815	\N	\N
12578626	f	0.0599999999999999978	2021-07-06 20:14:38.928252+00	pole	15901240029	\N	\N
12578615	t	0.989999999999999991	2021-05-18 17:52:25.770647+00	pole	15901324811	392	0
12578434	f	0.510000000000000009	2021-05-18 17:52:24.252079+00	pole	15901333701	211	0
12578627	t	1	2021-07-06 20:14:38.969206+00	pole	16100362400	\N	\N
12578628	f	0.630000000000000004	2021-07-06 20:14:38.977505+00	pole	16101050612	\N	\N
12578629	f	0.380000000000000004	2021-07-06 20:14:39.018978+00	pole	16301023018	\N	\N
12578630	t	1	2021-07-06 20:14:39.027882+00	pole	16301184725	\N	\N
12578631	t	1	2021-07-06 20:14:39.044162+00	pole	16302025413	\N	\N
12578365	t	1	2021-05-18 17:52:23.677379+00	pole	16401215429	142	0
12578632	t	1	2021-07-06 20:14:39.069241+00	pole	16401575226	\N	\N
12578633	f	0.340000000000000024	2021-07-06 20:14:39.086308+00	pole	16501045000	\N	\N
12578634	f	0.0200000000000000004	2021-07-06 20:14:39.103171+00	pole	16501580619	\N	\N
12578515	t	0.989999999999999991	2021-05-18 17:52:24.928861+00	pole	22000175809	292	0
12578635	t	1	2021-07-06 20:14:39.12808+00	pole	22000433201	\N	\N
12578636	t	0.969999999999999973	2021-07-06 20:14:39.144198+00	pole	22001512810	\N	\N
12578637	f	0.0100000000000000002	2021-07-06 20:14:39.16135+00	pole	29601084513	\N	\N
12578638	f	0.0400000000000000008	2021-07-06 20:14:39.169378+00	pole	29601422623	\N	\N
12578639	t	0.989999999999999991	2021-07-06 20:14:39.178239+00	pole	29601521527	\N	\N
12578640	f	0.119999999999999996	2021-07-06 20:14:39.19428+00	pole	29700553101	\N	\N
12578641	f	0.309999999999999998	2021-07-06 20:14:39.211446+00	pole	29701261012	\N	\N
12578642	f	0.160000000000000003	2021-07-06 20:14:39.219286+00	pole	29701315222	\N	\N
12578643	t	1	2021-07-06 20:14:39.244553+00	pole	29800012904	\N	\N
12578644	f	0	2021-07-06 20:14:39.261715+00	pole	29901113229	\N	\N
12578645	f	0.28999999999999998	2021-07-06 20:14:39.269921+00	pole	29901194629	\N	\N
12578646	f	0.489999999999999991	2021-07-06 20:14:39.286246+00	pole	29901341804	\N	\N
12578647	t	1	2021-07-06 20:14:39.302675+00	pole	30000081915	\N	\N
12578648	t	1	2021-07-06 20:14:39.311516+00	pole	30000272325	\N	\N
12578649	t	0.989999999999999991	2021-07-06 20:14:39.319818+00	pole	30000385923	\N	\N
12578611	t	0.729999999999999982	2021-05-18 17:52:25.737637+00	pole	30100424824	388	0
12578650	f	0.0500000000000000028	2021-07-06 20:14:39.352852+00	pole	30200062407	\N	\N
12578651	t	0.82999999999999996	2021-07-06 20:14:39.377751+00	pole	30301130918	\N	\N
12578652	f	0.110000000000000001	2021-07-06 20:14:39.386498+00	pole	30301141508	\N	\N
12578653	t	1	2021-07-06 20:14:39.394766+00	pole	30400214412	\N	\N
12578654	f	0.140000000000000013	2021-07-06 20:14:39.402617+00	pole	30400480726	\N	\N
12578613	t	1	2021-05-18 17:52:25.754154+00	pole	30400531116	390	0
12578655	f	0.510000000000000009	2021-07-06 20:14:39.419659+00	pole	30401182916	\N	\N
12578656	t	0.770000000000000018	2021-07-06 20:14:39.427619+00	pole	30401205318	\N	\N
12578657	f	0.0400000000000000008	2021-07-06 20:14:39.436417+00	pole	30401232201	\N	\N
12578658	f	0.0899999999999999967	2021-07-06 20:14:39.444796+00	pole	30401244412	\N	\N
12578659	t	0.979999999999999982	2021-07-06 20:14:39.477541+00	pole	30501412415	\N	\N
12578660	t	0.849999999999999978	2021-07-06 20:14:39.494646+00	pole	30600045513	\N	\N
12578661	t	1	2021-07-06 20:14:39.502347+00	pole	30600235410	\N	\N
12578662	f	0.0599999999999999978	2021-07-06 20:14:39.52869+00	pole	30600283129	\N	\N
12578663	t	1	2021-07-06 20:14:39.536919+00	pole	30600402403	\N	\N
12578493	f	0.510000000000000009	2021-05-18 17:52:24.74493+00	pole	30601263712	270	0
12578664	f	0.160000000000000003	2021-07-06 20:14:39.553015+00	pole	30601400420	\N	\N
12578665	f	0.100000000000000006	2021-07-06 20:14:39.561376+00	pole	30601400828	\N	\N
12578666	t	1	2021-07-06 20:14:39.577838+00	pole	30700384125	\N	\N
12578667	f	0.409999999999999976	2021-07-06 20:14:39.603183+00	pole	30701245813	\N	\N
12578668	t	0.979999999999999982	2021-07-06 20:14:39.611717+00	pole	30701365814	\N	\N
12578669	f	0.0100000000000000002	2021-07-06 20:14:39.619183+00	pole	30702000618	\N	\N
12578670	t	0.969999999999999973	2021-07-06 20:14:39.636448+00	pole	30800335719	\N	\N
12578671	t	1	2021-07-06 20:14:39.644406+00	pole	30800471224	\N	\N
12578672	t	1	2021-07-06 20:14:39.653058+00	pole	30800570802	\N	\N
12578673	t	1	2021-07-06 20:14:39.669281+00	pole	30801392614	\N	\N
12578674	f	0.0700000000000000067	2021-07-06 20:14:39.678101+00	pole	30900553212	\N	\N
12578390	f	0.200000000000000011	2021-05-18 17:52:23.885512+00	pole	30901224514	167	0
12578610	t	0.989999999999999991	2021-05-18 17:52:25.7292+00	pole	30901293205	387	0
12578675	t	1	2021-07-06 20:14:39.703031+00	pole	30901523718	\N	\N
12578676	t	0.880000000000000004	2021-07-06 20:14:39.719451+00	pole	31001021901	\N	\N
12578677	t	1	2021-07-06 20:14:39.753103+00	pole	31001364518	\N	\N
12578678	f	0.0599999999999999978	2021-07-06 20:14:39.761635+00	pole	31101034815	\N	\N
12578679	t	0.959999999999999964	2021-07-06 20:14:39.778212+00	pole	31200424207	\N	\N
12578680	t	0.969999999999999973	2021-07-06 20:14:39.803052+00	pole	31401385708	\N	\N
12578681	f	0.320000000000000007	2021-07-06 20:14:39.811519+00	pole	31401474309	\N	\N
12578682	f	0.0200000000000000004	2021-07-06 20:14:39.819323+00	pole	31401495227	\N	\N
12578683	t	1	2021-07-06 20:14:39.828088+00	pole	31500235705	\N	\N
12578684	f	0.57999999999999996	2021-07-06 20:14:39.836528+00	pole	31501391922	\N	\N
12578685	f	0.140000000000000013	2021-07-06 20:14:39.844472+00	pole	31501442614	\N	\N
12578686	t	0.989999999999999991	2021-07-06 20:14:39.853128+00	pole	31600423514	\N	\N
12578605	t	1	2021-05-18 17:52:25.687725+00	pole	32301091519	382	0
12578616	f	0.239999999999999991	2021-05-18 17:52:25.779258+00	pole	32301093318	393	0
12578608	t	0.880000000000000004	2021-05-18 17:52:25.712554+00	pole	32301101528	385	0
12578621	f	0.380000000000000004	2021-05-18 17:52:25.821488+00	pole	32301102608	398	0
12578614	t	0.890000000000000013	2021-05-18 17:52:25.762934+00	pole	32301103919	391	0
12578620	f	0.640000000000000013	2021-05-18 17:52:25.812568+00	pole	32301104018	397	0
12578618	t	0.900000000000000022	2021-05-18 17:52:25.795504+00	pole	32301104628	395	0
12578609	t	0.900000000000000022	2021-05-18 17:52:25.720409+00	pole	32301104709	386	0
12578612	t	0.989999999999999991	2021-05-18 17:52:25.745442+00	pole	32301110009	389	0
12578622	t	1	2021-05-18 17:52:25.829603+00	pole	32301110929	399	0
12578617	t	0.989999999999999991	2021-05-18 17:52:25.787688+00	pole	32301112928	394	0
12578619	t	1	2021-05-18 17:52:25.803944+00	pole	32301115428	396	0
12578604	t	0.989999999999999991	2021-05-18 17:52:25.679205+00	pole	32301115918	381	0
12578607	t	0.800000000000000044	2021-05-18 17:52:25.704246+00	pole	32500192704	384	0
12578606	f	0.0700000000000000067	2021-05-18 17:52:25.695542+00	pole	34801052114	383	0
12578687	f	0.209999999999999992	2021-07-06 20:14:39.861507+00	pole	31800150015	\N	\N
12578688	t	0.979999999999999982	2021-07-06 20:14:39.869517+00	pole	31801174924	\N	\N
12578689	t	1	2021-07-06 20:14:39.878232+00	pole	31801210104	\N	\N
12578690	t	1	2021-07-06 20:14:39.894494+00	pole	31900261724	\N	\N
12578691	t	1	2021-07-06 20:14:39.903198+00	pole	31900403905	\N	\N
12578692	t	0.989999999999999991	2021-07-06 20:14:39.911657+00	pole	31901122921	\N	\N
12578693	t	1	2021-07-06 20:14:39.928292+00	pole	31901543714	\N	\N
12578694	t	0.82999999999999996	2021-07-06 20:14:39.936798+00	pole	32300032314	\N	\N
12578695	f	0.209999999999999992	2021-07-06 20:14:39.944383+00	pole	32300171012	\N	\N
12578696	f	0.0700000000000000067	2021-07-06 20:14:39.953222+00	pole	32300263521	\N	\N
12578697	t	0.939999999999999947	2021-07-06 20:14:39.961591+00	pole	32300293221	\N	\N
12578698	f	0.340000000000000024	2021-07-06 20:14:39.986684+00	pole	32300441828	\N	\N
12578699	f	0.190000000000000002	2021-07-06 20:14:40.003382+00	pole	32300491609	\N	\N
12578700	t	1	2021-07-06 20:14:40.011712+00	pole	32301084418	\N	\N
12578701	t	1	2021-07-06 20:14:40.027912+00	pole	32301084508	\N	\N
12578702	t	1	2021-07-06 20:14:40.036751+00	pole	32301084519	\N	\N
12578703	t	0.989999999999999991	2021-07-06 20:14:40.044814+00	pole	32301084528	\N	\N
12578704	t	1	2021-07-06 20:14:40.061878+00	pole	32301084619	\N	\N
12578294	t	0.900000000000000022	2021-05-18 17:52:22.8517+00	pole	32301084628	71	0
12578705	t	0.859999999999999987	2021-07-06 20:14:40.10339+00	pole	32301084709	\N	\N
12578706	t	0.969999999999999973	2021-07-06 20:14:40.111817+00	pole	32301084718	\N	\N
12578707	t	0.859999999999999987	2021-07-06 20:14:40.119604+00	pole	32301084728	\N	\N
12578708	t	0.930000000000000049	2021-07-06 20:14:40.128363+00	pole	32301084808	\N	\N
12578709	t	0.939999999999999947	2021-07-06 20:14:40.13682+00	pole	32301084818	\N	\N
12578710	t	0.949999999999999956	2021-07-06 20:14:40.144761+00	pole	32301084828	\N	\N
12578711	t	0.979999999999999982	2021-07-06 20:14:40.153644+00	pole	32301084908	\N	\N
12578712	t	0.969999999999999973	2021-07-06 20:14:40.169902+00	pole	32301084929	\N	\N
12578713	t	0.890000000000000013	2021-07-06 20:14:40.178421+00	pole	32301085009	\N	\N
12578714	t	0.949999999999999956	2021-07-06 20:14:40.194668+00	pole	32301085028	\N	\N
12578715	t	0.989999999999999991	2021-07-06 20:14:40.228495+00	pole	32301085208	\N	\N
12578716	t	1	2021-07-06 20:14:40.244651+00	pole	32301085228	\N	\N
12578717	t	1	2021-07-06 20:14:40.253554+00	pole	32301085308	\N	\N
12578718	t	0.989999999999999991	2021-07-06 20:14:40.261956+00	pole	32301085318	\N	\N
12578719	t	0.989999999999999991	2021-07-06 20:14:40.278572+00	pole	32301085408	\N	\N
12578720	t	1	2021-07-06 20:14:40.28692+00	pole	32301085418	\N	\N
12578721	t	0.989999999999999991	2021-07-06 20:14:40.30351+00	pole	32301085508	\N	\N
12578722	t	1	2021-07-06 20:14:40.312187+00	pole	32301085518	\N	\N
12578723	t	0.989999999999999991	2021-07-06 20:14:40.319704+00	pole	32301085528	\N	\N
12578724	t	1	2021-07-06 20:14:40.353463+00	pole	32301085709	\N	\N
12578725	t	0.959999999999999964	2021-07-06 20:14:40.369745+00	pole	32301085729	\N	\N
12578726	t	0.989999999999999991	2021-07-06 20:14:40.386882+00	pole	32301085818	\N	\N
12578727	f	0.510000000000000009	2021-07-06 20:14:40.412185+00	pole	32301085918	\N	\N
12578728	t	0.959999999999999964	2021-07-06 20:14:40.419835+00	pole	32301085928	\N	\N
12578729	t	0.780000000000000027	2021-07-06 20:14:40.428581+00	pole	32301090008	\N	\N
12578730	t	0.760000000000000009	2021-07-06 20:14:40.486893+00	pole	32301090218	\N	\N
12578731	t	0.75	2021-07-06 20:14:40.503517+00	pole	32301090309	\N	\N
12578732	t	0.989999999999999991	2021-07-06 20:14:40.528518+00	pole	32301090409	\N	\N
12578733	t	0.979999999999999982	2021-07-06 20:14:40.544814+00	pole	32301090428	\N	\N
12578734	t	0.969999999999999973	2021-07-06 20:14:40.553617+00	pole	32301090508	\N	\N
12578735	t	1	2021-07-06 20:14:40.569814+00	pole	32301090529	\N	\N
12578736	f	0.380000000000000004	2021-07-06 20:14:40.619846+00	pole	32301090728	\N	\N
12578737	f	0.280000000000000027	2021-07-06 20:14:40.628523+00	pole	32301090808	\N	\N
12578738	f	0.330000000000000016	2021-07-06 20:14:40.637124+00	pole	32301090819	\N	\N
12578739	f	0.220000000000000001	2021-07-06 20:14:40.653762+00	pole	32301090908	\N	\N
12578740	t	0.75	2021-07-06 20:14:40.669854+00	pole	32301090928	\N	\N
12578741	f	0.440000000000000002	2021-07-06 20:14:40.68709+00	pole	32301091018	\N	\N
12578742	t	1	2021-07-06 20:14:40.703697+00	pole	32301091109	\N	\N
12578743	t	0.75	2021-07-06 20:14:40.720008+00	pole	32301091128	\N	\N
12578744	t	0.939999999999999947	2021-07-06 20:14:40.737119+00	pole	32301091218	\N	\N
12578745	t	0.959999999999999964	2021-07-06 20:14:40.744972+00	pole	32301091228	\N	\N
12578746	t	0.979999999999999982	2021-07-06 20:14:40.753671+00	pole	32301091308	\N	\N
12578747	t	1	2021-07-06 20:14:40.7788+00	pole	32301091409	\N	\N
12578748	t	1	2021-07-06 20:14:40.787113+00	pole	32301091418	\N	\N
12578749	t	1	2021-07-06 20:14:40.803738+00	pole	32301091509	\N	\N
12578750	t	1	2021-07-06 20:14:40.820229+00	pole	32301091528	\N	\N
12578751	t	0.989999999999999991	2021-07-06 20:14:40.837145+00	pole	32301091618	\N	\N
12578752	t	0.949999999999999956	2021-07-06 20:14:40.876352+00	pole	32301091718	\N	\N
12578753	t	0.969999999999999973	2021-07-06 20:14:40.914207+00	pole	32301091729	\N	\N
12578754	t	0.989999999999999991	2021-07-06 20:14:40.953711+00	pole	32301091829	\N	\N
12578755	t	0.989999999999999991	2021-07-06 20:14:40.962166+00	pole	32301091909	\N	\N
12578756	t	0.989999999999999991	2021-07-06 20:14:40.978565+00	pole	32301091928	\N	\N
12578757	t	0.989999999999999991	2021-07-06 20:14:40.987301+00	pole	32301092009	\N	\N
12578758	t	0.92000000000000004	2021-07-06 20:14:41.02051+00	pole	32301092119	\N	\N
12578759	t	0.989999999999999991	2021-07-06 20:14:41.037321+00	pole	32301092208	\N	\N
12578760	t	1	2021-07-06 20:14:41.062281+00	pole	32301092309	\N	\N
12578761	t	1	2021-07-06 20:14:41.070534+00	pole	32301092318	\N	\N
12578762	t	0.989999999999999991	2021-07-06 20:14:41.087377+00	pole	32301092408	\N	\N
12578428	t	1	2021-05-18 17:52:24.202311+00	pole	32301092428	205	0
12578763	t	0.989999999999999991	2021-07-06 20:14:41.13755+00	pole	32301092608	\N	\N
12578764	t	0.959999999999999964	2021-07-06 20:14:41.178575+00	pole	32301092729	\N	\N
12578584	t	0.989999999999999991	2021-05-18 17:52:25.512246+00	pole	32301092819	361	0
12578765	t	0.680000000000000049	2021-07-06 20:14:41.212478+00	pole	32301092908	\N	\N
12578766	f	0.540000000000000036	2021-07-06 20:14:41.23709+00	pole	32301093009	\N	\N
12578767	f	0.239999999999999991	2021-07-06 20:14:41.245718+00	pole	32301093018	\N	\N
12578768	t	0.949999999999999956	2021-07-06 20:14:41.262422+00	pole	32301093108	\N	\N
12578769	t	0.839999999999999969	2021-07-06 20:14:41.278911+00	pole	32301093128	\N	\N
12578770	f	0.469999999999999973	2021-07-06 20:14:41.287392+00	pole	32301093208	\N	\N
12578771	f	0.140000000000000013	2021-07-06 20:14:41.295116+00	pole	32301093219	\N	\N
12578772	f	0.0500000000000000028	2021-07-06 20:14:41.304004+00	pole	32301093229	\N	\N
12578773	f	0.0500000000000000028	2021-07-06 20:14:41.312484+00	pole	32301093309	\N	\N
12578774	f	0.330000000000000016	2021-07-06 20:14:41.328978+00	pole	32301093328	\N	\N
12578775	f	0.340000000000000024	2021-07-06 20:14:41.345182+00	pole	32301093419	\N	\N
12578776	f	0.209999999999999992	2021-07-06 20:14:41.353832+00	pole	32301093428	\N	\N
12578777	f	0.390000000000000013	2021-07-06 20:14:41.370329+00	pole	32301093518	\N	\N
12578778	t	0.849999999999999978	2021-07-06 20:14:41.378879+00	pole	32301093529	\N	\N
12578779	f	0.640000000000000013	2021-07-06 20:14:41.387428+00	pole	32301093608	\N	\N
12578382	f	0.28999999999999998	2021-05-18 17:52:23.818764+00	pole	32301093628	159	0
12578780	f	0.320000000000000007	2021-07-06 20:14:41.412612+00	pole	32301093708	\N	\N
12578781	f	0.510000000000000009	2021-07-06 20:14:41.42897+00	pole	32301093729	\N	\N
12578782	f	0.220000000000000001	2021-07-06 20:14:41.445339+00	pole	32301093818	\N	\N
12578783	f	0.400000000000000022	2021-07-06 20:14:41.495403+00	pole	32301094019	\N	\N
12578784	f	0.530000000000000027	2021-07-06 20:14:41.503978+00	pole	32301094028	\N	\N
12578785	t	0.810000000000000053	2021-07-06 20:14:41.512354+00	pole	32301094109	\N	\N
12578786	t	0.699999999999999956	2021-07-06 20:14:41.537444+00	pole	32301094208	\N	\N
12578787	f	0.560000000000000053	2021-07-06 20:14:41.545125+00	pole	32301094219	\N	\N
12578788	t	0.810000000000000053	2021-07-06 20:14:41.570329+00	pole	32301094318	\N	\N
12578789	t	0.949999999999999956	2021-07-06 20:14:41.587541+00	pole	32301094409	\N	\N
12578790	t	0.969999999999999973	2021-07-06 20:14:41.595146+00	pole	32301094418	\N	\N
12578791	t	0.959999999999999964	2021-07-06 20:14:41.612483+00	pole	32301094508	\N	\N
12578792	t	0.989999999999999991	2021-07-06 20:14:41.620278+00	pole	32301094519	\N	\N
12578793	t	0.989999999999999991	2021-07-06 20:14:41.637399+00	pole	32301094609	\N	\N
12578794	t	0.979999999999999982	2021-07-06 20:14:41.64531+00	pole	32301094618	\N	\N
12578795	t	0.989999999999999991	2021-07-06 20:14:41.704232+00	pole	32301094829	\N	\N
12578796	t	1	2021-07-06 20:14:41.712446+00	pole	32301094909	\N	\N
12578797	t	1	2021-07-06 20:14:41.72029+00	pole	32301094918	\N	\N
12578798	t	1	2021-07-06 20:14:41.728664+00	pole	32301094929	\N	\N
12578799	t	1	2021-07-06 20:14:41.745499+00	pole	32301095019	\N	\N
12578800	t	1	2021-07-06 20:14:41.754285+00	pole	32301095029	\N	\N
12578801	t	1	2021-07-06 20:14:41.779149+00	pole	32301095128	\N	\N
12578802	t	1	2021-07-06 20:14:41.78748+00	pole	32301095208	\N	\N
12578803	t	1	2021-07-06 20:14:41.795248+00	pole	32301095219	\N	\N
12578804	t	1	2021-07-06 20:14:41.804142+00	pole	32301095229	\N	\N
12578805	t	1	2021-07-06 20:14:41.812725+00	pole	32301095309	\N	\N
12578806	t	1	2021-07-06 20:14:41.829194+00	pole	32301095328	\N	\N
12578807	t	1	2021-07-06 20:14:41.837614+00	pole	32301095409	\N	\N
12578808	t	1	2021-07-06 20:14:41.845472+00	pole	32301095418	\N	\N
12578809	t	1	2021-07-06 20:14:41.879053+00	pole	32301095529	\N	\N
12578810	t	1	2021-07-06 20:14:41.921659+00	pole	32301095608	\N	\N
12578811	t	1	2021-07-06 20:14:41.929644+00	pole	32301095618	\N	\N
12578812	t	1	2021-07-06 20:14:41.93705+00	pole	32301095629	\N	\N
12578813	t	0.989999999999999991	2021-07-06 20:14:41.946076+00	pole	32301095708	\N	\N
12578814	t	0.949999999999999956	2021-07-06 20:14:41.962314+00	pole	32301095728	\N	\N
12578815	t	0.910000000000000031	2021-07-06 20:14:42.32252+00	pole	32301095828	\N	\N
12578816	t	0.719999999999999973	2021-07-06 20:14:42.339071+00	pole	32301095908	\N	\N
12578817	t	0.739999999999999991	2021-07-06 20:14:42.363636+00	pole	32301095928	\N	\N
12578818	t	0.930000000000000049	2021-07-06 20:14:42.370867+00	pole	32301100009	\N	\N
12578819	t	0.839999999999999969	2021-07-06 20:14:42.379403+00	pole	32301100019	\N	\N
12578820	t	0.989999999999999991	2021-07-06 20:14:42.413166+00	pole	32301100128	\N	\N
12578234	t	0.880000000000000004	2021-05-18 17:52:22.252581+00	pole	32301100229	11	0
12578821	t	0.959999999999999964	2021-07-06 20:14:42.455805+00	pole	32301100319	\N	\N
12578822	t	0.92000000000000004	2021-07-06 20:14:42.464446+00	pole	32301100328	\N	\N
12578823	t	0.930000000000000049	2021-07-06 20:14:42.480596+00	pole	32301100418	\N	\N
12578824	t	0.760000000000000009	2021-07-06 20:14:42.489167+00	pole	32301100428	\N	\N
12578825	t	0.959999999999999964	2021-07-06 20:14:42.50612+00	pole	32301100518	\N	\N
12578826	t	0.930000000000000049	2021-07-06 20:14:42.530469+00	pole	32301100619	\N	\N
12578827	t	0.969999999999999973	2021-07-06 20:14:42.539364+00	pole	32301100629	\N	\N
12578828	t	0.989999999999999991	2021-07-06 20:14:42.580754+00	pole	32301100818	\N	\N
12578829	t	0.969999999999999973	2021-07-06 20:14:42.589475+00	pole	32301100829	\N	\N
12578830	t	0.969999999999999973	2021-07-06 20:14:42.597736+00	pole	32301100908	\N	\N
12578831	t	0.969999999999999973	2021-07-06 20:14:42.630521+00	pole	32301101019	\N	\N
12578832	t	0.979999999999999982	2021-07-06 20:14:42.655709+00	pole	32301101119	\N	\N
12578833	t	0.989999999999999991	2021-07-06 20:14:42.672896+00	pole	32301101209	\N	\N
12578834	f	0.25	2021-07-06 20:14:42.697685+00	pole	32301101308	\N	\N
12578835	f	0.660000000000000031	2021-07-06 20:14:42.705613+00	pole	32301101319	\N	\N
12578836	t	0.67000000000000004	2021-07-06 20:14:42.714232+00	pole	32301101329	\N	\N
12578837	f	0.550000000000000044	2021-07-06 20:14:42.730565+00	pole	32301101418	\N	\N
12578838	t	0.67000000000000004	2021-07-06 20:14:42.739438+00	pole	32301101429	\N	\N
12578839	t	0.979999999999999982	2021-07-06 20:14:42.755488+00	pole	32301101519	\N	\N
12578840	t	0.849999999999999978	2021-07-06 20:14:42.798705+00	pole	32301101618	\N	\N
12578841	t	1	2021-07-06 20:14:42.823002+00	pole	32301101718	\N	\N
12578842	t	0.989999999999999991	2021-07-06 20:14:42.830589+00	pole	32301101728	\N	\N
12578518	t	1	2021-05-18 17:52:24.953495+00	pole	32301101809	295	0
12578843	t	0.979999999999999982	2021-07-06 20:14:42.86451+00	pole	32301101908	\N	\N
12578844	t	0.969999999999999973	2021-07-06 20:14:42.873037+00	pole	32301101919	\N	\N
12578845	t	0.969999999999999973	2021-07-06 20:14:42.880519+00	pole	32301101928	\N	\N
12578355	t	0.989999999999999991	2021-05-18 17:52:23.360057+00	pole	32301102009	132	0
12578846	f	0.179999999999999993	2021-07-06 20:14:42.905442+00	pole	32301102029	\N	\N
12578847	f	0.320000000000000007	2021-07-06 20:14:42.914172+00	pole	32301102109	\N	\N
12578848	f	0.479999999999999982	2021-07-06 20:14:42.922715+00	pole	32301102118	\N	\N
12578849	f	0.640000000000000013	2021-07-06 20:14:42.931016+00	pole	32301102128	\N	\N
12578850	f	0.280000000000000027	2021-07-06 20:14:42.947719+00	pole	32301102219	\N	\N
12578851	f	0.359999999999999987	2021-07-06 20:14:42.955577+00	pole	32301102228	\N	\N
12578852	f	0.650000000000000022	2021-07-06 20:14:42.989844+00	pole	32301102318	\N	\N
12578853	f	0.220000000000000001	2021-07-06 20:14:42.998221+00	pole	32301102329	\N	\N
12578854	f	0.440000000000000002	2021-07-06 20:14:43.039447+00	pole	32301102519	\N	\N
12578855	f	0.510000000000000009	2021-07-06 20:14:43.048037+00	pole	32301102528	\N	\N
12578856	f	0.609999999999999987	2021-07-06 20:14:43.064456+00	pole	32301102619	\N	\N
12578505	f	0.57999999999999996	2021-05-18 17:52:24.844907+00	pole	32301102628	282	0
12578857	f	0.280000000000000027	2021-07-06 20:14:43.089587+00	pole	32301102718	\N	\N
12578858	t	0.800000000000000044	2021-07-06 20:14:43.105567+00	pole	32301102809	\N	\N
12578859	t	0.969999999999999973	2021-07-06 20:14:43.139363+00	pole	32301102919	\N	\N
12578860	t	0.989999999999999991	2021-07-06 20:14:43.147692+00	pole	32301102929	\N	\N
12578861	t	1	2021-07-06 20:14:43.155539+00	pole	32301103008	\N	\N
12578862	t	1	2021-07-06 20:14:43.172992+00	pole	32301103028	\N	\N
12578863	t	1	2021-07-06 20:14:43.189723+00	pole	32301103108	\N	\N
12578864	t	1	2021-07-06 20:14:43.198009+00	pole	32301103119	\N	\N
12578865	t	0.989999999999999991	2021-07-06 20:14:43.214662+00	pole	32301103208	\N	\N
12578866	t	1	2021-07-06 20:14:43.239774+00	pole	32301103308	\N	\N
12578867	f	0.419999999999999984	2021-07-06 20:14:43.247715+00	pole	32301103318	\N	\N
12578868	t	0.719999999999999973	2021-07-06 20:14:43.255813+00	pole	32301103329	\N	\N
12578869	t	0.75	2021-07-06 20:14:43.264477+00	pole	32301103409	\N	\N
12578870	t	1	2021-07-06 20:14:43.289094+00	pole	32301103509	\N	\N
12578871	t	1	2021-07-06 20:14:43.297747+00	pole	32301103518	\N	\N
12578872	t	1	2021-07-06 20:14:43.306246+00	pole	32301103529	\N	\N
12578873	t	1	2021-07-06 20:14:43.314788+00	pole	32301103608	\N	\N
12578874	t	1	2021-07-06 20:14:43.331206+00	pole	32301103628	\N	\N
12578875	t	0.989999999999999991	2021-07-06 20:14:43.347387+00	pole	32301103718	\N	\N
12578876	t	1	2021-07-06 20:14:43.364584+00	pole	32301103808	\N	\N
12578877	f	0.390000000000000013	2021-07-06 20:14:43.381196+00	pole	32301103829	\N	\N
12578878	t	0.780000000000000027	2021-07-06 20:14:43.406837+00	pole	32301103909	\N	\N
12578879	t	0.800000000000000044	2021-07-06 20:14:43.422575+00	pole	32301103928	\N	\N
12578880	t	0.709999999999999964	2021-07-06 20:14:43.447597+00	pole	32301104028	\N	\N
12578881	t	0.989999999999999991	2021-07-06 20:14:43.473204+00	pole	32301104129	\N	\N
12578882	t	1	2021-07-06 20:14:43.481504+00	pole	32301104208	\N	\N
12578883	t	1	2021-07-06 20:14:43.497341+00	pole	32301104229	\N	\N
12578884	t	1	2021-07-06 20:14:43.506382+00	pole	32301104308	\N	\N
12578885	t	0.75	2021-07-06 20:14:43.556203+00	pole	32301104509	\N	\N
12578886	t	0.800000000000000044	2021-07-06 20:14:43.564406+00	pole	32301104518	\N	\N
12578887	t	0.890000000000000013	2021-07-06 20:14:43.572215+00	pole	32301104529	\N	\N
12578888	t	0.959999999999999964	2021-07-06 20:14:43.581281+00	pole	32301104609	\N	\N
12578889	t	0.760000000000000009	2021-07-06 20:14:43.589752+00	pole	32301104618	\N	\N
12578890	t	0.859999999999999987	2021-07-06 20:14:43.614473+00	pole	32301104718	\N	\N
12578891	t	0.859999999999999987	2021-07-06 20:14:43.622436+00	pole	32301104728	\N	\N
12578892	t	0.900000000000000022	2021-07-06 20:14:43.639813+00	pole	32301104818	\N	\N
12578893	t	0.979999999999999982	2021-07-06 20:14:43.647642+00	pole	32301104829	\N	\N
12578894	t	0.900000000000000022	2021-07-06 20:14:43.656122+00	pole	32301104908	\N	\N
12578895	t	0.890000000000000013	2021-07-06 20:14:43.672573+00	pole	32301104928	\N	\N
12578896	t	0.739999999999999991	2021-07-06 20:14:43.681243+00	pole	32301105008	\N	\N
12578897	t	0.689999999999999947	2021-07-06 20:14:43.698025+00	pole	32301105028	\N	\N
12578898	t	0.680000000000000049	2021-07-06 20:14:43.706148+00	pole	32301105108	\N	\N
12578899	f	0.630000000000000004	2021-07-06 20:14:43.714905+00	pole	32301105118	\N	\N
12578900	t	0.869999999999999996	2021-07-06 20:14:43.748432+00	pole	32301105229	\N	\N
12578901	t	0.989999999999999991	2021-07-06 20:14:43.75614+00	pole	32301105308	\N	\N
12578902	t	1	2021-07-06 20:14:43.789888+00	pole	32301105418	\N	\N
12578903	t	1	2021-07-06 20:14:43.798267+00	pole	32301105428	\N	\N
12578904	t	0.989999999999999991	2021-07-06 20:14:43.806327+00	pole	32301105508	\N	\N
12578905	t	0.989999999999999991	2021-07-06 20:14:43.814951+00	pole	32301105519	\N	\N
12578906	t	1	2021-07-06 20:14:43.823338+00	pole	32301105529	\N	\N
12578907	t	1	2021-07-06 20:14:43.839826+00	pole	32301105618	\N	\N
12578908	t	1	2021-07-06 20:14:43.848343+00	pole	32301105628	\N	\N
12578909	t	1	2021-07-06 20:14:43.856199+00	pole	32301105708	\N	\N
12578910	t	1	2021-07-06 20:14:43.864781+00	pole	32301105719	\N	\N
12578911	t	0.989999999999999991	2021-07-06 20:14:43.923501+00	pole	32301105809	\N	\N
12578912	t	0.989999999999999991	2021-07-06 20:14:43.939747+00	pole	32301105828	\N	\N
12578913	t	0.979999999999999982	2021-07-06 20:14:43.956835+00	pole	32301105918	\N	\N
12578914	t	1	2021-07-06 20:14:43.98184+00	pole	32301110019	\N	\N
12578915	t	1	2021-07-06 20:14:43.990288+00	pole	32301110029	\N	\N
12578916	t	0.979999999999999982	2021-07-06 20:14:43.997815+00	pole	32301110109	\N	\N
12578917	t	1	2021-07-06 20:14:44.015271+00	pole	32301110129	\N	\N
12578918	t	0.979999999999999982	2021-07-06 20:14:44.031601+00	pole	32301110219	\N	\N
12578919	t	1	2021-07-06 20:14:44.056736+00	pole	32301110318	\N	\N
12578920	t	1	2021-07-06 20:14:44.065034+00	pole	32301110329	\N	\N
12578921	t	1	2021-07-06 20:14:44.07284+00	pole	32301110409	\N	\N
12578922	t	1	2021-07-06 20:14:44.090259+00	pole	32301110429	\N	\N
12578923	t	1	2021-07-06 20:14:44.098039+00	pole	32301110509	\N	\N
12578924	t	1	2021-07-06 20:14:44.122962+00	pole	32301110609	\N	\N
12578925	t	1	2021-07-06 20:14:44.131861+00	pole	32301110619	\N	\N
12578926	t	1	2021-07-06 20:14:44.140149+00	pole	32301110629	\N	\N
12578927	t	1	2021-07-06 20:14:44.147823+00	pole	32301110709	\N	\N
12578928	t	1	2021-07-06 20:14:44.173017+00	pole	32301110809	\N	\N
12578929	t	1	2021-07-06 20:14:44.206643+00	pole	32301110919	\N	\N
12578930	t	0.760000000000000009	2021-07-06 20:14:44.240165+00	pole	32301111029	\N	\N
12578931	t	0.880000000000000004	2021-07-06 20:14:44.247973+00	pole	32301111109	\N	\N
12578932	t	0.989999999999999991	2021-07-06 20:14:44.256644+00	pole	32301111119	\N	\N
12578933	t	1	2021-07-06 20:14:44.265159+00	pole	32301111129	\N	\N
12578934	t	1	2021-07-06 20:14:44.272926+00	pole	32301111209	\N	\N
12578935	t	1	2021-07-06 20:14:44.281498+00	pole	32301111218	\N	\N
12578936	t	1	2021-07-06 20:14:44.290189+00	pole	32301111228	\N	\N
12578937	t	1	2021-07-06 20:14:44.297933+00	pole	32301111308	\N	\N
12578938	t	1	2021-07-06 20:14:44.306752+00	pole	32301111318	\N	\N
12578939	t	1	2021-07-06 20:14:44.315333+00	pole	32301111328	\N	\N
12578940	t	1	2021-07-06 20:14:44.33161+00	pole	32301111419	\N	\N
12578941	t	1	2021-07-06 20:14:44.340069+00	pole	32301111428	\N	\N
12578942	t	0.989999999999999991	2021-07-06 20:14:44.356901+00	pole	32301111518	\N	\N
12578943	t	1	2021-07-06 20:14:44.365159+00	pole	32301111529	\N	\N
12578944	t	1	2021-07-06 20:14:44.372915+00	pole	32301111609	\N	\N
12578945	t	0.989999999999999991	2021-07-06 20:14:44.381787+00	pole	32301111619	\N	\N
12578946	t	1	2021-07-06 20:14:44.389985+00	pole	32301111629	\N	\N
12578947	t	1	2021-07-06 20:14:44.398116+00	pole	32301111709	\N	\N
12578948	t	1	2021-07-06 20:14:44.415244+00	pole	32301111729	\N	\N
12578251	t	1	2021-05-18 17:52:22.494302+00	pole	32301111808	28	0
12578949	t	1	2021-07-06 20:14:44.431603+00	pole	32301111818	\N	\N
12578950	t	1	2021-07-06 20:14:44.439818+00	pole	32301111828	\N	\N
12578951	t	1	2021-07-06 20:14:44.448069+00	pole	32301111909	\N	\N
12578952	t	1	2021-07-06 20:14:44.456729+00	pole	32301111918	\N	\N
12578953	t	1	2021-07-06 20:14:44.48186+00	pole	32301112018	\N	\N
12578954	t	1	2021-07-06 20:14:44.498087+00	pole	32301112108	\N	\N
12578955	t	1	2021-07-06 20:14:44.506745+00	pole	32301112119	\N	\N
12578956	t	1	2021-07-06 20:14:44.515472+00	pole	32301112129	\N	\N
12578957	t	0.979999999999999982	2021-07-06 20:14:44.532015+00	pole	32301112219	\N	\N
12578958	t	0.979999999999999982	2021-07-06 20:14:44.540391+00	pole	32301112229	\N	\N
12578959	t	0.900000000000000022	2021-07-06 20:14:44.556941+00	pole	32301112319	\N	\N
12578960	t	1	2021-07-06 20:14:44.565009+00	pole	32301112329	\N	\N
12578961	t	0.989999999999999991	2021-07-06 20:14:44.573383+00	pole	32301112409	\N	\N
12578962	t	0.969999999999999973	2021-07-06 20:14:44.582075+00	pole	32301112419	\N	\N
12578963	f	0.170000000000000012	2021-07-06 20:14:44.598303+00	pole	32301112509	\N	\N
12578964	f	0.28999999999999998	2021-07-06 20:14:44.607355+00	pole	32301112519	\N	\N
12578965	f	0.119999999999999996	2021-07-06 20:14:44.615482+00	pole	32301112529	\N	\N
12578966	f	0.119999999999999996	2021-07-06 20:14:44.640396+00	pole	32301112629	\N	\N
12578967	f	0.5	2021-07-06 20:14:44.648157+00	pole	32301112709	\N	\N
12578968	f	0.589999999999999969	2021-07-06 20:14:44.65692+00	pole	32301112719	\N	\N
12578969	t	0.729999999999999982	2021-07-06 20:14:44.665561+00	pole	32301112728	\N	\N
12578970	f	0.57999999999999996	2021-07-06 20:14:44.67321+00	pole	32301112808	\N	\N
12578971	t	0.699999999999999956	2021-07-06 20:14:44.682307+00	pole	32301112818	\N	\N
12578972	t	0.849999999999999978	2021-07-06 20:14:44.707198+00	pole	32301112918	\N	\N
12578973	t	0.989999999999999991	2021-07-06 20:14:44.723239+00	pole	32301113008	\N	\N
12578974	t	0.989999999999999991	2021-07-06 20:14:44.731785+00	pole	32301113019	\N	\N
12578975	t	0.959999999999999964	2021-07-06 20:14:44.740337+00	pole	32301113029	\N	\N
12578976	t	0.989999999999999991	2021-07-06 20:14:44.748387+00	pole	32301113108	\N	\N
12578977	t	1	2021-07-06 20:14:44.765368+00	pole	32301113129	\N	\N
12578978	t	1	2021-07-06 20:14:44.773556+00	pole	32301113209	\N	\N
12578979	t	1	2021-07-06 20:14:44.781774+00	pole	32301113218	\N	\N
12578980	t	1	2021-07-06 20:14:44.790471+00	pole	32301113228	\N	\N
12578981	t	1	2021-07-06 20:14:44.798278+00	pole	32301113308	\N	\N
12578982	t	1	2021-07-06 20:14:44.815506+00	pole	32301113328	\N	\N
12578983	t	1	2021-07-06 20:14:44.823317+00	pole	32301113408	\N	\N
12578984	t	1	2021-07-06 20:14:44.840238+00	pole	32301113428	\N	\N
12578985	t	1	2021-07-06 20:14:44.84855+00	pole	32301113508	\N	\N
12578986	t	1	2021-07-06 20:14:44.857331+00	pole	32301113518	\N	\N
12578457	t	1	2021-05-18 17:52:24.445101+00	pole	32301113529	234	0
12578987	t	1	2021-07-06 20:14:44.87314+00	pole	32301113609	\N	\N
12578988	t	1	2021-07-06 20:14:44.882022+00	pole	32301113619	\N	\N
12578989	t	1	2021-07-06 20:14:44.898426+00	pole	32301113709	\N	\N
12578990	t	1	2021-07-06 20:14:44.907208+00	pole	32301113719	\N	\N
12578991	t	1	2021-07-06 20:14:44.915427+00	pole	32301113729	\N	\N
12578992	t	1	2021-07-06 20:14:44.923355+00	pole	32301113809	\N	\N
12578993	t	1	2021-07-06 20:14:44.948423+00	pole	32301113909	\N	\N
12578994	t	1	2021-07-06 20:14:44.965528+00	pole	32301113929	\N	\N
12578995	t	1	2021-07-06 20:14:44.973266+00	pole	32301114008	\N	\N
12578996	t	1	2021-07-06 20:14:44.982281+00	pole	32301114018	\N	\N
12578997	t	1	2021-07-06 20:14:44.99065+00	pole	32301114028	\N	\N
12578998	t	1	2021-07-06 20:14:44.998307+00	pole	32301114108	\N	\N
12578999	t	0.989999999999999991	2021-07-06 20:14:45.006946+00	pole	32301114118	\N	\N
12579000	t	0.989999999999999991	2021-07-06 20:14:45.015457+00	pole	32301114128	\N	\N
12579001	t	0.989999999999999991	2021-07-06 20:14:45.032131+00	pole	32301114218	\N	\N
12579002	t	1	2021-07-06 20:14:45.040472+00	pole	32301114228	\N	\N
12579003	t	1	2021-07-06 20:14:45.057092+00	pole	32301114318	\N	\N
12579004	t	1	2021-07-06 20:14:45.065356+00	pole	32301114328	\N	\N
12578519	t	1	2021-05-18 17:52:24.962249+00	pole	32301114408	296	0
12579005	t	1	2021-07-06 20:14:45.090691+00	pole	32301114429	\N	\N
12579006	t	1	2021-07-06 20:14:45.098234+00	pole	32301114509	\N	\N
12579007	t	1	2021-07-06 20:14:45.106965+00	pole	32301114519	\N	\N
12579008	t	1	2021-07-06 20:14:45.123606+00	pole	32301114609	\N	\N
12579009	t	1	2021-07-06 20:14:45.132029+00	pole	32301114619	\N	\N
12579010	t	1	2021-07-06 20:14:45.140431+00	pole	32301114629	\N	\N
12579011	t	1	2021-07-06 20:14:45.157274+00	pole	32301114719	\N	\N
12579012	t	1	2021-07-06 20:14:45.173525+00	pole	32301114809	\N	\N
12579013	t	1	2021-07-06 20:14:45.181907+00	pole	32301114819	\N	\N
12579014	t	1	2021-07-06 20:14:45.2157+00	pole	32301114928	\N	\N
12579015	t	1	2021-07-06 20:14:45.223202+00	pole	32301115009	\N	\N
12579016	t	1	2021-07-06 20:14:45.232038+00	pole	32301115018	\N	\N
12579017	t	1	2021-07-06 20:14:45.265462+00	pole	32301115128	\N	\N
12579018	t	1	2021-07-06 20:14:45.273482+00	pole	32301115209	\N	\N
12579019	t	1	2021-07-06 20:14:45.290533+00	pole	32301115229	\N	\N
12579020	t	0.979999999999999982	2021-07-06 20:14:45.298414+00	pole	32301115309	\N	\N
12579021	t	0.979999999999999982	2021-07-06 20:14:45.307171+00	pole	32301115318	\N	\N
12579022	t	1	2021-07-06 20:14:45.315564+00	pole	32301115328	\N	\N
12579023	t	1	2021-07-06 20:14:45.332565+00	pole	32301115419	\N	\N
12579024	t	1	2021-07-06 20:14:45.348296+00	pole	32301115509	\N	\N
12579025	t	1	2021-07-06 20:14:45.356886+00	pole	32301115518	\N	\N
12578404	t	1	2021-05-18 17:52:24.002409+00	pole	32301115609	181	0
12579026	t	1	2021-07-06 20:14:45.382732+00	pole	32301115618	\N	\N
12579027	t	1	2021-07-06 20:14:45.390917+00	pole	32301115628	\N	\N
12579028	t	1	2021-07-06 20:14:45.407134+00	pole	32301115719	\N	\N
12579029	t	1	2021-07-06 20:14:45.415553+00	pole	32301115729	\N	\N
12579030	t	1	2021-07-06 20:14:45.423405+00	pole	32301115809	\N	\N
12579031	t	1	2021-07-06 20:14:45.4406+00	pole	32301115828	\N	\N
12579032	t	0.989999999999999991	2021-07-06 20:14:45.448607+00	pole	32301115909	\N	\N
12579033	t	1	2021-07-06 20:14:45.465571+00	pole	32301115928	\N	\N
12579034	t	0.989999999999999991	2021-07-06 20:14:45.473299+00	pole	32301120008	\N	\N
12579035	t	1	2021-07-06 20:14:45.482443+00	pole	32301120018	\N	\N
12579036	t	1	2021-07-06 20:14:45.498355+00	pole	32301120108	\N	\N
12579037	t	0.969999999999999973	2021-07-06 20:14:45.515795+00	pole	32301120128	\N	\N
12579038	t	1	2021-07-06 20:14:45.540763+00	pole	32301120228	\N	\N
12579039	t	1	2021-07-06 20:14:45.557542+00	pole	32301120319	\N	\N
12579040	t	0.989999999999999991	2021-07-06 20:14:45.574127+00	pole	32301120409	\N	\N
12579041	t	1	2021-07-06 20:14:45.582265+00	pole	32301120418	\N	\N
12579042	t	1	2021-07-06 20:14:45.590347+00	pole	32301120428	\N	\N
12579043	t	1	2021-07-06 20:14:45.607609+00	pole	32301120518	\N	\N
12579044	t	1	2021-07-06 20:14:45.615675+00	pole	32301120528	\N	\N
12579045	t	1	2021-07-06 20:14:45.623681+00	pole	32301120608	\N	\N
12579046	t	1	2021-07-06 20:14:45.632433+00	pole	32301120619	\N	\N
12579047	t	1	2021-07-06 20:14:45.640634+00	pole	32301120628	\N	\N
12579048	t	1	2021-07-06 20:14:45.682542+00	pole	32301120818	\N	\N
12579049	t	0.989999999999999991	2021-07-06 20:14:45.71582+00	pole	32301120928	\N	\N
12579050	t	0.989999999999999991	2021-07-06 20:14:45.740858+00	pole	32301121028	\N	\N
12579051	f	0.0200000000000000004	2021-07-06 20:14:45.75728+00	pole	32301121118	\N	\N
12579052	f	0.320000000000000007	2021-07-06 20:14:45.765319+00	pole	32301121128	\N	\N
12579053	f	0.0800000000000000017	2021-07-06 20:14:45.77427+00	pole	32301121208	\N	\N
12579054	f	0.0100000000000000002	2021-07-06 20:14:45.799565+00	pole	32301121228	\N	\N
12579055	t	0.780000000000000027	2021-07-06 20:14:45.80789+00	pole	32301121308	\N	\N
12579056	f	0.450000000000000011	2021-07-06 20:14:45.815138+00	pole	32301141114	\N	\N
12579057	t	1	2021-07-06 20:14:45.83241+00	pole	32301174026	\N	\N
12579058	t	0.969999999999999973	2021-07-06 20:14:45.840659+00	pole	32301201706	\N	\N
12579059	t	1	2021-07-06 20:14:45.85749+00	pole	32301231123	\N	\N
12579060	f	0.239999999999999991	2021-07-06 20:14:45.86543+00	pole	32301233503	\N	\N
12579061	f	0.0500000000000000028	2021-07-06 20:14:45.87433+00	pole	32301242313	\N	\N
12579062	t	1	2021-07-06 20:14:45.890605+00	pole	32301485709	\N	\N
12579063	f	0.0700000000000000067	2021-07-06 20:14:45.898894+00	pole	32301503324	\N	\N
12579064	t	0.780000000000000027	2021-07-06 20:14:45.916237+00	pole	32400265718	\N	\N
12579065	t	1	2021-07-06 20:14:45.938311+00	pole	32400271918	\N	\N
12579066	t	1	2021-07-06 20:14:45.975075+00	pole	32400325018	\N	\N
12579067	t	1	2021-07-06 20:14:45.999312+00	pole	32500195615	\N	\N
12579068	t	0.959999999999999964	2021-07-06 20:14:46.00715+00	pole	32500201714	\N	\N
12579069	t	0.819999999999999951	2021-07-06 20:14:46.024425+00	pole	32501014522	\N	\N
12579070	t	1	2021-07-06 20:14:46.040926+00	pole	32600594617	\N	\N
12579071	f	0.0100000000000000002	2021-07-06 20:14:46.091052+00	pole	32700385108	\N	\N
12579072	f	0.540000000000000036	2021-07-06 20:14:46.099488+00	pole	32801431112	\N	\N
12579073	t	1	2021-07-06 20:14:46.107224+00	pole	32801545104	\N	\N
12579074	f	0.270000000000000018	2021-07-06 20:14:46.115939+00	pole	33000081420	\N	\N
12579075	t	1	2021-07-06 20:14:46.124211+00	pole	33000085111	\N	\N
12579076	t	0.939999999999999947	2021-07-06 20:14:46.141096+00	pole	33301120926	\N	\N
12579077	f	0.0299999999999999989	2021-07-06 20:14:46.182143+00	pole	33501365412	\N	\N
12579078	f	0.260000000000000009	2021-07-06 20:14:46.190947+00	pole	33501402825	\N	\N
12579079	t	1	2021-07-06 20:14:46.1991+00	pole	33501434012	\N	\N
12579080	t	1	2021-07-06 20:14:46.207328+00	pole	33501452019	\N	\N
12579081	t	1	2021-07-06 20:14:46.216073+00	pole	33501464919	\N	\N
12579082	f	0.200000000000000011	2021-07-06 20:14:46.232237+00	pole	33600375407	\N	\N
12579083	t	0.930000000000000049	2021-07-06 20:14:46.257417+00	pole	33700352823	\N	\N
12579084	t	1	2021-07-06 20:14:46.266129+00	pole	33700365512	\N	\N
12579085	t	1	2021-07-06 20:14:46.282517+00	pole	33700545517	\N	\N
12579086	f	0.0200000000000000004	2021-07-06 20:14:46.29982+00	pole	33701165814	\N	\N
12578432	t	0.760000000000000009	2021-05-18 17:52:24.23545+00	pole	33701302323	209	0
12579087	f	0.119999999999999996	2021-07-06 20:14:46.32447+00	pole	33800504204	\N	\N
12579088	t	1	2021-07-06 20:14:46.332229+00	pole	33901182607	\N	\N
12579089	t	0.989999999999999991	2021-07-06 20:14:46.342427+00	pole	33901183127	\N	\N
12579090	t	1	2021-07-06 20:14:46.357717+00	pole	33901500703	\N	\N
12579091	t	1	2021-07-06 20:14:46.373908+00	pole	34000051510	\N	\N
12579092	t	1	2021-07-06 20:14:46.39883+00	pole	34000191222	\N	\N
12579093	t	1	2021-07-06 20:14:46.407653+00	pole	34001370803	\N	\N
12579094	t	1	2021-07-06 20:14:46.415966+00	pole	34100155616	\N	\N
12579095	t	0.900000000000000022	2021-07-06 20:14:46.423724+00	pole	34100205218	\N	\N
12579096	f	0.0500000000000000028	2021-07-06 20:14:46.466337+00	pole	34200012201	\N	\N
12579097	t	0.880000000000000004	2021-07-06 20:14:46.474048+00	pole	34200034707	\N	\N
12579098	f	0.0299999999999999989	2021-07-06 20:14:46.482752+00	pole	34201040410	\N	\N
12579099	t	0.92000000000000004	2021-07-06 20:14:46.499147+00	pole	34201362524	\N	\N
12579100	f	0.630000000000000004	2021-07-06 20:14:46.516319+00	pole	34300021410	\N	\N
12579101	f	0.190000000000000002	2021-07-06 20:14:46.524085+00	pole	34300400925	\N	\N
12579102	t	1	2021-07-06 20:14:46.532918+00	pole	34300541317	\N	\N
12579103	t	0.959999999999999964	2021-07-06 20:14:46.54106+00	pole	34301065629	\N	\N
12579104	f	0.0599999999999999978	2021-07-06 20:14:46.549048+00	pole	34301095009	\N	\N
12579105	t	0.939999999999999947	2021-07-06 20:14:46.557885+00	pole	34301145802	\N	\N
12579106	t	0.989999999999999991	2021-07-06 20:14:46.566484+00	pole	34301151912	\N	\N
12579107	t	0.939999999999999947	2021-07-06 20:14:46.591352+00	pole	34301294525	\N	\N
12579108	t	0.939999999999999947	2021-07-06 20:14:46.60798+00	pole	34301374813	\N	\N
12579109	f	0.309999999999999998	2021-07-06 20:14:46.616444+00	pole	34301424707	\N	\N
12579110	f	0.660000000000000031	2021-07-06 20:14:46.633101+00	pole	34301453523	\N	\N
12579111	f	0.0100000000000000002	2021-07-06 20:14:46.692166+00	pole	34400230020	\N	\N
12579112	t	0.839999999999999969	2021-07-06 20:14:46.707682+00	pole	34400303125	\N	\N
12579113	t	0.939999999999999947	2021-07-06 20:14:46.733252+00	pole	34400394006	\N	\N
12578586	f	0.0500000000000000028	2021-05-18 17:52:25.529225+00	pole	34400403205	363	0
12579114	f	0.149999999999999994	2021-07-06 20:14:46.749927+00	pole	34400592320	\N	\N
12579115	t	1	2021-07-06 20:14:46.757711+00	pole	34400595700	\N	\N
12579116	t	0.900000000000000022	2021-07-06 20:14:46.766081+00	pole	34401091323	\N	\N
12579117	f	0.419999999999999984	2021-07-06 20:14:46.7992+00	pole	34801083120	\N	\N
12579118	t	1	2021-07-06 20:14:46.807783+00	pole	34901293001	\N	\N
12579119	f	0.0100000000000000002	2021-07-06 20:14:46.841409+00	pole	35100560222	\N	\N
12579120	t	0.849999999999999978	2021-07-06 20:14:46.849439+00	pole	35101051713	\N	\N
12579121	t	1	2021-07-06 20:14:46.892099+00	pole	35101145524	\N	\N
12578317	f	0.530000000000000027	2021-05-18 17:52:23.043316+00	pole	35101182013	94	0
12579122	t	0.969999999999999973	2021-07-06 20:14:46.907695+00	pole	35101534826	\N	\N
12579123	f	0.239999999999999991	2021-07-06 20:14:46.916081+00	pole	35200154201	\N	\N
12579124	t	0.989999999999999991	2021-07-06 20:14:46.941028+00	pole	35401573022	\N	\N
12579125	t	0.989999999999999991	2021-07-06 20:14:46.949636+00	pole	35500575109	\N	\N
12579126	t	1	2021-07-06 20:14:46.958005+00	pole	35501070209	\N	\N
12579127	f	0.5	2021-07-06 20:14:46.965712+00	pole	35501085529	\N	\N
12579128	t	1	2021-07-06 20:14:46.974828+00	pole	35501091329	\N	\N
12579129	t	0.989999999999999991	2021-07-06 20:14:46.990981+00	pole	35501154425	\N	\N
12579130	f	0.5	2021-07-06 20:14:46.999518+00	pole	35501325128	\N	\N
12579131	f	0.650000000000000022	2021-07-06 20:14:47.008013+00	pole	35501425510	\N	\N
12579132	t	1	2021-07-06 20:14:47.015771+00	pole	35501541503	\N	\N
12579133	t	0.969999999999999973	2021-07-06 20:14:47.033258+00	pole	35600284809	\N	\N
12579134	f	0.220000000000000001	2021-07-06 20:14:47.041773+00	pole	35600501306	\N	\N
12579135	t	0.819999999999999951	2021-07-06 20:14:47.049457+00	pole	35600544319	\N	\N
12578262	t	1	2021-05-18 17:52:22.586178+00	pole	35601575210	39	0
12579136	t	1	2021-07-06 20:14:47.11621+00	pole	35601582220	\N	\N
12579137	t	1	2021-07-06 20:14:47.125072+00	pole	35700034310	\N	\N
12579138	t	1	2021-07-06 20:14:47.132835+00	pole	35700040920	\N	\N
12579139	t	1	2021-07-06 20:14:47.141574+00	pole	35700310103	\N	\N
12579140	t	1	2021-07-06 20:14:47.157644+00	pole	35701451127	\N	\N
12579141	t	1	2021-07-06 20:14:47.166166+00	pole	35801340023	\N	\N
12579142	t	0.699999999999999956	2021-07-06 20:14:47.20762+00	pole	36001265813	\N	\N
12579143	f	0.0599999999999999978	2021-07-06 20:14:47.224994+00	pole	42400135928	\N	\N
12579144	f	0.28999999999999998	2021-07-06 20:14:47.241408+00	pole	42400220307	\N	\N
12579145	f	0.0100000000000000002	2021-07-06 20:14:47.250208+00	pole	42400405229	\N	\N
12579146	f	0.0299999999999999989	2021-07-06 20:14:47.349759+00	pole	42501082612	\N	\N
12579147	t	0.930000000000000049	2021-07-06 20:14:47.358215+00	pole	42501115001	\N	\N
\.


--
-- Data for Name: rs_core_annotationflag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationflag (title) FROM stdin;
Fence
Obstructed
Edge of image
Atypical
\.


--
-- Data for Name: rs_core_annotationset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationset (name, type) FROM stdin;
guardrail	cont
pole	pt
\.


--
-- Data for Name: rs_core_annotationset_flags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationset_flags (id, annotationset_id, annotationflag_id) FROM stdin;
1	guardrail	Fence
2	guardrail	Obstructed
3	guardrail	Edge of image
4	guardrail	Atypical
\.


--
-- Data for Name: rs_core_holdouttestinfo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_holdouttestinfo (id, round_number, presence, in_balance_set, certainty, left_certainty, front_certainty, right_certainty, category, annotation_id, image_id) FROM stdin;
1	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	30000385923
2	5	f	t	0.419999999999999984	0	0.419999999999999984	0	tn	guardrail	30200062407
3	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	35801471221
4	5	f	t	0.699999999999999956	0	0.699999999999999956	0	fp	guardrail	35701451127
5	5	t	t	0.369999999999999996	0	0.369999999999999996	0	fn	guardrail	35700310103
6	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	35701420526
7	5	t	t	0.619999999999999996	0	0.619999999999999996	0	tp	guardrail	34400391623
8	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	34400300325
9	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	34400592320
10	5	f	t	0.599999999999999978	0	0.599999999999999978	0	fp	guardrail	34400303125
11	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	34400370205
12	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	34401091323
13	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	34400403205
14	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	35700040920
15	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	35501154425
16	5	f	t	0.510000000000000009	0	0.510000000000000009	0	fp	guardrail	35501070209
17	5	t	t	0.5	0	0.5	0	tp	guardrail	35501091329
18	5	f	t	0.0299999999999999989	0	0.0299999999999999989	0	tn	guardrail	35501425510
19	5	t	t	0.699999999999999956	0	0.699999999999999956	0	tp	guardrail	29901322813
20	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	29901341804
21	5	t	t	0.220000000000000001	0	0.220000000000000001	0	fn	guardrail	29901113229
22	5	f	t	0.969999999999999973	0	0.969999999999999973	0	fp	guardrail	29901194629
23	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	34400230020
24	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	34201521024
25	5	t	t	0.609999999999999987	0	0.609999999999999987	0	tp	guardrail	34201070010
26	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	16400161125
27	5	t	t	0.0899999999999999967	0	0.0899999999999999967	0	fn	guardrail	16301184725
28	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	16301023018
29	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	16300504528
30	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	16300222214
31	5	t	t	0.520000000000000018	0	0.520000000000000018	0	tp	guardrail	29901051509
32	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	29701443127
33	5	t	t	0.0400000000000000008	0	0.0400000000000000008	0	fn	guardrail	29701315222
34	5	f	t	0.650000000000000022	0	0.650000000000000022	0	fp	guardrail	29700553621
35	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	33301120926
36	5	f	t	0.25	0	0.25	0	tn	guardrail	31200424207
37	5	t	t	0.510000000000000009	0	0.510000000000000009	0	tp	guardrail	34901293001
38	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	34200012201
39	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	29700553101
40	5	f	t	0.979999999999999982	0	0.979999999999999982	0	fp	guardrail	30001011809
41	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	35801340023
42	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	16301022617
43	5	t	t	0.810000000000000053	0	0.810000000000000053	0	tp	guardrail	34400595700
44	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	35501325128
45	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	16100345009
46	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	34200034707
47	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	35401573022
48	5	f	t	0.0200000000000000004	0	0.0200000000000000004	0	tn	guardrail	29701261012
49	5	t	t	0.67000000000000004	0	0.67000000000000004	0	tp	guardrail	34201040410
50	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	33400080617
51	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	16101050612
52	5	f	t	0.560000000000000053	0	0.560000000000000053	0	fp	guardrail	29901432208
53	5	t	t	0.209999999999999992	0	0.209999999999999992	0	fn	guardrail	16302025413
54	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	30000272325
55	5	t	t	1	0	1	0	tp	guardrail	34400070221
56	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	16301245502
57	5	t	t	0.25	0	0.25	0	fn	guardrail	35501095409
58	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	16401575226
59	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	16100362400
60	5	f	t	0.479999999999999982	0	0.479999999999999982	0	tn	guardrail	30001205208
61	5	t	t	0.880000000000000004	0	0.880000000000000004	0	tp	guardrail	30200201401
62	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	29701532424
63	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	35700034310
64	5	f	t	0.67000000000000004	0	0.67000000000000004	0	fp	guardrail	33401471905
65	5	t	t	0.5	0	0.5	0	tp	guardrail	34400394006
66	5	f	t	0	0	0	0	tn	guardrail	16401215429
67	5	t	t	0.640000000000000013	0	0.640000000000000013	0	tp	guardrail	32400230908
68	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	30500211224
69	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	34100155616
70	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	30502041402
71	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	30500414711
72	5	f	t	0.429999999999999993	0	0.429999999999999993	0	tn	guardrail	30501412415
73	5	t	t	0.859999999999999987	0	0.859999999999999987	0	tp	guardrail	30500483409
74	5	f	t	0.479999999999999982	0	0.479999999999999982	0	tn	guardrail	31101314311
75	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	34801052114
76	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	34801083120
77	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	34100221828
78	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	34101115407
79	5	t	t	0.959999999999999964	0	0.959999999999999964	0	tp	guardrail	34100321517
80	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	22001132920
81	5	t	t	0.179999999999999993	0	0.179999999999999993	0	fn	guardrail	22000433201
82	5	f	t	0.689999999999999947	0	0.689999999999999947	0	fp	guardrail	15901333701
83	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	33000215519
84	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	32400313308
85	5	t	t	0.880000000000000004	0	0.880000000000000004	0	tp	guardrail	32400355028
86	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	32400325018
87	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	34100282611
88	5	f	t	0.699999999999999956	0	0.699999999999999956	0	fp	guardrail	32400271918
89	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	36001265813
90	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	15901324811
91	5	t	t	0.939999999999999947	0	0.939999999999999947	0	tp	guardrail	22000175809
92	5	f	t	0.0899999999999999967	0	0.0899999999999999967	0	tn	guardrail	15901091226
93	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	30400531116
94	5	f	t	0.770000000000000018	0	0.770000000000000018	0	fp	guardrail	30401232201
95	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	29601521527
96	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	29601422623
97	5	t	t	0.780000000000000027	0	0.780000000000000027	0	tp	guardrail	35101182013
98	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	35100180614
99	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	35101051713
100	5	f	t	0.849999999999999978	0	0.849999999999999978	0	fp	guardrail	32500201714
101	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	31901543714
102	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	31901522512
103	5	t	t	0.540000000000000036	0	0.540000000000000036	0	tp	guardrail	31900261724
104	5	f	t	0.5	0	0.5	0	fp	guardrail	31901122921
105	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	30901293205
106	5	f	t	0.989999999999999991	0	0.989999999999999991	0	fp	guardrail	32501014522
107	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	30400214412
108	5	f	t	0.179999999999999993	0	0.179999999999999993	0	tn	guardrail	31900161110
109	5	t	t	0.760000000000000009	0	0.760000000000000009	0	tp	guardrail	33800281503
110	5	f	t	0.479999999999999982	0	0.479999999999999982	0	tn	guardrail	30901224514
111	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	35100165617
112	5	f	t	0.640000000000000013	0	0.640000000000000013	0	fp	guardrail	35101534826
113	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	30900553212
114	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32500192704
115	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	30100424824
116	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	34100205218
117	5	t	t	0.0200000000000000004	0	0.0200000000000000004	0	fn	guardrail	32400265718
118	5	f	t	0.599999999999999978	0	0.599999999999999978	0	fp	guardrail	35100560222
119	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	36002001114
120	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	31900403905
121	5	t	t	0.660000000000000031	0	0.660000000000000031	0	tp	guardrail	15901225329
122	5	f	t	0.239999999999999991	0	0.239999999999999991	0	tn	guardrail	15901110815
123	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	30401182916
124	5	f	t	0.530000000000000027	0	0.530000000000000027	0	fp	guardrail	30401205318
125	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	32500195615
126	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	33000081420
127	5	t	t	0.699999999999999956	0	0.699999999999999956	0	tp	guardrail	33000085111
128	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	15901240029
129	5	t	t	0.209999999999999992	0	0.209999999999999992	0	fn	guardrail	30400480726
130	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	33800504204
131	5	t	t	0.130000000000000004	0	0.130000000000000004	0	fn	guardrail	35101145524
132	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	34800560920
133	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	31400173203
134	5	f	t	0.25	0	0.25	0	tn	guardrail	32501102524
135	5	t	t	0.270000000000000018	0	0.270000000000000018	0	fn	guardrail	32600594617
136	5	f	t	0.75	0	0.75	0	fp	guardrail	32700031900
137	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	42400450315
138	5	f	t	0.130000000000000004	0	0.130000000000000004	0	tn	guardrail	42401304003
139	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	42400405229
140	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	35601575210
141	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	35601190424
142	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	35601070529
143	5	t	t	0.28999999999999998	0	0.28999999999999998	0	fn	guardrail	35600544319
144	5	f	t	0.220000000000000001	0	0.220000000000000001	0	tn	guardrail	35601582220
145	5	t	t	0.550000000000000044	0	0.550000000000000044	0	tp	guardrail	33901183127
146	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	30801333508
147	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	30600402403
148	5	f	t	0.650000000000000022	0	0.650000000000000022	0	fp	guardrail	30601400420
149	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	30601263712
150	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	31600423514
151	5	t	t	0.599999999999999978	0	0.599999999999999978	0	tp	guardrail	31501442614
152	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	32801545104
153	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	31401385708
154	5	f	t	0.680000000000000049	0	0.680000000000000049	0	fp	guardrail	31500235705
155	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32801431112
156	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	32700170321
157	5	t	t	0.530000000000000027	0	0.530000000000000027	0	tp	guardrail	31801210104
158	5	f	t	0.5	0	0.5	0	fp	guardrail	33501452019
159	5	t	t	0.179999999999999993	0	0.179999999999999993	0	fn	guardrail	33500481628
160	5	f	t	0.969999999999999973	0	0.969999999999999973	0	fp	guardrail	33501434012
161	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	33501402825
162	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	33501464919
163	5	t	t	1	0	1	0	tp	guardrail	42400220307
164	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	33500181408
165	5	t	t	0.0100000000000000002	0	0.0100000000000000002	0	fn	guardrail	30300400825
166	5	f	t	0.619999999999999996	0	0.619999999999999996	0	fp	guardrail	35900171209
167	5	t	t	0.0500000000000000028	0	0.0500000000000000028	0	fn	guardrail	35600501306
168	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	29800012904
169	5	t	t	0.57999999999999996	0	0.57999999999999996	0	tp	guardrail	42400183706
170	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32700281324
171	5	t	t	0.479999999999999982	0	0.479999999999999982	0	fn	guardrail	31801174924
172	5	f	t	0.630000000000000004	0	0.630000000000000004	0	fp	guardrail	31401495227
173	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	42400515327
174	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	32500283502
175	5	t	t	0.959999999999999964	0	0.959999999999999964	0	tp	guardrail	35600275009
176	5	f	t	0.469999999999999973	0	0.469999999999999973	0	tn	guardrail	31501391922
177	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	15800251221
178	5	f	t	0.729999999999999982	0	0.729999999999999982	0	fp	guardrail	42400135928
179	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	16501045000
180	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	30301141508
181	5	t	t	0.859999999999999987	0	0.859999999999999987	0	tp	guardrail	30800471224
182	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	16501060119
183	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	33700375929
184	5	f	t	0.910000000000000031	0	0.910000000000000031	0	fp	guardrail	31401474309
185	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	35600284809
186	5	f	t	0.429999999999999993	0	0.429999999999999993	0	tn	guardrail	30800051125
187	5	t	t	0.719999999999999973	0	0.719999999999999973	0	tp	guardrail	30600045513
188	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	33501365412
189	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	30800335719
190	5	f	t	0.739999999999999991	0	0.739999999999999991	0	fp	guardrail	31800150015
191	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	30800570802
192	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	16501580619
193	5	t	t	0.92000000000000004	0	0.92000000000000004	0	tp	guardrail	16500135607
194	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32700330528
195	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	32700385108
196	5	f	t	0.989999999999999991	0	0.989999999999999991	0	fp	guardrail	15801484909
197	5	t	t	0.0200000000000000004	0	0.0200000000000000004	0	fn	guardrail	33701302323
198	5	f	t	0.260000000000000009	0	0.260000000000000009	0	tn	guardrail	33901182607
199	5	t	t	0.790000000000000036	0	0.790000000000000036	0	tp	guardrail	34000045310
200	5	f	t	0.25	0	0.25	0	tn	guardrail	33700591706
201	5	t	t	0.28999999999999998	0	0.28999999999999998	0	fn	guardrail	33701165814
202	5	f	t	0.67000000000000004	0	0.67000000000000004	0	fp	guardrail	33700352823
203	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	42501082612
204	5	f	t	0.130000000000000004	0	0.130000000000000004	0	tn	guardrail	34001370803
205	5	t	t	0.5	0	0.5	0	tp	guardrail	34000104729
206	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	34000051510
207	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	34000191222
208	5	f	t	0.660000000000000031	0	0.660000000000000031	0	fp	guardrail	31001021901
209	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	31001261018
210	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	31001363418
211	5	t	t	0.619999999999999996	0	0.619999999999999996	0	tp	guardrail	31300315228
212	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301354704
213	5	t	t	0.23000000000000001	0	0.23000000000000001	0	fn	guardrail	32301204606
214	5	f	t	0.569999999999999951	0	0.569999999999999951	0	fp	guardrail	32300473808
215	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301485709
216	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32300323606
217	5	t	t	0.660000000000000031	0	0.660000000000000031	0	tp	guardrail	32301174026
218	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32301233503
219	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	32300431021
220	5	f	t	0.880000000000000004	0	0.880000000000000004	0	fp	guardrail	32301242313
221	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	32301163729
222	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	32301114108
223	5	t	t	0.709999999999999964	0	0.709999999999999964	0	tp	guardrail	32300491609
224	5	f	t	0	0	0	0	tn	guardrail	35201071529
225	5	t	t	0.220000000000000001	0	0.220000000000000001	0	fn	guardrail	30702000618
226	5	f	t	0.530000000000000027	0	0.530000000000000027	0	fp	guardrail	30700384125
227	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	30701245813
228	5	f	t	0.25	0	0.25	0	tn	guardrail	30700411425
229	5	t	t	0.709999999999999964	0	0.709999999999999964	0	tp	guardrail	34301151912
230	5	f	t	0.450000000000000011	0	0.450000000000000011	0	tn	guardrail	34300541317
231	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	34301065629
232	5	f	t	0.510000000000000009	0	0.510000000000000009	0	fp	guardrail	34301535911
233	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	34301145802
234	5	f	t	0.0899999999999999967	0	0.0899999999999999967	0	tn	guardrail	35200154201
235	5	t	t	0.859999999999999987	0	0.859999999999999987	0	tp	guardrail	42500252129
236	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	30700322607
237	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	32300032314
238	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	33600375407
239	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	33700365512
240	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	34000182102
241	5	t	t	0.650000000000000022	0	0.650000000000000022	0	tp	guardrail	32300263521
242	5	f	t	0.25	0	0.25	0	tn	guardrail	34301453523
243	5	t	t	0.0100000000000000002	0	0.0100000000000000002	0	fn	guardrail	34301374813
244	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	32301141114
245	5	t	t	0.479999999999999982	0	0.479999999999999982	0	fn	guardrail	42500034620
246	5	f	t	0.25	0	0.25	0	tn	guardrail	32300293221
247	5	t	t	0.930000000000000049	0	0.930000000000000049	0	tp	guardrail	34301095009
248	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	30700573221
249	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	34301451503
250	5	f	t	0.770000000000000018	0	0.770000000000000018	0	fp	guardrail	30701365814
251	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	31001305524
252	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32300171012
253	5	t	t	0.729999999999999982	0	0.729999999999999982	0	tp	guardrail	32301100319
254	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301231123
255	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	33700223417
256	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	32301503324
257	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	34301294525
258	5	f	t	0.0899999999999999967	0	0.0899999999999999967	0	tn	guardrail	34301424707
259	5	t	t	0.520000000000000018	0	0.520000000000000018	0	tp	guardrail	32301201706
260	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	34301182805
261	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	34301333500
262	5	f	t	0.569999999999999951	0	0.569999999999999951	0	fp	guardrail	35200250623
263	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	42501115001
264	5	f	t	0.25	0	0.25	0	tn	guardrail	33700545517
265	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	16300221524
266	5	f	t	0.260000000000000009	0	0.260000000000000009	0	tn	guardrail	22000431902
267	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	35801404307
268	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	35501541503
269	5	t	t	0.0299999999999999989	0	0.0299999999999999989	0	fn	guardrail	30000081915
270	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	35500575109
271	5	t	t	0.569999999999999951	0	0.569999999999999951	0	tp	guardrail	31101034815
272	5	f	t	0.170000000000000012	0	0.170000000000000012	0	tn	guardrail	22001512810
273	5	t	t	0.0299999999999999989	0	0.0299999999999999989	0	fn	guardrail	16100350429
274	5	f	t	0.599999999999999978	0	0.599999999999999978	0	fp	guardrail	30401244412
275	5	t	t	0.270000000000000018	0	0.270000000000000018	0	fn	guardrail	30600235410
276	5	f	t	0.450000000000000011	0	0.450000000000000011	0	tn	guardrail	35100530209
277	5	t	t	0.550000000000000044	0	0.550000000000000044	0	tp	guardrail	35501085529
278	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	30901523718
279	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	30301130918
280	5	f	t	0.969999999999999973	0	0.969999999999999973	0	fp	guardrail	30601400828
281	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	32700170921
282	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	35902013028
283	5	t	t	0.780000000000000027	0	0.780000000000000027	0	tp	guardrail	30600283129
284	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	34300021410
285	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	30801392614
286	5	f	t	1	0	1	0	fp	guardrail	29601072011
287	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	33600384827
288	5	f	t	0.130000000000000004	0	0.130000000000000004	0	tn	guardrail	31001364518
289	5	t	t	0.75	0	0.75	0	tp	guardrail	32300441828
290	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	34300400925
291	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	30600250212
292	5	f	t	0.640000000000000013	0	0.640000000000000013	0	fp	guardrail	33600004504
293	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	34301153803
294	5	f	t	0.209999999999999992	0	0.209999999999999992	0	tn	guardrail	34201362524
295	5	t	t	0.92000000000000004	0	0.92000000000000004	0	tp	guardrail	29601544005
296	5	f	t	0.239999999999999991	0	0.239999999999999991	0	tn	guardrail	29601084513
297	5	t	t	0.0299999999999999989	0	0.0299999999999999989	0	fn	guardrail	31000211513
298	5	f	t	0.650000000000000022	0	0.650000000000000022	0	fp	guardrail	33901500703
299	5	t	t	0.179999999999999993	0	0.179999999999999993	0	fn	guardrail	34401231412
300	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	42501474203
301	5	t	t	0.729999999999999982	0	0.729999999999999982	0	tp	guardrail	32301094308
302	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	32301093309
303	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	32301094709
304	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	32301093009
305	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301090728
306	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	32301095008
307	5	t	t	0.869999999999999996	0	0.869999999999999996	0	tp	guardrail	32301090619
308	5	f	t	0.0700000000000000067	0	0.0700000000000000067	0	tn	guardrail	32301092509
309	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301095708
310	5	f	t	0.859999999999999987	0	0.859999999999999987	0	fp	guardrail	32301090318
311	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	32301090028
312	5	f	t	0.429999999999999993	0	0.429999999999999993	0	tn	guardrail	32301090228
313	5	t	t	0.900000000000000022	0	0.900000000000000022	0	tp	guardrail	32301090329
314	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301090428
315	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	32301090518
316	5	f	t	0.640000000000000013	0	0.640000000000000013	0	fp	guardrail	32301090808
317	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301090829
318	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301090908
319	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301091218
320	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301091318
321	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301091418
322	5	f	t	0.589999999999999969	0	0.589999999999999969	0	fp	guardrail	32301091608
323	5	t	t	0.270000000000000018	0	0.270000000000000018	0	fn	guardrail	32301091618
324	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301091708
325	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301091729
326	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	32301091909
327	5	t	t	0.479999999999999982	0	0.479999999999999982	0	fn	guardrail	32301091918
328	5	f	t	0.520000000000000018	0	0.520000000000000018	0	fp	guardrail	32301092018
329	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301092109
330	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301092309
331	5	t	t	0.949999999999999956	0	0.949999999999999956	0	tp	guardrail	32301092318
332	5	f	t	0.299999999999999989	0	0.299999999999999989	0	tn	guardrail	32301092518
333	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301092528
334	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	32301092619
335	5	t	t	0.330000000000000016	0	0.330000000000000016	0	fn	guardrail	32301092718
336	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32301093229
337	5	t	t	0.770000000000000018	0	0.770000000000000018	0	tp	guardrail	32301093318
338	5	f	t	0.299999999999999989	0	0.299999999999999989	0	tn	guardrail	32301093518
339	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301094129
340	5	f	t	0.930000000000000049	0	0.930000000000000049	0	fp	guardrail	32301094508
341	5	t	t	0.46000000000000002	0	0.46000000000000002	0	fn	guardrail	32301094519
342	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301094609
343	5	t	t	0.770000000000000018	0	0.770000000000000018	0	tp	guardrail	32301094818
344	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301095608
345	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301095718
346	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	32301095728
347	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301094329
348	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32301093818
349	5	t	t	0.810000000000000053	0	0.810000000000000053	0	tp	guardrail	32301095029
350	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	32301092908
351	5	t	t	0.320000000000000007	0	0.320000000000000007	0	fn	guardrail	32301092929
352	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	32301094729
353	5	t	t	0.429999999999999993	0	0.429999999999999993	0	fn	guardrail	32301094718
354	5	f	t	0.419999999999999984	0	0.419999999999999984	0	tn	guardrail	32301090819
355	5	t	t	0.82999999999999996	0	0.82999999999999996	0	tp	guardrail	32301095918
356	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	32301094118
357	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301093708
358	5	f	t	0.849999999999999978	0	0.849999999999999978	0	fp	guardrail	32301092218
359	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301095219
360	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301095108
361	5	t	t	0.880000000000000004	0	0.880000000000000004	0	tp	guardrail	32301092828
362	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301092628
363	5	t	t	0.369999999999999996	0	0.369999999999999996	0	fn	guardrail	32301090629
364	5	f	t	0.910000000000000031	0	0.910000000000000031	0	fp	guardrail	32301092809
365	5	t	t	0.28999999999999998	0	0.28999999999999998	0	fn	guardrail	32301090008
366	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301090018
367	5	t	t	0.640000000000000013	0	0.640000000000000013	0	tp	guardrail	32301090409
368	5	f	t	0.309999999999999998	0	0.309999999999999998	0	tn	guardrail	32301090718
369	5	t	t	0.0899999999999999967	0	0.0899999999999999967	0	fn	guardrail	32301090919
370	5	f	t	0.550000000000000044	0	0.550000000000000044	0	fp	guardrail	32301090928
371	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	32301091008
372	5	f	t	0.220000000000000001	0	0.220000000000000001	0	tn	guardrail	32301091208
373	5	t	t	0.949999999999999956	0	0.949999999999999956	0	tp	guardrail	32301091308
374	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301091409
375	5	t	t	0.160000000000000003	0	0.160000000000000003	0	fn	guardrail	32301091509
376	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	32301091519
377	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301091718
378	5	f	t	0.469999999999999973	0	0.469999999999999973	0	tn	guardrail	32301091809
379	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301091928
380	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301092009
381	5	t	t	0.25	0	0.25	0	fn	guardrail	32301092028
382	5	f	t	0.540000000000000036	0	0.540000000000000036	0	fp	guardrail	32301092819
383	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301092919
384	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301093018
385	5	t	t	0.589999999999999969	0	0.589999999999999969	0	tp	guardrail	32301093108
386	5	f	t	0.429999999999999993	0	0.429999999999999993	0	tn	guardrail	32301093208
387	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301093219
388	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	32301093328
389	5	t	t	0	0	0	0	fn	guardrail	32301093409
390	5	f	t	0.0200000000000000004	0	0.0200000000000000004	0	tn	guardrail	32301093428
391	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	32301093929
392	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301094019
393	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301094109
394	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	32301094618
395	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	32301094629
396	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	32301094829
397	5	t	t	0.959999999999999964	0	0.959999999999999964	0	tp	guardrail	32301094909
398	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301094918
399	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301095118
400	5	f	t	0.530000000000000027	0	0.530000000000000027	0	fp	guardrail	32301095128
401	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301095208
402	5	f	t	0.390000000000000013	0	0.390000000000000013	0	tn	guardrail	32301095229
403	5	t	t	0.800000000000000044	0	0.800000000000000044	0	tp	guardrail	32301095409
404	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301095418
405	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	32301095429
406	5	f	t	0.680000000000000049	0	0.680000000000000049	0	fp	guardrail	32301095518
407	5	t	t	0.320000000000000007	0	0.320000000000000007	0	fn	guardrail	32301095529
408	5	f	t	0.100000000000000006	0	0.100000000000000006	0	tn	guardrail	32301095629
409	5	t	t	0.520000000000000018	0	0.520000000000000018	0	tp	guardrail	32301095809
410	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301095819
411	5	t	t	0.5	0	0.5	0	tp	guardrail	32301095928
412	5	f	t	0.699999999999999956	0	0.699999999999999956	0	fp	guardrail	32301094228
413	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301093628
414	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301094418
415	5	t	t	0.599999999999999978	0	0.599999999999999978	0	tp	guardrail	32301094318
416	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301094219
417	5	t	t	0.479999999999999982	0	0.479999999999999982	0	fn	guardrail	32301094808
418	5	f	t	0.739999999999999991	0	0.739999999999999991	0	fp	guardrail	32301093119
419	5	t	t	0.0500000000000000028	0	0.0500000000000000028	0	fn	guardrail	32301092729
420	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301094208
421	5	t	t	0.939999999999999947	0	0.939999999999999947	0	tp	guardrail	32301093618
422	5	f	t	0.340000000000000024	0	0.340000000000000024	0	tn	guardrail	32301091128
423	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	32301095508
424	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	32301090108
425	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	32301090118
426	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	32301090128
427	5	t	t	0.510000000000000009	0	0.510000000000000009	0	tp	guardrail	32301090208
428	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	32301090218
429	5	t	t	0	0	0	0	fn	guardrail	32301090418
430	5	f	t	0.680000000000000049	0	0.680000000000000049	0	fp	guardrail	32301090608
431	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301090708
432	5	f	t	0.270000000000000018	0	0.270000000000000018	0	tn	guardrail	32301091018
433	5	t	t	0.900000000000000022	0	0.900000000000000022	0	tp	guardrail	32301091029
434	5	f	t	0.100000000000000006	0	0.100000000000000006	0	tn	guardrail	32301091118
435	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	32301091228
436	5	f	t	0.680000000000000049	0	0.680000000000000049	0	fp	guardrail	32301091829
437	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	32301092128
438	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	32301092208
439	5	t	t	0.510000000000000009	0	0.510000000000000009	0	tp	guardrail	32301092408
440	5	f	t	0.209999999999999992	0	0.209999999999999992	0	tn	guardrail	32301092418
441	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301092428
442	5	f	t	0.739999999999999991	0	0.739999999999999991	0	fp	guardrail	32301092608
443	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301092709
444	5	f	t	0.25	0	0.25	0	tn	guardrail	32301093128
445	5	t	t	0.969999999999999973	0	0.969999999999999973	0	tp	guardrail	32301093508
446	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301093529
447	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301094028
448	5	f	t	0.959999999999999964	0	0.959999999999999964	0	fp	guardrail	32301095309
449	5	t	t	0.0500000000000000028	0	0.0500000000000000028	0	fn	guardrail	32301093829
450	5	f	t	0.0899999999999999967	0	0.0899999999999999967	0	tn	guardrail	32301093909
451	5	t	t	0.760000000000000009	0	0.760000000000000009	0	tp	guardrail	32301093729
452	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301094429
453	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	32301093608
454	5	f	t	0.660000000000000031	0	0.660000000000000031	0	fp	guardrail	32301084918
455	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301085418
456	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	32301084709
457	5	t	t	0.640000000000000013	0	0.640000000000000013	0	tp	guardrail	32301084429
458	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301084628
459	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301084808
460	5	f	t	0.609999999999999987	0	0.609999999999999987	0	fp	guardrail	32301084908
461	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	32301085208
462	5	f	t	0.0299999999999999989	0	0.0299999999999999989	0	tn	guardrail	32301085318
463	5	t	t	0.869999999999999996	0	0.869999999999999996	0	tp	guardrail	32301085329
464	5	f	t	0.340000000000000024	0	0.340000000000000024	0	tn	guardrail	32301085518
465	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301085609
466	5	f	t	0.609999999999999987	0	0.609999999999999987	0	fp	guardrail	32301085809
467	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301085228
468	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301085719
469	5	t	t	0.550000000000000044	0	0.550000000000000044	0	tp	guardrail	32301085018
470	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	32301084418
471	5	t	t	0.320000000000000007	0	0.320000000000000007	0	fn	guardrail	32301084508
472	5	f	t	0.520000000000000018	0	0.520000000000000018	0	fp	guardrail	32301084528
473	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301084619
474	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	32301084818
475	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301084929
476	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301085009
477	5	t	t	0.179999999999999993	0	0.179999999999999993	0	fn	guardrail	32301085028
478	5	f	t	0.910000000000000031	0	0.910000000000000031	0	fp	guardrail	32301085109
479	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301085128
480	5	f	t	0	0	0	0	tn	guardrail	32301085218
481	5	t	t	0.660000000000000031	0	0.660000000000000031	0	tp	guardrail	32301085308
482	5	f	t	0.5	0	0.5	0	fp	guardrail	32301085428
483	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	32301085618
484	5	f	t	0.949999999999999956	0	0.949999999999999956	0	fp	guardrail	32301085628
485	5	t	t	0.0899999999999999967	0	0.0899999999999999967	0	fn	guardrail	32301085709
486	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301085729
487	5	t	t	0.520000000000000018	0	0.520000000000000018	0	tp	guardrail	32301085828
488	5	f	t	0.270000000000000018	0	0.270000000000000018	0	tn	guardrail	32301085908
489	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301085918
490	5	f	t	0.560000000000000053	0	0.560000000000000053	0	fp	guardrail	32301085928
491	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	32301084608
492	5	f	t	0.479999999999999982	0	0.479999999999999982	0	tn	guardrail	32301085408
493	5	t	t	0.689999999999999947	0	0.689999999999999947	0	tp	guardrail	32301085528
494	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301102309
495	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301102408
496	5	f	t	0.790000000000000036	0	0.790000000000000036	0	fp	guardrail	32301100709
497	5	t	t	0.23000000000000001	0	0.23000000000000001	0	fn	guardrail	32301103008
498	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	32301100729
499	5	t	t	0.739999999999999991	0	0.739999999999999991	0	tp	guardrail	32301100829
500	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301100919
501	5	t	t	0.0500000000000000028	0	0.0500000000000000028	0	fn	guardrail	32301101019
502	5	f	t	0.530000000000000027	0	0.530000000000000027	0	fp	guardrail	32301101209
503	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301101329
504	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32301101618
505	5	t	t	0.869999999999999996	0	0.869999999999999996	0	tp	guardrail	32301102029
506	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	32301102919
507	5	t	t	0.0899999999999999967	0	0.0899999999999999967	0	fn	guardrail	32301103219
508	5	f	t	0.949999999999999956	0	0.949999999999999956	0	fp	guardrail	32301103318
509	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	32301104509
510	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301104518
511	5	t	t	0.959999999999999964	0	0.959999999999999964	0	tp	guardrail	32301105028
512	5	f	t	0.179999999999999993	0	0.179999999999999993	0	tn	guardrail	32301102519
513	5	t	t	0.0899999999999999967	0	0.0899999999999999967	0	fn	guardrail	32301102508
514	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	32301105308
515	5	t	t	0.479999999999999982	0	0.479999999999999982	0	fn	guardrail	32301105408
516	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301103529
517	5	t	t	0.739999999999999991	0	0.739999999999999991	0	tp	guardrail	32301100308
518	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301100518
519	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	32301105609
520	5	f	t	0.5	0	0.5	0	fp	guardrail	32301103919
521	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301100418
522	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301104318
523	5	t	t	0.739999999999999991	0	0.739999999999999991	0	tp	guardrail	32301102708
524	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301105819
525	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301102109
526	5	f	t	0.660000000000000031	0	0.660000000000000031	0	fp	guardrail	32301104918
527	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301100409
528	5	f	t	0.309999999999999998	0	0.309999999999999998	0	tn	guardrail	32301100208
529	5	t	t	0.680000000000000049	0	0.680000000000000049	0	tp	guardrail	32301100219
530	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32301100229
531	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301100328
532	5	f	t	0.770000000000000018	0	0.770000000000000018	0	fp	guardrail	32301100509
533	5	t	t	0.220000000000000001	0	0.220000000000000001	0	fn	guardrail	32301100528
534	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301100629
535	5	t	t	0.939999999999999947	0	0.939999999999999947	0	tp	guardrail	32301100719
536	5	f	t	0.270000000000000018	0	0.270000000000000018	0	tn	guardrail	32301101128
537	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301101229
538	5	f	t	0.67000000000000004	0	0.67000000000000004	0	fp	guardrail	32301101308
539	5	t	t	0.0400000000000000008	0	0.0400000000000000008	0	fn	guardrail	32301101408
540	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	32301101528
541	5	t	t	0.770000000000000018	0	0.770000000000000018	0	tp	guardrail	32301101728
542	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	32301101818
543	5	t	t	0.46000000000000002	0	0.46000000000000002	0	fn	guardrail	32301101829
544	5	f	t	0.709999999999999964	0	0.709999999999999964	0	fp	guardrail	32301102118
545	5	t	t	0.209999999999999992	0	0.209999999999999992	0	fn	guardrail	32301102208
546	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301102318
547	5	t	t	0.530000000000000027	0	0.530000000000000027	0	tp	guardrail	32301102329
548	5	f	t	0.239999999999999991	0	0.239999999999999991	0	tn	guardrail	32301102419
549	5	t	t	0.369999999999999996	0	0.369999999999999996	0	fn	guardrail	32301102608
550	5	f	t	0.57999999999999996	0	0.57999999999999996	0	fp	guardrail	32301102628
551	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	32301102809
552	5	f	t	0.309999999999999998	0	0.309999999999999998	0	tn	guardrail	32301102828
553	5	t	t	0.839999999999999969	0	0.839999999999999969	0	tp	guardrail	32301103108
554	5	f	t	0.179999999999999993	0	0.179999999999999993	0	tn	guardrail	32301103409
555	5	t	t	0.23000000000000001	0	0.23000000000000001	0	fn	guardrail	32301103418
556	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	32301103509
557	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301103518
558	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	32301104009
559	5	t	t	0.560000000000000053	0	0.560000000000000053	0	tp	guardrail	32301104018
560	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	32301104108
561	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	32301104129
562	5	f	t	0.67000000000000004	0	0.67000000000000004	0	fp	guardrail	32301104609
563	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	32301104728
564	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301104829
565	5	t	t	0.800000000000000044	0	0.800000000000000044	0	tp	guardrail	32301104908
566	5	f	t	0.170000000000000012	0	0.170000000000000012	0	tn	guardrail	32301104928
567	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301105008
568	5	f	t	0.810000000000000053	0	0.810000000000000053	0	fp	guardrail	32301105018
569	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301105108
570	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301105208
571	5	t	t	0.569999999999999951	0	0.569999999999999951	0	tp	guardrail	32301105229
572	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	32301105418
573	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	32301105428
574	5	f	t	0.57999999999999996	0	0.57999999999999996	0	fp	guardrail	32301105618
575	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	32301105628
576	5	f	t	0.0299999999999999989	0	0.0299999999999999989	0	tn	guardrail	32301105729
577	5	t	t	0.689999999999999947	0	0.689999999999999947	0	tp	guardrail	32301105908
578	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	32301100428
579	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	32301104809
580	5	f	t	0.630000000000000004	0	0.630000000000000004	0	fp	guardrail	32301103808
581	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301104208
582	5	f	t	0.100000000000000006	0	0.100000000000000006	0	tn	guardrail	32301104709
583	5	t	t	0.869999999999999996	0	0.869999999999999996	0	tp	guardrail	32301101319
584	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301102728
585	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301102818
586	5	f	t	0.550000000000000044	0	0.550000000000000044	0	fp	guardrail	32301101608
587	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301102219
588	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	32301103018
589	5	t	t	0.630000000000000004	0	0.630000000000000004	0	tp	guardrail	32301101108
590	5	f	t	0.0200000000000000004	0	0.0200000000000000004	0	tn	guardrail	32301100109
591	5	t	t	0.450000000000000011	0	0.450000000000000011	0	fn	guardrail	32301100118
592	5	f	t	0.910000000000000031	0	0.910000000000000031	0	fp	guardrail	32301100609
593	5	t	t	0.330000000000000016	0	0.330000000000000016	0	fn	guardrail	32301100619
594	5	f	t	0.469999999999999973	0	0.469999999999999973	0	tn	guardrail	32301100808
595	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	32301101008
596	5	f	t	0.419999999999999984	0	0.419999999999999984	0	tn	guardrail	32301101029
597	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301101119
598	5	f	t	0.550000000000000044	0	0.550000000000000044	0	fp	guardrail	32301101219
599	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	32301101429
600	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301101509
601	5	t	t	0.849999999999999978	0	0.849999999999999978	0	tp	guardrail	32301101519
602	5	f	t	0.0299999999999999989	0	0.0299999999999999989	0	tn	guardrail	32301101629
603	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301101708
604	5	f	t	0.839999999999999969	0	0.839999999999999969	0	fp	guardrail	32301101809
605	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301101928
606	5	f	t	0.0700000000000000067	0	0.0700000000000000067	0	tn	guardrail	32301102018
607	5	t	t	0.630000000000000004	0	0.630000000000000004	0	tp	guardrail	32301102128
608	5	f	t	0.469999999999999973	0	0.469999999999999973	0	tn	guardrail	32301102228
609	5	t	t	0.0500000000000000028	0	0.0500000000000000028	0	fn	guardrail	32301102528
610	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	32301102619
611	5	t	t	0.130000000000000004	0	0.130000000000000004	0	fn	guardrail	32301102718
612	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	32301103028
613	5	t	t	0.930000000000000049	0	0.930000000000000049	0	tp	guardrail	32301103119
614	5	f	t	0.390000000000000013	0	0.390000000000000013	0	tn	guardrail	32301103129
615	5	t	t	0.220000000000000001	0	0.220000000000000001	0	fn	guardrail	32301103208
616	5	f	t	0.599999999999999978	0	0.599999999999999978	0	fp	guardrail	32301103229
617	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	32301103308
618	5	f	t	0.179999999999999993	0	0.179999999999999993	0	tn	guardrail	32301103329
619	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	32301103618
620	5	f	t	0.390000000000000013	0	0.390000000000000013	0	tn	guardrail	32301103628
621	5	t	t	0.0100000000000000002	0	0.0100000000000000002	0	fn	guardrail	32301103819
622	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	32301103829
623	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301103909
624	5	f	t	0	0	0	0	tn	guardrail	32301103928
625	5	t	t	0.930000000000000049	0	0.930000000000000049	0	tp	guardrail	32301104028
626	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	32301104118
627	5	t	t	0.0100000000000000002	0	0.0100000000000000002	0	fn	guardrail	32301104219
628	5	f	t	0.969999999999999973	0	0.969999999999999973	0	fp	guardrail	32301104308
629	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	32301104328
630	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301104418
631	5	t	t	0.910000000000000031	0	0.910000000000000031	0	tp	guardrail	32301104529
632	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301104618
633	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301104818
634	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	32301105118
635	5	t	t	0.309999999999999998	0	0.309999999999999998	0	fn	guardrail	32301105219
636	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	32301105318
637	5	t	t	0.630000000000000004	0	0.630000000000000004	0	tp	guardrail	32301105329
638	5	f	t	0.419999999999999984	0	0.419999999999999984	0	tn	guardrail	32301105519
639	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	32301105708
640	5	f	t	0.959999999999999964	0	0.959999999999999964	0	fp	guardrail	32301105719
641	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301105809
642	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301105828
643	5	t	t	0.589999999999999969	0	0.589999999999999969	0	tp	guardrail	32301105918
644	5	f	t	0.220000000000000001	0	0.220000000000000001	0	tn	guardrail	32301105929
645	5	t	t	0.160000000000000003	0	0.160000000000000003	0	fn	guardrail	32301104429
646	5	f	t	0.530000000000000027	0	0.530000000000000027	0	fp	guardrail	32301104718
647	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301120228
648	5	f	t	0.340000000000000024	0	0.340000000000000024	0	tn	guardrail	32301120008
649	5	t	t	0.719999999999999973	0	0.719999999999999973	0	tp	guardrail	32301120409
650	5	f	t	0.479999999999999982	0	0.479999999999999982	0	tn	guardrail	32301120319
651	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301120918
652	5	f	t	0.719999999999999973	0	0.719999999999999973	0	fp	guardrail	32301120708
653	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	32301120018
654	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32301120028
655	5	t	t	0.57999999999999996	0	0.57999999999999996	0	tp	guardrail	32301120108
656	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301120119
657	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301120128
658	5	f	t	0.709999999999999964	0	0.709999999999999964	0	fp	guardrail	32301120218
659	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	32301120309
660	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301120328
661	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	32301120418
662	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301120428
663	5	t	t	0.0200000000000000004	0	0.0200000000000000004	0	fn	guardrail	32301120518
664	5	f	t	0.910000000000000031	0	0.910000000000000031	0	fp	guardrail	32301120528
665	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301120619
666	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	32301120718
667	5	t	t	0.609999999999999987	0	0.609999999999999987	0	tp	guardrail	32301120809
668	5	f	t	0.5	0	0.5	0	fp	guardrail	32301120818
669	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	32301120829
670	5	f	t	0.739999999999999991	0	0.739999999999999991	0	fp	guardrail	32301120928
671	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	32301121019
672	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301121028
673	5	t	t	0.819999999999999951	0	0.819999999999999951	0	tp	guardrail	32301121108
674	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301121118
675	5	t	t	0.28999999999999998	0	0.28999999999999998	0	fn	guardrail	32301121208
676	5	f	t	0.719999999999999973	0	0.719999999999999973	0	fp	guardrail	32301121218
677	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301121228
678	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301121308
679	5	t	t	0.82999999999999996	0	0.82999999999999996	0	tp	guardrail	32301120908
680	5	f	t	0.220000000000000001	0	0.220000000000000001	0	tn	guardrail	32301120608
681	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	32301120628
682	5	f	t	0.689999999999999947	0	0.689999999999999947	0	fp	guardrail	32301113428
683	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301114308
684	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32301114619
685	5	t	t	0.800000000000000044	0	0.800000000000000044	0	tp	guardrail	32301114328
686	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	32301113629
687	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301115209
688	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	32301112009
689	5	t	t	0.23000000000000001	0	0.23000000000000001	0	fn	guardrail	32301114208
690	5	f	t	0.0100000000000000002	0	0.0100000000000000002	0	tn	guardrail	32301110119
691	5	t	t	0.75	0	0.75	0	tp	guardrail	32301110129
692	5	f	t	0.299999999999999989	0	0.299999999999999989	0	tn	guardrail	32301110329
693	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301110529
694	5	f	t	0.869999999999999996	0	0.869999999999999996	0	fp	guardrail	32301110619
695	5	t	t	0.320000000000000007	0	0.320000000000000007	0	fn	guardrail	32301110709
696	5	f	t	0.220000000000000001	0	0.220000000000000001	0	tn	guardrail	32301110919
697	5	t	t	0.949999999999999956	0	0.949999999999999956	0	tp	guardrail	32301110929
698	5	f	t	0.409999999999999976	0	0.409999999999999976	0	tn	guardrail	32301111119
699	5	t	t	0.0800000000000000017	0	0.0800000000000000017	0	fn	guardrail	32301111129
700	5	f	t	0.699999999999999956	0	0.699999999999999956	0	fp	guardrail	32301111209
701	5	t	t	0.0299999999999999989	0	0.0299999999999999989	0	fn	guardrail	32301111228
702	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301111419
703	5	t	t	0.910000000000000031	0	0.910000000000000031	0	tp	guardrail	32301111619
704	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32301111629
705	5	t	t	0.160000000000000003	0	0.160000000000000003	0	fn	guardrail	32301111709
706	5	f	t	0.589999999999999969	0	0.589999999999999969	0	fp	guardrail	32301111719
707	5	t	t	0.140000000000000013	0	0.140000000000000013	0	fn	guardrail	32301111818
708	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301111828
709	5	t	t	0.5	0	0.5	0	tp	guardrail	32301111928
710	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301112219
711	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	32301112309
712	5	f	t	0.619999999999999996	0	0.619999999999999996	0	fp	guardrail	32301112319
713	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301112429
714	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301112609
715	5	t	t	0.930000000000000049	0	0.930000000000000049	0	tp	guardrail	32301112619
716	5	f	t	0.270000000000000018	0	0.270000000000000018	0	tn	guardrail	32301112709
717	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301112829
718	5	f	t	0.680000000000000049	0	0.680000000000000049	0	fp	guardrail	32301112909
719	5	t	t	0.340000000000000024	0	0.340000000000000024	0	fn	guardrail	32301113019
720	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301113218
721	5	t	t	0.810000000000000053	0	0.810000000000000053	0	tp	guardrail	32301113308
722	5	f	t	0.280000000000000027	0	0.280000000000000027	0	tn	guardrail	32301113418
723	5	t	t	0.23000000000000001	0	0.23000000000000001	0	fn	guardrail	32301113508
724	5	f	t	0.969999999999999973	0	0.969999999999999973	0	fp	guardrail	32301113609
725	5	t	t	0.170000000000000012	0	0.170000000000000012	0	fn	guardrail	32301113909
726	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301113929
727	5	t	t	0.979999999999999982	0	0.979999999999999982	0	tp	guardrail	32301114318
728	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301114429
729	5	t	t	0	0	0	0	fn	guardrail	32301114509
730	5	f	t	0.959999999999999964	0	0.959999999999999964	0	fp	guardrail	32301114609
731	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301114709
732	5	f	t	0.209999999999999992	0	0.209999999999999992	0	tn	guardrail	32301114819
733	5	t	t	0.650000000000000022	0	0.650000000000000022	0	tp	guardrail	32301115009
734	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301115018
735	5	t	t	0.0200000000000000004	0	0.0200000000000000004	0	fn	guardrail	32301115219
736	5	f	t	0.739999999999999991	0	0.739999999999999991	0	fp	guardrail	32301115318
737	5	t	t	0.209999999999999992	0	0.209999999999999992	0	fn	guardrail	32301115518
738	5	f	t	0.369999999999999996	0	0.369999999999999996	0	tn	guardrail	32301115529
739	5	t	t	0.969999999999999973	0	0.969999999999999973	0	tp	guardrail	32301115618
740	5	f	t	0.450000000000000011	0	0.450000000000000011	0	tn	guardrail	32301115628
741	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301115809
742	5	f	t	0.609999999999999987	0	0.609999999999999987	0	fp	guardrail	32301115818
743	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301115928
744	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301115729
745	5	t	t	0.599999999999999978	0	0.599999999999999978	0	tp	guardrail	32301114629
746	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32301112229
747	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301110228
748	5	f	t	0.930000000000000049	0	0.930000000000000049	0	fp	guardrail	32301112629
749	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301111518
750	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	32301110019
751	5	t	t	0.609999999999999987	0	0.609999999999999987	0	tp	guardrail	32301110109
752	5	f	t	0.170000000000000012	0	0.170000000000000012	0	tn	guardrail	32301110209
753	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	32301110219
754	5	f	t	0.880000000000000004	0	0.880000000000000004	0	fp	guardrail	32301110308
755	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301110318
756	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301110409
757	5	t	t	0.880000000000000004	0	0.880000000000000004	0	tp	guardrail	32301110419
758	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301110609
759	5	t	t	0.130000000000000004	0	0.130000000000000004	0	fn	guardrail	32301110629
760	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	32301110809
761	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	32301110829
762	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301110909
763	5	t	t	0.520000000000000018	0	0.520000000000000018	0	tp	guardrail	32301111019
764	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	32301111029
765	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301111318
766	5	f	t	0.930000000000000049	0	0.930000000000000049	0	fp	guardrail	32301111328
767	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301111428
768	5	f	t	0.209999999999999992	0	0.209999999999999992	0	tn	guardrail	32301111508
769	5	t	t	0.900000000000000022	0	0.900000000000000022	0	tp	guardrail	32301111529
770	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301111609
771	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	32301111918
772	5	f	t	0.810000000000000053	0	0.810000000000000053	0	fp	guardrail	32301112018
773	5	t	t	0.149999999999999994	0	0.149999999999999994	0	fn	guardrail	32301112129
774	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32301112329
775	5	t	t	0.729999999999999982	0	0.729999999999999982	0	tp	guardrail	32301112509
776	5	f	t	0.179999999999999993	0	0.179999999999999993	0	tn	guardrail	32301112519
777	5	t	t	0.0599999999999999978	0	0.0599999999999999978	0	fn	guardrail	32301112529
778	5	f	t	0.75	0	0.75	0	fp	guardrail	32301112719
779	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301112728
780	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	32301112808
781	5	t	t	0.67000000000000004	0	0.67000000000000004	0	tp	guardrail	32301112918
782	5	f	t	0.340000000000000024	0	0.340000000000000024	0	tn	guardrail	32301113108
783	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301113209
784	5	f	t	0.890000000000000013	0	0.890000000000000013	0	fp	guardrail	32301113408
785	5	t	t	0.179999999999999993	0	0.179999999999999993	0	fn	guardrail	32301113518
786	5	f	t	0.100000000000000006	0	0.100000000000000006	0	tn	guardrail	32301113529
787	5	t	t	0.550000000000000044	0	0.550000000000000044	0	tp	guardrail	32301113719
788	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32301113729
789	5	t	t	0.130000000000000004	0	0.130000000000000004	0	fn	guardrail	32301113809
790	5	f	t	0.660000000000000031	0	0.660000000000000031	0	fp	guardrail	32301113819
791	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301114008
792	5	f	t	0.160000000000000003	0	0.160000000000000003	0	tn	guardrail	32301114028
793	5	t	t	0.589999999999999969	0	0.589999999999999969	0	tp	guardrail	32301114228
794	5	f	t	0.349999999999999978	0	0.349999999999999978	0	tn	guardrail	32301114418
795	5	t	t	0.429999999999999993	0	0.429999999999999993	0	fn	guardrail	32301114519
796	5	f	t	0.630000000000000004	0	0.630000000000000004	0	fp	guardrail	32301114529
797	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	32301114719
798	5	f	t	0.170000000000000012	0	0.170000000000000012	0	tn	guardrail	32301114809
799	5	t	t	0.67000000000000004	0	0.67000000000000004	0	tp	guardrail	32301114829
800	5	f	t	0.149999999999999994	0	0.149999999999999994	0	tn	guardrail	32301114908
801	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301115028
802	5	f	t	0.619999999999999996	0	0.619999999999999996	0	fp	guardrail	32301115118
803	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301115229
804	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301115309
805	5	t	t	0.619999999999999996	0	0.619999999999999996	0	tp	guardrail	32301115419
806	5	f	t	0.25	0	0.25	0	tn	guardrail	32301115509
807	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301115709
808	5	f	t	0.930000000000000049	0	0.930000000000000049	0	fp	guardrail	32301115719
809	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301115828
810	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301112209
811	5	t	t	0.839999999999999969	0	0.839999999999999969	0	tp	guardrail	32301113328
812	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301110009
813	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301110029
814	5	f	t	0.75	0	0.75	0	fp	guardrail	32301110719
815	5	t	t	0.25	0	0.25	0	fn	guardrail	32301111009
816	5	f	t	0.119999999999999996	0	0.119999999999999996	0	tn	guardrail	32301111218
817	5	t	t	0.680000000000000049	0	0.680000000000000049	0	tp	guardrail	32301111729
818	5	f	t	0.359999999999999987	0	0.359999999999999987	0	tn	guardrail	32301112119
819	5	t	t	0.5	0	0.5	0	tp	guardrail	32301113008
820	5	f	t	0.560000000000000053	0	0.560000000000000053	0	fp	guardrail	32301113029
821	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301113129
822	5	f	t	0.440000000000000002	0	0.440000000000000002	0	tn	guardrail	32301113619
823	5	t	t	0.57999999999999996	0	0.57999999999999996	0	tp	guardrail	32301113829
824	5	f	t	0.28999999999999998	0	0.28999999999999998	0	tn	guardrail	32301114118
825	5	t	t	0.0700000000000000067	0	0.0700000000000000067	0	fn	guardrail	32301114408
826	5	f	t	0.849999999999999978	0	0.849999999999999978	0	fp	guardrail	32301114928
827	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301115128
828	5	f	t	0.489999999999999991	0	0.489999999999999991	0	tn	guardrail	32301115328
829	5	t	t	0.92000000000000004	0	0.92000000000000004	0	tp	guardrail	32301115609
830	5	f	t	0.0899999999999999967	0	0.0899999999999999967	0	tn	guardrail	32301115918
831	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301091818
832	5	f	t	0.719999999999999973	0	0.719999999999999973	0	fp	guardrail	32301091109
833	5	t	t	0.400000000000000022	0	0.400000000000000022	0	fn	guardrail	32301092328
834	5	f	t	0.140000000000000013	0	0.140000000000000013	0	tn	guardrail	32301093419
835	5	t	t	0.739999999999999991	0	0.739999999999999991	0	tp	guardrail	32301095828
836	5	f	t	0.0800000000000000017	0	0.0800000000000000017	0	tn	guardrail	32301093718
837	5	t	t	0.270000000000000018	0	0.270000000000000018	0	fn	guardrail	32301093809
838	5	f	t	0.540000000000000036	0	0.540000000000000036	0	fp	guardrail	32301095019
839	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301094409
840	5	f	t	0.309999999999999998	0	0.309999999999999998	0	tn	guardrail	32301085118
841	5	t	t	0.719999999999999973	0	0.719999999999999973	0	tp	guardrail	32301084718
842	5	f	t	0.299999999999999989	0	0.299999999999999989	0	tn	guardrail	32301084728
843	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	32301100929
844	5	f	t	0.979999999999999982	0	0.979999999999999982	0	fp	guardrail	32301101908
845	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	32301102429
846	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32301103428
847	5	t	t	0.599999999999999978	0	0.599999999999999978	0	tp	guardrail	32301103608
848	5	f	t	0.450000000000000011	0	0.450000000000000011	0	tn	guardrail	32301103709
849	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	32301104628
850	5	f	t	0.760000000000000009	0	0.760000000000000009	0	fp	guardrail	32301105529
851	5	t	t	0.110000000000000001	0	0.110000000000000001	0	fn	guardrail	32301120508
852	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	32301121009
853	5	t	t	0.790000000000000036	0	0.790000000000000036	0	tp	guardrail	32301110519
854	5	f	t	0.469999999999999973	0	0.469999999999999973	0	tn	guardrail	32301111808
855	5	t	t	0.299999999999999989	0	0.299999999999999989	0	fn	guardrail	32301111909
856	5	f	t	0.599999999999999978	0	0.599999999999999978	0	fp	guardrail	32301112108
857	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301112419
858	5	f	t	0.309999999999999998	0	0.309999999999999998	0	tn	guardrail	32301112818
859	5	t	t	0.599999999999999978	0	0.599999999999999978	0	tp	guardrail	32301113318
860	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301115428
861	5	t	t	0.489999999999999991	0	0.489999999999999991	0	fn	guardrail	32301100019
862	5	f	t	0.880000000000000004	0	0.880000000000000004	0	fp	guardrail	32301095318
863	5	t	t	0.239999999999999991	0	0.239999999999999991	0	fn	guardrail	32301110819
864	5	f	t	0.0599999999999999978	0	0.0599999999999999978	0	tn	guardrail	32301113709
865	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301114729
866	5	f	t	0.400000000000000022	0	0.400000000000000022	0	tn	guardrail	32301100029
867	5	t	t	0.190000000000000002	0	0.190000000000000002	0	fn	guardrail	32301100009
868	5	f	t	0.800000000000000044	0	0.800000000000000044	0	fp	guardrail	32301091429
869	5	t	t	0.330000000000000016	0	0.330000000000000016	0	fn	guardrail	32301091628
870	5	f	t	0.130000000000000004	0	0.130000000000000004	0	tn	guardrail	32301114018
871	5	t	t	0.57999999999999996	0	0.57999999999999996	0	tp	guardrail	32301101418
872	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301095618
873	5	t	t	0.349999999999999978	0	0.349999999999999978	0	fn	guardrail	32301115409
874	5	f	t	0.609999999999999987	0	0.609999999999999987	0	fp	guardrail	32301110729
875	5	t	t	0.5	0	0.5	0	tp	guardrail	32301103728
876	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301084519
877	5	t	t	0.930000000000000049	0	0.930000000000000049	0	tp	guardrail	32301084828
878	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301085508
879	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	32301085818
880	5	f	t	0.709999999999999964	0	0.709999999999999964	0	fp	guardrail	32301090309
881	5	t	t	0.200000000000000011	0	0.200000000000000011	0	fn	guardrail	32301090508
882	5	f	t	0.320000000000000007	0	0.320000000000000007	0	tn	guardrail	32301090529
883	5	t	t	0.989999999999999991	0	0.989999999999999991	0	tp	guardrail	32301091328
884	5	f	t	0.130000000000000004	0	0.130000000000000004	0	tn	guardrail	32301091528
885	5	t	t	0.260000000000000009	0	0.260000000000000009	0	fn	guardrail	32301092119
886	5	f	t	0.92000000000000004	0	0.92000000000000004	0	fp	guardrail	32301092229
887	5	t	t	0.100000000000000006	0	0.100000000000000006	0	fn	guardrail	32301093028
888	5	f	t	0.0500000000000000028	0	0.0500000000000000028	0	tn	guardrail	32301093918
889	5	t	t	0.609999999999999987	0	0.609999999999999987	0	tp	guardrail	32301094009
890	5	f	t	0.0400000000000000008	0	0.0400000000000000008	0	tn	guardrail	32301094529
891	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	32301095328
892	5	f	t	0.630000000000000004	0	0.630000000000000004	0	fp	guardrail	32301095908
893	5	t	t	0.409999999999999976	0	0.409999999999999976	0	fn	guardrail	32301094929
894	5	f	t	0.270000000000000018	0	0.270000000000000018	0	tn	guardrail	32301100128
895	5	t	t	0.589999999999999969	0	0.589999999999999969	0	tp	guardrail	32301100818
896	5	f	t	0.380000000000000004	0	0.380000000000000004	0	tn	guardrail	32301100908
897	5	t	t	0.469999999999999973	0	0.469999999999999973	0	fn	guardrail	32301101718
898	5	f	t	0.880000000000000004	0	0.880000000000000004	0	fp	guardrail	32301101919
899	5	t	t	0.419999999999999984	0	0.419999999999999984	0	fn	guardrail	32301102009
900	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301102908
901	5	t	t	0.810000000000000053	0	0.810000000000000053	0	tp	guardrail	32301102929
902	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301103718
903	5	t	t	0.380000000000000004	0	0.380000000000000004	0	fn	guardrail	32301104229
904	5	f	t	0.520000000000000018	0	0.520000000000000018	0	fp	guardrail	32301104409
905	5	t	t	0.280000000000000027	0	0.280000000000000027	0	fn	guardrail	32301105128
906	5	f	t	0.190000000000000002	0	0.190000000000000002	0	tn	guardrail	32301105508
907	5	t	t	0.67000000000000004	0	0.67000000000000004	0	tp	guardrail	32301110429
908	5	f	t	0.46000000000000002	0	0.46000000000000002	0	tn	guardrail	32301110509
909	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301111109
910	5	f	t	0.510000000000000009	0	0.510000000000000009	0	fp	guardrail	32301111308
911	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301111409
912	5	f	t	0.330000000000000016	0	0.330000000000000016	0	tn	guardrail	32301112028
913	5	t	t	0.969999999999999973	0	0.969999999999999973	0	tp	guardrail	32301112409
914	5	f	t	0.23000000000000001	0	0.23000000000000001	0	tn	guardrail	32301112928
915	5	t	t	0.440000000000000002	0	0.440000000000000002	0	fn	guardrail	32301113118
916	5	f	t	0.780000000000000027	0	0.780000000000000027	0	fp	guardrail	32301113228
917	5	t	t	0.359999999999999987	0	0.359999999999999987	0	fn	guardrail	32301113919
918	5	f	t	0.200000000000000011	0	0.200000000000000011	0	tn	guardrail	32301114128
919	5	t	t	0.57999999999999996	0	0.57999999999999996	0	tp	guardrail	32301114218
920	5	f	t	0.110000000000000001	0	0.110000000000000001	0	tn	guardrail	32301114918
921	5	t	t	0.119999999999999996	0	0.119999999999999996	0	fn	guardrail	32301115109
922	5	f	t	0.569999999999999951	0	0.569999999999999951	0	fp	guardrail	32301115909
923	5	t	t	0.390000000000000013	0	0.390000000000000013	0	fn	guardrail	32301120209
924	5	f	t	0.100000000000000006	0	0.100000000000000006	0	tn	guardrail	32301120728
925	5	t	t	0.780000000000000027	0	0.780000000000000027	0	tp	guardrail	32301121128
\.


--
-- Data for Name: rs_core_routeimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_routeimage (route_id, image_base_name, location, mile_post, image_path, aspect_ratio, route_index) FROM stdin;
40001651098	16300504528	0101000020E61000007C1BAC49818053C0CE3FB09932D24140	0.0970000028610228937	d04/163/50	1.25	1
40002958051	34401091323	0101000020E61000006DE34F5436A053C049D9226937C64140	0.194000005722046009	d04/344/69	1.25	1
40001100042	29901194629	0101000020E610000084CB74F9A06653C0FA19283ADC134240	2.8680000305175799	d04/299/79	1.95999999999999996	1
40002339051	35501425510	0101000020E6100000D6A0794A988A53C0F894528660C84140	0.80299997329711903	d04/355/102	1.25	1
40001524064	30000272325	0101000020E61000005BCEA5B82A7653C0AEF5A0FBCD044240	5.48400020599364968	d04/300/27	1.95999999999999996	1
40002543051	33400080617	0101000020E610000025B78196899153C0719EFBBCF3B84140	0.0890000015497208058	d04/334/8	1.95999999999999996	1
40001415033	29701261012	0101000020E6100000709DDA74DF6C53C0E053EF5F0F064240	0.0930000022053718983	d04/297/86	1.95999999999999996	1
40001009051	34400303125	0101000020E610000096DC723FF19453C024319CC651B14140	6.68800020217896041	d04/344/30	1.25	2
40002217051	34400595700	0101000020E61000001349F4328A9E53C0C6AEA3607CC24140	0.56999999284744296	d04/344/59	1.25	2
40001009051	34400370205	0101000020E61000005864856CEA9153C00CF038A000A94140	12.5380001068115003	d04/344/37	1.25	3
40001628098	16401215429	0101000020E61000007FBA26497C7853C0C592CDB0ACCE4140	3.66000008583068981	d04/164/81	1.25	1
40002217051	34400592320	0101000020E61000005B971AA19F9E53C06B35DA6097C14140	0.0700000002980231961	d04/344/59	1.25	1
40001937096	16100345009	0101000020E61000006759411D208153C0B159E48D82984140	0.00899999961256981069	d04/161/34	1.25	1
40001720051	35501070209	0101000020E6100000CE273CB2839353C0CE95F727A7D34140	9.13399982452392933	d04/355/67	1.25	2
40002757051	34400394006	0101000020E610000084AFF90244A053C0F0B1AA14F1BD4140	0.0570000000298023016	d04/344/39	1.25	1
40001720051	35501095409	0101000020E6100000E1DFB1E9529253C0BDF9B2599ACF4140	11.7119998931884997	d04/355/69	1.25	5
40001935096	35401573022	0101000020E610000024B31FCEE88053C00E164ED2FC9B4140	0.301999986171722024	d04/354/117	1.95999999999999996	1
40002744051	34400403205	0101000020E610000045EFF906CBA053C0D606825BD2BD4140	0.0419999994337559024	d04/344/40	1.25	1
40001100042	29901341804	0101000020E6100000C1406BD9355C53C079DAD08371094240	15.0989999771118004	d04/299/94	1.95999999999999996	3
40001945051	35501154425	0101000020E6100000C2AEDCC1BE9153C05F5E807D74D24140	0.544000029563904031	d04/355/75	1.25	1
40001121096	34201040410	0101000020E6100000BF5C305DAD8A53C0BD34EAC660A14140	1.87999999523162997	d04/342/64	1.25	1
40001100042	29901322813	0101000020E6100000850F8013E55D53C00BA07312A5084240	13.5600004196166992	d04/299/92	1.95999999999999996	2
40002310051	33401471905	0101000020E6100000199AA1A7B78F53C0BAFEB858ACBD4140	3.7520000934600799	d04/334/107	1.95999999999999996	1
40001602098	16301184725	0101000020E61000006FE70CD6497753C0FDAD539BEED24140	4.84499979019165039	d04/163/78	1.25	1
40001218096	34201521024	0101000020E6100000C4B0C398F48653C02C4C3A257BA84140	1.16999995708465998	d04/342/112	1.25	1
40001106096	34201070010	0101000020E6100000DC7AF255178D53C0E0BA624678A24140	1.65199995040893999	d04/342/67	1.25	1
40001238042	29901113229	0101000020E61000006F62ED94B36C53C00A302C7FBE144240	0.100000001490115994	d04/299/71	1.95999999999999996	1
40001404033	30001011809	0101000020E610000053978C63A46D53C0D9BB9A971E044240	2.59699988365172985	d04/300/61	1.95999999999999996	1
40001544096	35701451127	0101000020E610000031D52714FD7C53C0AE6DE580B8BD4140	0.542999982833861972	d04/357/105	1.25	1
40002756051	34400391623	0101000020E6100000C96B6F0132A053C045CA60D6D5BD4140	0.105999998748302002	d04/344/39	1.25	1
40001507098	16302025413	0101000020E61000004DD47723187253C0F25190E91AD64140	5.01000022888184038	d04/163/122	1.25	1
40001428098	34901293001	0101000020E6100000A851ED78387553C08F72309B00E04140	2.18000006675719993	d04/349/89	1.95999999999999996	1
40001346033	29701443127	0101000020E6100000A275F97B4E6453C0ED8CA5FE30F54140	1.70200002193450994	d04/297/104	1.95999999999999996	1
40001230051	34400230020	0101000020E6100000042159C0049853C0A6D24F38BBB84140	0.126000002026558006	d04/344/23	1.25	1
40001505033	29901432208	0101000020E61000000D349F73375D53C00142356FE6014240	0.310000002384186013	d04/299/103	1.95999999999999996	1
40001637098	16301022617	0101000020E6100000BA3DF7D4A07E53C003C70A2362CB4140	1.29299998283386008	d04/163/62	1.25	1
40001518064	29901051509	0101000020E6100000369A12FF666F53C05FCBD01D69134240	3.91300010681151988	d04/299/65	1.95999999999999996	1
40002136051	35501325128	0101000020E610000060066344228E53C0F97DA42D53C84140	1.01400005817412997	d04/355/92	1.25	1
40001521042	29700553621	0101000020E6100000AB4EBD24047553C0405FC4888E3E4240	0.162000000476836992	d04/297/55	1.95999999999999996	2
40001145098	16300222214	0101000020E6100000548EC9E2FE8653C0540D0C6A09DC4140	1.19700002670287997	d04/163/22	1.25	2
40001306064	31200424207	0101000020E6100000626C7C81348453C029F922EBBAF94140	4.09899997711181996	d04/312/42	1.95999999999999996	1
40001637098	16301023018	0101000020E61000007862D68BA17E53C000868A1645CB4140	1.35300004482268998	d04/163/62	1.25	2
40001002051	33301120926	0101000020E6100000A67C08AAC68953C0F547BD4CB9BC4140	2.3610000610351598	d04/333/72	1.95999999999999996	1
40001932096	16101050612	0101000020E61000002007CA12427E53C01C846F50B1A64140	0.642000019550323042	d04/161/65	1.25	1
40001937096	16100362400	0101000020E61000003CE180F1678153C049032E7E099B4140	1.41400003433228005	d04/161/36	1.25	3
40001162051	34400070221	0101000020E61000006DB4D25A079D53C04DFF48C78BBC4140	3.38700008392333984	d04/344/7	1.25	2
40001537033	29701532424	0101000020E61000005188DBFC9A6053C02A183A1B97F64140	2.30399990081787021	d04/297/113	1.95999999999999996	1
40001506098	16400161125	0101000020E6100000A516A5DF197353C0BD5065BDBDDC4140	1.85599994659424006	d04/164/16	1.25	1
40001613098	16401575226	0101000020E61000006D74CE4F717B53C02769FE98D6CB4140	7.20599985122681019	d04/164/117	1.25	1
40001361051	35801340023	0101000020E6100000D6EC37C945A353C0075B913DE7B74140	1.17299997806549006	d04/358/94	1.95999999999999996	1
40001537098	16301245502	0101000020E610000013F9E417947053C0CB3D6E090ACF4140	2.6340000629425	d04/163/84	1.25	1
40001253033	30200201401	0101000020E6100000BEA59C2F766553C0B1602C1DBDFB4140	2.73200011253356978	d04/302/20	1.95999999999999996	1
40001303051	35801471221	0101000020E6100000CC913AA693A653C077442A3174BC4140	7.14400005340575994	d04/358/107	1.95999999999999996	2
40001009051	34400300325	0101000020E6100000CF85915E549553C05B649698C2B14140	6.26800012588500977	d04/344/30	1.25	1
40001607064	30000385923	0101000020E6100000C78CA669067853C06D5DC53DF1014240	1.32099997997284002	d04/300/38	1.95999999999999996	1
40001141033	30200062407	0101000020E6100000CCCFB293667153C0B15E56725FF14140	2.39299988746643022	d04/302/6	1.95999999999999996	1
40001231096	35700310103	0101000020E6100000AB7823F3C88753C050A50B5641B74140	0.796999990940093994	d04/357/31	1.25	1
40001693064	30001205208	0101000020E610000026CE401B6F7353C0F9707FE48C034240	0.245000004768371998	d04/300/80	1.95999999999999996	1
40002372051	35700034310	0101000020E6100000A2D68FA8AB8A53C0E66E21D96DB94140	3.14100003242492987	d04/357/3	1.25	1
40002372051	35700040920	0101000020E61000007FEC3F7CAA8A53C057201F99B3B84140	3.53600001335143999	d04/357/4	1.25	2
40001543096	35701420526	0101000020E6100000883C9347017C53C0F1D6F9B7CBBE4140	2.28699994087219016	d04/357/102	1.25	1
40001408033	29701315222	0101000020E6100000222F10A90E6A53C0E74306A85FFE4140	0.215000003576278992	d04/297/91	1.95999999999999996	1
40001143051	32400265718	0101000020E61000001E7C725EAD9C53C0E6F4ABEFB2AF4140	3.84500002861022994	d04/324/26	1.25	2
40001434042	30400214412	0101000020E610000091DC50E7C06E53C0521F926B54364240	2.21099996566772017	d04/304/21	1.95999999999999996	1
40001324064	30900553212	0101000020E61000003A8B83F08D8553C0C4831C4AA3084240	2.3889999389648402	d04/309/55	1.95999999999999996	1
40001007051	35101051713	0101000020E6100000EB6E9EEA909553C0D55526A199BC4140	2.04600000381469993	d04/351/65	1.25	1
40002129051	15901091226	0101000020E61000001667B1B98F8E53C0642AB3F798CB4140	2.68199992179871005	d04/159/69	1.25	1
40001001042	30502041402	0101000020E6100000993567333D6B53C040790E1B1B194240	25.5540008544922017	d04/305/124	1.95999999999999996	2
40001172096	34100282611	0101000020E61000009D63E53C088353C07F0E982C93A14140	0.202000007033348	d04/341/28	1.25	1
40001412042	30500483409	0101000020E61000001B75BEE9277553C058B89B960E394240	0.542999982833861972	d04/305/48	1.95999999999999996	1
40001600042	30500211224	0101000020E61000007D9AEED00B6C53C0E3D6EE682D2D4240	5.84999990463257014	d04/305/21	1.95999999999999996	1
40001106033	31900261724	0101000020E6100000D5CA845FEA6B53C0A3586E6935DC4140	0.448000013828277976	d04/319/26	1.95999999999999996	1
40001723051	33800504204	0101000020E61000006C49A2F28A9353C09D11A5BDC1E44140	3.40100002288818004	d04/338/50	1.95999999999999996	1
40001143051	32400230908	0101000020E610000012DDB3AE51A053C00541367F02AF4140	0.423000007867812999	d04/324/23	1.25	1
40001406042	30401232201	0101000020E61000004B9D3699A77853C0A93A9AD99D3D4240	1.38399994373321999	d04/304/83	1.95999999999999996	1
40003349051	35100165617	0101000020E61000008048BF7D1D9E53C04C35B39602C64140	0.47900000214576699	d04/351/16	1.25	1
40001492042	30400480726	0101000020E61000007F4FAC53E57653C0DBA4A2B1F63F4240	0.365999996662140004	d04/304/48	1.95999999999999996	1
40001506051	35100180614	0101000020E6100000D15CA791969E53C0E0354305E2C54140	0.398000001907349021	d04/351/18	1.25	1
40001141096	34100321517	0101000020E6100000F1E5F4AB6F8553C081C6962F799A4140	0.15199999511241899	d04/341/32	1.25	1
40001143051	32400325018	0101000020E6100000863AAC70CB9653C0B8A2DE9DC6AE4140	9.13500022888183949	d04/324/32	1.25	5
40001103098	22000175809	0101000020E61000004942C7B3F08353C0BB25DEA6E4D34140	2.41199994087219016	d04/220/17	1.25	1
40001143051	32400355028	0101000020E610000093814DE7D49353C0E399869796AE4140	11.8380002975463992	d04/324/35	1.25	6
40002169051	33000215519	0101000020E610000028F62BF8C88C53C06BD8EF8975D94140	0	d04/330/21	1.95999999999999996	1
40001143051	32400313308	0101000020E61000000C5BB395179853C0F9E6EDBE19AF4140	7.97599983215332031	d04/324/31	1.25	4
40002108051	33000081420	0101000020E6100000E1B4E045DF8E53C09B4D918D51DA4140	1.01400005817412997	d04/330/8	1.95999999999999996	1
40002106051	15901333701	0101000020E6100000CB51DBE18A8F53C03BB9F0CD80DC4140	1.41100001335143999	d04/159/93	1.25	2
40001368098	34801052114	0101000020E610000088916F00477753C0819EBC7E77E64140	1.33599996566771995	d04/348/65	1.95999999999999996	1
40001001064	22001132920	0101000020E6100000052857C2A48053C0D80638CEB7EE4140	4.9970002174377397	d04/220/73	1.25	1
40001960064	22000433201	0101000020E61000001C7E9296A58353C022AC21CC48E54140	2.2950000762939502	d04/220/43	1.25	2
40002112051	33000085111	0101000020E610000025B1A4DCFD8E53C0665133FF43D94140	0.0120000001043081006	d04/330/8	1.95999999999999996	1
40002143051	15901110815	0101000020E6100000948CF73EB08A53C00CE313573ACC4140	1.23599994182587003	d04/159/71	1.25	1
40002050096	36002001114	0101000020E61000004A68812C7A7B53C0E5362BECB3A24140	1.10599994659424006	d04/360/120	1.25	1
40001528064	30901224514	0101000020E6100000892E03298C7553C0F599588572074240	1.12600004673003995	d04/309/82	1.95999999999999996	1
40001820042	30100424824	0101000020E6100000D798219F215753C042F1BE85D0074240	1.32200002670287997	d04/301/42	1.95999999999999996	1
40001007051	35101145524	0101000020E61000003A1C02ECC88D53C0492BBEA1F0B34140	10.7150001525878995	d04/351/74	1.25	2
40001590042	30401205318	0101000020E61000008BF3812EAB7953C0EFAD484C503F4240	0.0320000015199184001	d04/304/80	1.95999999999999996	1
40001415042	30500414711	0101000020E610000099D36531317753C07144AD1F51344240	5.62400007247924982	d04/305/41	1.95999999999999996	1
40001945064	31901543714	0101000020E6100000A1134207DD8353C0A05A33E83AED4140	8.87199974060058949	d04/319/114	1.95999999999999996	2
40001913096	34100205218	0101000020E61000003B14AA40527A53C0CE8B135FEDA04140	0.0790000036358833035	d04/341/20	1.25	1
40001001042	30501412415	0101000020E61000000355EDE49D7553C0D6427F57BA304240	6.32600021362305043	d04/305/101	1.95999999999999996	1
40001913096	34100221828	0101000020E6100000D44A7C493E7B53C06FFDAA121B9F4140	1.3730000257492101	d04/341/22	1.25	2
40002110051	15901225329	0101000020E6100000818010244A8B53C0656C8DAD0CD14140	2.98699998855590998	d04/159/82	1.25	1
40001452098	34800560920	0101000020E6100000DD465E31FE7553C0A3ACDF4C4CE04140	0.209999993443488991	d04/348/56	1.95999999999999996	1
40001402098	34801083120	0101000020E6100000B5D892FA577553C0A4B61ECF78EB4140	0.171000003814696988	d04/348/68	1.95999999999999996	1
40002106051	15901324811	0101000020E6100000B3486EA8F38F53C0BF45274BADDD4140	0.681999981403351052	d04/159/92	1.25	1
40001109033	31900403905	0101000020E6100000A6F7E868B06C53C0B788DE9854E74140	7.09499979019165039	d04/319/40	1.95999999999999996	1
40002232096	36001265813	0101000020E6100000181B04673A7653C0C1E09A3BFAAC4140	0.499000012874602994	d04/360/86	1.25	1
40001328098	31901122921	0101000020E610000040D422475F7853C0322889DB57DF4140	0.634999990463256947	d04/319/72	1.95999999999999996	1
40001621042	29601521527	0101000020E61000004E870442216753C0D042A78C24314240	1.63100004196166992	d04/296/112	1.95999999999999996	1
40001717096	32500195615	0101000020E610000088C90A340E7553C08D02E9071AAE4140	1.66400003433228005	d04/325/19	1.25	2
40001755042	29601422623	0101000020E61000000C4D2377226853C0087767EDB6294240	1.50499999523162997	d04/296/102	1.95999999999999996	1
40002229096	32501014522	0101000020E610000042171E45E77653C05E0C8A8B48A64140	0.0599999986588954995	d04/325/61	1.25	1
40001143051	32400271918	0101000020E610000012E04FE8509C53C02C103D2993AF4140	4.17500019073485973	d04/324/27	1.25	3
40001113096	34101115407	0101000020E6100000CC03FD2AE58953C013EDCFEA899B4140	2.54800009727477983	d04/341/71	1.25	1
40001542042	30401182916	0101000020E6100000662A696A7E7953C09603E21A44404240	0.656000018119812012	d04/304/78	1.95999999999999996	1
40001717096	32500192704	0101000020E610000089D1730BDD7453C0345FCA6548AE4140	1.22399997711181996	d04/325/19	1.25	1
40002110051	15901240029	0101000020E610000054C6BFCFB88B53C010A26B15B3D24140	3.9909999370575	d04/159/84	1.25	2
40002510051	35100560222	0101000020E6100000A39AED65B69253C007955DD5FEBD4140	0.187999993562698003	d04/351/56	1.25	1
40001566042	30400531116	0101000020E6100000E3885A3F227853C03CF54883DB3D4240	0.0599999986588954995	d04/304/53	1.95999999999999996	1
40001945064	31901522512	0101000020E6100000CB468C43A28253C01A0AE93A9EEA4140	7.01800012588500977	d04/319/112	1.95999999999999996	1
40001531098	31900161110	0101000020E61000009B705413E96C53C0FB6E04F3A1D34140	1.64400005340575994	d04/319/16	1.95999999999999996	1
40001505096	33800281503	0101000020E6100000F31142516A7A53C08351499D80C84140	2.89800000190734997	d04/338/28	1.95999999999999996	1
40001007051	35101182013	0101000020E61000005A10CAFBB88A53C0FA2F6BBD3AB24140	13.7810001373290998	d04/351/78	1.25	3
40002328051	35101534826	0101000020E61000004DB38A48DE8E53C0A4575E4DF9C34140	1.03100001811981001	d04/351/113	1.25	1
40001675096	32700385108	0101000020E6100000CB773AA1A17653C0BB6A5496D7B84140	0.222000002861023005	d04/327/38	1.25	1
40002339064	30800471224	0101000020E610000082B34A9F8C7953C0338232326D0D4240	0.0329999998211861004	d04/308/47	1.95999999999999996	1
40001115064	42400515327	0101000020E6100000A8A8FA95CE8E53C0AF8273A14DE34140	2.25500011444092019	d04/424/51	1.25	1
40002523051	35601070529	0101000020E610000057957D57848C53C04D91329875BA4140	3.60299992561340021	d04/356/67	1.25	1
40001154096	33501365412	0101000020E6100000554CA59F708353C0AE3F2E162BA34140	0.0379999987781048029	d04/335/96	1.25	1
40002305096	33500181408	0101000020E61000003FD46CD4797953C0E9FF6673E6B84140	0.00800000037997961044	d04/335/18	1.25	1
40001720096	32500283502	0101000020E61000002CFCCF50927553C0F9FDF6D099AB4140	0.379000008106232023	d04/325/28	1.25	1
40001007096	35601582220	0101000020E6100000A600625C3B8853C0374EAF39ACB24140	4.13600015640258967	d04/356/118	1.25	2
40001127096	33501402825	0101000020E61000005AEC9BA0728553C0BE6BD097DEA34140	1.1269999742507899	d04/335/100	1.25	1
40001614033	31501442614	0101000020E610000075E04158326653C0DAE4F04927DD4140	2.02399992942810014	d04/315/104	1.95999999999999996	1
40002127051	35600275009	0101000020E61000004CA8E0F0028E53C096F6BCD17DCF4140	0.670000016689300981	d04/356/27	1.25	1
40001417064	30801333508	0101000020E61000006F9EEA909B7C53C05BD5ED47E5074240	1.04299998283386008	d04/308/93	1.95999999999999996	1
40001121098	16501580619	0101000020E610000012A7EE25688853C082B0AE658DD34140	1.04499995708465998	d04/165/118	1.25	1
40002525051	35600544319	0101000020E6100000224F37F5A68D53C05455682096B84140	0.314000010490416981	d04/356/54	1.25	1
40001706096	32700170321	0101000020E6100000E4B622D6077653C0A946544DB5B54140	0.133000001311301991	d04/327/17	1.25	1
40001210042	30601400420	0101000020E6100000A7F1C1210A6F53C053B70E69AF1E4240	11.3850002288818004	d04/306/100	1.95999999999999996	2
40001207033	31400173203	0101000020E6100000BB88A537126653C0FFD4D3A299F34140	0.66699999570846602	d04/314/17	1.95999999999999996	1
40001319051	35900171209	0101000020E610000039F2406491A553C0627E13AF57BD4140	2.15899991989136009	d04/359/17	1.95999999999999996	1
40002392051	33901182607	0101000020E610000040CE458DD38E53C062C0ED64CBC54140	0.866999983787536954	d04/339/78	1.95999999999999996	1
40001001051	15800251221	0101000020E610000094F6065F988853C0B5368DEDB5C54140	2.72099995613098011	d04/158/25	1.25	1
40001207042	30600045513	0101000020E610000052BAF42F496E53C07203F4B1711E4240	1.26900005340575994	d04/306/4	1.95999999999999996	1
40001117042	30301141508	0101000020E6100000CB5BBFAA445E53C0A7A73407AD1A4240	2.77699995040893999	d04/303/74	1.95999999999999996	2
40001220042	30300400825	0101000020E610000097F7DD19926B53C0B05758703F174240	0.0160000007599592001	d04/303/40	1.95999999999999996	1
40002312051	35601190424	0101000020E610000077E6D484238F53C06E2CCD5257BF4140	1.00499999523162997	d04/356/79	1.25	1
40001928096	33501464919	0101000020E61000009184D8F4FB7F53C0C25C9C42F8A84140	1.92900002002715998	d04/335/106	1.25	2
40002127051	35600284809	0101000020E6100000404750A1DF8E53C05D03B6DECACE4140	1.53900003433228005	d04/356/28	1.25	2
40001204033	31401495227	0101000020E6100000983DBFDE336653C0DC52BDEB22EE4140	0.0480000004172324995	d04/314/109	1.95999999999999996	1
40001136064	42400183706	0101000020E61000005840FC57318953C0176EAFBB2FEF4140	0.184000000357628007	d04/424/18	1.25	1
40001162051	32801431112	0101000020E610000025D126E2889C53C026E71FD84CBD4140	2.77800011634827015	d04/328/103	1.95999999999999996	1
40001928096	33501452019	0101000020E61000007FDEAF5D357F53C0FC3905F9D9A64140	0.595000028610229048	d04/335/105	1.25	1
40001702096	32700330528	0101000020E610000026074724657653C02A90D959F4B54140	1.05499994754790993	d04/327/33	1.25	1
40001727096	32501102524	0101000020E61000005E413FF8757853C0F2CF0CE203A64140	0.718999981880187988	d04/325/70	1.25	1
40001917096	33501434012	0101000020E6100000CF64A4839A7E53C0B4F688E29FA74140	1.16100001335143999	d04/335/103	1.25	1
40001883096	32700281324	0101000020E6100000A3C5BE09AA7853C07308C14FC1B54140	0.0390000008046626975	d04/327/28	1.25	1
40001154098	33700375929	0101000020E6100000889A8D3ADF8153C0DAA9B9DC60D84140	4.88399982452393022	d04/337/37	1.95999999999999996	3
40001941064	42401304003	0101000020E610000016B545E39A8353C00B85BEAA69E84140	2.20900011062621981	d04/424/90	1.25	1
40001341096	16501045000	0101000020E6100000044FC69DF78153C06B35DA6097C44140	2.08200001716613992	d04/165/64	1.25	1
40001002098	31801210104	0101000020E61000000CDEA1725D7153C00C91D3D7F3DF4140	8.18999958038330078	d04/318/81	1.95999999999999996	2
40001166051	32801545104	0101000020E6100000D15735ADB99D53C0C53FC7A244B74140	1.22599995136261009	d04/328/114	1.95999999999999996	1
40001007096	35601575210	0101000020E610000032303C40C18753C007B1D8CB5BB24140	3.68199992179871005	d04/356/117	1.25	1
40001210042	30601263712	0101000020E6100000E7C41EDA476E53C0A74C20DBE8304240	0.052000001072883599	d04/306/86	1.95999999999999996	1
40002524051	35600501306	0101000020E6100000A02AF05F6A8E53C0B72407EC6AB54140	1.38300001621246005	d04/356/50	1.25	1
40001728096	32700031900	0101000020E61000002A3A92CB7F7953C059901C9F7FA74140	2.25	d04/327/3	1.25	1
40001126064	42400405229	0101000020E61000001E9ECA0E968B53C026EC91BC29E74140	1.52900004386902011	d04/424/40	1.25	1
40001124033	31500235705	0101000020E610000083AB973A236F53C06A9B87B8DEE74140	4.43400001525878995	d04/315/23	1.95999999999999996	1
40001341096	16501060119	0101000020E6100000EE7893DF228353C0A659EA6A3CC44140	3.15499997138977006	d04/165/66	1.25	2
40001644098	33701302323	0101000020E610000019EB76514F7E53C049AEAC7EB6D04140	0.888000011444092019	d04/337/90	1.95999999999999996	1
40001338042	30800335719	0101000020E610000023467474817953C0F2F16492EC164240	0.651000022888184038	d04/308/33	1.95999999999999996	1
40001131064	42400135928	0101000020E6100000DBCF7355EA8A53C0123F106AD0EA4140	0.361999988555907981	d04/424/13	1.25	1
40001126033	31600423514	0101000020E6100000AADB3411916D53C0582A5E1BE0E94140	3.72600007057189986	d04/316/42	1.95999999999999996	1
40001141064	42400220307	0101000020E61000009BA49EAAE78953C0C4318111EAEE4140	1.27100002765656006	d04/424/22	1.25	1
40001403064	30800051125	0101000020E6100000BE182543E97C53C0A7125443D10F4240	2.25099992752075018	d04/308/5	1.95999999999999996	1
40001521096	16500135607	0101000020E6100000C3E22659BD7953C00F63D2DF4BC64140	0.811999976634979026	d04/165/13	1.25	1
40001526033	31401385708	0101000020E6100000530B804CC65B53C0EB7F6F8912ED4140	1.90600001811981001	d04/314/98	1.95999999999999996	1
40001500064	30800570802	0101000020E610000046A055C1837953C052AA8E66760D4240	2.30699992179871005	d04/308/57	1.95999999999999996	1
40002392051	33901183127	0101000020E6100000E6E37F97BE8E53C0606F078FDBC54140	0.94700002670288097	d04/339/78	1.95999999999999996	2
40001535096	15801484909	0101000020E6100000A35A4414137953C04526851ED6BA4140	5.6279997825622603	d04/158/108	1.25	1
40001106064	31800150015	0101000020E6100000A941E268D88853C077C883E3E8E44140	0.503000020980834961	d04/318/15	1.95999999999999996	1
40001002098	31801174924	0101000020E610000065B1039D7F7153C0C75DCEB6E4E44140	5.50400018692016957	d04/318/77	1.95999999999999996	1
40001112064	42400450315	0101000020E6100000DA6E27B6278C53C04CB0EE0EDFE04140	1.78600001335143999	d04/424/45	1.25	1
40001206042	30600402403	0101000020E61000003FF78A13046D53C0F7D26FBAC01E4240	2.23699998855590998	d04/306/40	1.95999999999999996	1
40001142051	32600594617	0101000020E6100000A61EB3FDF59C53C078AD293520AB4140	0.721000015735625999	d04/326/59	1.95999999999999996	1
40001915096	34000051510	0101000020E610000070534D5A027D53C0A8EAD44B42A04140	4.47700023651122958	d04/340/5	1.25	2
40001191051	34301065629	0101000020E61000007E7D63BEF29553C00057B26323A74140	0.444000005722046009	d04/343/66	1.25	1
40001157051	32301231123	0101000020E61000002E2F0ACCD49C53C0327F3B3F7BB14140	0.955999970436095969	d04/323/83	1.25	1
40001154098	33700365512	0101000020E6100000F092EE9D078253C06F7B270B04DA4140	3.97799992561340021	d04/337/36	1.95999999999999996	2
40001145064	42501115001	0101000020E6100000EB854C431E7D53C078E7F5CC37F94140	14.8850002288818004	d04/425/71	1.25	2
40001754096	35200250623	0101000020E6100000B75219106B7853C016D3968455954140	1.90199995040893999	d04/352/25	1.95999999999999996	1
40001739096	34000191222	0101000020E61000006BC9F495D17553C06BB2EB83D19C4140	3.57800006866454989	d04/340/19	1.25	2
40001150051	32301485709	0101000020E61000008070F4E7119A53C056010869D7B34140	2.64199995994568004	d04/323/108	1.25	1
40001235096	35201071529	0101000020E61000004455A75E128753C03E1B5EB5D7B74140	0.0160000007599592001	d04/352/67	1.95999999999999996	1
40001357051	34301294525	0101000020E6100000612C1DBD2BA153C08B5C267964B54140	0.27099999785423301	d04/343/89	1.25	1
40001185051	34301145802	0101000020E6100000D3BAB2B04C9553C0B48295F9FDAC4140	2.8440001010894802	d04/343/74	1.25	1
40001177051	32301141114	0101000020E6100000168B3ACE489C53C019D2979471AE4140	1.33599996566771995	d04/323/74	1.25	1
40001505064	30702000618	0101000020E6100000C877CEBBD67B53C0CE7D834078154240	2.40100002288818004	d04/307/120	1.95999999999999996	1
40001910064	31001261018	0101000020E61000007E9065C1C48153C05161116855FA4140	0.187999993562698003	d04/310/86	1.95999999999999996	1
40001102051	32300171012	0101000020E6100000A5F0452003A353C0ADD62E127FAD4140	0.893000006675719993	d04/323/17	1.25	1
40001113051	32300491609	0101000020E610000083458F29699E53C076ACAD3319A94140	5.18499994277954013	d04/323/49	1.25	3
40001154098	33700352823	0101000020E61000007C8B3D6A028253C0BF3AD8AC44DC4140	2.76099991798401012	d04/337/35	1.95999999999999996	1
40001151064	42500252129	0101000020E6100000277B95C6798D53C0BEC51E3581F14140	0.437000006437302024	d04/425/25	1.25	1
40001158051	32301201706	0101000020E6100000CA0DD0C7469F53C05A5A571696B14140	2.37899994850159002	d04/323/80	1.25	2
40001157051	32301242313	0101000020E6100000256F25E07C9D53C0189EF24300B34140	2.0309998989105198	d04/323/84	1.25	3
40001953096	34000104729	0101000020E6100000548F34B8AD7A53C011B8BFC469994140	0.0219999998807907	d04/340/10	1.25	1
40001168051	34301182805	0101000020E6100000B5615E91A9A153C01F0D4C135BB44140	0.977999985218047985	d04/343/78	1.25	1
40001224096	33600375407	0101000020E6100000FEE4396C6C8853C061495E42AAAE4140	1.76499998569488992	d04/336/37	1.95999999999999996	1
40001105051	32300263521	0101000020E6100000B39943520BA053C036453646A1AC4140	1.19700002670287997	d04/323/26	1.25	1
40001425064	31001021901	0101000020E6100000CD357117068053C0355C89E53B064240	2.05699992179871005	d04/310/62	1.95999999999999996	1
40001185051	34301151912	0101000020E6100000C0102851659553C02D49F9A46EAC4140	3.16400003433227983	d04/343/75	1.25	2
40001002042	30700411425	0101000020E610000043A44BA4D97153C01E407562C51B4240	11.0620002746581996	d04/307/41	1.95999999999999996	3
40001909064	31001305524	0101000020E6100000206118B0E48053C0E9DA72897EF84140	2.4309999942779501	d04/310/90	1.95999999999999996	1
40001171051	32301100319	0101000020E610000093E1783E03A053C0AFCE31207BB24140	1.18700003623962003	d04/323/70	1.25	238
40001915096	34000045310	0101000020E6100000C8A71144277D53C0A81EC429CEA04140	4.14799976348877042	d04/340/4	1.25	1
40001666098	33701165814	0101000020E610000080924C987A8653C065283806AECC4140	1.07899999618530007	d04/337/76	1.95999999999999996	1
40001330098	33700223417	0101000020E61000006BF0BE2A177953C08E95F32098E44140	0.790000021457672008	d04/337/22	1.95999999999999996	1
40001100098	33700545517	0101000020E6100000715413E9A37D53C0A999FFA1AAD64140	0.606999993324280007	d04/337/54	1.95999999999999996	1
40001145064	42501082612	0101000020E6100000BEFB3E775D8053C009F76F03E3F74140	11.8319997787475994	d04/425/68	1.25	1
40001155051	32301163729	0101000020E6100000A3E5400F359C53C022C5008926B14140	1.26100003719329989	d04/323/76	1.25	1
40001512064	30700573221	0101000020E610000082AED8BAAF7653C02FD6DC7646114240	0.00600000005215405984	d04/307/57	1.95999999999999996	1
40001002042	30700384125	0101000020E6100000FA7E6ABCF47353C04E2C4BCF4F1D4240	8.91399955749512074	d04/307/38	1.95999999999999996	2
40001111051	32300323606	0101000020E610000054628D69DC9F53C0F9C32A3982A74140	0.072999998927116394	d04/323/32	1.25	1
40001113051	32300473808	0101000020E610000057BA7141EC9E53C051D43EC2D5A64140	3.71499991416931019	d04/323/47	1.25	2
40001355051	34301333500	0101000020E61000008201840FA5A053C032A3699AC1B74140	0.411000013351439986	d04/343/93	1.25	1
40001188051	34301095009	0101000020E61000004E6ECACBD09453C0210CF26904A74140	1.40199995040893999	d04/343/69	1.25	1
40001105051	32300293221	0101000020E61000002338899C199F53C0E7B45D5782A84140	3.85100007057189986	d04/323/29	1.25	2
40001746096	35200154201	0101000020E6100000633CEF6B497753C0F749A4236F9B4140	0.273999989032744973	d04/352/15	1.95999999999999996	1
40001158051	32301174026	0101000020E61000001594FD4EEE9C53C08A2F2471A0B04140	0.0359999984502792011	d04/323/77	1.25	1
40001100098	33700591706	0101000020E61000009C059090378153C0B6B86BAE3FD44140	4.28000020980834961	d04/337/59	1.95999999999999996	2
40001157051	32301233503	0101000020E610000094D85A04EB9C53C06E1C0CD011B24140	1.30700004100800005	d04/323/83	1.25	2
40001209051	32301354704	0101000020E61000002D75351E919E53C0270FB0FB33B34140	0.924000024795532005	d04/323/95	1.25	1
40001399051	34301451503	0101000020E6100000EF377FB8D0A253C0702D49545EBD4140	0.808000028133392001	d04/343/105	1.25	1
40001190051	34300541317	0101000020E6100000D2A755F4079453C0DC91FB6717A84140	1.25300002098083008	d04/343/54	1.25	1
40001399051	34301453523	0101000020E6100000826A285ADEA253C0117B57F3D2BC4140	1.1180000305175799	d04/343/105	1.25	2
40001329051	34301424707	0101000020E6100000450CE0D2D6A153C002052857C2BF4140	0.882000029087066983	d04/343/102	1.25	1
40001214042	30701365814	0101000020E610000093342493787A53C03D17FCEC361B4240	6.38399982452393022	d04/307/96	1.95999999999999996	1
40001300051	32300032314	0101000020E61000001B18D41206A453C0D152C3C8DCAF4140	0.500999987125396951	d04/323/3	1.25	1
40001171051	32301114108	0101000020E61000009FD8F96DBE9F53C0F0124141CEAF4140	2.65000009536742986	d04/323/71	1.25	531
40001154051	32301503324	0101000020E610000015DE8A69CB9A53C0B026AA12C0B04140	0.514999985694885032	d04/323/110	1.25	1
40001331051	34301374813	0101000020E610000090696D1ADBA153C0A118B4EB39B84140	1.27900004386902011	d04/343/97	1.25	1
40001510064	30701245813	0101000020E6100000021FCDA2C17053C02700B507100F4240	11.0030002593993999	d04/307/84	1.95999999999999996	1
40001938096	34001370803	0101000020E61000004076CD9A0E8353C0FCB781F1C29B4140	0.911000013351439986	d04/340/97	1.25	1
40001158051	32301204606	0101000020E61000009135D9F5C19F53C0375A69ADC3B14140	2.81299996376037997	d04/323/80	1.25	3
40001120051	32300431021	0101000020E61000003FDC7AF2D59C53C046072461DFA44140	2.93799996376037997	d04/323/43	1.25	1
40001997064	31001363418	0101000020E6100000C67FCBAD5A7E53C07F96F8ED35F64140	1.60399997234343994	d04/310/96	1.95999999999999996	1
40001002042	30700322607	0101000020E610000011436106197953C05706D506271E4240	3.64000010490416992	d04/307/32	1.95999999999999996	1
40002311064	29601072011	0101000020E61000000023C385977953C08D73E5FDC9004240	0.0820000022649765015	d04/296/67	1.95999999999999996	1
40001148064	31101034815	0101000020E61000003EBE73DEB58853C07EFFE6C589F64140	0.902000010013579989	d04/311/63	1.95999999999999996	1
40001185051	34301153803	0101000020E610000003BCBB84799553C009E643ABEEAB4140	3.4440000057220499	d04/343/75	1.25	3
40001008096	34300021410	0101000020E61000007BEAA2320F8353C0FF42EAD1AFAF4140	1.75800001621246005	d04/343/2	1.25	1
40001706096	32700170921	0101000020E610000003B16CE6107653C088E3AF7F8DB54140	0.222000002861023005	d04/327/17	1.25	2
40001004064	30901523718	0101000020E610000084A7469EDA7E53C0BD299B28F8034240	11.875	d04/309/112	1.95999999999999996	1
40001137098	33901500703	0101000020E6100000FD063763628453C0F5143944DCE04140	2.06100010871886985	d04/339/110	1.95999999999999996	1
40001622042	29601544005	0101000020E610000021FAFF82EE6553C0EA20AF0793304240	0.323000013828277976	d04/296/114	1.95999999999999996	1
40001720051	35500575109	0101000020E61000008087FDF9919553C06D86C03687E14140	0.875999987125396951	d04/355/57	1.25	1
40001432064	30801392614	0101000020E6100000E7B3F281D37D53C0C51D6FF25B014240	0.670000016689300981	d04/308/99	1.95999999999999996	1
40001717064	22001512810	0101000020E61000000DC51D6FF27953C01F3240FDC2F34140	5.21799993515015004	d04/220/111	1.25	1
40001406042	30401244412	0101000020E6100000F40E01D15D7753C011F05AF8B03D4240	2.53999996185303001	d04/304/84	1.95999999999999996	2
40001531064	31000211513	0101000020E61000005A07ACC1207853C00A6AF816D6064240	3.89000010490416992	d04/310/21	1.95999999999999996	1
40001225042	30600250212	0101000020E6100000524832AB776C53C09A4EA1A98D144240	0.225999996066093001	d04/306/25	1.95999999999999996	1
40001400033	30000081915	0101000020E6100000DEBBBCEFCE6F53C0DB53CD075F014240	2.33800005912780984	d04/300/8	1.95999999999999996	1
40001330051	34401231412	0101000020E6100000C7551B52FB9D53C077C47CD4BAC64140	0.052000001072883599	d04/344/83	1.25	1
40001616042	30600235410	0101000020E6100000C82764E76D6B53C0D46D3FCF552C4240	0.519999980926514005	d04/306/23	1.95999999999999996	1
40001117042	30301130918	0101000020E61000004856D9D2FE5E53C0C68BE0DAE41B4240	1.8550000190734901	d04/303/73	1.95999999999999996	1
40001673064	29601084513	0101000020E610000005847B0A257A53C07D68D59DDDFF4140	0.317000001668929998	d04/296/68	1.95999999999999996	1
40002509051	35100530209	0101000020E61000003B42BC64D29253C021D335EE28BE4140	0.795000016689300981	d04/351/53	1.25	1
40001310064	42501474203	0101000020E6100000E83812C3E97A53C0B1F9B836540E4240	14.3809995651244993	d04/425/107	1.25	1
40001113051	32300441828	0101000020E610000030968EDE959D53C0D52FC7E182A34140	0.726999998092651034	d04/323/44	1.25	1
40001207096	34201362524	0101000020E61000004BB61556058F53C0B941A32A5CA64140	0.112000003457068995	d04/342/96	1.25	1
40001308051	35902013028	0101000020E61000005E413FF875A353C0750E547C32B94140	2.41400003433227983	d04/359/121	1.95999999999999996	1
40002124051	35501541503	0101000020E6100000B274F4AE308F53C0A01E36EC52D14140	0.55500000715255704	d04/355/114	1.25	1
40001937096	16100350429	0101000020E610000014D7E7201E8153C00B6EB598E9984140	0.22900000214576699	d04/161/35	1.25	2
40001240042	30600283129	0101000020E6100000D2EE46D5E57053C0529B38B9DF164240	0.0500000007450581013	d04/306/28	1.95999999999999996	1
40001960064	22000431902	0101000020E610000073B21E08DA8353C0169DD1FB6BE54140	2.10100007057189986	d04/220/43	1.25	1
40001136051	34300400925	0101000020E61000009E4FD31D7A9653C004A09B470FA84140	3.78600001335143999	d04/343/40	1.25	1
40001303051	35801404307	0101000020E61000003D9E961F38A553C08331225168B34140	1.6759999990463299	d04/358/100	1.95999999999999996	1
40001210042	30601400828	0101000020E6100000C44373F8FF6E53C03B21CF89981E4240	11.4449996948241992	d04/306/100	1.95999999999999996	3
40001997064	31001364518	0101000020E6100000E3F7DB43677E53C061BB20C77BF64140	1.75899994373321999	d04/310/96	1.95999999999999996	2
40001116051	33600004504	0101000020E61000008F029F7AFF9853C0B4FE3B4789A84140	0.597999989986420011	d04/336/0	1.95999999999999996	1
40001171051	32301090228	0101000020E6100000DCAC0B8945A053C0DE196D5512B44140	0.277000010013579989	d04/323/69	1.25	56
40001171051	32301090329	0101000020E6100000CB5BBFAA44A053C083B982120BB44140	0.29199999570846602	d04/323/69	1.25	59
40001171051	32301090428	0101000020E61000006D1107BF43A053C0B6F9DA8E04B44140	0.305999994277953991	d04/323/69	1.25	62
40001171051	32301090518	0101000020E610000001BD70E742A053C0489858CFFFB34140	0.316000014543532992	d04/323/69	1.25	64
40001171051	32301090619	0101000020E61000006815EC7541A053C0CEA8F92AF9B34140	0.331000000238419023	d04/323/69	1.25	67
40001171051	32301090728	0101000020E61000006330DA3E3FA053C0080E1E5CF0B34140	0.351000010967255027	d04/323/69	1.25	71
40001171051	32301090808	0101000020E61000005D5C99A63EA053C0D9A95E23EEB34140	0.356000006198883001	d04/323/69	1.25	72
40001171051	32301090829	0101000020E6100000DB3BFE663DA053C0D0B12891E9B34140	0.365999996662140004	d04/323/69	1.25	74
40001171051	32301090908	0101000020E61000006A3E9DE13CA053C0ADE17DB0E7B34140	0.370999991893767977	d04/323/69	1.25	75
40001171051	32301091218	0101000020E6100000F01D90DF36A053C08236397CD2B34140	0.419999986886977983	d04/323/69	1.25	85
40001171051	32301091318	0101000020E610000050D0DCF934A053C0564046E5CBB34140	0.435999989509583019	d04/323/69	1.25	88
40001171051	32301091608	0101000020E6100000DCF63DEA2FA053C0A01518B2BAB34140	0.476000010967255027	d04/323/69	1.25	96
40001171051	32301091618	0101000020E6100000CAEA0C422FA053C08A213999B8B34140	0.481000006198883001	d04/323/69	1.25	97
40001171051	32301091708	0101000020E61000006C2D27FC2DA053C08C193CA7B4B34140	0.490999996662140004	d04/323/69	1.25	99
40001171051	32301091729	0101000020E6100000671767672CA053C0AC72A1F2AFB34140	0.501999974250793013	d04/323/69	1.25	101
40001171051	32301091909	0101000020E6100000AF2E5D7729A053C0FEA3CA8BA7B34140	0.522000014781952015	d04/323/69	1.25	105
40001171051	32301091918	0101000020E61000009D3935E128A053C08D36D8E5A5B34140	0.526000022888184038	d04/323/69	1.25	106
40001171051	32301092018	0101000020E61000005793A7AC26A053C0374B6EB99FB34140	0.541000008583068959	d04/323/69	1.25	109
40001171051	32301092109	0101000020E61000005999DF1F25A053C0C26E33709BB34140	0.550999999046326017	d04/323/69	1.25	111
40001171051	32301092309	0101000020E61000008458479F20A053C0E0B2AFE18EB34140	0.580999970436095969	d04/323/69	1.25	117
40001171051	32301092509	0101000020E61000009E1FEB4E1CA053C07CD058A082B34140	0.611000001430511031	d04/323/69	1.25	123
40001171051	32301092518	0101000020E610000027EF88AF1BA053C0E8BA95CA80B34140	0.615999996662140004	d04/323/69	1.25	124
40001171051	32301092528	0101000020E61000008D4468041BA053C083FB5CC87EB34140	0.620000004768372026	d04/323/69	1.25	125
40001171051	32301093009	0101000020E61000009D9D0C8E12A053C0BC5CC47762B34140	0.686999976634979026	d04/323/69	1.25	138
40001171051	32301093309	0101000020E61000009A7F4F070DA053C0DD5CFC6D4FB34140	0.731000006198882946	d04/323/69	1.25	147
40001171051	32301094308	0101000020E6100000B13F3F4203A053C01893FE5E0AB34140	0.880999982357025035	d04/323/69	1.25	177
40001171051	32301094709	0101000020E6100000FE7A2A4C04A053C050F4650EEEB24140	0.940999984741211049	d04/323/69	1.25	189
40001171051	32301095008	0101000020E61000005C35745806A053C0B55F2D2DD9B24140	0.986000001430511031	d04/323/69	1.25	198
40001171051	32301095708	0101000020E610000096FF35C508A053C02723788DA7B24140	1.09099996089934992	d04/323/69	1.25	219
40001171051	32301090018	0101000020E6100000171E45E746A053C0173D5C1723B44140	0.240999996662140004	d04/323/69	1.25	49
40001171051	32301090409	0101000020E6100000C0DEB36444A053C02B0428FC08B44140	0.296000003814696988	d04/323/69	1.25	60
40001171051	32301090629	0101000020E6100000D39DCCE440A053C034D6FECEF6B34140	0.335999995470046997	d04/323/69	1.25	68
40001171051	32301090718	0101000020E6100000F7BE02E23FA053C02B9611CDF2B34140	0.345999985933304	d04/323/69	1.25	70
40001171051	32301090919	0101000020E610000093EEF8403CA053C0EABDE776E5B34140	0.375999987125397006	d04/323/69	1.25	76
40001171051	32301090928	0101000020E610000011B4B8B53BA053C0CEF22B8CE3B34140	0.381000012159347978	d04/323/69	1.25	77
40001171051	32301091008	0101000020E6100000E260CA1B3BA053C0CE401B6FE1B34140	0.384999990463257002	d04/323/69	1.25	78
40001171051	32301091208	0101000020E610000020717E7937A053C016A8209AD4B34140	0.416000008583069014	d04/323/69	1.25	84
40001171051	32301091308	0101000020E610000062C5049035A053C0CC3C5EEDCDB34140	0.430999994277953991	d04/323/69	1.25	87
40001171051	32301091409	0101000020E61000009EFD929E33A053C088D68A36C7B34140	0.446999996900558028	d04/323/69	1.25	90
40001171051	32301091509	0101000020E61000003B8375D231A053C0C7AAF70AC1B34140	0.460999995470046997	d04/323/69	1.25	93
40001171051	32301091519	0101000020E610000058FBE02131A053C0D4D4B2B5BEB34140	0.467000007629394975	d04/323/69	1.25	94
40001171051	32301091718	0101000020E61000005AF3E32F2DA053C08D0B0742B2B34140	0.495999991893767977	d04/323/69	1.25	100
40001171051	32301091928	0101000020E61000009820D91228A053C0D01731A2A3B34140	0.531000018119812012	d04/323/69	1.25	107
40001171051	32301092009	0101000020E6100000931E865627A053C01E5F8C92A1B34140	0.536000013351439986	d04/323/69	1.25	108
40001171051	32301092028	0101000020E6100000BED17DEF25A053C06E50FBAD9DB34140	0.545000016689300981	d04/323/69	1.25	110
40001171051	32301092218	0101000020E61000002A38BC2022A053C0DE16D11B93B34140	0.570999979972839022	d04/323/69	1.25	115
40001171051	32301092619	0101000020E61000007003E38519A053C0A454C2137AB34140	0.632000029087066983	d04/323/69	1.25	127
40001171051	32301092628	0101000020E6100000F4CD91F018A053C0E08C502278B34140	0.635999977588654009	d04/323/69	1.25	128
40001171051	32301092718	0101000020E610000017AAACB717A053C0955DD5FE73B34140	0.646000027656554954	d04/323/69	1.25	130
40001171051	32301092809	0101000020E6100000E970636916A053C04FD724896FB34140	0.656000018119812012	d04/323/69	1.25	132
40001171051	32301092819	0101000020E61000006C2409C215A053C06334E14D6DB34140	0.661000013351439986	d04/323/69	1.25	133
40001171051	32301092908	0101000020E6100000E4FE7E8C14A053C05FF9E24169B34140	0.670000016689300981	d04/323/69	1.25	135
40001171051	32301092919	0101000020E6100000AE788FD813A053C0316711E566B34140	0.675999999046326017	d04/323/69	1.25	136
40001171051	32301092929	0101000020E61000000EB2762513A053C08557378364B34140	0.681999981403351052	d04/323/69	1.25	137
40001171051	32301093018	0101000020E6100000BB438A0112A053C0874F3A9160B34140	0.690999984741211049	d04/323/69	1.25	139
40001171051	32301093108	0101000020E61000002D1911D610A053C089192B7B5CB34140	0.700999975204467995	d04/323/69	1.25	141
40001171051	32301093208	0101000020E6100000520FD1E80EA053C051EB47D455B34140	0.716000020503998025	d04/323/69	1.25	144
40001171051	32301093219	0101000020E61000001C89E1340EA053C0E79CE96F53B34140	0.722000002861022949	d04/323/69	1.25	145
40001171051	32301093229	0101000020E6100000E719FB920DA053C05930F14751B34140	0.726000010967254972	d04/323/69	1.25	146
40001171051	32301093318	0101000020E61000003070D4650CA053C03EB324404DB34140	0.736000001430511031	d04/323/69	1.25	148
40001171051	32301093328	0101000020E61000008ED7CDD60BA053C07AEBB24E4BB34140	0.740999996662140004	d04/323/69	1.25	149
40001171051	32301093428	0101000020E6100000F5A512F909A053C0DD81959E44B34140	0.755999982357025035	d04/323/69	1.25	152
40001171051	32301093518	0101000020E610000031F20DE008A053C0DF1D746440B34140	0.764999985694885032	d04/323/69	1.25	154
40001171051	32301093708	0101000020E61000000EAF35A506A053C05C08CD0935B34140	0.791000008583068959	d04/323/69	1.25	159
40001171051	32301093818	0101000020E6100000561C188A05A053C0FBC2D08F2BB34140	0.810999989509582964	d04/323/69	1.25	163
40001171051	32301093929	0101000020E61000003AC1EDBF04A053C09017D2E121B34140	0.830999970436095969	d04/323/69	1.25	167
40001171051	32301094019	0101000020E6100000750A4D6D04A053C0A9995A5B1DB34140	0.841000020503998025	d04/323/69	1.25	169
40001171051	32301094109	0101000020E6100000C8957A1604A053C05F84848318B34140	0.851000010967254972	d04/323/69	1.25	171
40001171051	32301094118	0101000020E6100000694826F103A053C0A798DE5916B34140	0.856000006198882946	d04/323/69	1.25	172
40001171051	32301094129	0101000020E6100000EC9C0BC803A053C0558C4EF113B34140	0.861000001430511031	d04/323/69	1.25	173
40001171051	32301094508	0101000020E61000002285573703A053C07FD12F5BFCB24140	0.911000013351439986	d04/323/69	1.25	183
40001171051	32301094519	0101000020E6100000DAD5F55503A053C0C7B7770DFAB24140	0.916000008583068959	d04/323/69	1.25	184
40001171051	32301094609	0101000020E6100000E6690AAE03A053C0F4ECA820F5B24140	0.925999999046326017	d04/323/69	1.25	186
40001171051	32301094618	0101000020E6100000ECB314DA03A053C0CBBBEA01F3B24140	0.930999994277953991	d04/323/69	1.25	187
40001171051	32301094629	0101000020E61000008DD9ED0E04A053C0076A42A4F0B24140	0.935999989509582964	d04/323/69	1.25	188
40001171051	32301094718	0101000020E61000002E44E27904A053C0DB25602AECB24140	0.94499999284744296	d04/323/69	1.25	190
40001171051	32301094729	0101000020E6100000FD0461B804A053C0A6327B8FE9B24140	0.950999975204467995	d04/323/69	1.25	191
40001171051	32301094818	0101000020E6100000270E452605A053C0A26D4617E5B24140	0.959999978542327992	d04/323/69	1.25	193
40001171051	32301094829	0101000020E6100000214E716605A053C056389380E2B24140	0.966000020503998025	d04/323/69	1.25	194
40001171051	32301094918	0101000020E610000068B51BD805A053C0E32D4613DEB24140	0.975000023841858021	d04/323/69	1.25	196
40001171051	32301095029	0101000020E6100000201A27CF06A053C022B2FE85D4B24140	0.995999991893767977	d04/323/69	1.25	200
40001171051	32301095108	0101000020E61000009DDC4A0A07A053C0055D0C2FD2B24140	1.00100004673003995	d04/323/69	1.25	201
40001171051	32301095118	0101000020E610000091007F4207A053C031FC96EFCFB24140	1.00600004196166992	d04/323/69	1.25	202
40001171051	32301095128	0101000020E61000000EC3A27D07A053C032EE618ACDB24140	1.00999999046325994	d04/323/69	1.25	203
40001171051	32301095208	0101000020E61000001424B6BB07A053C0C771F101CBB24140	1.01600003242493009	d04/323/69	1.25	204
40001171051	32301095219	0101000020E6100000DEC83CF207A053C0E6D88BB2C8B24140	1.02100002765656006	d04/323/69	1.25	205
40001171051	32301095229	0101000020E6100000D3EC702A08A053C03B9B9F2CC6B24140	1.02699995040893999	d04/323/69	1.25	206
40001171051	32301095409	0101000020E610000036F7FCD508A053C0ACD106BBBCB24140	1.04600000381469993	d04/323/69	1.25	210
40001171051	32301095608	0101000020E610000067D7BD1509A053C0F39A68A1AEB24140	1.07599997520446999	d04/323/69	1.25	216
40001171051	32301095728	0101000020E6100000FCB0396208A053C0293520E7A2B24140	1.10000002384185991	d04/323/69	1.25	221
40001171051	32301095918	0101000020E6100000DE9DC60707A053C0F48EAE2D97B24140	1.125	d04/323/69	1.25	226
40001171051	32301084429	0101000020E61000005B1F7B6242A053C08B94771F91B44140	0.00700000021606683991	d04/323/68	1.25	2
40001171051	32301084508	0101000020E61000008AE8329042A053C0042D6EED8EB44140	0.0109999999403954003	d04/323/68	1.25	3
40001171051	32301084528	0101000020E61000004955C9B642A053C0E3207C838AB44140	0.0209999997168778992	d04/323/68	1.25	5
40001171051	32301084619	0101000020E61000005500E72043A053C0F10EF0A485B44140	0.0309999994933604986	d04/323/68	1.25	7
40001171051	32301084709	0101000020E61000009074BCB843A053C0ACFE08C380B44140	0.0419999994337559024	d04/323/68	1.25	9
40001171051	32301084808	0101000020E610000072416C9F44A053C056B77A4E7AB44140	0.0560000017285346985	d04/323/68	1.25	12
40001171051	32301084908	0101000020E610000088C5B99745A053C0D70AE42373B44140	0.0710000023245811046	d04/323/68	1.25	15
40001171051	32301084918	0101000020E61000006CC317DC45A053C0C016050B71B44140	0.0759999975562096058	d04/323/68	1.25	16
40001171051	32301085018	0101000020E6100000475DC6A846A053C0419880046AB44140	0.0909999981522559981	d04/323/68	1.25	19
40001171051	32301085208	0101000020E610000029136D7D47A053C03B1A87FA5DB44140	0.115999996662140004	d04/323/68	1.25	24
40001171051	32301085228	0101000020E6100000DB5E1CA647A053C02C1D627259B44140	0.126000002026558006	d04/323/68	1.25	26
40001171051	32301085318	0101000020E61000007651F4C047A053C070C273A554B44140	0.136000007390976008	d04/323/68	1.25	28
40001171051	32301085329	0101000020E61000007C6DECC847A053C05F1B3BF251B44140	0.142000004649161987	d04/323/68	1.25	29
40001171051	32301085518	0101000020E61000003B9567B947A053C0E83D84A746B44140	0.165999993681907987	d04/323/68	1.25	34
40001171051	32301085609	0101000020E61000003B7E5EA747A053C01473B5BA41B44140	0.175999999046325989	d04/323/68	1.25	36
40001171051	32301085719	0101000020E6100000F372D87D47A053C0A194B5F237B44140	0.196999996900558	d04/323/68	1.25	40
40001171051	32301085809	0101000020E6100000AC7E5B6647A053C01B1F775B33B44140	0.206000000238418995	d04/323/68	1.25	42
40001171051	32301090108	0101000020E6100000A765FF9746A053C08000080E1EB44140	0.250999987125397006	d04/323/69	1.25	51
40001171051	32301090118	0101000020E6100000B258D47146A053C0F7C610001CB44140	0.256000012159347978	d04/323/69	1.25	52
40001171051	32301090128	0101000020E6100000D0717F3F46A053C053BC259419B44140	0.259999990463257002	d04/323/69	1.25	53
40001171051	32301090208	0101000020E6100000304CA60A46A053C05AE1F14817B44140	0.266000002622603982	d04/323/69	1.25	54
40001171051	32301090218	0101000020E61000007DE9EDCF45A053C03D8CFFF114B44140	0.27099999785423301	d04/323/69	1.25	55
40001171051	32301090608	0101000020E61000009D6DC90542A053C086F0C39CFBB34140	0.326000005006789995	d04/323/69	1.25	66
40001171051	32301090708	0101000020E6100000E5396C6C40A053C0E886A6ECF4B34140	0.340999990701675026	d04/323/69	1.25	69
40001171051	32301091018	0101000020E6100000ACDADA673AA053C09A7B48F8DEB34140	0.391000002622603982	d04/323/69	1.25	79
40001171051	32301091029	0101000020E6100000060FD3BE39A053C0D124B1A4DCB34140	0.397000014781952015	d04/323/69	1.25	80
40001171051	32301091118	0101000020E6100000A87FFF9C38A053C008A63FA0D8B34140	0.405999988317490013	d04/323/69	1.25	82
40001171051	32301091128	0101000020E61000000DECE70338A053C0E0748181D6B34140	0.411000013351439986	d04/323/69	1.25	83
40001171051	32301091228	0101000020E61000008B13043436A053C08F60F426D0B34140	0.425999999046326017	d04/323/69	1.25	86
40001171051	32301091829	0101000020E61000005C446F4C2AA053C0D93741E5A9B34140	0.515999972820281982	d04/323/69	1.25	104
40001171051	32301092128	0101000020E6100000ACCB84BA23A053C0B85C589297B34140	0.560999989509582964	d04/323/69	1.25	113
40001171051	32301092208	0101000020E61000005FECBDF822A053C078E9CB7795B34140	0.564999997615813987	d04/323/69	1.25	114
40001171051	32301092418	0101000020E6100000D3B947DB1DA053C06E58AE1287B34140	0.600000023841858021	d04/323/69	1.25	121
40001171051	32301092428	0101000020E61000004502FC091DA053C07A8269BD84B34140	0.606000006198882946	d04/323/69	1.25	122
40001171051	32301092608	0101000020E6100000ABA5CA411AA053C03D27BD6F7CB34140	0.625999987125396951	d04/323/69	1.25	126
40001171051	32301092709	0101000020E610000035C0BB4B18A053C06A6226F675B34140	0.640999972820281982	d04/323/69	1.25	129
40001171051	32301092729	0101000020E610000071C79BFC16A053C025DC758071B34140	0.652000010013579989	d04/323/69	1.25	131
40001171051	32301093119	0101000020E61000003438A51710A053C03DE477E459B34140	0.705999970436095969	d04/323/69	1.25	142
40001171051	32301093128	0101000020E6100000E08101840FA053C0C1E270E657B34140	0.711000025272369052	d04/323/69	1.25	143
40001171051	32301093508	0101000020E610000030AA567009A053C03701E19E42B34140	0.759999990463256947	d04/323/69	1.25	153
40001171051	32301093529	0101000020E6100000DE3B6A4C08A053C0401878EE3DB34140	0.771000027656554954	d04/323/69	1.25	155
40001171051	32301093618	0101000020E610000067C6EC7607A053C02AA09ADC39B34140	0.779999971389770952	d04/323/69	1.25	157
40001171051	32301093628	0101000020E61000006220BE0207A053C03DA1325937B34140	0.786000013351439986	d04/323/69	1.25	158
40001171051	32301093729	0101000020E6100000AFC0A10106A053C0353FA31930B34140	0.800999999046326017	d04/323/69	1.25	161
40001171051	32301093829	0101000020E61000008056AA5505A053C0EBA5CE4829B34140	0.815999984741211049	d04/323/69	1.25	164
40001171051	32301093909	0101000020E610000068CFC02305A053C04BCEE4F626B34140	0.820999979972839022	d04/323/69	1.25	165
40001171051	32301094028	0101000020E6100000AA7CCF4804A053C01B5B74571BB34140	0.846000015735625999	d04/323/69	1.25	170
40001171051	32301094208	0101000020E6100000D52C2BA803A053C04BD05FE811B34140	0.865999996662140004	d04/323/69	1.25	174
40001171051	32301094219	0101000020E61000002E02637D03A053C07BBC900E0FB34140	0.870999991893767977	d04/323/69	1.25	175
40001171051	32301094228	0101000020E61000003F11305F03A053C00B9755D80CB34140	0.875999987125396951	d04/323/69	1.25	176
40001171051	32301094418	0101000020E6100000FEF38F1903A053C022EA4F2C01B34140	0.901000022888184038	d04/323/69	1.25	181
40001171051	32301094429	0101000020E6100000ECCDB92503A053C05A09826CFEB24140	0.906000018119812012	d04/323/69	1.25	182
40001171051	32301094808	0101000020E61000005048D7F104A053C0CB9E0436E7B24140	0.954999983310699019	d04/323/69	1.25	192
40001171051	32301095309	0101000020E610000054B4835B08A053C0908BC5CAC3B24140	1.03100001811981001	d04/323/69	1.25	207
40001171051	32301095418	0101000020E6100000A86A27EF08A053C0A64819CCBAB24140	1.04999995231627996	d04/323/69	1.25	211
40001171051	32301095429	0101000020E61000000DBD6A0A09A053C06C223317B8B24140	1.0559999942779501	d04/323/69	1.25	212
40001171051	32301095508	0101000020E61000008435841909A053C08B89CDC7B5B24140	1.06099998950958008	d04/323/69	1.25	213
40001171051	32301095518	0101000020E610000061D2CE1F09A053C0F212F7B3B3B24140	1.06500005722046009	d04/323/69	1.25	214
40001171051	32301095529	0101000020E6100000CC12F81E09A053C064EEB5FBB0B24140	1.07099997997284002	d04/323/69	1.25	215
40001171051	32301095629	0101000020E6100000432FEDE508A053C0565925A2A9B24140	1.08599996566771995	d04/323/69	1.25	218
40001171051	32301095819	0101000020E6100000F6F301DC07A053C027E6B4029EB24140	1.11099994182587003	d04/323/69	1.25	223
40001171051	32301095928	0101000020E6100000F06778B306A053C0F65267A494B24140	1.13100004196166992	d04/323/69	1.25	227
40001171051	32301084818	0101000020E61000000D795FF044A053C08156050F78B44140	0.061000000685453401	d04/323/68	1.25	13
40001171051	32301084929	0101000020E6100000EEB83C3146A053C0DAEE79596EB44140	0.0810000002384186069	d04/323/68	1.25	17
40001171051	32301085009	0101000020E61000008EF51E7846A053C0522B4CDF6BB44140	0.0869999974966049056	d04/323/68	1.25	18
40001171051	32301085028	0101000020E61000008F7F55E446A053C05599188167B44140	0.0970000028610228937	d04/323/68	1.25	20
40001171051	32301085128	0101000020E6100000DC02F85D47A053C0C30BC79860B44140	0.111000001430511003	d04/323/68	1.25	23
40001171051	32301085218	0101000020E6100000A6A77E9447A053C0D1CB28965BB44140	0.120999999344349005	d04/323/68	1.25	25
40001171051	32301085308	0101000020E6100000E8960CB647A053C0B59613FE56B44140	0.131999999284744013	d04/323/68	1.25	27
40001171051	32301085408	0101000020E61000009ACBB2CC47A053C0BF9F75E84FB44140	0.14599999785423301	d04/323/68	1.25	30
40001171051	32301085428	0101000020E6100000888ED3C647A053C0BC7E1C284BB44140	0.156000003218651012	d04/323/68	1.25	32
40001171051	32301085528	0101000020E61000000BFAC1AF47A053C09C08D11044B44140	0.171000003814696988	d04/323/68	1.25	35
40001171051	32301085618	0101000020E61000003462669F47A053C0AA807B9E3FB44140	0.180999994277953991	d04/323/68	1.25	37
40001171051	32301085628	0101000020E610000005C7C09547A053C0647EC9213DB44140	0.186000004410743991	d04/323/68	1.25	38
40001171051	32301085709	0101000020E6100000ACAC6D8A47A053C0AD08ED8B3AB44140	0.190999999642371993	d04/323/68	1.25	39
40001171051	32301085828	0101000020E61000003B0B314D47A053C0AC472B082FB44140	0.216000005602836997	d04/323/68	1.25	44
40001171051	32301085908	0101000020E61000005852EE3E47A053C03DF4DDAD2CB44140	0.221000000834464999	d04/323/68	1.25	45
40001171051	32301085918	0101000020E6100000239B502D47A053C09DC0CF132AB44140	0.225999996066093001	d04/323/68	1.25	46
40001171051	32301085928	0101000020E61000005924DC1A47A053C08670CCB227B44140	0.231000006198883001	d04/323/68	1.25	47
40001171051	32301100208	0101000020E61000007B3D4E8704A053C0E694809884B24140	1.16600000858306996	d04/323/70	1.25	234
40001171051	32301100219	0101000020E61000003404B63904A053C0CF728F5B82B24140	1.16999995708465998	d04/323/70	1.25	235
40001171051	32301100229	0101000020E610000069311DDF03A053C0EF7D05C47FB24140	1.1759999990463299	d04/323/70	1.25	236
40001171051	32301100308	0101000020E6100000A591859E03A053C01FACB5E67DB24140	1.17999994754790993	d04/323/70	1.25	237
40001171051	32301100328	0101000020E6100000C220FAFF02A053C01BB96E4A79B24140	1.19000005722046009	d04/323/70	1.25	239
40001171051	32301100418	0101000020E610000010340B5902A053C077A04E7974B24140	1.20099997520446999	d04/323/70	1.25	241
40001171051	32301100509	0101000020E6100000582B24AA01A053C03795568D6FB24140	1.21099996566771995	d04/323/70	1.25	243
40001171051	32301100518	0101000020E6100000C40F296101A053C06F9AE3816DB24140	1.21599996089934992	d04/323/70	1.25	244
40001171051	32301100528	0101000020E6100000F437A11001A053C05E7DE13A6BB24140	1.22099995613097989	d04/323/70	1.25	245
40001171051	32301100629	0101000020E6100000EEF0321E00A053C062AF665364B24140	1.23599994182587003	d04/323/70	1.25	248
40001171051	32301100709	0101000020E610000012F8C3CFFF9F53C02D18A60062B24140	1.24100005626678001	d04/323/70	1.25	249
40001171051	32301100719	0101000020E610000030E35C79FF9F53C088DFA8705FB24140	1.24600005149840998	d04/323/70	1.25	250
40001171051	32301100729	0101000020E6100000898A822AFF9F53C0D7CADF185DB24140	1.25100004673003995	d04/323/70	1.25	251
40001171051	32301100829	0101000020E6100000E3625639FE9F53C02DCDAD1056B24140	1.26600003242493009	d04/323/70	1.25	254
40001171051	32301100919	0101000020E610000054F0259EFD9F53C09B7BA3B151B24140	1.27600002288818004	d04/323/70	1.25	256
40001171051	32301101128	0101000020E6100000D9C00C7CFB9F53C044C93F8E41B24140	1.31099998950958008	d04/323/70	1.25	263
40001171051	32301101209	0101000020E6100000BB062230FB9F53C09EEC66463FB24140	1.31500005722046009	d04/323/70	1.25	264
40001171051	32301101229	0101000020E6100000091A3389FA9F53C0D026874F3AB24140	1.32599997520446999	d04/323/70	1.25	266
40001171051	32301101308	0101000020E610000009BE0E41FA9F53C0BF37972C38B24140	1.33000004291534002	d04/323/70	1.25	267
40001171051	32301101329	0101000020E6100000D44E289FF99F53C057DB036333B24140	1.34099996089934992	d04/323/70	1.25	269
40001171051	32301101408	0101000020E610000027F15E5AF99F53C0F920BA5631B24140	1.34599995613097989	d04/323/70	1.25	270
40001171051	32301101528	0101000020E6100000C9EE5DDEF79F53C00ACBE9FC25B24140	1.37000000476837003	d04/323/70	1.25	275
40001171051	32301101618	0101000020E6100000D557FC4BF79F53C0A26E563321B24140	1.38100004196166992	d04/323/70	1.25	277
40001171051	32301101728	0101000020E6100000B8CEBF5DF69F53C0F55D00D017B24140	1.40100002288818004	d04/323/70	1.25	281
40001171051	32301101829	0101000020E6100000F90505EFF59F53C015D742DA10B24140	1.41600000858306996	d04/323/70	1.25	284
40001171051	32301102029	0101000020E6100000AC826275F59F53C0CA56975302B24140	1.44599997997284002	d04/323/70	1.25	290
40001171051	32301102109	0101000020E6100000A04A7265F59F53C088E30A3900B24140	1.45099997520446999	d04/323/70	1.25	291
40001171051	32301102309	0101000020E6100000F4A78DEAF49F53C072480FE8F1B14140	1.48099994659424006	d04/323/70	1.25	297
40001171051	32301102408	0101000020E61000002F08F6A9F49F53C05805C5EAEAB14140	1.49500000476837003	d04/323/70	1.25	300
40001171051	32301102508	0101000020E610000095E70B6BF49F53C0AF0793E2E3B14140	1.50999999046325994	d04/323/70	1.25	303
40001171051	32301102519	0101000020E6100000D6917E56F49F53C045B9347EE1B14140	1.51499998569488992	d04/323/70	1.25	304
40001171051	32301102708	0101000020E610000006A3EDF3F39F53C0C94C58D1D5B14140	1.53999996185303001	d04/323/70	1.25	309
40001171051	32301102919	0101000020E6100000712BCE62F39F53C0067470FAC4B14140	1.57599997520446999	d04/323/70	1.25	316
40001171051	32301103219	0101000020E6100000EF4F4E59F29F53C06B5501ADAFB14140	1.62000000476837003	d04/323/70	1.25	325
40001171051	32301103318	0101000020E6100000E9A91FE5F19F53C0685485ABA8B14140	1.63499999046325994	d04/323/70	1.25	328
40001171051	32301103529	0101000020E6100000EA2285B2F09F53C0FFDA0B1698B14140	1.66999995708465998	d04/323/70	1.25	335
40001171051	32301103919	0101000020E6100000F0D187D3EE9F53C0C50490357EB14140	1.72500002384185991	d04/323/70	1.25	346
40001171051	32301104318	0101000020E61000003A2BFDDFEC9F53C01504EA2862B14140	1.78499996662140004	d04/323/70	1.25	358
40001171051	32301104509	0101000020E61000002DDF9FF7EB9F53C0FEECECD055B14140	1.81099998950958008	d04/323/70	1.25	363
40001171051	32301104518	0101000020E6100000DBB232D0EB9F53C022B59ABF53B14140	1.81500005722046009	d04/323/70	1.25	364
40001171051	32301104918	0101000020E61000004D60DFF3E89F53C01F88878B37B14140	1.875	d04/323/70	1.25	376
40001171051	32301105028	0101000020E61000007758F2C2E79F53C071A5434C2EB14140	1.8949999809265099	d04/323/70	1.25	380
40001171051	32301105308	0101000020E61000000145D1A8E59F53C06D1F4D501EB14140	1.92999994754790993	d04/323/70	1.25	387
40001171051	32301105609	0101000020E6100000742090F0E29F53C09C4940F108B14140	1.97500002384185991	d04/323/70	1.25	396
40001171051	32301105819	0101000020E6100000E6CAA0DAE09F53C0AA48E06AF8B04140	2.00999999046325994	d04/323/70	1.25	403
40001171051	32301100118	0101000020E610000056A9EA2F05A053C0A822707F89B24140	1.15499997138977006	d04/323/70	1.25	232
40001171051	32301100428	0101000020E61000005EBA490C02A053C06CB64D4C72B24140	1.20500004291534002	d04/323/70	1.25	242
40001171051	32301100609	0101000020E610000089844AB700A053C048FFCBB568B24140	1.22599995136261009	d04/323/70	1.25	246
40001171051	32301100619	0101000020E6100000B8ACC26600A053C091E5136866B24140	1.23099994659424006	d04/323/70	1.25	247
40001171051	32301101008	0101000020E61000004F1CE505FD9F53C0EAE2DB604DB24140	1.28499996662140004	d04/323/70	1.25	258
40001171051	32301101029	0101000020E610000007701F5EFC9F53C05EDE776748B24140	1.29499995708465998	d04/323/70	1.25	260
40001171051	32301101108	0101000020E6100000BA31981AFC9F53C095E3045C46B24140	1.29999995231627996	d04/323/70	1.25	261
40001171051	32301101119	0101000020E6100000BBBE6AC0FB9F53C03743609B43B24140	1.3059999942779501	d04/323/70	1.25	262
40001171051	32301101219	0101000020E6100000CED0D3DBFA9F53C0B1EDFEC23CB24140	1.32099997997284002	d04/323/70	1.25	265
40001171051	32301101319	0101000020E6100000502855ECF99F53C026378AAC35B24140	1.33599996566771995	d04/323/70	1.25	268
40001171051	32301101429	0101000020E6100000BCE1E3B8F89F53C0A10106932CB24140	1.35599994659424006	d04/323/70	1.25	272
40001171051	32301101509	0101000020E6100000584A8567F89F53C00F34FA2C2AB24140	1.36099994182587003	d04/323/70	1.25	273
40001171051	32301101519	0101000020E6100000B1F1AA18F89F53C02263A4CD27B24140	1.36600005626678001	d04/323/70	1.25	274
40001171051	32301101629	0101000020E6100000413C0103F79F53C0E4F38AA71EB24140	1.38600003719329989	d04/323/70	1.25	278
40001171051	32301101708	0101000020E61000006A7693CEF69F53C07A2F63AF1CB24140	1.38999998569488992	d04/323/70	1.25	279
40001171051	32301101809	0101000020E61000005E865A2EF69F53C08AE18F4715B24140	1.40600001811981001	d04/323/70	1.25	282
40001171051	32301101928	0101000020E6100000FFC5D8AEF59F53C0D8193AD109B24140	1.42999994754790993	d04/323/70	1.25	287
40001171051	32301102018	0101000020E6100000D6181989F59F53C0574DC6E704B24140	1.44000005722046009	d04/323/70	1.25	289
40001171051	32301102118	0101000020E6100000A0336953F59F53C0BF8C73E5FDB14140	1.45500004291534002	d04/323/70	1.25	292
40001171051	32301102128	0101000020E610000035DC3642F59F53C068D718CFFBB14140	1.46000003814696999	d04/323/70	1.25	293
40001171051	32301102208	0101000020E61000000B46802EF59F53C05CBF057EF9B14140	1.46500003337859996	d04/323/70	1.25	294
40001171051	32301102219	0101000020E6100000C3510317F59F53C00A5751CDF6B14140	1.47099995613097989	d04/323/70	1.25	295
40001171051	32301102318	0101000020E6100000BEF0EFD8F49F53C06DBF21F9EFB14140	1.48500001430511008	d04/323/70	1.25	298
40001171051	32301102329	0101000020E6100000E23C9CC0F49F53C015527E52EDB14140	1.49100005626678001	d04/323/70	1.25	299
40001171051	32301102419	0101000020E61000001EB40D92F49F53C001982144E8B14140	1.50100004673003995	d04/323/70	1.25	301
40001171051	32301102528	0101000020E61000000C1B0A44F49F53C0E8D0D84DDFB14140	1.5199999809265099	d04/323/70	1.25	305
40001171051	32301102608	0101000020E61000005AE6632DF49F53C0E9667FA0DCB14140	1.52600002288818004	d04/323/70	1.25	306
40001171051	32301102619	0101000020E6100000FAAF181AF49F53C0AECACF57DAB14140	1.52999997138977006	d04/323/70	1.25	307
40001171051	32301102628	0101000020E6100000FA980F08F49F53C0C1559E40D8B14140	1.53499996662140004	d04/323/70	1.25	308
40001171051	32301102718	0101000020E6100000484D60DFF39F53C09F635122D3B14140	1.54499995708465998	d04/323/70	1.25	310
40001171051	32301102728	0101000020E6100000A75599CEF39F53C0A0B14005D1B14140	1.54999995231627996	d04/323/70	1.25	311
40001171051	32301102809	0101000020E6100000B35F77BAF39F53C061B47D7ECEB14140	1.5559999942779501	d04/323/70	1.25	312
40001171051	32301102828	0101000020E6100000CC733392F39F53C0BCF781F5C9B14140	1.56500005722046009	d04/323/70	1.25	314
40001171051	32301103018	0101000020E61000009B4E571CF39F53C0519A722ABEB14140	1.59000003337859996	d04/323/70	1.25	319
40001171051	32301103028	0101000020E6100000421DFBFEF29F53C0116F9D7FBBB14140	1.59599995613097989	d04/323/70	1.25	320
40001171051	32301103108	0101000020E6100000B44B0AE2F29F53C095E35F15B9B14140	1.60000002384185991	d04/323/70	1.25	321
40001171051	32301103119	0101000020E6100000735C7CC0F29F53C08B6F287CB6B14140	1.60599994659424006	d04/323/70	1.25	322
40001171051	32301103409	0101000020E610000020D7868AF19F53C07C19D69EA3B14140	1.64600002765656006	d04/323/70	1.25	330
40001171051	32301103418	0101000020E610000037EB4262F19F53C0C52D3075A1B14140	1.65100002288818004	d04/323/70	1.25	331
40001171051	32301103509	0101000020E610000038781508F19F53C07A185A9D9CB14140	1.66100001335143999	d04/323/70	1.25	333
40001171051	32301103518	0101000020E6100000374A03E4F09F53C05E4D9EB29AB14140	1.66499996185303001	d04/323/70	1.25	334
40001171051	32301104009	0101000020E6100000861E317AEE9F53C0A540553B79B14140	1.73599994182587003	d04/323/70	1.25	348
40001171051	32301104018	0101000020E61000009E32ED51EE9F53C0A56032FA76B14140	1.74100005626678001	d04/323/70	1.25	349
40001171051	32301104108	0101000020E6100000631A3C02EE9F53C0CC1AAB8372B14140	1.75	d04/323/70	1.25	351
40001171051	32301104129	0101000020E61000008005D5ABED9F53C0C7CB3F9F6DB14140	1.75999999046325994	d04/323/70	1.25	353
40001171051	32301104208	0101000020E6100000B5775787ED9F53C01C188A856BB14140	1.76499998569488992	d04/323/70	1.25	354
40001171051	32301104609	0101000020E61000000BC4A16DEB9F53C0DE76A1B94EB14140	1.82599997520446999	d04/323/70	1.25	366
40001171051	32301104709	0101000020E6100000BD12EDCFEA9F53C0CA0A348E47B14140	1.84099996089934992	d04/323/70	1.25	369
40001171051	32301104728	0101000020E6100000400BAE5EEA9F53C0FBFC9C2743B14140	1.85000002384185991	d04/323/70	1.25	371
40001171051	32301104809	0101000020E6100000B10BAB1DEA9F53C0FD1C7AE640B14140	1.8550000190734901	d04/323/70	1.25	372
40001171051	32301104908	0101000020E61000006B1ACA3FE99F53C00021EDDA39B14140	1.87000000476837003	d04/323/70	1.25	375
40001171051	32301104928	0101000020E61000000C433FAEE89F53C04955247035B14140	1.87999999523162997	d04/323/70	1.25	377
40001171051	32301105008	0101000020E6100000304AD05FE89F53C01CC3521333B14140	1.88399994373321999	d04/323/70	1.25	378
40001171051	32301105018	0101000020E6100000BE918A10E89F53C076B867A730B14140	1.88999998569488992	d04/323/70	1.25	379
40001171051	32301105108	0101000020E6100000D71B107CE79F53C025FAC6212CB14140	1.89999997615814009	d04/323/70	1.25	381
40001171051	32301105208	0101000020E61000002AEFF494E69F53C04CA60A4625B14140	1.91499996185303001	d04/323/70	1.25	384
40001171051	32301105229	0101000020E610000067C526E8E59F53C090EFF73020B14140	1.9259999990463299	d04/323/70	1.25	386
40001171051	32301105418	0101000020E610000055BC9179E49F53C0B304190115B14140	1.95000004768372004	d04/323/70	1.25	391
40001171051	32301105428	0101000020E61000005C655C27E49F53C0F6894D7512B14140	1.95500004291534002	d04/323/70	1.25	392
40001171051	32301105618	0101000020E61000007FE552A6E29F53C0392EE3A606B14140	1.9800000190734901	d04/323/70	1.25	397
40001171051	32301105729	0101000020E610000039984D80E19F53C0E37CFB84FDB04140	2	d04/323/70	1.25	401
40001171051	32301105908	0101000020E61000000B8D1656E09F53C0F4D83B48F4B04140	2.01999998092651012	d04/323/70	1.25	405
40001171051	32301103208	0101000020E6100000E45C797FF29F53C0E6E03E17B2B14140	1.61600005626678001	d04/323/70	1.25	324
40001171051	32301103229	0101000020E61000004825862EF29F53C03C670B08ADB14140	1.62600004673003995	d04/323/70	1.25	326
40001171051	32301103308	0101000020E61000002594BE10F29F53C0A34C593CABB14140	1.62999999523162997	d04/323/70	1.25	327
40001171051	32301103329	0101000020E6100000EF80FCB6F19F53C0A5A6B805A6B14140	1.64100003242493009	d04/323/70	1.25	329
40001171051	32301103628	0101000020E61000009683EA30F09F53C00A40924891B14140	1.68499994277953991	d04/323/70	1.25	338
40001171051	32301103819	0101000020E6100000A3906456EF9F53C0BBFB2D4B85B14140	1.71000003814696999	d04/323/70	1.25	343
40001171051	32301103829	0101000020E6100000EB28BD25EF9F53C04647CDB282B14140	1.71599996089934992	d04/323/70	1.25	344
40001171051	32301103909	0101000020E6100000AF3E1EFAEE9F53C083F5245580B14140	1.72099995613097989	d04/323/70	1.25	345
40001171051	32301103928	0101000020E6100000DF6696A9EE9F53C014F0C6DD7BB14140	1.7300000190734901	d04/323/70	1.25	347
40001171051	32301104028	0101000020E6100000C2679027EE9F53C0E30E8A9C74B14140	1.74500000476837003	d04/323/70	1.25	350
40001171051	32301104118	0101000020E6100000335184D4ED9F53C026E2ADF36FB14140	1.75600004196166992	d04/323/70	1.25	352
40001171051	32301104219	0101000020E610000034B04456ED9F53C01D801EB468B14140	1.77100002765656006	d04/323/70	1.25	355
40001171051	32301104308	0101000020E6100000F9979306ED9F53C07FF6234564B14140	1.77999997138977006	d04/323/70	1.25	357
40001171051	32301104418	0101000020E61000008C710F53EC9F53C0EFFE78AF5AB14140	1.79999995231627996	d04/323/70	1.25	361
40001171051	32301104429	0101000020E610000069C93E23EC9F53C07445292158B14140	1.8059999942779501	d04/323/70	1.25	362
40001171051	32301104529	0101000020E610000099AC9B9CEB9F53C077499C1551B14140	1.82099997997284002	d04/323/70	1.25	365
40001171051	32301104618	0101000020E6100000C3B81B44EB9F53C0A93B05AF4CB14140	1.83000004291534002	d04/323/70	1.25	367
40001171051	32301104718	0101000020E610000064CA87A0EA9F53C0003ED3A645B14140	1.84500002861022994	d04/323/70	1.25	370
40001171051	32301104818	0101000020E6100000230CA8DCE99F53C0C2AEDCC13EB14140	1.86000001430511008	d04/323/70	1.25	373
40001171051	32301105118	0101000020E6100000B4452D28E79F53C0F639E3A029B14140	1.90499997138977006	d04/323/70	1.25	382
40001171051	32301105219	0101000020E6100000DE99643FE69F53C05FA7A2C222B14140	1.91999995708465998	d04/323/70	1.25	385
40001171051	32301105318	0101000020E6100000DE6EEE54E59F53C0B0A481C41BB14140	1.93599998950958008	d04/323/70	1.25	388
40001171051	32301105519	0101000020E6100000AF946588E39F53C0ED35F39A0DB14140	1.96599996089934992	d04/323/70	1.25	394
40001171051	32301105708	0101000020E610000051A96D1EE29F53C064496F6E02B14140	1.99000000953674006	d04/323/70	1.25	399
40001171051	32301105719	0101000020E6100000C29261CBE19F53C01914BCD7FFB04140	1.99500000476837003	d04/323/70	1.25	400
40001171051	32301105809	0101000020E6100000EC42BD2AE19F53C0DE0DB3E1FAB04140	2.00600004196166992	d04/323/70	1.25	402
40001171051	32301105828	0101000020E6100000F9AB5B98E09F53C0F98F3B5BF6B04140	2.01500010490416992	d04/323/70	1.25	404
40001171051	32301105918	0101000020E6100000AC11B00CE09F53C01340D6F8F1B04140	2.02500009536742986	d04/323/70	1.25	406
40001171051	32301105929	0101000020E6100000467A51BBDF9F53C027416E75EFB04140	2.02999997138977006	d04/323/70	1.25	407
40001171051	32301113428	0101000020E6100000A18E22C6C69F53C07B06C36FF9AF4140	2.55500006675719993	d04/323/71	1.25	512
40001171051	32301114308	0101000020E6100000659B0AA7BB9F53C044FAEDEBC0AF4140	2.68000006675719993	d04/323/71	1.25	537
40001171051	32301120008	0101000020E61000000734C7A8A19F53C060B1E1444FAF4140	2.93499994277954013	d04/323/72	1.25	588
40001171051	32301120028	0101000020E61000009C6C0377A09F53C0FE6DAA494BAF4140	2.9440000057220499	d04/323/72	1.25	590
40001171051	32301120108	0101000020E6100000A8BE98D29F9F53C010F9783249AF4140	2.94899988174437988	d04/323/72	1.25	591
40001171051	32301120119	0101000020E6100000B4E21B0A9F9F53C082305CC246AF4140	2.9549999237060498	d04/323/72	1.25	592
40001171051	32301120128	0101000020E61000006D1F4D509E9F53C08A833A9B44AF4140	2.95900011062621981	d04/323/72	1.25	593
40001171051	32301120218	0101000020E6100000DF81A6CA9C9F53C0B6CCD88640AF4140	2.97000002861022994	d04/323/72	1.25	595
40001171051	32301120228	0101000020E6100000C20F73EE9B9F53C0E6CC76853EAF4140	2.97399997711181996	d04/323/72	1.25	596
40001171051	32301120309	0101000020E6100000578DCAF29A9F53C0B896C9703CAF4140	2.98000001907348988	d04/323/72	1.25	597
40001171051	32301120319	0101000020E61000004D416D0A9A9F53C094F430B43AAF4140	2.98499989509583008	d04/323/72	1.25	598
40001171051	32301120328	0101000020E6100000EEF6B41E999F53C07180AA1B39AF4140	2.99000000953674006	d04/323/72	1.25	599
40001171051	32301120418	0101000020E6100000301D2911979F53C038D08DFA35AF4140	2.99900007247924982	d04/323/72	1.25	601
40001171051	32301120428	0101000020E61000000C4AE2F6959F53C06E8D637F34AF4140	3.00399994850159002	d04/323/72	1.25	602
40001171051	32301120518	0101000020E610000055EB0E73939F53C00587BC8A31AF4140	3.0139999389648402	d04/323/72	1.25	604
40001171051	32301120528	0101000020E6100000DE196D55929F53C07057546930AF4140	3.01900005340575994	d04/323/72	1.25	605
40001171051	32301120608	0101000020E610000009FB7612919F53C00BAC883F2FAF4140	3.02399992942810014	d04/323/72	1.25	606
40001171051	32301120619	0101000020E6100000AB0F7FA88F9F53C08FBEEE192EAF4140	3.02900004386901989	d04/323/72	1.25	607
40001171051	32301120628	0101000020E6100000A655E35B8E9F53C007F5882C2DAF4140	3.03399991989136009	d04/323/72	1.25	608
40001171051	32301120708	0101000020E6100000D036ED188D9F53C07F5935632CAF4140	3.03900003433227983	d04/323/72	1.25	609
40001171051	32301120718	0101000020E6100000711DE38A8B9F53C0854AB7802BAF4140	3.0450000762939502	d04/323/72	1.25	610
40001171051	32301120818	0101000020E6100000F769CB6F879F53C0A3B1513129AF4140	3.05999994277954013	d04/323/72	1.25	613
40001171051	32301120829	0101000020E61000003F6480FA859F53C05171773128AF4140	3.06500005722045987	d04/323/72	1.25	614
40001171051	32301120908	0101000020E6100000390609F6849F53C09E56766627AF4140	3.0690000057220499	d04/323/72	1.25	615
40001171051	32301120918	0101000020E610000069D5F896839F53C0E0794E1F26AF4140	3.07500004768371982	d04/323/72	1.25	616
40001171051	32301120928	0101000020E6100000A50AEB6B829F53C08DDD4FD724AF4140	3.0799999237060498	d04/323/72	1.25	617
40001171051	32301121019	0101000020E6100000A10ED022809F53C01943948A21AF4140	3.08999991416931019	d04/323/72	1.25	619
40001171051	32301121028	0101000020E610000042DB20497F9F53C0D887500020AF4140	3.09500002861022994	d04/323/72	1.25	620
40001171051	32301121108	0101000020E6100000E9AC60657E9F53C002B1112D1EAF4140	3.09899997711181996	d04/323/72	1.25	621
40001171051	32301121118	0101000020E6100000F5D0E39C7D9F53C01598045E1CAF4140	3.10400009155272993	d04/323/72	1.25	622
40001171051	32301121208	0101000020E6100000674A46297C9F53C09BB6DA1E18AF4140	3.11500000953674006	d04/323/72	1.25	624
40001171051	32301121228	0101000020E61000004460F6FC7A9F53C0364591FF13AF4140	3.12400007247924982	d04/323/72	1.25	626
40001171051	32301121308	0101000020E61000009FF3AED5799F53C02D13D96212AF4140	3.12899994850159002	d04/323/72	1.25	627
40001171051	32301110109	0101000020E61000005830968EDE9F53C01F5BE03CE6B04140	2.04999995231628018	d04/323/71	1.25	411
40001171051	32301110119	0101000020E610000005D61643DE9F53C03DC27AEDE3B04140	2.05500006675719993	d04/323/71	1.25	412
40001171051	32301110129	0101000020E6100000AC5F9FEFDD9F53C0C2082B5FE1B04140	2.06100010871886985	d04/323/71	1.25	413
40001171051	32301110209	0101000020E6100000EEC4F6A4DD9F53C00BEF7211DFB04140	2.06500005722045987	d04/323/71	1.25	414
40001171051	32301110228	0101000020E6100000AC4B3217DD9F53C0CC9BC3B5DAB04140	2.07500004768371982	d04/323/71	1.25	416
40001171051	32301110329	0101000020E6100000E2C0502CDC9F53C01133A083D3B04140	2.08999991416931019	d04/323/71	1.25	419
40001171051	32301110529	0101000020E610000072254C62DA9F53C02AA67796C5B04140	2.11999988555907981	d04/323/71	1.25	425
40001171051	32301110619	0101000020E61000001337B8BED99F53C0802C4487C0B04140	2.13100004196166992	d04/323/71	1.25	427
40001171051	32301110709	0101000020E6100000BA7B2535D99F53C02997C62FBCB04140	2.14000010490416992	d04/323/71	1.25	429
40001171051	32301110919	0101000020E610000068F9CB38D79F53C096FAC3E0ABB04140	2.17499995231628018	d04/323/71	1.25	436
40001171051	32301110929	0101000020E61000000F9A5DF7D69F53C01A9D989AA9B04140	2.18000006675719993	d04/323/71	1.25	437
40001171051	32301111119	0101000020E61000004BE658DED59F53C0D38B35B79DB04140	2.2049999237060498	d04/323/71	1.25	442
40001171051	32301111129	0101000020E6100000B0DC77B1D59F53C0686BE9769BB04140	2.21000003814696999	d04/323/71	1.25	443
40001171051	32301111228	0101000020E6100000D59EED2CD59F53C0DE1099A894B04140	2.22399997711181996	d04/323/71	1.25	446
40001171051	32301111419	0101000020E610000058F66E3DD49F53C0F00280BE88B04140	2.25	d04/323/71	1.25	451
40001171051	32301111518	0101000020E61000005D5A1EB5D39F53C0ED2F16E181B04140	2.2639999389648402	d04/323/71	1.25	454
40001171051	32301111619	0101000020E6100000F461AC25D39F53C069F459547AB04140	2.27999997138977006	d04/323/71	1.25	457
40001171051	32301111629	0101000020E6100000CAB4ECFFD29F53C02EB4CE5378B04140	2.28500008583068981	d04/323/71	1.25	458
40001171051	32301111709	0101000020E6100000582AB9D4D29F53C029A1AAF875B04140	2.28999996185303001	d04/323/71	1.25	459
40001171051	32301111719	0101000020E61000006A227DA4D29F53C05ABBED4273B04140	2.2950000762939502	d04/323/71	1.25	460
40001171051	32301111818	0101000020E61000003BFDA02ED29F53C016551A8C6CB04140	2.30999994277954013	d04/323/71	1.25	463
40001171051	32301111828	0101000020E610000042D47D00D29F53C0B2DD98F969B04140	2.31500005722045987	d04/323/71	1.25	464
40001171051	32301112009	0101000020E6100000126A8654D19F53C0B7D3D68860B04140	2.33500003814696999	d04/323/71	1.25	468
40001171051	32301112219	0101000020E610000054A4671FD09F53C01370BEC74FB04140	2.36999988555907981	d04/323/71	1.25	475
40001171051	32301112229	0101000020E61000000178FAF7CF9F53C07FFED6A94DB04140	2.375	d04/323/71	1.25	476
40001171051	32301112309	0101000020E6100000C58D5BCCCF9F53C0A46A60504BB04140	2.38000011444092019	d04/323/71	1.25	477
40001171051	32301112319	0101000020E6100000D7851F9CCF9F53C093F139C148B04140	2.38499999046325994	d04/323/71	1.25	478
40001171051	32301112429	0101000020E610000042E0EDE6CE9F53C00328A14F3FB04140	2.40499997138977006	d04/323/71	1.25	482
40001171051	32301112609	0101000020E610000043FA9232CE9F53C07F96F8ED35B04140	2.42499995231628018	d04/323/71	1.25	486
40001171051	32301112619	0101000020E6100000256EBA0ACE9F53C0EC2411D033B04140	2.43000006675719993	d04/323/71	1.25	487
40001171051	32301112629	0101000020E6100000F7A402DDCD9F53C0F21BCB6031B04140	2.43499994277954013	d04/323/71	1.25	488
40001171051	32301112709	0101000020E61000007FFED6A9CD9F53C07D3958A42EB04140	2.44000005722045987	d04/323/71	1.25	489
40001171051	32301112909	0101000020E61000005021B2A3CC9F53C05A1EB5D320B04140	2.47000002861022994	d04/323/71	1.25	495
40001171051	32301113019	0101000020E61000005C1723B7CB9F53C000B0952B17B04140	2.4909999370575	d04/323/71	1.25	499
40001171051	32301113218	0101000020E61000005D7C1BACC99F53C0F504D37A09B04140	2.51999998092651012	d04/323/71	1.25	505
40001171051	32301113308	0101000020E6100000F95A86EEC89F53C0B0AC342905B04140	2.52900004386901989	d04/323/71	1.25	507
40001171051	32301113418	0101000020E61000006473D53CC79F53C09689C7EAFBAF4140	2.54900002479553001	d04/323/71	1.25	511
40001171051	32301113508	0101000020E6100000CA83995BC69F53C0A5A54D30F7AF4140	2.55999994277954013	d04/323/71	1.25	513
40001171051	32301113609	0101000020E610000018C85812C59F53C09D9FE238F0AF4140	2.57500004768371982	d04/323/71	1.25	516
40001171051	32301113629	0101000020E610000055596F2FC49F53C064F5FD8AEBAF4140	2.58500003814696999	d04/323/71	1.25	518
40001171051	32301113909	0101000020E610000074C3A519C19F53C06CA7F79EDBAF4140	2.61999988555907981	d04/323/71	1.25	525
40001171051	32301114208	0101000020E61000002EC72B10BD9F53C04CA4349BC7AF4140	2.66499996185303001	d04/323/71	1.25	534
40001171051	32301114318	0101000020E61000001D1D5723BB9F53C0D4A6A091BEAF4140	2.68499994277954013	d04/323/71	1.25	538
40001171051	32301114328	0101000020E6100000EEF77AADBA9F53C07CF1457BBCAF4140	2.68899989128113015	d04/323/71	1.25	539
40001171051	32301114429	0101000020E610000001248914B99F53C026F26E76B5AF4140	2.7049999237060498	d04/323/71	1.25	542
40001171051	32301114509	0101000020E610000083054191B89F53C09E8A6544B3AF4140	2.71000003814696999	d04/323/71	1.25	543
40001171051	32301114609	0101000020E6100000A86E2EFEB69F53C0259B06A0ACAF4140	2.72499990463257014	d04/323/71	1.25	546
40001171051	32301114619	0101000020E6100000A8B6E56DB69F53C061495E42AAAF4140	2.73000001907348988	d04/323/71	1.25	547
40001171051	32301114629	0101000020E610000091D3D7F3B59F53C0BCC8A942A8AF4140	2.73499989509583008	d04/323/71	1.25	548
40001171051	32301114709	0101000020E610000015B58F70B59F53C005DD0319A6AF4140	2.74000000953674006	d04/323/71	1.25	549
40001171051	32301115009	0101000020E6100000820761C9B09F53C0FD1B0F1192AF4140	2.78500008583068981	d04/323/71	1.25	558
40001171051	32301115018	0101000020E6100000CF5F8D58B09F53C0455E7B0B90AF4140	2.78999996185303001	d04/323/71	1.25	559
40001171051	32301115209	0101000020E61000003D9281F2AD9F53C015472FB484AF4140	2.81399989128113015	d04/323/71	1.25	564
40001171051	32301115219	0101000020E6100000BE73396FAD9F53C0E2815C3D82AF4140	2.81999993324280007	d04/323/71	1.25	565
40001171051	32301115318	0101000020E6100000C6C37B0EAC9F53C0434651B17BAF4140	2.83400011062621981	d04/323/71	1.25	568
40001171051	32301115518	0101000020E6100000F7AFAC34A99F53C0FE3A26416EAF4140	2.86500000953674006	d04/323/71	1.25	574
40001171051	32301115529	0101000020E6100000B636E8A6A89F53C01641ADB36BAF4140	2.86999988555907981	d04/323/71	1.25	575
40001171051	32301115618	0101000020E61000007A4FE5B4A79F53C0F562CD6D67AF4140	2.88000011444092019	d04/323/71	1.25	577
40001171051	32301115628	0101000020E61000007BAEA536A79F53C0A8B7504365AF4140	2.8840000629425	d04/323/71	1.25	578
40001171051	32301115729	0101000020E61000005E5617A6A59F53C0CF91A68B5EAF4140	2.90000009536742986	d04/323/71	1.25	581
40001171051	32301115818	0101000020E61000005E1498A9A49F53C03D9CC0745AAF4140	2.90899991989136009	d04/323/71	1.25	583
40001171051	32301115928	0101000020E61000004EE08C50A29F53C02F0D688E51AF4140	2.92899990081787021	d04/323/71	1.25	587
40001171051	32301110029	0101000020E610000070CE88D2DE9F53C02412E04FE8B04140	2.0450000762939502	d04/323/71	1.25	410
40001171051	32301110308	0101000020E6100000A1CE26D1DC9F53C067AE788FD8B04140	2.0799999237060498	d04/323/71	1.25	417
40001171051	32301110318	0101000020E610000006973380DC9F53C09F29CF17D6B04140	2.08400011062621981	d04/323/71	1.25	418
40001171051	32301110409	0101000020E6100000F58A02D8DB9F53C0303E16ECD0B04140	2.09599995613098011	d04/323/71	1.25	420
40001171051	32301110609	0101000020E61000009010E50BDA9F53C07F3A79ECC2B04140	2.12599992752075018	d04/323/71	1.25	426
40001171051	32301110629	0101000020E6100000BAD7497DD99F53C0F7F24C79BEB04140	2.13499999046325994	d04/323/71	1.25	428
40001171051	32301110719	0101000020E6100000B50309E5D89F53C0E89903A9B9B04140	2.14599990844727007	d04/323/71	1.25	430
40001171051	32301110809	0101000020E610000032C9C859D89F53C0024A9E46B5B04140	2.15499997138977006	d04/323/71	1.25	432
40001171051	32301110829	0101000020E610000086F8D1BAD79F53C02F51BD35B0B04140	2.16599988937378019	d04/323/71	1.25	434
40001171051	32301110909	0101000020E610000044DB3175D79F53C08974E4EDADB04140	2.1700000762939502	d04/323/71	1.25	435
40001171051	32301111009	0101000020E6100000C35BD6B3D69F53C0571DDE18A7B04140	2.18600010871886985	d04/323/71	1.25	438
40001171051	32301111019	0101000020E6100000865A2E76D69F53C0F9D85DA0A4B04140	2.19000005722045987	d04/323/71	1.25	439
40001171051	32301111029	0101000020E6100000CEF28645D69F53C036E3D98AA2B04140	2.19499993324280007	d04/323/71	1.25	440
40001171051	32301111318	0101000020E6100000F88E75CCD49F53C0F203FCBF8FB04140	2.23499989509583008	d04/323/71	1.25	448
40001171051	32301111328	0101000020E61000001CC418A2D49F53C09A4EA1A98DB04140	2.24000000953674006	d04/323/71	1.25	449
40001171051	32301111428	0101000020E6100000946DE00ED49F53C027ACE86A86B04140	2.25500011444092019	d04/323/71	1.25	452
40001171051	32301111508	0101000020E6100000B8A283E4D39F53C0FE7A2A4C84B04140	2.2590000629425	d04/323/71	1.25	453
40001171051	32301111529	0101000020E6100000F3D4D97FD39F53C0FACF9A1F7FB04140	2.26999998092651012	d04/323/71	1.25	455
40001171051	32301111609	0101000020E610000005CD9D4FD39F53C055979D8F7CB04140	2.27600002288818004	d04/323/71	1.25	456
40001171051	32301111729	0101000020E610000018F60F7DD29F53C0AFD9250571B04140	2.29999995231628018	d04/323/71	1.25	461
40001171051	32301111918	0101000020E610000012DDB3AED19F53C0AE18648165B04140	2.32500004768371982	d04/323/71	1.25	466
40001171051	32301112018	0101000020E6100000A1DF5229D19F53C0F3812E2B5EB04140	2.33999991416931019	d04/323/71	1.25	469
40001171051	32301112129	0101000020E610000048F6AD7BD09F53C0CEF8BEB854B04140	2.35999989509583008	d04/323/71	1.25	473
40001171051	32301112209	0101000020E61000008F8E064BD09F53C083C30B2252B04140	2.3659999370575	d04/323/71	1.25	474
40001171051	32301112329	0101000020E610000007DCA96FCF9F53C0E1DC706946B04140	2.39000010490416992	d04/323/71	1.25	479
40001171051	32301112509	0101000020E610000090943EBECE9F53C0DBF6E2303DB04140	2.41000008583068981	d04/323/71	1.25	483
40001171051	32301112519	0101000020E610000061CB8690CE9F53C0D6E3BED53AB04140	2.41499996185303001	d04/323/71	1.25	484
40001171051	32301112529	0101000020E610000014A4085FCE9F53C0DDAC664238B04140	2.4200000762939502	d04/323/71	1.25	485
40001171051	32301112719	0101000020E610000079B4CC7DCD9F53C0A3A5E14A2CB04140	2.44499993324280007	d04/323/71	1.25	490
40001171051	32301112728	0101000020E610000026885F56CD9F53C0A3F3D02D2AB04140	2.45000004768371982	d04/323/71	1.25	491
40001171051	32301112808	0101000020E6100000203E552ACD9F53C0C85F5AD427B04140	2.4549999237060498	d04/323/71	1.25	492
40001171051	32301112918	0101000020E6100000389AC871CC9F53C04F06A2821EB04140	2.47399997711181996	d04/323/71	1.25	496
40001171051	32301113029	0101000020E61000001BFA8271CB9F53C0ADD117E714B04140	2.49499988555907981	d04/323/71	1.25	500
40001171051	32301113108	0101000020E61000009E205624CB9F53C0A3E716BA12B04140	2.5	d04/323/71	1.25	501
40001171051	32301113129	0101000020E6100000F1214D61CA9F53C0282092C60DB04140	2.50999999046325994	d04/323/71	1.25	503
40001171051	32301113209	0101000020E6100000CE4B6A0DCA9F53C00622D5C10BB04140	2.51500010490416992	d04/323/71	1.25	504
40001171051	32301113328	0101000020E6100000C9AB730CC89F53C06B9C4D4700B04140	2.53999996185303001	d04/323/71	1.25	509
40001171051	32301113408	0101000020E610000005DEC9A7C79F53C019ECE126FEAF4140	2.5450000762939502	d04/323/71	1.25	510
40001171051	32301113518	0101000020E61000004D9363FCC59F53C0AD263E2DF5AF4140	2.56399989128113015	d04/323/71	1.25	514
40001171051	32301113529	0101000020E61000008997A773C59F53C0FB592C45F2AF4140	2.56999993324280007	d04/323/71	1.25	515
40001171051	32301113619	0101000020E61000001E43119CC49F53C0271994C4EDAF4140	2.5799999237060498	d04/323/71	1.25	517
40001171051	32301113729	0101000020E61000002B2515D7C29F53C0192E1796E4AF4140	2.59999990463257014	d04/323/71	1.25	521
40001171051	32301113809	0101000020E6100000D89C8367C29F53C0D98C7857E2AF4140	2.60500001907348988	d04/323/71	1.25	522
40001171051	32301113819	0101000020E6100000DE2E4503C29F53C0B78EBB52E0AF4140	2.60999989509583008	d04/323/71	1.25	523
40001171051	32301113829	0101000020E61000008BA6B393C19F53C00BADF314DEAF4140	2.61500000953674006	d04/323/71	1.25	524
40001171051	32301114008	0101000020E61000002127A7D1BF9F53C099E26025D5AF4140	2.6340000629425	d04/323/71	1.25	528
40001171051	32301114028	0101000020E610000068D9A4ECBE9F53C0BF9CD9AED0AF4140	2.64400005340575994	d04/323/71	1.25	530
40001171051	32301114228	0101000020E61000006A58422DBC9F53C024C1655FC3AF4140	2.67400002479553001	d04/323/71	1.25	536
40001171051	32301114418	0101000020E61000000CFDB8A2B99F53C078FEFEDEB7AF4140	2.70000004768371982	d04/323/71	1.25	541
40001171051	32301114519	0101000020E61000002A61B719B89F53C04C080C48B1AF4140	2.71499991416931019	d04/323/71	1.25	544
40001171051	32301114719	0101000020E6100000273A26E6B49F53C0887FD8D2A3AF4140	2.74499988555907981	d04/323/71	1.25	550
40001171051	32301114809	0101000020E6100000099AE0E5B39F53C073D9E89C9FAF4140	2.75500011444092019	d04/323/71	1.25	552
40001171051	32301114829	0101000020E61000009FE925C6B29F53C01CBA34D99AAF4140	2.76500010490416992	d04/323/71	1.25	554
40001171051	32301114908	0101000020E610000063BA6B64B29F53C06A8BC63599AF4140	2.76900005340575994	d04/323/71	1.25	555
40001171051	32301115028	0101000020E61000008EFDD1DCAF9F53C0467E58CA8DAF4140	2.7950000762939502	d04/323/71	1.25	560
40001171051	32301115118	0101000020E610000083B174F4AE9F53C07EA3C27D89AF4140	2.80399990081787021	d04/323/71	1.25	562
40001171051	32301115229	0101000020E61000003D5002F6AC9F53C0E2A139FC7FAF4140	2.82500004768371982	d04/323/71	1.25	566
40001171051	32301115309	0101000020E610000013471E88AC9F53C0D8E54AF37DAF4140	2.8299999237060498	d04/323/71	1.25	567
40001171051	32301115419	0101000020E610000014DA28A1AA9F53C047A6E8ED74AF4140	2.84899997711181996	d04/323/71	1.25	571
40001171051	32301115509	0101000020E6100000EA18FCA2A99F53C0377BB14170AF4140	2.85999989509583008	d04/323/71	1.25	573
40001171051	32301115719	0101000020E61000007C551D28A69F53C0337FF1B160AF4140	2.89499998092651012	d04/323/71	1.25	580
40001171051	32301115828	0101000020E610000095E5DA06A49F53C068DF26ED57AF4140	2.91499996185303001	d04/323/71	1.25	584
40001171051	32301084718	0101000020E6100000665133FF43A053C04E44BFB67EB44140	0.0460000000894070019	d04/323/68	1.25	10
40001171051	32301084728	0101000020E6100000B3A6C35444A053C0B571C45A7CB44140	0.0509999990463256975	d04/323/68	1.25	11
40001171051	32301084828	0101000020E6100000E26CDF4845A053C070DDDE7F75B44140	0.0659999996423721036	d04/323/68	1.25	14
40001171051	32301085118	0101000020E61000007094BC3A47A053C0C71EEBF362B44140	0.105999998748302002	d04/323/68	1.25	22
40001171051	32301085818	0101000020E610000029E55A5947A053C06405BF0D31B44140	0.210999995470046997	d04/323/68	1.25	43
40001171051	32301090309	0101000020E6100000E26CDF4845A053C03438A51710B44140	0.280999988317490013	d04/323/69	1.25	57
40001171051	32301090508	0101000020E6100000A227655243A053C05EBA490C02B44140	0.312000006437302024	d04/323/69	1.25	63
40001171051	32301090529	0101000020E6100000A2FCEE6742A053C0BACF3B5FFDB34140	0.321999996900558028	d04/323/69	1.25	65
40001171051	32301091109	0101000020E610000036DB262639A053C0D272A087DAB34140	0.402000010013579989	d04/323/69	1.25	81
40001171051	32301091328	0101000020E6100000031F285C34A053C00490DAC4C9B34140	0.439999997615813987	d04/323/69	1.25	89
40001171051	32301091429	0101000020E6100000E6536C7132A053C0195B632BC3B34140	0.456000000238419023	d04/323/69	1.25	92
40001171051	32301091528	0101000020E6100000055C46A030A053C03FED0104BDB34140	0.470999985933304	d04/323/69	1.25	95
40001171051	32301091628	0101000020E61000003057F5A82EA053C0D291B7B7B6B34140	0.486000001430510975	d04/323/69	1.25	98
40001171051	32301092119	0101000020E61000008837216324A053C023F36D6699B34140	0.555999994277953991	d04/323/69	1.25	112
40001171051	32301092229	0101000020E6100000771DBB5521A053C04572E8E390B34140	0.577000021934509055	d04/323/69	1.25	116
40001171051	32301092328	0101000020E6100000F1CCBA351FA053C0E8AFA1E58AB34140	0.591000020503998025	d04/323/69	1.25	119
40001171051	32301093028	0101000020E6100000BC74385F11A053C0826A285A5EB34140	0.695999979972839022	d04/323/69	1.25	140
40001171051	32301093419	0101000020E61000004E78AE940AA053C076267ED646B34140	0.750999987125396951	d04/323/69	1.25	151
40001171051	32301093718	0101000020E610000086B4215A06A053C01B9540EF32B34140	0.795000016689300981	d04/323/69	1.25	160
40001171051	32301093809	0101000020E61000009D3EA7C505A053C08F90DCF52DB34140	0.805999994277953991	d04/323/69	1.25	162
40001171051	32301093918	0101000020E610000098254BF704A053C0176536C824B34140	0.825999975204467995	d04/323/69	1.25	166
40001171051	32301094009	0101000020E61000001B35159804A053C0AEAC7EB61FB34140	0.836000025272369052	d04/323/69	1.25	168
40001171051	32301094529	0101000020E61000004C60298103A053C0CE801F7AF7B24140	0.921000003814697044	d04/323/69	1.25	185
40001171051	32301094929	0101000020E6100000C830822106A053C05F13E346DBB24140	0.981000006198882946	d04/323/69	1.25	197
40001171051	32301095019	0101000020E6100000A357039406A053C0EC0896D9D6B24140	0.990999996662140004	d04/323/69	1.25	199
40001171051	32301095318	0101000020E6100000C63EB78608A053C08BA6B393C1B24140	1.03600001335143999	d04/323/69	1.25	208
40001171051	32301095328	0101000020E6100000AE2AFBAE08A053C0D48CFB45BFB24140	1.04100000858306996	d04/323/69	1.25	209
40001171051	32301095618	0101000020E610000024FF380609A053C0E3AB787EACB24140	1.08000004291534002	d04/323/69	1.25	217
40001171051	32301095828	0101000020E610000020178B9507A053C08C13BAA69BB24140	1.11600005626678001	d04/323/69	1.25	224
40001171051	32301095908	0101000020E610000086F6A05607A053C0C418479B99B24140	1.12000000476837003	d04/323/69	1.25	225
40001171051	32301100009	0101000020E61000003EEEB66606A053C09E6FFA6992B24140	1.13499999046325994	d04/323/70	1.25	228
40001171051	32301100019	0101000020E6100000F198261106A053C07BE706F98FB24140	1.14100003242493009	d04/323/70	1.25	229
40001171051	32301100929	0101000020E610000020DD6344FD9F53C031FF32294FB24140	1.28100001811981001	d04/323/70	1.25	257
40001171051	32301101418	0101000020E61000003FD7080EF99F53C0128365112FB24140	1.35000002384185991	d04/323/70	1.25	271
40001171051	32301101908	0101000020E6100000E8B11CD7F59F53C063C279820EB24140	1.41999995708465998	d04/323/70	1.25	285
40001171051	32301102429	0101000020E6100000CA9EA97CF49F53C02504ABEAE5B14140	1.50600004196166992	d04/323/70	1.25	302
40001171051	32301103428	0101000020E610000032A13836F19F53C0979B5E189FB14140	1.65499997138977006	d04/323/70	1.25	332
40001171051	32301103608	0101000020E6100000AE38E686F09F53C0D77B3BD395B14140	1.67499995231627996	d04/323/70	1.25	336
40001171051	32301103709	0101000020E610000068BA3203F09F53C0B10001C68EB14140	1.69000005722046009	d04/323/70	1.25	339
40001171051	32301103728	0101000020E6100000D9A326B0EF9F53C0184EE3288AB14140	1.70000004768372004	d04/323/70	1.25	341
40001171051	32301104628	0101000020E61000005833D70EEB9F53C087B3113E4AB14140	1.83500003814696999	d04/323/70	1.25	368
40001171051	32301110519	0101000020E61000008AC33EA6DA9F53C005DEC9A7C7B04140	2.1159999370575	d04/323/71	1.25	424
40001171051	32301110729	0101000020E61000005688A29BD89F53C007019E59B7B04140	2.15100002288818004	d04/323/71	1.25	431
40001171051	32301110819	0101000020E6100000DF6E490ED89F53C0C27AEDE3B2B04140	2.16000008583068981	d04/323/71	1.25	433
40001171051	32301111808	0101000020E61000009B4AF553D29F53C0804754A86EB04140	2.30500006675719993	d04/323/71	1.25	462
40001171051	32301111909	0101000020E61000009AA9B5D5D19F53C09688A6A267B04140	2.31999993324280007	d04/323/71	1.25	465
40001171051	32301112108	0101000020E6100000A6881DD7D09F53C0DE7F1AAD59B04140	2.34899997711181996	d04/323/71	1.25	471
40001171051	32301112419	0101000020E610000072A9A514CF9F53C0C67949AD41B04140	2.40100002288818004	d04/323/71	1.25	481
40001171051	32301112818	0101000020E610000097715303CD9F53C0C9AD49B725B04140	2.45900011062621981	d04/323/71	1.25	493
40001171051	32301113318	0101000020E6100000E793707CC89F53C0D5EAABAB02B04140	2.53500008583068981	d04/323/71	1.25	508
40001171051	32301114018	0101000020E6100000DFDBF467BF9F53C0942B6112D3AF4140	2.6389999389648402	d04/323/71	1.25	529
40001171051	32301114118	0101000020E6100000639236FABD9F53C0AA6CB30CCCAF4140	2.65400004386901989	d04/323/71	1.25	532
40001171051	32301114408	0101000020E6100000361DA622BA9F53C000660811BAAF4140	2.69499993324280007	d04/323/71	1.25	540
40001171051	32301114729	0101000020E6100000B63CC560B49F53C096D7A5A1A1AF4140	2.75	d04/323/71	1.25	551
40001171051	32301114928	0101000020E610000088DBA161B19F53C0BAC4ECC094AF4140	2.77900004386901989	d04/323/71	1.25	557
40001171051	32301115128	0101000020E6100000B394D16DAE9F53C050E3DEFC86AF4140	2.80999994277954013	d04/323/71	1.25	563
40001171051	32301115328	0101000020E6100000671A03A1AB9F53C0F7C8E6AA79AF4140	2.83899998664856001	d04/323/71	1.25	569
40001171051	32301115409	0101000020E61000003DE30C0FAB9F53C05262D7F676AF4140	2.84500002861022994	d04/323/71	1.25	570
40001171051	32301115428	0101000020E610000091B6F127AA9F53C03084F7B072AF4140	2.85400009155272993	d04/323/71	1.25	572
40001171051	32301115609	0101000020E61000009837E224A89F53C0A1E8706369AF4140	2.875	d04/323/71	1.25	576
40001171051	32301120508	0101000020E610000072D06FA9949F53C0229A2FE532AF4140	3.0090000629425	d04/323/72	1.25	603
40001171051	32301121009	0101000020E61000008F2A792B819F53C035B22B2D23AF4140	3.08500003814696999	d04/323/72	1.25	618
40001171051	32301084418	0101000020E61000000852CEBC41A053C073BC02D193B44140	0.00100000004749745	d04/323/68	1.25	1
40001171051	32301084519	0101000020E61000007FDE54A442A053C0DC7179628CB44140	0.017000000923872001	d04/323/68	1.25	4
40001171051	32301084608	0101000020E6100000D73DC3E542A053C07FA9FAF087B44140	0.0270000007003546004	d04/323/68	1.25	6
40001171051	32301084628	0101000020E6100000C6A1235E43A053C09959958E83B44140	0.0359999984502792011	d04/323/68	1.25	8
40001171051	32301085109	0101000020E6100000A5063F1647A053C073D2A00D65B44140	0.101000003516674	d04/323/68	1.25	21
40001171051	32301085418	0101000020E61000003AAC70CB47A053C04314387E4DB44140	0.15199999511241899	d04/323/68	1.25	31
40001171051	32301085508	0101000020E61000007651F4C047A053C0AB8F2C0549B44140	0.160999998450279014	d04/323/68	1.25	33
40001171051	32301085729	0101000020E61000000599AE7147A053C067CAF38535B44140	0.202000007033348	d04/323/68	1.25	41
40001171051	32301090008	0101000020E6100000D06EE30547A053C0CF84268925B44140	0.236000001430511003	d04/323/69	1.25	48
40001171051	32301090028	0101000020E6100000C4F1D7BF46A053C0F053556820B44140	0.246000006794930004	d04/323/69	1.25	50
40001171051	32301090318	0101000020E6100000F54D9A0645A053C03A8B83F00DB44140	0.286000013351439986	d04/323/69	1.25	58
40001171051	32301090418	0101000020E6100000B966971444A053C0C1E3DBBB06B44140	0.300999999046326017	d04/323/69	1.25	61
40001171051	32301090819	0101000020E610000022D1BAFC3DA053C0B7216BB2EBB34140	0.361999988555907981	d04/323/69	1.25	73
40001171051	32301091418	0101000020E6100000099D7C1F33A053C036B05582C5B34140	0.451000005006789995	d04/323/69	1.25	91
40001171051	32301091809	0101000020E6100000FCF0E2B32BA053C0783705E8ADB34140	0.507000029087066983	d04/323/69	1.25	102
40001171051	32301091818	0101000020E6100000D2A2E30F2BA053C0BAA29410ACB34140	0.510999977588654009	d04/323/69	1.25	103
40001171051	32301092318	0101000020E6100000A9ECAAF61FA053C0CF1FE4068DB34140	0.586000025272369052	d04/323/69	1.25	118
40001171051	32301092408	0101000020E61000005C3E92921EA053C0BAD5181989B34140	0.596000015735625999	d04/323/69	1.25	120
40001171051	32301092828	0101000020E610000043ED123015A053C0DB28FC636BB34140	0.666000008583068959	d04/323/69	1.25	134
40001171051	32301093409	0101000020E61000005A51DE220BA053C0F32785D448B34140	0.745999991893767977	d04/323/69	1.25	150
40001171051	32301093608	0101000020E610000061342BDB07A053C064E025DD3BB34140	0.776000022888184038	d04/323/69	1.25	156
40001171051	32301094318	0101000020E610000046E80C3103A053C0A89BD54C08B34140	0.884999990463256947	d04/323/69	1.25	178
40001171051	32301094329	0101000020E6100000CF6FF32103A053C0FD5DE9C605B34140	0.890999972820281982	d04/323/69	1.25	179
40001171051	32301094409	0101000020E610000094B3661A03A053C07ACDBC6603B34140	0.896000027656554954	d04/323/69	1.25	180
40001171051	32301094909	0101000020E61000009E1095A105A053C064624E2BE0B24140	0.971000015735625999	d04/323/69	1.25	195
40001171051	32301095718	0101000020E61000007357659508A053C0465C001AA5B24140	1.09599995613097989	d04/323/69	1.25	220
40001171051	32301095809	0101000020E61000009114EC1A08A053C05B4F6331A0B24140	1.10599994659424006	d04/323/69	1.25	222
40001171051	32301100029	0101000020E6100000CEC243BD05A053C01299A8948DB24140	1.14600002765656006	d04/323/70	1.25	230
40001171051	32301100109	0101000020E61000000307B47405A053C04DA3247F8BB24140	1.15100002288818004	d04/323/70	1.25	231
40001171051	32301100128	0101000020E6100000F2118CDE04A053C02792431F87B24140	1.15999996662140004	d04/323/70	1.25	233
40001171051	32301100409	0101000020E6100000E10B93A902A053C0EDF88AC976B24140	1.19599997997284002	d04/323/70	1.25	240
40001171051	32301100808	0101000020E6100000548EC9E2FE9F53C04359F8FA5AB24140	1.25600004196166992	d04/323/70	1.25	252
40001171051	32301100818	0101000020E6100000B956D691FE9F53C07F07509D58B24140	1.25999999046325994	d04/323/70	1.25	253
40001171051	32301100908	0101000020E6100000D8E54AF3FD9F53C01D0CD01154B24140	1.27100002765656006	d04/323/70	1.25	255
40001171051	32301101019	0101000020E610000085494CABFC9F53C0D436B4B74AB24140	1.29100000858306996	d04/323/70	1.25	259
40001171051	32301101608	0101000020E6100000B6555A90F79F53C0474B2F7B23B24140	1.37600004673003995	d04/323/70	1.25	276
40001171051	32301101718	0101000020E6100000D055A98FF69F53C081F80A1C1AB24140	1.39600002765656006	d04/323/70	1.25	280
40001171051	32301101818	0101000020E6100000A635BC0FF69F53C0A3CD716E13B24140	1.40999996662140004	d04/323/70	1.25	283
40001171051	32301101919	0101000020E6100000D65D34BFF59F53C0D09849D40BB24140	1.4259999990463299	d04/323/70	1.25	286
40001171051	32301102009	0101000020E6100000D52F229BF59F53C009628F3F07B24140	1.43599998950958008	d04/323/70	1.25	288
40001171051	32301102908	0101000020E6100000AEFE637CF39F53C09A9DA0A8C7B14140	1.57000005245209007	d04/323/70	1.25	315
40001171051	32301102929	0101000020E61000002A37514BF39F53C0F5566EB3C2B14140	1.58000004291534002	d04/323/70	1.25	317
40001171051	32301103718	0101000020E61000009710BDD6EF9F53C0BEFCA94C8CB14140	1.69500005245209007	d04/323/70	1.25	340
40001171051	32301104229	0101000020E61000000A038530ED9F53C073CC689A66B14140	1.77600002288818004	d04/323/70	1.25	356
40001171051	32301105128	0101000020E6100000366C00DBE69F53C027DE5C5727B14140	1.90999996662140004	d04/323/70	1.25	383
40001171051	32301105508	0101000020E6100000D36A48DCE39F53C0D52F6C2810B14140	1.96000003814696999	d04/323/70	1.25	393
40001171051	32301110429	0101000020E61000005F13E346DB9F53C0E5B27680CCB04140	2.10500001907348988	d04/323/71	1.25	422
40001171051	32301110509	0101000020E610000072DD94F2DA9F53C051B758F6C9B04140	2.1110000610351598	d04/323/71	1.25	423
40001171051	32301111109	0101000020E610000039EE940ED69F53C00823F609A0B04140	2.20099997520446999	d04/323/71	1.25	441
40001171051	32301111308	0101000020E6100000F3B798FAD49F53C00E59EE1692B04140	2.23000001907348988	d04/323/71	1.25	447
40001171051	32301111409	0101000020E6100000FE203768D49F53C030760CD98AB04140	2.24499988555907981	d04/323/71	1.25	450
40001171051	32301112028	0101000020E6100000E272BC02D19F53C00C12EC095CB04140	2.34500002861022994	d04/323/71	1.25	470
40001171051	32301112409	0101000020E61000005490FA46CF9F53C0BAABB24A44B04140	2.39499998092651012	d04/323/71	1.25	480
40001171051	32301112928	0101000020E6100000C1F39C3ECC9F53C00960144E1CB04140	2.47900009155272993	d04/323/71	1.25	497
40001171051	32301113228	0101000020E6100000BD283053C99F53C02B0A606F07B04140	2.52500009536742986	d04/323/71	1.25	506
40001171051	32301113919	0101000020E61000008B7B3DA9C09F53C0EA44DD62D9AF4140	2.625	d04/323/71	1.25	526
40001171051	32301114128	0101000020E6100000B7065B91BD9F53C0C22A830FCAAF4140	2.65899991989136009	d04/323/71	1.25	533
40001171051	32301114218	0101000020E61000006AE27899BC9F53C0F4C0C760C5AF4140	2.6700000762939502	d04/323/71	1.25	535
40001171051	32301114918	0101000020E6100000C32165D5B19F53C01D8425C396AF4140	2.77500009536742986	d04/323/71	1.25	556
40001171051	32301115109	0101000020E6100000F380C355AF9F53C0953B7D4E8BAF4140	2.79999995231628018	d04/323/71	1.25	561
40001171051	32301115909	0101000020E6100000F34CD477A39F53C02D7189C855AF4140	2.9200000762939502	d04/323/71	1.25	585
40001171051	32301120209	0101000020E6100000B6E8537D9D9F53C02568DD5042AF4140	2.96499991416931019	d04/323/72	1.25	594
40001171051	32301120728	0101000020E6100000848E0C288A9F53C00DEC42BD2AAF4140	3.04900002479553001	d04/323/72	1.25	611
40001171051	32301102228	0101000020E6100000713C9F01F59F53C00D491C68F4B14140	1.47500002384185991	d04/323/70	1.25	296
40001171051	32301102818	0101000020E6100000604A13A5F39F53C03F2C8A0DCCB14140	1.56099998950958008	d04/323/70	1.25	313
40001171051	32301103008	0101000020E6100000D721ED35F39F53C0B5E3E198C0B14140	1.58500003814696999	d04/323/70	1.25	318
40001171051	32301103129	0101000020E6100000254C07A1F29F53C0DF8D603EB4B14140	1.61099994182587003	d04/323/70	1.25	323
40001171051	32301103618	0101000020E6100000328DCB5DF09F53C0DECE19AC93B14140	1.67999994754790993	d04/323/70	1.25	337
40001171051	32301103808	0101000020E6100000FCD8C985EF9F53C0CC7454DA87B14140	1.70500004291534002	d04/323/70	1.25	342
40001171051	32301104328	0101000020E61000004002DAB1EC9F53C076FEEDB25FB14140	1.78999996185303001	d04/323/70	1.25	359
40001171051	32301104409	0101000020E610000092BB197FEC9F53C0B95510035DB14140	1.79499995708465998	d04/323/70	1.25	360
40001171051	32301104829	0101000020E610000023997A82E99F53C0F39A0DE83BB14140	1.86600005626678001	d04/323/70	1.25	374
40001171051	32301105329	0101000020E6100000F6549808E59F53C0528E137019B14140	1.94000005722046009	d04/323/70	1.25	389
40001171051	32301105408	0101000020E610000014573AC4E49F53C0A7DA5D5617B14140	1.94500005245209007	d04/323/70	1.25	390
40001171051	32301105529	0101000020E6100000809D9B36E39F53C02BB638190BB14140	1.97099995613097989	d04/323/70	1.25	395
40001171051	32301105628	0101000020E61000001B65FD66E29F53C0632992AF04B14140	1.98500001430511008	d04/323/70	1.25	398
40001171051	32301110009	0101000020E610000088DFA870DF9F53C098A66329EDB04140	2.03500008583068981	d04/323/71	1.25	408
40001171051	32301110019	0101000020E6100000F9C89C1DDF9F53C005AB459FEAB04140	2.04099988937378019	d04/323/71	1.25	409
40001171051	32301110219	0101000020E61000006AE6DA61DD9F53C0C576F700DDB04140	2.06999993324280007	d04/323/71	1.25	415
40001171051	32301110419	0101000020E61000004311418BDB9F53C055AA9F92CEB04140	2.09999990463257014	d04/323/71	1.25	421
40001171051	32301111209	0101000020E610000022F47D82D59F53C094DC611399B04140	2.21499991416931019	d04/323/71	1.25	444
40001171051	32301111218	0101000020E6100000A5486359D59F53C0E828ACF996B04140	2.22000002861022994	d04/323/71	1.25	445
40001171051	32301111928	0101000020E6100000A1528083D19F53C05607E52263B04140	2.3299999237060498	d04/323/71	1.25	467
40001171051	32301112119	0101000020E610000084E04CA7D09F53C068CBB91457B04140	2.35500001907348988	d04/323/71	1.25	472
40001171051	32301112829	0101000020E6100000618CA3CDCC9F53C0B3D30FEA22B04140	2.46499991416931019	d04/323/71	1.25	494
40001171051	32301113008	0101000020E6100000D3D457FCCB9F53C099B0A2AB19B04140	2.48499989509583008	d04/323/71	1.25	498
40001171051	32301113118	0101000020E6100000150F39C7CA9F53C0FEDC2B4E10B04140	2.50500011444092019	d04/323/71	1.25	502
40001171051	32301113709	0101000020E6100000EFAA07CCC39F53C0AC376A85E9AF4140	2.58999991416931019	d04/323/71	1.25	519
40001171051	32301113719	0101000020E610000014848659C39F53C0605EDB36E7AF4140	2.59500002861022994	d04/323/71	1.25	520
40001171051	32301113929	0101000020E6100000688E5143C09F53C0F1C5CD5FD7AF4140	2.63000011444092019	d04/323/71	1.25	527
40001171051	32301114529	0101000020E610000085C3C194B79F53C083DF8618AFAF4140	2.72000002861022994	d04/323/71	1.25	545
40001171051	32301114819	0101000020E61000003E822C55B39F53C05C89E53B9DAF4140	2.7590000629425	d04/323/71	1.25	553
40001171051	32301115709	0101000020E61000001CD71AA5A69F53C074F27DCC62AF4140	2.89000010490416992	d04/323/71	1.25	579
40001171051	32301115809	0101000020E6100000943E6315A59F53C036BFAB2F5CAF4140	2.90499997138977006	d04/323/71	1.25	582
40001171051	32301115918	0101000020E61000008F705AF0A29F53C0C3AC61D053AF4140	2.92400002479553001	d04/323/71	1.25	586
40001171051	32301120018	0101000020E610000091036509A19F53C04ABD022C4DAF4140	2.93899989128113015	d04/323/72	1.25	589
40001171051	32301120409	0101000020E61000002943B005989F53C0BB1E3B5E37AF4140	2.99399995803833008	d04/323/72	1.25	600
40001171051	32301120809	0101000020E6100000736E6EA7889F53C0CC165AE729AF4140	3.05500006675719993	d04/323/72	1.25	612
40001171051	32301121128	0101000020E6100000BA2EFCE07C9F53C0D4528A671AAF4140	3.10899996757507013	d04/323/72	1.25	623
40001171051	32301121218	0101000020E6100000CDB62E907B9F53C0A109B9F715AF4140	3.11899995803833008	d04/323/72	1.25	625
40001224096	33600384827	0101000020E610000001289023E78753C0624F96B5A8AF4140	2.53299999237060991	d04/336/38	1.95999999999999996	2
40001745064	31300315228	0101000020E6100000E24F9EC3467953C04402FC091DF14140	1.58800005912781006	d04/313/31	1.95999999999999996	1
40001717096	32500201714	0101000020E6100000CE37A27B567553C026AC8DB113AE4140	1.97800004482268998	d04/325/20	1.25	3
40001516033	29800012904	0101000020E6100000601DC70F955D53C08F1E1A715CF64140	1.0509999990463299	d04/298/1	1.95999999999999996	1
40001339051	34301535911	0101000020E6100000D12CBFC2B89C53C04520A8644ABD4140	0.998000025749206987	d04/343/113	1.25	1
40001521042	29700553101	0101000020E610000036EE28290B7553C051C9EF236D3E4240	0.0829999968409537991	d04/297/55	1.95999999999999996	1
40001145098	16300221524	0101000020E6100000C0649934FC8653C0D2A0B2ABDADB4140	1.09800004959106001	d04/163/22	1.25	1
40001545096	33500481628	0101000020E610000081481A37107E53C0564C0059E3BD4140	0.742999970912933017	d04/335/48	1.25	1
40001140051	34200012201	0101000020E610000006234097BA9A53C07EBD67C988AB4140	0.620000004768372026	d04/342/1	1.25	1
40001131098	42500034620	0101000020E61000002F55C4445E8A53C071164042DEDE4140	1.8680000305175799	d04/425/3	1.25	1
40001507064	30901293205	0101000020E610000096896C31897C53C00BCE8536A5134240	1.37800002098083008	d04/309/89	1.95999999999999996	1
40001933096	34100155616	0101000020E6100000BEEEBE74A47F53C0C1FD254E93A14140	2.57200002670287997	d04/341/15	1.25	1
40001344033	31401474309	0101000020E6100000E8ED19D3DD6353C0A5BA25DEA6EF4140	0.363999992609023992	d04/314/107	1.95999999999999996	1
40001144051	34200034707	0101000020E6100000FF902342489853C0654BFB8B45AC4140	0.876999974250793013	d04/342/3	1.25	1
40001613033	31501391922	0101000020E6100000CF5037AB196753C0AC521FED24E34140	0.00400000018998981043	d04/315/99	1.95999999999999996	1
40001315064	31101314311	0101000020E6100000E65DF580798953C0C6AA9C514EF84140	0.0399999991059303006	d04/311/91	1.95999999999999996	1
40001739096	34000182102	0101000020E610000049E47107207653C0287C5B559B9B4140	2.80299997329712003	d04/340/18	1.25	1
40001720051	35501085529	0101000020E6100000BB59CD84F09253C00EC1CCD2A9D04140	10.8380002975463992	d04/355/68	1.25	3
40001720051	35501091329	0101000020E61000004F948444DA9253C01620C0D831D04140	11.1079998016356996	d04/355/69	1.25	4
\.


--
-- Data for Name: rs_core_userannotationsummary; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_userannotationsummary (id, round_number, total, annotation_id, user_id, presence) FROM stdin;
\.


--
-- Data for Name: rs_core_userimageannotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_userimageannotation (id, presence, "timestamp", comment, annotation_id, image_id, user_id, front_view, left_view, right_view) FROM stdin;
\.


--
-- Data for Name: rs_core_userimageannotation_flags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_userimageannotation_flags (id, userimageannotation_id, annotationflag_id) FROM stdin;
\.


--
-- Data for Name: rs_core_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_userprofile (id, email, organization, years_of_service, user_id) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 21, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 28, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 46, true);


--
-- Name: django_redirect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_redirect_id_seq', 1, false);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 3, true);


--
-- Name: rs_core_aiimageannotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_aiimageannotation_id_seq', 12579147, true);


--
-- Name: rs_core_annotationset_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_annotationset_flags_id_seq', 4, true);


--
-- Name: rs_core_holdouttestinfo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_holdouttestinfo_id_seq', 925, true);


--
-- Name: rs_core_userannotationsummary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userannotationsummary_id_seq', 1, false);


--
-- Name: rs_core_userimageannotation_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userimageannotation_flags_id_seq', 24, true);


--
-- Name: rs_core_userimageannotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userimageannotation_id_seq', 3585, true);


--
-- Name: rs_core_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userprofile_id_seq', 20, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_redirect django_redirect_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_redirect
    ADD CONSTRAINT django_redirect_pkey PRIMARY KEY (id);


--
-- Name: django_redirect django_redirect_site_id_old_path_ac5dd16b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_redirect
    ADD CONSTRAINT django_redirect_site_id_old_path_ac5dd16b_uniq UNIQUE (site_id, old_path);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: rs_core_aiimageannotation rs_core_aiimageannotation_image_id_annotation_id_de79cd29_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_aiimageannotation
    ADD CONSTRAINT rs_core_aiimageannotation_image_id_annotation_id_de79cd29_uniq UNIQUE (image_id, annotation_id);


--
-- Name: rs_core_aiimageannotation rs_core_aiimageannotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_aiimageannotation
    ADD CONSTRAINT rs_core_aiimageannotation_pkey PRIMARY KEY (id);


--
-- Name: rs_core_annotationflag rs_core_annotationflag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationflag
    ADD CONSTRAINT rs_core_annotationflag_pkey PRIMARY KEY (title);


--
-- Name: rs_core_annotationset_flags rs_core_annotationset_fl_annotationset_id_annotat_8f0e7f92_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset_flags
    ADD CONSTRAINT rs_core_annotationset_fl_annotationset_id_annotat_8f0e7f92_uniq UNIQUE (annotationset_id, annotationflag_id);


--
-- Name: rs_core_annotationset_flags rs_core_annotationset_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset_flags
    ADD CONSTRAINT rs_core_annotationset_flags_pkey PRIMARY KEY (id);


--
-- Name: rs_core_annotationset rs_core_annotationset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset
    ADD CONSTRAINT rs_core_annotationset_pkey PRIMARY KEY (name);


--
-- Name: rs_core_holdouttestinfo rs_core_holdouttestinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_holdouttestinfo
    ADD CONSTRAINT rs_core_holdouttestinfo_pkey PRIMARY KEY (id);


--
-- Name: rs_core_routeimage rs_core_routeimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_routeimage
    ADD CONSTRAINT rs_core_routeimage_pkey PRIMARY KEY (image_base_name);


--
-- Name: rs_core_userannotationsummary rs_core_userannotationsummary_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userannotationsummary
    ADD CONSTRAINT rs_core_userannotationsummary_pkey PRIMARY KEY (id);


--
-- Name: rs_core_userimageannotation rs_core_userimageannotat_user_id_image_id_annotat_bc441fbd_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation
    ADD CONSTRAINT rs_core_userimageannotat_user_id_image_id_annotat_bc441fbd_uniq UNIQUE (user_id, image_id, annotation_id);


--
-- Name: rs_core_userimageannotation_flags rs_core_userimageannotat_userimageannotation_id_a_6d10d5a8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation_flags
    ADD CONSTRAINT rs_core_userimageannotat_userimageannotation_id_a_6d10d5a8_uniq UNIQUE (userimageannotation_id, annotationflag_id);


--
-- Name: rs_core_userimageannotation_flags rs_core_userimageannotation_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation_flags
    ADD CONSTRAINT rs_core_userimageannotation_flags_pkey PRIMARY KEY (id);


--
-- Name: rs_core_userimageannotation rs_core_userimageannotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation
    ADD CONSTRAINT rs_core_userimageannotation_pkey PRIMARY KEY (id);


--
-- Name: rs_core_userprofile rs_core_userprofile_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userprofile
    ADD CONSTRAINT rs_core_userprofile_email_key UNIQUE (email);


--
-- Name: rs_core_userprofile rs_core_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userprofile
    ADD CONSTRAINT rs_core_userprofile_pkey PRIMARY KEY (id);


--
-- Name: rs_core_userprofile rs_core_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userprofile
    ADD CONSTRAINT rs_core_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_redirect_old_path_c6cc94d3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_redirect_old_path_c6cc94d3 ON public.django_redirect USING btree (old_path);


--
-- Name: django_redirect_old_path_c6cc94d3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_redirect_old_path_c6cc94d3_like ON public.django_redirect USING btree (old_path varchar_pattern_ops);


--
-- Name: django_redirect_site_id_c3e37341; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_redirect_site_id_c3e37341 ON public.django_redirect USING btree (site_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: rs_core_aii_annotat_a4271a_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aii_annotat_a4271a_idx ON public.rs_core_aiimageannotation USING btree (annotation_id, uncertainty_group, uncertainty_measure DESC, image_id);


--
-- Name: rs_core_aii_image_i_d04ca4_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aii_image_i_d04ca4_idx ON public.rs_core_aiimageannotation USING btree (image_id, annotation_id);


--
-- Name: rs_core_aii_uncerta_217593_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aii_uncerta_217593_idx ON public.rs_core_aiimageannotation USING btree (uncertainty_group);


--
-- Name: rs_core_aiimageannotation_annotation_id_5dd15dc7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aiimageannotation_annotation_id_5dd15dc7 ON public.rs_core_aiimageannotation USING btree (annotation_id);


--
-- Name: rs_core_aiimageannotation_annotation_id_5dd15dc7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aiimageannotation_annotation_id_5dd15dc7_like ON public.rs_core_aiimageannotation USING btree (annotation_id varchar_pattern_ops);


--
-- Name: rs_core_aiimageannotation_image_id_efbb458d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aiimageannotation_image_id_efbb458d ON public.rs_core_aiimageannotation USING btree (image_id);


--
-- Name: rs_core_aiimageannotation_image_id_efbb458d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_aiimageannotation_image_id_efbb458d_like ON public.rs_core_aiimageannotation USING btree (image_id varchar_pattern_ops);


--
-- Name: rs_core_annotationflag_title_795975fb_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationflag_title_795975fb_like ON public.rs_core_annotationflag USING btree (title varchar_pattern_ops);


--
-- Name: rs_core_annotationset_flags_annotationflag_id_a59b281a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationset_flags_annotationflag_id_a59b281a ON public.rs_core_annotationset_flags USING btree (annotationflag_id);


--
-- Name: rs_core_annotationset_flags_annotationflag_id_a59b281a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationset_flags_annotationflag_id_a59b281a_like ON public.rs_core_annotationset_flags USING btree (annotationflag_id varchar_pattern_ops);


--
-- Name: rs_core_annotationset_flags_annotationset_id_e11e56d2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationset_flags_annotationset_id_e11e56d2 ON public.rs_core_annotationset_flags USING btree (annotationset_id);


--
-- Name: rs_core_annotationset_flags_annotationset_id_e11e56d2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationset_flags_annotationset_id_e11e56d2_like ON public.rs_core_annotationset_flags USING btree (annotationset_id varchar_pattern_ops);


--
-- Name: rs_core_annotationset_name_281c6acf_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_annotationset_name_281c6acf_like ON public.rs_core_annotationset USING btree (name varchar_pattern_ops);


--
-- Name: rs_core_holdouttestinfo_annotation_id_5bc95c56; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_annotation_id_5bc95c56 ON public.rs_core_holdouttestinfo USING btree (annotation_id);


--
-- Name: rs_core_holdouttestinfo_annotation_id_5bc95c56_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_annotation_id_5bc95c56_like ON public.rs_core_holdouttestinfo USING btree (annotation_id varchar_pattern_ops);


--
-- Name: rs_core_holdouttestinfo_image_id_edfe1e99; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_image_id_edfe1e99 ON public.rs_core_holdouttestinfo USING btree (image_id);


--
-- Name: rs_core_holdouttestinfo_image_id_edfe1e99_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_image_id_edfe1e99_like ON public.rs_core_holdouttestinfo USING btree (image_id varchar_pattern_ops);


--
-- Name: rs_core_holdouttestinfo_in_balance_set_b6fca210; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_in_balance_set_b6fca210 ON public.rs_core_holdouttestinfo USING btree (in_balance_set);


--
-- Name: rs_core_holdouttestinfo_presence_3719c49a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_presence_3719c49a ON public.rs_core_holdouttestinfo USING btree (presence);


--
-- Name: rs_core_holdouttestinfo_round_number_e7397902; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_holdouttestinfo_round_number_e7397902 ON public.rs_core_holdouttestinfo USING btree (round_number);


--
-- Name: rs_core_routeimage_image_base_name_a7b8781b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_routeimage_image_base_name_a7b8781b_like ON public.rs_core_routeimage USING btree (image_base_name varchar_pattern_ops);


--
-- Name: rs_core_routeimage_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_routeimage_location_id ON public.rs_core_routeimage USING gist (location);


--
-- Name: rs_core_routeimage_route_id_ad5a35c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_routeimage_route_id_ad5a35c3 ON public.rs_core_routeimage USING btree (route_id);


--
-- Name: rs_core_routeimage_route_id_ad5a35c3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_routeimage_route_id_ad5a35c3_like ON public.rs_core_routeimage USING btree (route_id varchar_pattern_ops);


--
-- Name: rs_core_use_image_i_b448f4_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_use_image_i_b448f4_idx ON public.rs_core_userimageannotation USING btree (image_id, annotation_id);


--
-- Name: rs_core_use_user_id_629c3d_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_use_user_id_629c3d_idx ON public.rs_core_userimageannotation USING btree (user_id, annotation_id, presence, image_id);


--
-- Name: rs_core_userannotationsummary_annotation_id_ef492547; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userannotationsummary_annotation_id_ef492547 ON public.rs_core_userannotationsummary USING btree (annotation_id);


--
-- Name: rs_core_userannotationsummary_annotation_id_ef492547_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userannotationsummary_annotation_id_ef492547_like ON public.rs_core_userannotationsummary USING btree (annotation_id varchar_pattern_ops);


--
-- Name: rs_core_userannotationsummary_presence_1e2c4a87; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userannotationsummary_presence_1e2c4a87 ON public.rs_core_userannotationsummary USING btree (presence);


--
-- Name: rs_core_userannotationsummary_user_id_9562dbb4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userannotationsummary_user_id_9562dbb4 ON public.rs_core_userannotationsummary USING btree (user_id);


--
-- Name: rs_core_userimageannotat_annotationflag_id_cfa140bd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotat_annotationflag_id_cfa140bd_like ON public.rs_core_userimageannotation_flags USING btree (annotationflag_id varchar_pattern_ops);


--
-- Name: rs_core_userimageannotatio_userimageannotation_id_f202c898; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotatio_userimageannotation_id_f202c898 ON public.rs_core_userimageannotation_flags USING btree (userimageannotation_id);


--
-- Name: rs_core_userimageannotation_annotation_id_1a04caa8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_annotation_id_1a04caa8 ON public.rs_core_userimageannotation USING btree (annotation_id);


--
-- Name: rs_core_userimageannotation_annotation_id_1a04caa8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_annotation_id_1a04caa8_like ON public.rs_core_userimageannotation USING btree (annotation_id varchar_pattern_ops);


--
-- Name: rs_core_userimageannotation_flags_annotationflag_id_cfa140bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_flags_annotationflag_id_cfa140bd ON public.rs_core_userimageannotation_flags USING btree (annotationflag_id);


--
-- Name: rs_core_userimageannotation_image_id_5dd6b7a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_image_id_5dd6b7a5 ON public.rs_core_userimageannotation USING btree (image_id);


--
-- Name: rs_core_userimageannotation_image_id_5dd6b7a5_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_image_id_5dd6b7a5_like ON public.rs_core_userimageannotation USING btree (image_id varchar_pattern_ops);


--
-- Name: rs_core_userimageannotation_user_id_b4b6ae62; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userimageannotation_user_id_b4b6ae62 ON public.rs_core_userimageannotation USING btree (user_id);


--
-- Name: rs_core_userprofile_email_aba8c941_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rs_core_userprofile_email_aba8c941_like ON public.rs_core_userprofile USING btree (email varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_redirect django_redirect_site_id_c3e37341_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_redirect
    ADD CONSTRAINT django_redirect_site_id_c3e37341_fk_django_site_id FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_aiimageannotation rs_core_aiimageannot_annotation_id_5dd15dc7_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_aiimageannotation
    ADD CONSTRAINT rs_core_aiimageannot_annotation_id_5dd15dc7_fk_rs_core_a FOREIGN KEY (annotation_id) REFERENCES public.rs_core_annotationset(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_aiimageannotation rs_core_aiimageannot_image_id_efbb458d_fk_rs_core_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_aiimageannotation
    ADD CONSTRAINT rs_core_aiimageannot_image_id_efbb458d_fk_rs_core_r FOREIGN KEY (image_id) REFERENCES public.rs_core_routeimage(image_base_name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_annotationset_flags rs_core_annotationse_annotationflag_id_a59b281a_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset_flags
    ADD CONSTRAINT rs_core_annotationse_annotationflag_id_a59b281a_fk_rs_core_a FOREIGN KEY (annotationflag_id) REFERENCES public.rs_core_annotationflag(title) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_annotationset_flags rs_core_annotationse_annotationset_id_e11e56d2_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_annotationset_flags
    ADD CONSTRAINT rs_core_annotationse_annotationset_id_e11e56d2_fk_rs_core_a FOREIGN KEY (annotationset_id) REFERENCES public.rs_core_annotationset(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_holdouttestinfo rs_core_holdouttesti_annotation_id_5bc95c56_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_holdouttestinfo
    ADD CONSTRAINT rs_core_holdouttesti_annotation_id_5bc95c56_fk_rs_core_a FOREIGN KEY (annotation_id) REFERENCES public.rs_core_annotationset(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_holdouttestinfo rs_core_holdouttesti_image_id_edfe1e99_fk_rs_core_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_holdouttestinfo
    ADD CONSTRAINT rs_core_holdouttesti_image_id_edfe1e99_fk_rs_core_r FOREIGN KEY (image_id) REFERENCES public.rs_core_routeimage(image_base_name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userannotationsummary rs_core_userannotati_annotation_id_ef492547_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userannotationsummary
    ADD CONSTRAINT rs_core_userannotati_annotation_id_ef492547_fk_rs_core_a FOREIGN KEY (annotation_id) REFERENCES public.rs_core_annotationset(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userannotationsummary rs_core_userannotationsummary_user_id_9562dbb4_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userannotationsummary
    ADD CONSTRAINT rs_core_userannotationsummary_user_id_9562dbb4_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userimageannotation rs_core_userimageann_annotation_id_1a04caa8_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation
    ADD CONSTRAINT rs_core_userimageann_annotation_id_1a04caa8_fk_rs_core_a FOREIGN KEY (annotation_id) REFERENCES public.rs_core_annotationset(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userimageannotation_flags rs_core_userimageann_annotationflag_id_cfa140bd_fk_rs_core_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation_flags
    ADD CONSTRAINT rs_core_userimageann_annotationflag_id_cfa140bd_fk_rs_core_a FOREIGN KEY (annotationflag_id) REFERENCES public.rs_core_annotationflag(title) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userimageannotation rs_core_userimageann_image_id_5dd6b7a5_fk_rs_core_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation
    ADD CONSTRAINT rs_core_userimageann_image_id_5dd6b7a5_fk_rs_core_r FOREIGN KEY (image_id) REFERENCES public.rs_core_routeimage(image_base_name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userimageannotation_flags rs_core_userimageann_userimageannotation__f202c898_fk_rs_core_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation_flags
    ADD CONSTRAINT rs_core_userimageann_userimageannotation__f202c898_fk_rs_core_u FOREIGN KEY (userimageannotation_id) REFERENCES public.rs_core_userimageannotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userimageannotation rs_core_userimageannotation_user_id_b4b6ae62_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userimageannotation
    ADD CONSTRAINT rs_core_userimageannotation_user_id_b4b6ae62_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rs_core_userprofile rs_core_userprofile_user_id_8af177c7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_userprofile
    ADD CONSTRAINT rs_core_userprofile_user_id_8af177c7_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

