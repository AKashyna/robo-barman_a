
import dash
from dash import html, dcc, Input, Output, State, dash_table
from plotly.subplots import make_subplots
import plotly.graph_objs as go

# Dane
grawitacja = 9.81  # m/s^2
masa_drona = 0.5  # kg
okres_probkowania = 0.1  # s
maksymalna_sila_silnika = 25  # N
wspolczynnik_oporu_powietrza = 0.54
powierzchnia_drona = 0.12 # m^2
gestosc_powietrza = 1.225 # kg/m³ dla 15 stopni - wikipedia

maksymalny_sygnal_sterujacy = 50
maksymalna_wysokosc = 120 #m
maksymalny_czas = 100 #s

docelowe_wysokosci = [(0, 10), (15, 20), (20, 30), (30, 15)] #(czas, wysokosc)

czas_symulacji = 20  # s
wzmocnienie = 5  # reguluje część proporcjonalną
czas_zdwojenia = 15  # s reguluje część całkującą
czas_wyprzedzenia = 0.75  # s reguluje część różniczkującą

# Funkcja symulująca lot drona
def symuluj_lot_drona(maksymalna_sila_silnika, grawitacja, masa_drona,
                      okres_probkowania, czas_symulacji,
                      wzmocnienie, maksymalny_sygnal_sterujacy, docelowe_wysokosci, czas_zdwojenia, czas_wyprzedzenia):

    docelowa_wysokosc = docelowe_wysokosci[0][1]
    docelowe_wysokosci.pop(0)

    uplyw_czasu = 0  # s
    aktualna_wysokosc = 0  # m
    aktualna_predkosc = 0 # m/s
    aktualne_przyspieszenie = 0 # m/s^2
    roznica = docelowa_wysokosc - aktualna_wysokosc  # m
    sygnal_sterujacy = 0

    probki_czasu = [uplyw_czasu]
    wysokosci = [aktualna_wysokosc]
    roznice_wysokosci = [roznica]
    planowane_wysokosci = []
    sygnaly = [sygnal_sterujacy]
    hipotetyczne_sygnaly = [sygnal_sterujacy]
    predkosci = [aktualna_predkosc]
    przyspieszenia = [aktualne_przyspieszenie]

    while uplyw_czasu <= czas_symulacji:
        if len(docelowe_wysokosci) > 0 and uplyw_czasu >= docelowe_wysokosci[0][0]:
            docelowa_wysokosc = docelowe_wysokosci[0][1]
            docelowe_wysokosci.pop(0)

        # REGULATOR PID
        roznica = docelowa_wysokosc - aktualna_wysokosc

        czesc_proporcjonalna = roznice_wysokosci[-1]
        czesc_calkujaca = (okres_probkowania / czas_zdwojenia) * sum(roznice_wysokosci)
        czesc_rozniczkujaca = (czas_wyprzedzenia / okres_probkowania) * (roznica - roznice_wysokosci[-1])

        hipotetyczny_sygnal_sterujacy = max(wzmocnienie * (czesc_proporcjonalna + czesc_calkujaca + czesc_rozniczkujaca), 0)
        sygnal_sterujacy = min(hipotetyczny_sygnal_sterujacy, maksymalny_sygnal_sterujacy)
        sila_unoszenia = maksymalna_sila_silnika * sygnal_sterujacy / maksymalny_sygnal_sterujacy

        # SYMULACJA SYSTEMU
        sgn = 0
        if predkosci[-1] < 0:
            sgn = -1
        if predkosci[-1] > 0:
            sgn = 1
        aktualne_przyspieszenie = (sila_unoszenia / masa_drona) - grawitacja - ((0.5 * wspolczynnik_oporu_powietrza * powierzchnia_drona * gestosc_powietrza * pow(predkosci[-1], 2) * sgn) / masa_drona)
        aktualna_predkosc = aktualne_przyspieszenie * okres_probkowania + predkosci[-1]
        aktualna_wysokosc = predkosci[-1] * okres_probkowania + wysokosci[-1]

        aktualna_wysokosc = min(max(aktualna_wysokosc, 0),maksymalna_wysokosc)
        if aktualna_wysokosc == 0:
            aktualna_predkosc = max(aktualna_predkosc, 0)

        # REJESTRACJA DANYCH
        uplyw_czasu += okres_probkowania

        wysokosci.append(aktualna_wysokosc)
        probki_czasu.append(uplyw_czasu)
        roznice_wysokosci.append(roznica)
        planowane_wysokosci.append(docelowa_wysokosc)
        sygnaly.append(sygnal_sterujacy)
        hipotetyczne_sygnaly.append(hipotetyczny_sygnal_sterujacy)
        predkosci.append(aktualna_predkosc)
        przyspieszenia.append(aktualne_przyspieszenie)

    return {
        "time_samples": probki_czasu,
        "altitudes": wysokosci,
        "altitude_differences": roznice_wysokosci,
        "target_altitudes": planowane_wysokosci,
        "signals": sygnaly,
        "hypothetical_signals": hipotetyczne_sygnaly,
        "velocities": predkosci,
        "accelerations": przyspieszenia
    }

