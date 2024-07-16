from datetime import datetime, timedelta

def get_statut(date_echeance, date_ctrl):
    # Convert string dates to datetime objects if they are not None
    if date_echeance:
        date_echeance = datetime.strptime(str(date_echeance), "%Y-%m-%d")
    if date_ctrl:
        date_ctrl = datetime.strptime(str(date_ctrl), "%Y-%m-%d")

    # Calculate the status based on the criteria
    if date_ctrl:
        return 'Controlé'
    elif date_echeance and (date_echeance - datetime.today()).days <= 30:
        return 'Urgent'
    else:
        return 'Non Controlé'
