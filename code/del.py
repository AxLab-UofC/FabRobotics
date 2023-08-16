from bluepy import btle
import bluepy
from Constants import toioADDR

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'


# Initialisation  -------
toio_addr = toioADDR[53]
p = btle.Peripheral(toio_addr)
p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
#   svc = p.getServiceByUUID( service_uuid )
#   ch = svc.getCharacteristics( char_uuid )[0]
#   ch.write( setup_data )

# Main loop --------

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print "Waiting..."
    # Perhaps do something else here