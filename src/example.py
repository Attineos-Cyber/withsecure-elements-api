import os
from statistics import mean

import withsecure
from withsecure.enums import IncidentStatus

client_id = os.environ.get('WS_CLIENT_ID')
secret_id = os.environ.get('WS_SECRET_ID')

if __name__ == "__main__":
    client = withsecure.Client(client_id, secret_id)
    client.authenticate()

    searchdate = "2025-01-01T00:00:00Z"
    resolution_type = ('unconfirmed', 'confirmed', 'falsePositive')
    status_type = ('new', 'acknowledged', 'inProgress', 'monitoring', 'closed', 'waitingForCustomer')

    incidents = client.get_incident_list(start_time=searchdate, status=status_type, resolution=resolution_type, limit=5)
    print("Nombre d'incident depuis le début de l'année : %s" % len(incidents))

    close_time_dt = []

    for incident in incidents:
        start_dt = incident.created_timestamp.strftime('%Y:%m:%d - %H:%M:%S')
        end_dt = incident.updated_timestamp.strftime('%Y:%m:%d - %H:%M:%S') if incident.status == IncidentStatus.Closed else None
        diff_dt = (incident.updated_timestamp - incident.created_timestamp).total_seconds() if end_dt else 0


        if diff_dt != 0:
            close_time_dt.append(diff_dt)

        print("%s\t%s\t(%s min) - %s" % (start_dt, end_dt, diff_dt, incident.id))

    mean_time = mean(close_time_dt)
    hours = mean_time // 3600
    minutes = (mean_time % 3600) // 60
    print("Temps moyen de résolution (en minutes): %dh %dm" % (hours, minutes))