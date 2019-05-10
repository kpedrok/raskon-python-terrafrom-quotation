json_data = [{
    "queue": "RANKED_SOLO_5x5",
    "name": "Riven's Cutthroats",
    "entries": [
        {
            "leaguePoints": 812,
            "isFreshBlood": False,
            "isHotStreak": False,
            "division": "I",
            "isInactive": False,
            "isVeteran": False,
            "losses": 277,
            "playerOrTeamName": "CLG Bunso",
            "playerOrTeamId": "19732914",
            "wins": 356
        },
        {
            "leaguePoints": 567,
            "isFreshBlood": False,
            "isHotStreak": False,
            "division": "I",
            "isInactive": False,
            "isVeteran": False,
            "losses": 56,
            "playerOrTeamName": "SKT Frost",
            "playerOrTeamId": "66401633",
            "wins": 160
        },
    ]}]

# print(json_data)
# print(json_data[0]["entries"])
sorted(json_data[0]["entries"], key=lambda d: d["leaguePoints"])
a = sorted(json_data[0]["entries"], key=lambda d: d["leaguePoints"])
print(a)