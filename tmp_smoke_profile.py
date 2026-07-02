from services.profile_service import ProfileService

if __name__ == '__main__':
    ps = ProfileService()
    try:
        res = ps.process_profile({'username': 'deandriani_', 'id': None})
        print('RESULT:', res)
    finally:
        ps.shutdown()
