import json
import matplotlib.pyplot as grafico
from server import TelemetryListener
from numpy import NaN
import numpy as np
def _get_listener():
    try:
        print('Starting listener on localhost:20778')
        return TelemetryListener()
    except OSError as exception:
        print(f'Unable to setup connection: {exception.args[1]}')
        print('Failed to open connector, stopping.')
        exit(127)


def dati(merlofx, boomshoot, sambov, N_players):
    listener = _get_listener()

    lista = [merlofx, boomshoot, sambov]
    temp = {}
    track_length = 0
    try:

        while True:
            packet = listener.get()
            dati = packet.to_dict()

            for i, j in dati.items():
                if i == "track_length":
                    if track_length == 0:
                        track_length = j

                if i == 'lap_data':
                    for DizionarioLapData in j:
                        for t, z in DizionarioLapData.items():
                            for giocatore in lista:

                                if giocatore["Car_ID"] == j.index(DizionarioLapData):
                                    if t == "current_lap_num" and z == giocatore["lap"] + 1:
                                        giocatore["lap"] = giocatore["lap"] + 1

                                    if t == "total_distance":
                                        if track_length != 0:
                                            lapfloat = z/track_length
                                            lapfloat1 = round(lapfloat, 1)
                                            if lapfloat1 not in giocatore["floatLap"] and len(giocatore["floatLap"]) < int(N_laps/0.1) + 1:
                                                giocatore["floatLap"].append(lapfloat1)



                if i == 'car_idx':
                    print("card ID:", j)
                    count = 0
                    for r in lista:
                        for key, val in r.items():
                            for key1, val1 in temp.items():
                                if key == key1 and val == val1:
                                    count = count + 1

                    if count == 4:
                        continue

                    for r in lista:
                        if j != 0:

                            if r['Car_ID'] == j - 1:
                                for key, val in r.items():
                                    for key1, val1 in temp.items():
                                        if key == key1:
                                            if temp[key1] not in r[key1]:
                                                r[key].append(temp[key1])

                                print(r)

                        else:
                            if r['Car_ID'] == N_players - 1:
                                for key, val in r.items():
                                    for key1, val1 in temp.items():
                                        if key1 == key:
                                            if temp[key1] not in r[key1]:
                                                r[key].append(temp[key1])
                                print(r)



                if i == 'lap_history_data':
                    print()
                    a = False

                    temp = {}

                    if isinstance(j, list) == True: #j lista di dizionari con tutti i giri rilevati
                        for s in j:
                            for t, z in s.items():
                                if z != 0:
                                    print(t, ":", z, end=", ")
                                    temp[t] = z
                                    a = True
                                else:
                                    a = False
                            if a:
                                print()
                if i == 'car_status_data':

                    for DizionarioStatusData in j:
                        for z, k in DizionarioStatusData.items():

                            if z == "visual_tyre_compound":
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(DizionarioStatusData) and len(giocatore["Tyre"]) < giocatore["lap"]:
                                        giocatore["Tyre"].append(k)


                            elif z == 'tyres_age_laps':
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(DizionarioStatusData) and len(giocatore["TyreAge"]) < giocatore["lap"]:
                                        giocatore["TyreAge"].append(k)

                            elif z == 'fuel_in_tank':
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(DizionarioStatusData) and len(giocatore["fuel"]) < len(giocatore["floatLap"]):
                                        giocatore["fuel"].append(k)

                            elif z == 'ers_store_energy':
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(DizionarioStatusData) and len(giocatore["ers_energy"]) < len(giocatore["floatLap"]):
                                        giocatore["ers_energy"].append(k)
                if i == 'classification_data':
                    for dizionario in j:
                        for key, val in dizionario.items():
                            if key == 'tyre_stints_visual':
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(dizionario):
                                        for tyre in val:
                                            if tyre != 0:
                                                giocatore["EndTyre"] = tyre
                                print(key, val)
                if i == 'car_damage_data':
                    for dizionario in j:
                        for key, val in dizionario.items():
                            if key == 'tyres_damage':
                                for giocatore in lista:
                                    if giocatore["Car_ID"] == j.index(dizionario) and len(giocatore["FrontDamage"]) < len(giocatore["floatLap"]):
                                        giocatore["FrontDamage"].append((val[2] + val[3])/2.0)
                                    if giocatore["Car_ID"] == j.index(dizionario) and len(giocatore["RearDamage"]) < len(giocatore["floatLap"]):
                                        giocatore["RearDamage"].append((val[0] + val[1])/2.0)




    except KeyboardInterrupt:
        print('Stop the car, stop the car Checo.')
        print('Stop the car, stop at pit exit.')
        print('Just pull over to the side.')


