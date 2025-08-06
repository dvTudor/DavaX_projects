def generate_report(data: dict):
    high_scorers = []
    for key in data:
        if data[key] >= 80:
            high_scorers.append(key + '-' + str(data[key]))
    high_scorers.sort(key=lambda score: -int(score.split('-')[1]))
    return high_scorers