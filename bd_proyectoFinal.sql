PGDMP                         z            bd_proyectoFinal    13.2    13.2     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ?           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ?           1262    19825    bd_proyectoFinal    DATABASE     v   CREATE DATABASE "bd_proyectoFinal" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
 "   DROP DATABASE "bd_proyectoFinal";
                postgres    false                        2615    19826    registro    SCHEMA        CREATE SCHEMA registro;
    DROP SCHEMA registro;
                postgres    false            ?            1259    19838    trades    TABLE     ?   CREATE TABLE public.trades (
    tomar_ganancias double precision,
    precio_entrada double precision,
    moneda character varying,
    detener_perdidas double precision,
    tipo character varying,
    id integer NOT NULL
);
    DROP TABLE public.trades;
       public         heap    postgres    false            ?            1259    19855    trades_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.trades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.trades_id_seq;
       public          postgres    false    203            ?           0    0    trades_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.trades_id_seq OWNED BY public.trades.id;
          public          postgres    false    204            ?            1259    19827    usuario    TABLE       CREATE TABLE public.usuario (
    id integer NOT NULL,
    nickname character varying NOT NULL,
    password1 character varying NOT NULL,
    email character varying,
    role character varying(20),
    api character varying,
    api_secret character varying
);
    DROP TABLE public.usuario;
       public         heap    postgres    false            ?            1259    19833    usuario_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public          postgres    false    201            ?           0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public          postgres    false    202            ,           2604    19857 	   trades id    DEFAULT     f   ALTER TABLE ONLY public.trades ALTER COLUMN id SET DEFAULT nextval('public.trades_id_seq'::regclass);
 8   ALTER TABLE public.trades ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    204    203            +           2604    19835 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    202    201            ?          0    19838    trades 
   TABLE DATA                 public          postgres    false    203   ?       ?          0    19827    usuario 
   TABLE DATA                 public          postgres    false    201   _       ?           0    0    trades_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.trades_id_seq', 2, true);
          public          postgres    false    204            ?           0    0    usuario_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.usuario_id_seq', 5, true);
          public          postgres    false    202            .           2606    19837    usuario pk_cod_us 
   CONSTRAINT     O   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT pk_cod_us PRIMARY KEY (id);
 ;   ALTER TABLE ONLY public.usuario DROP CONSTRAINT pk_cod_us;
       public            postgres    false    201            0           2606    19865    trades trades_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.trades DROP CONSTRAINT trades_pkey;
       public            postgres    false    203            ?   ?   x????
?0??}?s??SL??ʼ? g???!?????W??????v}s??v??y{??z'$.?x37ޅzRb!`Nʌ??B??Ɛ=jt?E'?K??!?d
??ihzH2VҢ܄#PT?BC???#?f?*???։?d?.j?d?([?,g???ÿN??E/??^?      ?   ?  x????k?0???W?--?.????K?PX ????iPdK??b;?1۟??SJ??K'??t???????=?????0?????1?uW\?qU?u??MZ?0?>?U??P?WE??5?l??T??x]|??}?(??f.?u????X?i????????)bS??p?C?z잶ۓ??]l.?O{??^NKs?{??;??|i???v=?c*g}_緉#?8??E?
?y&??màcN6'???j?7h=C???q??j???/??ǲ ?
P<'?$ ?1?a??N???"?,??g3??z??h́K"&??H=?u:?.?gv??C??Ye??m?????%#?? ??F?fZ"pZ??(GNh B???i????E?l?P???!?`?.kv`]$VY????MD?!?1*v?1\2?ō??w??Y??ج-?n?7 Y,?Qr?     