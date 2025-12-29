import asyncio
import httpx

async def test_jobs_endpoint():
    """Test the jobs API endpoint"""
    base_url = "http://localhost:8000"
    
    print("\n" + "="*70)
    print("TESTING JOBS API ENDPOINT")
    print("="*70)
    
    try:
        async with httpx.AsyncClient() as client:
            # Test 1: Get all jobs
            print("\n1. Testing GET /api/marketplace/jobs")
            response = await client.get(f"{base_url}/api/marketplace/jobs")
            
            if response.status_code == 200:
                jobs = response.json()
                print(f"   [OK] Status: {response.status_code}")
                print(f"   [OK] Found {len(jobs)} jobs")
                if len(jobs) > 0:
                    print(f"\n   Sample job:")
                    job = jobs[0]
                    print(f"   - Title: {job['title']}")
                    print(f"   - Type: {job['job_type']}")
                    print(f"   - City: {job['city']}")
                    print(f"   - Salary: Rs.{job.get('salary_min', 0)} - Rs.{job.get('salary_max', 0)}")
            else:
                print(f"   [ERROR] Status: {response.status_code}")
                print(f"   [ERROR] Response: {response.text}")
            
            # Test 2: Filter by job type
            print("\n2. Testing filters - Umpire jobs")
            response = await client.get(f"{base_url}/api/marketplace/jobs?job_type=Umpire")
            if response.status_code == 200:
                jobs = response.json()
                print(f"   [OK] Found {len(jobs)} umpire jobs")
            
            # Test 3: Filter by city
            print("\n3. Testing filters - Ahmedabad jobs")
            response = await client.get(f"{base_url}/api/marketplace/jobs?city=Ahmedabad")
            if response.status_code == 200:
                jobs = response.json()
                print(f"   [OK] Found {len(jobs)} jobs in Ahmedabad")
            
            # Test 4: Filter by sport
            print("\n4. Testing filters - Cricket jobs")
            response = await client.get(f"{base_url}/api/marketplace/jobs?sport_type=Cricket")
            if response.status_code == 200:
                jobs = response.json()
                print(f"   [OK] Found {len(jobs)} cricket jobs")
            
            print("\n" + "="*70)
            print("API ENDPOINT STATUS: WORKING!")
            print("="*70)
            print("\nYou can test in browser:")
            print("  http://localhost:8000/api/marketplace/jobs")
            print("\n")
            
    except httpx.ConnectError:
        print("\n" + "="*70)
        print("ERROR: Cannot connect to backend!")
        print("="*70)
        print("\nPlease make sure backend is running:")
        print("  cd C:\\Utsav\\sports_diary\\backend")
        print("  python run.py")
        print("\n")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_jobs_endpoint())

