try:
    from keyboards import Enumeration
except ModuleNotFoundError:
    import sys
    from os.path import abspath, dirname
    sys.path.append(dirname(dirname(abspath(__file__))))
    print(sys.path)
    from keyboards import Enumeration

DUCKY_ONE_2_VID = 0x04d9
DUCKY_ONE_2_PID = 0x0348

if __name__ == '__main__':
    devices = Enumeration(vid=DUCKY_ONE_2_VID, pid=DUCKY_ONE_2_PID)
    for device in devices.find():
        device.open()
        info = f"Device: vid/pid: {device.vendor_id}/{device.product_id}\n" \
               f"  path:          {device.path}\n" \
               f"  serial_number: {device.serial_number}\n" \
               f"  usage_page:    {device.usage_page}\n" \
               f"  usage:         {device.usage}\n" \
               f"  Manufacturer:  {device.manufacturer_string}\n" \
               f"  Product:       {device.product_string}"
        print(device, info)
        device.close()