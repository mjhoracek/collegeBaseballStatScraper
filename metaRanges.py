def metaRanges(array):

    # Hitter Ranges
    avg = []
    obp = []
    slg = []
    ops = []
    gp = []
    ab = []
    rH = []
    hH = []
    doubles = []
    triples = []
    homers = []
    rbi = []
    hpH = []
    walks = []
    strikeouts = []
    sb = []
    cs = []

    # Pitcher Ranges
    w = []
    l = []
    era = []
    app = []
    gs = []
    cg = []
    sho = []
    sv = []
    ip = []
    hP = []
    rP = []
    er = []
    bb = []
    so = []
    wp = []
    hpP = []
    oba = []

    index = 0
    while index < len(array):
        if 'AVG' in array[index]:
            avg.append(array[index]["AVG"])
            obp.append(array[index]['OBP'])
            slg.append(array[index]['SLG'])
            ops.append(array[index]['OPS'])
            gp.append(array[index]['GP'])
            ab.append(array[index]['AB'])
            rH.append(array[index]['R'])
            hH.append(array[index]['H'])
            doubles.append(array[index]['2B'])
            homers.append(array[index]['HR'])
            rbi.append(array[index]['RBI'])
            hpH.append(array[index]['HP'])
            walks.append(array[index]['BB'])
            strikeouts.append(array[index]['SO'])
            sb.append(array[index]['SB'])
            cs.append(array[index]['CS'])
            triples.append(array[index]['3B'])
        if 'W' in array[index]:
            w.append(array[index]['W'])
            l.append(array[index]['L'])
            era.append(array[index]['ERA'])
            app.append(array[index]['APP'])
            gs.append(array[index]['GS'])
            cg.append(array[index]['CG'])
            sho.append(array[index]['SHO'])
            sv.append(array[index]['SV'])
            ip.append(array[index]['IP'])
            hP.append(array[index]['H'])
            rP.append(array[index]['R'])
            er.append(array[index]['ER'])
            bb.append(array[index]['BB'])
            so.append(array[index]['SO'])
            wp.append(array[index]['WP'])
            hpP.append(array[index]['HP'])
            oba.append(array[index]['OBA'])
        index += 1;
    

    pitchers = {
        'W' : [min(w), max(w)],
        'L' : [min(l), max(l)],
        'ERA' : [min(era), max(era)],
        'APP' : [min(app), max(app)],
        'GS' : [min(gs), max(gs)],
        'CG' : [min(cg), max(cg)],
        'SHO' : [min(sho), max(sho)],
        'SV' : [min(sv), max(sv)],
        'IP' : [min(w), max(w)],
        'H' : [min(w), max(w)],
        'R' : [min(w), max(w)],
        'ER' : [min(w), max(w)],
        'BB' : [min(w), max(w)],
        'SO' : [min(w), max(w)],
        'WP' : [min(w), max(w)],
        'HP' : [min(w), max(w)],
        'OBA' : [min(w), max(w)],
    }

    hitters = {
        'AVG' : [min(avg), max(avg)],
        'OBP' : [min(obp), max(obp)],
        'SLG' : [min(slg), max(slg)],
        'OPS' : [min(ops), max(ops)],
        'GP' : [min(gp), max(gp)],
        'AB' : [min(ab), max(ab)],
        'R' : [min(rH), max(rH)],
        'H' : [min(hH), max(hH)],
        '2B' : [min(doubles), max(doubles)],
        'HR' : [min(homers), max(homers)],
        'RBI' : [min(rbi), max(rbi)],
        'HP' : [min(hpH), max(hpH)],
        'BB' : [min(walks), max(walks)],
        'SO' : [min(strikeouts), max(strikeouts)],
        'SB' : [min(sb), max(sb)],
        'CS' : [min(cs), max(cs)],
        '3B' : [min(triples), max(triples)],
    }

    ranges = {
        'hitters' : hitters,
        'pitchers' : pitchers
    }

    return ranges