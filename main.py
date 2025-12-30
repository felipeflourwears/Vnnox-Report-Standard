from models.ModelConfig import ModelConfig
from models.ModelToken import ModelToken
from models.ModelVnnox import ModelVnnox
from models.ModelReport import ModelReport
from models.ModelS3 import ModelS3
from models.ModelMail import ModelMail

model_config = ModelConfig()
model_token = ModelToken()
model_vnnox = ModelVnnox()
model_report = ModelReport()
model_s3 = ModelS3()
model_mail = ModelMail()


TOKEN = ModelToken.getTokenDB()
NAME = "ReportPlayers"


def main(TOKEN, NAME):
    print("Starting Generate Report")
    
    name_players = [
        "presidente 61 Miami ZD0122400016", 
        "presidente 44 Miami",
        "Presidente 14 Miami",
        "presidente 19",
        "presidente 62 Miami",
        "presidente 21 miami",
        "presidente 35",
        "presidente 3 miami"
    ]
    data_players, players_ids = model_vnnox.get_players_data(TOKEN, name_players)
    #print(data_players)
    #print(players_ids)

    total_players, online_count, offline_count = model_vnnox.request_data_info_analytics(data_players)
    #print(total_players, online_count, offline_count)

    #Get Screenshot in realtime
    model_vnnox.get_screen_player(TOKEN, players_ids)


    #test = model_vnnox.get_solution(TOKEN, "ZD0122400016")
    #print("SOLUTION:", test)

    gen_pdf_content = model_report.gen_pdf_vnnox(data_players, online_count, offline_count, total_players, TOKEN)
    gen_csv_content = model_report.generate_csv_vnnox(data_players, TOKEN)
    save_files = model_report.save_files(gen_pdf_content, gen_csv_content, NAME)

if __name__ == "__main__":
    main(TOKEN, NAME)
