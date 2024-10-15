
import os, sys
import time

import html_ops as ho

def write( spots, site_dir=None, dev_mode=False ):
    
    if site_dir is None:
        site_dir = os.getcwd()

    # Get/Write out the current time for easy comparison
    currentTime = time.asctime()
    
    # Put the data in a table
    tabHtml = """
    <html>
        <head>
            <meta http-equiv="refresh" content="60" />
            <title>Lot Status</title>
            <script type="text/javascript" src="sorttable.js">
            </script>
            <style type="text/css">
            th, td {
              padding: 3px !important;
            }

            /* Sortable tables */
            table.sortable thead {
                background-color: #333;
                color: #cccccc;
                font-weight: bold;
                cursor: default;
            }
            th {
              font-size: 100%;
            }
            </style>
        </head>
        <table border="1" class="sortable">"""


    tabHtml += ("<tr><th>Space Number</th>"
                    "<th>Occupied</th>"
                    "<th>Time Present</th>"
                    "<th>Paid</th>"
                    "<th>Current Time</th>"
                    "<th>Paid Start Time</th>"
                    "<th>Paid End Time</th>"
                    "<th>License Number</th>"
                    "<th>License State</th>"
                    "<th>Monthly</th>"
                    "<th>Occupation Start Time</th>"
                    "<th>Occupation End Time</th>"
                "</tr>")

    n_remaining = len(spots)
    
    # Make a separate table like normal, with paids only
    ptabHtml = tabHtml

    for s in spots:
        spot = spots[s]
        
        # Occupied once past presence threshold
        # -- Can be occupied and not paid for
        # -- duration of 'freeTime' or 'violationThresh'
        # -- before marked as violating.
        # -- Which is NOT what we want to indicate when
        # -- presenting the number of spots available
        occupied = spot.occupied
        deduct = occupied or spot.monthly
        deduct = deduct or spot.faultyCamera
        deduct = deduct or spot.handicap

        n_remaining -= deduct
        
        # Default row to white
        rcolor = '#FFFFFF'

        # Black out if camera is failed
        if spot.faultyCamera or spot.paid == -1000:
            rcolor = '#808080'

        if spot.violation:
            rcolor = '#FF0000'
        elif spot.failedDetection:
            rcolor = '#FF7F00'
        elif spot.monthly:
            rcolor = '#0000FF'
        elif spot.paid == 1:
            rcolor = '#00FF00'
        elif spot.paid == -1:
            rcolor = '#FC0FC0'
        elif spot.paid == -2:
            rcolor = '#8B4513'
        elif spot.handicap:
            rcolor = '#FFFF00'

        rowsty = 'style="background-color:%s"' % rcolor
        row = '<tr %s>' % rowsty
        spaceText = 'Space ' + str(s)
        imname = 'imgs/spot%d.jpg' % spot.number
        linkText = '<a href="' + imname + '">' + spaceText + '</a>'
        spaceCell = '<td>' + linkText + '</td>'
        occCell = '<td> ' + str(occupied) + '</td>'
        presCell = '<td> ' + str(spot.tPresent) + '</td>'
        paidCell = '<td> ' + str(spot.paid) + '</td>'
        currentTimeCell = '<td> ' + currentTime + '</td>'
        if spot.payStartTime:
            pst_lt = time.localtime(spot.payStartTime)
            pst_str = time.asctime(pst_lt)
        else:
            pst_str = ''
        if spot.payEndTime:
            pet_lt = time.localtime(spot.payEndTime)
            pet_str = time.asctime(pet_lt)
        else:
            pet_str = ''
        pstCell = '<td> ' + pst_str + '</td>'
        petCell = '<td> ' + pet_str + '</td>'
        lpnCell = '<td> ' + str(spot.lpn) + '</td>'
        lpsCell = '<td> ' + str(spot.lps) + '</td>'
        mnthCell = '<td> ' + str(spot.monthly) + '</td>'
        ost_lt = time.localtime(spot.occupationStartTime)
        oet_lt = time.localtime(spot.occupationEndTime)
        ostCell = '<td> ' + time.asctime(ost_lt) + '</td>'
        oetCell = '<td> ' + time.asctime(oet_lt) + '</td>'
        row += spaceCell 
        row = row + occCell + presCell + paidCell
        row = row + currentTimeCell + pstCell + petCell
        row = row + lpnCell + lpsCell
        row += mnthCell
        row = row + ostCell + oetCell
        row += '</tr>'
        tabHtml += row
        

        ### PAID TABLE
        
        # Only show paid or violators on paid table
        showMe = spot.paid == 1 or spot.violation
        
        # Don't show monthlies on paid table
        dontShowMe = spot.monthly

        # If the Payment API is broken, blow up the paid page
        if spot.paid < 0:
            showMe = True
            donShowMe = False

        # Only populate subtable with what's certain cases
        if showMe and not dontShowMe:
            ptabHtml += row

    
    endHtml = """
        </table>
    </html>"""

    tabHtml += endHtml
    ptabHtml += endHtml
    
    with open('table.html','w') as f:
        f.write(tabHtml)
    with open('paidTable.html','w') as f:
        f.write(ptabHtml)
    
    nHtml = """\
            <div>
              <font size="7">
              %d
              </font>
            </div>
            """ % n_remaining 

    ho.write_page( 'n_avail.html', 'Available Spots', 30, nHtml )
    
    if not dev_mode:
        target = os.path.join(site_dir,'newtable/index.html')
        os.rename("table.html",target)
        target = os.path.join(site_dir,'whospaid/index.html')
        os.rename("paidTable.html",target)
        target = os.path.join(site_dir,'n_spots_available/index.html')
        os.rename("n_avail.html",target)
    else:
        print 'WARNING: html products not going to served site location!'


    return

