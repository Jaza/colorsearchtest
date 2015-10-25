# -*- coding: utf-8 -*-


def delta_e_cie1976_query(lab_l, lab_a, lab_b, limit):
    """
    Queries the color table in the database, and sorts results
    using the Delta E CIE 1976 formula, comparing each record's Lab
    color to the Lab color specified in the arguments.
    """

    from sqlalchemy import text

    from colorsearchtest.database import db

    return (db.session
        .execute(
            text(
                'SELECT        c.rgb_r,'
                '              c.rgb_g,'
                '              c.rgb_b,'
                '              SQRT('
                '        POW((:lab_l - c.lab_l), 2.0) +'
                '        POW((:lab_a - c.lab_a), 2.0) +'
                '        POW((:lab_b - c.lab_b), 2.0))'
                '    AS delta_e_cie1976 '
                'FROM          color c '
                'ORDER BY      delta_e_cie1976 '
                'LIMIT         :limit'),
            dict(lab_l=lab_l,
                 lab_a=lab_a,
                 lab_b=lab_b,
                 limit=limit)))


def delta_e_cie2000_query(lab_l, lab_a, lab_b, kl=1.0, kc=1.0, kh=1.0, limit=10, range_threshold=20.0):
    """
    Queries the color table in the database, and sorts results
    using the Delta E CIE 2000 formula, comparing each record's Lab
    color to the Lab color specified in the arguments.
    """

    from sqlalchemy import text

    from colorsearchtest.database import db

    r = (db.session
        .execute(
            text(
                'CREATE OR REPLACE FUNCTION '
                'DELTA_E_CIE2000(double precision, double precision,'
                '                double precision, double precision,'
                '                double precision, double precision,'
                '                double precision, double precision,'
                '                double precision) '
                'RETURNS double precision '
                'AS $$ '
                ''
                'WITH '
                '    c AS (SELECT'
                '            (CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))'
                '        AS lab_pair_str,'
                '            (($1 + $4) /'
                '                2.0)'
                '        AS avg_lp,'
                '            SQRT('
                '                POW($2, 2.0) +'
                '                POW($3, 2.0))'
                '        AS c1,'
                '            SQRT('
                '                POW(($5), 2.0) +'
                '                POW(($6), 2.0))'
                '        AS c2),'
                '    gs AS (SELECT'
                '            c.lab_pair_str,'
                '            (0.5 *'
                '                (1.0 - SQRT('
                '                    POW(((c.c1 + c.c2) / 2.0), 7.0) / ('
                '                        POW(((c.c1 + c.c2) / 2.0), 7.0) +'
                '                        POW(25.0, 7.0)))))'
                '        AS g'
                '        FROM c'
                '        WHERE c.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    ap AS (SELECT'
                '            gs.lab_pair_str,'
                '            ((1.0 + gs.g) * $2)'
                '        AS a1p,'
                '            ((1.0 + gs.g) * $5)'
                '        AS a2p'
                '        FROM gs'
                '        WHERE gs.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    cphp AS (SELECT'
                '            ap.lab_pair_str,'
                '            SQRT('
                '                POW(ap.a1p, 2.0) +'
                '                POW($3, 2.0))'
                '        AS c1p,'
                '            SQRT('
                '                POW(ap.a2p, 2.0) +'
                '                POW($6, 2.0))'
                '        AS c2p,'
                '            ('
                '                DEGREES(ATAN2($3, ap.a1p)) + ('
                '                    CASE'
                '                        WHEN DEGREES(ATAN2($3, ap.a1p)) < 0.0'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '        AS h1p,'
                '            ('
                '                DEGREES(ATAN2($6, ap.a2p)) + ('
                '                    CASE'
                '                        WHEN DEGREES(ATAN2($6, ap.a2p)) < 0.0'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '        AS h2p'
                '        FROM ap'
                '        WHERE ap.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    av AS (SELECT'
                '            cphp.lab_pair_str,'
                '            ((cphp.c1p + cphp.c2p) /'
                '                2.0)'
                '        AS avg_c1p_c2p,'
                '            (((CASE'
                '                WHEN (ABS(cphp.h1p - cphp.h2p) > 180.0)'
                '                THEN 360.0'
                '                ELSE 0.0'
                '                END) +'
                '              cphp.h1p +'
                '              cphp.h2p) /'
                '                2.0)'
                '        AS avg_hp'
                '        FROM cphp'
                '        WHERE cphp.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    ts AS (SELECT'
                '            av.lab_pair_str,'
                '            (1.0 - '
                '                0.17 * COS(RADIANS(av.avg_hp - 30.0)) +'
                '                0.24 * COS(RADIANS(2.0 * av.avg_hp)) +'
                '                0.32 * COS(RADIANS(3.0 * av.avg_hp + 6.0)) -'
                '                0.2 * COS(RADIANS(4.0 * av.avg_hp - 63.0)))'
                '        AS t,'
                '            (('
                '                    (cphp.h2p - cphp.h1p) +'
                '                    (CASE'
                '                        WHEN (ABS(cphp.h2p - cphp.h1p) > 180.0)'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '                -'
                '                (CASE'
                '                    WHEN (cphp.h2p > cphp.h1p)'
                '                    THEN 720.0'
                '                    ELSE 0.0'
                '                    END))'
                '        AS delta_hlp'
                '        FROM av'
                '        INNER JOIN cphp'
                '        ON av.lab_pair_str = cphp.lab_pair_str'
                '        WHERE av.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    d AS (SELECT'
                '            ts.lab_pair_str,'
                '            ($4 - $1)'
                '        AS delta_lp,'
                '            (cphp.c2p - cphp.c1p)'
                '        AS delta_cp,'
                '            (2.0 * ('
                '                SQRT(cphp.c2p * cphp.c1p) *'
                '                SIN(RADIANS(ts.delta_hlp) / 2.0)))'
                '        AS delta_hp,'
                '            (1.0 + ('
                '                (0.015 * POW(c.avg_lp - 50.0, 2.0)) /'
                '                SQRT(20.0 + POW(c.avg_lp - 50.0, 2.0))))'
                '        AS s_l,'
                '            (1.0 + 0.045 * av.avg_c1p_c2p)'
                '        AS s_c,'
                '            (1.0 + 0.015 * av.avg_c1p_c2p * ts.t)'
                '        AS s_h,'
                '            (30.0 * EXP(-(POW(((av.avg_hp - 275.0) / 25.0), 2.0))))'
                '        AS delta_ro,'
                '            SQRT('
                '                (POW(av.avg_c1p_c2p, 7.0)) /'
                '                (POW(av.avg_c1p_c2p, 7.0) + POW(25.0, 7.0)))'
                '        AS r_c'
                '        FROM ts'
                '        INNER JOIN cphp'
                '        ON ts.lab_pair_str = cphp.lab_pair_str'
                '        INNER JOIN c'
                '        ON ts.lab_pair_str = c.lab_pair_str'
                '        INNER JOIN av'
                '        ON ts.lab_pair_str = av.lab_pair_str'
                '        WHERE ts.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))),'
                '    r AS (SELECT'
                '            d.lab_pair_str,'
                '            (-2.0 * d.r_c * SIN(2.0 * RADIANS(d.delta_ro)))'
                '        AS r_t'
                '        FROM d'
                '        WHERE d.lab_pair_str = ('
                '            CAST($1 AS VARCHAR) || \',\' ||'
                '            CAST($2 AS VARCHAR) || \',\' ||'
                '            CAST($3 AS VARCHAR) || \',\' ||'
                '            CAST($4 AS VARCHAR) || \',\' ||'
                '            CAST($5 AS VARCHAR) || \',\' ||'
                '            CAST($6 AS VARCHAR))) '
                'SELECT'
                '        SQRT('
                '            POW(d.delta_lp / (d.s_l * $7), 2.0) +'
                '            POW(d.delta_cp / (d.s_c * $8), 2.0) +'
                '            POW(d.delta_hp / (d.s_h * $9), 2.0) +'
                '            r.r_t *'
                '            (d.delta_cp / (d.s_c * $8)) *'
                '            (d.delta_hp / (d.s_h * $9)))'
                '    AS delta_e_cie2000 '
                'FROM          r '
                'INNER JOIN    d '
                'ON            r.lab_pair_str = d.lab_pair_str '
                'WHERE         r.lab_pair_str = ('
                '          CAST($1 AS VARCHAR) || \',\' ||'
                '          CAST($2 AS VARCHAR) || \',\' ||'
                '          CAST($3 AS VARCHAR) || \',\' ||'
                '          CAST($4 AS VARCHAR) || \',\' ||'
                '          CAST($5 AS VARCHAR) || \',\' ||'
                '          CAST($6 AS VARCHAR))'
                ''
                ' $$ '
                ''
                'LANGUAGE SQL '
                'IMMUTABLE '
                'RETURNS NULL ON NULL INPUT')))

    db.session.commit()

    return (db.session
        .execute(
            text(
                'SELECT        c.rgb_r,'
                '              c.rgb_g,'
                '              c.rgb_b,'
                '        DELTA_E_CIE2000(:lab_l, :lab_a, :lab_b,'
                '                        c.lab_l, c.lab_a, c.lab_b,'
                '                        :kl, :kc, :kh)'
                '    AS de2000 '
                'FROM          color c '
                'WHERE         c.lab_l BETWEEN'
                '    :lab_l_low_threshold AND :lab_l_high_threshold '
                'AND           c.lab_a BETWEEN'
                '    :lab_a_low_threshold AND :lab_a_high_threshold '
                'AND           c.lab_b BETWEEN'
                '    :lab_b_low_threshold AND :lab_b_high_threshold '
                'ORDER BY      de2000 '
                'LIMIT         :limit'),
            dict(lab_l=lab_l,
                 lab_a=lab_a,
                 lab_b=lab_b,
                 kl=kl,
                 kc=kc,
                 kh=kh,
                 lab_l_low_threshold=(lab_l - range_threshold),
                 lab_l_high_threshold=(lab_l + range_threshold),
                 lab_a_low_threshold=(lab_a - range_threshold),
                 lab_a_high_threshold=(lab_a + range_threshold),
                 lab_b_low_threshold=(lab_b - range_threshold),
                 lab_b_high_threshold=(lab_b + range_threshold),
                 limit=limit)))


