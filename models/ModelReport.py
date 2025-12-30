from datetime import datetime
from models.ModelVnnox import ModelVnnox
import pdfkit
import platform
import io
import csv

model_vnnox = ModelVnnox()

from .ModelConfig import ModelConfig
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Python 3.8 

class ModelReport:

    def verifySystem(self):
        if platform.system() == "Windows":
            return r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        else:
            return r'/usr/local/bin/wkhtmltopdf'

    def requirementsPDF(self):
        now = datetime.now(ZoneInfo("America/Mexico_City"))
        #date = now.strftime("%d/%m/%Y")
        date= now.strftime("%Y-%m-%d")
        ruta_wkhtmltopdf = self.verifySystem()
        config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)

        return date, config
    

    def gen_pdf_vnnox(self, data, onlineStatus, offlineStatus, totalPlayers, TOKEN):
        date, config = self.requirementsPDF()

        try:
            header = self.header_pdf(onlineStatus, offlineStatus, totalPlayers)

            contenido_pdf = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #ffffff;
                    }}
                    .container {{
                        width: 100%;
                        text-align: center;
                    }}
                    .card {{
                        border: none;
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        width: 200px;
                        display: inline-block;
                        margin-right: 20px;
                        background-color: #EF5350;
                        color: #ffffff;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .card-total {{
                        background-color: #09BAF7;
                    }}
                    .card-online {{
                        background-color: #14C90B;
                    }}
                    .card-offline {{
                        background-color: #FA1010;
                    }}
                    table {{
                        width: 100%;
                        margin-top: 20px;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        border: 1px solid #000;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .circle {{
                        width: 15px;
                        height: 15px;
                        border-radius: 50%;
                        display: inline-block;
                    }}
                    .circle-green {{
                        background-color: #14C90B;
                    }}
                    .circle-red {{
                        background-color: #FA1010;
                    }}
                    .cell-yellow {{
                        background-color: #FFC107;
                    }}
                    .cell-red {{
                        background-color: #EF5350;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    {header}

                    <table>
                        <thead>
                            <tr>
                                <th>STORE</th>
                                <th>RACK SN</th>
                                <th>ONLINE STATUS</th>
                                <th>LAST ONLINE TIME</th>
                                <th>SOLUTION</th>
                                <th>VIDEO SOLUTION</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            for item in data:
                online_circle = "circle-green" if item["onlineStatus"] == 1 else "circle-red"

                last_online = datetime.strptime(item["lastOnlineTime"], "%Y-%m-%d %H:%M:%S")
                today = datetime.strptime(date, "%Y-%m-%d")
                diff_days = (today.date() - last_online.date()).days
                solution = model_vnnox.get_solution(TOKEN, item["sn"])

                if diff_days > 7:
                    row_class = "cell-red"
                elif diff_days > 3:
                    row_class = "cell-yellow"
                else:
                    row_class = ""

                contenido_pdf += f"""
                <tr class="{row_class}">
                    <td>{item["name"]}</td>
                    <td>{item["sn"]}</td>
                    <td><div class="circle {online_circle}"></div></td>
                    <td>{item["lastOnlineTime"]}</td>
                    <td>{solution}</td>
                    <td>
                        <img 
                            src="https://retailmibeex.net/apiVnnox/screenPlayers/{item['playerId']}.jpg"
                            width="250"
                            alt="No Screenshot"
                        >
                    </td>
                </tr>
                """

            contenido_pdf += """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """

            pdfkit_options = {
                "page-size": "A4",
                "encoding": "UTF-8",
            }

            pdf = pdfkit.from_string(
                contenido_pdf,
                False,
                configuration=config,
                options=pdfkit_options
            )

            return pdf

        except Exception as e:
            print("Error PDF:", e)
            return None

        
    def generate_csv_vnnox(self, data, token):
        columnas_deseadas = [
            "STORE",
            "RACK SN",
            "ONLINE STATUS",
            "LAST ONLINE TIME",
            "VIDEO SOLUTION",
            "SCREENSHOT URL"
        ]

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(columnas_deseadas)

        # Rows
        for item in data:
            # Get solution exactly like PDF
            solution = model_vnnox.get_solution(token, item["sn"])

            screenshot_url = (
                f"https://retailmibeex.net/apiVnnox/screenPlayers/"
                f"{item['playerId']}.jpg"
            )

            writer.writerow([
                item.get("name", ""),                # STORE
                item.get("sn", ""),                  # RACK SN
                "ONLINE" if item.get("onlineStatus") == 1 else "OFFLINE",
                item.get("lastOnlineTime", ""),
                solution,                            # VIDEO SOLUTION
                screenshot_url                       # SCREENSHOT URL
            ])

        return output

        
    def header_pdf(self, onlinePlayer, offlinePlayer, totalPlayers):
        now = datetime.now(ZoneInfo("America/Mexico_City"))
        date = now.strftime("%d/%m/%Y")
        contenido_pdf = f"""
            <div class="logo">
                <img src="https://www.retailmibeex.net/apiVnnox/black.jpg" alt="Logo">
            </div>
            <div class="date">Date: {date}</div>
            <div class="card card-total">
                <h2>Total Players</h2>
                <p>{totalPlayers}</p>
            </div>
            <div class="card card-online">
                <h2>Online</h2>
                <p>{onlinePlayer}</p>
            </div>
            <div class="card card-offline">
                <h2>Offline</h2>
                <p>{offlinePlayer}</p>
            </div>

            <div class="legend" style="text-align: left;">
                <h3>Status</h3>
                <div class="legend-item">
                    <span style="display:inline-block; width:20px; height:20px; background-color:#FFC107; margin-right:8px;"></span>
                    3 to 7 days
                </div>
                <div class="legend-item">
                    <span style="display:inline-block; width:20px; height:20px; background-color:red; margin-right:8px;"></span>
                    More than 7 days
                </div>
            </div>

        """
        return contenido_pdf
    
    def save_files(self, gen_pdf_content, gen_csv_content, NAME):
        if gen_pdf_content and gen_csv_content:
            # Guardar PDF
            with open(f"reports/{NAME}.pdf", "wb") as f:
                f.write(gen_pdf_content)
            print(f"PDF guardado como {NAME}.pdf")
            
            # Guardar CSV
            with open(f"reports/{NAME}.csv", "w", encoding="utf-8") as f:
                f.write(gen_csv_content.getvalue())
            print(f"CSV guardado como {NAME}.csv")
        else:
            print("No se generaron los archivos")
