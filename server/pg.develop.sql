--
-- PostgreSQL database dump
--

-- Dumped from database version 11.9 (Debian 11.9-1.pgdg90+1)
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

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
DROP INDEX public.rs_core_use_user_id_629c3d_idx;
DROP INDEX public.rs_core_use_image_i_b448f4_idx;
DROP INDEX public.rs_core_routeimage_route_id_ad5a35c3_like;
DROP INDEX public.rs_core_routeimage_route_id_ad5a35c3;
DROP INDEX public.rs_core_routeimage_location_id;
DROP INDEX public.rs_core_routeimage_image_base_name_a7b8781b_like;
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
ALTER TABLE ONLY public.rs_core_routeimage DROP CONSTRAINT rs_core_routeimage_pkey;
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
DROP TABLE public.rs_core_routeimage;
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
    presence boolean NOT NULL,
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
-- Name: rs_core_routeimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rs_core_routeimage (
    route_id character varying(20) NOT NULL,
    image_base_name character varying(15) NOT NULL,
    location public.geometry(Point,4326) NOT NULL,
    mile_post double precision,
    image_path character varying(100) NOT NULL
);


ALTER TABLE public.rs_core_routeimage OWNER TO postgres;

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
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$VxU2TdJOvJ2N$PH/qimirElGmCGYgR4gzOp8jEH+JmakdRSGBHKmoLOM=	2021-02-17 22:25:22.69876+00	t	admin			hongyi@renci.org	t	t	2020-10-18 19:38:21.120339+00
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
r40a1xfep6zpdwu177j4zqqosu7qsfoe	.eJxVjEEOwiAQRe_C2pCBQgGX7nsGMjOgVA0kpV0Z765NutDtf-_9l4i4rSVuPS9xTuIslDj9boT8yHUH6Y711iS3ui4zyV2RB-1yaik_L4f7d1Cwl2-dzVUrcqxIJzAOAg3euzQCI4yGLXtGr63PEFR2RANr7UgTOwKwwYv3B9xkN5I:1lCVG6:sqdxE6HQauP6LDcl11GZXRUC8k1UfTvRfT0gt1_n9U8	2021-03-03 22:25:22.710118+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	dotdsidev.renci.org	dotdsidev
2	dotdsi.renci.org	dotdsi
\.