if __name__ == '__main__':
    merloID = int(input("Position Merlo FX, press 999 if not present:"))
    boomshootID = int(input("Position Boomshoot, press 999 if not present:"))
    sambovID = int(input("Position Sambov, press 999 if not present:"))
    N_players = int(input("Number of players:"))
    N_laps = int(input("Number of laps:"))

    merlofx = {"Car_ID": merloID, "lap_time_in_ms": [], "sector1_time_in_ms": [], "sector2_time_in_ms": [],
               "sector3_time_in_ms": [], "Tyre": [], "TyreAge": [], "lap" : 0, "fuel": [], "floatLap" : [], "ers_energy": [], "name" : "merlofx", "EndTyre" : 0, "FrontDamage" : [], "RearDamage" : []}
    boomshoot = {"Car_ID": boomshootID, "lap_time_in_ms": [], "sector1_time_in_ms": [], "sector2_time_in_ms": [],
                 "sector3_time_in_ms": [], "Tyre": [], "TyreAge": [], "lap" : 0, "fuel": [], "floatLap" : [], "ers_energy": [], "name":"boomshoot", "EndTyre": 0, "FrontDamage" : [], "RearDamage" : []}
    sambov = {"Car_ID": sambovID, "lap_time_in_ms": [], "sector1_time_in_ms": [], "sector2_time_in_ms": [],
              "sector3_time_in_ms": [], "Tyre": [], "TyreAge": [], "lap" : 0, "fuel": [], "floatLap" : [], "ers_energy": [], "name":"sambov", "EndTyre": 0, "FrontDamage" : [], "RearDamage" : []}

    lista_giocatori = [merlofx, boomshoot, sambov]

    dati(merlofx, boomshoot, sambov, N_players)

    print(merlofx)
    print(boomshoot)
    print(sambov)

    giri = []
    for i in range(1, (N_laps + 1)):
        giri.append(i)


    fig1, ax1 = grafico.subplots()
    fig2, ax2 = grafico.subplots()
    fig3, ax3 = grafico.subplots()
    fig4, ax4 = grafico.subplots()

    ax1.set_title("LAP TIME", fontsize=24)
    ax1.set_xlabel("N giro", fontsize=14)
    ax1.set_ylabel("time", fontsize=14)

    boomshootmanc = N_laps - len(boomshoot["lap_time_in_ms"])
    if boomshootmanc > 0:
        for i in range(boomshootmanc):
            boomshoot["lap_time_in_ms"].append(NaN)
    ax1.plot(giri, boomshoot["lap_time_in_ms"], label="boomshoot", linewidth=3)

    merlomanc = N_laps - len(merlofx["lap_time_in_ms"])
    if merlomanc > 0:
        for i in range(merlomanc):
            merlofx["lap_time_in_ms"].append(NaN)
    ax1.plot(giri, merlofx["lap_time_in_ms"], label="merlofx", linewidth=3)

    sambovmanc = N_laps - len(sambov["lap_time_in_ms"])
    if sambovmanc > 0:
        for i in range(sambovmanc):
            sambov["lap_time_in_ms"].append(NaN)
    ax1.plot(giri, sambov["lap_time_in_ms"], label="sambov", linewidth=3)

    ax1.legend()

    ax2.set_title("SECTOR 1", fontsize=24)
    ax2.set_xlabel("N giro", fontsize=14)
    ax2.set_ylabel("time", fontsize=14)


    boomshootmanc = N_laps - len(boomshoot["sector1_time_in_ms"])
    if boomshootmanc > 0:
        for i in range(boomshootmanc):
            boomshoot["sector1_time_in_ms"].append(NaN)
    ax2.plot(giri, boomshoot["sector1_time_in_ms"], label="boomshoot", linewidth=3)

    merlomanc = N_laps - len(merlofx["sector1_time_in_ms"])
    if merlomanc > 0:
        for i in range(merlomanc):
            merlofx["sector1_time_in_ms"].append(NaN)
    ax2.plot(giri, merlofx["sector1_time_in_ms"], label="merlofx", linewidth=3)

    sambovmanc = N_laps - len(sambov["sector1_time_in_ms"])
    if sambovmanc > 0:
        for i in range(sambovmanc):
            sambov["sector1_time_in_ms"].append(NaN)
    ax2.plot(giri,sambov["sector1_time_in_ms"], label="sambov", linewidth=3)

    ax2.legend()

    ax3.set_title("SECTOR 2", fontsize=24)
    ax3.set_xlabel("N giro", fontsize=14)
    ax3.set_ylabel("time", fontsize=14)


    boomshootmanc = N_laps - len(boomshoot["sector2_time_in_ms"])
    if boomshootmanc > 0:
        for i in range(boomshootmanc):
            boomshoot["sector2_time_in_ms"].append(NaN)
    ax3.plot(giri, boomshoot["sector2_time_in_ms"], label="boomshoot", linewidth=3)

    merlomanc = N_laps - len(merlofx["sector2_time_in_ms"])
    if merlomanc > 0:
        for i in range(merlomanc):
            merlofx["sector2_time_in_ms"].append(NaN)
    ax3.plot(giri, merlofx["sector2_time_in_ms"], label="merlofx", linewidth=3)


    sambovmanc = N_laps - len(sambov["sector2_time_in_ms"])
    if sambovmanc > 0:
        for i in range(sambovmanc):
            sambov["sector2_time_in_ms"].append(NaN)
    ax3.plot(giri, sambov["sector2_time_in_ms"], label="sambov", linewidth=3)


    ax3.legend()

    ax4.set_title("SECTOR 3", fontsize=24)
    ax4.set_xlabel("N giro", fontsize=14)
    ax4.set_ylabel("time", fontsize=14)


    boomshootmanc = N_laps - len(boomshoot["sector3_time_in_ms"])
    if boomshootmanc > 0:
        for i in range(boomshootmanc):
            boomshoot["sector3_time_in_ms"].append(NaN)
    ax4.plot(giri, boomshoot["sector3_time_in_ms"], label="boomshoot", linewidth=3)

    merlomanc = N_laps - len(merlofx["sector3_time_in_ms"])
    if merlomanc > 0:
        for i in range(merlomanc):
            merlofx["sector3_time_in_ms"].append(NaN)
    ax4.plot(giri, merlofx["sector3_time_in_ms"], label="merlofx", linewidth=3)

    sambovmanc = N_laps - len(sambov["sector3_time_in_ms"])
    if sambovmanc > 0:
        for i in range(sambovmanc):
            sambov["sector3_time_in_ms"].append(NaN)
    ax4.plot(giri, sambov["sector3_time_in_ms"], label="sambov", linewidth=3)

    ax4.legend()

    ############################################

    for giocatore in lista_giocatori:
        for idx, ele in enumerate(giocatore["Tyre"]):
            if idx != 0 and ele != giocatore["Tyre"][idx - 1]:
                giocatore["Tyre"][idx - 1] = ele

    for giocatore in lista_giocatori:
        try:
            giocatore["Tyre"][- 1] = giocatore["EndTyre"]
        except:
            print()

    gomme, axgomme = grafico.subplots()

    axgomme.set_title("TYRE", fontsize=24)
    axgomme.set_xlabel("N giro", fontsize=14)
    axgomme.set_ylabel("Player", fontsize=14)

    giri1 = []
    for i in range(0, (N_laps)):
        giri1.append(i)

    for idx, i in enumerate(boomshoot["Tyre"]):
        if len(boomshoot["Tyre"]) - 1 != idx:
            if i == 16:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], boomshoot["Car_ID"] + 1), color='red', linewidth=3, label = "boomshoot")
            elif i == 17:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], boomshoot["Car_ID"] + 1), color='yellow', linewidth=3, label = "boomshoot")
            elif i == 18:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], boomshoot["Car_ID"] + 1), color='white',linewidth=3, label = "boomshoot")
            elif i == 7:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], boomshoot["Car_ID"] + 1), color='green', linewidth=3, label = "boomshoot")
            elif i == 8:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], boomshoot["Car_ID"] + 1), color='blue', linewidth=3, label = "boomshoot")
        else:
            if i == 16:
                axgomme.plot([idx, idx + 1], [boomshoot["Car_ID"] + 1, boomshoot["Car_ID"] + 1], color='red', linewidth=3, label = "boomshoot")
            elif i == 17:
                axgomme.plot([idx, idx + 1], [boomshoot["Car_ID"] + 1, boomshoot["Car_ID"] + 1], color='yellow', linewidth=3, label = "boomshoot")
            elif i == 18:
                axgomme.plot([idx, idx + 1], [boomshoot["Car_ID"] + 1, boomshoot["Car_ID"] + 1], color='white',linewidth=3, label = "boomshoot")
            elif i == 7:
                axgomme.plot([idx, idx + 1], [boomshoot["Car_ID"] + 1, boomshoot["Car_ID"] + 1], color='green', linewidth=3, label = "boomshoot")
            elif i == 8:
                axgomme.plot([idx, idx + 1], [boomshoot["Car_ID"] + 1, boomshoot["Car_ID"] + 1], color='blue', linewidth=3, label = "boomshoot")


    for idx, i in enumerate(merlofx["Tyre"]):
        if len(merlofx["Tyre"]) - 1 != idx:
            if i == 16:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], merlofx["Car_ID"] + 1), color='red', linewidth=3, label = "merlofx")
            elif i == 17:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], merlofx["Car_ID"] + 1), color='yellow', linewidth=3, label = "merlofx")
            elif i == 18:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], merlofx["Car_ID"] + 1), color='white',linewidth=3, label = "merlofx")
            elif i == 7:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], merlofx["Car_ID"] + 1), color='green', linewidth=3, label = "merlofx")
            elif i == 8:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], merlofx["Car_ID"] + 1), color='blue', linewidth=3, label = "merlofx")
        else:
            if i == 16:
                axgomme.plot([idx, idx + 1], [merlofx["Car_ID"] + 1, merlofx["Car_ID"] + 1], color='red', linewidth=3, label = "merlofx")
            elif i == 17:
                axgomme.plot([idx, idx + 1], [merlofx["Car_ID"] + 1, merlofx["Car_ID"] + 1], color='yellow', linewidth=3, label = "merlofx")
            elif i == 18:
                axgomme.plot([idx, idx + 1], [merlofx["Car_ID"] + 1, merlofx["Car_ID"] + 1], color='white',linewidth=3, label = "merlofx")
            elif i == 7:
                axgomme.plot([idx, idx + 1], [merlofx["Car_ID"] + 1, merlofx["Car_ID"] + 1], color='green', linewidth=3, label = "merlofx")
            elif i == 8:
                axgomme.plot([idx, idx + 1], [merlofx["Car_ID"] + 1, merlofx["Car_ID"] + 1], color='blue', linewidth=3, label = "merlofx")



    for idx, i in enumerate(sambov["Tyre"]):
        if len(sambov["Tyre"]) - 1 != idx:
            if i == 16:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], sambov["Car_ID"] + 1), color='red', linewidth=3, label = "sambov")
            elif i == 17:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], sambov["Car_ID"] + 1), color='yellow', linewidth=3, label = "sambov")
            elif i == 18:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], sambov["Car_ID"] + 1), color='white',linewidth=3, label = "sambov")
            elif i == 7:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], sambov["Car_ID"] + 1), color='green', linewidth=3, label = "sambov")
            elif i == 8:
                axgomme.plot(giri1[idx:idx + 2], np.full_like(giri1[idx:idx + 2], sambov["Car_ID"] + 1), color='blue', linewidth=3, label = "sambov")
        else:
            if i == 16:
                axgomme.plot([idx, idx + 1], [sambov["Car_ID"] + 1, sambov["Car_ID"] + 1], color='red', linewidth=3, label = "sambov")
            elif i == 17:
                axgomme.plot([idx, idx + 1], [sambov["Car_ID"] + 1, sambov["Car_ID"] + 1], color='yellow', linewidth=3, label = "sambov")
            elif i == 18:
                axgomme.plot([idx, idx + 1], [sambov["Car_ID"] + 1, sambov["Car_ID"] + 1], color='white',linewidth=3, label = "sambov")
            elif i == 7:
                axgomme.plot([idx, idx + 1], [sambov["Car_ID"] + 1, sambov["Car_ID"] + 1], color='green', linewidth=3, label = "sambov")
            elif i == 8:
                axgomme.plot([idx, idx + 1], [sambov["Car_ID"] + 1, sambov["Car_ID"] + 1], color='blue', linewidth=3, label = "sambov")
    car_id = []
    nomi = []
    for diz in lista_giocatori:
        if diz["Tyre"]:
            car_id.append(diz["Car_ID"] + 1)
            nomi.append(diz["name"])

    axgomme.set_yticks(car_id)
    axgomme.set_yticklabels(nomi)

    ############################################

    fuel, axfuel = grafico.subplots()

    axfuel.set_title("FUEL", fontsize=24)
    axfuel.set_xlabel("lap", fontsize=14)
    axfuel.set_ylabel("fuel(Kg)", fontsize=14)

    lenFloatLap = int(N_laps / 0.1)

    boomshootmanc1 = lenFloatLap - len(boomshoot["floatLap"])

    if boomshootmanc1 > 0:
        for i in range(boomshootmanc1):
            boomshoot["floatLap"].append(NaN)
            boomshoot["fuel"].append(NaN)

    axfuel.plot(boomshoot["floatLap"], boomshoot["fuel"], label="boomshoot", linewidth=3)

    merlomanc1 = lenFloatLap - len(merlofx["floatLap"])

    if merlomanc1 > 0:
        for i in range(merlomanc1):
            merlofx["floatLap"].append(NaN)
            merlofx["fuel"].append(NaN)

    axfuel.plot(merlofx["floatLap"], merlofx["fuel"], label="merlofx", linewidth=3)

    sambovmanc1 = lenFloatLap - len(sambov["floatLap"])

    if sambovmanc1 > 0:
        for i in range(sambovmanc1):
            sambov["floatLap"].append(NaN)
            sambov["fuel"].append(NaN)

    axfuel.plot(sambov["floatLap"], sambov["fuel"], label="sambov", linewidth=3)

    axfuel.legend()

    ############################################

    ers, axers = grafico.subplots()

    axers.set_title("ERS", fontsize=24)
    axers.set_xlabel("lap", fontsize=14)
    axers.set_ylabel("ers(Joule)", fontsize=14)

    ers_capacity = merlofx["ers_energy"][0]

    for giocatore in lista_giocatori:
        for i,j in giocatore.items():
            if i == "ers_energy":
                for k in j:
                    giocatore["ers_energy"][j.index(k)] = (k/ers_capacity) * 100

    boomshootmanc1 = lenFloatLap - len(boomshoot["ers_energy"])

    if boomshootmanc1 > 0:
        for i in range(boomshootmanc1):
            boomshoot["ers_energy"].append(NaN)

    axers.plot(boomshoot["floatLap"], boomshoot["ers_energy"], label="boomshoot", linewidth=3)

    merlomanc1 = lenFloatLap - len(merlofx["ers_energy"])

    if merlomanc1 > 0:
        for i in range(merlomanc1):
            merlofx["ers_energy"].append(NaN)

    axers.plot(merlofx["floatLap"], merlofx["ers_energy"], label="merlofx", linewidth=3)

    sambovmanc1 = lenFloatLap - len(sambov["ers_energy"])

    if sambovmanc1 > 0:
        for i in range(sambovmanc1):
            sambov["ers_energy"].append(NaN)

    axers.plot(sambov["floatLap"], sambov["ers_energy"], label="sambov", linewidth=3)

    axers.legend()

    ############################################

    FrontDamage, axfront = grafico.subplots()

    axfront.set_title("FRONT TYRE DAMAGE", fontsize=24)
    axfront.set_xlabel("lap", fontsize=14)
    axfront.set_ylabel("damage(%)", fontsize=14)

    boomshootmanc1 = lenFloatLap - len(boomshoot["FrontDamage"])

    if boomshootmanc1 > 0:
        for i in range(boomshootmanc1):
            boomshoot["FrontDamage"].append(NaN)

    axfront.plot(boomshoot["floatLap"], boomshoot["FrontDamage"], label="boomshoot", linewidth=3)

    merlomanc1 = lenFloatLap - len(merlofx["FrontDamage"])

    if merlomanc1 > 0:
        for i in range(merlomanc1):
            merlofx["FrontDamage"].append(NaN)

    axfront.plot(merlofx["floatLap"], merlofx["FrontDamage"], label="merlofx", linewidth=3)

    sambovmanc1 = lenFloatLap - len(sambov["FrontDamage"])

    if sambovmanc1 > 0:
        for i in range(sambovmanc1):
            sambov["FrontDamage"].append(NaN)

    axfront.plot(sambov["floatLap"], sambov["FrontDamage"], label="sambov", linewidth=3)

    axfront.legend()

    ############################################

    RearDamage, axrear = grafico.subplots()

    axrear.set_title("REAR TYRE DAMAGE", fontsize=24)
    axrear.set_xlabel("lap", fontsize=14)
    axrear.set_ylabel("damage(%)", fontsize=14)

    boomshootmanc1 = lenFloatLap - len(boomshoot["RearDamage"])

    if boomshootmanc1 > 0:
        for i in range(boomshootmanc1):
            boomshoot["RearDamage"].append(NaN)

    axrear.plot(boomshoot["floatLap"], boomshoot["RearDamage"], label="boomshoot", linewidth=3)

    merlomanc1 = lenFloatLap - len(merlofx["RearDamage"])

    if merlomanc1 > 0:
        for i in range(merlomanc1):
            merlofx["RearDamage"].append(NaN)

    axrear.plot(merlofx["floatLap"], merlofx["RearDamage"], label="merlofx", linewidth=3)

    sambovmanc1 = lenFloatLap - len(sambov["RearDamage"])

    if sambovmanc1 > 0:
        for i in range(sambovmanc1):
            sambov["RearDamage"].append(NaN)

    axrear.plot(sambov["floatLap"], sambov["RearDamage"], label="sambov", linewidth=3)

    axrear.legend()

    ############################################

    grafico.show()