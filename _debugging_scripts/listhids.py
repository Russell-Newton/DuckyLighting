try:
    from keyboards import Enumeration
except ModuleNotFoundError:
    import sys
    from os.path import abspath, dirname
    sys.path.append(dirname(dirname(abspath(__file__))))
    print(sys.path)
    from keyboards import Enumeration

VID = 0x04d9
PID = 0

if __name__ == '__main__':
    devices = Enumeration(vid=VID, pid=PID)
    for device in devices.find():
        device.open()
        info = f"Device: vid/pid: {device.vendor_id}/{device.product_id}\n" \
               f"  path:          {device.path}\n" \
               f"  serial_number: {device.serial_number}\n" \
               f"  usage_page:    {device.usage_page}\n" \
               f"  usage:         {device.usage}\n" \
               f"  Manufacturer:  {device.manufacturer_string}\n" \
               f"  Product:       {device.product_string}"
        print(info)
        device.close()