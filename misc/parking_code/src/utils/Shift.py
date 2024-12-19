
import time
import datetime


def determineEnforcers( toForce, sendForce ):
    now = time.time()
    hr = float(time.strftime('%H'))
    dow = datetime.datetime.today().weekday()
    
    for i, enforcer  in enumerate(toForce):
    
        onShift = False
        if dow in enforcer['workdays']:
            shift = enforcer['shift']

            # TODO: fix for people who work more than
            #       12 hours overnight
            if shift[0] < shift[1]:
                # Day shift
                onShift = shift[0] < hr and shift[1] > hr
            else:
                # Night shift
                if hr > 12 and shift[0] > 12:
                    # Noon to midnight
                    onShift = hr > shift[0]
                else:
                    # Midnight to noon
                    onShift = hr < shift[1]
        
        if onShift:
            sendForce.append(enforcer['contact'])