# Funkcja do rysowania wykresów
def rysuj_wysokosc(dane, tytul):
    wykres = make_subplots()
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["altitudes"], mode='lines', name='Wysokość aktualna', line=dict(color='blue')))
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["target_altitudes"], mode='lines', name='Wysokość docelowa', line=dict(dash='dash', color='black')))
    wykres.update_layout(title=tytul)
    wykres.update_xaxes(title_text="Czas [s]")
    wykres.update_yaxes(title_text="Wysokość [m]")
    return wykres

def rysuj_predkosc(dane, tytul):
    wykres = make_subplots(specs=[[{"secondary_y": True}]])
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["velocities"], mode='lines', name='Prędkość', line=dict(color='red')), secondary_y=False)
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["accelerations"], mode='lines', name='Przyspieszenie', line=dict(color='purple')),secondary_y=True)
    wykres.update_layout(title=tytul)
    wykres.update_xaxes(title_text="Czas [s]")
    wykres.update_yaxes(title_text="Prędkość [m/s]", secondary_y=False)
    wykres.update_yaxes(title_text="Przyspieszenie [m/s²]", secondary_y=True)
    return wykres

def rysuj_sygnaly(dane, tytul):
    wykres = make_subplots()
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["signals"], mode='lines', name='Rzeczywisty sygnał sterujący', line=dict(color='green')))
    wykres.add_trace(go.Scatter(x=dane["time_samples"], y=dane["hypothetical_signals"], mode='lines', name='Hipotetyczny sygnał sterujący', line=dict(color='orange')))
    wykres.update_layout(title=tytul)
    wykres.update_xaxes(title_text="Czas [s]")
    wykres.update_yaxes(title_text="Rzeczywisty sygnał sterujący")
    return wykres

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)
app.title = "Symulacja lotu drona"

