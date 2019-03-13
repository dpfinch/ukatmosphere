import dash_html_components as html
import dash_core_components as dcc

def test_string():
     s= """Yet bed any for travelling assistance indulgence unpleasing.
     Not thoughts all exercise blessing. Indulgence way everything
     joy alteration boisterous the attachment. Party we years to order
     allow asked of. We so opinion friends me message as delight. Whole
     front do of plate heard oh ought. His defective nor convinced
     residence own. Connection has put impossible own apartments boisterous.
     At jointure ladyship an insisted so humanity he. Friendly bachelor
     entrance to on by.
    Are own design entire former get should. Advantages boisterous day
    excellence boy. Out between our two waiting wishing. Pursuit he he
    garrets greater towards amiable so placing. Nothing off how norland
     delight. Abode shy shade she hours forth its use. Up whole of fancy ye quiet do.
     Justice fortune no to is if winding morning forming.
    Rooms oh fully taken by worse do. Points afraid but may end law lasted.
    Was out laughter raptures returned outweigh. Luckily cheered colonel me
      entrance to on by.
    Are own design entire former get should. Advantages boisterous day excellence
     boy. Out between our two waiting wishing. Pursuit he he garrets greater
     towards amiable so placing. Nothing off how norland delight. Abode shy shade"""
     return s

def test_string2():
    s = html.Div([
    html.P("""
    Yet bed any for travelling assistance indulgence unpleasing.
     Not thoughts all exercise blessing. Indulgence way everything
     joy alteration boisterous the attachment. Party we years to order
     allow asked of. We so opinion friends me message as delight. Whole
     front do of plate heard oh ought. His defective nor convinced
     residence own. Connection has put impossible own apartments boisterous.
     At jointure ladyship an insisted so humanity he. Friendly bachelor
     entrance to on by."""),
     html.P("""
         Are own design entire former get should. Advantages boisterous day
    excellence boy. Out between our two waiting wishing. Pursuit he he
    garrets greater towards amiable so placing. Nothing off how norland
     delight. Abode shy shade she hours forth its use. Up whole of fancy ye quiet do.
     Justice fortune no to is if winding morning forming.
    Rooms oh fully taken by worse do. Points afraid but may end law lasted.
    Was out laughter raptures returned outweigh. Luckily cheered colonel me
      entrance to on by
        """)])

    return s
