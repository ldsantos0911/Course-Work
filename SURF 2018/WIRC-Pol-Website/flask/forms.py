from wtforms import Form, validators, SelectField, StringField, SubmitField, \
                    TextField, FieldList, FormField, DecimalField

values = ['Name', '2MASS Name', 'WISE Name', 'SDSS Name', 'PanSTARRS Name', 
'Other Name', 'RA (h:m:s)', 'Dec (d:m:s)', 'RA', 'DEC', 'SpT', 'SpT_Type', 
'Peculiarities', 'radius', 'e_radius', 'log_g', 'e_log_g', 'Teff', 'e_Teff', 
'Mass', 'e_Mass', 'Member', 'Quality', 'LACEwING', 'LACEwING probability', 
'D_Trig', 'e_D_Trig', 'pmRA', 'e_pmRA', 'pmDE', 'e_pmDE', 'HRV', 'e_HRV',
'Gaia_G', 'e_Gaia_G', "SDSS_u'", "e_SDSS_u'", "SDSS_g'", "e_SDSS_g'", 
"SDSS_r'", "e_SDSS_r'", "SDSS_i'", "e_SDSS_i'", "SDSS_z'", "e_SDSS_z'", 
'PanSTARRS_y', 'e_PanSTARRS_y', 'MKO_Y', 'e_MKO_Y', 'J', 'e_J', 'H', 'e_H', 
'K', 'e_K', 'MKO_J', 'e_MKO_J', 'MKO_H', 'e_MKO_H', 'MKO_K', 'e_MKO_K', 
"MKO_L'", "e_MKO_L'", 'IRAC3p6', 'e_IRAC3p6', 'IRAC4p5', 'e_IRAC4p5', 
'IRAC5p8', 'e_IRAC5p8', 'IRAC8', 'e_IRAC8', 'WISE_W1', 'e_WISE_W1', 'WISE_W2',
'e_WISE_W2', 'WISE_W3', 'e_WISE_W3', 'WISE_W4', 'e_WISE_W4', 'Variable', 
'e_Variable', 'Variable_period', 'e_Variable_period', 'Polarized Filter', 
'Polarized %', 'e_Polarized %', 'Polarized Angle', 'Q/I', 'e_Q/I', 'U/I', 
'e_U/I', 'InDwarfArchive', 'Comments', 'L_T Transition', 'Young', 'Variable%', 
'Polarization', 'Priority', 'Declination', 'Visible', 'Varflag', 'Polflag', 
'Ltflag', 'Jflag', 'Ranking', 'Star', 'Min', 'Max', 'R', 'Instrument', 
'Source', 'Filename', 'Filename2', 'Sp Note']

choices = []
for value in values:
    choices.append((value, value))

conditions = [('=', 'equals'), ('>', 'is greater than'), ('<', 
              'is less than'), ('range', 'is in range'), ('in', 'contains')]

class QueryForm(Form):
    field = SelectField(u'Field', [validators.InputRequired()], choices=choices)
    condition = SelectField(u'Condition', [validators.InputRequired()], choices=conditions)
    query = StringField(u'Query', [validators.DataRequired()])

class QueriesForm(Form):
    view = TextField(u'View', [validators.DataRequired()])
    queries = FieldList(FormField(QueryForm), min_entries=1, max_entries=10)
    submit = SubmitField(u'Submit')

class FindingForm(Form):
    name = StringField(u'Name')
    RA = DecimalField(u'RA')
    Dec = DecimalField(u'DEC')
    submit = SubmitField(u'Create')
    