--
-- Data for Name: rs_core_aiimageannotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_aiimageannotation (id, presence, certainty, "timestamp", annotation_id, image_id, uncertainty_measure, uncertainty_group) FROM stdin;
12576503	f	0	2021-01-17 16:24:07.900363+00	guardrail	16100362400	0	1
12576564	f	0	2021-01-17 16:24:10.280222+00	guardrail	16300221524	0	1
12576598	f	0	2021-01-17 16:24:11.398758+00	guardrail	22000431902	0	1
12576504	f	0	2021-01-17 16:24:07.968471+00	guardrail	16401215429	0	1
12576511	f	0	2021-01-17 16:24:08.401896+00	guardrail	30000385923	0	1
12576542	f	0	2021-01-17 16:24:09.662419+00	guardrail	30200062407	0	1
12576510	f	0	2021-01-17 16:24:08.386159+00	guardrail	30001205208	0	1
12576513	f	0	2021-01-17 16:24:08.49309+00	guardrail	35801471221	0	5
12576517	f	0	2021-01-17 16:24:08.669198+00	guardrail	35701451127	0	5
12576512	f	0	2021-01-17 16:24:08.47814+00	guardrail	35801404307	0	5
12576519	f	0	2021-01-17 16:24:08.719591+00	guardrail	35700310103	0	5
12576515	t	1	2021-01-17 16:24:08.628195+00	guardrail	35701420526	0	5
12576529	f	0	2021-01-17 16:24:09.210941+00	guardrail	34400391623	0	4
12576584	f	0	2021-01-17 16:24:10.998879+00	guardrail	34800560920	0	5
12576525	t	1	2021-01-17 16:24:09.102737+00	guardrail	34400300325	0	4
12576527	f	0	2021-01-17 16:24:09.136392+00	guardrail	34400592320	0	5
12576526	f	0	2021-01-17 16:24:09.11984+00	guardrail	34400303125	0	4
12576520	f	0	2021-01-17 16:24:08.8536+00	guardrail	34400370205	0	4
12576521	f	0	2021-01-17 16:24:08.910893+00	guardrail	34401091323	0	5
12576524	f	0	2021-01-17 16:24:09.08646+00	guardrail	34400403205	0	4
12576607	f	0	2021-01-17 16:24:11.591993+00	guardrail	32400230908	0	3
12576534	t	1	2021-01-17 16:24:09.453749+00	guardrail	35501541503	0	5
12576518	f	0	2021-01-17 16:24:08.694697+00	guardrail	35700040920	0	5
12576541	f	0	2021-01-17 16:24:09.645187+00	guardrail	35501154425	0	5
12576540	f	0	2021-01-17 16:24:09.627977+00	guardrail	35501070209	0	5
12576536	f	0	2021-01-17 16:24:09.561643+00	guardrail	35501091329	0	5
12576533	f	0	2021-01-17 16:24:09.369345+00	guardrail	35501425510	0	5
12576543	t	1	2021-01-17 16:24:09.678123+00	guardrail	30200201401	0	1
12576575	f	0	2021-01-17 16:24:10.596479+00	guardrail	30500211224	0	2
12576546	f	0	2021-01-17 16:24:09.779488+00	guardrail	29901322813	0	1
12576549	t	1	2021-01-17 16:24:09.829217+00	guardrail	29901341804	0	1
12576548	t	1	2021-01-17 16:24:09.811699+00	guardrail	29901113229	0	1
12576545	f	0	2021-01-17 16:24:09.712683+00	guardrail	29901194629	0	1
12576508	f	0	2021-01-17 16:24:08.218746+00	guardrail	30000081915	0	1
12576522	t	1	2021-01-17 16:24:09.020335+00	guardrail	34400230020	0	4
12576552	f	0	2021-01-17 16:24:09.921127+00	guardrail	34201521024	0	4
12576554	f	0	2021-01-17 16:24:10.012988+00	guardrail	34201070010	0	4
12576587	t	1	2021-01-17 16:24:11.090174+00	guardrail	34100155616	0	4
12576505	f	0	2021-01-17 16:24:07.984238+00	guardrail	16400161125	0	1
12576559	f	0	2021-01-17 16:24:10.196002+00	guardrail	16301184725	0	1
12576561	t	1	2021-01-17 16:24:10.230214+00	guardrail	16301023018	0	1
12576562	f	0	2021-01-17 16:24:10.24693+00	guardrail	16300504528	0	1
12576563	f	0	2021-01-17 16:24:10.26296+00	guardrail	16300222214	0	1
12576539	f	0	2021-01-17 16:24:09.612365+00	guardrail	35500575109	0	5
12576547	f	0	2021-01-17 16:24:09.796117+00	guardrail	29901051509	0	1
12576571	t	1	2021-01-17 16:24:10.496527+00	guardrail	29701443127	0	1
12576568	f	0	2021-01-17 16:24:10.388705+00	guardrail	29701315222	0	1
12576569	t	1	2021-01-17 16:24:10.447258+00	guardrail	29700553621	0	1
12576567	t	1	2021-01-17 16:24:10.330452+00	guardrail	29701532424	0	1
12576574	t	1	2021-01-17 16:24:10.571478+00	guardrail	30502041402	0	2
12576582	f	0	2021-01-17 16:24:10.965531+00	guardrail	31101034815	0	2
12576577	f	0	2021-01-17 16:24:10.689732+00	guardrail	30500414711	0	2
12576573	f	0	2021-01-17 16:24:10.546187+00	guardrail	30501412415	0	2
12576576	t	1	2021-01-17 16:24:10.664457+00	guardrail	30500483409	0	2
12576557	f	0	2021-01-17 16:24:10.129692+00	guardrail	33301120926	0	3
12576532	f	0	2021-01-17 16:24:09.353379+00	guardrail	31200424207	0	2
12576581	f	0	2021-01-17 16:24:10.949674+00	guardrail	31101314311	0	2
12576566	f	0	2021-01-17 16:24:10.313116+00	guardrail	34901293001	0	5
12576585	t	1	2021-01-17 16:24:11.015907+00	guardrail	34801052114	0	5
12576583	t	1	2021-01-17 16:24:10.981654+00	guardrail	34801083120	0	5
12576590	f	0	2021-01-17 16:24:11.174652+00	guardrail	34100221828	0	4
12576591	f	0	2021-01-17 16:24:11.19029+00	guardrail	34101115407	0	4
12576589	f	0	2021-01-17 16:24:11.157931+00	guardrail	34100321517	0	4
12576556	f	0	2021-01-17 16:24:10.112232+00	guardrail	34200012201	0	4
12576570	t	1	2021-01-17 16:24:10.471244+00	guardrail	29700553101	0	1
12576595	t	1	2021-01-17 16:24:11.291201+00	guardrail	22001512810	0	1
12576596	t	1	2021-01-17 16:24:11.307364+00	guardrail	22001132920	0	1
12576597	f	0	2021-01-17 16:24:11.383237+00	guardrail	22000433201	0	1
12576602	t	1	2021-01-17 16:24:11.466578+00	guardrail	15901333701	0	0
12576599	f	0	2021-01-17 16:24:11.4161+00	guardrail	15901240029	0	0
12576500	t	1	2021-01-17 16:24:07.809711+00	guardrail	16100350429	0	0
12576578	f	0	2021-01-17 16:24:10.714252+00	guardrail	33000215519	0	3
12576611	t	1	2021-01-17 16:24:11.657931+00	guardrail	32400313308	0	3
12576606	t	1	2021-01-17 16:24:11.574846+00	guardrail	32400355028	0	3
12576610	t	1	2021-01-17 16:24:11.642432+00	guardrail	32400325018	0	3
12576507	t	0.5	2021-01-17 16:24:08.202626+00	guardrail	30001011809	50	0
12576514	t	0.510000000000000009	2021-01-17 16:24:08.553411+00	guardrail	35801340023	49	0
12576560	t	0.650000000000000022	2021-01-17 16:24:10.212789+00	guardrail	16301022617	35	0
12576588	t	0.650000000000000022	2021-01-17 16:24:11.107545+00	guardrail	34100282611	35	0
12576528	f	0.340000000000000024	2021-01-17 16:24:09.194095+00	guardrail	34400595700	34	0
12576538	t	0.689999999999999947	2021-01-17 16:24:09.595028+00	guardrail	35501325128	31	0
12576608	t	0.859999999999999987	2021-01-17 16:24:11.607876+00	guardrail	32400271918	14	0
12576501	t	0.869999999999999996	2021-01-17 16:24:07.825958+00	guardrail	16100345009	13	0
12576612	t	0.890000000000000013	2021-01-17 16:24:11.675529+00	guardrail	30401244412	10	0
12576592	t	0.910000000000000031	2021-01-17 16:24:11.241797+00	guardrail	36001265813	8	0
12576553	t	0.939999999999999947	2021-01-17 16:24:09.995592+00	guardrail	34200034707	6	0
12576603	t	0.959999999999999964	2021-01-17 16:24:11.48358+00	guardrail	15901324811	4	0
12576550	f	0.0500000000000000028	2021-01-17 16:24:09.846172+00	guardrail	35401573022	4	0
12576594	t	0.989999999999999991	2021-01-17 16:24:11.274284+00	guardrail	22000175809	1	0
12576601	t	1	2021-01-17 16:24:11.448899+00	guardrail	15901091226	0	0
12576615	f	0	2021-01-17 16:24:11.807716+00	guardrail	30400480726	0	1
12576618	f	0	2021-01-17 16:24:11.857857+00	guardrail	30400531116	0	1
12576675	f	0	2021-01-17 16:24:13.661728+00	guardrail	30600235410	0	2
12576617	t	1	2021-01-17 16:24:11.842203+00	guardrail	30401232201	0	2
12576622	f	0	2021-01-17 16:24:11.925014+00	guardrail	29601521527	0	1
12576619	f	0	2021-01-17 16:24:11.875195+00	guardrail	29601422623	0	1
12576572	f	0	2021-01-17 16:24:10.521526+00	guardrail	29701261012	0	1
12576625	f	0	2021-01-17 16:24:11.974616+00	guardrail	33800504204	0	4
12576671	t	1	2021-01-17 16:24:13.552824+00	guardrail	33901182607	0	4
12576633	f	0	2021-01-17 16:24:12.209771+00	guardrail	35100530209	0	5
12576537	f	0	2021-01-17 16:24:09.577904+00	guardrail	35501085529	0	5
12576628	t	1	2021-01-17 16:24:12.04256+00	guardrail	35101182013	0	5
12576627	f	0	2021-01-17 16:24:12.017401+00	guardrail	35100180614	0	5
12576629	t	1	2021-01-17 16:24:12.059114+00	guardrail	35101145524	0	5
12576632	f	0	2021-01-17 16:24:12.157894+00	guardrail	35101051713	0	5
12576647	f	0	2021-01-17 16:24:12.660457+00	guardrail	32500201714	0	3
12576634	f	0	2021-01-17 16:24:12.234932+00	guardrail	31901543714	0	3
12576635	f	0	2021-01-17 16:24:12.259949+00	guardrail	31901522512	0	3
12576639	f	0	2021-01-17 16:24:12.434743+00	guardrail	31900261724	0	2
12576636	f	0	2021-01-17 16:24:12.285066+00	guardrail	31901122921	0	2
12576643	f	0	2021-01-17 16:24:12.500754+00	guardrail	30901293205	0	2
12576685	f	0	2021-01-17 16:24:13.919389+00	guardrail	31400173203	0	2
12576642	f	0	2021-01-17 16:24:12.485012+00	guardrail	30901523718	0	2
12576648	f	0	2021-01-17 16:24:12.727294+00	guardrail	32501102524	0	3
12576646	f	0	2021-01-17 16:24:12.634919+00	guardrail	32501014522	0	3
12576650	f	0	2021-01-17 16:24:12.835582+00	guardrail	32600594617	0	3
12576691	t	1	2021-01-17 16:24:14.019683+00	guardrail	32700031900	0	3
12576653	f	0	2021-01-17 16:24:12.910718+00	guardrail	30301130918	0	1
12576614	f	0	2021-01-17 16:24:11.792715+00	guardrail	30400214412	0	1
12576659	f	0	2021-01-17 16:24:13.277898+00	guardrail	42400450315	0	5
12576654	f	0	2021-01-17 16:24:12.935399+00	guardrail	42401304003	0	5
12576657	t	1	2021-01-17 16:24:13.01097+00	guardrail	42400405229	0	5
12576668	f	0	2021-01-17 16:24:13.502972+00	guardrail	35601575210	0	5
12576661	f	0	2021-01-17 16:24:13.3107+00	guardrail	35601190424	0	5
12576516	f	0	2021-01-17 16:24:08.643211+00	guardrail	35700034310	0	5
12576663	f	0	2021-01-17 16:24:13.343321+00	guardrail	35601070529	0	5
12576666	f	0	2021-01-17 16:24:13.468442+00	guardrail	35600544319	0	5
12576664	f	0	2021-01-17 16:24:13.394324+00	guardrail	35601582220	0	5
12576551	f	0	2021-01-17 16:24:09.862268+00	guardrail	34201040410	0	4
12576670	f	0	2021-01-17 16:24:13.536098+00	guardrail	33901183127	0	4
12576674	t	1	2021-01-17 16:24:13.602775+00	guardrail	30601400828	0	2
12576711	f	0	2021-01-17 16:24:14.613344+00	guardrail	30801333508	0	2
12576678	f	0	2021-01-17 16:24:13.711116+00	guardrail	30600402403	0	2
12576673	t	1	2021-01-17 16:24:13.586299+00	guardrail	30601400420	0	2
12576676	t	1	2021-01-17 16:24:13.678184+00	guardrail	30601263712	0	2
12576695	t	1	2021-01-17 16:24:14.086742+00	guardrail	31600423514	0	2
12576680	f	0	2021-01-17 16:24:13.79526+00	guardrail	31501442614	0	2
12576684	t	1	2021-01-17 16:24:13.903611+00	guardrail	32801545104	0	3
12576498	f	0	2021-01-17 16:24:07.513698+00	guardrail	33400080617	0	3
12576688	t	1	2021-01-17 16:24:13.969237+00	guardrail	31401385708	0	2
12576681	f	0	2021-01-17 16:24:13.853496+00	guardrail	31500235705	0	2
12576690	f	0	2021-01-17 16:24:14.003497+00	guardrail	32700170921	0	3
12576683	t	1	2021-01-17 16:24:13.886681+00	guardrail	32801431112	0	3
12576689	f	0	2021-01-17 16:24:13.986768+00	guardrail	32700170321	0	3
12576699	f	0	2021-01-17 16:24:14.212969+00	guardrail	31801210104	0	2
12576697	f	0	2021-01-17 16:24:14.120569+00	guardrail	15801484909	0	0
12576502	f	0	2021-01-17 16:24:07.885578+00	guardrail	16101050612	0	1
12576638	t	1	2021-01-17 16:24:12.375248+00	guardrail	31900161110	0	2
12576544	f	0	2021-01-17 16:24:09.695917+00	guardrail	29901432208	0	1
12576706	f	0	2021-01-17 16:24:14.429605+00	guardrail	33501452019	0	4
12576705	f	0	2021-01-17 16:24:14.404631+00	guardrail	33500481628	0	3
12576702	f	0	2021-01-17 16:24:14.287537+00	guardrail	33501434012	0	3
12576704	t	1	2021-01-17 16:24:14.37985+00	guardrail	33501402825	0	3
12576708	f	0	2021-01-17 16:24:14.488018+00	guardrail	33501464919	0	4
12576624	f	0	2021-01-17 16:24:11.959001+00	guardrail	33800281503	0	4
12576710	f	0	2021-01-17 16:24:14.537807+00	guardrail	35902013028	0	5
12576660	f	0	2021-01-17 16:24:13.294881+00	guardrail	42400220307	0	5
12576640	f	0	2021-01-17 16:24:12.450305+00	guardrail	30901224514	0	2
12576703	f	0	2021-01-17 16:24:14.312596+00	guardrail	33500181408	0	3
12576565	t	1	2021-01-17 16:24:10.296137+00	guardrail	16302025413	0	1
12576652	f	0	2021-01-17 16:24:12.885519+00	guardrail	30300400825	0	1
12576709	f	0	2021-01-17 16:24:14.513201+00	guardrail	35900171209	0	5
12576631	f	0	2021-01-17 16:24:12.100605+00	guardrail	35100165617	0	5
12576667	f	0	2021-01-17 16:24:13.486035+00	guardrail	35600501306	0	5
12576509	f	0	2021-01-17 16:24:08.285636+00	guardrail	30000272325	0	1
12576523	f	0	2021-01-17 16:24:09.069747+00	guardrail	34400070221	0	4
12576621	t	1	2021-01-17 16:24:11.908624+00	guardrail	29601084513	0	1
12576701	f	0	2021-01-17 16:24:14.262317+00	guardrail	29800012904	0	1
12576626	t	0.560000000000000053	2021-01-17 16:24:11.991896+00	guardrail	35101534826	43	0
12576655	f	0.409999999999999976	2021-01-17 16:24:12.960684+00	guardrail	42400183706	41	0
12576692	f	0.239999999999999991	2021-01-17 16:24:14.036966+00	guardrail	32700281324	24	0
12576698	t	0.810000000000000053	2021-01-17 16:24:14.136404+00	guardrail	31801174924	18	0
12576558	t	0.910000000000000031	2021-01-17 16:24:10.180577+00	guardrail	16301245502	8	0
12576677	f	0.0700000000000000067	2021-01-17 16:24:13.693836+00	guardrail	30600283129	7	0
12576687	t	0.930000000000000049	2021-01-17 16:24:13.953872+00	guardrail	31401495227	6	0
12576656	t	0.939999999999999947	2021-01-17 16:24:12.985684+00	guardrail	42400515327	6	0
12576641	f	0.0500000000000000028	2021-01-17 16:24:12.467916+00	guardrail	30900553212	4	0
12576649	t	0.979999999999999982	2021-01-17 16:24:12.810746+00	guardrail	32500283502	2	0
12576662	t	0.979999999999999982	2021-01-17 16:24:13.32751+00	guardrail	35600275009	2	0
12576682	t	0.989999999999999991	2021-01-17 16:24:13.869011+00	guardrail	31501391922	1	0
12576696	f	0	2021-01-17 16:24:14.103377+00	guardrail	15800251221	0	0
12576787	f	0	2021-01-17 16:24:16.500412+00	guardrail	34300021410	0	4
12576658	f	0	2021-01-17 16:24:13.136335+00	guardrail	42400135928	0	5
12576717	f	0	2021-01-17 16:24:14.728783+00	guardrail	16501045000	0	1
12576651	f	0	2021-01-17 16:24:12.860233+00	guardrail	30301141508	0	1
12576644	f	0	2021-01-17 16:24:12.585807+00	guardrail	32500192704	0	3
12576714	f	0	2021-01-17 16:24:14.678663+00	guardrail	30801392614	0	2
12576745	f	0	2021-01-17 16:24:15.330898+00	guardrail	31000211513	0	2
12576716	f	0	2021-01-17 16:24:14.713099+00	guardrail	30800471224	0	2
12576720	f	0	2021-01-17 16:24:14.778834+00	guardrail	16501060119	0	1
12576623	t	1	2021-01-17 16:24:11.94209+00	guardrail	29601072011	0	1
12576605	f	0	2021-01-17 16:24:11.557485+00	guardrail	30100424824	0	1
12576725	t	1	2021-01-17 16:24:14.863439+00	guardrail	33700545517	0	4
12576742	t	1	2021-01-17 16:24:15.2807+00	guardrail	34000045310	0	4
12576722	f	0	2021-01-17 16:24:14.813334+00	guardrail	33701302323	0	4
12576726	f	0	2021-01-17 16:24:14.878993+00	guardrail	33700591706	0	4
12576724	t	1	2021-01-17 16:24:14.846467+00	guardrail	33701165814	0	4
12576721	f	0	2021-01-17 16:24:14.796327+00	guardrail	33700375929	0	4
12576723	t	1	2021-01-17 16:24:14.828921+00	guardrail	33700352823	0	4
12576731	f	0	2021-01-17 16:24:14.970917+00	guardrail	33600384827	0	4
12576728	f	0	2021-01-17 16:24:14.921806+00	guardrail	33700223417	0	4
12576686	f	0	2021-01-17 16:24:13.936855+00	guardrail	31401474309	0	2
12576734	t	1	2021-01-17 16:24:15.030283+00	guardrail	42501082612	0	5
12576740	f	0	2021-01-17 16:24:15.24627+00	guardrail	34001370803	0	4
12576586	f	0	2021-01-17 16:24:11.07405+00	guardrail	34100205218	0	4
12576743	t	1	2021-01-17 16:24:15.29621+00	guardrail	34000104729	0	4
12576741	t	1	2021-01-17 16:24:15.26351+00	guardrail	34000051510	0	4
12576738	f	0	2021-01-17 16:24:15.214043+00	guardrail	34000191222	0	4
12576746	t	1	2021-01-17 16:24:15.346312+00	guardrail	31001021901	0	2
12576747	f	0	2021-01-17 16:24:15.36375+00	guardrail	31001261018	0	2
12576749	f	0	2021-01-17 16:24:15.397425+00	guardrail	31001363418	0	2
12576732	t	1	2021-01-17 16:24:14.987991+00	guardrail	31300315228	0	2
12576748	f	0	2021-01-17 16:24:15.380751+00	guardrail	31001364518	0	2
12576756	t	1	2021-01-17 16:24:15.689281+00	guardrail	32301354704	0	3
12576760	t	1	2021-01-17 16:24:15.923648+00	guardrail	32301204606	0	3
12576771	t	1	2021-01-17 16:24:16.190985+00	guardrail	32300473808	0	3
12576609	f	0	2021-01-17 16:24:11.625164+00	guardrail	32400265718	0	3
12576762	f	0	2021-01-17 16:24:15.990056+00	guardrail	32301485709	0	3
12576764	f	0	2021-01-17 16:24:16.073201+00	guardrail	32300323606	0	3
12576752	f	0	2021-01-17 16:24:15.498317+00	guardrail	32301174026	0	3
12576766	f	0	2021-01-17 16:24:16.105814+00	guardrail	32301233503	0	3
12576754	f	0	2021-01-17 16:24:15.655984+00	guardrail	32301503324	0	3
12576767	f	0	2021-01-17 16:24:16.123205+00	guardrail	32300431021	0	3
12576750	t	1	2021-01-17 16:24:15.456286+00	guardrail	32301242313	0	3
12576753	f	0	2021-01-17 16:24:15.589847+00	guardrail	32300441828	0	3
12576759	f	0	2021-01-17 16:24:15.830552+00	guardrail	32301163729	0	3
12576768	f	0	2021-01-17 16:24:16.139341+00	guardrail	32301114108	0	3
12576770	t	1	2021-01-17 16:24:16.172516+00	guardrail	32300491609	0	3
12576665	t	1	2021-01-17 16:24:13.452855+00	guardrail	35600284809	0	5
12576773	f	0	2021-01-17 16:24:16.233573+00	guardrail	35201071529	0	5
12576776	f	0	2021-01-17 16:24:16.291245+00	guardrail	30702000618	0	2
12576712	t	1	2021-01-17 16:24:14.637423+00	guardrail	30800051125	0	2
12576781	f	0	2021-01-17 16:24:16.3741+00	guardrail	30700384125	0	2
12576775	f	0	2021-01-17 16:24:16.273921+00	guardrail	30701245813	0	2
12576780	f	0	2021-01-17 16:24:16.358368+00	guardrail	30700411425	0	2
12576630	t	1	2021-01-17 16:24:12.07508+00	guardrail	35100560222	0	5
12576790	t	1	2021-01-17 16:24:16.625069+00	guardrail	34300400925	0	4
12576796	t	1	2021-01-17 16:24:16.74224+00	guardrail	34301151912	0	4
12576791	f	0	2021-01-17 16:24:16.650737+00	guardrail	34300541317	0	4
12576795	t	1	2021-01-17 16:24:16.724912+00	guardrail	34301065629	0	4
12576782	f	0	2021-01-17 16:24:16.39143+00	guardrail	34301535911	0	4
12576788	f	0	2021-01-17 16:24:16.525462+00	guardrail	34301145802	0	4
12576794	f	0	2021-01-17 16:24:16.708875+00	guardrail	34301294525	0	4
12576679	t	1	2021-01-17 16:24:13.728136+00	guardrail	30600045513	0	2
12576774	t	1	2021-01-17 16:24:16.258419+00	guardrail	35200154201	0	5
12576707	f	0	2021-01-17 16:24:14.454254+00	guardrail	33501365412	0	3
12576672	t	1	2021-01-17 16:24:13.56856+00	guardrail	30600250212	0	2
12576733	t	1	2021-01-17 16:24:15.00575+00	guardrail	42500252129	0	5
12576593	f	0	2021-01-17 16:24:11.257202+00	guardrail	36002001114	0	5
12576778	t	1	2021-01-17 16:24:16.323923+00	guardrail	30700322607	0	2
12576715	f	0	2021-01-17 16:24:14.696851+00	guardrail	30800335719	0	2
12576700	t	1	2021-01-17 16:24:14.237865+00	guardrail	31800150015	0	2
12576757	t	1	2021-01-17 16:24:15.756624+00	guardrail	32300032314	0	3
12576730	f	0	2021-01-17 16:24:14.955193+00	guardrail	33600004504	0	4
12576713	f	0	2021-01-17 16:24:14.662571+00	guardrail	30800570802	0	2
12576729	f	0	2021-01-17 16:24:14.937868+00	guardrail	33600375407	0	4
12576727	f	0	2021-01-17 16:24:14.896487+00	guardrail	33700365512	0	4
12576739	t	0.609999999999999987	2021-01-17 16:24:15.230344+00	guardrail	34000182102	39	0
12576763	f	0.280000000000000027	2021-01-17 16:24:16.057075+00	guardrail	32300263521	28	0
12576792	f	0.280000000000000027	2021-01-17 16:24:16.67556+00	guardrail	34301453523	28	0
12576789	f	0.260000000000000009	2021-01-17 16:24:16.609386+00	guardrail	34301374813	26	0
12576755	t	0.75	2021-01-17 16:24:15.671976+00	guardrail	32301141114	25	0
12576718	f	0.209999999999999992	2021-01-17 16:24:14.746041+00	guardrail	16501580619	20	0
12576783	t	0.790000000000000036	2021-01-17 16:24:16.408409+00	guardrail	34301424707	20	0
12576735	t	0.900000000000000022	2021-01-17 16:24:15.055098+00	guardrail	42500034620	9	0
12576769	t	0.939999999999999947	2021-01-17 16:24:16.156712+00	guardrail	32300293221	6	0
12576797	f	0.0500000000000000028	2021-01-17 16:24:16.759298+00	guardrail	34301153803	4	0
12576784	f	0.0400000000000000008	2021-01-17 16:24:16.425335+00	guardrail	34301095009	3	0
12576777	t	0.989999999999999991	2021-01-17 16:24:16.308237+00	guardrail	30700573221	1	0
12576637	t	0.989999999999999991	2021-01-17 16:24:12.359428+00	guardrail	31900403905	1	0
12576600	f	0	2021-01-17 16:24:11.43335+00	guardrail	15901225329	0	0
12576555	t	0.989999999999999991	2021-01-17 16:24:10.096623+00	guardrail	34201362524	1	0
12576793	f	0.0100000000000000002	2021-01-17 16:24:16.692233+00	guardrail	34301451503	1	0
12576535	t	0.989999999999999991	2021-01-17 16:24:09.545605+00	guardrail	35501095409	1	0
12576604	t	1	2021-01-17 16:24:11.542201+00	guardrail	15901110815	0	0
12576506	f	0	2021-01-17 16:24:08.052087+00	guardrail	16401575226	0	1
12576719	f	0	2021-01-17 16:24:14.763253+00	guardrail	16500135607	0	1
12576620	f	0	2021-01-17 16:24:11.892257+00	guardrail	29601544005	0	1
12576613	f	0	2021-01-17 16:24:11.725439+00	guardrail	30401182916	0	1
12576616	f	0	2021-01-17 16:24:11.824988+00	guardrail	30401205318	0	2
12576779	f	0	2021-01-17 16:24:16.341466+00	guardrail	30701365814	0	2
12576744	f	0	2021-01-17 16:24:15.313636+00	guardrail	31001305524	0	2
12576751	f	0	2021-01-17 16:24:15.481568+00	guardrail	32300171012	0	3
12576758	f	0	2021-01-17 16:24:15.815019+00	guardrail	32301100319	0	3
12576761	f	0	2021-01-17 16:24:15.938625+00	guardrail	32301201706	0	3
12576765	f	0	2021-01-17 16:24:16.09004+00	guardrail	32301231123	0	3
12576645	f	0	2021-01-17 16:24:12.610214+00	guardrail	32500195615	0	3
12576694	f	0	2021-01-17 16:24:14.069681+00	guardrail	32700330528	0	3
12576693	f	0	2021-01-17 16:24:14.053517+00	guardrail	32700385108	0	3
12576580	f	0	2021-01-17 16:24:10.924941+00	guardrail	33000081420	0	3
12576579	f	0	2021-01-17 16:24:10.857645+00	guardrail	33000085111	0	3
12576499	t	1	2021-01-17 16:24:07.743568+00	guardrail	33401471905	0	3
12576669	f	0	2021-01-17 16:24:13.518758+00	guardrail	33901500703	0	4
12576786	f	0	2021-01-17 16:24:16.475009+00	guardrail	34301182805	0	4
12576785	f	0	2021-01-17 16:24:16.450587+00	guardrail	34301333500	0	4
12576530	t	1	2021-01-17 16:24:09.269781+00	guardrail	34400394006	0	4
12576531	f	0	2021-01-17 16:24:09.285996+00	guardrail	34401231412	0	5
12576772	f	0	2021-01-17 16:24:16.208322+00	guardrail	35200250623	0	5
12576737	f	0	2021-01-17 16:24:15.147578+00	guardrail	42501115001	0	5
12576736	t	1	2021-01-17 16:24:15.080523+00	guardrail	42501474203	0	5
\.


