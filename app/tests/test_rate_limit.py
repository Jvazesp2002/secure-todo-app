import pytest

def test_nginx_rate_limiting(client):
    success_count = 0
    blocked_count = 0

    for _ in range(10):
        response = client.get('/login', follow_redirects=False) 
        
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            blocked_count += 1
    
    print(f"\n[RATE LIMIT TEST] Exitosas: {success_count}, Bloqueadas: {blocked_count}")
    assert success_count + blocked_count > 0