def delta_e_cie2000_query_old(lab_l, lab_a, lab_b, kl=1.0, kc=1.0, kh=1.0, limit=10):
    """
    Old version of delta_e_cie2000_query, that uses waaay too many
    nested subqueries, instead of the 'WITH' statement (CTEs).
    """

    from sqlalchemy import text

    from colorsearchtest.database import db

    r = (db.session
        .execute(
            text(
                'CREATE OR REPLACE FUNCTION '
                'DELTA_E_CIE2000(double precision, double precision,'
                '                double precision, double precision,'
                '                double precision, double precision,'
                '                double precision, double precision,'
                '                double precision) '
                'RETURNS double precision '
                'AS $$ '
                ''
                'SELECT    /*  r.rgb_r,'
                '              r.rgb_g,'
                '              r.rgb_b,'
                '              r.lab1_l,'
                '              r.lab1_a,'
                '              r.lab1_b,'
                '              r.lab2_l,'
                '              r.lab2_a,'
                '              r.lab2_b,'
                '              r.avg_lp,'
                '              r.c1,'
                '              r.c2,'
                '              r.g,'
                '              r.a1p,'
                '              r.a2p,'
                '              r.c1p,'
                '              r.c2p,'
                '              r.h1p,'
                '              r.h2p,'
                '              r.avg_c1p_c2p,'
                '              r.avg_hp,'
                '              r.t,'
                '              r.delta_hlp,'
                '              r.delta_lp,'
                '              r.delta_cp,'
                '              r.delta_hp,'
                '              r.s_l,'
                '              r.s_c,'
                '              r.s_h,'
                '              r.delta_ro,'
                '              r.r_c,'
                '              r.r_t, */ '
                ''
                '        SQRT('
                '            POW(r.delta_lp / (r.s_l * $7), 2.0) +'
                '            POW(r.delta_cp / (r.s_c * $8), 2.0) +'
                '            POW(r.delta_hp / (r.s_h * $9), 2.0) +'
                '            r.r_t *'
                '            (r.delta_cp / (r.s_c * $8)) *'
                '            (r.delta_hp / (r.s_h * $9)))'
                '    AS de2000 '
                'FROM          ('
                ''
                '    SELECT    /*  d.rgb_r,'
                '                  d.rgb_g,'
                '                  d.rgb_b, */'
                '                  d.lab1_l,'
                '                  d.lab1_a,'
                '                  d.lab1_b,'
                '                  d.lab2_l,'
                '                  d.lab2_a,'
                '                  d.lab2_b,'
                '                  d.avg_lp,'
                '                  d.c1,'
                '                  d.c2,'
                '                  d.g,'
                '                  d.a1p,'
                '                  d.a2p,'
                '                  d.c1p,'
                '                  d.c2p,'
                '                  d.h1p,'
                '                  d.h2p,'
                '                  d.avg_c1p_c2p,'
                '                  d.avg_hp,'
                '                  d.t,'
                '                  d.delta_hlp,'
                '                  d.delta_lp,'
                '                  d.delta_cp,'
                '                  d.delta_hp,'
                '                  d.s_l,'
                '                  d.s_c,'
                '                  d.s_h,'
                '                  d.delta_ro,'
                '                  d.r_c,'
                '            (-2.0 * d.r_c * SIN(2.0 * RADIANS(d.delta_ro)))'
                '        AS r_t'
                '    FROM          ('
                ''
                '    SELECT    /*  ts.rgb_r,'
                '                  ts.rgb_g,'
                '                  ts.rgb_b, */'
                '                  ts.lab1_l,'
                '                  ts.lab1_a,'
                '                  ts.lab1_b,'
                '                  ts.lab2_l,'
                '                  ts.lab2_a,'
                '                  ts.lab2_b,'
                '                  ts.avg_lp,'
                '                  ts.c1,'
                '                  ts.c2,'
                '                  ts.g,'
                '                  ts.a1p,'
                '                  ts.a2p,'
                '                  ts.c1p,'
                '                  ts.c2p,'
                '                  ts.h1p,'
                '                  ts.h2p,'
                '                  ts.avg_c1p_c2p,'
                '                  ts.avg_hp,'
                '                  ts.t,'
                '                  ts.delta_hlp,'
                '            ($4 - $1)'
                '        AS delta_lp,'
                '            (ts.c2p - ts.c1p)'
                '        AS delta_cp,'
                '            (2.0 * ('
                '                SQRT(ts.c2p * ts.c1p) *'
                '                SIN(RADIANS(ts.delta_hlp) / 2.0)))'
                '        AS delta_hp,'
                '            (1.0 + ('
                '                (0.015 * POW(ts.avg_lp - 50.0, 2.0)) /'
                '                SQRT(20.0 + POW(ts.avg_lp - 50.0, 2.0))))'
                '        AS s_l,'
                '            (1.0 + 0.045 * ts.avg_c1p_c2p)'
                '        AS s_c,'
                '            (1.0 + 0.015 * ts.avg_c1p_c2p * ts.t)'
                '        AS s_h,'
                '            (30.0 * EXP(-(POW(((ts.avg_hp - 275.0) / 25.0), 2.0))))'
                '        AS delta_ro,'
                '            SQRT('
                '                (POW(ts.avg_c1p_c2p, 7.0)) /'
                '                (POW(ts.avg_c1p_c2p, 7.0) + POW(25.0, 7.0)))'
                '        AS r_c'
                '    FROM          ('
                ''
                '    SELECT    /*  av.rgb_r,'
                '                  av.rgb_g,'
                '                  av.rgb_b, */'
                '                  av.lab1_l,'
                '                  av.lab1_a,'
                '                  av.lab1_b,'
                '                  av.lab2_l,'
                '                  av.lab2_a,'
                '                  av.lab2_b,'
                '                  av.avg_lp,'
                '                  av.c1,'
                '                  av.c2,'
                '                  av.g,'
                '                  av.a1p,'
                '                  av.a2p,'
                '                  av.c1p,'
                '                  av.c2p,'
                '                  av.h1p,'
                '                  av.h2p,'
                '                  av.avg_c1p_c2p,'
                '                  av.avg_hp,'
                '            (1.0 - '
                '                0.17 * COS(RADIANS(av.avg_hp - 30.0)) +'
                '                0.24 * COS(RADIANS(2.0 * av.avg_hp)) +'
                '                0.32 * COS(RADIANS(3.0 * av.avg_hp + 6.0)) -'
                '                0.2 * COS(RADIANS(4.0 * av.avg_hp - 63.0)))'
                '        AS t,'
                '            (('
                '                    (av.h2p - av.h1p) +'
                '                    (CASE'
                '                        WHEN (ABS(av.h2p - av.h1p) > 180.0)'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '                -'
                '                (CASE'
                '                    WHEN (av.h2p > av.h1p)'
                '                    THEN 720.0'
                '                    ELSE 0.0'
                '                    END))'
                '        AS delta_hlp'
                '    FROM          ('
                ''
                '    SELECT    /*  cphp.rgb_r,'
                '                  cphp.rgb_g,'
                '                  cphp.rgb_b, */'
                '                  cphp.lab1_l,'
                '                  cphp.lab1_a,'
                '                  cphp.lab1_b,'
                '                  cphp.lab2_l,'
                '                  cphp.lab2_a,'
                '                  cphp.lab2_b,'
                '                  cphp.avg_lp,'
                '                  cphp.c1,'
                '                  cphp.c2,'
                '                  cphp.g,'
                '                  cphp.a1p,'
                '                  cphp.a2p,'
                '                  cphp.c1p,'
                '                  cphp.c2p,'
                '                  cphp.h1p,'
                '                  cphp.h2p,'
                '            ((cphp.c1p + cphp.c2p) /'
                '                2.0)'
                '        AS avg_c1p_c2p,'
                '            (((CASE'
                '                WHEN (ABS(cphp.h1p - cphp.h2p) > 180.0)'
                '                THEN 360.0'
                '                ELSE 0.0'
                '                END) +'
                '              cphp.h1p +'
                '              cphp.h2p) /'
                '                2.0)'
                '        AS avg_hp'
                '    FROM          ('
                ''
                '    SELECT    /*  ap.rgb_r,'
                '                  ap.rgb_g,'
                '                  ap.rgb_b, */'
                '                  ap.lab1_l,'
                '                  ap.lab1_a,'
                '                  ap.lab1_b,'
                '                  ap.lab2_l,'
                '                  ap.lab2_a,'
                '                  ap.lab2_b,'
                '                  ap.avg_lp,'
                '                  ap.c1,'
                '                  ap.c2,'
                '                  ap.g,'
                '                  ap.a1p,'
                '                  ap.a2p,'
                '            SQRT('
                '                POW(ap.a1p, 2.0) +'
                '                POW($3, 2.0))'
                '        AS c1p,'
                '            SQRT('
                '                POW(ap.a2p, 2.0) +'
                '                POW($6, 2.0))'
                '        AS c2p,'
                '            ('
                '                DEGREES(ATAN2($3, ap.a1p)) + ('
                '                    CASE'
                '                        WHEN DEGREES(ATAN2($3, ap.a1p)) < 0.0'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '        AS h1p,'
                '            ('
                '                DEGREES(ATAN2($6, ap.a2p)) + ('
                '                    CASE'
                '                        WHEN DEGREES(ATAN2($6, ap.a2p)) < 0.0'
                '                        THEN 360.0'
                '                        ELSE 0.0'
                '                        END))'
                '        AS h2p'
                '    FROM          ('
                ''
                '    SELECT    /*  gs.rgb_r,'
                '                  gs.rgb_g,'
                '                  gs.rgb_b, */'
                '                  gs.lab1_l,'
                '                  gs.lab1_a,'
                '                  gs.lab1_b,'
                '                  gs.lab2_l,'
                '                  gs.lab2_a,'
                '                  gs.lab2_b,'
                '                  gs.avg_lp,'
                '                  gs.c1,'
                '                  gs.c2,'
                '                  gs.g,'
                '            ((1.0 + gs.g) * $2)'
                '        AS a1p,'
                '            ((1.0 + gs.g) * $5)'
                '        AS a2p'
                '    FROM          ('
                ''
                '    SELECT    /*  c.rgb_r,'
                '                  c.rgb_g,'
                '                  c.rgb_b, */'
                '                  c.lab1_l,'
                '                  c.lab1_a,'
                '                  c.lab1_b,'
                '                  c.lab2_l,'
                '                  c.lab2_a,'
                '                  c.lab2_b,'
                '                  c.avg_lp,'
                '                  c.c1,'
                '                  c.c2,'
                '            (0.5 *'
                '                (1.0 - SQRT('
                '                    POW(((c.c1 + c.c2) / 2.0), 7.0) / ('
                '                        POW(((c.c1 + c.c2) / 2.0), 7.0) +'
                '                        POW(25.0, 7.0)))))'
                '        AS g'
                '    FROM          ('
                ''
                '    SELECT    /*  s.rgb_r,'
                '                  s.rgb_g,'
                '                  s.rgb_b, */'
                '                  $1 AS lab1_l,'
                '                  $2 AS lab1_a,'
                '                  $3 AS lab1_b,'
                '                  $4 AS lab2_l,'
                '                  $5 AS lab2_a,'
                '                  $6 AS lab2_b,'
                '            (($1 + $4) /'
                '                2.0)'
                '        AS avg_lp,'
                '            SQRT('
                '                POW($2, 2.0) +'
                '                POW($3, 2.0))'
                '        AS c1,'
                ''
                '            SQRT('
                '                POW(($5), 2.0) +'
                '                POW(($6), 2.0))'
                '        AS c2'
                '    ) AS c'
                ''
                '    ) AS gs '
                ''
                '    ) AS ap '
                ''
                '    ) AS cphp '
                ''
                '    ) AS av '
                ''
                '    ) AS ts '
                ''
                '    ) AS d '
                ''
                '    ) AS r '
                ''
                ' $$ '
                ''
                'LANGUAGE SQL '
                'IMMUTABLE '
                'RETURNS NULL ON NULL INPUT')))

    db.session.commit()

    return (db.session
        .execute(
            text(
                'SELECT        c.rgb_r,'
                '              c.rgb_g,'
                '              c.rgb_b,'
                '        DELTA_E_CIE2000(:lab_l, :lab_a, :lab_b,'
                '                        c.lab_l, c.lab_a, c.lab_b,'
                '                        :kl, :kc, :kh)'
                '    AS de2000 '
                'FROM          color c '
                'ORDER BY      de2000 '
                'LIMIT         :limit'),
            dict(lab_l=lab_l,
                 lab_a=lab_a,
                 lab_b=lab_b,
                 kl=kl,
                 kc=kc,
                 kh=kh,
                 limit=limit)))