--
-- Data for Name: rs_core_annotationflag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationflag (title) FROM stdin;
Fence
Obstructed
Edge of image
\.


--
-- Data for Name: rs_core_annotationset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationset (name, type) FROM stdin;
guardrail	cont
\.


--
-- Data for Name: rs_core_annotationset_flags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_annotationset_flags (id, annotationset_id, annotationflag_id) FROM stdin;
1	guardrail	Fence
2	guardrail	Obstructed
3	guardrail	Edge of image
\.


--
-- Data for Name: rs_core_routeimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rs_core_routeimage (route_id, image_base_name, location, mile_post, image_path) FROM stdin;
40002543051	33400080617	0101000020E610000025B78196899153C0719EFBBCF3B84140	0.0890000015497207642	d04/334/8
40002310051	33401471905	0101000020E6100000199AA1A7B78F53C0BAFEB858ACBD4140	3.75200009346008301	d04/334/107
40001937096	16100350429	0101000020E610000014D7E7201E8153C00B6EB598E9984140	0.229000002145767212	d04/161/35
40001937096	16100345009	0101000020E61000006759411D208153C0B159E48D82984140	0.00899999961256980896	d04/161/34
40001932096	16101050612	0101000020E61000002007CA12427E53C01C846F50B1A64140	0.642000019550323486	d04/161/65
40001937096	16100362400	0101000020E61000003CE180F1678153C049032E7E099B4140	1.41400003433227539	d04/161/36
40001628098	16401215429	0101000020E61000007FBA26497C7853C0C592CDB0ACCE4140	3.66000008583068848	d04/164/81
40001506098	16400161125	0101000020E6100000A516A5DF197353C0BD5065BDBDDC4140	1.85599994659423828	d04/164/16
40001613098	16401575226	0101000020E61000006D74CE4F717B53C02769FE98D6CB4140	7.20599985122680664	d04/164/117
40001404033	30001011809	0101000020E610000053978C63A46D53C0D9BB9A971E044240	2.5969998836517334	d04/300/61
40001400033	30000081915	0101000020E6100000DEBBBCEFCE6F53C0DB53CD075F014240	2.33800005912780762	d04/300/8
40001524064	30000272325	0101000020E61000005BCEA5B82A7653C0AEF5A0FBCD044240	5.48400020599365234	d04/300/27
40001693064	30001205208	0101000020E610000026CE401B6F7353C0F9707FE48C034240	0.245000004768371582	d04/300/80
40001607064	30000385923	0101000020E6100000C78CA669067853C06D5DC53DF1014240	1.32099997997283936	d04/300/38
40001303051	35801404307	0101000020E61000003D9E961F38A553C08331225168B34140	1.67599999904632568	d04/358/100
40001303051	35801471221	0101000020E6100000CC913AA693A653C077442A3174BC4140	7.14400005340576172	d04/358/107
40001361051	35801340023	0101000020E6100000D6EC37C945A353C0075B913DE7B74140	1.17299997806549072	d04/358/94
40001543096	35701420526	0101000020E6100000883C9347017C53C0F1D6F9B7CBBE4140	2.28699994087219238	d04/357/102
40002372051	35700034310	0101000020E6100000A2D68FA8AB8A53C0E66E21D96DB94140	3.14100003242492676	d04/357/3
40001544096	35701451127	0101000020E610000031D52714FD7C53C0AE6DE580B8BD4140	0.542999982833862305	d04/357/105
40002372051	35700040920	0101000020E61000007FEC3F7CAA8A53C057201F99B3B84140	3.53600001335144043	d04/357/4
40001231096	35700310103	0101000020E6100000AB7823F3C88753C050A50B5641B74140	0.796999990940093994	d04/357/31
40001009051	34400370205	0101000020E61000005864856CEA9153C00CF038A000A94140	12.5380001068115234	d04/344/37
40002958051	34401091323	0101000020E61000006DE34F5436A053C049D9226937C64140	0.194000005722045898	d04/344/69
40001230051	34400230020	0101000020E6100000042159C0049853C0A6D24F38BBB84140	0.126000002026557922	d04/344/23
40001162051	34400070221	0101000020E61000006DB4D25A079D53C04DFF48C78BBC4140	3.38700008392333984	d04/344/7
40002744051	34400403205	0101000020E610000045EFF906CBA053C0D606825BD2BD4140	0.0419999994337558746	d04/344/40
40001009051	34400300325	0101000020E6100000CF85915E549553C05B649698C2B14140	6.26800012588500977	d04/344/30
40001009051	34400303125	0101000020E610000096DC723FF19453C024319CC651B14140	6.68800020217895508	d04/344/30
40002217051	34400592320	0101000020E61000005B971AA19F9E53C06B35DA6097C14140	0.0700000002980232239	d04/344/59
40002217051	34400595700	0101000020E61000001349F4328A9E53C0C6AEA3607CC24140	0.569999992847442627	d04/344/59
40002756051	34400391623	0101000020E6100000C96B6F0132A053C045CA60D6D5BD4140	0.10599999874830246	d04/344/39
40002757051	34400394006	0101000020E610000084AFF90244A053C0F0B1AA14F1BD4140	0.0570000000298023224	d04/344/39
40001330051	34401231412	0101000020E6100000C7551B52FB9D53C077C47CD4BAC64140	0.052000001072883606	d04/344/83
40001306064	31200424207	0101000020E6100000626C7C81348453C029F922EBBAF94140	4.09899997711181641	d04/312/42
40002339051	35501425510	0101000020E6100000D6A0794A988A53C0F894528660C84140	0.802999973297119141	d04/355/102
40002124051	35501541503	0101000020E6100000B274F4AE308F53C0A01E36EC52D14140	0.555000007152557373	d04/355/114
40001720051	35501095409	0101000020E6100000E1DFB1E9529253C0BDF9B2599ACF4140	11.7119998931884766	d04/355/69
40001720051	35501091329	0101000020E61000004F948444DA9253C01620C0D831D04140	11.1079998016357422	d04/355/69
40001720051	35501085529	0101000020E6100000BB59CD84F09253C00EC1CCD2A9D04140	10.8380002975463867	d04/355/68
40002136051	35501325128	0101000020E610000060066344228E53C0F97DA42D53C84140	1.0140000581741333	d04/355/92
40001720051	35500575109	0101000020E61000008087FDF9919553C06D86C03687E14140	0.875999987125396729	d04/355/57
40001720051	35501070209	0101000020E6100000CE273CB2839353C0CE95F727A7D34140	9.13399982452392578	d04/355/67
40001945051	35501154425	0101000020E6100000C2AEDCC1BE9153C05F5E807D74D24140	0.544000029563903809	d04/355/75
40001141033	30200062407	0101000020E6100000CCCFB293667153C0B15E56725FF14140	2.39299988746643066	d04/302/6
40001253033	30200201401	0101000020E6100000BEA59C2F766553C0B1602C1DBDFB4140	2.73200011253356934	d04/302/20
40001505033	29901432208	0101000020E61000000D349F73375D53C00142356FE6014240	0.310000002384185791	d04/299/103
40001100042	29901194629	0101000020E610000084CB74F9A06653C0FA19283ADC134240	2.86800003051757812	d04/299/79
40001100042	29901322813	0101000020E6100000850F8013E55D53C00BA07312A5084240	13.5600004196166992	d04/299/92
40001518064	29901051509	0101000020E6100000369A12FF666F53C05FCBD01D69134240	3.91300010681152344	d04/299/65
40001238042	29901113229	0101000020E61000006F62ED94B36C53C00A302C7FBE144240	0.100000001490116119	d04/299/71
40001100042	29901341804	0101000020E6100000C1406BD9355C53C079DAD08371094240	15.0989999771118164	d04/299/94
40001935096	35401573022	0101000020E610000024B31FCEE88053C00E164ED2FC9B4140	0.301999986171722412	d04/354/117
40001121096	34201040410	0101000020E6100000BF5C305DAD8A53C0BD34EAC660A14140	1.87999999523162842	d04/342/64
40001218096	34201521024	0101000020E6100000C4B0C398F48653C02C4C3A257BA84140	1.16999995708465576	d04/342/112
40001144051	34200034707	0101000020E6100000FF902342489853C0654BFB8B45AC4140	0.876999974250793457	d04/342/3
40001106096	34201070010	0101000020E6100000DC7AF255178D53C0E0BA624678A24140	1.65199995040893555	d04/342/67
40001207096	34201362524	0101000020E61000004BB61556058F53C0B941A32A5CA64140	0.112000003457069397	d04/342/96
40001140051	34200012201	0101000020E610000006234097BA9A53C07EBD67C988AB4140	0.620000004768371582	d04/342/1
40001002051	33301120926	0101000020E6100000A67C08AAC68953C0F547BD4CB9BC4140	2.36100006103515625	d04/333/72
40001537098	16301245502	0101000020E610000013F9E417947053C0CB3D6E090ACF4140	2.63400006294250488	d04/163/84
40001602098	16301184725	0101000020E61000006FE70CD6497753C0FDAD539BEED24140	4.84499979019165039	d04/163/78
40001637098	16301022617	0101000020E6100000BA3DF7D4A07E53C003C70A2362CB4140	1.2929999828338623	d04/163/62
40001637098	16301023018	0101000020E61000007862D68BA17E53C000868A1645CB4140	1.35300004482269287	d04/163/62
40001651098	16300504528	0101000020E61000007C1BAC49818053C0CE3FB09932D24140	0.0970000028610229492	d04/163/50
40001145098	16300222214	0101000020E6100000548EC9E2FE8653C0540D0C6A09DC4140	1.19700002670288086	d04/163/22
40001145098	16300221524	0101000020E6100000C0649934FC8653C0D2A0B2ABDADB4140	1.09800004959106445	d04/163/22
40001507098	16302025413	0101000020E61000004DD47723187253C0F25190E91AD64140	5.01000022888183594	d04/163/122
40001428098	34901293001	0101000020E6100000A851ED78387553C08F72309B00E04140	2.18000006675720215	d04/349/89
40001537033	29701532424	0101000020E61000005188DBFC9A6053C02A183A1B97F64140	2.30399990081787109	d04/297/113
40001408033	29701315222	0101000020E6100000222F10A90E6A53C0E74306A85FFE4140	0.215000003576278687	d04/297/91
40001521042	29700553621	0101000020E6100000AB4EBD24047553C0405FC4888E3E4240	0.162000000476837158	d04/297/55
40001521042	29700553101	0101000020E610000036EE28290B7553C051C9EF236D3E4240	0.0829999968409538269	d04/297/55
40001346033	29701443127	0101000020E6100000A275F97B4E6453C0ED8CA5FE30F54140	1.70200002193450928	d04/297/104
40001415033	29701261012	0101000020E6100000709DDA74DF6C53C0E053EF5F0F064240	0.0930000022053718567	d04/297/86
40001001042	30501412415	0101000020E61000000355EDE49D7553C0D6427F57BA304240	6.32600021362304688	d04/305/101
40001001042	30502041402	0101000020E6100000993567333D6B53C040790E1B1B194240	25.5540008544921875	d04/305/124
40001600042	30500211224	0101000020E61000007D9AEED00B6C53C0E3D6EE682D2D4240	5.84999990463256836	d04/305/21
40001412042	30500483409	0101000020E61000001B75BEE9277553C058B89B960E394240	0.542999982833862305	d04/305/48
40001415042	30500414711	0101000020E610000099D36531317753C07144AD1F51344240	5.62400007247924805	d04/305/41
40002169051	33000215519	0101000020E610000028F62BF8C88C53C06BD8EF8975D94140	0	d04/330/21
40002112051	33000085111	0101000020E610000025B1A4DCFD8E53C0665133FF43D94140	0.0120000001043081284	d04/330/8
40002108051	33000081420	0101000020E6100000E1B4E045DF8E53C09B4D918D51DA4140	1.0140000581741333	d04/330/8
40001315064	31101314311	0101000020E6100000E65DF580798953C0C6AA9C514EF84140	0.0399999991059303284	d04/311/91
40001148064	31101034815	0101000020E61000003EBE73DEB58853C07EFFE6C589F64140	0.902000010013580322	d04/311/63
40001402098	34801083120	0101000020E6100000B5D892FA577553C0A4B61ECF78EB4140	0.171000003814697266	d04/348/68
40001452098	34800560920	0101000020E6100000DD465E31FE7553C0A3ACDF4C4CE04140	0.209999993443489075	d04/348/56
40001368098	34801052114	0101000020E610000088916F00477753C0819EBC7E77E64140	1.33599996566772461	d04/348/65
40001913096	34100205218	0101000020E61000003B14AA40527A53C0CE8B135FEDA04140	0.0790000036358833313	d04/341/20
40001933096	34100155616	0101000020E6100000BEEEBE74A47F53C0C1FD254E93A14140	2.57200002670288086	d04/341/15
40001172096	34100282611	0101000020E61000009D63E53C088353C07F0E982C93A14140	0.202000007033348083	d04/341/28
40001141096	34100321517	0101000020E6100000F1E5F4AB6F8553C081C6962F799A4140	0.151999995112419128	d04/341/32
40001913096	34100221828	0101000020E6100000D44A7C493E7B53C06FFDAA121B9F4140	1.37300002574920654	d04/341/22
40001113096	34101115407	0101000020E6100000CC03FD2AE58953C013EDCFEA899B4140	2.54800009727478027	d04/341/71
40002232096	36001265813	0101000020E6100000181B04673A7653C0C1E09A3BFAAC4140	0.499000012874603271	d04/360/86
40002050096	36002001114	0101000020E61000004A68812C7A7B53C0E5362BECB3A24140	1.10599994659423828	d04/360/120
40001103098	22000175809	0101000020E61000004942C7B3F08353C0BB25DEA6E4D34140	2.41199994087219238	d04/220/17
40001717064	22001512810	0101000020E61000000DC51D6FF27953C01F3240FDC2F34140	5.21799993515014648	d04/220/111
40001001064	22001132920	0101000020E6100000052857C2A48053C0D80638CEB7EE4140	4.99700021743774414	d04/220/73
40001960064	22000433201	0101000020E61000001C7E9296A58353C022AC21CC48E54140	2.29500007629394531	d04/220/43
40001960064	22000431902	0101000020E610000073B21E08DA8353C0169DD1FB6BE54140	2.10100007057189941	d04/220/43
40002110051	15901240029	0101000020E610000054C6BFCFB88B53C010A26B15B3D24140	3.99099993705749512	d04/159/84
40002110051	15901225329	0101000020E6100000818010244A8B53C0656C8DAD0CD14140	2.9869999885559082	d04/159/82
40002129051	15901091226	0101000020E61000001667B1B98F8E53C0642AB3F798CB4140	2.68199992179870605	d04/159/69
40002106051	15901333701	0101000020E6100000CB51DBE18A8F53C03BB9F0CD80DC4140	1.41100001335144043	d04/159/93
40002106051	15901324811	0101000020E6100000B3486EA8F38F53C0BF45274BADDD4140	0.68199998140335083	d04/159/92
40002143051	15901110815	0101000020E6100000948CF73EB08A53C00CE313573ACC4140	1.2359999418258667	d04/159/71
40001820042	30100424824	0101000020E6100000D798219F215753C042F1BE85D0074240	1.32200002670288086	d04/301/42
40001143051	32400355028	0101000020E610000093814DE7D49353C0E399869796AE4140	11.8380002975463867	d04/324/35
40001143051	32400230908	0101000020E610000012DDB3AE51A053C00541367F02AF4140	0.42300000786781311	d04/324/23
40001143051	32400271918	0101000020E610000012E04FE8509C53C02C103D2993AF4140	4.17500019073486328	d04/324/27
40001143051	32400265718	0101000020E61000001E7C725EAD9C53C0E6F4ABEFB2AF4140	3.84500002861022949	d04/324/26
40001143051	32400325018	0101000020E6100000863AAC70CB9653C0B8A2DE9DC6AE4140	9.13500022888183594	d04/324/32
40001143051	32400313308	0101000020E61000000C5BB395179853C0F9E6EDBE19AF4140	7.97599983215332031	d04/324/31
40001406042	30401244412	0101000020E6100000F40E01D15D7753C011F05AF8B03D4240	2.53999996185302734	d04/304/84
40001542042	30401182916	0101000020E6100000662A696A7E7953C09603E21A44404240	0.656000018119812012	d04/304/78
40001434042	30400214412	0101000020E610000091DC50E7C06E53C0521F926B54364240	2.21099996566772461	d04/304/21
40001492042	30400480726	0101000020E61000007F4FAC53E57653C0DBA4A2B1F63F4240	0.365999996662139893	d04/304/48
40001590042	30401205318	0101000020E61000008BF3812EAB7953C0EFAD484C503F4240	0.0320000015199184418	d04/304/80
40001406042	30401232201	0101000020E61000004B9D3699A77853C0A93A9AD99D3D4240	1.38399994373321533	d04/304/83
40001566042	30400531116	0101000020E6100000E3885A3F227853C03CF54883DB3D4240	0.0599999986588954926	d04/304/53
40001755042	29601422623	0101000020E61000000C4D2377226853C0087767EDB6294240	1.50499999523162842	d04/296/102
40001622042	29601544005	0101000020E610000021FAFF82EE6553C0EA20AF0793304240	0.323000013828277588	d04/296/114
40001673064	29601084513	0101000020E610000005847B0A257A53C07D68D59DDDFF4140	0.317000001668930054	d04/296/68
40001621042	29601521527	0101000020E61000004E870442216753C0D042A78C24314240	1.63100004196166992	d04/296/112
40002311064	29601072011	0101000020E61000000023C385977953C08D73E5FDC9004240	0.0820000022649765015	d04/296/67
40001505096	33800281503	0101000020E6100000F31142516A7A53C08351499D80C84140	2.89800000190734863	d04/338/28
40001723051	33800504204	0101000020E61000006C49A2F28A9353C09D11A5BDC1E44140	3.40100002288818359	d04/338/50
40002328051	35101534826	0101000020E61000004DB38A48DE8E53C0A4575E4DF9C34140	1.03100001811981201	d04/351/113
40001506051	35100180614	0101000020E6100000D15CA791969E53C0E0354305E2C54140	0.398000001907348633	d04/351/18
40001007051	35101182013	0101000020E61000005A10CAFBB88A53C0FA2F6BBD3AB24140	13.7810001373291016	d04/351/78
40001007051	35101145524	0101000020E61000003A1C02ECC88D53C0492BBEA1F0B34140	10.7150001525878906	d04/351/74
40002510051	35100560222	0101000020E6100000A39AED65B69253C007955DD5FEBD4140	0.187999993562698364	d04/351/56
40003349051	35100165617	0101000020E61000008048BF7D1D9E53C04C35B39602C64140	0.479000002145767212	d04/351/16
40001007051	35101051713	0101000020E6100000EB6E9EEA909553C0D55526A199BC4140	2.04600000381469727	d04/351/65
40002509051	35100530209	0101000020E61000003B42BC64D29253C021D335EE28BE4140	0.795000016689300537	d04/351/53
40001945064	31901543714	0101000020E6100000A1134207DD8353C0A05A33E83AED4140	8.87199974060058594	d04/319/114
40001945064	31901522512	0101000020E6100000CB468C43A28253C01A0AE93A9EEA4140	7.01800012588500977	d04/319/112
40001328098	31901122921	0101000020E610000040D422475F7853C0322889DB57DF4140	0.634999990463256836	d04/319/72
40001109033	31900403905	0101000020E6100000A6F7E868B06C53C0B788DE9854E74140	7.09499979019165039	d04/319/40
40001531098	31900161110	0101000020E61000009B705413E96C53C0FB6E04F3A1D34140	1.64400005340576172	d04/319/16
40001106033	31900261724	0101000020E6100000D5CA845FEA6B53C0A3586E6935DC4140	0.448000013828277588	d04/319/26
40001528064	30901224514	0101000020E6100000892E03298C7553C0F599588572074240	1.1260000467300415	d04/309/82
40001324064	30900553212	0101000020E61000003A8B83F08D8553C0C4831C4AA3084240	2.38899993896484375	d04/309/55
40001004064	30901523718	0101000020E610000084A7469EDA7E53C0BD299B28F8034240	11.875	d04/309/112
40001507064	30901293205	0101000020E610000096896C31897C53C00BCE8536A5134240	1.37800002098083496	d04/309/89
40001717096	32500192704	0101000020E610000089D1730BDD7453C0345FCA6548AE4140	1.22399997711181641	d04/325/19
40001717096	32500195615	0101000020E610000088C90A340E7553C08D02E9071AAE4140	1.66400003433227539	d04/325/19
40002229096	32501014522	0101000020E610000042171E45E77653C05E0C8A8B48A64140	0.0599999986588954926	d04/325/61
40001717096	32500201714	0101000020E6100000CE37A27B567553C026AC8DB113AE4140	1.97800004482269287	d04/325/20
40001727096	32501102524	0101000020E61000005E413FF8757853C0F2CF0CE203A64140	0.718999981880187988	d04/325/70
40001720096	32500283502	0101000020E61000002CFCCF50927553C0F9FDF6D099AB4140	0.379000008106231689	d04/325/28
40001142051	32600594617	0101000020E6100000A61EB3FDF59C53C078AD293520AB4140	0.721000015735626221	d04/326/59
40001117042	30301141508	0101000020E6100000CB5BBFAA445E53C0A7A73407AD1A4240	2.77699995040893555	d04/303/74
40001220042	30300400825	0101000020E610000097F7DD19926B53C0B05758703F174240	0.0160000007599592209	d04/303/40
40001117042	30301130918	0101000020E61000004856D9D2FE5E53C0C68BE0DAE41B4240	1.85500001907348633	d04/303/73
40001941064	42401304003	0101000020E610000016B545E39A8353C00B85BEAA69E84140	2.2090001106262207	d04/424/90
40001136064	42400183706	0101000020E61000005840FC57318953C0176EAFBB2FEF4140	0.184000000357627869	d04/424/18
40001115064	42400515327	0101000020E6100000A8A8FA95CE8E53C0AF8273A14DE34140	2.25500011444091797	d04/424/51
40001126064	42400405229	0101000020E61000001E9ECA0E968B53C026EC91BC29E74140	1.52900004386901855	d04/424/40
40001131064	42400135928	0101000020E6100000DBCF7355EA8A53C0123F106AD0EA4140	0.361999988555908203	d04/424/13
40001112064	42400450315	0101000020E6100000DA6E27B6278C53C04CB0EE0EDFE04140	1.78600001335144043	d04/424/45
40001141064	42400220307	0101000020E61000009BA49EAAE78953C0C4318111EAEE4140	1.27100002765655518	d04/424/22
40002312051	35601190424	0101000020E610000077E6D484238F53C06E2CCD5257BF4140	1.00499999523162842	d04/356/79
40002127051	35600275009	0101000020E61000004CA8E0F0028E53C096F6BCD17DCF4140	0.670000016689300537	d04/356/27
40002523051	35601070529	0101000020E610000057957D57848C53C04D91329875BA4140	3.60299992561340332	d04/356/67
40001007096	35601582220	0101000020E6100000A600625C3B8853C0374EAF39ACB24140	4.13600015640258789	d04/356/118
40002127051	35600284809	0101000020E6100000404750A1DF8E53C05D03B6DECACE4140	1.53900003433227539	d04/356/28
40002525051	35600544319	0101000020E6100000224F37F5A68D53C05455682096B84140	0.31400001049041748	d04/356/54
40002524051	35600501306	0101000020E6100000A02AF05F6A8E53C0B72407EC6AB54140	1.38300001621246338	d04/356/50
40001007096	35601575210	0101000020E610000032303C40C18753C007B1D8CB5BB24140	3.68199992179870605	d04/356/117
40001137098	33901500703	0101000020E6100000FD063763628453C0F5143944DCE04140	2.06100010871887207	d04/339/110
40002392051	33901183127	0101000020E6100000E6E37F97BE8E53C0606F078FDBC54140	0.947000026702880859	d04/339/78
40002392051	33901182607	0101000020E610000040CE458DD38E53C062C0ED64CBC54140	0.866999983787536621	d04/339/78
40001225042	30600250212	0101000020E6100000524832AB776C53C09A4EA1A98D144240	0.225999996066093445	d04/306/25
40001210042	30601400420	0101000020E6100000A7F1C1210A6F53C053B70E69AF1E4240	11.3850002288818359	d04/306/100
40001210042	30601400828	0101000020E6100000C44373F8FF6E53C03B21CF89981E4240	11.4449996948242188	d04/306/100
40001616042	30600235410	0101000020E6100000C82764E76D6B53C0D46D3FCF552C4240	0.519999980926513672	d04/306/23
40001210042	30601263712	0101000020E6100000E7C41EDA476E53C0A74C20DBE8304240	0.052000001072883606	d04/306/86
40001240042	30600283129	0101000020E6100000D2EE46D5E57053C0529B38B9DF164240	0.0500000007450580597	d04/306/28
40001206042	30600402403	0101000020E61000003FF78A13046D53C0F7D26FBAC01E4240	2.2369999885559082	d04/306/40
40001207042	30600045513	0101000020E610000052BAF42F496E53C07203F4B1711E4240	1.26900005340576172	d04/306/4
40001614033	31501442614	0101000020E610000075E04158326653C0DAE4F04927DD4140	2.02399992942810059	d04/315/104
40001124033	31500235705	0101000020E610000083AB973A236F53C06A9B87B8DEE74140	4.43400001525878906	d04/315/23
40001613033	31501391922	0101000020E6100000CF5037AB196753C0AC521FED24E34140	0.00400000018998980522	d04/315/99
40001162051	32801431112	0101000020E610000025D126E2889C53C026E71FD84CBD4140	2.7780001163482666	d04/328/103
40001166051	32801545104	0101000020E6100000D15735ADB99D53C0C53FC7A244B74140	1.22599995136260986	d04/328/114
40001207033	31400173203	0101000020E6100000BB88A537126653C0FFD4D3A299F34140	0.666999995708465576	d04/314/17
40001344033	31401474309	0101000020E6100000E8ED19D3DD6353C0A5BA25DEA6EF4140	0.363999992609024048	d04/314/107
40001204033	31401495227	0101000020E6100000983DBFDE336653C0DC52BDEB22EE4140	0.0480000004172325134	d04/314/109
40001526033	31401385708	0101000020E6100000530B804CC65B53C0EB7F6F8912ED4140	1.90600001811981201	d04/314/98
40001706096	32700170321	0101000020E6100000E4B622D6077653C0A946544DB5B54140	0.133000001311302185	d04/327/17
40001706096	32700170921	0101000020E610000003B16CE6107653C088E3AF7F8DB54140	0.222000002861022949	d04/327/17
40001728096	32700031900	0101000020E61000002A3A92CB7F7953C059901C9F7FA74140	2.25	d04/327/3
40001883096	32700281324	0101000020E6100000A3C5BE09AA7853C07308C14FC1B54140	0.0390000008046627045	d04/327/28
40001675096	32700385108	0101000020E6100000CB773AA1A17653C0BB6A5496D7B84140	0.222000002861022949	d04/327/38
40001702096	32700330528	0101000020E610000026074724657653C02A90D959F4B54140	1.0549999475479126	d04/327/33
40001126033	31600423514	0101000020E6100000AADB3411916D53C0582A5E1BE0E94140	3.72600007057189941	d04/316/42
40001001051	15800251221	0101000020E610000094F6065F988853C0B5368DEDB5C54140	2.72099995613098145	d04/158/25
40001535096	15801484909	0101000020E6100000A35A4414137953C04526851ED6BA4140	5.62799978256225586	d04/158/108
40001002098	31801174924	0101000020E610000065B1039D7F7153C0C75DCEB6E4E44140	5.50400018692016602	d04/318/77
40001002098	31801210104	0101000020E61000000CDEA1725D7153C00C91D3D7F3DF4140	8.18999958038330078	d04/318/81
40001106064	31800150015	0101000020E6100000A941E268D88853C077C883E3E8E44140	0.503000020980834961	d04/318/15
40001516033	29800012904	0101000020E6100000601DC70F955D53C08F1E1A715CF64140	1.05099999904632568	d04/298/1
40001917096	33501434012	0101000020E6100000CF64A4839A7E53C0B4F688E29FA74140	1.16100001335144043	d04/335/103
40002305096	33500181408	0101000020E61000003FD46CD4797953C0E9FF6673E6B84140	0.00800000037997961044	d04/335/18
40001127096	33501402825	0101000020E61000005AEC9BA0728553C0BE6BD097DEA34140	1.12699997425079346	d04/335/100
40001545096	33500481628	0101000020E610000081481A37107E53C0564C0059E3BD4140	0.74299997091293335	d04/335/48
40001928096	33501452019	0101000020E61000007FDEAF5D357F53C0FC3905F9D9A64140	0.595000028610229492	d04/335/105
40001154096	33501365412	0101000020E6100000554CA59F708353C0AE3F2E162BA34140	0.0379999987781047821	d04/335/96
40001928096	33501464919	0101000020E61000009184D8F4FB7F53C0C25C9C42F8A84140	1.92900002002716064	d04/335/106
40001319051	35900171209	0101000020E610000039F2406491A553C0627E13AF57BD4140	2.15899991989135742	d04/359/17
40001308051	35902013028	0101000020E61000005E413FF875A353C0750E547C32B94140	2.41400003433227539	d04/359/121
40001417064	30801333508	0101000020E61000006F9EEA909B7C53C05BD5ED47E5074240	1.0429999828338623	d04/308/93
40001403064	30800051125	0101000020E6100000BE182543E97C53C0A7125443D10F4240	2.25099992752075195	d04/308/5
40001500064	30800570802	0101000020E610000046A055C1837953C052AA8E66760D4240	2.30699992179870605	d04/308/57
40001432064	30801392614	0101000020E6100000E7B3F281D37D53C0C51D6FF25B014240	0.670000016689300537	d04/308/99
40001338042	30800335719	0101000020E610000023467474817953C0F2F16492EC164240	0.651000022888183594	d04/308/33
40002339064	30800471224	0101000020E610000082B34A9F8C7953C0338232326D0D4240	0.0329999998211860657	d04/308/47
40001341096	16501045000	0101000020E6100000044FC69DF78153C06B35DA6097C44140	2.0820000171661377	d04/165/64
40001121098	16501580619	0101000020E610000012A7EE25688853C082B0AE658DD34140	1.04499995708465576	d04/165/118
40001521096	16500135607	0101000020E6100000C3E22659BD7953C00F63D2DF4BC64140	0.811999976634979248	d04/165/13
40001341096	16501060119	0101000020E6100000EE7893DF228353C0A659EA6A3CC44140	3.15499997138977051	d04/165/66
40001154098	33700375929	0101000020E6100000889A8D3ADF8153C0DAA9B9DC60D84140	4.88399982452392578	d04/337/37
40001644098	33701302323	0101000020E610000019EB76514F7E53C049AEAC7EB6D04140	0.888000011444091797	d04/337/90
40001154098	33700352823	0101000020E61000007C8B3D6A028253C0BF3AD8AC44DC4140	2.76099991798400879	d04/337/35
40001666098	33701165814	0101000020E610000080924C987A8653C065283806AECC4140	1.07899999618530273	d04/337/76
40001100098	33700545517	0101000020E6100000715413E9A37D53C0A999FFA1AAD64140	0.606999993324279785	d04/337/54
40001100098	33700591706	0101000020E61000009C059090378153C0B6B86BAE3FD44140	4.28000020980834961	d04/337/59
40001154098	33700365512	0101000020E6100000F092EE9D078253C06F7B270B04DA4140	3.97799992561340332	d04/337/36
40001330098	33700223417	0101000020E61000006BF0BE2A177953C08E95F32098E44140	0.790000021457672119	d04/337/22
40001224096	33600375407	0101000020E6100000FEE4396C6C8853C061495E42AAAE4140	1.76499998569488525	d04/336/37
40001116051	33600004504	0101000020E61000008F029F7AFF9853C0B4FE3B4789A84140	0.597999989986419678	d04/336/0
40001224096	33600384827	0101000020E610000001289023E78753C0624F96B5A8AF4140	2.53299999237060547	d04/336/38
40001745064	31300315228	0101000020E6100000E24F9EC3467953C04402FC091DF14140	1.58800005912780762	d04/313/31
40001151064	42500252129	0101000020E6100000277B95C6798D53C0BEC51E3581F14140	0.437000006437301636	d04/425/25
40001145064	42501082612	0101000020E6100000BEFB3E775D8053C009F76F03E3F74140	11.8319997787475586	d04/425/68
40001131098	42500034620	0101000020E61000002F55C4445E8A53C071164042DEDE4140	1.86800003051757812	d04/425/3
40001310064	42501474203	0101000020E6100000E83812C3E97A53C0B1F9B836540E4240	14.3809995651245117	d04/425/107
40001145064	42501115001	0101000020E6100000EB854C431E7D53C078E7F5CC37F94140	14.8850002288818359	d04/425/71
40001739096	34000191222	0101000020E61000006BC9F495D17553C06BB2EB83D19C4140	3.57800006866455078	d04/340/19
40001739096	34000182102	0101000020E610000049E47107207653C0287C5B559B9B4140	2.80299997329711914	d04/340/18
40001938096	34001370803	0101000020E61000004076CD9A0E8353C0FCB781F1C29B4140	0.91100001335144043	d04/340/97
40001915096	34000051510	0101000020E610000070534D5A027D53C0A8EAD44B42A04140	4.47700023651123047	d04/340/5
40001915096	34000045310	0101000020E6100000C8A71144277D53C0A81EC429CEA04140	4.14799976348876953	d04/340/4
40001953096	34000104729	0101000020E6100000548F34B8AD7A53C011B8BFC469994140	0.0219999998807907104	d04/340/10
40001909064	31001305524	0101000020E6100000206118B0E48053C0E9DA72897EF84140	2.4309999942779541	d04/310/90
40001531064	31000211513	0101000020E61000005A07ACC1207853C00A6AF816D6064240	3.8900001049041748	d04/310/21
40001425064	31001021901	0101000020E6100000CD357117068053C0355C89E53B064240	2.05699992179870605	d04/310/62
40001910064	31001261018	0101000020E61000007E9065C1C48153C05161116855FA4140	0.187999993562698364	d04/310/86
40001997064	31001364518	0101000020E6100000E3F7DB43677E53C061BB20C77BF64140	1.75899994373321533	d04/310/96
40001997064	31001363418	0101000020E6100000C67FCBAD5A7E53C07F96F8ED35F64140	1.60399997234344482	d04/310/96
40001157051	32301242313	0101000020E6100000256F25E07C9D53C0189EF24300B34140	2.03099989891052246	d04/323/84
40001102051	32300171012	0101000020E6100000A5F0452003A353C0ADD62E127FAD4140	0.893000006675720215	d04/323/17
40001158051	32301174026	0101000020E61000001594FD4EEE9C53C08A2F2471A0B04140	0.0359999984502792358	d04/323/77
40001113051	32300441828	0101000020E610000030968EDE959D53C0D52FC7E182A34140	0.726999998092651367	d04/323/44
40001154051	32301503324	0101000020E610000015DE8A69CB9A53C0B026AA12C0B04140	0.514999985694885254	d04/323/110
40001177051	32301141114	0101000020E6100000168B3ACE489C53C019D2979471AE4140	1.33599996566772461	d04/323/74
40001209051	32301354704	0101000020E61000002D75351E919E53C0270FB0FB33B34140	0.924000024795532227	d04/323/95
40001300051	32300032314	0101000020E61000001B18D41206A453C0D152C3C8DCAF4140	0.500999987125396729	d04/323/3
40001171051	32301100319	0101000020E610000093E1783E03A053C0AFCE31207BB24140	1.18700003623962402	d04/323/70
40001155051	32301163729	0101000020E6100000A3E5400F359C53C022C5008926B14140	1.26100003719329834	d04/323/76
40001158051	32301204606	0101000020E61000009135D9F5C19F53C0375A69ADC3B14140	2.81299996376037598	d04/323/80
40001158051	32301201706	0101000020E6100000CA0DD0C7469F53C05A5A571696B14140	2.37899994850158691	d04/323/80
40001150051	32301485709	0101000020E61000008070F4E7119A53C056010869D7B34140	2.64199995994567871	d04/323/108
40001105051	32300263521	0101000020E6100000B39943520BA053C036453646A1AC4140	1.19700002670288086	d04/323/26
40001111051	32300323606	0101000020E610000054628D69DC9F53C0F9C32A3982A74140	0.072999998927116394	d04/323/32
40001157051	32301231123	0101000020E61000002E2F0ACCD49C53C0327F3B3F7BB14140	0.955999970436096191	d04/323/83
40001157051	32301233503	0101000020E610000094D85A04EB9C53C06E1C0CD011B24140	1.30700004100799561	d04/323/83
40001120051	32300431021	0101000020E61000003FDC7AF2D59C53C046072461DFA44140	2.93799996376037598	d04/323/43
40001171051	32301114108	0101000020E61000009FD8F96DBE9F53C0F0124141CEAF4140	2.65000009536743164	d04/323/71
40001105051	32300293221	0101000020E61000002338899C199F53C0E7B45D5782A84140	3.85100007057189941	d04/323/29
40001113051	32300491609	0101000020E610000083458F29699E53C076ACAD3319A94140	5.18499994277954102	d04/323/49
40001113051	32300473808	0101000020E610000057BA7141EC9E53C051D43EC2D5A64140	3.71499991416931152	d04/323/47
40001754096	35200250623	0101000020E6100000B75219106B7853C016D3968455954140	1.90199995040893555	d04/352/25
40001235096	35201071529	0101000020E61000004455A75E128753C03E1B5EB5D7B74140	0.0160000007599592209	d04/352/67
40001746096	35200154201	0101000020E6100000633CEF6B497753C0F749A4236F9B4140	0.273999989032745361	d04/352/15
40001510064	30701245813	0101000020E6100000021FCDA2C17053C02700B507100F4240	11.0030002593994141	d04/307/84
40001505064	30702000618	0101000020E6100000C877CEBBD67B53C0CE7D834078154240	2.40100002288818359	d04/307/120
40001512064	30700573221	0101000020E610000082AED8BAAF7653C02FD6DC7646114240	0.00600000005215406418	d04/307/57
40001002042	30700322607	0101000020E610000011436106197953C05706D506271E4240	3.6400001049041748	d04/307/32
40001214042	30701365814	0101000020E610000093342493787A53C03D17FCEC361B4240	6.38399982452392578	d04/307/96
40001002042	30700411425	0101000020E610000043A44BA4D97153C01E407562C51B4240	11.0620002746582031	d04/307/41
40001002042	30700384125	0101000020E6100000FA7E6ABCF47353C04E2C4BCF4F1D4240	8.91399955749511719	d04/307/38
40001339051	34301535911	0101000020E6100000D12CBFC2B89C53C04520A8644ABD4140	0.998000025749206543	d04/343/113
40001329051	34301424707	0101000020E6100000450CE0D2D6A153C002052857C2BF4140	0.88200002908706665	d04/343/102
40001188051	34301095009	0101000020E61000004E6ECACBD09453C0210CF26904A74140	1.40199995040893555	d04/343/69
40001355051	34301333500	0101000020E61000008201840FA5A053C032A3699AC1B74140	0.41100001335144043	d04/343/93
40001168051	34301182805	0101000020E6100000B5615E91A9A153C01F0D4C135BB44140	0.977999985218048096	d04/343/78
40001008096	34300021410	0101000020E61000007BEAA2320F8353C0FF42EAD1AFAF4140	1.75800001621246338	d04/343/2
40001185051	34301145802	0101000020E6100000D3BAB2B04C9553C0B48295F9FDAC4140	2.84400010108947754	d04/343/74
40001331051	34301374813	0101000020E610000090696D1ADBA153C0A118B4EB39B84140	1.27900004386901855	d04/343/97
40001136051	34300400925	0101000020E61000009E4FD31D7A9653C004A09B470FA84140	3.78600001335144043	d04/343/40
40001190051	34300541317	0101000020E6100000D2A755F4079453C0DC91FB6717A84140	1.25300002098083496	d04/343/54
40001399051	34301453523	0101000020E6100000826A285ADEA253C0117B57F3D2BC4140	1.11800003051757812	d04/343/105
40001399051	34301451503	0101000020E6100000EF377FB8D0A253C0702D49545EBD4140	0.808000028133392334	d04/343/105
40001357051	34301294525	0101000020E6100000612C1DBD2BA153C08B5C267964B54140	0.270999997854232788	d04/343/89
40001191051	34301065629	0101000020E61000007E7D63BEF29553C00057B26323A74140	0.444000005722045898	d04/343/66
40001185051	34301151912	0101000020E6100000C0102851659553C02D49F9A46EAC4140	3.16400003433227539	d04/343/75
40001185051	34301153803	0101000020E610000003BCBB84799553C009E643ABEEAB4140	3.4440000057220459	d04/343/75
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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 11, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 21, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 39, true);


--
-- Name: django_redirect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_redirect_id_seq', 1, false);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 2, true);


--
-- Name: rs_core_aiimageannotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_aiimageannotation_id_seq', 12576797, true);


--
-- Name: rs_core_annotationset_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_annotationset_flags_id_seq', 3, true);


--
-- Name: rs_core_userimageannotation_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userimageannotation_flags_id_seq', 18, true);


--
-- Name: rs_core_userimageannotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userimageannotation_id_seq', 310, true);


--
-- Name: rs_core_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rs_core_userprofile_id_seq', 10, true);


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
-- Name: rs_core_routeimage rs_core_routeimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rs_core_routeimage
    ADD CONSTRAINT rs_core_routeimage_pkey PRIMARY KEY (image_base_name);


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

