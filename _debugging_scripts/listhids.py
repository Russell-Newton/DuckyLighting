# import hid
from keyboards import Enumeration

DUCKY_ONE_2_VID = 0x04d9
DUCKY_ONE_2_PID = 0x0348
DUCKY_ONE_2_USAGE = 1
DUCKY_ONE_2_USAGE_PAGE = 0xff00

if __name__ == '__main__':
    # hid.hid_init()
    # for device in hid.hid_enumerate(vendor_id=DUCKY_ONE_2_VID, product_id=DUCKY_ONE_2_PID):
    #     info = f"Device: vid/pid: {device.vendor_id}/{device.product_id}\n" \
    #            f"  path:          {device.path}\n" \
    #            f"  serial_number: {device.serial_number}\n" \
    #            f"  usage_page:    {device.usage_page}\n" \
    #            f"  usage:         {device.usage}\n" \
    #            f"  Manufacturer:  {device.manufacturer_string}\n" \
    #            f"  Product:       {device.product_string}"
    #     print(info)

    # for device in hid.enumerate(vid=DUCKY_ONE_2_VID, pid=DUCKY_ONE_2_PID):
    #     info = f"Device: vid/pid: {device['vendor_id']}/{device['product_id']}\n" \
    #            f"  path:          {device['path']}\n" \
    #            f"  serial_number: {device['serial_number']}\n" \
    #            f"  usage_page:    {device['usage_page']}\n" \
    #            f"  usage:         {device['usage']}\n" \
    #            f"  Manufacturer:  {device['manufacturer_string']}\n" \
    #            f"  Product:       {device['product_string']}"
    #     print(info)
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