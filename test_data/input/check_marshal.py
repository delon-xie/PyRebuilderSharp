import struct

for ver in ['3.5', '3.6', '3.7', '3.8', '3.9', '3.10']:
    path = f'/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc'
    data = open(path, 'rb').read()
    
    # Determine header size
    if ver in ('2.7',):
        hdr = 8
    elif ver in ('3.5', '3.6'):
        hdr = 12
    else:
        hdr = 16
    
    # Marshal starts here
    pos = hdr
    type_byte = data[pos]
    actual_type = type_byte & 0x7f
    has_ref = (type_byte & 0x80) != 0
    
    print(f'{ver}: header={hdr}, marshal_at={pos}, type={type_byte:#x} (type={actual_type:#x}, has_ref={has_ref})')
    
    if has_ref:
        ref_idx = struct.unpack('<I', data[pos+1:pos+5])[0]
        fields_start = pos + 5
        print(f'  ref_index={ref_idx} at {pos+1}-{pos+4}')
        print(f'  fields_at={fields_start}')
        
        argcount = struct.unpack('<I', data[fields_start:fields_start+4])[0]
        print(f'  argcount={argcount}')
        
        # Check if 3.8+ has posOnlyArgCount
        posOnly = struct.unpack('<I', data[fields_start+4:fields_start+8])[0]
        if ver >= '3.8':
            print(f'  posOnlyArgCount={posOnly}')
            nlocals = struct.unpack('<I', data[fields_start+12:fields_start+16])[0]
        else:
            nlocals = struct.unpack('<I', data[fields_start+4:fields_start+8])[0]
        print(f'  nlocals={nlocals}')
    else:
        print(f'  No FLAG_REF')
        fields_start = pos + 1
        print(f'  fields_at={fields_start}')
        argcount = struct.unpack('<I', data[fields_start:fields_start+4])[0]
        print(f'  argcount={argcount}')

    print()
