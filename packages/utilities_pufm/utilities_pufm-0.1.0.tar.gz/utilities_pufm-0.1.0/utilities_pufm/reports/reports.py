# import pdfkit
# from prints.rich import custom_print
# from utilities.time.time import get_current_time

# class MigrationReport:
#     _instance = None

#     def __new__(cls):
#         # Verifica se uma instância já existe; se não, cria uma nova
#         if cls._instance is None:
#             cls._instance = super(MigrationReport, cls).__new__(cls)
#             cls._instance._initialized = False  # Inicializa apenas uma vez
#         return cls._instance
    
#     def __init__(self) -> None:
#         self.config_pdf = pdfkit.configuration(wkhtmltopdf="./report/wkhtmltopdf.exe")
#         self.report_init = []
#         self.timestamp = get_current_time()
#         tables_visits = []

#     def print_and_report(self, text: list, report: object, rich: bool = False, colors: list = ["yellow"]) -> None:
        
#         custom_print(text=''.join(text), rich=True, colors=colors)
        
#         gerar_relatorio(text=text, report=report, rich=rich)
    
# def gerar_relatorio(list_msg: list = None, local: str = None):
    
#     if local == "init":
#         report_init.extend(list_msg)
# # 
#     html_content = f"""
#     <html lang="pt-BR">
#     <head>
#         <meta charset="UTF-8">
#     </head>
#     <body>
#         <p>Prezados,</p>
#         <p>A seguir o relatório da migração em andamento realizada em {timestamp}.</p>
#         <h3>Visão Geral:</h3>
#         <p>{''.join(it+'<br/>' for it in report_init)}</p>
#         <h3>Migração das Tabelas:</h3>
#         {''.join('<h4>'+d['table']+'</h4>'+d['info']+format_list(d['coments'])+format_list(d['reports']) for d in tables_visits)}

#         <p>Atenciosamente,<br/>PROTIC,</p>
#     </body>
#     </html>
#     """

#     html_filename = os.path.join(config.config["html_dir"], f"relatorio_migration_{timestamp}.html")
#     with open(html_filename, "w", encoding="utf-8") as file:
#         file.write(html_content)
#     print(f"[REPORT]: Relatório HTML salvo como: {html_filename}")

#     pdf_filename = os.path.join(config.config["pdf_dir"], f"relatorio_migration_{timestamp}.pdf")
#     pdfkit.from_file(html_filename, pdf_filename, configuration=config_pdf)
#     print(f"[REPORT]: Relatório PDF salvo como: {pdf_filename}")