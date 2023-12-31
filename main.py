import os
import flet as ft
import configparser
from util import Util

utl = Util()
cfg = configparser.ConfigParser()
if not os.path.exists('cfg.ini'):
    with open('cfg.ini', 'w') as file:
        file.write('[DEFAULT]' + '\n')
        utl.update_cfg(secao='DEFAULT', chave='pasta_download', new='')
cfg.read('cfg.ini')
def pages(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.window_width = 1550
    page.title = "Arquivos SimAm Robô V_1.0.0"
    progressBar = ft.ProgressBar(width=700,color=ft.colors.GREEN_ACCENT_700)

    lista_exercicio = []
    lista_competencias = []

    def start(e):
        utl.update_cfg(secao='DEFAULT', chave='pasta_download', new=txt_pasta_daownload.value)
        utl.update_cfg(new=txt_pasta_daownload.value)
        cfg.read('cfg.ini')
        for i in exercecios.controls:
            if i.value:
                lista_exercicio.append(int(i.label))

        for i in competencias.controls:
            if i.value:
                lista_competencias.append(i.label)

        if not txt_user.value:
            txt_user.error_text = "Informe os dados de credenciais."
            page.update()
        else:
            exercecios.disabled = True
            ex_all.disabled = True
            comp_all.disabled = True
            competencias.disabled = True
            page.add(progressBar)
            btn_start.disabled=True
            page.update()
            from consulta import Consulta
            t = Consulta()
            t.start(lista_exercicio, lista_competencias, txt_user.value, txt_password.value)
            progressBar.value=100
            exercecios.disabled = False
            ex_all.disabled = False
            comp_all.disabled = False
            competencias.disabled = False
            btn_start.disabled = False
            page.add(txt_footer)
            page.update()

    def checkbox_changed_exercicio(e):
        ex_2013.value=ex_all.value
        ex_2014.value=ex_all.value
        ex_2015.value=ex_all.value
        ex_2016.value=ex_all.value
        ex_2017.value=ex_all.value
        ex_2018.value=ex_all.value
        ex_2019.value=ex_all.value
        ex_2020.value=ex_all.value
        ex_2021.value=ex_all.value
        ex_2022.value=ex_all.value
        ex_2023.value=ex_all.value
        ex_2024.value=ex_all.value
        page.update()

    def checkbox_changed_competencia(e):
        abertura.value = comp_all.value
        janeiro.value = comp_all.value
        fevereiro.value = comp_all.value
        marco.value = comp_all.value
        abril.value = comp_all.value
        maio.value = comp_all.value
        junho.value = comp_all.value
        julho.value = comp_all.value
        agosto.value = comp_all.value
        setembro.value = comp_all.value
        outubro.value = comp_all.value
        novembro.value = comp_all.value
        dezembro.value = comp_all.value
        fechamento.value = comp_all.value
        page.update()

    page.add(ft.Text("Arquivos Sim Am", size=20, color='blue'))
    txt_user = ft.TextField(label="User", text_size=12, width=250, height=35)
    txt_password = ft.TextField(label="Password", text_size=12, width=250, height=35, password=True, can_reveal_password=True)
    txt_pasta_daownload = ft.TextField(label="Pasta de download padão do navegador", value=cfg['DEFAULT']['pasta_download'],text_size=12, width=700, height=35)
    txt_footer = ft.Text("Processo Finalizado", size=20, color='green')
    divisor = ft.Divider(height=2, thickness=3)

    btn_start = ft.ElevatedButton("Iniciar", on_click=start, icon=ft.icons.DOWNLOADING)

    ex_all = ft.Checkbox(label="Todos", value=False, on_change=checkbox_changed_exercicio)
    ex_2013 = ft.Checkbox(label="2013", value=True)
    ex_2014 = ft.Checkbox(label="2014", value=False)
    ex_2015 = ft.Checkbox(label="2015", value=False)
    ex_2016 = ft.Checkbox(label="2016", value=False)
    ex_2017 = ft.Checkbox(label="2017", value=False)
    ex_2018 = ft.Checkbox(label="2018", value=False)
    ex_2019 = ft.Checkbox(label="2019", value=False)
    ex_2020 = ft.Checkbox(label="2020", value=False)
    ex_2021 = ft.Checkbox(label="2021", value=False)
    ex_2022 = ft.Checkbox(label="2022", value=False)
    ex_2023 = ft.Checkbox(label="2023", value=False)
    ex_2024 = ft.Checkbox(label="2024", value=False)

    exercecios = ft.Row([ex_2013,ex_2014, ex_2015,ex_2016,ex_2017,ex_2018, ex_2019,ex_2020,ex_2021,ex_2022, ex_2023,ex_2024])

    comp_all = ft.Checkbox(label="Todas", value=False, on_change=checkbox_changed_competencia)
    abertura = ft.Checkbox(label="Abertura de Exercício", value=True)
    janeiro = ft.Checkbox(label="Janeiro", value=False)
    fevereiro = ft.Checkbox(label="Fevereiro", value=False)
    marco = ft.Checkbox(label="Março", value=False)
    abril = ft.Checkbox(label="Abril", value=False)
    maio = ft.Checkbox(label="Maio", value=False)
    junho = ft.Checkbox(label="Junho", value=False)
    julho = ft.Checkbox(label="Julho", value=False)
    agosto = ft.Checkbox(label="Agosto", value=False)
    setembro = ft.Checkbox(label="Setembro", value=False)
    outubro = ft.Checkbox(label="Outubro", value=False)
    novembro = ft.Checkbox(label="Novembro", value=False)
    dezembro = ft.Checkbox(label="Dezembro", value=False)
    fechamento = ft.Checkbox(label="Encerramento de Exercício", value=False)

    competencias = ft.Row([abertura, janeiro, fevereiro, marco, abril, maio, junho, julho, agosto, setembro, outubro, novembro, dezembro, fechamento])

    list_arquivos = ft.ListView(expand=1, spacing=2, padding=20, auto_scroll=True)

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,

        tabs=[
            ft.Tab(
                text="Credenciais",
                icon=ft.icons.POLICY,
                content=ft.Container(
                                    content=ft.Column([txt_pasta_daownload, ex_all, exercecios, comp_all, competencias, txt_user, txt_password, btn_start]),
                                    alignment=ft.alignment.center,
                                    padding=15
                                    ),
            ),
        ],
        expand=1,
    )

    page.add(t)


if __name__ == "__main__":
    # ft.app(port=3636, target=main, view=ft.WEB_BROWSER)
    ft.app(target=pages)

#  pyinstaller --name Sim_Am_robo_V_1.0.0 --onefile --icon=robo.ico --noconsole main.py
# flet pack --name Sim_Am_robo_V_1.0.0 --icon=robo.ico main.py