import sys
sys.path.insert(0, '.')

try:
    from app.models import Message
    print('SUCCESS: Message model imported successfully')
except Exception as e:
    import traceback
    print(f'ERROR: {e}')
    traceback.print_exc()