app.layout = html.Div([
    html.Div([
        html.Div([

            html.Div([
                html.Button('Symuluj lot drona', id='przycisk-symulacji', n_clicks=0),
            ],style={'width': '90%', 'display': 'flex', 'padding': '10px', 'vertical-align': 'top', 'justify-content' : 'center' }),
            html.Div([
                dash_table.DataTable(id='tabela-docelowych-wysokosci',
                                     columns=[
                                         {"name": "Czas", "id": "czas"},
                                         {"name": "Docelowa wysokość", "id": "wysokosc"}
                                     ],
                                     data=[{"czas": czas, "wysokosc": wysokosc} for czas, wysokosc in docelowe_wysokosci],
                                     editable=True
                                     )
            ], style={'width': '90%', 'display': 'inline-block', 'padding': '10px', 'vertical-align': 'top'}),

            html.Div([
                html.Div([
                    html.Label("Czas symulacji:"),
                    dcc.Slider(id='suwak-czasu-symulacji', min=0, max=100, step=10, value=40),
                    html.Div(id='wyjscie-czasu-symulacji')
                ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'}),

                html.Div([
                    html.Label("Wzmocnienie:"),
                    dcc.Slider(id='suwak-wzmocnienia-sygnalu', min=0, max=25, step=2.5, value=5),
                    html.Div(id='wyjscie-wzmocnienia-sygnalu')
                ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'}),

                html.Div([
                    html.Label("Czas zdwojenia:"),
                    dcc.Slider(id='suwak-czasu-zdwojenia', min=0, max=50, step=5, value=15),
                    html.Div(id='wyjscie-czasu-zdwojenia')
                ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'}),

                html.Div([
                    html.Label("Czas wyprzedzenia:"),
                    dcc.Slider(id='suwak-czasu-wyprzedzenia', min=0, max=2.5, step=0.25, value=0.75),
                    html.Div(id='wyjscie-czasu-wyprzedzenia')
                ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'}),

            ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '100%'}),

        ],style={'display': 'inline-block', 'vertical-align': 'top', 'width': '30%'}),

        html.Div([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Wysokość', children=[
                    dcc.Graph(id='wykres-wysokosci')
                ]),
                dcc.Tab(label='Prędkość', children=[
                    dcc.Graph(id='wykres-predkosci')
                ]),
                dcc.Tab(label='Sygnały sterujące', children=[
                    dcc.Graph(id='wykres-sterujacy')
                ]),
            ]),
        ],style={'display': 'inline-block', 'vertical-align': 'top', 'width': '70%'}),

    ],id='sekcja-robocza'),
])

@app.callback(
    [Output('wykres-wysokosci', 'figure'),
     Output('wykres-predkosci', 'figure'),
     Output('wykres-sterujacy', 'figure')],
    [Input('przycisk-symulacji', 'n_clicks'),
     Input('tabela-docelowych-wysokosci', 'data')],
    [State('suwak-czasu-symulacji', 'value'),
     State('suwak-wzmocnienia-sygnalu', 'value'),
     State('suwak-czasu-zdwojenia', 'value'),
     State('suwak-czasu-wyprzedzenia', 'value')]
)

def aktualizuj_wyniki(n_clicks, tabela, czas_symulacji, wzmocnienie, czas_zdwojenia, czas_wyprzedzenia):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate

    docelowe_wysokosci = [(max(float(row['czas']), 0), max(0, float(row['wysokosc']))) for row in tabela]
    docelowe_wysokosci = sorted(docelowe_wysokosci, key=lambda x: (x[0], x[1]))
    docelowe_wysokosci_unikalne = [docelowe_wysokosci[0]]
    for i in range(1, len(docelowe_wysokosci)):
        if docelowe_wysokosci[i][0] != docelowe_wysokosci[i - 1][0]:
            docelowe_wysokosci_unikalne.append(docelowe_wysokosci[i])

    wyniki = symuluj_lot_drona(maksymalna_sila_silnika, grawitacja, masa_drona,
                               okres_probkowania, czas_symulacji,
                               wzmocnienie, maksymalny_sygnal_sterujacy, docelowe_wysokosci_unikalne,
                               czas_zdwojenia, czas_wyprzedzenia)

    wykres_wysokosci = rysuj_wysokosc(wyniki, 'Wysokość drona w czasie')
    wykres_predkosci = rysuj_predkosc(wyniki, 'Prędkość i przyspieszenie drona w czasie')
    wykres_sterujacy = rysuj_sygnaly(wyniki, 'Sygnały sterujące drona w czasie')

    return wykres_wysokosci, wykres_predkosci, wykres_sterujacy

if __name__ == '__main__':
    app.run_server(debug=True)
